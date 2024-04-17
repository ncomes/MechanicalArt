#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates spline IK
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.rigging.flags import tek_flag
from mca.mya.utils import constraint


def spline_ctrl(start_joint,
                end_joint,
                spline_ctrl_start,
                spline_ctrl_end,
                aux_ctrl_joint,
                region,
                side,
                mid_spline_flag=True,
                root_align_transform=True):
    """

    :param pm.nt.Joint start_joint: Start of joint chain
    :param pm.nt.Joint end_joint: End of joint chain
    :param pm.nt.Joint spline_ctrl_start: Control joint for start of curve
    :param pm.nt.Joint spline_ctrl_end: Control joint for end of curve
    :param pm.nt.Joint aux_ctrl_joint: Aux joint on end of chain
    :param str region: Region on body
    :param str side: Side on body
    :param bool mid_spline_flag: If True, creates a flag in middle of curve
    :param bool root_align_transform: If True, creates align transform
    :return: Returns a dictionary of built objects
    :rtype: dictionary
    """

    if not pm.objExists(start_joint):
        raise pm.MayaNodeError("start_joint given, {0} , doesn't exist".format(start_joint))
    if not pm.objExists(start_joint):
        raise pm.MayaNodeError("spline_ctrl_start given, {0} , doesn't exist".format(spline_ctrl_start))
    if not pm.objExists(start_joint):
        raise pm.MayaNodeError("spline_ctrl_end, {0} , doesn't exist".format(spline_ctrl_end))


    flag_nodes = []
    parent_cons = []

    # START FLAG
    start_label = '{0}_start'.format(region)
    start_flag_node = tek_flag.Flag.create(spline_ctrl_start,
                                       label=start_label,
                                       add_align_transform=root_align_transform)
    start_parent_con = pm.parentConstraint(start_flag_node, spline_ctrl_start, w=1, mo=1)
    parent_cons.append(start_parent_con)
    flag_nodes.append(start_flag_node)
    pm.addAttr(ln='tekParent', at='message')

    # END FLAG
    end_label = '{0}_end'.format(region)
    end_flag_node = tek_flag.Flag.create(spline_ctrl_end,
                                     label=end_label,
                                     add_align_transform=root_align_transform)
    end_parent_con = pm.parentConstraint(end_flag_node, spline_ctrl_end, w=1, mo=1)
    parent_cons.append(end_parent_con)
    flag_nodes.append(end_flag_node)
    pm.addAttr(ln='tekParent', at='message')

    # AUX FLAG

    aux_flag_node = tek_flag.Flag.create(aux_ctrl_joint,
                                     label=region + '_aux',
                                     add_align_transform=True)
    aux_parent_con = pm.parentConstraint(aux_flag_node, aux_ctrl_joint, w=1, mo=1)
    aux_flag_align_transform = aux_flag_node.get_align_transform()
    aux_attach = constraint.parent_constraint_safe(spline_ctrl_end, aux_flag_align_transform,
                                                   skip_rotate_attrs=[], skip_translate_attrs=[])
    aux_secondary_constraint = pm.parentConstraint(end_joint, aux_ctrl_joint)
    parent_cons.append(aux_parent_con)
    parent_cons.append(aux_secondary_constraint)
    pm.addAttr(ln='tekParent', at='message')


    # CREATE SPLINE IK
    handle, eff, curve = pm.ikHandle(sol='ikSplineSolver',
                                     n=region + '_ikHandle',
                                     ccv=True,
                                     ns=2,
                                     startJoint=start_joint,
                                     endEffector=end_joint)
    pm.rename(curve, f'{region}_curve')

    # SKIN CONTROL JOINTS TO CURVE
    influ = [spline_ctrl_start, spline_ctrl_end]
    pm.skinCluster(influ,
                   curve,
                   n=f'{region}_skinCluster',
                   toSelectedBones=True, bindMethod=0,
                   skinMethod=0, normalizeWeights=1)

    # MIDDLE FLAG
    if mid_spline_flag:
        cv = pm.PyNode(f'{curve}.cv[2]')
        clus = pm.cluster(cv, n=f'mid{region}_cluster')[1]
        mid_flag = tek_flag.Flag.create_ratio(object_to_match=clus,
                                          label=f'{region}_mid',
                                          scale=0.5,
                                          add_align_transform=True,
                                          is_sub=True)
        mid_flag_align_transform = mid_flag.alignTransform.get()

        mid_flag_constraint = pm.pointConstraint(start_flag_node,
                                                  end_flag_node,
                                                  mid_flag_align_transform)
        parent_cons.append(mid_flag_constraint)
        pm.addAttr(ln='tekParent', at='message')

        pm.connectAttr(f'f_{region}_mid.translate', f'{clus}.translate')
        pm.connectAttr(f'f_{region}_mid.rotate', f'{clus}.rotate')

        clus_grp = pm.group(clus, n=f'NO_TOUCH_{side}_{region}_mid')
        pm.parent(clus_grp, pm.PyNode('DO_NOT_TOUCH'))
        pm.setAttr(f'{clus_grp}.visibility', 0)
    else:
        pass

    # SQUASH AND STRETCH (LENGTH ONLY)
    mult_node = pm.createNode("multiplyDivide", n=f'flags_{end_joint}_stretchFactor')
    info_node = pm.createNode("curveInfo", n=f'{curve}_infoNode')

    pm.connectAttr(f'{curve}Shape.worldSpace', f'{info_node}.inputCurve')
    pm.connectAttr(f'{info_node}.arcLength', f'{mult_node}.input1.input1X')

    length = pm.getAttr(f'{info_node}.arcLength')

    pm.setAttr(f'{mult_node}.input2X', length)
    pm.setAttr(f'{mult_node}.operation', 2)

    return_dictionary = {}
    return_dictionary['flag_nodes'] = flag_nodes
    return_dictionary['aux_flag'] = aux_flag_node
    return_dictionary['parent_cons'] = parent_cons
    return_dictionary['curve'] = curve
    return_dictionary['handle'] = handle
    return_dictionary['mult_node'] = mult_node
    return_dictionary['info_node'] = info_node
    return_dictionary['length'] = length
    if mid_spline_flag:
        return_dictionary['mid_flag'] = mid_flag
        return_dictionary['clus'] = clus
        return_dictionary['clus_grp'] = clus_grp
    else:
        pass

    return return_dictionary


