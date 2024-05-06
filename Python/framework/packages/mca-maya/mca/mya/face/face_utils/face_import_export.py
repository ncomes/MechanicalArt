#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Face: Staging UI. """

# system global imports
import logging
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import os
# mca python imports
from mca.mya.rigging import frag
from mca.mya.face.face_utils import face_util
from mca.common.paths import paths
from mca.common.tools.progressbar import progressbar_ui
from mca.mya.utils import fbx_utils, scene_utils


def export_all_blendshapes(asset_id, region_name, remove_mtls=True):
    """
    Exports all the blend shapes in a scene.

    :param string asset_id: The str asset id for the asset.
    :param string region_name: The region name for the mesh to identify what mesh is being looked at.
    """

    # get all meshes that have blend shapes
    shapes = face_util.get_all_scene_blendshapes(asset_id, region_name)
    blendshape_path = paths.get_face_blendshape_path(asset_id=asset_id)
    shapes_grp = {}
    shapes = [x for x in shapes if cmds.objExists(x)]
    for shape in shapes:
        grp = cmds.listRelatives(shape, p=True)
        if grp:
            shapes_grp.setdefault(shape, grp[0])
    cmds.parent(shapes, w=True)

    export_blendshapes(blendshape_path, shapes)

    for shape, pose_grp in shapes_grp.items():
        if pose_grp:
            cmds.parent(shape, pose_grp)

    if remove_mtls:
        mtls = [os.path.join(blendshape_path, x) for x in os.listdir(blendshape_path) if '.mtl' in str(x)]
        [os.remove(x) for x in mtls]


def export_blendshapes(path, meshes, remove_mtls=False):
    """
    Exports a list of meshes.

    :param str path: The file path.
    :param list(str) meshes: List of meshes that will be exported.
    :param bool remove_mtls: If True, the mtls in the folder will be removed.
    """

    ui = progressbar_ui.ProgressBarStandard()
    ui.update_status(0, 'Exporting Blend Shapes')

    if not isinstance(meshes, list):
        meshes = [meshes]
    meshes_paths = list(map(lambda x: os.path.join(path, f'{x}.fbx'), meshes))

    i = 100.0 / (len(meshes_paths) + 1)
    step = i
    # Export meshes
    for blendshape_mesh, blendshape_path in zip(meshes, meshes_paths):

        mesh_group = pm.listRelatives(blendshape_mesh, parent=True)
        if mesh_group:
            pm.parent(blendshape_mesh, world=True)

        ui.update_status(step, f'Exporting: {os.path.basename(blendshape_path)}')

        mesh_pos = pm.xform(blendshape_mesh, q=True, t=True, ws=True)
        pm.xform(blendshape_mesh, t=(0,0,0), ws=True)

        texture_attr = pm.listConnections(f'{blendshape_mesh}Shape', t=pm.nt.ShadingEngine, plugs=True, c=True)
        if texture_attr:
            texture_attrs = texture_attr[0]
            des_texture_attr = texture_attrs[0]
            source_texture_attr = texture_attrs[1]
            pm.disconnectAttr(des_texture_attr, source_texture_attr)

        cmds.select(blendshape_mesh)
        fbx_utils.export_fbx(blendshape_path, blendshape_mesh)
        pm.xform(blendshape_mesh, t=mesh_pos, ws=True)

        if mesh_group:
            pm.parent(blendshape_mesh, mesh_group[0])
        if texture_attr:
            pm.connectAttr(des_texture_attr, source_texture_attr)

        step += i

    if remove_mtls:
        mtls = [os.path.join(path, x) for x in os.listdir(path) if '.mtl' in str(x)]
        [os.remove(x) for x in mtls]

    ui.update_status(100, 'Blend Shapes Exported')


def import_all_blendshapes(asset_id, region, ext='.fbx', exist_check=False):
    """
    Imports blend shapes associated with a blend shape mesh.

    :param string asset_id: The str asset id for the asset.
    :param string region: The region name for the mesh to identify what mesh is being looked at.
    :param str ext: Name of the file extension.
    :param bool exist_check: If True, will check to see if the mesh is already in the scene.
    :return: Returns a dictionary with all of the poses that were imported and the pose group that the get
            Parented under.
    :rtype: Dictionary
    """

    ui = progressbar_ui.ProgressBarStandard()
    ui.update_status(0, 'Starting Up')

    all_roots = frag.get_all_frag_roots()
    frag_root = [x for x in all_roots if x.asset_id == asset_id]
    if not frag_root:
        logging.warning(f'Cannot import blend shapes.  No rig will in the scene with the asset id {asset_id}.')
        return

    frag_root = frag_root[0]

    pose_grp = [x.node() for x in pm.ls('*.isPoseGrp', r=True, o=True, type=pm.nt.Transform)]
    if not pose_grp:
        pose_grp = pm.group(em=True, n='pose_grp')
        pose_grp.addAttr('isPoseGrp', at=bool, dv=True)
    else:
        pose_grp = pose_grp[0]

    frag_root.get_rig().connect_node(pose_grp, 'facePoseGrp', 'facePoseGrp')

    parameters = face_util.get_parameters_region_instance(asset_id, region)
    pose_list = parameters.get_pose_list()
    if exist_check:
        pose_list = [x for x in pose_list if not pm.objExists(x)]

    blendshape_path = paths.get_face_blendshape_path(asset_id=asset_id)
    meshes = [x for x in os.listdir(blendshape_path) if ext in str(x) and x.split('.')[0] in pose_list]
    if not meshes:
        return

    meshes_paths = list(map(lambda x: os.path.join(blendshape_path, x), meshes))
    import_list = []
    i = 100.0 / (len(meshes) + 1)
    step = i

    dialog_style = cmds.optionVar(q='FileDialogStyle')
    changed_dialog = set_native_dialog(dialog_style)

    try:
        for blendshape_mesh, mesh_path in zip(meshes, meshes_paths):
            ui.update_status(step, f'importing: {blendshape_mesh}')
            new_nodes = cmds.file(mesh_path, i=True, returnNewNodes=True)
            clean_node = scene_utils.clean_imported_nodes(new_nodes)
            if clean_node:
                imported_node = cmds.rename(clean_node[0], blendshape_mesh.split('.')[0])
                import_list.append(imported_node)
            step += i
        pm.parent(import_list, pose_grp)

    except Exception as e:
        logging.error(e)
        return

    finally:
        if changed_dialog:
            cmds.optionVar(iv=('FileDialogStyle', dialog_style))

    # Temporary hot mess
    face_util.sort_shapes(import_list)

    ui.update_status(100, 'Finished Importing')
    pose_dict = {}
    pose_dict['shapes'] = import_list
    pose_dict['pose_grp'] = pose_grp

    return pose_dict


def set_native_dialog(dialog_style):
    """
    Sets Maya default file dialog style to avoid import issues when using cmds.file()

    :param int dialog_style: Current file dialog style, 1 for OS native and 2 for Maya default
    :return: True if dialog style was changed to Maya default, otherwise False
    """

    if dialog_style != 2:
        cmds.optionVar(iv=('FileDialogStyle', 2))
        return True
    return False
