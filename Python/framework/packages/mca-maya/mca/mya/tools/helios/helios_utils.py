#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains misc utils for use within Helios' ecosystem.
"""

# System global imports
import os
import shutil
# software specific imports
import maya.cmds as cmds
import pymel.core as pm
# PySide2 imports
from PySide2 import QtWidgets
# mca python imports
from mca.common import log

from mca.common import paths as path_utils
from mca.common.assetlist import assetlist
from mca.common.utils import lists, fileio
from mca.common.paths import path_utils, project_paths
from mca.common.pyqt import messages
from mca.common.modifiers import decorators

from mca.mya.modifiers import ma_decorators
from mca.mya.utils import attr_utils, dag, fbx_utils, node_util, optionvars, material_utils, naming, scene_utils
from mca.mya.deformations import skin_utils
from mca.mya.rigging import skel_utils, rig_utils
from mca.mya.pyqt import dialogs

from mca.mya.tools.helios import helios_registry

logger = log.MCA_LOGGER


class MCAHeliosOptionVars(optionvars.MCAOptionVars):
    """
    This handles keeping track of Helio's UI values to be restored or used during various UI functions.
    """

    # Helios Misc
    MCALastMaterialPath = {'default_value': project_paths.MCA_PROJECT_ROOT, 'docstring': 'Branch content path.'}

    # Helios Main
    MCALastOpenTab = {'default_value': [], 'docstring': 'The last opened tabs.'}

    MCAPerfMaterials = {'default_value': False, 'docstring': 'If performance materials should be used when importing assets.'}
    MCAWithSkinning = {'default_value': False, 'docstring': 'If skins should be imported when importing assets.'}
    MCAToSelected = {'default_value': False, 'docstring': 'If existing scene skeletons should be used when importing assets.'}
    MCAWithFullSkeleton = {'default_value': False, 'docstring': 'If the full skeleton should be merged in.'}

    MCAExportSourceMa = {'default_value': False, 'docstring': 'If when exporting a source file should be saved as well.'}
    MCAExportSkn = {'default_value': False, 'docstring': 'If when exporting a skn file should be saved as well.'}

    # Helios Wizard
    MCALastAssetType = {'default_value': '', 'docstring': 'The last archetype selected in the wizard.'}
    MCALastRelease = {'default_value': 'None', 'docstring': 'The last release option selected in the wizard.'}
    MCACreateFolders = {'default_value': False, 'docstring': 'If the new asset folder structure should be generated when the scene is organized.'}


HELIOS_OPTION_VARS = MCAHeliosOptionVars()
NODE_WHITE_LIST = (pm.nt.Transform, pm.nt.Mesh, pm.nt.SkinCluster, pm.nt.BlendShape, pm.nt.DagPose,
                   pm.nt.Phong, pm.nt.Blinn, pm.nt.Lambert, pm.nt.ShadingEngine, pm.nt.GroupId, pm.nt.GroupParts, pm.nt.MaterialInfo,
                   pm.nt.Reverse, pm.nt.RemapValue, pm.nt.Bump2d, pm.nt.Place2dTexture, pm.nt.File)


# Misc tools
@ma_decorators.keep_selection_decorator
@decorators.track_fnc
def apply_materials_to_selected_cmd():
    """
    UI command to find and apply materials using the MCA material builder. This works within Helios' ecosystem to import/restore materials on models.
    """

    # sort selection
    selection = pm.selected()
    selection = [x for x in selection if isinstance(x, (pm.nt.Transform, pm.MeshFace))]

    # find materials
    starting_directory = HELIOS_OPTION_VARS.MCALastMaterialPath
    found_path_list, _ = QtWidgets.QFileDialog.getOpenFileNames(None, 'Select Shader', starting_directory, 'texture (*.tga)')
    if found_path_list:
        HELIOS_OPTION_VARS.MCALastMaterialPath = os.path.dirname(found_path_list[0])

    # sort files to unique list.
    found_material_list = []
    unique_file_list = []
    for file_path in found_path_list:
        file_name = os.path.basename(file_path).rpartition('_')[0]
        if file_name not in found_material_list:
            found_material_list.append(file_name)
            unique_file_list.append(file_path)

    # generate MCA materials and apply the first we found.
    for index, file_path in enumerate(unique_file_list):
        mca_material = material_utils.DefaultMaterial(file_path)
        if not index:
            material_utils.assign_material(mca_material.material_node, selection)


@decorators.track_fnc
def duplicate_material_cmd():
    """
    Duplicate a Helios safe material with a different name so that the engine see it
    as a new material slot.

    """

    selected_material = lists.get_first_in_list(pm.selected())
    if not selected_material:
        return

    if not selected_material.hasAttr('texture_path'):
        return

    new_name = messages.text_prompt_message('Enter a name', f'{selected_material.name()}: Select a new name for this material.')
    if new_name == 'Cancel':
        return

    new_name = naming.make_maya_safe_name(new_name)
    if not new_name:
        return

    new_material = pm.duplicate(selected_material, n=new_name, ic=True)[0]
    new_material.deleteAttr('texture_path')


# Import fncs
def import_source_file(file_path):
    """
    Helios core function for importing and cleaning fbx files for use in organizing scenes.
    Based on the NODE_WHITE_LIST established at the head of this file all other node types are removed.
    NOTE this function should be modified to support other file times if required.

    :param str file_path: A full path to a given .fbx file.
    :return: A list of all imported nodes that are part of a type matching those in the NODE_WHITE_LIST.
    :rtype: list[PyNode]
    """

    return_list = []
    imported_node_list = []
    things_to_delete = []
    if file_path.lower().endswith('.fbx'):
        imported_node_list = fbx_utils.import_fbx(file_path)
        material_list = [x for x in imported_node_list if x.hasAttr('texture_path')]
        material_utils.consolidate_materials(material_list)
        pm.delete(pm.ls(imported_node_list, type=pm.nt.DisplayLayer))

    for x in imported_node_list:
        if not cmds.objExists(x.name()):
            continue
        if isinstance(x, NODE_WHITE_LIST):
            return_list.append(x)
        else:
            things_to_delete.append(x)
    pm.delete(things_to_delete)
    return return_list


def copy_skn_weights(bind_root, node_list, skin_path):
    """
    From a save skin weights file, import and copy skins.

    :param Joint bind_root: The root joint of the skeleton our meshes will be bound to.
    :param list[Transform] node_list: A list of all shaped transforms that need skinning data.
    :param str skin_path: The path to a save skin weights file.
    """

    unbound_nodes = []
    for node in node_list:
        if isinstance(node, pm.nt.Transform):
            if node.getShape() and not skin_utils.find_related_skin_cluster(node):
                unbound_nodes.append(node)
            else:
                child_list = node.getChildren(type=pm.nt.Transform)
                for child_node in child_list:
                    if child_node.getShape() and not skin_utils.find_related_skin_cluster(child_node):
                        unbound_nodes.append(child_node)

    if not unbound_nodes:
        return

    if not os.path.exists(skin_path):
        for node in unbound_nodes:
            pm.skinCluster(node, [bind_root], tsb=True,
                           normalizeWeights=1, maximumInfluences=skin_utils.DEFAULT_MAX_INFLUENCES,
                           obeyMaxInfluences=True, removeUnusedInfluence=False)
    else:
        imported_skin_node_list = fbx_utils.import_fbx(skin_path)

        skinned_node_list = [node for node in imported_skin_node_list if
                             isinstance(node, pm.nt.Transform) and node.getShape() and
                             skin_utils.find_related_skin_cluster(node)]

        # bind to the imported skeleton
        # $TODO FSchorch Maybe make something that does the bind rebind at the same time?
        skin_utils.copy_skin_weights(skinned_node_list, unbound_nodes, match_influences=True)
        skin_utils.rebind_mesh_to_skel(unbound_nodes, bind_root)

        pm.delete(imported_skin_node_list)


def import_helios_asset(mca_asset, with_skinning=True, skel_root_dict=None, organize_only=False):
    """
    From a Helios Data class import and organize the asset.

    :param MCAAsset mca_asset: MCAAsset data class which contains information on how to import and construct the scene hierarchy.
    :param bool with_skinning: If skinning should be kept or applied to the imported models.
    :param dict{str|Joint} skel_root_dict: A dictionary of rig asset ids to the joints they represent. When importing
        with skinning if the rig asset id matches the incoming asset it will be bound against it instead of deleted.
        If skinning is enabled but a root dict was not provided this will be generated during the import process.
    :param bool organize_only: If the scene should only build organization groups and not attempt to import.
    :return: The imported organization group, and the skel_root_dict
    :rtype: Transform, dict{str|Joint}
    """

    if skel_root_dict is None:
        skel_root_dict = {}

    organization_group = pm.group(n=mca_asset.asset_name, em=True, w=True)
    attr_dict = {'name': mca_asset.asset_name,
                 'asset_id': mca_asset.asset_id,
                 'path': path_utils.to_relative_path(mca_asset.sm_path) or '',
                 'type': mca_asset.asset_type,
                 'subtype': mca_asset.asset_subtype,
                 'archetype': mca_asset.asset_archetype
                 }
    attr_utils.set_compound_attribute_groups(organization_group, 'helios', attr_dict)

    if os.path.exists(mca_asset.sm_path) and not organize_only:
        sm_path = mca_asset.sm_path
        sk_path = mca_asset.sk_path
        import_path = sk_path if os.path.exists(sk_path) else sm_path

        imported_node_list = import_source_file(import_path)
        parentable_object_list = []
        shaped_transform_list = []
        # geo organization
        for node in imported_node_list:
            if isinstance(node, pm.nt.Transform):
                if node.getShape():
                    shaped_transform_list.append(node)

                if node.getParent():
                    continue
                else:
                    if isinstance(node, (pm.nt.Locator, pm.nt.Joint)):
                        # this may need to be revisited but it's normally reserved for nodes under another shaped transform.
                        continue
                parentable_object_list.append(node)
        if parentable_object_list:
            pm.parent(parentable_object_list, organization_group)
        imported_joints = pm.ls(imported_node_list, type=pm.nt.Joint)

        # skinning
        if not with_skinning:
            pm.delete(imported_joints)
            attr_utils.set_attr_state(shaped_transform_list, False)
        else:
            # if we want the asset skinned lets try and do so.
            if imported_joints:
                # if it's already skinned because it came in with joints
                if skel_root_dict and mca_asset.skel_path in skel_root_dict:
                    skin_utils.rebind_mesh_to_skel(shaped_transform_list, skel_root_dict[mca_asset.skel_path])
                    pm.delete(imported_joints)
                elif skel_root_dict and 'default' in skel_root_dict:
                    skin_utils.rebind_mesh_to_skel(shaped_transform_list, skel_root_dict['default'])
                    pm.delete(imported_joints)
                else:
                    # we do not have a skel root for this type of asset so lets register it and pass it down.
                    imported_root = dag.get_absolute_parent(imported_joints[0], node_type=pm.nt.Joint)
                    if not imported_root.hasAttr('asset_id'):
                        imported_root.addAttr('asset_id', dt='string')
                    imported_root.setAttr('asset_id', mca_asset.asset_id)
                    skel_root_dict[mca_asset.skel_path] = imported_root
                    if 'default' not in skel_root_dict:
                        skel_root_dict['default'] = imported_root
            else:
                if mca_asset.skel_path not in skel_root_dict:
                    # we didn't have a skeleton from import, so lets see if we have a root joint to bind against for this type.
                    skel_path = mca_asset.skel_path
                    if skel_path and os.path.exists(skel_path):
                        bind_root = skel_utils.import_skeleton(skel_path)
                        if bind_root:
                            bind_root.setAttr('asset_id', mca_asset.asset_id)
                            skel_root_dict[mca_asset.skel_path] = bind_root
                if mca_asset.skel_path in skel_root_dict:
                    # we should almost never hit this. Either an asset will be skinned with an SK or there is a reason
                    # we never exported it with skinning to being with.
                    if mca_asset.skin_path:
                        copy_skn_weights(skel_root_dict[mca_asset.skel_path], shaped_transform_list, mca_asset.skin_path)
                    else:
                        for node in shaped_transform_list:
                            # if we don't have a skin file bind them all to the root.
                            pm.skinCluster(node, [skel_root_dict[mca_asset.skel_path]], tsb=True,
                                           normalizeWeights=1, maximumInfluences=skin_utils.DEFAULT_MAX_INFLUENCES,
                                           obeyMaxInfluences=True, removeUnusedInfluence=False)

    for sub_asset in mca_asset.local_asset_list:
        # recursively import and organize under the root.
        sub_org_group, sub_skel_root_dict = import_helios_asset(sub_asset, with_skinning=with_skinning, skel_root_dict=skel_root_dict)
        sub_skel_root_dict.update(skel_root_dict)
        skel_root_dict = sub_skel_root_dict
        sub_org_group.setParent(organization_group)

    displaylayer_node = lists.get_first_in_list(pm.ls(f'{mca_asset.file_name}_dl', type=pm.nt.DisplayLayer))
    if not displaylayer_node:
        displaylayer_node = pm.createDisplayLayer(n=f'{mca_asset.file_name}_dl', nr=True, e=True)
    displaylayer_node.addMembers(organization_group)
    source_ma_path = os.path.join(mca_asset.source_path, 'Model', 'Maya', f'{mca_asset.file_name}.ma')
    fileio.touch_path(source_ma_path)
    pm.renameFile(source_ma_path)
    return organization_group, skel_root_dict


def find_export_groups(node):
    """
    Search through all children and identify exportable groups.

    :param Transform node: The starting group to base our export off of.
    :return: Tuples of the export group and its export path in a list of all found groups.
    :rtype: list[(Transform, str)...]
    """

    helios_group_list = []
    for node in dag.get_children_in_order(node, node_type=pm.nt.Transform):
        if node.hasAttr('helios'):
            export_path = None
            if node.hasAttr('helios_type') and node.getAttr('helios_type') == 'model':
                if node.hasAttr('helios_path'):
                    export_path = node.getAttr('helios_path')
            helios_group_list.append((node, path_utils.to_full_path(export_path)))
    return helios_group_list


def get_exportable_meshes(export_group):
    """
    From a valid export group find all exportable meshes. This is used during SM/SK exports.

    :param Transform export_group: A group that represents a valid exportable group.
    :return: A list of all valid shaped transforms or groups containing valid shaped transforms.
    :rtype: list[Transform]
    """

    exportable_node_list = []
    blendshape_targets = []
    for node in export_group.getChildren(type=pm.nt.Transform):
        if node.hasAttr('helios') or not pm.objExists(node):
            continue

        # Take all objects not marked up with Helios' markup. Since we can have nested exports we want to make sure
        # we're only grabbing one representative of it at a time.
        node_shape = node.getShape()
        if node_shape:
            blend_node = lists.get_first_in_list(node_shape.listConnections(type=pm.nt.BlendShape))
            if blend_node:
                blendshape_targets += pm.blendShape(blend_node, q=True, target=True)

        node_children = node.getChildren()
        if node_children:
            # We're recursively running this to find and delete blendshape targets. They're restored on import.
            # They become embedded in the FBX file.
            get_exportable_meshes(node)

        exportable_node_list.append(node)

    exportable_node_list = [x for x in exportable_node_list if x not in blendshape_targets]
    pm.delete(blendshape_targets)
    return exportable_node_list


def get_exportable_meshes_organization(export_group):
    """
    From a valid export group find all meshes and the names of their parents for restoring after RBF operations.
    This is used to find group pairings for RBF retargeting.

    :param Transform export_group: A group that represents a valid exportable group.
    :return: A list of all valid shaped transforms or groups containing valid shaped transforms.
    :rtype: list[Transform]
    """

    organization_dict = {'main': []}
    return_list = []
    for node in export_group.getChildren(type=pm.nt.Transform):
        # Take all objects not marked up with Helios' markup. Since we can have nested exports we want to make sure
        # we're only grabbing one representative of it at a time.
        if node.hasAttr('helios'):
            continue
        elif node.getShape():
            return_list.append(node)
            organization_dict['main'].append(naming.get_basename(node))
        else:
            node_children = node.getChildren()
            return_list += node_children
            organization_dict[naming.get_basename(node)] = [naming.get_basename(x) for x in node_children if x.getShape()]

    return return_list, organization_dict


def get_asset_from_export_group(export_group):
    """
    Read Helios markup off an object to build an asset data class for use with exporting.

    :param Transform export_group: A transform with Helios markup.
    :return: A MCA asset data class.
    :rtype: MCAAsset
    """

    data_dict = {}
    is_dirty = False
    if export_group.hasAttr('helios'):
        # find local attrs and add them to our data dict.
        for attr in export_group.helios.getChildren():
            data_dict[attr.attrName().replace('helios_', '')] = attr.get()

    for node in export_group.getChildren(type=pm.nt.Transform):
        # find and sub objects and import them into our data dict.
        if node.hasAttr('helios'):
            mca_asset = get_asset_from_export_group(node)
            if 'local_asset_list' not in data_dict:
                data_dict['local_asset_list'] = []
            data_dict['local_asset_list'].append(mca_asset.asset_id)

    asset_id = data_dict.get('asset_id', '')
    mca_asset = assetlist.MCAAsset(asset_id, data_dict) if data_dict else None
    if mca_asset:
        asset_id = mca_asset.asset_id
        if asset_id:
            found_mca_asset = assetlist.get_asset_by_id(asset_id)
            if not found_mca_asset or found_mca_asset.get_data_dict() != mca_asset.get_data_dict():
                mca_asset.DIRTY = True
    return mca_asset


def export_helios_asset(node, update_skn=False, save_source=False, register_assets=True):
    """
    From a given node find all valid exportable groups and export them to their file paths.

    :param Transform node: A node in the export hierarchy.
    :param bool update_skn: If the skn file associated with this model should be updated.
    :param bool save_source: If a source .ma should be saved during export.
    :param bool register_assets: If the exported assets should be added to our helios asset registry.
    """

    # safety save.
    scene_utils.backup_scene('helios_export')

    # collect all potential bind roots
    bind_root_list = skin_utils.get_all_hierarchy_bind_roots(node)
    bind_dict = {}

    deletable_roots = []
    for bind_root in bind_root_list:
        # make a bind dict for asset_id lookups.
        if bind_root.hasAttr('asset_id') and bind_root.getAttr('asset_id'):
            bind_dict[bind_root.getAttr('asset_id')] = bind_root
            if len(bind_root_list) == 1:
                # If we only have a single root also assign this as the default fallback.
                bind_dict['default'] = bind_root
        else:
            bind_dict['default'] = bind_root

    delete_root_after_export = False
    export_group_list = find_export_groups(node)
    for export_group, export_path in export_group_list:
        if not export_path and not register_assets:
            continue
        # $TODO FSchorsch we should be able to get this data earlier so we don't have to ask it every time.
        mca_asset = get_asset_from_export_group(export_group)

        if not mca_asset:
            logger.warning(f'{export_group} was unable to be converted into a MCAAsset. It will be skipped. '
                                            f'Re-organize scene to correct markup.')
            continue

        if register_assets:
            mca_asset.register(commit=False)

        exportable_node_list = get_exportable_meshes(export_group)

        if not exportable_node_list:
            continue
        else:
            node_list = exportable_node_list[:]

            sm_export = True
            if len(node_list) == 1:
                if len(node_list[0].vtx) == 4:
                    sm_export = False

            # cleanup for skinning, we'll need valid binds to generate an SK file.
            if mca_asset.asset_id not in bind_dict and 'default' not in bind_dict:
                delete_root_after_export = True
                if mca_asset.asset_id:
                    skel_path = mca_asset.skel_path
                    bind_root = None
                    if skel_path and os.path.exists(skel_path):
                        bind_root = skel_utils.import_skeleton(skel_path)
                    else:
                        logger.warning(f'{mca_asset.asset_id} was not found in the asset list. '
                                                            f'We will attempt to recover a skeleton from the SK file.')
                        sk_path = mca_asset.sk_path
                        if os.path.exists(sk_path):
                            imported_nodes = fbx_utils.import_fbx(sk_path)
                            imported_joint_list = pm.ls(imported_nodes, type=pm.nt.Joint)
                            if imported_joint_list:
                                pm.delete(set(imported_nodes).difference(set(imported_joint_list)))
                                bind_root = dag.get_absolute_parent(imported_joint_list[0])
                        else:
                            logger.warning(f'Unable to recover a skeleton from an SK file. '
                                           f'Only the SM will be exported.')
                    if bind_root:
                        deletable_roots.append(bind_root)
                        bind_dict[mca_asset.asset_id] = bind_root

            if mca_asset.asset_id in bind_dict:
                bind_root = bind_dict[mca_asset.asset_id]
                if mca_asset and os.path.exists(mca_asset.skel_path):
                    # Reset rotations so we don't export accidental model changes.
                    skel_utils.restore_skeleton_bindpose(mca_asset.skel_path, bind_root)
                else:
                    for joint_node in bind_root.listRelatives(ad=True, type=pm.nt.Joint):
                        # Reset rotations so we don't export accidental model changes.
                        try:
                            joint_node.r.set([0, 0, 0])
                        except:
                            pass

                # if we neither had a bind root nor were able to import one continue. Some assets might only be static
                # meshes, for instance anything working with Nanite.
                copy_skins_path = None
                if os.path.exists(mca_asset.skin_path):
                    # try our local skn first
                    copy_skins_path = mca_asset.skin_path
                else:
                    # if we don't have a local skin path try our rig's sk.
                    if mca_asset:
                        copy_skins_path = mca_asset.sk_path
                if copy_skins_path:
                    copy_skn_weights(bind_dict[mca_asset.asset_id], node_list, copy_skins_path)
                    node_list += [bind_dict[mca_asset.asset_id]]
                    if mca_asset and os.path.exists(mca_asset.skel_path):
                        # Importing an old skel can overwrite markup so restore it. Likely a bug with FBX importing.
                        skel_utils.restore_skeleton_markup(mca_asset.skel_path, bind_dict[mca_asset.asset_id])
            elif 'default' in bind_dict:
                bind_root = bind_dict['default']
                for joint_node in bind_root.listRelatives(ad=True, type=pm.nt.Joint):
                    # Reset rotations so we don't export accidental model changes.
                    for x in attr_utils.ROTATION_ATTRS:
                        joint_node.disconnectAttr(x)
                        joint_node.setAttr(x, 0)

                node_list += [bind_dict['default']]

        # time to export, first a sk, an options skn, and a sm.
        pm.parent(exportable_node_list, None)

        # we will always have an SM, but not always an SK.
        sm_path = mca_asset.sm_path
        skn_path = mca_asset.skin_path
        sk_path = mca_asset.sk_path
        source_ma_path = os.path.join(mca_asset.source_path, 'Model', 'Maya', f'{mca_asset.file_name}.ma')

        do_triangulate = fbx_utils.FBXExportTriangulate(q=True)
        fbx_utils.FBXExportTriangulate(v=False)
        if bind_dict:
            if mca_asset.asset_id in bind_dict or 'default' in bind_dict:
                # only export the SK if we have an actual skeleton.
                fileio.touch_path(sk_path)
                joint_list = pm.ls(node_list, type=pm.nt.Joint)
                if not os.path.exists(mca_asset.skel_path):
                    # If we have no skel registered with this asset export one before we trim joints.
                    root_joint = dag.get_absolute_parent(joint_list[0])
                    if not root_joint.hasAttr('asset_id'):
                        root_joint.addAttr('asset_id', dt='string')
                    root_joint.setAttr('asset_id', mca_asset.asset_id)
                    fileio.touch_path(mca_asset.skel_path)
                    skel_utils.export_skeleton(mca_asset.skel_path, root_joint)
                if joint_list:
                    _trim_exportable_joints(dag.get_absolute_parent(joint_list[0], node_type=pm.nt.Joint))
                fbx_utils.export_fbx(sk_path, node_list)
                if update_skn and sm_export:
                    fileio.touch_path(skn_path, True)
                    shutil.copy2(sk_path, skn_path)

        if sm_export:
            with pm.UndoChunk():
                if mca_asset.asset_id in bind_dict:
                    pm.delete(bind_dict[mca_asset.asset_id])
                if 'default' in bind_dict and pm.objExists(bind_dict['default']):
                    pm.delete(bind_dict['default'])
                if save_source:
                    fileio.touch_path(source_ma_path)
                    scene_utils.save_as(source_ma_path)
                fileio.touch_path(sm_path)
                fbx_utils.export_fbx(sm_path, exportable_node_list)

            pm.undo()
        pm.parent(exportable_node_list, export_group)
        fbx_utils.FBXExportTriangulate(v=do_triangulate)

    if delete_root_after_export and deletable_roots:
        pm.delete(deletable_roots)

    if register_assets:
        assetlist.AssetListRegistry().commit()


def _trim_exportable_joints(skel_root):
    """
    Trim null joints before exporting.

    :param Joint skel_root: Skeletal root joint.
    """

    deletable_joints = [x for x in pm.listRelatives(skel_root, ad=True, type=pm.nt.Joint) if 'null' in x.name()]
    pm.delete(deletable_joints)


def get_all_mca_assets(mca_asset):
    """
    From a Helios build structure find and return all model paths.

    :param MCAAsset mca_asset: The MCA Asset to search though
    :return: A list of all fbx model paths used by this organization structure.
    :rtype: list[MCAAsset, ...]
    """

    return_list = [mca_asset]
    for child_asset in mca_asset.local_asset_list:
        if isinstance(child_asset, str):
            logger.warning(f'Failed to find child asset. {child_asset} of {mca_asset.asset_name}')
            continue
        return_list += get_all_mca_assets(child_asset)
    return return_list


def organize_scene_from_archetype(helios_archetype, asset_name, base_dir=None, modified_base_dir=False, create_directories=False):
    """
    From a Helios Archetype create the organization structure for this scene.

    :param HeliosArchetype helios_archetype: The archetype to convert into a Helios Asset build structure
    :param str asset_name: Name of the new Helios Asset build structure
    :param str base_dir: The base directory this asset should be built.
    :param bool modified_base_dir: If the base directory has been modified from the templates expectations.
    :param bool create_directories: If the folder structure should be built out at the same time.
    """

    mca_asset = helios_registry.create_new_assets_from_archetype(helios_archetype, asset_name, base_dir=base_dir, modified_base_dir=modified_base_dir)
    import_helios_asset(mca_asset, organize_only=True)

    if create_directories:
        create_folder_structure(mca_asset)


def create_folder_structure(mca_asset):
    """
    From the Helios Asset build structure find all model paths and make sure the working directories are available.

    :param MCAAsset mca_asset:  The Helios Asset to build from.
    """

    mca_asset_list = get_all_mca_assets(mca_asset)
    for mca_asset in mca_asset_list:
        # Add trailing slashes so that the directory structure is not clipped.
        meshes_path = mca_asset.meshes_path+'\\'
        textures_path = mca_asset.textures_path+'\\'
        source_path = mca_asset.source_path+'\\'
        for file_path in [meshes_path, textures_path, source_path]:
            fileio.touch_path(file_path)


@decorators.track_fnc
def helios_rbf_cmd():
    """
    Helios UI command for retargeting permutations.
    """

    selection = pm.selected()
    if not selection:
        dialogs.info_prompt(title='No Selection', text='Please make a selection')
        return

    operand_dict = {}
    for node in selection:
        # For each object selected sort it and find our actionable groups.
        if node.hasAttr('helios_name'):
            if node not in operand_dict:
                operand_dict[node] = []

        else:
            object_parent = node.getParent()
            if object_parent and object_parent.hasAttr('helios_name'):
                if object_parent not in operand_dict:
                    operand_dict[object_parent] = []
                if node.getShape():
                    operand_dict[object_parent].append(node)
                else:
                    for x in node.getChildren():
                        if x.getShape():
                            operand_dict[object_parent].append(x)

    helios_rbf(operand_dict)


@ma_decorators.undo_decorator
def helios_rbf(operand_dict):
    """
    Runs the given dict of export groups and their optional children through Helios' automated RBF reprocessing.

    :param dict operand_dict: A dictionary of export groups and optionally the objects in those export groups to be processed.
    """

    helios_archetype = None
    imported_path_dict = {}
    for export_group, exportable_list in operand_dict.items():
        mca_asset = get_asset_from_export_group(export_group)

        # find our archetype if we don't have it yet
        if not helios_archetype:
            for _, helios_archetype in helios_registry.HeliosArchetypeRegistry().NAME_REGISTRY.items():
                if helios_archetype.type == mca_asset.asset_type:
                    break
                helios_archetype = None

        if not helios_archetype:
            continue

        # find our rbf remap from the archetytpe
        rbf_dict = helios_archetype.overfill.get('rbf', {})

        if not rbf_dict:
            continue

        for property_name, value_dict in rbf_dict.items():
            # based on the rbf lookup find our remap targets
            attr_value = getattr(mca_asset, property_name)
            for rbf_name, path_list in value_dict.items():
                if rbf_name == attr_value:
                    # get our source/target import paths
                    source_path, target_path = value_dict[attr_value]
                else:
                    # get our alternate group name
                    alt_name = rbf_name

        # get our nodes to retarget, and the organization structure they're using if we've got sub groups.
        nodes_to_process, organization_dict = get_exportable_meshes_organization(export_group)
        nodes_to_process = exportable_list or nodes_to_process

        if not nodes_to_process:
            continue

        # find our alternative group
        export_group_parent = export_group.getParent()
        alt_group = None
        for node in export_group_parent.getChildren():
            if node != export_group:
                alt_asset = get_asset_from_export_group(node)
                if getattr(alt_asset, property_name) == alt_name:
                    alt_group = node
                    break

        if not alt_group:
            continue

        # grab our source and target objects. if we're doing multiples reuse them.
        if source_path in imported_path_dict:
            source_node = imported_path_dict[source_path]
        else:
            source_node = lists.get_first_in_list(
                pm.ls(fbx_utils.import_fbx(path_utils.to_full_path(source_path)), type=pm.nt.Transform))
            imported_path_dict[source_path] = source_node

        if target_path in imported_path_dict:
            target_node = imported_path_dict[target_path]
        else:
            target_node = lists.get_first_in_list(
                pm.ls(fbx_utils.import_fbx(path_utils.to_full_path(target_path)), type=pm.nt.Transform))
            imported_path_dict[target_path] = target_node

        if not all([source_node, target_node]):
            continue

        for node in nodes_to_process:
            attr_utils.unlock_all_attrs(node)
            pm.makeIdentity(node, apply=True)

        rbf_return_list = node_util.rbf_retarget(source_node, target_node, nodes_to_process)

        # organize our retargeted meshes back into our organization structure.
        for group_name, name_list in organization_dict.items():
            if group_name == 'main':
                parent_group = alt_group
            elif name_list:
                parent_group = pm.group(n=group_name, w=True, em=True)
                parent_group.setParent(alt_group)
            else:
                continue

            for node in rbf_return_list:
                if naming.get_basename(node) in name_list:
                    node.setParent(parent_group)

    pm.delete(list(imported_path_dict.values()))
