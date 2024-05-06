#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Face: Utility Functions. """

# system global imports
from __future__ import print_function, division, absolute_import

# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import os
# mca python imports
from mca.common import log
from mca.common.paths import paths
from mca.common.textio import jsonio
from mca.mya.face import source_data
from mca.mya.modeling import blendshape_model, face_model, rivets
from mca.mya.utils import namespace, display_layers, fbx_utils, naming, groups, attr_utils
from mca.mya.rigging import mesh_markup_rig, chain_markup
from mca.mya.rigging.flags import flag_utils
from mca.mya.rigging import frag, rig_utils, skel_utils
from mca.mya.face.face_utils import face_skinning
from mca.mya.deformations import skin_utils

logger = log.MCA_LOGGER

def get_source_face_data_path(asset_id):
    """
    Returns the path to the source data file.

    :param string asset_id: The str asset id for the asset.
    :return: Returns the path to the source data file.
    :rtype: str
    """

    return os.path.join(paths.get_face_data_path(asset_id), source_data.FACE_FILE_NAME)


def get_source_face_data(asset_id):
    """
    Returns an instance of SourceFaceData for a specific mesh.

    :param string asset_id: The str asset id for the asset.
    :return: Returns an instance of FaceMeshRegionData for a specific mesh.
    :rtype: SourceFaceData
    """

    face_data_path = get_source_face_data_path(asset_id=asset_id)
    src_data = source_data.SourceFaceData.load(face_data_path)
    return src_data


def set_common_flag_positions(mesh, wrapped_root):
    """
    Sets null joint positions for face based on common UV data

    :param pm.nt.Transform mesh: Face mesh being rigged
    :param ChainMarkup wrapped_root: Wrapped root joint for face rig
    """
    # Get positions which are in a dict containing left null joint names as keys and UV coordinates as values
    info_dict = get_common_face_data().flag_positions
    if not info_dict:
        return
    for jnt, uv_data in info_dict.items():
        if pm.objExists(jnt):
            jnt = pm.PyNode(jnt)
            # Move joint to UV
            locator = pm.spaceLocator(n=f'{jnt}_locator_temp')
            pin = rivets.create_uv_pin(mesh, locator, uv=uv_data)
            pm.delete(pm.pointConstraint(locator, jnt, mo=False))
            current = jnt.ty.get()
            jnt.ty.set(current-1)
            wrapped_joint = chain_markup.JointMarkup(jnt)
            # Mirror position to right side
            if wrapped_joint.side == 'left':
                skel_region = wrapped_joint.region
                right_side_jnt = wrapped_root.get_start(skel_region, 'right')
                if right_side_jnt:
                    jnt_translate = jnt.getTranslation(space='world')
                    mirror_translate = pm.datatypes.Vector(-jnt_translate.x, jnt_translate.y, jnt_translate.z)
                    right_side_jnt.setTranslation(mirror_translate, space='world')
            # Make sure center is centered
            elif wrapped_joint.side == 'center':
                jnt.tz.set(0.0)
            pm.delete(pin)
            pm.delete(locator)

def get_common_face_data():
    """
    Returns an instance of SourceFaceData based on common data.

    :return: Returns an instance of FaceMeshRegionData.
    :rtype: SourceFaceData
    """

    face_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
    src_data = source_data.SourceFaceData.load(face_data_path)
    return src_data


def get_common_face_region_data(region_name):
    """
    Returns an instance of FaceMeshRegionData.


    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    :return: Returns an instance of FaceMeshRegionData for a specific mesh.
    :rtype: FaceMeshRegionData
    """

    face_data_path = os.path.join(paths.get_common_face(), 'rig_source_data.json')
    region_data = source_data.FaceMeshRegionData.load(face_data_path, region_name)
    return region_data


def get_face_region_data(asset_id, region_name):
    """
    Returns an instance of FaceMeshRegionData for a specific mesh.


    :param string asset_id: The str asset id for the asset.
    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    :return: Returns an instance of FaceMeshRegionData for a specific mesh.
    :rtype: FaceMeshRegionData
    """

    face_data_path = get_source_face_data_path(asset_id=asset_id)
    region_data = source_data.FaceMeshRegionData.load(face_data_path, region_name)
    return region_data


def get_parameters_region_instance(asset_id, region_name):
    """
    Returns an instance of ParameterData based on the parameters dictionary.

    :param string asset_id: The str asset id for the asset.
    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    :return: Returns an instance of ParameterData based on the parameters dictionary.
    :rtype: ParameterData
    """

    region_data = get_face_region_data(asset_id, region_name)
    return region_data.get_parameters()


