#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fncs related to interacting with Maya DAG objects.
"""
# System global imports

# software specific imports
import pymel.core as pm
import maya.mel as mel

#  python imports
from mca.common.utils import list_utils

from mca.mya.rigging import skin_utils
from mca.mya.utils import attr_utils, naming

from mca.common import log
logger = log.MCA_LOGGER


def create_aligned_parent_group(node, suffix=None, attr_name=None, group_attr=None, orient_obj=None):
    """
    Create an alignment group and set it to the parent of the passed node.

    :param Transform node: A transform node to create a parent of.
    :param str suffix: A suffix to add to the new align group.
    :param str attr_name: The name that should be used to connect from the passed node to the alignment group.
    :param str group_attr: The name that should be used to connect the align group to the passed node.
    :param Transform orient_obj: If the align group should use a different orientation target.
    :return: The newly created alignment group
    :rtype: Transform
    """
    if not isinstance(node, pm.nt.Transform):
        return

    attr_name = attr_name or 'align_group'
    group_attr = group_attr or 'align_object'
    suffix = suffix or 'align'

    node_name = naming.get_basename(node)
    group_name = f'{node_name}_{suffix}'

    align_group = pm.group(n=group_name, em=True)
    align_group.addAttr(group_attr, at='message')
    if node.hasAttr('rotateOrder'):
        align_group.rotateOrder.set(node.rotateOrder.get())
    pm.delete(pm.parentConstraint(node, align_group, w=1, mo=False))

    if orient_obj:
        pm.delete(pm.orientConstraint(orient_obj, align_group, w=1, mo=False))

    object_parent = node.getParent()
    if object_parent:
        align_group.setParent(object_parent)
    node.setParent(align_group)

    if isinstance(node, pm.nodetypes.Joint):
        node.jointOrient.set([0, 0, 0])
        for axis_name in attr_utils.ROTATION_ATTRS:
            if not node.attr(axis_name).isLocked():
                node.setAttr(axis_name, 0)

    attr_utils.set_attribute(node, {attr_name:align_group.attr(group_attr)})
    return align_group


def parent_shape_node(donor_node_list, to_node, maintain_offset=False, replace=True, freeze_transform=True, delete_original=True):
    """
    Parent all shape nodes from a list of shaped transform to a given node.

    :param list(Transform) donor_node_list: A list of trasnforms with shapes we'll copy to our selected node.
    :param Transform to_node: The transform we wish to add new shapes to.
    :param bool maintain_offset: If position of the doners should be maintained.
    :param bool replace: If the node's original shapes should be removed before adding the donors.
    :param bool freeze_transform: If we should freeze the transforms of the donor before parenting them.
    :param bool delete_original: If we should delete the donor transforms.
    :return: The base object we've added the new shapes to.
    :rtype: Transform
    """
    if not isinstance(donor_node_list, list):
        donor_node_list = [donor_node_list]

    new_shape = None
    if replace:
        old_shapes = to_node.getShapes()
        if old_shapes:
            pm.delete(old_shapes)

    for node in donor_node_list:
        if freeze_transform and not maintain_offset:
            pm.makeIdentity(node, apply=1, t=1, r=1, s=0)

        if maintain_offset:
            pm.parent(node, to_node)
            pm.makeIdentity(node, apply=1, t=1, r=1, s=0)
            pm.parent(node, w=True)

        new_shape = pm.parent(node.getShapes(), to_node, add=1, s=1)[0]
        # gets around double namespaces.
        shape_name = f'{naming.get_basename(to_node)}Shape'
        for i, shape in enumerate(to_node.getShapes()):
            shape.rename(shape_name) if i == 0 else shape.rename(shape_name + str(i + 1))
    if delete_original:
        pm.delete(donor_node_list)

    return new_shape


def get_primary_axis(node):
    """
    From the current node's translation or the translation of it's first child. Find the largest deviant and return it.

    :param Transform node: The node to check for the primary axis.
    :return: Str of the axis identifier and a bool if the value is positive or negative.
    :rtype: str, bool
    """
    child_node = list_utils.get_first_in_list(node.getChildren(type=pm.nt.Transform))

    target_node = child_node or node

    max_val = 0
    primary_axis = 'x'
    axis_is_positive = True
    for axis_name, x in zip('xyz', target_node.t.get()):
        if abs(x) > max_val:
            max_val = abs(x)
            primary_axis = axis_name
            if x > 0:
                axis_is_positive = True
            else:
                axis_is_positive = False
    return primary_axis, axis_is_positive


def get_between_nodes(start_node, end_node, node_type=None):
    """
    Returns in between nodes between the first and last.

    :param Transform start_node: Start node to trace between nodes.
    :param Transform end_node: End node to trace between nodes.
    :param PyNode node_type: Node type to return.
    :return: Returns a list of the first, last, and in between joints.
    :rtype: list(Transform)
    """

    if not start_node or not end_node:
        return

    node_list = list()
    node_list.append(end_node)
    current_node = end_node
    while start_node != current_node:
        current_node = current_node.getParent() if current_node else None
        if not current_node:
            logger.warning('{0} is not in the hierarchy of {1}'.format(start_node, end_node))
        node_list.append(current_node)

    if node_type:
        node_list = [node for node in node_list if isinstance(node, node_type)]

    node_list.reverse()

    return node_list


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


def get_ordered_hierarchy(root_node, object_type=None):
    """
    Non-inclusive child getter. Notably this generates the return list in DAG hierarchy order.

    :param PyNode root_node: The root node to get all children from.
    :param Class, tuple object_type: A PyNode class type to filter by.
    :return: A list of all found children that match the given class type.
    :rtype: list(PyNode)
    """
    return_list = []
    for child_node in root_node.getChildren():
        if object_type and not isinstance(child_node, object_type):
            continue
        return_list += [child_node]+get_ordered_hierarchy(child_node, object_type)
    return return_list


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

    nodes = list_utils.force_list(node)
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

def get_curve_data(shape_node):
    """
    Retrieves the curve data from the given shape node.

    :param pm.Shape shape_node: flag curve shape node.
    :return: dictionary containing all the curve shape data.
    :rtype: dict
    """

    curve_data = {'knots': tuple(shape_node.getKnots()),
                  'cvs': tuple(map(tuple, shape_node.getCVs('world'))),
                  'degree': shape_node.degree(),
                  'form': int(shape_node.form())}

    return curve_data

def create_locator_at_object(node, name=None):
    name = name or 'new_loc'
    new_loc = pm.spaceLocator(n=name)
    pm.delete(pm.parentConstraint(node, new_loc))
    return new_loc

def create_line_between(node_a, node_b, name=None):
    """
    Creates a referenced NURBs line that traces between two objects. This is a live setup.

    :param str or nt.Transform node_a: Start of the line
    :param str or nt.Transform node_b: End of the line
    :return: Transform of created curve which draws the line
    :rtype: pm.nt.Transform
    """

    pos1 = node_a.getTranslation(space='world')
    pos2 = node_b.getTranslation(space='world')
    # Linear curve
    curve_node = pm.curve(d=1, p=[pos1, pos2], k=[0, 1])
    node_name = name or naming.get_basename(curve_node)
    _, node_a_cluster = skin_utils.create_cluster_from_component_names(curve_node.cv[0], f'{node_name}_a')
    _, node_b_cluster = skin_utils.create_cluster_from_component_names(curve_node.cv[1], f'{node_name}_b')
    pm.parent([node_a_cluster, node_b_cluster], curve_node)
    curve_node.inheritsTransform.set(0)
    node_a_cluster.inheritsTransform.set(0)
    node_b_cluster.inheritsTransform.set(0)
    node_a_cluster.hide()
    node_b_cluster.hide()
    pm.pointConstraint(node_a, node_a_cluster, w=1, mo=1)
    pm.pointConstraint(node_b, node_b_cluster, w=1, mo=1)
    line_shape = pm.PyNode(curve_node).getShape()
    line_shape.overrideEnabled.set(1)
    line_shape.overrideDisplayType.set(1)#template
    line_shape.overrideColor.set(3) #set to gray color
    # gets around double namespaces.
    curve_node.rename(node_name)
    curve_node.getShape().rename(f'{node_name}Shape')
    return curve_node
