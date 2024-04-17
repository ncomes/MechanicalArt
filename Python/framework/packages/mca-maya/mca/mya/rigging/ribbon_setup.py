#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Handles the setup functions for a ribbon.
"""
# System global imports
# software specific imports
import pymel.core as pm
#  python imports
from mca.common.utils import pymaths

from mca.mya.rigging import rig_utils


def create_ribbon_along_nodes(node_list, name='ribbon'):
    """
    Create a ribbon aligned along a series of nodes.

    :param list node_list: A list of objects to build the ribbon along.
    :param str name: The name to use with the new ribbon object.
    :rtype: Transform
    :return: The transform of the ribbon's nurbs curve.
    """
    nurbs_curve, make_nurbs_node = pm.nurbsPlane(n=name)
    list_length = len(node_list)
    make_nurbs_node.patchesV.set(list_length * 2 - 4)
    primary_axis = None
    previous_vector = None
    for index, node in enumerate(node_list):
        # index*2 gets the node aligned cvs.
        # index*2-1 gets the mid point aligned cvs.
        if not primary_axis:
            primary_axis, _ = rig_utils.find_primary_axis(node)
            index_offset = ('XYZ'.index(primary_axis) + 2) % 3
            axis_offset = pm.dt.Vector([1 if x == index_offset else 0 for x in range(3)])

        m1 = pm.dt.TransformationMatrix(node.getMatrix(ws=True))
        current_pos = pm.xform(node, q=True, ws=True, t=True)

        m1.addTranslation(axis_offset, 'preTransform')
        offset_pos = m1.getTranslation('world')

        # Find a point in space 1 unit offset by 1 axis. IE if the primary axis is X the offset is 1 unit Y local transform
        # This vector is normalized and becomes our starting point.
        x_product_norm = pymaths.normalize_vector(pymaths.sub_vectors(offset_pos, current_pos))
        if previous_vector:
            midpoint = pymaths.find_midpoint_between_points(previous_pos, current_pos)
            x_product_average = pymaths.average_vectors([x_product_norm, previous_vector])
            _place_cv_along_point(nurbs_curve, index * 2 - 1, midpoint, x_product_average)
        previous_vector = x_product_norm[:]
        previous_pos = current_pos[:]

        _place_cv_along_point(nurbs_curve, index * 2, current_pos, x_product_norm)
    return nurbs_curve


def _place_cv_along_point(nurbs_curve, index, current_pos, x_product):
    """
    Helper function for create_ribbon_along_nodes

    :param makeNurbPlane nurbs_curve:
    :param int index: The row index for the nurbs plane.
    :param list[float, float, float] current_pos: The world space position of where the cvs should be placed around.
    :param list[float, float, float] x_product: The cross product from the point to align the cvs to.
    """
    for i in range(4):
        pos = pymaths.add_vectors(current_pos, pymaths.scale_vector(x_product, (i - 1.5) * 2.5))
        pm.move(nurbs_curve.cv[i][index], pos)