#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with Maya scene
"""

# System global imports
import os
import traceback
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
#  python imports
from mca.common import log
from mca.mya.utils import maya_utils, node_utils
from mca.common.utils import fileio
from mca.mya.modifiers import ma_decorators

logger = log.MCA_LOGGER
MAX_BACKUPS = 10


def delete_unknown_nodes():
    """
    Find all unknown nodes in current scene and deletes them.
    """

    unknown = pm.ls(type='unknown')
    deleted = list()
    for n in unknown:
        if pm.objExists(n):
            pm.lockNode(n, lock=False)
            pm.delete(n)
            deleted.append(n)

    if deleted:
        logger.info('Deleted unknowns: {}'.format(deleted))
    return deleted


def delete_turtle_nodes():
    """
    Find all turtle nodes in current scene and delete them.
    """

    plugin_list = pm.pluginInfo(query=True, pluginsInUse=True) or list()
    turtle_nodes = list()
    for plugin in plugin_list:
        if plugin[0] == 'Turtle':
            turtle_types = ['ilrBakeLayer',
                            'ilrBakeLayerManager',
                            'ilrOptionsNode',
                            'ilrUIOptionsNode']
            turtle_nodes = maya_utils.delete_nodes_of_type(turtle_types)
            break

    if turtle_nodes:
        logger.info('Removed Turtle nodes: {}'.format(turtle_nodes))
    return turtle_nodes

def delete_unused_plugins():
    """
    Removes all nodes in current scene that belongs to unused plugins (plugins that are not loaded).
    """

    # this functionality is not available in old Maya versions
    list_pm = dir(pm)
    if 'unknownPlugin' not in list_pm:
        return []

    unknown_nodes = pm.ls(type='unknown')
    if unknown_nodes:
        return []

    unused = list()
    unknown_plugins = pm.unknownPlugin(query=True, list=True) or list()
    for unknown_plugin in unknown_plugins:
        try:
            pm.unknownPlugin(unknown_plugin, remove=True)
        except Exception:
            continue
        unused.append(unknown_plugin)

    if unused:
        logger.info('Removed unused plugins: {}'.format(unused))
    return unused


def delete_garbage():
    """
    Delete all garbage nodes from current scene.
    """

    straight_delete_types = list()
    if maya_utils.get_version() > 2014:
        straight_delete_types += ['hyperLayout', 'hyperView']       # Maya 2014 crashes when tyring to remove those
        if 'hyperGraphLayout' in straight_delete_types:
            straight_delete_types.remove('hyperGraphLayout')

    deleted_nodes = maya_utils.delete_nodes_of_type(straight_delete_types)
    check_connection_node_type = ['shadingEngine', 'partition', 'objectSet']
    check_connection_nodes = list()
    for check_type in check_connection_node_type:
        nodes_of_type = pm.ls(type=check_type)
        check_connection_nodes += nodes_of_type

    garbage_nodes = deleted_nodes if deleted_nodes else list()
    nodes_to_skip = ['characterPartition']
    for connection_node in check_connection_nodes:
        if (not connection_node or not pm.objExists(connection_node)) or connection_node in nodes_to_skip:
            continue
        if node_utils.is_empty(connection_node):
            pm.lockNode(connection_node, lock=False)
            try:
                pm.delete(connection_node)
            except Exception:
                pass
            if not pm.objExists(connection_node):
                garbage_nodes.append(connection_node)

    if garbage_nodes:
        logger.info('Delete Garbage Nodes: {}'.format(garbage_nodes))
    return garbage_nodes

def delete_unused_shader_nodes():
    """
    Deletes all unused shader nodes from this scene.
    """

    temp_cube = None
    try:
        # Since Maya 2020 an error is thrown when running Delete Unused Nodes if the StandardSurface default shader is
        # unassigned. We create a temporary object, assign the default StandardSurface material to it, then delete
        # Unused and delete the sphere
        temp_cube = pm.polyCube(name='TEMP_StandardSurface_Assignment')[0]
        temp_standard_shader = pm.sets( renderable=True, noSurfaceShader=True, empty=True, name='standardSurface1SG')
        standard_material = pm.PyNode('standardSurface1')
        standard_material.outColor.connect(temp_standard_shader.surfaceShader)
        pm.sets(temp_standard_shader, edit=True, forceElement=temp_cube)
        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    except Exception as exc:
        logger.warning('Error while deleting unused nodes: "{}"'.format(exc))
    finally:
        if temp_cube:
            pm.delete(temp_cube)


def delete_empty_namespaces():
    """
    Removes all namespaces from bottom up to remove children namespaces first.
    """
    deleted_ns = list()
    namespace_list = list()
    for ns in pm.listNamespaces( recursive  =True, internal =False):
        namespace_list.append(ns)

    # reverse iterate through the contents of the list to remove the deepest layers first
    for ns in reversed(namespace_list):
        if not pm.namespaceInfo(ns, ls=True):
            deleted_ns.append(ns)
            pm.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
    return deleted_ns

def delete_empty_display_layers():
    """
    Deletes all display layers that are empty within current scene.
    """

    empty_layer_list = list()
    default_display_layer = pm.PyNode('defaultLayer') if pm.objExists('defaultLayer') else None
    for display_layer in pm.ls(type=pm.nt.DisplayLayer):
        if display_layer != default_display_layer and not display_layer.listMembers():
            empty_layer_list.append(display_layer)

    pm.delete(empty_layer_list)
    return empty_layer_list

def delete_render_layers():
    """
    Deletes all render layers in current scene (except default render layer).
    """

    render_layers = [x for x in pm.ls(type='renderLayer') if x != pm.nt.RenderLayer('defaultRenderLayer')]
    if render_layers:
        pm.delete(render_layers)
        logger.info('Delete Render Layers: {}'.format(render_layers))
    return render_layers

def delete_orphaned_controller_tags():
    """
    Deletes all controller tags that are orphaned.
    """

    controller_tags = [x for x in pm.ls(
        type=pm.nt.Controller) if x.exists() and not x.controllerObject.listConnections()]
    if controller_tags:
        pm.delete(controller_tags)
        logger.info('Delete Orphaned Controller Tags: {}'.format(controller_tags))
    return controller_tags

def delete_orphaned_group_id_nodes():
    """
    Deletes all group id nodes that are orphaned.
    """

    group_id_nodes = [x for x in pm.ls(type='groupId') if not x.listConnections()]
    if group_id_nodes:
        pm.delete(group_id_nodes)
        logger.info('Delete Orphaned Group ID Nodes: {}'.format(group_id_nodes))
    return group_id_nodes

def delete_orphaned_time_editor_tracks():
    """
    Deletes all time editor tracks that are orphaned in current scene.
    """

    time_editor_tracks = [x for x in pm.ls(type='timeEditorTracks') if not x.listConnections()]
    if time_editor_tracks:
        pm.delete(time_editor_tracks)
        logger.info('Delete Orphaned Time Editor Track Nodes: {}'.format(time_editor_tracks))
    return time_editor_tracks

def delete_orphaned_graph_editor_infos():
    """
    Deletes all the graph editor info nodes that are orphaned in current scene.
    """

    graph_editor_info = [x for x in pm.ls(type='nodeGraphEditorInfo') if not x.listConnections()]
    if graph_editor_info:
        pm.delete(graph_editor_info)
        logger.info('Delete Orphaned Graph Editor Info Nodes: {}'.format(graph_editor_info))
    return graph_editor_info

def delete_orphaned_reference_nodes():
    """
    Deletes all the reference nodes that are unlocked and orphaned in current scene.
    """

    reference_nodes = [x for x in pm.ls(type='reference') if not x.listConnections() and not x.isLocked()]
    if reference_nodes:
        pm.delete(reference_nodes)
        logger.info('Delete Orphaned Reference Nodes: {}'.format(reference_nodes))
    return reference_nodes

def delete_orphaned_nodes():
    """
    Deletes all orphaned nodes from current scene.
    """
    deleted_nodes = []
    deleted_nodes += delete_orphaned_controller_tags()
    deleted_nodes += delete_orphaned_group_id_nodes()
    deleted_nodes += delete_orphaned_time_editor_tracks()
    deleted_nodes += delete_orphaned_graph_editor_infos()
    deleted_nodes += delete_orphaned_reference_nodes()
    return deleted_nodes


def clean_scene():
    """
    Cleans invalid nodes from current scene.
    """
    deleted_nodes = []
    deleted_nodes += delete_unknown_nodes()
    deleted_nodes += delete_turtle_nodes()
    deleted_nodes += delete_unused_plugins()
    deleted_nodes += delete_garbage()
    delete_unused_shader_nodes()
    deleted_nodes += delete_empty_namespaces()
    deleted_nodes += delete_empty_display_layers()
    deleted_nodes += delete_render_layers()
    deleted_nodes += delete_orphaned_nodes()
    return deleted_nodes


def backup_scene(backup_name=None):
    """
    Save a copy of the scene to our backup directory on the C drive.

    :param str backup_name: Name of the backup file. Otherwise, it'll default to "mca_backup"
    """
    scene_name = pm.sceneName()

    backup_name = backup_name or 'mca_backup'

    clean_scene()
    backup_dir = os.path.join(r'C:\export_backup', '')
    fileio.touch_path(backup_dir)
    files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith('.ma') and backup_name in f]

    files.sort(key=os.path.getmtime)
    if len(files) >= MAX_BACKUPS:
        backup_path = files[0]
    else:
        index = 1
        while index <= len(files) + 1 and index <= MAX_BACKUPS:
            backup_path = os.path.join(backup_dir, f'{backup_name}{index}.ma')
            index += 1
    pm.saveAs(backup_path, f=True)

    if scene_name:
        pm.renameFile(scene_name)


@ma_decorators.not_undoable_decorator
def clean_imported_nodes(new_nodes):
    """
    Removes anything that is not a mesh or transform from a given list of objects in Maya

    :param list(str) new_nodes: List of nodes to clean
    :return: String names of transform node(s)
    :rtype: list(str)
    """

    m_sel = om.MSelectionList()
    clean_node = []
    junk_list = []

    for x, node in enumerate(new_nodes):
        m_sel.add(node)
        m_obj_node = om.MObject()
        m_sel.getDependNode(x, m_obj_node)
        node_type = m_obj_node.apiTypeStr()
        if node_type == 'kTransform':
            clean_node.append(node.replace("|", ""))
        elif node_type != 'kMesh' and node_type != 'kTransform':
            junk_list.append(node)

    pm.sets('initialShadingGroup', fe=clean_node)
    for junk_item in junk_list:
        if cmds.objExists(junk_item):
            pm.delete(junk_item)
    delete_garbage()

    return clean_node


def save_as(file_path):
    """
    Saves Maya scene into the given file path.

    :param str file_path: file path where we want to store Maya scene file.
    :return: True if the save as operation was completed successfully; False otherwise.
    :rtype: bool
    """

    saved = False
    if not file_path:
        return saved

    logger.debug('Saving "{}"'.format(file_path))

    file_type = 'mayaAscii'
    if file_path.endswith('.mb'):
        file_type = 'mayaBinary'

    try:
        pm.renameFile(file_path)
        pm.saveFile(type=file_type)
        saved = True
    except Exception:
        logger.error(str(traceback.format_exc()))
        saved = False

    if saved:
        logger.debug('Scene saved successfully into: {}'.format(file_path))
    else:
        if not pm.about(batch=True):
            pm.confirmDialog(message='Warning:\n\nMaya was unable to save!', button='Confirm')
        logger.warning('Scene not saved: {}'.format(file_path))

    return saved
