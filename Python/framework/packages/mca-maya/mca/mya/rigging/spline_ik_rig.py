#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates spline IK
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.rigging import rig_utils
from mca.mya.rigging.flags import frag_flag
from mca.mya.utils import attr_utils, constraint, naming
from mca.mya.rigging import joint_utils


def spline_ctrl(spline_joint_chain, end_helper_joint, mid_helper_joint, region, side,
                start_helper_joint=None, mid_flag=True, can_retract=True, root_align_transform=True):
    """
    Creates a flexible spline IK. This spline IK has more features than a simple spline IK, but less micro control.
    It requires an end and mid helper to be able to recover animation.

    :param list[Joint] spline_joint_chain: A continuous hierarchy of joints for the ik to be built on.
    :param Joint start_helper_joint: A joint separated, but co-located with the start joint of the primary chain.
    :param Joint end_helper_joint: A joint co-located with the last joint spline_joint_chain
    :param Joint mid_helper_joint: A joint that sits at the midpoint between the first and last joint of the spline_joint_chain
        We use this to store the midpoint control position, and is required to recover animation.
    :param str region: Region identifier
    :param str side: Side identifier
    :param bool mid_flag: If a midpoint flag should be built.
    :param bool can_retract: If this spline IK should be able to retract along it's length.
    :param bool root_align_transform: If we should create align transforms when building the flags.
    :return: A dictionary of notable built nodes.
    :rtype: dict
    """

    constraint_list = []
    flag_list = []
    suffix = 'spline_ik'

    sca = 1.0


    # We'll need to duplicate our end helper as a holder for the final orientation of the chain.
    # $Hack FSchorsch it's a bit of a hack that we need this node, but the smooth transition from aux orientation to
    # chain orientation requires two targets since mya cannot lerp an orientation constraint with a single target.
    orient_end = joint_utils.duplicate_joint(end_helper_joint, f'{region}_{side}_{suffix}_orient_end')
    orient_end.setParent(None)
    constraint_list.append(constraint.scale_constraint_safe(spline_joint_chain[-1], orient_end))

    start_flag = None
    if start_helper_joint:
        start_flag = frag_flag.Flag.create(start_helper_joint,
                                      label=f'{region}_{side}_{suffix}_start',
                                      add_align_transform=root_align_transform,
                                      is_sub=True)
        start_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
        start_flag.set_as_detail()
        constraint_list.append(constraint.parent_constraint_safe(start_flag, start_helper_joint))
        flag_list.append(start_flag)
    else:
        start_helper_joint = joint_utils.duplicate_joint(spline_joint_chain[0], f'{region}_{side}_{suffix}_start_align')
        start_helper_joint.setParent(None)

    end_flag = frag_flag.Flag.create(end_helper_joint,
                                label=f'{region}_{side}_{suffix}_end',
                                scale=sca,
                                add_align_transform=root_align_transform)
    end_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
    # We want the Spline Ik to follow both the rotation and the position of the end flag.
    constraint_list.append(constraint.parent_constraint_safe(end_flag, end_helper_joint))

    end_aux_flag = frag_flag.Flag.create(end_helper_joint,
                                    label=f'{region}_{side}_{suffix}_end_aux',
                                    scale=sca*.75,
                                    add_align_transform=True,
                                    is_sub=True)
    end_aux_flag.get_align_transform().setParent(end_flag)
    end_aux_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS + attr_utils.TRANSLATION_ATTRS)
    end_aux_flag.set_as_sub()
    # We want the AUX flag to handle the orientation of all children joints of the IK Spline.
    end_aux_constraint = constraint.parent_constraint_safe([end_aux_flag, spline_joint_chain[-1]], orient_end)
    constraint_list.append(end_aux_constraint)
    # appending this in reverse order so it'll better match the bind joint list on frag
    flag_list.append(end_aux_flag)
    flag_list.append(end_flag)

    # CREATE SPLINE IK
    spline_ik_handle, spline_ik_eff, spline_ik_curve = pm.ikHandle(sol='ikSplineSolver',
                                                                   n=f'{region}_{side}_{suffix}_ikHandle',
                                                                   ccv=True,
                                                                   numSpans=2,
                                                                   startJoint=spline_joint_chain[0],
                                                                   endEffector=spline_joint_chain[-1])
    spline_ik_curve.rename(f'{region}_{side}_{suffix}_curve')
    ik_solver = spline_ik_handle.ikSolver.get()
    # chain orientation group
    chain_grp = rig_utils.create_align_transform(spline_joint_chain[0])
    if start_flag:
        constraint_list.append(constraint.parent_constraint_safe(start_flag, chain_grp, mo=True))

    # SKIN CONTROL JOINTS TO CURVE
    influ = [start_helper_joint, end_helper_joint]
    skin_cluster = pm.skinCluster(influ,
                   spline_ik_curve,
                   n=f'{region}_{side}_{suffix}_skinCluster',
                   toSelectedBones=True, bindMethod=0,
                   skinMethod=0, normalizeWeights=1)

    # MIDDLE FLAG
    if mid_flag:
        clus = pm.cluster(spline_ik_curve.cv[2], n=f'{region}_{side}_{suffix}_cluster')[1]
        clus.v.set(False)

        mid_flag = frag_flag.Flag.create(clus,
                                    label=f'{region}_{side}_{suffix}_mid',
                                    scale=sca*.5,
                                    add_align_transform=True,
                                    is_sub=True)
        mid_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS + attr_utils.ROTATION_ATTRS)
        flag_list.append(mid_flag)

        constraint_list.append(constraint.parent_constraint_safe(mid_flag, mid_helper_joint))
        # using a constriant here results in some awkward results, directly connect the attrs instead.
        mid_flag.t >> clus.t
        mid_flag.r >> clus.r
    mult_nodes = []
    mult_node = pm.createNode("multiplyDivide", n=f'{region}_{side}_{suffix}_multi_stretch')
    mult_nodes.append(mult_node)
    info_node = pm.createNode("curveInfo", n=f'{region}_{side}_{suffix}_curve_info')

    spline_ik_curve.getShape().worldSpace >> info_node.inputCurve
    info_node.arcLength >> mult_node.input1.input1X

    spline_length = info_node.getAttr('arcLength')
    mult_node.setAttr('input2X', spline_length)
    mult_node.setAttr('operation', 2)

    for joint_node in spline_joint_chain:
        mult_node.outputX >> joint_node.sx

    if can_retract:
        remap_nodes = []
        # End joint orientaton for retract.
        end_flag.addAttr('retract', dv=0, min=0, max=10, k=True)

        # CREATE MOTION PATH NODE FOR AUX TO FOLLOW CURVE
        last_in_chain = spline_joint_chain[-1]
        mp = pm.createNode('motionPath', n=f'{region}_{side}_{suffix}_mp')
        last_in_chain.tx >> mp.uValue
        spline_ik_curve.worldSpace >> mp.geometryPath

        # CREATE MULTIPLY/DIVIDE NODE TO DIVIDE UVALUE
        mult = pm.createNode('multiplyDivide', n=f'{region}_{side}_{suffix}_multi_retract')
        mult_nodes.append(mult)
        mult.setAttr('operation', 2)
        mp.uValue >> mult.input1X
        mult.setAttr('input2X', 6)

        # CREATE CONDITION NODE SO JOINT IS ONLY SCALED WHEN NEEDED
        condition = pm.createNode('condition', n=f'{region}_{side}_{suffix}_condition')
        mp.uValue >> condition.firstTerm
        mult.outputX >> condition.colorIfTrueR
        condition.setAttr('secondTerm', 6)
        condition.setAttr('operation', 4)
        condition.outColorR >> end_helper_joint.sy
        condition.outColorR >> end_helper_joint.sz

        # switch prime joint orientation from ux flag to main flag.
        aux_con_remap = pm.createNode('remapValue', n=f'{region}_{side}_{suffix}_constraint_remap')
        remap_nodes.append(aux_con_remap)
        aux_con_remap.setAttr('inputMin', 0.00)
        aux_con_remap.setAttr('inputMax', 3.00)
        aux_con_remap.setAttr('outputMin', 1.00)
        aux_con_remap.setAttr('outputMax', 0.01)

        constraint_rev = pm.createNode('reverse', n=f'{region}_{side}_{suffix}_constraint_reverse')
        aux_con_remap.outValue >> constraint_rev.inputX
        end_flag.retract >> aux_con_remap.inputValue

        aux_con_remap.outValue >> end_aux_constraint.attr(f'{naming.get_basename(end_aux_flag)}W0')
        constraint_rev.outputX >> end_aux_constraint.attr(f'{naming.get_basename(spline_joint_chain[-1])}W1')

        increment_value = 10 / len(spline_joint_chain)
        # retract joints along chain.
        for index, chain_joint in enumerate(spline_joint_chain):
            joint_tx = chain_joint.getAttr('tx')
            if index:
                # handle translation down the spline
                remap_tx = pm.createNode('remapValue', n=f'{naming.get_basename(chain_joint)}_{suffix}_remap_tx')
                remap_nodes.append(remap_tx)
                end_flag.retract >> remap_tx.inputValue

                # joint will be at its default tx value until we enter the remap range, where it will shrink
                remap_tx.setAttr('outputMin', joint_tx)
                remap_tx.setAttr('outputMax', 0.001)
                # set our active range for this joint for it's slice between 0-10
                remap_tx.setAttr('inputMin', (index - 1.0) * increment_value)
                remap_tx.setAttr('inputMax', index * increment_value)
                remap_tx.outValue >> chain_joint.tx

            # start the scale delayed
            remap_sca = pm.createNode('remapValue', n=f'{naming.get_basename(chain_joint)}_{suffix}_remap_scale')
            remap_nodes.append(remap_sca)
            remap_sca.setAttr('outputMin', 1)
            remap_sca.setAttr('outputMax', 0)
            end_flag.retract >> remap_sca.inputValue
            remap_sca.setAttr('inputMin', min((index + 1) * increment_value, (10 - increment_value * 1.25)))
            remap_sca.setAttr('inputMax', min((index + 2) * increment_value, (10 - increment_value * .75)))


            remap_sca.outValue >> chain_joint.sy
            remap_sca.outValue >> chain_joint.sz

    return_dictionary = {}
    return_dictionary['flag_nodes'] = flag_list
    return_dictionary['start_flag'] = start_flag
    return_dictionary['mid_flag'] = mid_flag
    return_dictionary['end_flag'] = end_flag
    return_dictionary['aux_flag'] = end_aux_flag
    return_dictionary['orient_end'] = orient_end
    return_dictionary['parent_cons'] = constraint_list
    return_dictionary['curve'] = spline_ik_curve
    return_dictionary['handle'] = spline_ik_curve
    return_dictionary['do_not_touch'] = [orient_end, spline_ik_handle, spline_ik_curve, clus]
    return_dictionary['start_helper_joint'] = start_helper_joint
    return_dictionary['spline_skin_cluster'] = skin_cluster
    return_dictionary['mult_nodes'] = mult_nodes
    return_dictionary['info_node'] = info_node
    return_dictionary['ik_solver'] = ik_solver

    if can_retract:
        return_dictionary['remap_nodes'] = remap_nodes
        return_dictionary['motion_path'] = mp
        return_dictionary['condition'] = condition
        return_dictionary['reverse_nodes'] = constraint_rev

    if mid_flag:
        return_dictionary['mid_flag'] = mid_flag
        return_dictionary['do_not_touch'].append(clus)
    if not start_flag:
        return_dictionary['do_not_touch'].append(start_helper_joint)

    return return_dictionary