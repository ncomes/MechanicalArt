#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source head functions.  Where we get our blend shapes from.

"""
# python imports
from __future__ import print_function, division, absolute_import
import os
import shutil
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
#  python imports
from mca.common.paths import paths
from mca.mya.utils import attr_utils, display_layers
from mca.mya.modeling import blendshape_model, blendshape_node, face_model
from mca.mya.face import source_data
from mca.mya.face.face_utils import face_util
from mca.mya.rigging import mesh_markup_rig
from mca.mya.rigging import frag
from mca.common.assetlist import assetlist

SOURCE_FILE = 'source_head'


def convert_to_source_mesh(mesh, asset_id):
    """
    Returns the an instance of face_model.FaceModel.  This is a duplicate mesh that we will export and use for
    generating blend shapes.

    :param pm.nt.Transform mesh: A blend shape mesh.
    :param str asset_id: Asset Identifier.
    :return: Returns the an instance of face_model.FaceModel
    :rtype: face_model.FaceModel
    """

    if not mesh.hasAttr(mesh_markup_rig._MESH_MARKUP):
        raise AttributeError(f'{mesh} does not have {mesh_markup_rig._MESH_MARKUP} attribute.')
    if not isinstance(mesh, face_model.FaceModel):
        mesh = face_model.FaceModel(mesh)
    # Duplicate the mesh, remove from layers, and unparent.
    source_mesh = pm.duplicate(mesh.mesh, name=f'source_{mesh.type_name}')[0]
    pm.parent(source_mesh, w=True)
    display_layers.remove_objects_from_layers(source_mesh)
    source_mesh = face_model.FaceModel(source_mesh)

    # Change the category so we can identify it as a source mesh
    source_mesh.category = frag.FACE_SOURCE_CATEGORY

    # check to make sure all the blendshapes are in the scene.
    source_mesh.import_blendshapes(asset_id=asset_id, exist_check=True)
    parameters_inst = source_mesh.get_parameters(asset_id=asset_id)
    shapes = parameters_inst.get_pose_list()
    shapes = [x for x in shapes if pm.objExists(x)]

    blendshape_node.BlendShapeNode.create(shapes=shapes,
                                            mesh=source_mesh.mesh,
                                            label=source_mesh.part_type_name)
    attr_utils.unlock_all_attrs(source_mesh.mesh)

    return source_mesh


def convert_all_to_source_mesh(mesh_list, asset_id, mesh_component):
    """
    Take the source mesh and updates the information to the source data.

    :param list(pm.nt.Transform) mesh_list: A blend shape mesh.
    :param str asset_id: Asset Identifier.
    :param mesh_component:
    :return: Returns a list of all the source meshes
    :rtype: list(face_model.FaceModel)
    """

    source_list = [convert_to_source_mesh(x, asset_id) for x in mesh_list]
    mesh_dict = {}
    for mesh_inst in source_list:
        mesh_dict[mesh_inst.type_name] = mesh_inst.mesh
    attr_utils.set_compound_attribute_groups(mesh_component, frag.FACE_SOURCE_CATEGORY, mesh_dict)
    return source_list


def export_source_shapes(source_list, asset_id, save_source_data=False):
    """
    Exports the source meshes into a file in the common directory.

    :param list(pm.nt.Transform) source_list:
    :param str asset_id: Asset Identifier.
    :param bool save_source_data: Transfers the source data to the source location.
    """

    _asset = assetlist.get_asset_by_id(asset_id)
    asset_name = _asset.asset_name
    face_path = os.path.join(paths.get_common_face(), 'SourceHeads', asset_name)
    if not os.path.exists(face_path):
        os.makedirs(face_path)

    source_meshes = []
    source_instances = []
    # Create a new list with using the FaceModel instance
    for source in source_list:
        if not isinstance(source, face_model.FaceModel):
            source_instances.append(face_model.FaceModel(source))
            source_meshes.append(source)
        else:
            source_instances.append(source)
            source_meshes.append(source.mesh)
    # Disconnect the meshes before exporting so it doesn't export the whole rig.
    for mesh in source_meshes:
        pm.disconnectAttr(mesh.message)

    for mesh_inst in source_instances:
        parameters_inst = mesh_inst.get_parameters(asset_id=asset_id)
        shapes = parameters_inst.get_pose_list()
        shapes = [x for x in shapes if pm.objExists(x)]
        pm.delete(shapes)

    scene_name = pm.sceneName()

    full_path = os.path.join(face_path, f'{SOURCE_FILE}.ma')

    pm.select(source_meshes)
    cmds.file(rename=full_path)
    cmds.file(force=True, exportSelected=True, type="mayaAscii")

    cmds.file(rename=scene_name)
    if not save_source_data:
        return

    face_data_path = face_util.get_source_face_data_path(asset_id=asset_id)
    shutil.copy(face_data_path, face_path)


def import_source_head(source_head_name):
    """
    Imports a source head with the given source asset name.

    :param str source_head_name: the asset name for the source head.
    :return: Returns a list of meshes that have been imported into the scene
    :rtype: list(pm.nt.Mesh)
    """

    face_path = os.path.join(paths.get_common_face(), 'SourceHeads', source_head_name)
    if not os.path.exists(face_path):
        return
    file_name = os.path.join(face_path, f'{SOURCE_FILE}.ma')
    new_nodes = pm.importFile(file_name, f=True, defaultNamespace=True, returnNewNodes=True)

    return new_nodes


def generate_blendshapes(source_mesh, target_mesh):
    """
    Generates blend shapes from a source mesh.

    :param str source_mesh: a mesh with blend shapes attached.
    :param str target_mesh: the mesh transfering the blend shape to.
    :return: Returns a list of blend shapes created.
    :rtype: list(str)
    """

    if isinstance(target_mesh, face_model.FaceModel):
        target_mesh = target_mesh.mesh

    if not isinstance(source_mesh, face_model.FaceModel):
        source_mesh = face_model.FaceModel(source_mesh)

    blendnode = source_mesh.get_main_blendnode()

    transfer_mesh = source_mesh.duplicate(label=f'{source_mesh.mesh}_edit')
    transfer_mesh.mesh.addAttr('generateMesh', at='message')
    pm.parent(transfer_mesh.mesh, w=True)
    transfer_mesh.mesh.tx.set(25)
    transfer_mesh.mesh.v.set(1)

    parallel_blendnode = blendshape_model.create_parallel_blendnode(diff_mesh=source_mesh.mesh,
                                                                    pose_mesh=target_mesh,
                                                                    last_mesh=transfer_mesh.mesh,
                                                                    name='gen_edit_parallel_blendnode')
    shapes = blendnode.generate_face_shapes(transfer_mesh.mesh)
    pm.delete(parallel_blendnode, transfer_mesh.mesh)

    pose_grp = face_util.create_pose_grp(shapes=shapes)
    pm.parent(shapes, pose_grp)

    # Temporary hot mess
    face_util.sort_shapes(shapes)
    pose_dict = {}
    pose_dict['shapes'] = shapes
    pose_dict['pose_grp'] = pose_grp
    return pose_dict


def get_source_head_data(source_mesh_name):
    """
    Returns an instance of SourceFaceData for a specific mesh.

    :param str source_mesh_name: The str name for the source_head.
    :return: Returns an instance of FaceMeshRegionData for a specific mesh.
    :rtype: SourceFaceData
    """

    data_path = os.path.join(paths.get_common_face(), 'SourceHeads', source_mesh_name, source_data.FACE_FILE_NAME)
    src_data = source_data.SourceFaceData.load(data_path)
    return src_data


def get_source_head_region_data(source_mesh_name):
    """
    Returns an instance of SourceFaceData for a specific mesh.

    :param str source_mesh_name: The str name for the source_head.
    :return: Returns an instance of FaceMeshRegionData for a specific mesh.
    :rtype: SourceFaceData
    """

    data_path = os.path.join(paths.get_common_face(), 'SourceHeads', source_mesh_name, source_data.FACE_FILE_NAME)
    src_data = source_data.SourceFaceData.load(data_path)

    region_list = src_data.blendshape_regions_list
    region_dict = {}
    for region in region_list:
        region_dict.setdefault(region, source_data.FaceMeshRegionData.load(data_path, region))
    return region_dict


def connect_source_meshes_to_rig(source_mesh_name, parameter_node, offset=-25.0):
    """
    Imports and connects the source head blend node to a rig.

    :param str source_mesh_name: Name of the source head that will be imported and used.
    :param FragFaceParameter parameter_node: The parameter node that is connected to all the blend shapes.
    :param float offset: Offset the mesh so they do not sit directly on the rig.
    """

    # Get a dictionary of all the blend shapes in the source head and the data.
    region_dict = get_source_head_region_data(source_mesh_name)

    # import the source head
    source_list = import_source_head(source_mesh_name)
    source_list = [face_model.FaceModel(x) for x in source_list if isinstance(x, pm.nt.Transform)]
    # Go through the meshes and get the parameter data to connect to the rig.
    for mesh in source_list:
        mesh.mesh.tx.set(offset)
        blendnode = mesh.get_main_blendnode()
        region_data = region_dict.get(mesh.region, None)
        if not region_data:
            continue
        parameters = region_data.get_parameters()
        parameters_list = parameters.get_parameters_list()
        # connect the blend node to the rig
        blendnode.reconnect_to_rig(parameters=parameters_list, parameter_node=parameter_node)

    face_mesh_component = frag.get_face_mesh_component(parameter_node)

    mesh_dict = {}
    for mesh in source_list:
        mesh_dict.setdefault(mesh.category, {})
        mesh_dict[mesh.category].update({mesh.type_name: pm.PyNode(mesh.mesh)})

    for category in mesh_dict.keys():
        attr_utils.set_compound_attribute_groups(face_mesh_component.pynode, category, mesh_dict[category])

