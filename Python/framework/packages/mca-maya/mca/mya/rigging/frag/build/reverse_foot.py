#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to building a reverse foot.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import flags, joint_utils
from mca.mya.utils import attr_utils, constraint_utils, dag_utils, naming

from mca.common import log
logger = log.MCA_LOGGER

def build_reverse_foot(ankle_joint, ball_joint, ik_flag, scale=None):
    """
    Builds a reverse foot rig.

    NOTE: These are the live skel joints not duplicates.
    :param Joint ankle_joint:
    :param Joint ball_joint:
    :return: A dictionary containing build objects.
    :rtype: dict
    """
    scale = scale or 1.0

    ik_flag_pynode = ik_flag.pynode

    wrapped_joint = joint_utils.JointMarkup(ankle_joint)

    # Ball life rotate axis
    # $HACK there is probably a better way to determine this.
    temp_loc = pm.spaceLocator()
    ball_pos = pm.xform(ball_joint, ws=True, q=True, t=True)
    temp_loc.t.set([0]+ball_pos[1:])
    temp_loc.setParent(ball_joint)
    
    primary_axis, _ = dag_utils.get_primary_axis(temp_loc)
    pm.delete(temp_loc)

    # Find our contacts
    skel_hierarchy = joint_utils.SkeletonHierarchy(ankle_joint)

    toe_null_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, f'{wrapped_joint.region}_toe_null') # -z
    ball_null_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, f'{wrapped_joint.region}_ball_null') # z up/down y left/right
    heel_null_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, f'{wrapped_joint.region}_heel_null') # +z
    exterior_null_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, f'{wrapped_joint.region}_outer_rock_null') # -x
    interior_null_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, f'{wrapped_joint.region}_inner_rock_null') # +x
    if not all([toe_null_joint, ball_null_joint, heel_null_joint, exterior_null_joint, interior_null_joint]):
        logger.error('Missing contact joint aborting build')
        return {}

    # IK Toe flag
    ik_ball_flag = flags.Flag.create(f'{wrapped_joint.side}_{wrapped_joint.region}_toe_ik', ball_joint, scale, flag_path='rotation')
    ik_ball_flag.side = wrapped_joint.side
    ik_ball_flag.region = wrapped_joint.region
    ik_flag_pynode.v >> ik_ball_flag.pynode.v
    ik_ball_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)

    # Duplicate the base chain.
    rev_ankle_joint, rev_ball_joint, *_ = joint_utils.duplicate_chain(ankle_joint, ball_joint, suffix='rvc')

    # Contact joints and primary alignment group
    contact_alignment_grp = pm.group(em=True, w=True, n=f'{wrapped_joint.side}_{wrapped_joint.region}_contract_align_grp')
    toe_pivot_joint = joint_utils.duplicate_joint(toe_null_joint, duplicate_name=f'{naming.get_basename(toe_null_joint)}_piv')
    pm.delete(constraint_utils.parent_constraint_safe(toe_pivot_joint, contact_alignment_grp))
    toe_pivot_joint.setParent(contact_alignment_grp)
    toe_contact_joint = joint_utils.duplicate_joint(toe_null_joint, duplicate_name=f'{naming.get_basename(toe_null_joint)}_cnt')
    toe_contact_joint.setParent(toe_pivot_joint)
    ball_pivot_joint = joint_utils.duplicate_joint(ball_null_joint, duplicate_name=f'{naming.get_basename(ball_null_joint)}_piv')
    ball_pivot_joint.setParent(toe_contact_joint)
    ext_contact_joint = joint_utils.duplicate_joint(exterior_null_joint, duplicate_name=f'{naming.get_basename(exterior_null_joint)}_cnt')
    ext_contact_joint.setParent(ball_pivot_joint)
    int_contact_joint = joint_utils.duplicate_joint(interior_null_joint, duplicate_name=f'{naming.get_basename(interior_null_joint)}_cnt')
    int_contact_joint.setParent(ext_contact_joint)
    heel_contact_joint = joint_utils.duplicate_joint(heel_null_joint, duplicate_name=f'{naming.get_basename(heel_null_joint)}_cnt')
    heel_contact_joint.setParent(int_contact_joint)

    # Rev chain
    foot_rev_joint = joint_utils.duplicate_joint(ankle_joint, duplicate_name=f'{naming.get_basename(ankle_joint)}_rev')
    ball_rev_joint = joint_utils.duplicate_joint(ball_joint, duplicate_name=f'{naming.get_basename(ball_joint)}_rev')
    ball_can_joint = joint_utils.duplicate_joint(ball_joint, duplicate_name=f'{naming.get_basename(ball_joint)}_can')
    ball_rev_joint.setParent(heel_contact_joint)
    ball_can_joint.setParent(heel_contact_joint)
    foot_rev_joint.setParent(ball_rev_joint)

    pm.makeIdentity(pm.listRelatives(contact_alignment_grp, ad=True), t=True, r=True, s=True, n=False, pn=True, apply=True)

    # Constraints
    constraint_utils.parent_constraint_safe(foot_rev_joint, rev_ankle_joint, mo=True)
    constraint_utils.parent_constraint_safe(ball_can_joint, rev_ball_joint, mo=True)
    constraint_utils.orient_constraint_safe(rev_ankle_joint, ankle_joint, mo=True)
    constraint_utils.orient_constraint_safe(rev_ball_joint, ball_joint, mo=True)

    alignment_constraint = constraint_utils.parent_constraint_safe(ik_flag_pynode, contact_alignment_grp, mo=True)
    constraint_utils.parent_constraint_safe(heel_contact_joint, ik_ball_flag.align_group, mo=True)
    constraint_utils.parent_constraint_safe(ik_ball_flag.pynode, ball_can_joint)

    # add the reverse foot control attributes
    ik_flag_pynode.addAttr('_______', k=True, at='bool')
    ik_flag_pynode.setAttr('_______', e=True, cb=True, l=True)
    ik_flag_pynode.addAttr('ballLift', k=True, at='double')
    # Skeleton orientation matters here, the rest of the joints are null joints and should be fixed orientation.
    ik_flag_pynode.ballLift >> ball_rev_joint.attr(f'r{primary_axis}'.lower())
    ik_flag_pynode.addAttr('ballPivot', k=True, at='double')
    ik_flag_pynode.ballPivot >> ball_pivot_joint.attr(f'ry')
    ik_flag_pynode.addAttr('toeLift', k=True, at='double')
    ik_flag_pynode.toeLift >> toe_contact_joint.attr(f'rz')
    ik_flag_pynode.addAttr('toePivot', k=True, at='double')
    ik_flag_pynode.toePivot >> toe_pivot_joint.attr(f'ry')
    ik_flag_pynode.addAttr('heelLift', k=True, at='double')
    ik_flag_pynode.heelLift >> heel_contact_joint.attr(f'rz')
    ik_flag_pynode.addAttr('footLean', k=True, at='double')
    clamp_ext = pm.createNode(pm.nt.Clamp, n=f'{wrapped_joint.side}_{wrapped_joint.region}_roll_clamp')
    clamp_ext.minR.set(-180)
    clamp_ext.maxG.set(180)
    ik_flag_pynode.footLean >> clamp_ext.inputR
    ik_flag_pynode.footLean >> clamp_ext.inputG
    clamp_ext.outputR >> ext_contact_joint.attr(f'rx')
    clamp_ext.outputG >> int_contact_joint.attr(f'rx')
    unit_conv_nodes = [x for x in clamp_ext.listConnections() if isinstance(x, pm.nt.UnitConversion)]

    # create dictionary
    return_dictionary = {}
    return_dictionary['reverse_contact_joints'] = [heel_contact_joint, int_contact_joint, ext_contact_joint, ball_pivot_joint, toe_contact_joint, toe_pivot_joint]
    return_dictionary['reverse_chain'] = [rev_ankle_joint, rev_ball_joint]
    return_dictionary['reverse_foot_grp'] = contact_alignment_grp
    return_dictionary['ik_ball_flag'] = ik_ball_flag
    return_dictionary['alignment_constraint'] = alignment_constraint

    return_dictionary['clamp'] = clamp_ext
    return_dictionary['unit_conv_nodes'] = unit_conv_nodes
    return return_dictionary