def retract_aux(joint,
                follow_joint,
                curve,
                jnt_constraint,
                start_flg,
                aux_flg):

    """

    :param pm.nt.Joint joint: Joint to work with
    :param pm.nt.Joint follow_joint: Joint which initial joint should follow
    :param pm.nt.Transform curve: Curve to follow on
    :param pm.nt.parentConstraint jnt_constraint: Constraint to work with
    :param pm.nt.Transform start_flg: Flag which contains retract control
    :param str aux_flg: Flag which aux jnt is constrained to
    :return: Returns a dictionary of built nodes
    :rtype: dictionary
    """

    joint = joint[0]
    # CREATE MOTION PATH NODE FOR AUX TO FOLLOW CURVE
    mp = pm.createNode('motionPath', n=f'{joint}_mp')
    pm.connectAttr(f'{follow_joint}.translateX', f'{mp}.uValue')
    pm.connectAttr(f'{curve}.worldSpace', f'{mp}.geometryPath')

    # CREATE MULTIPLY/DIVIDE NODE TO DIVIDE UVALUE
    mult = pm.createNode('multiplyDivide', n=f'{joint}_mult_node')
    pm.setAttr(f'{mult}.operation', 2)
    pm.connectAttr(f'{mp}.uValue', f'{mult}.input1X')
    pm.setAttr(f'{mult}.input2X', 6)

    # CREATE CONDITION NODE SO JOINT IS ONLY SCALED WHEN NEEDED
    condition = pm.createNode('condition', n=f'{joint}_cond')
    pm.connectAttr(f'{mp}.uValue', f'{condition}.firstTerm')
    pm.connectAttr(f'{mult}.output.outputX', f'{condition}.colorIfTrue.colorIfTrueR')
    pm.setAttr(f'{condition}.secondTerm', 6)
    pm.setAttr(f'{condition}.operation', 4)
    pm.connectAttr(f'{condition}.outColor.outColorR', f'{joint}.scale.scaleY')
    pm.connectAttr(f'{condition}.outColor.outColorR', f'{joint}.scale.scaleZ')

    # SWITCH AUX JOINT CONSTRAINT FROM FLAG TO JNT
    aux_con_remap_01 = pm.createNode('remapValue', n=f'{joint}_constraint_remap_01')
    aux_con_remap_02 = pm.createNode('remapValue', n=f'{joint}_constraint_remap_02')

    pm.connectAttr(f'{start_flg}.Retract', f'{aux_con_remap_01}.inputValue')
    pm.setAttr(f'{aux_con_remap_01}.inputMin', 0.00)
    pm.setAttr(f'{aux_con_remap_01}.inputMax', 3.00)
    pm.setAttr(f'{aux_con_remap_01}.outputMin', 1.00)
    pm.setAttr(f'{aux_con_remap_01}.outputMax', 0.00)
    pm.connectAttr(f'{aux_con_remap_01}.outValue', f'{jnt_constraint}.{aux_flg}W0')

    pm.connectAttr(f'{start_flg}.Retract', f'{aux_con_remap_02}.inputValue')
    pm.setAttr(f'{aux_con_remap_02}.inputMin', 0.00)
    pm.setAttr(f'{aux_con_remap_02}.inputMax', 3.00)
    pm.setAttr(f'{aux_con_remap_02}.outputMin', 0.00)
    pm.setAttr(f'{aux_con_remap_02}.outputMax', 1.00)
    pm.connectAttr(f'{aux_con_remap_02}.outValue', f'{jnt_constraint}.{follow_joint}W1')

    return_dictionary = {}
    return_dictionary['aux_motion_path'] = mp
    return_dictionary['aux_mult'] = mult
    return_dictionary['aux_condition'] = condition
    return return_dictionary


