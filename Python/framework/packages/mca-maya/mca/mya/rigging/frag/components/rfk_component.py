#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that represents the basis for a new rfk rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils

from mca.mya.rigging.frag.build import rfk_chain
from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class RFKComponent(frag_rig.FRAGAnimatedComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, **kwargs):
        """
        Creates a new RFK component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: TemplateComponent
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

        frag_rig_node = super().create(frag_rig, rig_side, rig_region, alignment_node, **kwargs)

        # Save kwargs to node attrs we'll use these for serializing.
        # None here.

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()
        align_node = alignment_node or start_joint
        pm.delete(pm.pointConstraint(align_node, flags_group))
        pm.delete(pm.pointConstraint(align_node, dnt_group))

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = dag_utils.get_between_nodes(start_joint, end_joint)
        rfk_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='rfk')
        rfk_joint_chain[0].setParent(dnt_group)

        rfk_results = rfk_chain.build_rfk_chain(rfk_joint_chain, scale)
        mid_groups = rfk_results.get('mid_groups')
        pm.parent(mid_groups, dnt_group)

        flag_list = rfk_results.get('flags')
        for flag_node in flag_list:
            flag_node.align_group.setParent(flags_group)

        for bind_joint_node, rfk_joint_node in zip(bind_chain, rfk_joint_chain):
            constraint_utils.parent_constraint_safe(rfk_joint_node, bind_joint_node)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        # NOTE during the attach portion it'll skip the sub flags because they are a longer lister than the bind chain
        frag_rig_node.connect_nodes(rfk_results.get('flags') + rfk_results.get('sub_flags'), 'flags', 'fragParent')

        frag_rig_node.connect_nodes(flag_list[1:-1], 'mid_flags')
        frag_rig_node.connect_nodes(rfk_results.get('sub_flags'), 'sub_flags')
        frag_rig_node.connect_nodes(rfk_joint_chain, 'rfk_chain', 'fragParent')
        frag_rig_node.connect_node(flag_list[0], 'start_flag')
        frag_rig_node.connect_node(flag_list[-1], 'end_flag')
        frag_rig_node.connect_nodes(mid_groups, 'mid_groups', 'fragParent')
        frag_rig_node.connect_nodes(rfk_results.get('mid_offset_groups'), 'mid_offset_groups', 'fragParent')
        frag_rig_node.connect_nodes(rfk_results.get('reverse_nodes'), 'reverse_nodes', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return None, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        bind_chain = skel_hierarchy.get_full_chain(self.side, self.region)
        return_list = []
        for bind_joint, frag_flag in zip(bind_chain, self.flags):
            flag_pynode = frag_flag.pynode
            # $Hack when using the parent constraint safe here we are unable to set keys on the component.
            return_list.append(constraint_utils.orient_constraint_safe(bind_joint, flag_pynode))
            for attr_name in attr_utils.SCALE_ATTRS:
                if flag_pynode.attr(attr_name).isSettable():
                    flag_pynode.attr(attr_name) >> flag_pynode.attr(attr_name)
        return skel_hierarchy, return_list