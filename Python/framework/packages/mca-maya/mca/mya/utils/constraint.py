#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for interacting with Maya Joints
"""
# System global imports

# python imports
import pymel.core as pm

#  python imports
from mca.common.utils import lists


def constraint_safe_attrs(node, attr_prefix, skip_list=None):
    """
    Verifies which axis for a given transform type are safe to connect to.
    :param Transform node:
    :param str attr_prefix: 't', 'r', 's' A string representing (t)ranslation, (r)otation, (s)cale
    :param list[str] skip_list: A list of the string names of attributes to be skipped. ('x', 'y', 'z')
    :return: A list of strings either the axis, or 'none' if 'none' it is safe to constrain
    :rtype list[str]:
    """

    safe_list = []
    for index, axis in enumerate(['x', 'y', 'z']):
        # for each exist
        if skip_list and axis in skip_list:
            # if we're skipping it mark it as so.
            safe_list.append(axis)
            continue
        attr_str = '{0}{1}'.format(attr_prefix, axis)
        node_attr = node.attr(attr_str)
        if node_attr.isSettable() and not node_attr.isLocked():
            attr_connections = lists.get_first_in_list(node_attr.listConnections())
            if not attr_connections or isinstance(attr_connections, (pm.nt.AnimCurve, pm.nt.AnimLayer)):
                # if we can set the value, and it's not locked, we can constrain it.
                safe_list.append('none')
        else:
            safe_list.append(axis)
    return safe_list


def parent_constraint_safe(source_node, driven_node, skip_rotate_attrs=None, skip_translate_attrs=None, **kwargs):
    """
    Create a parent constraint between objects keeping in check locked or unsettable attrs.

    :param Transform source_node: The node that will dictate the movement of the constraint.
    :param Transform driven_node: The node that will follow the movement of another.
    :param list[str] skip_rotate_attrs: A list of the string names of attributes to be skipped from the rotation group. ('x', 'y', 'z')
    :param list[str] skip_translate_attrs: A list of the string names of attributes to be skipped from the translation group. ('x', 'y', 'z')
    :return: Returns the created parent constraint or None on failure.
    :rtype ParentConstraint|None:
    """

    if not source_node or not driven_node:
        return None

    stc = constraint_safe_attrs(driven_node, 't', skip_translate_attrs)
    src = constraint_safe_attrs(driven_node, 'r', skip_rotate_attrs)

    if any('none' in safe_list for safe_list in [stc, src]):
        return pm.parentConstraint(source_node, driven_node, skipTranslate=stc, skipRotate=src, **kwargs)


def point_constraint_safe(source_node, driven_node, skip_attrs=None, **kwargs):
    """
    Create a point constraint between objects keeping in check locked or unsettable attrs.

    :param Transform source_node: The node that will dictate the movement of the constraint.
    :param Transform driven_node: The node that will follow the movement of another.
    :param list[str] skip_attrs: A list of the string names of attributes to be skipped. ('x', 'y', 'z')
    :return: Returns the created point constraint or None on failure.
    :rtype PointConstraint|None:
    """

    if not source_node or not driven_node:
        return None

    stc = constraint_safe_attrs(driven_node, 't', skip_attrs)

    if 'none' in stc:
        return pm.pointConstraint(source_node, driven_node, skip=stc, **kwargs)


def orient_constraint_safe(source_node, driven_node, skip_attrs=None, **kwargs):
    """
    Create an orient constraint between objects keeping in check locked or unsettable attrs.

    :param Transform source_node: The node that will dictate the movement of the constraint.
    :param Transform driven_node: The node that will follow the movement of another.
    :param list[str] skip_attrs: A list of the string names of attributes to be skipped. ('x', 'y', 'z')
    :return: Returns the created orient constraint or None on failure.
    :rtype OrientConstraint|None:
    """

    if not source_node or not driven_node:
        return None

    src = constraint_safe_attrs(driven_node, 'r', skip_attrs)

    if 'none' in src:
        return pm.orientConstraint(source_node, driven_node, skip=src, **kwargs)


def scale_constraint_safe(source_node, driven_node, skip_attrs=None, **kwargs):
    """
    Create a scale constraint between objects keeping in check locked or unsettable attrs.

    :param Transform source_node: The node that will dictate the movement of the constraint.
    :param Transform driven_node: The node that will follow the movement of another.
    :param Bool mo: If the offset to the source node should be maintained.
    :param list[str] skip_attrs: A list of the string names of attributes to be skipped. ('x', 'y', 'z')
    :return: Returns the created scale constraint or None on failure.
    :rtype ScaleConstraint|None:
    """

    if not source_node or not driven_node:
        return None

    ssc = constraint_safe_attrs(driven_node, 's', skip_attrs)

    if 'none' in ssc:
        return pm.scaleConstraint(source_node, driven_node, skip=ssc, **kwargs)


def get_constraint_targets(constraint):
    """
    Returns the transforms that are influencing the constraint.

    :param pm.PyNode constraint: constraint node to get targets of.
    :return: transform nodes affecting the constraint.
    :rtype: list(pm.PyNode)
    """

    transforms = list(set(constraint.target.listConnections(type='transform')))
    transforms = [x for x in transforms if isinstance(x, pm.nt.Transform) and pm.nodeType(x) == 'transform']

    return transforms

