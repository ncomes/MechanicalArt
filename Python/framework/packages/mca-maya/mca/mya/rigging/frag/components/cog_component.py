#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the cog rig component.
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

class CogComponent(frag_rig.FRAGAnimatedComponentSingle):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, scale=None, alignment_node=None, **kwargs):
        """
        Creates a new World component on the provided chain of joints from start to end.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: WorldComponent
        """
        # Initialize our FRAGNode
        if not start_joint:
            logger.error('No root joint provided will abort build')
            return

        frag_rig_node = super().create(frag_rig, 'center', 'cog', alignment_node, **kwargs)

        # Save kwargs to node attrs we'll use these for serializing.
        # None here.

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        align_node = alignment_node or start_joint
        pm.delete(pm.pointConstraint(align_node, flags_group))

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = [start_joint]

        # Should always come in as pelvis, spine01, end of pelvis is start of spine.
        # We're going to duplicate the chain then reverse the order. We'll drive the pelvis from spine 1's position.
        cog_flag = flags.Flag.create('f_cog', start_joint, scale)
        cog_flag.side = 'center'
        cog_flag.region = 'cog'
        cog_flag.set_attr_state(attr_list=attr_utils.SCALE_ATTRS)
        new_curve = flags.import_flag('cog')

        # Unqiue logic to make sure the cog flag is always flat.
        if new_curve:
            pm.delete(pm.pointConstraint(start_joint, new_curve, w=True, mo=False))
            if scale != 1.0:
                new_curve.s.set(3*[scale])
            pm.makeIdentity(new_curve, apply=True, s=True)
            dag_utils.parent_shape_node(new_curve, cog_flag.pynode, maintain_offset=True)

        cog_flag.align_group.setParent(flags_group)
        cog_flag.set_attr_state(attr_list=attr_utils.SCALE_ATTRS)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes([cog_flag], 'flags', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return None, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        bind_chain = self.joints
        wrapped_joint = joint_utils.JointMarkup(bind_chain[0])
        pelvis_joint = skel_hierarchy.get_chain_start(wrapped_joint.side, wrapped_joint.region)
        return_list = [constraint_utils.parent_constraint_safe(pelvis_joint, self.flags[0].pynode)]
        return skel_hierarchy, return_list
