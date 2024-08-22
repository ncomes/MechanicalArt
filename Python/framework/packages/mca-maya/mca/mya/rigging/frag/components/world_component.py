#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the world rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import flags, joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils, naming

from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class WorldComponent(frag_rig.FRAGAnimatedComponentSingle):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, scale=None, alignment_node=None, **kwargs):
        """
        Creates a new World component on the provided chain of joints from start to end.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given hierarchy.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: WorldComponent
        """
        # Initialize our FRAGNode
        if not start_joint:
            logger.error('No root joint provided will abort build')
            return

        frag_rig_node = super().create(frag_rig, 'center', 'root', alignment_node, **kwargs)

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

        world_root = joint_utils.duplicate_joint(start_joint, naming.get_basename(f'{start_joint}_world'))
        world_root.setParent(dnt_group)

        world_flag = flags.Flag.create('f_world', start_joint, scale, flag_path='root')
        world_flag.align_group.setParent(flags_group)
        offset_flag = flags.Flag.create('f_world_offset', start_joint, scale*.85, flag_path='root')
        offset_flag.align_group.setParent(world_flag.pynode)
        offset_flag.detail = True
        root_flag = flags.Flag.create('f_root', start_joint, scale*.65, flag_path='root')
        root_flag.align_group.setParent(world_flag.pynode)
        root_flag.sub = True

        for flag in [world_flag, offset_flag, root_flag]:
            flag.side = 'center'
            flag.region = 'root'

        flag_list = [world_flag, offset_flag, root_flag]

        for flag_node in flag_list:
            flag_node.set_attr_state(True, attr_utils.SCALE_ATTRS)

        constraint_utils.parent_constraint_safe(root_flag.pynode, world_root)
        constraint_utils.parent_constraint_safe(world_root, start_joint)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes([start_joint], 'joints')
        frag_rig_node.connect_nodes(flag_list, 'flags', 'fragParent')

        frag_rig_node.connect_nodes([world_root], 'world_chain', 'fragParent')
        frag_rig_node.connect_node(world_flag, 'world_flag', 'fragParent')
        frag_rig_node.connect_node(root_flag, 'root_flag', 'fragParent')
        frag_rig_node.connect_node(offset_flag, 'offset_flag', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, start_joint, skel_hierarchy=None, *args, **kwargs):
        if not start_joint:
            return None, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(start_joint)

        start_joint = skel_hierarchy.get_chain_start(self.side, self.region)
        # Root joint drives the world flag.
        # If the root joint needs to follow along switch the space of the root.
        # If the whole system needs to be offset, adjust the offset root.
        return_list = [constraint_utils.parent_constraint_safe(start_joint, self.pynode.world_flag.get())]
        return skel_hierarchy, return_list
        