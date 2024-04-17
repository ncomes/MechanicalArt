#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# system global imports
from __future__ import print_function, division, absolute_import
# python imports
import logging
import os
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
# mca python imports
from mca.common.paths import paths
from mca.common.utils import lists
from mca.mya.utils.om import om_utils
from mca.mya.modeling import vert_utils
from mca.mya.utils import naming
from mca.mya.rigging import chain_markup
from mca.mya.deformations import skin_utils
from mca.common.tools.progressbar import progressbar_ui


def apply_face_skinning_from_file(asset_id, mesh):
    """
    Applies skinning from an existing .sknr file.

    :param str asset_id: id of the rig
    :param pm.nt.mesh mesh: The mesh that the skinning will get applied.
    :return: Returns if the skin was set or not.
    :rtype: bool
    """

    skin_folder = paths.get_asset_skin_data_path(asset_id=asset_id)
    if os.path.exists(os.path.join(skin_folder, f'{mesh}_skin_data.json')):
        skin_utils.apply_skinning_to_mesh([mesh], skin_folder)
        return True
    else:
        return False


def export_face_skinning_to_file(asset_id, mesh):
    """
    Exports skinning from a mesh.

    :param str asset_id: id of the rig
    :param str/pm.nt.Transform mesh: The mesh that the skinning will get exported.
    :return: Returns The file name of the exported file.
    :rtype: str
    """

    mesh = str(mesh)

    if not pm.mel.findRelatedSkinCluster(mesh) != '':
        logging.warning(f'{mesh} does not have a skincluster attached.  No skinning was saved.')
        return False

    skin_folder = paths.get_asset_skin_data_path(asset_id=asset_id)
    pm.select(mesh)
    skin_utils.save_skin_weights_cmd(skin_folder)
    return True


def skin_to_head_joint(mesh_to_skin, root_joint):
    """
    Skins a mesh to the head joint.

    :param list(pm.nt.Transform or pm.general.MeshVertex) mesh_to_skin: The mesh that the skinning will get applied.
    :param pm.nt.Joint root_joint:  The root joint of the skeleton.
    """
    markup = chain_markup.ChainMarkup(root_joint)
    head_joint = markup.get_end('neck', 'center')

    if isinstance(mesh_to_skin[0], pm.nt.Transform):
        obj_to_skin = f'{mesh_to_skin[0]}Shape'
        selected_verts = pm.ls(f'{mesh_to_skin[0]}Shape.vtx[*]', fl=True)

    elif isinstance(mesh_to_skin[0], pm.general.MeshVertex):
        obj_to_skin = str(mesh_to_skin[0]).split('.vtx')[0]
        selected_verts = mesh_to_skin

    else:
        return
    obj_clus = skin_utils.get_skin_cluster_from_geometry(pm.PyNode(obj_to_skin))
    if not obj_clus:
        pm.skinCluster(head_joint, obj_to_skin, tsb=True, mi=4, nw=1)
    else:
        for vert in selected_verts:
            try:
                pm.skinPercent(obj_clus, vert, transformValue=(head_joint, 1.0))
            except RuntimeError:
                pm.skinCluster(obj_clus, edit=True, ai=head_joint)
                pm.skinPercent(obj_clus, vert, transformValue=(head_joint, 1.0))


def apply_common_skinning(mesh, mesh_type):
    """
    Applies common skinning

    :param list(pm.nt.Transform) mesh: Mesh to skin
    :param str mesh_type: Blendshape type to find skinning for
    """
    skin_folder = os.path.join(paths.get_common_face(), 'BaseSkinning')
    if not mesh_type:
        return
    skin_utils.apply_skinning_to_mesh([mesh], skin_folder, name_override=mesh_type)


def apply_non_deform_skinning(asset_id, mesh, non_deform_data):
    """
    Applies non_deform skinning

    :param str asset_id: Asset ID of character we are skinning (to check for skin data, if none yet will use common)
    :param str mesh: Mesh name
    :param dict non_deform_data: Dict containing non_deform vertex IDs from rig source data
    """

    vert_nums = list(non_deform_data.keys())
    vertex_list = list(map(lambda x: pm.MeshVertex(f'{mesh}Shape.vtx[{x}]'), vert_nums))
    skin_folder = paths.get_asset_skin_data_path(asset_id=asset_id)
    name_override = ''
    if not os.path.exists(os.path.join(skin_folder, f'{mesh}_skin_data')):
        skin_folder = os.path.join(paths.get_common_face(), 'BaseSkinning')
        name_override = 'head_blendshape'
    skin_utils.apply_skinning_to_verts(vertex_list, skin_folder, name_override=name_override)


