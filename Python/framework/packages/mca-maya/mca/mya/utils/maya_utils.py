#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilities for Maya
"""

# System global imports
import os

# software specific imports
import pymel.core as pm
import maya.mel as mel

#  python imports
from mca.common.utils import list_utils
from mca.common.project import paths


def maya_default_preferences_path():
    prefs_folder = paths.get_dcc_prefs_folder('maya')
    default_paths = os.path.join(prefs_folder, 'default_options')
    if not os.path.exists(default_paths):
        os.makedirs(default_paths)
    return os.path.normpath(default_paths)


def get_default_preferences_file():
    default_path = maya_default_preferences_path()
    file_path = os.path.join(default_path, 'maya_default_options.prefs')
    return os.path.normpath(file_path)

def get_version():
    """
    Returns version of the executed Maya, or 0 if not Maya version is found.

    :return: version of Maya.
    :rtype: int
    """

    return int(pm.about(version=True))


def get_api_version():
    """
    Returns the Maya API version.

    :return: version of Maya API.
    :rtype: int
    """

    return int(pm.about(api=True))


def get_float_version():
    """
    Returns the Maya version as a float value.

    :return: version of Maya as float value.
    :rtype: float
    """

    return mel.eval('getApplicationVersionAsFloat')


class SelectionMasks(object):
    """
    https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/filterExpand.html
    """

    Handle = 0
    NurbsCurves = 9
    NurbsSurfaces = 10
    NurbsCurvesOnSurface = 11
    Polygon = 12
    LocatorXYZ = 22
    OrientationLocator = 23
    LocatorUV = 24
    ControlVertices = 28
    CVs = 28
    EditPoints = 30
    PolygonVertices = 31
    PolygonEdges = 32
    PolygonFace = 34
    PolygonUVs = 35
    SubdivisionMeshPoints = 36
    SubdivisionMeshEdges = 37
    SubdivisionMeshFaces = 38
    CurveParameterPoints = 39
    CurveKnot = 40
    SurfaceParameterPoints = 41
    SurfaceKnot = 42
    SurfaceRange = 43
    TrimSurfaceEdge = 44
    SurfaceIsoparms = 45
    LatticePoints = 46
    Particles = 47
    ScalePivots = 49
    RotatePivots = 50
    SelectHandles = 51
    SubdivisionSurface = 68
    PolygonVertexFace = 70
    NurbsSurfaceFace = 72
    SubdivisionMeshUVs = 73
    

def delete_nodes_of_type(node_type):
    """
    Delete all nodes of the given Maya type.

    :param str or list(str) node_type: name/s of node type/s (eg: hyperView, etc)
    :return: list of delete nodes.
    :rtype: list(str)
    """

    node_type = list_utils.force_list(node_type)
    deleted_nodes = list()

    for node_type_name in node_type:
        nodes_to_delete = pm.ls(type=node_type_name)
        for n in nodes_to_delete:
            if n in ('hyperGraphLayout',):
                continue
            if not pm.objExists(n):
                continue

            pm.lockNode(n, lock=False)
            pm.delete(n)
            deleted_nodes.append(n)

    return deleted_nodes

