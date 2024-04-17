#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports

# software specific imports
import pymel.core as pm
import maya.mel as mel
#  python imports
from mca.common import log
from mca.common.utils import lists
from mca.mya.utils import naming


logger = log.MCA_LOGGER


def get_between_nodes(first, last, node_type=None):
    """
    Returns in between nodes between the first and last.

    :param pm.nt.DagNode first: Start node to trace between nodes.
    :param pm.nt.DagNode last: End node to trace between nodes.
    :param pm.nt.PyNode node_type: Node type to return.
    :return: Returns a list of the first, last, and in between joints.
    :rtype: list(pm.nt.DagNode)
    """

    if not isinstance(first, pm.nt.DagNode) or not isinstance(last, pm.nt.DagNode):
        first = pm.PyNode(first)
        last = pm.PyNode(last)

    node_list = list()
    node_list.append(last)
    current_node = last
    while first != current_node:
        current_node = current_node.getParent() if current_node else None
        if not current_node:
            logger.warning('{0} is not in the hierarchy of {1}'.format(first, last))
        node_list.append(current_node)

    if node_type:
        node_list = [node for node in node_list if isinstance(node, node_type)]

    node_list.reverse()

    return node_list


def parent_shape_node(from_objs,
                      to_obj,
                      maintain_offset=False,
                      replace=True,
                      freeze_transform=True,
                      delete_original=True,
                      swap_names=True):
    """
    parents the shape node on from_object to to_object
    """
    if not isinstance(from_objs, list):
        from_objs = [from_objs]

    if freeze_transform:
        for obj in from_objs:
            pm.makeIdentity(obj, apply=1, t=1, r=1, s=0)

    if maintain_offset:
        for obj in from_objs:
            pm.parent(obj, to_obj)
            pm.makeIdentity(obj, apply=1, t=1, r=1, s=0)
            pm.parent(obj, w=True)

    if swap_names and to_obj.getShapes():
        to_object_name = naming.get_basename(str(to_obj.getShapes()[0]))
        for obj in from_objs:
            obj.getShapes()[0].rename(to_object_name)

    if replace:
        old_shapes = to_obj.getShapes()
        if old_shapes:
            pm.delete(old_shapes)

    new_shape = None
    for obj in from_objs:
        new_shape = pm.parent(obj.getShapes(), to_obj, add=1, s=1)[0]
        # gets around double namespaces.
        shape_name = naming.get_basename(to_obj.getShapes()[0])
        for i, shape in enumerate(to_obj.getShapes()):
            shape.rename(shape_name) if i == 0 else shape.rename(shape_name + str(i + 1))
    if delete_original:
        pm.delete(from_objs)

    return new_shape


def get_all_parents(obj, node_type=None):
    """
    Returns a list of every parent from the given node to the scene root.
    If a node type is passed it will give the highest parent of that node type.

    For instance if a skeleton is inside a group and one of the child joints is the obj.
    If you filter for Joints instead of returning the group as one of the parents
    it will only return to the root joint of the skeletal hierarchy.

    :param pm.nt.DagNode obj: The starting node to check for parents.
    :param nodetype node_type: The filtering node type we want to check for
    :return: Returns a list of every parent from the given node to the scene root.
    :rtype: list(pm.nt.DagNode)
    """

    result = list()
    obj = pm.PyNode(obj)
    parent = obj.getParent()

    if parent:
        if node_type and not isinstance(parent, node_type):
            return result
        result = [parent] + get_all_parents(obj.getParent(), node_type=node_type)

    return result


def get_absolute_parent(obj_node, node_type=None, inclusive=True):
    """
    Return the most toplevel parent from a given node

    :param Transform obj_node: The transform to search from.
    :param Nodetype node_type: A pymel nodetype
    :param bool inclusive: If the current object should be included. If no parents are found it will return itself.
    :return: The top level transform object, or if inclusive itself.
    :rtype: Transform
    """

    if not isinstance(obj_node, pm.nt.Transform):
        return None

    last_parent = obj_node if inclusive else None

    found_parent = obj_node.getParent()
    while found_parent:
        if node_type and not isinstance(found_parent, node_type):
            found_parent = None
        else:
            last_parent = found_parent
            found_parent = found_parent.getParent()

    return last_parent


def get_absolute_child(start_node, node_type, inclusive=True):
    """
    Wrapper for _get_deepest_child used to return only the found node.

    :param Transform start_node:
    :param class node_type: PyNode class of the type to filter by.
    :param bool inclusive: If there are no children the starting node should be returned.
    :return: The lowest found child or itself (inclusive.
    :rtype: Transform
    """
    deepest_child, _ = _get_deepest_child(start_node, node_type=node_type)
    if not inclusive and deepest_child == start_node:
        return None
    return deepest_child