def get_all_scene_blendshapes(asset_id, region_name):
    """
    Returns a list of Blend Shape Meshes in the scene.

    :param string asset_id: The str asset id for the asset.
    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    :return: A list of Blend Shape Meshes in the scene.
    :rtype: list(pm.nt.Transform)
    """

    # Returns an instance of fragParameterData based on the region
    parameters = get_parameters_region_instance(asset_id, region_name)
    pose_list = parameters.get_pose_list()

    meshes = []
    for pose in pose_list:
        if cmds.objExists(pose) and pose not in meshes:
            meshes.append(pose)
    return meshes


def duplicate_blendshape_mesh(asset_id, mesh, region_name):
    """
    Returns the blend shape version of a mesh.

    :param string asset_id: The str asset id for the asset.
    :param pm.nt.Transform mesh: The mesh that gets duplicated.
    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    :return: Returns the blend shape version of a mesh.
    :rtype: pm.nt.Transform
    """

    region_data = get_face_region_data(asset_id, region_name)

    if not region_name == region_data.region_name:
        return

    type_name = region_data.mesh_type_name
    category = region_data.mesh_category
    side = region_data.side
    mirror_type = region_data.mirror_type
    bld_mesh = blendshape_model.duplicate_mesh(mesh, f'{str(mesh)}_blendshape')

    mesh_markup_rig.MeshMarkup.create(mesh=bld_mesh,
                                        type_name=type_name,
                                        category=category,
                                        side=side,
                                        mirror_type=mirror_type,
                                        region=region_name)

    return bld_mesh


def create_all_counter_part_meshes(asset_id, hide=True):
    """
    Duplicates the skinned meshes and tags them with the blend shape data.

    :param string asset_id: The str asset id for the asset.
    :param bool hide: If true, hides the original meshes after duplicating them.
    :return: Returns a list of all duplicated meshes.
    :rtype: list(pm.nt.Transform)
    """

    # Grab the source data
    source_data_path = os.path.join(paths.get_face_data_path(asset_id), source_data.FACE_FILE_NAME)
    path_exists = os.path.exists(source_data_path)
    if not path_exists:
        source_face = get_common_face_data()
    else:
        source_face = source_data.SourceFaceData.load(source_data_path)

    # get all meshes that have markup
    rig_mesh_markup = mesh_markup_rig.RigMeshMarkup.create()

    dup_meshes = []
    # look through the data find the common mesh, duplicate it and set the markup.
    for mesh_markup in rig_mesh_markup.mesh_list:
        type_name = mesh_markup.type_name
        region_name = mesh_markup.region

        opposite_region = source_face.get_counterpart(type_name, region_name)
        if not opposite_region:
            continue
        dup_mesh = blendshape_model.duplicate_mesh(mesh_markup.mesh, f'{mesh_markup.mesh}_blendshape')
        region_data = source_data.FaceMeshRegionData(opposite_region, source_face.data)
        region_dict = region_data.get_mesh_dict()

        mesh_type_name = region_dict.get('type_name', None)
        mesh_category = region_dict.get('category', None)
        side = region_dict.get('side', None)
        mirror_type = region_dict.get('mirror_type', None)

        mesh_markup_rig.MeshMarkup.create(mesh=dup_mesh,
                                            type_name=mesh_type_name,
                                            category=mesh_category,
                                            side=side,
                                            mirror_type=mirror_type,
                                            region=opposite_region)
        if hide:
            mesh_markup.mesh.v.set(0)
        dup_meshes.append(dup_mesh)
    return dup_meshes


def get_all_scene_face_meshes(ns=''):
    """
    Returns all the face meshes in the scene.

    :param str ns:
    :return: Returns all the face meshes in the scene.
    :rtype: list(pm.nt.Transform)
    """

    all_nodes = namespace.get_all_nodes_in_namespace(ns)
    mesh_shapes = pm.ls(all_nodes, geometry=True)
    mesh_list = list(set([x.getParent() for x in mesh_shapes if x.getParent().hasAttr(mesh_markup_rig.MCA_MESH_MARKUP)]))
    return mesh_list


def has_skinning_data(mesh_name, asset_id, ext='.json'):
    path = paths.get_asset_skin_data_path(asset_id)
    if not os.path.exists(path):
        return False
    files = [x for x in os.listdir(path) if ext in x and str(mesh_name) in x]
    if files:
        return True
    return False


