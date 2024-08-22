#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that represents the basis for a new Piston rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.utils import list_utils

from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils, naming

from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class PistonComponent(frag_rig.FRAGComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, **kwargs):
        """
        Creates a new Piston component on the provided pair of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :return: The newly created frag node.
        :rtype: PistonComponent
        """
        # Initialize our FRAGNode
        if not start_joint:
            logger.error('No start joint provided will abort build')
            return

        wrapped_joint = joint_utils.JointMarkup(start_joint)
        rig_side = wrapped_joint.side
        rig_region = wrapped_joint.region

        if not rig_side or not rig_region:
            logger.error('Missing joint markup and will abort build.')
            return

        frag_rig_node = super().create(frag_rig, rig_side, rig_region, **kwargs)

        # Save kwargs to node attrs we'll use these for serializing.
        # None here.

        # Get our organization groups
        dnt_group = frag_rig_node.add_do_not_touch_group()

        # Start building shiet.
        bind_chain = [start_joint, end_joint]

        dup_joint_list = []
        align_grp_list = []
        constraint_list = []
        for joint_node in bind_chain:
            dup_joint = joint_utils.duplicate_joint(joint_node, naming.get_basename(joint_node)+'_pst')
            dup_joint_list.append(dup_joint)
            dup_align = dag_utils.create_aligned_parent_group(dup_joint)
            align_grp_list.append(dup_align)
            dup_align.setParent(dnt_group)
            pm.parentConstraint(joint_node.getParent(), dup_align, mo=True)
            constraint_list.append(constraint_utils.parent_constraint_safe(dup_joint, joint_node))
            

        temp_loc = pm.spaceLocator()
        aim_constraint_list = []
        for joint_node, dup_joint, dup_align in zip(bind_chain, dup_joint_list, align_grp_list):
            # We want to align our temp loc to the other joint.
            opposite_joint = list_utils.get_first_in_list([x for x in dup_joint_list if x is not dup_joint])
            pm.delete(pm.pointConstraint(opposite_joint, temp_loc))
            temp_loc.setParent(dup_joint)
            primary_axis, axis_is_positive = dag_utils.get_primary_axis(dup_joint)
            lookat_loc = pm.spaceLocator(n=naming.get_basename(dup_joint)+'_loc')
            lookat_loc.setParent(dup_align)
            pm.delete(pm.parentConstraint(dup_joint, lookat_loc))
            lookat_axis_index = 'xyz'.index(primary_axis.lower())+1 % 3
            axis_value = 1.0 if axis_is_positive else -1.0
            lookat_axis = [axis_value if primary_axis.lower() == x else 0.0 for x in 'xyz']
            lookat_object_axis = [1.0 if i == lookat_axis_index else 0.0 for i in range(3)]
            lookat_loc.attr(f"t{'xyz'[lookat_axis_index]}").set(.5)
            aim_constraint_list.append(pm.aimConstraint(opposite_joint, dup_joint, mo=True, aim=lookat_axis, wuo=lookat_loc, u=lookat_object_axis))
            aim_constraint_list[-1].worldUpType.set(1)
        pm.delete(temp_loc)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes(dup_joint_list, 'pst_joints')
        frag_rig_node.connect_nodes(align_grp_list, 'align_groups')

        frag_rig_node.connect_nodes(aim_constraint_list, 'aim_constraints')
        frag_rig_node.connect_nodes(constraint_list, 'parent_constraints')

        return frag_rig_node