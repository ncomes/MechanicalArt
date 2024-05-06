#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Tracks Joint data for face meshes.
"""

from __future__ import print_function, division, absolute_import

import pymel.core as pm

from mca.mya.utils import dag
from mca.mya.rigging import rig_utils
from mca.mya.rigging.flags import frag_flag


FLAG_SHAPES = ('square', 'square', 'oval')


def rfk_chain(start_joint, end_joint, side, region, scale=1.0, create_sub_flags=True, suffix='rfk_chain'):
    """

    :param start_joint:
    :param end_joint:
    :param create_sub_flags:
    :param suffix:
    :return:
    """
    if not isinstance(start_joint, pm.nt.Joint) or not isinstance(end_joint, pm.nt.Joint):
        start_joint = pm.PyNode(start_joint)
        end_joint = pm.PyNode(end_joint)

    rfkChain = dag.get_between_nodes(start_joint, end_joint)
    num_mid_joints = len(rfkChain) - 2  # - start_joint, end_joint

    # Create Start and End flags
    label = rfkChain[0].nodeName().replace('_' + suffix, '')
    label = label.split(':')[-1]

    flags_groups = []
    start_rotate_flag = frag_flag.Flag.create_ratio(object_to_match=rfkChain[0], scale=scale, label=label)
    flags_groups.append(start_rotate_flag.getParent())

    label = rfkChain[-1].nodeName().replace(('_' + suffix), '')
    label = label.split(':')[-1]

    end_rotate_flag = frag_flag.Flag.create_ratio(object_to_match=rfkChain[-1], scale=scale, label=label)
    flags_groups.append(end_rotate_flag.getParent())

    mid_groups = []
    mid_offset_groups = []
    mid_flags = []
    weight_reverse_nodes = []
    # Subtrack the start and end joints
    for x in range(num_mid_joints):
        mid_joint = rfkChain[x + 1]
        mid_group = pm.group(empty=True, n="rfk_mid_group_{0}".format(x))
        pm.delete(pm.parentConstraint(mid_joint, mid_group, w=True, mo=False))
        # create aims
        # start_aims
        start_weight = 1 - pm.util.smoothstep(0, 1, (x + 1.0) / (num_mid_joints + 1.0))
        start_flag_loc = rig_utils.create_locator_at_object(start_rotate_flag)
        start_flag_loc.rename("start_flag_aims_orient_{0}".format(x))
        start_flag_loc_align = rig_utils.create_align_transform(start_flag_loc)
        start_x_loc = rig_utils.create_locator_at_object(start_rotate_flag)
        start_x_loc.rename("start_flag_aim_x_{0}".format(x))
        start_y_loc = rig_utils.create_locator_at_object(start_rotate_flag)
        start_y_loc.rename("start_flag_aim_y_{0}".format(x))
        start_x_loc.setParent(start_flag_loc)
        start_y_loc.setParent(start_flag_loc)
        pm.delete(pm.pointConstraint(mid_joint, start_flag_loc_align, w=True, mo=False))

        pm.move(start_x_loc, [5, 0, 0], r=1, os=1)
        pm.move(start_y_loc, [0, 5, 0], r=1, os=1)
        pm.orientConstraint(start_rotate_flag, start_flag_loc, w=1, mo=False)
        # End Aims
        end_weight = 1 - start_weight
        end_flag_loc = rig_utils.create_locator_at_object(end_rotate_flag)
        end_flag_loc.rename("end_flag_aims_orient_{0}".format(x))
        end_flag_loc_align = rig_utils.create_align_transform(end_flag_loc)
        end_x_loc = rig_utils.create_locator_at_object(end_rotate_flag)
        end_x_loc.rename("end_flag_aim_x_{0}".format(x))
        end_y_loc = rig_utils.create_locator_at_object(end_rotate_flag)
        end_y_loc.rename("end_flag_aim_y_{0}".format(x))
        end_x_loc.setParent(end_flag_loc)
        end_y_loc.setParent(end_flag_loc)
        pm.delete(pm.pointConstraint(mid_joint, end_flag_loc_align, w=True, mo=False))

        pm.move(end_x_loc, [5, 0, 0], r=1, os=1)
        pm.move(end_y_loc, [0, 5, 0], r=1, os=1)
        pm.orientConstraint(end_rotate_flag, end_flag_loc, w=1, mo=False)
        # Final Aims
        end_rotate_flag.addAttr("twist_bias_{0}".format(x + 1), dv=end_weight, min=0, max=1, keyable=True)
        bias_attr = end_rotate_flag.attr("twist_bias_{0}".format(x + 1))
        bias_attr.set(keyable=False, cb=False)
        weight_reverse = pm.createNode("reverse", n="bias_{0}_reverse".format(x + 1))
        weight_reverse_nodes.append(weight_reverse)
        bias_attr >> weight_reverse.inputX
        x_aim_loc = pm.spaceLocator()
        x_aim_loc.rename("aim_x_locator_{0}".format(x))
        x_const = pm.pointConstraint([start_x_loc, end_x_loc], x_aim_loc, w=1.0, mo=False)
        y_aim_loc = pm.spaceLocator()
        y_aim_loc.rename("aim_y_locator_{0}".format(x))
        y_const = pm.pointConstraint([start_y_loc, end_y_loc], y_aim_loc, w=1.0, mo=False)

        weight_reverse.outputX >> x_const.getWeightAliasList()[0]
        bias_attr >> x_const.getWeightAliasList()[1]
        weight_reverse.outputX >> y_const.getWeightAliasList()[0]
        bias_attr >> y_const.getWeightAliasList()[1]

        # Create Aim
        label = mid_joint.nodeName().replace('_' + suffix, '')
        label = label.split(':')[-1]

        mid_control = pm.spaceLocator()
        mid_control.rename("mid_{0}_aimer".format(x))
        mid_control.rotateOrder.set(mid_joint.rotateOrder.get())
        mid_control_align = rig_utils.create_align_transform(mid_control)
        pm.delete(pm.pointConstraint(mid_joint, mid_control_align, w=True, mo=False))

        start_flag_loc_align.setParent(mid_control_align)
        end_flag_loc_align.setParent(mid_control_align)
        pm.aimConstraint(x_aim_loc,
                            mid_control,
                            w=1,
                            offset=[0, 0, 0],
                            mo=False,
                            aimVector=[1, 0, 0],
                            upVector=[0, 1, 0],
                            worldUpType="object",
                            worldUpObject=y_aim_loc)

        offset_group = pm.group(empty=True, n="mid_{0}_offset_group_{1}_{2}".format(x, side, region))
        offset_group.rotateOrder.set(mid_joint.rotateOrder.get())
        pm.delete(pm.parentConstraint(mid_control, offset_group, w=True, mo=False))
        mid_offset_groups.append(offset_group)

        offset_group.setParent(mid_control)
        pm.delete(pm.parentConstraint(mid_joint, offset_group, w=True, mo=False))

        mid_flag = frag_flag.Flag.create(mid_joint, scale=scale, label=label, is_sub=True)

        mid_flag_align = mid_flag.get_align_transform()
        pm.orientConstraint(offset_group, mid_flag_align, w=1, mo=False)
        pm.pointConstraint(mid_joint, mid_flag, w=1)
        flags_groups.append(mid_flag_align)

        # control mid joint
        pm.pointConstraint(mid_joint, mid_control_align, mo=False, w=1)
        pm.orientConstraint(mid_flag, mid_joint, mo=False, w=1)
        mid_control_align.setParent(mid_group)
        y_aim_loc.setParent(mid_group)
        x_aim_loc.setParent(mid_group)
        mid_groups.append(mid_group)
        mid_flags.append(mid_flag)

    sub_end_align = None
    sub_start_align = None
    sub_end_flag = None
    sub_start_flag = None
    if create_sub_flags:
        # Create sub controls under start and end flags
        label = rfkChain[-1].nodeName().replace('_' + suffix, '')
        label = label.split(':')[-1]

        sub_end_flag = frag_flag.Flag.create_ratio(object_to_match=rfkChain[-1],
                                                   label=label,
                                                   scale=scale*.75,
                                                   add_align_transform=False,
                                                   is_detail=True,
                                                   is_sub=True)
        sub_end_flag = pm.rename(sub_end_flag, str(sub_end_flag) + '_sub')
        sub_end_align = rig_utils.create_align_transform(sub_end_flag)
        flags_groups.append(sub_end_align)

        label = rfkChain[0].nodeName().replace('_' + suffix, '')
        label = label.split(':')[-1]
        sub_start_flag = frag_flag.Flag.create_ratio(object_to_match=rfkChain[0],
                                                     label=label,
                                                     scale=scale*.75,
                                                     add_align_transform=False,
                                                     is_detail=True,
                                                     is_sub=True)
        sub_start_flag = pm.rename(sub_start_flag, str(sub_start_flag) + '_sub')
        sub_start_align = rig_utils.create_align_transform(sub_start_flag)
        flags_groups.append(sub_start_align)

    # final constraints
    pm.pointConstraint(rfkChain[-1], end_rotate_flag, mo=False, w=1)
    pm.pointConstraint(rfkChain[0], start_rotate_flag, mo=False, w=1)

    if create_sub_flags:
        pm.pointConstraint(rfkChain[-1], sub_end_align, mo=False, w=1)
        pm.pointConstraint(rfkChain[0], sub_start_align, mo=False, w=1)
        pm.orientConstraint(sub_end_flag, rfkChain[-1], mo=False, w=1)
        pm.orientConstraint(sub_start_flag, start_joint, mo=False, w=1)
        pm.orientConstraint(end_rotate_flag, sub_end_align, mo=False, w=1)
        pm.orientConstraint(start_rotate_flag, sub_start_align, mo=False, w=1)
    else:
        pm.orientConstraint(end_rotate_flag, rfkChain[-1], mo=False, w=1)
        pm.orientConstraint(start_rotate_flag, start_joint, mo=False, w=1)

    dict = {}
    dict['start_joint'] = start_joint
    dict['end_joint'] = end_joint
    dict['mid_flags'] = mid_flags
    dict['flags_groups'] = flags_groups
    dict['mid_groups'] = mid_groups
    dict['mid_offset_groups'] = mid_offset_groups
    dict['start_twist_flag'] = start_rotate_flag
    dict['end_twist_flag'] = end_rotate_flag
    dict['sub_flags'] = [sub_start_flag, sub_end_flag]
    dict['reverse_nodes'] = weight_reverse_nodes
    if not sub_start_flag and not sub_end_flag:
        dict['sub_flags'] = []

    return dict