def get_face_rigs_from_scene():
    """
    Returns all the face FRAGRigs from the scene.

    :return: Returns all the face FRAGRigs from the scene.
    :rtype: list(FRAGRig)
    """

    all_roots = frag.get_all_frag_roots()
    all_face_roots = [x for x in all_roots if x.assetType.get() == 'head']
    all_frag_rigs = list(map(lambda x: x.get_rig(), all_face_roots))
    all_frag_rigs = list(set(all_frag_rigs))
    return all_frag_rigs


def create_pose_grp(shapes=None):
    """
    Creates and returns the pose grp or if one exists, it returns that one.

    :return: Returns the pose grp
    :rtype: pm.nt.Group
    """

    pose_grp = [x.node() for x in pm.ls('*.isPoseGrp', r=True, o=True, type=pm.nt.Transform)]
    if not pose_grp:
        pose_grp = pm.group(em=True, n='pose_grp')
        pose_grp.addAttr('isPoseGrp', at=bool, dv=True)
    else:
        pose_grp = pose_grp[0]
    if shapes:
        pm.parent(shapes, pose_grp)

    return pose_grp


def face_scene_setup(focus_object, rig_node=None):
    """
    Cleans up the staging scene after the rig has been built.

    :param str focus_object: obj
    :param rig_node:
    :return:
    """

    # Zero flags
    if rig_node:
        flag_utils.zero_flags([rig_node])
    # Remove unused name spaces
    namespace.delete_empty_namespaces()

    # Turn off joints and turn textures on
    model_panel = cmds.getPanel(wf=True)
    if pm.modelEditor(model_panel, ex=True):
        #pm.modelEditor(model_panel, edit=True, j=False)
        pm.modelEditor(model_panel, edit=True, displayTextures=True)
    # Move the camera
    pm.viewFit(focus_object)
    # Make sure no source meshes are still in the scene
    for source_mesh in ['source_head_mesh', 'source_mouth_mesh']:
        if pm.objExists(source_mesh):
            pm.delete(source_mesh)


def sort_shapes(meshes):
    """
    Ignore this.  THIS IS A HOT PILE OF...
    This is a place holder.

    :param list(pm.nt.Transform) shapes:
    """

    dist = 150
    dist_y = 35
    i = 0
    for x, mesh in enumerate(meshes):
        if i > 20:
            i = 0
            dist_y += 35
            dist = 150

        set_dist = dist
        cmds.setAttr(f'{mesh}.tx', set_dist)
        cmds.setAttr(f'{mesh}.ty', dist_y)
        dist += 25
        i += 1


def clean_and_save_face_rig(asset_id, save_file=True):
    """
    Cleans up and saves the final rig scene.

    :param string asset_id: The str asset id for the asset.
    :param bool save_file: if True, the rig file will be saved.
    """

    frag_roots = frag.get_all_frag_roots()
    if not frag_roots:
        return
    frag_rig = frag_roots[0].get_rig()
    face_component = frag.get_face_mesh_component(frag_rig)
    if not face_component:
        return
    blendshape_meshes = face_component.get_all_category_meshes(frag.FACE_BLENDSHAPE_CATEGORY)
    skinned_meshes = face_component.get_all_category_meshes(frag.FACE_SKINNED_CATEGORY)
    for blendshape in blendshape_meshes:
        blendshape.v.set(0)
        blendshape = face_model.FaceModel(blendshape)
        scene_shapes = get_all_scene_blendshapes(asset_id, blendshape.region)
        pm.delete(scene_shapes)

    for skin_mesh in skinned_meshes:
        skin_mesh.v.set(1)
        if not skin_utils.get_skin_cluster_from_geometry(skin_mesh):
            if has_skinning_data(skin_mesh, asset_id):
                face_skinning.apply_face_skinning_from_file(asset_id, skin_mesh)

    head_mesh = face_component.head_mesh
    face_scene_setup(head_mesh.mesh, frag_rig)

    if save_file:
        file_path = paths.get_asset_maya_rig_file_path(asset_id)
        pm.saveAs(f'{file_path}.ma')