def face_skinning_converter_cmd(blendshape_mesh, skin_mesh, joints, start_frame, end_frame, delete_decomp_mesh=True):
    """
    Runs the Hans Godard Linear Skinning Decomposition Plugin.

    :param str/pm.nt.Transform blendshape_mesh: mesh to get skinned
    :param str/pm.nt.Transform skin_mesh: mesh to get skinned
    :param list(str/pm.nt.Joint) joints: List of joints that get skinned
    :param int start_frame: Start frame of the poses
    :param int end_frame: End frame of the poses
    :param list(str) end_frame: End frame of the poses
    :return: Returns a dictionary of everything that was created.
    :rtype: Dictionary
    """

    pm.select(blendshape_mesh, joints)
    str_joints = cmds.ls(sl=True, type='joint')

    # run skinning tool!
    result = skin_utils.skinning_converter_cmd(str_joints, start_frame, end_frame)
    decomp_grp = result.get('meshGrp', None)
    if not decomp_grp:
        return

    decomp_mesh = lists.get_first_in_list(cmds.listRelatives(decomp_grp, c=True))
    if not decomp_mesh:
        return

    skin_utils.copy_skin_weights(source_list=[pm.PyNode(decomp_mesh)],
                            target_list=[pm.PyNode(skin_mesh)],
                            match_influences=True)
    if delete_decomp_mesh:
        pm.delete(result['meshGrp'])
    pm.select(cl=True)

    return


def apply_skinning_from_data(verts_data, face_mesh, skinned_joints):
    """
    Applies skin data saved in rig_source_data.json

    :param FaceMeshRegionData face_data: Instance of FaceMeshRegionData class
    :param str/pm.nt.Transform face_mesh: Skinned face mesh to apply weights on

    """

    skin_clus = skin_utils.get_skin_cluster_from_geometry(face_mesh)
    vert_numbers = verts_data.keys()
    if not skin_clus:
        skin_clus = pm.skinCluster(skinned_joints, face_mesh, tsb=True)

    for vert_number in vert_numbers:
        full_vert_name = f'{face_mesh}.vtx[{vert_number}]'
        influences = verts_data.get(vert_number)
        influencing_joints = influences.keys()

        for influencing_joint in influencing_joints:
            if influencing_joint == list(influencing_joints)[0]:
                influence_value = 1.0
            else:
                influence_value = influences.get(influencing_joint)
            try:
                cmds.skinPercent(str(skin_clus), full_vert_name, tv=(influencing_joint, float(influence_value)))
            except RuntimeError:
                pm.skinCluster(skin_clus, edit=True, ai=influencing_joint)
                pm.skinPercent(skin_clus, full_vert_name, transformValue=(influencing_joint, float(influence_value)))


def verts_skin_data(verts):
    """
    Creates a dictionary containing vertex skin data
    :param list verts: List of vertices
    :param skinCluster skin_cluster:
    :return: Returns dictionary of all vertex skin data
    :rtype: dict

    """

    skinned_mesh = pm.PyNode(str(verts[0]).split('.vtx')[0])
    skin_cluster = skin_utils.get_skin_cluster_from_geometry(skinned_mesh)

    vertices_skin_data = {}

    for vert in verts:
        vert_number = vert_utils.get_vertices_as_numbers(str(vert))[0]
        skinned_joints = pm.skinCluster(vert, q=True, inf=True)
        influences_dict = {}
        for jnt in skinned_joints:
            influ = pm.skinPercent(skin_cluster, vert, transform=jnt, q=True)
            if influ != 0.0:
                influences_dict[str(jnt)] = str(influ)
            vertices_skin_data[vert_number] = influences_dict

    return vertices_skin_data


