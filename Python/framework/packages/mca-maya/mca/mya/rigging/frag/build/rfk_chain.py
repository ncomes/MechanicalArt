#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to building a simple RFK chain.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import flags, joint_utils
from mca.mya.utils import attr_utils, dag_utils, naming


def build_rfk_chain(joint_chain, scale=1.0):
    """

    :param joint_chain:
    :param scale:
    :return:
    """
    num_mid_joints = len(joint_chain) - 2  # - start_joint, end_joint
    wrapped_joint = joint_utils.JointMarkup(joint_chain[0])

    # Create Start and End flags
    flag_name = f'f_{wrapped_joint.side}_{wrapped_joint.region}'
    start_rotate_flag = flags.Flag.create(f'{flag_name}_start' ,alignment_node=joint_chain[0], scale=scale)
    start_rotate_flag.side = wrapped_joint.side
    start_rotate_flag.region = wrapped_joint.region
    pm.pointConstraint(joint_chain[0], start_rotate_flag.pynode)
    start_rotate_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)
    end_rotate_flag = flags.Flag.create(f'{flag_name}_end', alignment_node=joint_chain[-1], scale=scale)
    end_rotate_flag.side = wrapped_joint.side
    end_rotate_flag.region = wrapped_joint.region
    pm.pointConstraint(joint_chain[-1], end_rotate_flag.pynode)
    end_rotate_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)

    primary_axis, axis_is_positive = dag_utils.get_primary_axis(joint_chain[0])
    rot_offset = [0, 0, 0]
    if primary_axis == 'x':
        rot_offset = [0, -90, 90]

    flag_list = [start_rotate_flag]
    mid_groups = []
    mid_offset_groups = []
    weight_reverse_nodes = []
    # Subtract the start and end joints
    for index, joint_node in enumerate(joint_chain[1:-1]):
        mid_group = pm.group(empty=True, n=f"rfk_mid_group_{index+1}")
        pm.delete(pm.parentConstraint(joint_node, mid_group, w=True, mo=False))
        # create aims
        # start_aims
        start_weight = 1 - pm.util.smoothstep(0, 1, (index + 1.0) / (num_mid_joints + 1.0))
        start_flag_loc = dag_utils.create_locator_at_object(start_rotate_flag.pynode, f"start_flag_aims_orient_{index+1}")
        start_flag_loc_align = dag_utils.create_aligned_parent_group(start_flag_loc)
        start_x_loc = dag_utils.create_locator_at_object(start_rotate_flag.pynode, f"start_flag_aim_x_{index+1}")
        start_y_loc = dag_utils.create_locator_at_object(start_rotate_flag.pynode, f"start_flag_aim_y_{index+1}")
        start_x_loc.setParent(start_flag_loc)
        start_y_loc.setParent(start_flag_loc)
        pm.delete(pm.pointConstraint(joint_node, start_flag_loc_align, w=True, mo=False))

        pm.move(start_x_loc, [5, 0, 0], r=1, os=1)
        pm.move(start_y_loc, [0, 5, 0], r=1, os=1)
        pm.orientConstraint(start_rotate_flag.pynode, start_flag_loc, w=True, mo=False)
        # End Aims
        end_weight = 1 - start_weight
        end_flag_loc = dag_utils.create_locator_at_object(end_rotate_flag.pynode, f"end_flag_aims_orient_{index+1}")
        end_flag_loc_align = dag_utils.create_aligned_parent_group(end_flag_loc)
        end_x_loc = dag_utils.create_locator_at_object(end_rotate_flag.pynode, f"end_flag_aim_x_{index+1}")
        end_y_loc = dag_utils.create_locator_at_object(end_rotate_flag.pynode, f"end_flag_aim_y_{index+1}")
        end_x_loc.setParent(end_flag_loc)
        end_y_loc.setParent(end_flag_loc)
        pm.delete(pm.pointConstraint(joint_node, end_flag_loc_align, w=True, mo=False))

        pm.move(end_x_loc, [5, 0, 0], r=1, os=1)
        pm.move(end_y_loc, [0, 5, 0], r=1, os=1)
        pm.orientConstraint(end_rotate_flag.pynode, end_flag_loc, w=True, mo=False)
        # Final Aims
        end_rotate_flag.pynode.addAttr(f"twist_bias_{index+2}", dv=end_weight, min=0, max=1, keyable=True)
        bias_attr = end_rotate_flag.pynode.attr(f"twist_bias_{index+2}")
        bias_attr.set(keyable=False, cb=False)
        weight_reverse = pm.createNode("reverse", n=f"bias_{index+2}_reverse")
        weight_reverse_nodes.append(weight_reverse)
        bias_attr >> weight_reverse.inputX
        x_aim_loc = pm.spaceLocator(n=f"aim_x_locator_{index+1}")
        x_const = pm.pointConstraint([start_x_loc, end_x_loc], x_aim_loc, w=True, mo=False)
        y_aim_loc = pm.spaceLocator(n=f"aim_y_locator_{index+1}")
        y_const = pm.pointConstraint([start_y_loc, end_y_loc], y_aim_loc, w=True, mo=False)

        weight_reverse.outputX >> x_const.getWeightAliasList()[0]
        bias_attr >> x_const.getWeightAliasList()[1]
        weight_reverse.outputX >> y_const.getWeightAliasList()[0]
        bias_attr >> y_const.getWeightAliasList()[1]

        # Create Aim
        mid_control = pm.spaceLocator(n=f"mid_{index+1}_aimer")
        mid_control.rotateOrder.set(joint_node.rotateOrder.get())
        mid_control_align = dag_utils.create_aligned_parent_group(mid_control)
        pm.delete(pm.pointConstraint(joint_node, mid_control_align, w=True, mo=False))

        start_flag_loc_align.setParent(mid_control_align)
        end_flag_loc_align.setParent(mid_control_align)
        pm.aimConstraint(x_aim_loc, mid_control, w=True, offset=[0, 0, 0],
                         mo=False, aimVector=[1, 0, 0], upVector=[0, 1, 0],
                         worldUpType="object", worldUpObject=y_aim_loc)

        offset_group = pm.group(empty=True, n=f"mid_{index+1}_offset_group_{wrapped_joint.side}_{wrapped_joint.region}")
        offset_group.rotateOrder.set(joint_node.rotateOrder.get())
        pm.delete(pm.parentConstraint(mid_control, offset_group, w=True, mo=False))
        mid_offset_groups.append(offset_group)

        offset_group.setParent(mid_control)
        pm.delete(pm.parentConstraint(joint_node, offset_group, w=True, mo=False))

        mid_flag = flags.Flag.create(f'{flag_name}{index+1}_mid', joint_node, scale)
        mid_flag.side = wrapped_joint.side
        mid_flag.region = wrapped_joint.region
        pm.pointConstraint(joint_node, mid_flag.pynode, w=True, mo=False)
        pm.orientConstraint(offset_group, mid_flag.align_group, w=True, mo=False)
        mid_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)
        mid_flag.swap_shape('ring directional', scale, rot_offset)
        mid_flag.sub = True
        flag_list.append(mid_flag)

        # control mid joint
        pm.pointConstraint(joint_node, mid_control_align, w=True, mo=False)
        pm.orientConstraint(mid_flag.pynode, joint_node, w=True, mo=False)
        mid_control_align.setParent(mid_group)
        y_aim_loc.setParent(mid_group)
        x_aim_loc.setParent(mid_group)
        mid_groups.append(mid_group)
    flag_list.append(end_rotate_flag)

    sub_flag_list = []
    # Sub ctrls
    for joint_node in [joint_chain[-1], joint_chain[0]]:
        flag_name = f'{naming.get_basename(joint_node)}_sub'
        sub_flag = flags.Flag.create(flag_name, joint_node)
        sub_flag.side = wrapped_joint.side
        sub_flag.region = wrapped_joint.region
        sub_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)
        sub_flag.swap_shape('ring directional', scale*.75, rot_offset)
        sub_flag.detail = True
        sub_flag.sub = True
        sub_flag_list.append(sub_flag)

    # final constraints
    pm.pointConstraint(joint_chain[0], sub_flag_list[0].align_group, w=True, mo=False)
    pm.pointConstraint(joint_chain[-1], sub_flag_list[-1].align_group, w=True, mo=False)
    pm.orientConstraint(sub_flag_list[0].pynode, joint_chain[0], w=True, mo=False)
    pm.orientConstraint(sub_flag_list[-1].pynode, joint_chain[-1], w=True, mo=False)
    pm.orientConstraint(end_rotate_flag.pynode, sub_flag_list[-1].align_group, w=True, mo=False)
    pm.orientConstraint(start_rotate_flag.pynode, sub_flag_list[0].align_group, w=True, mo=False)

    return_dict = {}
    return_dict['start_flag'] = flag_list[0]
    return_dict['end_flag'] = flag_list[-1]
    return_dict['flags'] = flag_list+sub_flag_list
    return_dict['mid_flags'] = flag_list[1:-1]
    return_dict['mid_groups'] = mid_groups
    return_dict['mid_offset_groups'] = mid_offset_groups
    return_dict['sub_flags'] = sub_flag_list
    return_dict['reverse_nodes'] = weight_reverse_nodes
    return return_dict