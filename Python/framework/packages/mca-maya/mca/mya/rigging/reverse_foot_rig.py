#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an ik chain
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.utils import constraint, naming
from mca.mya.rigging import joint_utils
from mca.mya.rigging.flags import tek_flag


def reverse_foot_chain(start_joint,
                        end_joint,
                        side,
                        region,
                        scale=1.0,
                        contact_joints = None,
                        ik_foot_flag=None,
                        ball_lift_axis='z',
                        toe_lift_axis='z',
                        toe_pivot_axis='y',
                        heel_lift_axis='z',
                        foot_lean_axis='x',
                        ball_pivot_axis='y'):

        """
        Builds a reverse foot rig.

        toe_null, ball_null, heel_null exterior_null, interior_null

        toe z- (lift) y rot
        ball y rot
        exterior x-
        interior x+
        heel z+

        :param pm.nt.Joint start_joint: Start joint (ex: ankle)
        :param pm.nt.Joint end_joint: End joint (ex: toe)
        :param str side: Which side the foot is on.
        :param str region: A unique name for the region.  (ex: foot)
        :param flag.Flag ik_foot_flag: If there is an existing ik Flag.
        :param str ball_lift_axis: The axis in which to pivot.
        :param str toe_lift_axis: The axis in which to pivot.
        :param str toe_tap_axis: The axis in which to pivot.
        :param str toe_pivot_axis: The axis in which to pivot.
        :param str heel_lift_axis: The axis in which to pivot.
        :param str foot_lean_axis: The axis in which to pivot.
        :param str ball_pivot_axis: The axis in which to pivot.
        :return: Returns a dictionary with all of the built nodes.
        :rtype: dictionary
        """

        if not contact_joints or None in contact_joints:
            # No contact joints
            return

        if len(contact_joints) != 5:
            # Incorrect number of contact joints
            return

        #toe pivot > toe > ball > exterior > interior > heel > toe_joint > foot_joint

        side_prefix = side[:1].lower()

        foot_joint, toe_joint, *_ = joint_utils.duplicate_chain(start_joint, end_joint, suffix='dup')
        foot_joint.v.set(False)

        if not ik_foot_flag:
            ik_foot_flag = tek_flag.Flag.create(start_joint, scale=scale, label=f'{side}_{region}', add_align_transform=True)
        ik_toe_flag = tek_flag.Flag.create(toe_joint, scale=scale, label=f'{side_prefix}_{region}_toe_ik', add_align_transform=True)
        ik_foot_flag.v >> ik_toe_flag.v
        ik_toe_flag.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])

        # Contact joints
        contact_alignment_grp = pm.group(em=True, w=True, n=f'{side}_{region}_cnt_grp')
        toe_pivot_joint = joint_utils.duplicate_joint(contact_joints[0], duplicate_name=f'{naming.get_basename(contact_joints[0])}_piv')
        pm.delete(constraint.parent_constraint_safe(toe_pivot_joint, contact_alignment_grp))
        toe_pivot_joint.setParent(contact_alignment_grp)
        toe_contact_joint = joint_utils.duplicate_joint(contact_joints[0], duplicate_name=f'{naming.get_basename(contact_joints[0])}_cnt')
        toe_contact_joint.setParent(toe_pivot_joint)
        ball_pivot_joint = joint_utils.duplicate_joint(contact_joints[1], duplicate_name=f'{naming.get_basename(contact_joints[1])}_piv')
        ball_pivot_joint.setParent(toe_contact_joint)
        ext_contact_joint = joint_utils.duplicate_joint(contact_joints[2], duplicate_name=f'{naming.get_basename(contact_joints[2])}_cnt')
        ext_contact_joint.setParent(ball_pivot_joint)
        int_contact_joint = joint_utils.duplicate_joint(contact_joints[3], duplicate_name=f'{naming.get_basename(contact_joints[3])}_cnt')
        int_contact_joint.setParent(ext_contact_joint)
        heel_contact_joint = joint_utils.duplicate_joint(contact_joints[4], duplicate_name=f'{naming.get_basename(contact_joints[4])}_cnt')
        heel_contact_joint.setParent(int_contact_joint)


        # Rev chain
        foot_rev_joint = joint_utils.duplicate_joint(foot_joint, duplicate_name=f'{naming.get_basename(foot_joint)}_rev')
        ball_rev_joint = joint_utils.duplicate_joint(toe_joint, duplicate_name=f'{naming.get_basename(toe_joint)}_rev')
        ball_can_joint = joint_utils.duplicate_joint(toe_joint, duplicate_name=f'{naming.get_basename(toe_joint)}_can')
        ball_rev_joint.setParent(heel_contact_joint)
        ball_can_joint.setParent(heel_contact_joint)
        foot_rev_joint.setParent(ball_rev_joint)

        pm.makeIdentity(pm.listRelatives(contact_alignment_grp, ad=True), t=True, r=True, s=True, n=False, pn=True, apply=True)

        # Constraints
        constraint.parent_constraint_safe(foot_rev_joint, foot_joint, mo=True)
        constraint.parent_constraint_safe(ball_can_joint, toe_joint, mo=True)
        constraint.orient_constraint_safe(foot_joint, start_joint, mo=True)
        constraint.orient_constraint_safe(toe_joint, end_joint, mo=True)

        alignment_constraint = constraint.parent_constraint_safe(ik_foot_flag, contact_alignment_grp, mo=True)
        constraint.parent_constraint_safe(heel_contact_joint, ik_toe_flag.alignTransform.get(), mo=True)
        constraint.parent_constraint_safe(ik_toe_flag, ball_can_joint)

        # add the reverse foot control attributes
        ik_foot_flag.addAttr('_______', k=True, at='bool')
        ik_foot_flag.setAttr('_______', e=True, cb=True, l=True)
        ik_foot_flag.addAttr('ballLift', k=True, at='double')
        ik_foot_flag.ballLift >> ball_rev_joint.attr(f'r{ball_lift_axis}')
        ik_foot_flag.addAttr('ballPivot', k=True, at='double')
        ik_foot_flag.ballPivot >> ball_pivot_joint.attr(f'r{ball_pivot_axis}')
        ik_foot_flag.addAttr('toeLift', k=True, at='double')
        ik_foot_flag.toeLift >> toe_contact_joint.attr(f'r{toe_lift_axis}')
        ik_foot_flag.addAttr('toePivot', k=True, at='double')
        ik_foot_flag.toePivot >> toe_pivot_joint.attr(f'r{toe_pivot_axis}')
        ik_foot_flag.addAttr('heelLift', k=True, at='double')
        ik_foot_flag.heelLift >> heel_contact_joint.attr(f'r{heel_lift_axis}')
        ik_foot_flag.addAttr('footLean', k=True, at='double')
        clamp_ext = pm.createNode(pm.nt.Clamp, n=f'{side_prefix}_{region}_roll_clamp')
        clamp_ext.minR.set(-180)
        clamp_ext.maxG.set(180)
        ik_foot_flag.footLean >> clamp_ext.inputR
        ik_foot_flag.footLean >> clamp_ext.inputG
        clamp_ext.outputR >> ext_contact_joint.attr(f'r{foot_lean_axis}')
        clamp_ext.outputG >> int_contact_joint.attr(f'r{foot_lean_axis}')
        unit_conv_nodes = [x for x in clamp_ext.listConnections() if isinstance(x, pm.nt.UnitConversion)]

        # create dictionary
        return_dictionary = dict()
        return_dictionary['chain'] = [foot_joint, toe_joint]
        return_dictionary['start_joint'] = start_joint
        return_dictionary['end_joint'] = end_joint
        return_dictionary['reverse_contact_joints'] = [heel_contact_joint, int_contact_joint, ext_contact_joint, ball_pivot_joint, toe_contact_joint, toe_pivot_joint]
        return_dictionary['reverse_chain'] = [foot_rev_joint, ball_rev_joint]
        return_dictionary['reverse_foot_grp'] = contact_alignment_grp
        return_dictionary['ik_toe_flag'] = ik_toe_flag
        return_dictionary['alignment_constraint'] = alignment_constraint
        return_dictionary['clamp'] = clamp_ext
        return_dictionary['unit_conv_nodes'] = unit_conv_nodes

        return return_dictionary