def copy_weights_from_head(face_mesh, face_data, mesh_to_skin):
    """
    Copies weights from head mesh and applies them to another mesh

    param: str face_mesh: Name of face mesh to copy weights from
    param: FaceMeshRegionData face_data: Data for head, used to determine what joints should be skinned
    param: list(pm.nt.Transform or pm.general.MeshVertex) mesh_to_skin: Mesh or vertices to copy weights into
    """

    skinnable_joints = face_data.joints_skinned
    head_skin_clus = skin_utils.get_skin_cluster_from_geometry(pm.PyNode(face_mesh))

    if not head_skin_clus:
        return

    if isinstance(mesh_to_skin[0], pm.nt.Transform):
        obj_to_skin = f'{mesh_to_skin[0]}Shape'
        obj_verts = pm.ls(f'{mesh_to_skin[0]}Shape.vtx[*]', fl=True)

    elif isinstance(mesh_to_skin[0], pm.general.MeshVertex):
        obj_to_skin = str(mesh_to_skin[0]).split('.vtx')[0]
        obj_verts = mesh_to_skin

    else:
        return

    obj_clus = skin_utils.get_skin_cluster_from_geometry(pm.PyNode(obj_to_skin))
    if not obj_clus:
        obj_clus = pm.skinCluster(obj_to_skin, skinnable_joints)
    else:
        current_influences = pm.skinCluster(obj_to_skin, q=True, inf=True)
        for skinnable_joint in skinnable_joints:
            if skinnable_joint not in current_influences:
                pm.skinCluster(obj_clus, e=True, ai=skinnable_joint)

    pm.select(face_mesh, r=True)
    pm.select(obj_verts, add=True)
    pm.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='closestJoint')
    pm.skinCluster(obj_clus, e=True, rui=True)
    pm.select(cl=True)


def mirror_face_weights(verts_to_mirror, face_mesh, face_data):
    """
    Mirrors vertex weights on face mesh

    :param: list(pm.general.MeshVertex) verts_to_mirror: List of vertices to mirror weights from
    :param: str face_mesh: Name of face mesh
    :param: FaceMeshRegionData face_data: Data for head, used to find mirror vertex
    """

    prog_ui = progressbar_ui.ProgressBarStandard()
    prog_ui.update_status(0, 'Starting Up')

    i = 100.0 / (len(verts_to_mirror) + 1)

    head_skin_clus = skin_utils.get_skin_cluster_from_geometry(pm.PyNode(face_mesh))
    if not head_skin_clus:
        return

    all_vert_data = verts_skin_data(verts_to_mirror)
    mirror_data = face_data.get_mirror_data()
    vert_mirror_data = mirror_data.mirror_map

    for x, vertex in enumerate(verts_to_mirror):
        step = x * i
        prog_ui.update_status(step, f'Mirroring skin data...')
        vertex_number = vert_utils.get_vertices_as_numbers(str(vertex))[0]
        vert_skinning = all_vert_data.get(vertex_number, None)
        mir = vert_mirror_data.get(str(vertex_number))

        if not mir:
            pass

        else:
            mirror_vert_name = f'{face_mesh}.vtx[{mir}]'

            for face_joint in vert_skinning:
                if face_joint == list(vert_skinning)[0]:
                    joint_weight = 1.0
                else:
                    joint_weight = vert_skinning.get(face_joint, None)

                side = face_joint[:2]
                if side == 'r_':
                    face_joint = f'l_{face_joint[2:]}'

                elif side == 'l_':
                    face_joint = f'r_{face_joint[2:]}'
                cmds.skinPercent(head_skin_clus, mirror_vert_name, tv=(face_joint, float(joint_weight)))

    prog_ui.update_status(100, 'Finished')


def cleanup_face_skinning_right_left(face_mesh, mirror_data, joint_list):
    """
    Removes left side joint influences from right side of face mesh and vice versa.

    :param pm.nt.Transform face_mesh: Mesh to edit skinning on
    :param SourceVertexMirror mirror_data: Mirror vertex data from rig source data
    :param list(str) joint_list: List of all joint names
    """


    right_vert_list = [int(x) for x in mirror_data.right.keys()]
    left_vert_list = [int(x) for x in mirror_data.left.keys()]

    weight_dict, blend_weights = skin_utils.remove_wrong_side_influ(face_mesh.name(),
                                                                    right_vert_list,
                                                                    left_vert_list,
                                                                    joint_list,
                                                                    l_r_labels=['l_', 'r_'])
    skin_utils.set_skin_weights(weight_dict,
                                blend_weights,
                                face_mesh,
                                influence_set=joint_list)


