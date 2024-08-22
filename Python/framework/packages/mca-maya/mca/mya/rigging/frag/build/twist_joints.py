#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for twist joints up to 3.
"""

# System global imports
# software specific imports
import pymel.core as pm
# project python imports
from mca.common.utils import pymaths

from mca.mya.rigging import joint_utils
from mca.mya.utils import constraint_utils, dag_utils


def quick_build_twist_setup(root_joint):
    """
    Quickly build twist setups on a raw skeleton.

    :param Joint root_joint: Root joint of the skeletal hierarchy.
    """
    skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
    macro_grp = pm.group(n='twist_grp', em=True, w=True)
    macro_grp.v.set(False)
    for _, entry_dict in skel_hierarchy.twist_joints.items():
        for _, data_dict in entry_dict.items():
            twist_grp, _ = twist_setup(data_dict['joints'])
            if twist_grp:
                twist_grp.setParent(macro_grp)


def twist_setup(joint_list):
    """
    Build a twist joint drive system for a list of twist joints.

    :param list[Joint] joint_list: The list of twist joints which will be driven by this twist drive system.
    :return: The build group for this drive system. And the build dictionary of notable nodes.
    :rtype: Transform, dict
    """
    # collect all our used nodes.
    build_dict = {}

    joint_list = list(sorted(joint_list))
    if len(joint_list) > 3:
        # We don't support twist chains over 3.
        return None, {}

    first_twist = joint_list[0]
    root_joint = dag_utils.get_absolute_parent(first_twist, pm.nt.Joint)
    skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)
    parent_joint = first_twist.getParent()
    wrapped_parent_joint = joint_utils.JointMarkup(parent_joint)
    wrapped_twist_joint = joint_utils.JointMarkup(first_twist)
    side = wrapped_parent_joint.side
    skel_region = wrapped_parent_joint.region
    twist_chain_region = wrapped_twist_joint.region
    parent_chain = skel_hierarchy.get_full_chain(side, skel_region)
    child_joint = parent_chain[parent_chain.index(parent_joint) + 1]

    # determine if we're reversed or not by checking distance to parent from the first twist.
    start_pos = pm.xform(first_twist, q=True, ws=True, t=True)
    child_pos = pm.xform(child_joint, q=True, ws=True, t=True)
    parent_pos = pm.xform(parent_joint, q=True, ws=True, t=True)

    dis_to_parent = pymaths.get_vector_length(pymaths.sub_vectors(start_pos, parent_pos))
    dis_to_child = pymaths.get_vector_length(pymaths.sub_vectors(start_pos, child_pos))

    reverse = False if dis_to_child > dis_to_parent else True

    # start build setup
    twist_grp = pm.group(n=f'{side}_{twist_chain_region}_twist_grp', em=True, w=True)
    pm.delete(constraint_utils.parent_constraint_safe(parent_joint, twist_grp))
    constraint_utils.parent_constraint_safe(parent_joint.getParent(), twist_grp)
    mirror_chain = joint_utils.duplicate_chain(parent_joint, child_joint, suffix='mirror_chain')
    build_dict['mirror_chain'] = mirror_chain

    mirror_chain[0].setParent(twist_grp)
    constraint_utils.parent_constraint_safe(parent_joint, mirror_chain[0])
    constraint_utils.parent_constraint_safe(child_joint, mirror_chain[1])
    ik_chain = joint_utils.duplicate_chain(parent_joint, child_joint, suffix='ik')
    build_dict['ik_chain'] = ik_chain
    ik_chain[0].setParent(twist_grp)

    # IKSolver and zero pole vector to isolate rot.
    ik_handle_node, eff = pm.ikHandle(sol='ikRPsolver', sj=ik_chain[0], ee=ik_chain[1])
    ik_handle_node.rename(f'{side}_{twist_chain_region}_ikhandle')
    build_dict['ik_handle'] = ik_handle_node
    ik_handle_node.setParent(mirror_chain[-1])
    for axis in 'XYZ':
        ik_handle_node.setAttr(f'poleVector{axis}', 0)

    # locator to hold extracted rotation.
    offset_loc = pm.spaceLocator(n=f'{side}_{twist_chain_region}_offset_loc')
    build_dict['offset_loc'] = offset_loc
    offset_loc.setParent(mirror_chain[1] if reverse else mirror_chain[0])
    offset_loc.translate.set([0, 0, 0])
    offset_loc.rotate.set([0, 0, 0])
    orient_targets = [mirror_chain[1], ik_chain[1]] if reverse else [mirror_chain[0], ik_chain[0]]
    # Double constraint here reduces
    constraint_utils.orient_constraint_safe(orient_targets, offset_loc)

    # Multiply node that sets the rot value back to our twist joints.
    # And the last bit of logic to determine the rotation amount and attach them back to our twist joints.
    twist_multi = pm.createNode(pm.nt.MultiplyDivide, n=f'{side}_{twist_chain_region}_multi')
    build_dict['multi_node'] = twist_multi

    primary_axis, _ = dag_utils.get_primary_axis(parent_joint)
    rot_multiplier = 1 / len(joint_list) * 2.0
    rot_multiplier = rot_multiplier * -1.0 if reverse else rot_multiplier
    for index, twist_joint in enumerate(reversed(joint_list)):
        offset_loc.attr(f'r{primary_axis}') >> twist_multi.attr(f'input1{"XYZ"[index]}')
        twist_multi.setAttr(f'input2{"XYZ"[index]}', rot_multiplier * (index + 1))
        twist_multi.attr(f'output{"XYZ"[index]}') >> twist_joint.attr(f'r{primary_axis}')
    unit_conv_nodes = [x for x in twist_multi.listConnections() if isinstance(x, pm.nt.UnitConversion)]
    build_dict['unit_conv_nodes'] = unit_conv_nodes

    return twist_grp, build_dict