def _get_deepest_child(start_node, depth=0, node_type=None):
    """
    Check child depth and return the lowest found node.

    :param Transform start_node: The node to find the deepest child of.
    :param int depth: Current depth level
    :param class node_type: Filter type. EG: pm.nt.Joint
    :return: The lowest found child and their depth level
    :rtype: Transform, int
    """
    if not isinstance(start_node, pm.nt.Transform):
        return

    found_children = start_node.getChildren()

    deepest_child = start_node
    deepest_depth = depth
    for child_node in found_children:
        child_node, child_depth = _get_deepest_child(child_node, depth=depth + 1, node_type=node_type)
        if node_type and not isinstance(child_node, node_type):
            continue
        if child_depth > deepest_depth:
            deepest_child = child_node
            deepest_depth = child_depth
    return deepest_child, deepest_depth


def get_children_in_order(start_node, node_type=None, start=True):
    """
    Recursively get children to preserve order.

    :param Transform start_node: The starting DAG node to traverse the hierarchy.
    :param PyNode node_type: The PyNode class to filter by.
    :param bool start: If this is the first run of the loop. It'll include the root otherwise it'll skip it.
    :return: The list of children nodes in their DAG order.
    :rtype: list[Transform]
    """
    if not isinstance(start_node, pm.nt.Transform):
        logger.warning(f'{start_node} is not a Transform')
        return

    found_children = start_node.getChildren(type=node_type) if node_type else start_node.getChildren(type=pm.nt.Transform)
    ordered_list = [start_node] + found_children.copy() if start else found_children.copy()
    for child_node in found_children:
        child_list = get_children_in_order(child_node, node_type, False)
        ordered_list += child_list

    return ordered_list


def get_node_color_data(node):
    """
    Returns the color data in the given Maya node.
    >>> get_node_color_data('nurbsCircleShape1')
    {'overrideEnabled': True, 'overrideColorRGB': [0.4, 0.07, 0.07, 'overrideRGBColors': True,
    'useOutlinerColor': False, 'outlinerColor': [0.0, 0.0, 0.0]}

    :param str or pm.PyNode node: Maya we want to retrieve color of.
    :return: dictionary contianing all Maya color related color.
    :rtype: dict

    ..note:: colos are returned as a list of flota values in 0.0 to 1.0 range.
    """

    node = pm.PyNode(node)
    enabled = node.attr('overrideEnabled').get()
    use_outliner = node.attr('useOutlinerColor').get()
    outliner_color = node.attr('outlinerColor').get()
    override_rgb_colors = node.attr('overrideRGBColors').get()
    override_color = node.attr('overrideColor').get()

    override_rgb = [0.0, 0.0, 0.0]
    if override_rgb_colors:
        override_rgb = node.attr('overrideColorRGB').get()

    return {
        'overrideColor': override_color,
        'overrideEnabled': enabled,
        'overrideColorRGB': override_rgb,
        'overrideRGBColors': override_rgb_colors,
        'useOutlinerColor': use_outliner,
        'outlinerColor': outliner_color
    }


def set_node_color(node, color, outliner_color=None, use_outliner_color=False):
    """
    Sets the given Maya object override color. PyNode can represent an object or a shape.

    :param pm.PyNode or str or list(MObject) or list(str) node: PyMEL node we want to change color of.
    :param pm.Color or tuple(float, float, float) color: RGB color to set in 0 to 1 range.
    :param  pm.Color or tuple(float, float, float) or None outliner_color: RGB color to set to outliner
        item in 0 to 1 range.
    :param bool use_outliner_color: whether or not to apply outliner color.
    """

    nodes = lists.force_list(node)
    nodes = [pm.PyNode(mobj) for mobj in nodes]

    for node in nodes:
        if isinstance(color, int):
            color_attr = node.attr('overrideColor')
            enabled = node.attr('overrideEnabled')
            if not enabled.get():
                enabled.set(True)
            color_attr.set(color)
        else:
            color_attr = node.attr('overrideColorRGB')
            enabled = node.attr('overrideEnabled')
            override_rgb_colors = node.attr('overrideRGBColors')
            if not enabled.get():
                enabled.set(True)
            if not override_rgb_colors.get():
                override_rgb_colors.set(True)
            color_attr.set(color)

        if outliner_color:
            use_outliner_attr = node.attr('useOutlinerColor')
            if use_outliner_color:
                use_outliner_attr.set(True)
            node.attr('outlinerColor').set(outliner_color)

    # refresh outliner of outliner color has changed
    if outliner_color:
        mel.eval('AEdagNodeCommonRefreshOutliners();')