def smooth_vert_weights(vert_index_list, mesh_name, tol_val):
    """
    Smooths vertex weights out

    :param list(int) vert_index_list: List of vertex indices to operate on
    :param str mesh_name: Name of the mesh they belong to
    :param float tol_val: Tolerance value for smoothWeights operation (lower value = more smooth)
    """

    skin_clus = skin_utils.get_skin_cluster_from_geometry(pm.PyNode(mesh_name))
    for vert in vert_index_list:
        # smoothWeights combines weights from all selected, so we only want to run this
        # operation on small pieces otherwise we entirely lose integrity of our skinning
        adjacent_verts = om_utils.get_adjacent_vertices(f'{mesh_name}Shape.vtx[{vert}]')
        vertices = [f'{mesh_name}Shape.vtx[{x}]' for x in adjacent_verts + [vert]]
        # You can't just indicate which vertices to smooth for this command, they must be selected
        cmds.select(vertices, r=True)
        cmds.skinCluster(skin_clus, edit=True, smoothWeights=tol_val)
        # Not flushing undo or only flushing at the end will result in way too much RAM usage
        cmds.flushUndo()


def cleanup_lips_skinning(face_mesh, eyelash_data, joint_list):
    """
    Removes upper lip joint influences from bottom which is a common issue after LSD process

    :param pm.nt.Transform face_mesh: Mesh to edit skinning on
    :param SourceFaceEyelashShelf eyelash_data: Eye (and lip) snapping data from rig source data
    :param list(str) joint_list: List of all joint names
    """

    lip_data = eyelash_data.lip_snap
    og_vert_list = lip_data.get('bottom').keys()
    cmds.select([f'{face_mesh.name()}Shape.vtx[{x}]' for x in og_vert_list], r=True)
    # Expand selection from just the lip snap vertices to include surrounding as well
    for x in range(3):
        mel.eval('PolySelectTraverse 1')
    sel_verts = cmds.ls(sl=True, fl=True)
    cmds.select(cl=True)
    vert_list = vert_utils.get_vertices_as_numbers(sel_verts)
    weight_dictionary, blend_wghts = skin_utils.remove_keywords_influ_from_verts(face_mesh.name(),
                                                                                 vert_list,
                                                                                 joint_list,
                                                                                 ['upper', 'lower_lip_corner_02', 'lip',
                                                                                  'eyelid', 'cheek', 'nasolabial'])

    skin_utils.set_skin_weights(weight_dictionary,
                                blend_wghts,
                                face_mesh.name(),
                                influence_set=joint_list)


def cleanup_brows_skinning(face_mesh, vert_list, joint_list):
    """
    Removes some influences from common offenders knows for having influences in the brow region
    when they should not

    :param pm.nt.Transform face_mesh: Mesh to edit skinning on
    :param list(int) vert_list: List of vertex indices to operate on
    :param list(str) joint_list: List of all joint names
    """

    weight_dictionary, blend_wghts = skin_utils.remove_keywords_influ_from_verts(face_mesh.name(),
                                                                                 vert_list,
                                                                                 joint_list,
                                                                                 ['nose', 'chin'])
    skin_utils.set_skin_weights(weight_dictionary,
                                blend_wghts,
                                face_mesh.name(),
                                influence_set=joint_list)


def post_lsd_face_cleanup(mesh_node,
                          region_data,
                          wrapped_root,
                          asset_id=None):
    """
    Runs functions for cleaning up face skinning.

    :param pm.nt.Transform mesh_node: Face mesh node we are cleaning up skinning on
    :param FaceMeshRegionData region_data: Rig source data
    :param ChainMarkup wrapped_root: Wrapped root joint of the rig
    :param str asset_id: ID of the asset we are skinning. If None we'll grab common skinning data
    """

    joint_list = list(map(lambda x: naming.get_basename(x), wrapped_root.joints))

    apply_non_deform_skinning(asset_id, mesh_node, region_data.vertex_default_regions.get('non_deform'))
    brows = [int(x) for x in region_data.vertex_default_regions.get('brows').keys()]
    deform_area = [int(x) for x in region_data.vertex_default_regions.get('deform_area').keys()]

    cleanup_face_skinning_right_left(mesh_node, region_data.get_mirror_data(), joint_list)
    cleanup_lips_skinning(mesh_node, region_data.get_eyelids(), joint_list)
    cleanup_brows_skinning(mesh_node, brows, joint_list)

    majority_smooth = [x for x in deform_area if x not in brows]
    smooth_vert_weights(majority_smooth, mesh_node.name(), 0.08)
    smooth_vert_weights(brows, mesh_node.name(), 0.3)

    skin_cluster = skin_utils.get_skin_cluster_from_geometry(mesh_node)
    pm.skinPercent(skin_cluster, mesh_node, nrm=True)