def spore_shooter(align_grps,
                  start_flag,
                  val):

    """

    :param pm.nt.Transform align_grps: Groups to connect built nodes to
    :param float val: Value at which action is completed per joint
    :param pm.nt.Transform start_flag: Flag which contains controls for spore
    :return: Returns a dictionary of built nodes
    :rtype: dictionary
    """

    remap_nodes = []
    subtract_nodes = []
    multiply_nodes = []
    condition_nodes = []

    for align_grp in align_grps:
        align_grp = pm.PyNode(align_grp)

        # CREATE NODES
        remap_01 = pm.createNode('remapValue', n=f'{align_grp}_shoot_rm_value_01')
        remap_02 = pm.createNode('remapValue', n=f'{align_grp}_shoot_rm_value_01')
        sub = pm.createNode('plusMinusAverage', n=f'{align_grp}_shoot_subtract')
        mult = pm.createNode('multiplyDivide', n=f'{align_grp}_spore_size')
        cond = pm.createNode('condition', n=f'{align_grp}_spore_condition')
        cond_02 = pm.createNode('condition', n=f'{align_grp}_spore_condition_02')

        remap_nodes.append(remap_01)
        remap_nodes.append(remap_02)
        multiply_nodes.append(mult)
        subtract_nodes.append(sub)
        condition_nodes.append(cond)
        condition_nodes.append(cond_02)

        # CONNECT ATTRS
        pm.connectAttr(f'{start_flag}.Spore', f'{remap_01}.inputValue')
        pm.connectAttr(f'{start_flag}.Spore', f'{remap_02}.inputValue')
        pm.connectAttr(f'{remap_01}.outValue', f'{sub}.input1D[0]')
        pm.connectAttr(f'{remap_02}.outValue', f'{sub}.input1D[2]')

        pm.connectAttr(f'{sub}.output1D', f'{mult}.input2.input2X')
        pm.connectAttr(f'{start_flag}.Spore_Size', f'{mult}.input1.input1X')
        pm.connectAttr(f'{mult}.output.outputX', f'{cond}.colorIfTrue.colorIfTrueR')
        pm.connectAttr(f'{sub}.output1D', f'{cond}.colorIfFalse.colorIfFalseR')
        pm.connectAttr(f'{sub}.output1D', f'{cond}.firstTerm')
        pm.connectAttr(f'{cond}.outColor.outColorR', f'{cond_02}.firstTerm')
        pm.connectAttr(f'{cond}.outColor.outColorR', f'{cond_02}.colorIfFalse.colorIfFalseR')

        pm.connectAttr(f'{cond_02}.outColor.outColorR', f'{align_grp}.scale.scaleY')
        pm.connectAttr(f'{cond_02}.outColor.outColorR', f'{align_grp}.scale.scaleZ')

        # GET VALUES FOR STATIC ATTRS
        if align_grp == align_grps[0]:
            pm.setAttr(f'{remap_01}.inputMin', 0)
            pm.setAttr(f'{remap_01}.outputMax', 2)
            pm.setAttr(f'{remap_02}.outputMax', 1)

        else:
            prev_align = pm.pickWalk(align_grp, d='left')
            remap_01_input_min = pm.getAttr(f'{prev_align[0]}_shoot_rm_value_01.inputMax') - 0.50

            remap_01_input_max = remap_01_input_min + val
            remap_02_input_min = remap_01_input_max + 0.01
            remap_02_input_max = remap_02_input_min + (val - 0.01)

            # SET STATIC ATTRS
            pm.setAttr(f'{remap_01}.inputMax', remap_01_input_max)
            pm.setAttr(f'{remap_01}.inputMin', remap_01_input_min)
            pm.setAttr(f'{remap_01}.outputMin', 1)
            pm.setAttr(f'{remap_01}.outputMax', 3)

            pm.setAttr(f'{remap_02}.inputMax', remap_02_input_max)
            pm.setAttr(f'{remap_02}.inputMin', remap_02_input_min)
            pm.setAttr(f'{remap_02}.outputMax', 2)

        pm.setAttr(f'{sub}.operation', 2)
        pm.setAttr(f'{cond}.operation', 2)
        pm.setAttr(f'{cond_02}.operation', 4)
        pm.setAttr(f'{cond}.secondTerm', 1)
        pm.setAttr(f'{cond_02}.secondTerm', 1)
        pm.setAttr(f'{cond_02}.colorIfTrueR', 1.00)


    return_dictionary = {}
    return_dictionary['remap_nodes'] = remap_nodes
    return_dictionary['subtract_nodes'] = subtract_nodes
    return_dictionary['multiply_nodes'] = multiply_nodes
    return_dictionary['condition_nodes'] = condition_nodes
    return return_dictionary


