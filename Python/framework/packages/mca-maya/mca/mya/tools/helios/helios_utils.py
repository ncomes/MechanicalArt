#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains utility functions for Mercury, and the wizard.
"""

# python imports
import os
import shutil

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import fileio, path_utils, list_utils

from mca.mya.animation import camera_utils
from mca.mya.rigging import joint_utils, skin_utils
from mca.mya.modeling import geo_utils, material_utils
from mca.mya.utils import attr_utils, dag_utils, fbx_utils, naming, scene_utils

from mca.common import log
logger = log.MCA_LOGGER

NODE_WHITE_LIST = (pm.nt.Transform, pm.nt.Mesh, pm.nt.SkinCluster, pm.nt.BlendShape, pm.nt.DagPose,
                   pm.nt.Phong, pm.nt.Blinn, pm.nt.Lambert, pm.StandardSurface, pm.nt.ShadingEngine, pm.nt.GroupId,
                   pm.nt.GroupParts, pm.nt.MaterialInfo, pm.nt.Reverse, pm.nt.RemapValue, pm.nt.Bump2d,
                   pm.nt.Place2dTexture, pm.nt.File)


def import_asset(asset_entry, simple_materials=False, with_skinning=False, root_joint_dict=None):
    """
    Create the organization group for the asset, and import the meshes when possible.

    :param asset_entry:
    :param simple_materials:
    :param with_skinning:
    :param root_joint_dict:
    :return:
    """
    if root_joint_dict is None:
        root_joint_dict = {}

    asset_name = asset_entry.asset_name
    if 'right' in asset_entry.asset_subtype:
        asset_name = f'{asset_entry.asset_name}_right'
    elif 'left' in asset_entry.asset_subtype:
        asset_name = f'{asset_entry.asset_name}_left'
    organization_group = pm.group(n=asset_name, em=True, w=True)
    attr_dict = asset_entry.get_data_dict()
    attr_dict.update({'id': asset_entry.asset_id})

    attr_dict.pop('local_asset_list', None)
    local_asset_list = asset_entry.local_asset_list
    attr_utils.set_compound_attribute_groups(organization_group, 'asset', attr_dict)

    mesh_path = path_utils.to_full_path(attr_dict.get('mesh_path', None))
    if mesh_path:
        # Handle mesh importing here. Otherwise we're just creating an organization group.
        if not os.path.exists(mesh_path):
            logger.error(f'{mesh_path} does not exist! Sync your files.')
        else:
            imported_node_list = import_source_file(mesh_path, simple_materials)
            parentable_node_list = []
            shaped_transform_list = []
            for node in imported_node_list:
                if isinstance(node, pm.nt.Transform):
                    # if the node is a transform
                    if node.getShape():
                        # if it is a shaped transform
                        shaped_transform_list.append(node)

                    if node.getParent():
                        # if it has a parent
                        continue
                    else:
                        if isinstance(node, (pm.nt.Locator, pm.nt.Joint)):
                            # If it is either a locator or joint
                            continue
                    # Else add it to our parentable list.
                    parentable_node_list.append(node)

            if parentable_node_list:
                pm.parent(parentable_node_list, organization_group)

            # Handle skinning here.
            imported_joints = pm.ls(imported_node_list, type=pm.nt.Joint)
            if not with_skinning:
                # We don't want the meshes skinned. (CA might be just doing geo changes)
                pm.delete(imported_joints)
                attr_utils.set_attr_state(shaped_transform_list, False) # Unlock transform attrs. (Incase it was skinned)
            elif shaped_transform_list:
                # If we want it to be skinned, and we have skinnable meshes.
                skel_path = asset_entry.skeleton_path
                # $HACK converting the single slash to a double prevent's Maya from replacing the path value on FBX import, it's
                # An absolutely dumb work around to a bug with Maya's FBX import replacing escape characters.
                register_skel_path = path_utils.to_relative_path(skel_path).replace('\\', '\\\\')
                parent_skel_path_list = asset_entry.parent_skeletons()
                imported_root = None
                if imported_joints:
                    imported_root = dag_utils.get_absolute_parent(imported_joints[0], pm.nt.Joint)

                root_joint = root_joint_dict.get(register_skel_path)
                if not root_joint:
                    # We didn't find our skeleton in the lookup, see if an inherited skeleton is in here.
                    for parent_skel_path in parent_skel_path_list:
                        if path_utils.to_relative_path(parent_skel_path) in root_joint_dict:
                            # We have an inherited skeleton in the scene, so bind to that. But merge in the local skel.
                            root_joint = root_joint_dict[path_utils.to_relative_path(parent_skel_path)]
                            root_joint_dict[path_utils.to_relative_path(parent_skel_path)] = root_joint
                            root_joint = joint_utils.import_merge_skeleton(parent_skel_path, root_joint)
                            break

                if not root_joint and imported_joints:
                    # We could not find a skeleton root already available to bind to. Use the imported root, but
                    # import merge to ensure we have all expected joints.
                    root_joint = dag_utils.get_absolute_parent(imported_joints[0], pm.nt.Joint)
                    if not root_joint.hasAttr('skel_path'):
                        root_joint.addAttr('skel_path', dt='string')
                        root_joint.setAttr('skel_path', register_skel_path)
                    root_joint_dict[register_skel_path] = root_joint
                    root_joint = joint_utils.import_merge_skeleton(skel_path, root_joint)

                if not root_joint:
                    # The skeleton was not in the scene, was not inherited, and was not imported.
                    # Import it ourselves then.
                    root_joint = joint_utils.import_merge_skeleton(skel_path, root_joint)

                if root_joint:
                    # we should have a skel root by now. Otherwise we'll skip skin binding.
                    if imported_joints:
                        # We have imported joints, but we already have a valid skel root.
                        # If these are one and the same, the rebind fnc will just skip it.
                        skin_utils.rebind_meshes_to_skel(shaped_transform_list, root_joint)
                        if imported_root != root_joint:
                            pm.delete(imported_joints)

                    found_skin_path = asset_entry.skin_path
                    if not os.path.exists(found_skin_path):
                        found_skin_path = asset_entry.parent_skins()
                    skin_utils.bind_and_copy_from_file(shaped_transform_list, root_joint, found_skin_path, True)
    for child_entry in local_asset_list:
        import_group, root_joint_dict = import_asset(child_entry, with_skinning=with_skinning, root_joint_dict=root_joint_dict)
        if import_group:
            import_group.setParent(organization_group)

    return organization_group, root_joint_dict


def import_source_file(file_path, simple_materials=False, use_namespace=True):
    return_list = []
    imported_node_list = []
    things_to_delete = []
    if file_path.lower().endswith('.fbx'):
        if use_namespace:
            current_namespace = pm.namespaceInfo(currentNamespace=True)
            current_namespace = current_namespace if current_namespace != ':' else None
        else:
            current_namespace = None

        imported_node_list = fbx_utils.import_fbx(file_path, current_namespace)
        material_list = [x for x in imported_node_list if isinstance(x, (pm.nt.Phong, pm.nt.Blinn, pm.nt.Lambert, pm.StandardSurface))]
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


def export_asset(exportable_group_list, asset_entry=None, update_skn=False, save_source=False, update_thumbnail=False):
    # Always save before we do something stupid.
    scene_utils.backup_scene('helios_export')

    if not isinstance(exportable_group_list, list):
        exportable_group_list = [exportable_group_list]

    exported_file_list = []

    delete_skel = []
    root_joint_dict = {}
    for export_group in exportable_group_list:
        if not (len(exportable_group_list) == 1 and asset_entry):
            # This will allow for some clever overrides, but should almost never be used.
            # NOTE: this will only allow a single level export. No nested assets.
            asset_entry = get_asset_from_group(export_group)

        if asset_entry.mesh_path:
            exportable_node_list = get_exportable_nodes(export_group)
            if not exportable_node_list:
                continue

            if save_source:
                source_path = os.path.join(asset_entry.source_path, 'Maya', f'{asset_entry.asset_name}.ma')
                fileio.touch_path(source_path, True)
                pm.saveAs(source_path, f=True)
                exported_file_list.append(source_path)

            # Note we're not using this list for exporting it's just for cleanup, and later skin binding.
            all_shaped_transform_list = []
            for node in exportable_node_list[:]:
                for x in [node] + pm.listRelatives(node, ad=True, type=pm.nt.Transform):
                    if x.getShape():
                        if not skin_utils.get_skincluster(x):
                            # If we have no skin cluster sanitize the mesh real quick.
                            # This is mostly to keep new character meshes clean.
                            # Song and dance here if the node is passed through apply cube trick it's technically not
                            # the same object as it was before. So remove it and add it from the exportable node list.
                            replace = False
                            if x is node:
                                replace = True
                                exportable_node_list.remove(node)

                            x = geo_utils.apply_cube_trick(x)

                            if replace:
                                exportable_node_list.append(x)
                        all_shaped_transform_list.append(x)

            root_joint=None
            if 'model' in asset_entry.asset_type:
                skel_path = asset_entry.skeleton_path
                register_skel_path = path_utils.to_relative_path(skel_path).replace('\\', '\\\\')
                if not root_joint_dict:
                    # lets pre prime this so we don't do it every time.
                    for root_joint in joint_utils.get_hierarchy_bind_roots(export_group):
                        if not root_joint:
                            continue
                        # !BUG Maya removes the path seperators from attrs, so instead of storing the relative path,
                        # we're storing the file name to identify skeletons, this means we cannot refresh them only once here.
                        # we can refresh skeletons for each export but I don't think the time cost is worth it.
                        existing_skel_path = root_joint.getAttr('skel_path') if root_joint.hasAttr('skel_path') else ''
                        if existing_skel_path:
                            root_joint_dict[existing_skel_path] = root_joint

                # All model type entries should be exported with a skeleton. So lets get us one.
                if register_skel_path in root_joint_dict:
                    root_joint = root_joint_dict[register_skel_path]
                else:
                    # If we have no match import the skel associated with the asset.
                    skel_path = asset_entry.skeleton_path
                    if skel_path and os.path.exists(skel_path):
                        root_joint = joint_utils.import_merge_skeleton(asset_entry.skeleton_path)
                        delete_skel.append(root_joint)
                    if not root_joint:
                        # We failed to import for some reason. So create a new joint.
                        cmds.select(None)
                        root_joint = pm.Joint(n='root')

                # Once we have a skeleton rebind any meshes we're exporting to the same skel.
                nodes_to_rebind = []
                for node in all_shaped_transform_list:
                    # Check for weird skin bindings.
                    node_bind_root = joint_utils.get_bind_root(node)
                    if nodes_to_rebind and node_bind_root != root_joint:
                        nodes_to_rebind.append(node)
                if nodes_to_rebind:
                    # Switch them all to same root for exporting.
                    skin_utils.rebind_meshes_to_skel(nodes_to_rebind, root_joint)

                # Now any remaining unbound meshes should be bound to the skel.
                skin_utils.bind_and_copy_from_file(all_shaped_transform_list, root_joint, asset_entry.skin_path, True)
                pm.parent(exportable_node_list, None)

                if naming.get_basename(root_joint) != 'root':
                    # Make sure our latest skel is named root.
                    og_root = list_utils.get_first_in_list(pm.ls('root'))
                    if og_root:
                        og_root.rename('root1')
                root_joint.rename('root')

            # add in our skel root if we have one.
            fbx_utils.export_fbx(asset_entry.mesh_path, exportable_node_list+[root_joint] if root_joint else [])
            exported_file_list.append(asset_entry.mesh_path)
            if update_thumbnail:
                def get_midpoint(point_array):
                    mid_point = []
                    for i in range(3):
                        mid_point.append((point_array[i] + point_array[i + 3]) / 2.0)
                    return mid_point

                point_array = pm.exactWorldBoundingBox(exportable_node_list)
                midpoint = get_midpoint(point_array)

                new_cam_transform, new_cam_shape = pm.camera()
                new_cam_transform.rename('capture_cam')
                new_cam_transform.t.set(-200, 200, 200) if 'left' in asset_entry.asset_subtype else new_cam_transform.t.set(200, 200, 200)
                pm.mel.eval(f'cameraMakeNode 2 "{new_cam_transform.name()}";')
                cam_grp = new_cam_transform.getParent()
                cam_aim = cam_grp.getChildren()[-1]
                cam_aim.t.set(midpoint)

                pm.select(exportable_node_list)
                pm.viewFit(new_cam_shape)
                # Push camera in since viewFit is only filling about 50% of the space.
                # This takes it from 35 default to 60
                new_cam_shape.focalLength.set(60)

                asset_icon_path = f'{asset_entry.mesh_path[:-3]}jpg'
                fileio.touch_path(asset_icon_path, True)
                camera_utils.playblast_images(asset_icon_path, new_cam_transform, exportable_node_list, resolution=[124, 124], bg_color=[.5, .5, .5])
                exported_file_list.append(asset_icon_path)
                pm.delete(cam_grp)
            if update_skn:
                fileio.touch_path(asset_entry.skin_path)
                shutil.copyfile(asset_entry.mesh_path, asset_entry.skin_path)
                exported_file_list.append(asset_entry.skin_path)
            if not delete_skel and root_joint:
                # If we're not deleting the skeleton.
                # Grab the local skel path and see if it's live and not on disk.
                skel_path = path_utils.to_full_path(asset_entry._skeleton_path)
                if skel_path and not os.path.exists(skel_path):
                    # If we have a skeleton path, but it doesn't exist on disk.
                    pm.select([root_joint]+pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint))
                    fileio.touch_path(skel_path)
                    pm.exportSelected(skel_path, type='mayaAscii')
                    exported_file_list.append(skel_path)


            pm.parent(exportable_node_list, export_group)

            # Register our new asset but do not commit it.
            asset_entry.register(False)

    if delete_skel:
        pm.delete(delete_skel)
    # Commit all our export changes.
    asset_registry = assetlist.get_registry()
    if asset_registry.DIRTY:
        exported_file_list.append(assetlist.REGISTRY_FILE_PATH)
    asset_registry.commit()
    return exported_file_list


def get_asset_from_group(export_group):
    """
    From a given export group generate an asset from the markup.

    :param Transform export_group:
    :return: The generated asset.
    :rtype: Asset
    """
    if not export_group or not export_group.hasAttr('asset_id'):
        logger.error(f'{export_group} does not have proper Asset markup.')
        return

    data_dict = {}
    for attr in export_group.asset.getChildren():
        data_dict[attr.name().split('.')[-1].replace('asset_', '')] = attr.get()
    asset_id = data_dict.pop('id')
    asset_entry = assetlist.Asset(asset_id, data_dict)

    local_asset_list = []
    for child_node in export_group.getChildren():
        # We'll need to recursively add any children export groups.
        if child_node.hasAttr('asset_id'):
            child_asset = get_asset_from_group(child_node)
            if child_asset:
                local_asset_list.append(child_asset)
    asset_entry.local_asset_list+=local_asset_list
    return asset_entry


def get_all_exportable_groups(node=None):
    """
    From a given node, grab all export groups in its hierarchy. (Inclusive)
    Otherwise collect all export groups in the scene.

    :param Transform node: The head of the hierarchy you want to export.
    :return: A list of all the valid exportable transforms.
    :rtype: list[Transform]
    """

    return_list = []
    if node:
        for child_node in [node]+pm.listRelatives(node, ad=True, type=pm.nt.Transform):
            if child_node.hasAttr('asset_id'):
                return_list.append(child_node)
    else:
        for attr in pm.ls('*.asset_id'):
            export_group = attr.node()
            return_list.append(export_group)
    return return_list


def get_exportable_nodes(export_group):
    """
    From a given export group return all objects to be exported.

    :param Transform export_group:
    :return: A list of all the valid exportable transforms.
    :rtype: list[Transform]
    """
    if not export_group or not export_group.hasAttr('asset_id'):
        # we neither have a valid export group, nor asset_id.
        return []

    children_node_list = export_group.getChildren()
    exportable_node_list = []
    blendshape_targets = []
    for node in children_node_list:
        if node.hasAttr('asset_id'):
            # Exclude other export groups, they should be handled independently.
            continue

        node_shape = node.getShape()
        if node_shape:
            blend_node = list_utils.get_first_in_list(node_shape.listConnections(type=pm.nt.BlendShape))
            if blend_node:
                blendshape_targets += pm.blendShape(blend_node, q=True, target=True)

        node_children = node.getChildren()
        if node_children:
            # We're recursively running this to find and delete blendshape targets. They're restored on import.
            # They become embedded in the FBX file.
            get_exportable_nodes(node)

        exportable_node_list.append(node)

    exportable_node_list = [x for x in exportable_node_list if x not in blendshape_targets]
    pm.delete(blendshape_targets)
    return exportable_node_list



