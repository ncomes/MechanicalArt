#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A way to interact with joint chains in rigs.
"""
# System global imports
import math
# Software specific imports
import pymel.core as pm
import maya.cmds as cmds
#  python imports
from mca.common import log
from mca.mya.utils import dag, attr_utils, node_util, naming
from mca.mya.rigging import chain_markup


logger = log.MCA_LOGGER


def get_end_joint(start_joint):
    """
    Returns the end joint of a chain from the given start joint.

    :param  str or pm.Joint start_joint: joint to find end joint from.
    :param bool include_transforms: whether to include non-joint transforms in the chain.
    :return: found end joint in the hierarchy.
    :rtype: str or None
    """

    if not isinstance(start_joint, pm.nt.Joint):
        return None

    return dag.get_absolute_child(start_joint, node_type=pm.nt.Joint)


def get_end_joints(joint):
    """
    Loops through all children and returns all joints that have no joint children.

    :param str or pm.Joint joint: joint node.
    :return: end joints list.
    :rtype: list(pm.Joint)
    """

    joint = pm.PyNode(joint)
    result = list()
    children = joint.listRelatives(children=True, type='joint')
    if not children:
        result.append(joint)
    else:
        for child in children:
            result.extend(get_end_joints(child))

    return result


def sort_chain_by_hierarchy(joint_list, reverse=False):
    """
    Sorts given chain of joints by their hierarchy.

    :param list(pm.PyNode) joint_list: list of joints.
    :param bool reverse: whether order should happen from root to end or vice-versa.
    :return: list of Maya scene joints sorted by hierarchy
    :rtype: list(pm.PyNode)
    """

    order_dict = dict()
    for obj in joint_list:
        relative_count = len(pm.listRelatives(obj, ad=True, type=pm.nt.Joint))
        order_dict.setdefault(relative_count, list())
        order_dict[relative_count].append(obj)

    ordered_keys = list(order_dict.keys())
    ordered_keys.sort()

    sorted_list = list()
    for key in ordered_keys:
        sorted_list.extend(order_dict[key])

    # reverse to have the chain ordered from root to end.
    if not reverse:
        sorted_list.reverse()

    return sorted_list


def duplicate_joint(joint_node, duplicate_name=None):
    """
    Duplicates given joint.

    :param PyNode joint_node: Joint to be duplicated
    :param str duplicate_name: optional name for duplicated joint. If None, append _dup to name.
    :return: str
    """

    if not isinstance(joint_node, pm.nt.Joint):
        return

    wrapped_node = chain_markup.JointMarkup(joint_node)

    duplicate_name = duplicate_name or f'{wrapped_node.name}_dup'
    unique_name = duplicate_name
    index = 0
    while cmds.objExists(unique_name):
        index += 1
        unique_name = f'{duplicate_name}{index}'
    duplicate_name = unique_name

    new_joint_node = pm.duplicate(joint_node, po=True)[0]
    pm.rename(new_joint_node, duplicate_name)

    attr_utils.unlock_node_attributes(new_joint_node, attributes=attr_utils.TRANSFORM_ATTRS+['radius', 'v'])

    return new_joint_node


def duplicate_chain(start_joint, end_joint=None, parent=None, skip_joints=None, suffix=None):
    """
    Duplicates a joint chain based on the given start and end joint.

    :param pm.PyNode start_joint: start joint of chain.
    :param pm.PyNode end_joint: end joint of chain. If None, use end of current chain.
    :param pm.PyNode parent: parent transform for new chain.
    :param PyNode or None skip_joints: skip joints in chain that match.
    :param str suffix: new name prefix.
    :return: list of duplicate joints.
    :rtype: list(str)
    """

    if not pm.objExists(start_joint):
        logger.warning('Start joint "{}" does not exists!'.format(start_joint))
        return list()
    if end_joint and not pm.objExists(str(end_joint)):
        logger.warning('End joint "{}" does not exists!'.format(end_joint))
        return list()

    if parent:
        if not pm.objExists(parent):
            logger.warning('Given parent transform "{}" does not exists!'.format(parent))
            return list()
        if not isinstance(parent, pm.nt.Transform):
            logger.warning('Parent object "{}" is not a valid transform!'.format(parent))
            return list()

    if not end_joint:
        end_joint = get_end_joint(start_joint=start_joint)
    if start_joint == end_joint:
        joint_list = [start_joint]
    else:
        joint_list = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

    skip_joints = skip_joints or []

    dup_chain = []
    for index, joint_node in enumerate(joint_list):
        if joint_node in skip_joints:
            continue

        wrapped_joint = chain_markup.JointMarkup(joint_node)
        duplicate_name = f'{wrapped_joint.name}_{suffix}'
        duplicate_node = duplicate_joint(joint_node, duplicate_name)
        if index == 0:
            current_parent_node = duplicate_node.getParent()
            if parent:
                if current_parent_node != parent or not current_parent_node:
                    duplicate_node.setParent(parent)
            else:
                if current_parent_node:
                    duplicate_node.setParent(None)
        else:
            duplicate_node.setParent(dup_chain[-1])

        dup_chain.append(duplicate_node)

    return dup_chain


def subdivide_joint(source_joint=None, target_joint=None, count=1, prefix='joint', name='sub_1', duplicate=False):
    """
    Adds evenly spaced joints between given joints.

    :param str source_joint: first joint. If None, first selected joint will be used.
    :param str target_joint: second joint. If None, second selected joint will be used.
    :param int count: number of joints to add in between joint1 and joint2.
    :param str prefix: prefix to add in front of the new joints.
    :param str name: name to give to the new joints after the prefix.
    :param bool duplicate: whether to create a duplicate chain and keep the original chain intact.
    :return: list of newly created joints.
    :rtype: list(str)
    """

    if not source_joint and not target_joint:
        selection = pm.ls(sl=True)
        if pm.nodeType(selection[0]) == 'joint':
            source_joint = selection[0]
        if len(selection) > 1:
            if pm.nodeType(selection[1]) == 'joint':
                target_joint = selection[1]
    if source_joint and not target_joint:
        joint_relatives = pm.listRelatives(source_joint, type='joint')
        if joint_relatives:
            target_joint = joint_relatives[0]
    if not source_joint and not target_joint:
        return

    joints = list()
    top_joint = source_joint
    last_joint = None
    bottom_joint = target_joint
    radius = pm.getAttr('{}.radius'.format(source_joint))
    vector1 = pm.xform(source_joint, query=True, worldSpace=True, translation=True)
    vector2 = pm.xform(target_joint, query=True, worldSpace=True, translation=True)
    name = '{}_{}'.format(prefix, name)
    offset = 1.00 / (count + 1)
    value = offset

    if duplicate:
        pm.select(clear=True)
        top_joint = pm.joint(p=vector1, n=name, r=radius + 1)
        joints.append(top_joint)
        match = node_util.match_rotation(top_joint, source_joint)
        match.rotation()
        pm.makeIdentity(top_joint, apply=True, r=True)

    for i in range(count):
        position = math.get_inbetween_vector(vector1, vector2, value)
        pm.select(clear=True)
        joint = pm.joint(p=position, n=name, r=radius)
        pm.setAttr('{}.radius'.format(joint), radius)
        joints.append(joint)
        value += offset
        if i == 0:
            pm.parent(joint, top_joint)
            pm.makeIdentity(joint, apply=True, jointOrient=True)
        if last_joint:
            pm.parent(joint, last_joint)
            pm.makeIdentity(joint, apply=True, jointOrient=True)
            if not pm.isConnected('{}.scale'.format(last_joint), '{}.inverseScale'.format(joint)):
                pm.connectAttr('{}.scale'.format(last_joint), '{}.inverseScale'.format(joint))
        last_joint = joint

    if duplicate:
        pm.select(clear=True)
        bottom_joint = pm.joint(p=vector2, n=name, r=radius + 1)
        joints.append(bottom_joint)
        node_util.match_rotation(bottom_joint, source_joint)
        pm.makeIdentity(bottom_joint, apply=True, r=True)

    pm.parent(bottom_joint, joint)

    if not pm.isConnected('{}.scale'.format(joint), '{}.inverseScale'.format(bottom_joint)):
        pm.connectAttr('{}.scale'.format(joint), '{}.inverseScale'.format(bottom_joint))

    return joints


def insert_joints(joints, joint_count=1):
    """
    Inserts joints evenly spaced along a joint.

    :param list(str or pm.Joint) joints: list of joints to insert child joints to
    :param int joint_count: Number of joints to insert
    :return: List of created joints
    :rtype: list(pm.Joint)
    """

    if joint_count < 1:
        logger.warning('Must insert at least 1 joint')
        return

    pm.select(clear=True)

    result = list()
    for joint in joints:
        children = pm.listRelatives(joint, children=True, type='joint', fullPath=True)
        if not children:
            logger.warning('Joint "{}" needs at least a child in order to insert joints. Skipping!'.format(joint))
            continue

        name = joint
        end_joint = children[0]
        dst = math.distance_between_nodes(joint, end_joint)
        increment = dst / (joint_count + 1)
        direction = math.direction_vector_between_nodes(joint, end_joint)
        direction.normalize()
        direction *= increment

        for i in range(joint_count):
            position = pm.dt.Point(*pm.xform(joint, query=True, worldSpace=True, translation=True))
            position += direction
            joint = pm.insertJoint(joint)
            joint = pm.rename(joint, '{}#'.format(name))
            pm.joint(joint, edit=True, component=True, position=(position.x, position.y, position.z))
            result.append(joint)

    return result


def create_joints_on_cvs(curve, parented=True):
    """
    Creates a joint in each CV of the given curve.

    :param str curve: name of the curve.
    :param bool parented: whether or not, joints should be parented under the last joint created at the previous CV.
    :return: list of created joints.
    :rtype: list(str)
    """

    joints = list()
    last_joint = None

    cvs = pm.ls('{}.cv[*]'.format(curve), flatten=True)
    pm.select(clear=True)

    for i, cv in enumerate(cvs):
        position = pm.pointPosition(cv)
        if not parented:
            pm.select(clear=True)
        joint = pm.joint(n=f'joint_{curve}', p=position)
        joints.append(joint)
        if last_joint and parented:
            pm.joint(last_joint, e=True, zso=True, oj='xyz', sao='yup')
        last_joint = joint

    return joints


def create_skeleton_dict(root_joint):
    """
    Creates a name to object dictionary of the skeleton hierarchy. This is useful for making maps between skeletons.

    :return: A dictionary of absolute string names to the joint itself.
    :rtype dict{}:
    """

    skel_dict = {}
    for index, joint_node in enumerate([root_joint] + pm.listRelatives(root_joint, ad=True, type=pm.nt.Joint)):
        if not index:
            joint_name = 'root'
        else:
            joint_name = naming.get_basename(joint_node)
        skel_dict[joint_name] = joint_node
    return skel_dict


def inherit_joint_labelling(from_node, to_node):
    """
    Copy FBIK attribute values from one node to another node

    :param str or Joint from_node: Node to copy from
    :param str or Joint to_node: Node to copy to
    """

    from_node = pm.PyNode(from_node)
    to_node = pm.PyNode(to_node)
    if from_node.hasAttr('skelSide'):
        if not to_node.hasAttr('skelSide'):
            to_node.addAttr('skelSide', dt='string')
        to_node.setAttr('skelSide', from_node.getAttr('skelSide'))
    if from_node.hasAttr('skelRegion'):
        if not to_node.hasAttr('skelRegion'):
            to_node.addAttr('skelRegion', dt='string')
        to_node.setAttr('skelRegion', from_node.getAttr('skelRegion'))