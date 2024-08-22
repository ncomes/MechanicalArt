#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Open Maya Utilities.
"""

# System global imports
# mca python imports
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma
import pymel.core as pm

# mca python imports
from mca.mya.modifiers import ma_decorators

from mca.common import log
logger = log.MCA_LOGGER

def pynode_to_om2_mobject_mdag_path(node):
    """
    Convert a pynode into a MDagPath and MObject

    :param PyNode node: The PyNode to be converted.
    :return: The om equivalent objects.
    :rtype: MDagPath, MObject
    """

    if isinstance(node, pm.nt.DagNode):
        sel = om2.MSelectionList()
        sel.add(node.longName())
        return sel.getComponent(0)
    else:
        logger.error('Node type is not a DagNode. {0}, {1}'.format(node, type(node)))
        return None, None
    
def pynode_list_to_om2_selection_list(node_list):
    """
    Convert a list of pynodes into a MApi MSelectionList
    NOTE: All nodes must be dag nodes.
    
    :param list(PyNode) node_list: A list of nodes to convert.
    :return: The given PyNodes converted into a MSelectionList
    :rtype: MSelectionList
    """
    sel = om2.MSelectionList()
    for node in node_list:
        if isinstance(node, pm.nt.DagNode):
            sel.add(node.longName())
    return sel

def get_om2_keyframes_from_pynode_list(node_list):
    """
    From a given list of Dag PyNodes get their keyable attrs and return all keyframe values.
    
    :param list(PyNode) node_list: A list of nodes we want th keyframes from.
    :return: A list of all the keyframes numbers on this object.
    :rtype: list
    """
    if not isinstance(node_list, list):
        node_list = [node_list]
    sel = pynode_list_to_om2_selection_list(node_list)
        
    keyframe_list = set()
    for animated_plug in oma.MAnimUtil.findAnimatablePlugs(sel):
        anim_curve = oma.MFnAnimCurve(animated_plug)
        try:
            for i in range(anim_curve.numKeys):
                frame = anim_curve.input(i).value
                keyframe_list.add(frame)
        except:
             pass
    return list(sorted(keyframe_list)) if keyframe_list else (None, None)

def get_om2_keyframe_range_from_scene():
    """
    From all scene animation curves get the first and last keyframe.

    :return: The start and end frame of all animation in the scene.
    :rtype int, int:
    """
    it = om2.MItDependencyNodes(om2.MFn.kAnimCurveTimeToAngular)
    keyframe_list = set()
    while not it.isDone():
        anim_curve = oma.MFnAnimCurve(it.thisNode())
        for i in range(anim_curve.numKeys):
            frame = anim_curve.input(i).value
            keyframe_list.add(frame)
        it.next()
    keyframe_list = list(keyframe_list)
    return (min(keyframe_list), max(keyframe_list)) if keyframe_list else (None, None)

@ma_decorators.not_undoable_decorator
def om2_change_curve_start_time(node_list, offset=None):
    """
    Shifts all keyframes on a set of nodes by a given value. If no shift length is given it will zero the animation.
    NOTE: This command cannot be undone.

    :param PyNode node_list: A list of objects to shift the keyframes on.
    :param int shift_length: How much the animation should be shifted by.
    """
    if offset == 0.0:
        return

    if not isinstance(node_list, list):
        node_list = [node_list]

    for node in node_list:
        sel = pynode_list_to_om2_selection_list([node])
            
        for animated_plug in oma.MAnimUtil.findAnimatablePlugs(sel):
            try:
                anim_curve = oma.MFnAnimCurve(animated_plug)

                if offset > 0:
                    index_range = reversed(range(anim_curve.numKeys))
                else:
                    index_range = range(anim_curve.numKeys)

                frame = anim_curve.input(0).value
                if offset is None:
                    # If we never had an offset take the first fame value and subract it from 0 to create a 0 offset.
                    offset = 0.0 - frame
                for i in index_range:
                    
                        frame = anim_curve.input(i).value
                        if offset is None:
                            # If we never had an offset take the first fame value and subract it from 0 to create a 0 offset.
                            offset = 0.0 - frame
                        mtime = om2.MTime()
                        mtime.value = frame+offset
                        om2.MDGContext(mtime)
                        anim_curve.setInput(i, mtime)
            except:
                # Sometimes we get a non existant anim_curve
                pass


def get_closest_joint_to_vertex(vertex, mesh_name, joint_list):
    """
    Gets the closest joint to a provided vertex index.

    :param int vertex: Vertex index
    :param str mesh_name: Name of the mesh
    :param list(str) joint_list: List of names of joints to be considered
    :return: The name of the closest joint
    :rtype: str
    """
    closest_joint = None
    closest_distance = float('inf')

    # Create an empty MSelectionList. This is a wrapper for a list of MObjects (base class for nodes)
    selection_list = om2.MSelectionList()
    # Add specified node to MSelectionList. You can pass add() MObject or short/long names of nodes
    # and it will create an MObject for it if found
    selection_list.add(mesh_name)
    # getDagPath works by providing it an index to the list above then a reference to the DAG path is
    # stored along with the MObject for the node
    dag_path = selection_list.getDagPath(0)
    # Create MFnMesh to work with mesh
    mfn_mesh = om2.MFnMesh(dag_path)
    # getPoint uses the vertex index and creates and stores an MPoint which we can get the coordinates
    # of the vertex off later
    point = mfn_mesh.getPoint(vertex, space=om2.MSpace.kWorld)

    for jnt in joint_list:
        # Make sure selection list is empty
        selection_list.clear()

        # Add the joint object to the selection list
        selection_list.add(jnt)

        # Create MDagPath for joint
        dag_path = selection_list.getDagPath(0)

        # Create MFnTransform to get translation from joint
        jnt_fn = om2.MFnTransform(dag_path)
        jnt_pos = jnt_fn.translation(om2.MSpace.kWorld)

        # Create MVector obj at vertex position
        vertex_pos = om2.MVector(point.x, point.y, point.z)

        # Subtract joint and vertex vector components to get distance vector
        distance_vector = vertex_pos - jnt_pos
        # Use MVector length to get distance
        distance = distance_vector.length()

        # Check distance to see if closest
        if distance < closest_distance:
            closest_distance = distance
            closest_joint = jnt

    return closest_joint


def get_adjacent_vertices(vertex):
    """
    Gets adjacent vertex indices for specified vertex index

    :param str vertex: Vertex return adjacent vertex indices for
    :return: Adjacent vertex indices
    :rtype: list(int)
    """

    # Create an MSelectionList and add the vertex to it
    selection_list = om2.MSelectionList()
    selection_list.add(vertex)

    # Create an MFnMesh object from the selected mesh and get the DAG path and MObject for the component
    dag_path, component = selection_list.getComponent(0)

    # Get the adjacent vertices using MItMeshVertex. This is an iterator for vertices so if we don't provide
    # it a component it will go over all vertices on specified surface
    vertex_iter = om2.MItMeshVertex(dag_path, component)
    adjacent_vertices = []

    while not vertex_iter.isDone():
        # Get indices of vertices around our vertex
        connected_vertices = vertex_iter.getConnectedVertices()
        adjacent_vertices.extend(connected_vertices)
        vertex_iter.next()

    return adjacent_vertices