def export_head_sk(meshes, root_joint, sk_path):
    """
    Duplicates the meshes and skel, copies skinning from original mesh, deletes null joints from duplicated skel

    :param list(pm.nt.Transform) meshes: A list of meshes to duplicate
    :param pm.nt.Joint root_joint: Root joint for the SK being exported
    :param string sk_path: path of SK
    """

    # Duplicate meshes, make sure name is same as original and visible
    temp_meshes = []
    for mesh in meshes:
        dup_mesh = pm.duplicate(str(mesh))[0]
        pm.parent(dup_mesh, w=True)
        temp_meshes.append(dup_mesh)
        dup_mesh.rename(str(mesh))
        dup_mesh.v.set(1)

    root_name = naming.get_basename(root_joint)
    entire_skel = chain_markup.ChainMarkup(root_joint).joints

    # Get skin data for original meshes
    skins = {}
    for mesh, temp_mesh in list(zip(meshes, temp_meshes)):
        skin_data = skin_utils.get_skin_weights(mesh)
        skins[temp_mesh] = skin_data

    # Duplicate skeleton and fix root name after parenting under world
    dup_root = pm.duplicate(root_joint)[0]
    pm.parent(dup_root, w=True)
    dup_root.rename(root_name)

    # Create a temp namespace for original skeleton so we don't have duplicate joint names when setting weights
    head_sk_namespace = pm.namespace(addNamespace='TEMP_HEAD_SK')
    list(map(lambda x: namespace.move_node_to_namespace(x, head_sk_namespace), entire_skel))
    list(map(lambda x: namespace.move_node_to_namespace(x, head_sk_namespace), meshes))

    dup_skel_markup = chain_markup.ChainMarkup(dup_root)

    # Set weights
    for temp_mesh in temp_meshes:
        skin_data = skins.get(temp_mesh)
        set_wgt = skin_utils.set_skin_weights(skin_data[0],
                                              skin_data[1],
                                              temp_mesh,
                                              influence_set=dup_skel_markup.joints)

    # Remove null joints
    deletable_joints = [x for x in pm.listRelatives(dup_root, ad=True, type=pm.nt.Joint) if 'null' in x.name()]
    pm.delete(deletable_joints)
    dup_skel_markup.parse_joints()

    # Export list cleanup. Remove connections to nodes that should not be exported and delete constraints
    export_list = dup_skel_markup.joints + temp_meshes
    display_layers.remove_objects_from_layers(export_list)

    param_node = pm.PyNode('FragFaceParameters')
    attr_utils.remove_relationship_between_nodes(param_node, dup_root)

    constraints = [x for x in dup_root.listRelatives(ad=True, type=pm.nt.Constraint)]
    pm.delete(constraints)

    # Export and get rid of temp namespace, delete duplicated nodes
    try:
        fbx_utils.export_fbx(sk_path, export_list)

    except:
        raise

    finally:
        pm.delete(temp_meshes)
        pm.delete(dup_root)
        list(map(lambda x: namespace.move_node_to_namespace(x, ''), entire_skel))
        list(map(lambda x: namespace.move_node_to_namespace(x, ''), meshes))
        pm.namespace(removeNamespace=head_sk_namespace)




def set_head_rig_jnts(head_asset_id, wrapped_head_root):
    """
    Sets head rig non-face joints to the positions of the asset's body rig.

    :param str head_asset_id: Asset ID for the head.
    :param ChainMarkup wrapped_head_root: Wrapped root joint of the head rig.
    """

    # This is perhaps not the best way to find the body asset ID as it depends on naming conventions not changing.
    # But so far with all our head assets this would be ok.
    body_asset_id = head_asset_id.split('_head')[0]

    # Create temp namespace to import body skeleton into
    namespace.set_namespace('headtmp')
    body_skel_path = rig_utils.get_asset_skeleton(body_asset_id)
    body_root_joint = skel_utils.import_skeleton(body_skel_path)
    if not body_root_joint:
        logger.warning(f'Could not find .skl file for {body_asset_id}')
        return
    wrapped_body_root = chain_markup.ChainMarkup(body_root_joint)
    namespace.set_namespace('')

    # Look for matching regions between skeletons
    for region in wrapped_head_root.chain.keys():
        match = wrapped_body_root.chain.get(region)
        if match:
            head_jnts = wrapped_head_root.get_full_chain(region, 'center')
            body_jnts = wrapped_body_root.get_full_chain(region, 'center')
            # If region chains are unequal length we will match by name rather than markup (important for spine)
            do_name_check = True if len(head_jnts) != len(body_jnts) else False
            for body_jnt, head_jnt in list(zip(body_jnts, head_jnts)):
                if do_name_check:
                    body_jnt = next((x for x in body_jnts if naming.get_basename(x) == naming.get_basename(head_jnt)))
                    if not body_jnt:
                        continue
                pm.parentConstraint(body_jnt, head_jnt, mo=False)
    # Get rid of body joints now that head joints are positioned and freeze transforms on head skeleton
    namespace.purge_namespace('headtmp')
    pm.makeIdentity(wrapped_head_root.joints, a=True)

