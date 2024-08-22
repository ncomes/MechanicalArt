#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that represents the basis for a new reverse foot rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import joint_utils, flags
from mca.mya.utils import attr_utils, dag_utils, constraint_utils

from mca.mya.rigging.frag.build import reverse_foot
from mca.mya.rigging.frag.components import frag_rig, ikfk_component

from mca.common import log
logger = log.MCA_LOGGER

class ReverseFootComponent(ikfk_component.IKFKComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, lock_axis=None, ankle_as_primary=True, **kwargs):
        """
        Creates a new ReverseFoot component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: TemplateComponent
        """
        # Initialize our FRAGNode
        frag_rig_node = super().create(frag_rig, start_joint, end_joint, scale, alignment_node, lock_axis, **kwargs)
        if not frag_rig_node:
            return

        # Save kwargs to node attrs we'll use these for serializing.
        kwargs_dict = {}
        kwargs_dict['lock_axis'] = lock_axis
        kwargs_dict['ankle_as_primary'] = ankle_as_primary
        attr_utils.set_compound_attribute_groups(frag_rig_node.pynode, 'buildKwargs', kwargs_dict)

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = frag_rig_node.joints

        ik_flag = flags.Flag(frag_rig_node.pynode.ik_flag.get())
        ik_joint_chain = frag_rig_node.pynode.ik_chain.get()
        ik_handle = frag_rig_node.pynode.ik_handle.get()

        if not ankle_as_primary:
            ik_constraint = frag_rig_node.pynode.ik_constraint.get()
            pm.delete(ik_constraint)
            ik_align_transform = ik_flag.alignTransform.get()
            pm.delete(constraint_utils.point_constraint_safe(ik_joint_chain[3], ik_align_transform))
            constraint_utils.parent_constraint_safe(ik_flag, ik_align_transform, w=True, mo=True)

        reverse_foot_results = reverse_foot.build_reverse_foot(*bind_chain[-2:], ik_flag, scale)
        #reverse_node = frag_rig_node.pynode.reverse_node.get()
        reverse_foot_chain = reverse_foot_results.get('reverse_chain')
        reverse_foot_grp = reverse_foot_results.get('reverse_foot_grp')
        pm.parent([reverse_foot_chain[0], reverse_foot_grp], dnt_group)
    
        ik_handle.setParent(reverse_foot_chain[0])
        # Toe flag should be the only new flag in this system.
        ik_ball_flag = reverse_foot_results.get('ik_ball_flag')
        ik_ball_flag.align_group.setParent(flags_group)

        pm.delete(ik_joint_chain[-1].getChildren(type=pm.nt.Constraint))
        constraint_utils.orient_constraint_safe(ik_ball_flag.pynode, ik_joint_chain[-1])

        #fk_joint_chain = frag_rig_node.pynode.fk_chain.get()
        #pm.delete(bind_chain[-1].getChildren(type=pm.nt.Constraint))
        #bind_constraint = constraint_utils.parent_constraint_safe([fk_joint_chain[-1], reverse_foot_chain[-1]], bind_chain[-1])
        #reverse_node.straight >> bind_constraint.getWeightAliasList()[1]
        #reverse_node.inverse >> bind_constraint.getWeightAliasList()[0]        

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes([ik_ball_flag], 'flags', 'fragParent', merge_values=True)

        frag_rig_node.connect_nodes(reverse_foot_chain, 'rev_chain', 'fragParent')
        frag_rig_node.connect_node(reverse_foot_grp, 'rev_group', 'fragParent')
        frag_rig_node.connect_node(reverse_foot_results.get('clamp'), 'rev_clamp', 'fragParent')

        frag_rig_node.connect_nodes(reverse_foot_results.get('unit_conv_nodes'), 'unit_conv_nodes', 'fragParent', merge_values=True)

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        skel_hierarchy, return_list = super().attach_to_skeleton(root_joint, skel_hierarchy, *args, **kwargs)

        # The only missing flag at this point should be the IK toe.
        ik_ball_flag = self.flags[-1]
        ball_joint = skel_hierarchy.get_chain_end(self.side, self.region)
        return_list.append(constraint_utils.parent_constraint_safe(ball_joint, ik_ball_flag.pynode))
        return skel_hierarchy, return_list
