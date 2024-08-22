#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the pelvis rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils
from mca.mya.rigging import flags

from mca.mya.rigging.frag.build import fk_chain
from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class PelvisComponent(frag_rig.FRAGAnimatedComponentSingle):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, **kwargs):
        """
        Creates a new World component on the provided chain of joints from start to end.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: WorldComponent
        """
        # Initialize our FRAGNode
        if not start_joint:
            logger.error('No root joint provided will abort build')
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

        bind_chain = dag_utils.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Should always come in as pelvis, spine01, end of pelvis is start of spine.
        # We're going to duplicate the chain then reverse the order. We'll drive the pelvis from spine 1's position.
        fk_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, 'plv')
        rev_joint_chain = joint_utils.reverse_joint_chain(fk_joint_chain)
        rev_joint_chain[0].setParent(dnt_group)

        pelvis_flag = flags.Flag.create('f_pelvis', rev_joint_chain[0], scale)
        pelvis_flag.side = wrapped_joint.side
        pelvis_flag.region = wrapped_joint.region
        pelvis_flag.align_group.setParent(flags_group)
        pelvis_flag.set_attr_state(attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)

        constraint_utils.parent_constraint_safe(pelvis_flag.pynode, rev_joint_chain[-1], mo=True)
        constraint_utils.parent_constraint_safe(rev_joint_chain[-1], start_joint, mo=True)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes([pelvis_flag], 'flags', 'fragParent')

        frag_rig_node.connect_nodes(rev_joint_chain, 'rev_chain', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return None, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        bind_chain = skel_hierarchy.get_full_chain(self.side, self.region)
        return_list = []
        if bind_chain and len(bind_chain) == 2:
            rev_loc = pm.spaceLocator()
            return_list.append(rev_loc)
            # Align the locator to the second joint (spine1)
            pm.delete(pm.parentConstraint(bind_chain[-1], rev_loc))
            # Constrain our locator to the actual pelvis as it moves. This should mimic our reverse joint behavior.
            return_list.append(pm.parentConstraint(bind_chain[0], rev_loc, mo=True))
            return_list.append(constraint_utils.parent_constraint_safe(rev_loc, self.flags[0].pynode, mo=True))
        return skel_hierarchy, return_list