def retract_chain(joints,
                  leaves,
                  val,
                  start_flag,
                  start_xform):

    """

    :param pm.nt.Joint joints: Joints in chain
    :param pm.nt.Joint leaves: Leaf joints which work with chain
    :param float val: Value at which action is completed per joint
    :param pm.nt.Transform start_flag: Start control flag of spline chain (or object with extra controls)
    :param pm.nt.Transform start_xform: Start flag group to move back with chain
    :return: Returns dictionary of built nodes
    :rtype: dictionary
    """
    translate_nodes = []
    scale_nodes = []
    addition_nodes = []
    for x, joint in enumerate(joints):
        start_flag = pm.PyNode(start_flag)
        joint = pm.PyNode(joint)

        remap = pm.createNode('remapValue', n=f'{joint}_remap_retract')
        add = pm.createNode('plusMinusAverage', n=f'{joint}_add_retract')

        translate_nodes.append(remap)
        addition_nodes.append(add)

        output_value = pm.getAttr(f'{joint}.translateX') * -1
        pm.setAttr(f'{remap}.outputMax', output_value)

        if joint == joints[0]:
            remap_input_min = 0.00
        else:
            prev_joint = pm.pickWalk(joint, d='up')
            remap_input_min = pm.getAttr(f'{prev_joint[0]}_remap_retract.inputMax')

        add_1d_1_value = pm.getAttr(f'{joint}.translateX')
        remap_input_max = remap_input_min + val
        pm.setAttr(f'{remap}.outputMax', -12.755)
        pm.setAttr(f'{remap}.inputMax', remap_input_max)
        pm.setAttr(f'{remap}.inputMin', remap_input_min)
        pm.setAttr(f'{add}.input1D[1]', add_1d_1_value)

        pm.connectAttr(f'{start_flag}.Retract', f'{remap}.inputValue')
        pm.connectAttr(f'{remap}.outValue', f'{add}.input1D[0]')
        pm.connectAttr(f'{add}.output1D', f'{joint}.translateX')

        scale_remap = pm.createNode('remapValue', n=f'{joint}_scale_remap')
        scale_nodes.append(scale_remap)

        if joint == joints[0]:
            pm.setAttr(f'{scale_remap}.inputMin', 2.00)
            pm.setAttr(f'{scale_remap}.inputMax', 3.00)
            pm.connectAttr(f'{start_flag}.Retract', f'{scale_remap}.inputValue')
        else:
            pm.setAttr(f'{scale_remap}.inputMin', 3.00)
            pm.setAttr(f'{scale_remap}.inputMax', 0.01)

        if joint == joints[-1]:
            pm.connectAttr(f'{add}.output1D', f'{scale_remap}.inputValue')
        else:
            pass

        pm.setAttr(f'{scale_remap}.outputMin', 1.00)
        pm.setAttr(f'{scale_remap}.outputMax', 0.01)

        pm.connectAttr(f'{scale_remap}.outValue', f'{leaves[x]}.scale.scaleY')
        pm.connectAttr(f'{scale_remap}.outValue', f'{leaves[x]}.scale.scaleZ')

    # CONNECT TO NEXT ADDITION NODE INSTEAD OF OWN SO SCALING DOES NOT OCCUR WHEN STILL VISIBLE
    for x, node in enumerate(scale_nodes[1:-1]):
        add_nodes = addition_nodes[1:]
        next_node = add_nodes[x+1]
        pm.connectAttr(f'{next_node}.output1D', f'{node}.inputValue')

    # RETRACT ON START FLAG ALIGN TRANSFORM
    start_jnt_remap_ty = pm.createNode('remapValue', n=f'{start_xform}_retract_remap')
    pm.connectAttr(f'{start_flag}.Retract', f'{start_jnt_remap_ty}.inputValue')
    pm.setAttr(f'{start_jnt_remap_ty}.inputMin', 0.00)
    pm.setAttr(f'{start_jnt_remap_ty}.inputMax', 6.00)
    pm.setAttr(f'{start_jnt_remap_ty}.outputMin', 102.682)
    pm.setAttr(f'{start_jnt_remap_ty}.outputMax', 105.441)

    start_jnt_remap_tz = pm.createNode('remapValue', n=f'{start_xform}_retract_remap')
    pm.connectAttr(f'{start_flag}.Retract', f'{start_jnt_remap_tz}.inputValue')
    pm.setAttr(f'{start_jnt_remap_tz}.inputMin', 0.00)
    pm.setAttr(f'{start_jnt_remap_tz}.inputMax', 6.00)
    pm.setAttr(f'{start_jnt_remap_tz}.outputMin', 92.204)
    pm.setAttr(f'{start_jnt_remap_tz}.outputMax', 84.527)

    pm.connectAttr(f'{start_jnt_remap_ty}.outValue', f'{start_xform}.translateY')
    pm.connectAttr(f'{start_jnt_remap_tz}.outValue', f'{start_xform}.translateZ')

    return_dictionary = {}
    return_dictionary['translate_nodes'] = translate_nodes
    return_dictionary['addition_nodes'] = addition_nodes
    return_dictionary['scale_nodes'] = scale_nodes

    return return_dictionary

def mouth_closure(joint, start_flag):

    """

    :param str joint: Joint which controls mouth closure
    :param pm.nt.Transform start_flag: Start control flag of spline chain (or object with extra controls)
    :return: Returns remap node
    :rtype: nt.RemapValue
    """

    joint = pm.PyNode(joint)
    mouth_remap = pm.createNode('remapValue', n=f'{joint}_remap')

    pm.setAttr(f'{mouth_remap}.inputMax', -10.00)
    pm.setAttr(f'{mouth_remap}.inputMin', 10.00)
    pm.setAttr(f'{mouth_remap}.outputMin', 0.40)
    pm.setAttr(f'{mouth_remap}.outputMax', 1.50)

    pm.connectAttr(f'{start_flag}.Close', f'{mouth_remap}.inputValue')
    pm.connectAttr(f'{mouth_remap}.outValue', f'{joint}.scale.scaleY')
    pm.connectAttr(f'{mouth_remap}.outValue', f'{joint}.scale.scaleZ')

    return mouth_remap



