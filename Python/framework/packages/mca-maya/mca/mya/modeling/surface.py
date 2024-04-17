#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilities for Maya
"""

# System global imports

# software specific imports
import pymel.core as pm

# mca python imports


def get_closest_parameter_on_surface(surface, vector, space='preTransform'):
    """
    Returns the closest parameter value on the surface given vector.

    :param pm.PyNode surface: surface node.
    :param list(float, float, float) or pm.dt.Vector vector: position from which to check for closes parameter on
        given surface.
    :param int space: space.
    :return: parameter coordinates (UV) of the closest point on the surface.
    :rtype: list(int, int)
    """

    shapes = surface.getShapes()
    surface_shape = shapes[0] if shapes else surface
    uv, _, _ = surface_shape.closestPoint(vector, space=space)
    uv = list(uv)
    if uv[0] == 0:
        uv[0] = 0.001

    if uv[1] == 0:
        uv[1] = 0.001

    return uv

