#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the IK/FK rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.utils import pymaths

from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils, flags
from mca.mya.utils import attr_utils, dag_utils, constraint_utils

from mca.mya.rigging.frag.build import fk_chain
from mca.mya.rigging.frag.components import frag_rig, ik_component

from mca.common import log
logger = log.MCA_LOGGER

class IKFKComponent(ik_component.IKComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, lock_axis=None, **kwargs):
        """
        Creates a new IKFK component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :param str lock_axis: The axis to lock on the "elbow" of the fk chain.
        :return: The newly created frag node.
        :rtype: IKFKComponent
        """
        # Start building shiet.
        scale = scale or 1.0
        wrapped_joint = joint_utils.JointMarkup(start_joint)

        frag_rig_node = super().create(frag_rig, start_joint, end_joint, scale, alignment_node, **kwargs)
        if not frag_rig_node:
            return

        lock_axis = lock_axis.lower() if lock_axis and lock_axis.lower() in 'xyz' else 'z'

        # Save kwargs to node attrs we'll use these for serializing.
        kwargs_dict = {}
        kwargs_dict['lock_axis'] = lock_axis
        attr_utils.set_compound_attribute_groups(frag_rig_node.pynode, 'buildKwargs', kwargs_dict)

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()

        # Get our original build chain.
        bind_chain = frag_rig_node.joints

        # This might be more than 3 joints, but that's okay.
        fk_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, 'fkc')
        fk_joint_chain[0].setParent(dnt_group)
        fk_results = fk_chain.build_fk_chain(fk_joint_chain, scale)
        fk_flag_list = fk_results.get('flags')

        # Clean up our FK results and parent our Flag Aligns.
        for index, new_flag in enumerate(fk_flag_list):
            if not index:
                # Parent the first alignment group to the flags group and set root locks
                new_flag.align_group.setParent(flags_group)
            if index == 1:
                # Tidy up my mid flag by locking our non broken axes
                new_flag.set_attr_state(True, attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS+[f'r{x}' for x in 'xyz' if x != lock_axis])
            else:
                new_flag.set_attr_state(True, attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)

        # Correct the shape to a ring flag.
        fk_mid_flag = fk_flag_list[1]
        if lock_axis == 'x':
            rot_offset = [0, 0, 90]
        elif lock_axis == 'y':
            rot_offset = None
        else:
            rot_offset = [90, 0, 0]
        fk_mid_flag.swap_shape('ring', scale, rot_offset)

        # Get our OG component ik flags.
        ik_flag, pv_flag = frag_rig_node.flags
        switch_align = pm.spaceLocator(n=f'ikfk_switch_align')
        switch_align.setParent(fk_joint_chain[1])
        pm.delete(pm.parentConstraint(pv_flag.pynode, switch_align))
        ik_joint_chain = frag_rig_node.pynode.ik_chain.get()

        # switch flag
        switch_flag = flags.Flag.create(f'f_{frag_rig_node.side}_{frag_rig_node.region}_ikfk_switch', bind_chain[2], scale*.5, flag_path='triangle')
        switch_flag.side = wrapped_joint.side
        switch_flag.region = wrapped_joint.region
        pt1, pt2, pt3 = [pm.xform(x, q=True, ws=True, t=True) for x in bind_chain[:3]]
        norm_xprod = pymaths.get_planar_up(pt1, pt2, pt3)
        switch_align_group = switch_flag.align_group
        switch_align_group.t.set(pymaths.add_vectors(pt3, pymaths.scale_vector(norm_xprod, 10.0+scale)))
        # NOTE: lock the switch flag attrs here before we add the switch attr.
        switch_align_group.setParent(flags_group)
        constraint_utils.parent_constraint_safe(bind_chain[2], switch_align_group, mo=True)
        switch_flag.set_attr_state()

        switch_flag.pynode.addAttr('ikfk_switch', k=True, at='double', min=0.0, max=1.0, dv=1.0)
        reverse_node = attr_utils.invert_attribute(switch_flag.pynode.ikfk_switch)

        # Set our flag visibilities.
        reverse_node.straight >> ik_flag.pynode.v
        reverse_node.straight >> pv_flag.pynode.v
        reverse_node.straight >> frag_rig_node.pynode.pv_group.get().v
        for fk_flag in fk_flag_list:
            reverse_node.inverse >> fk_flag.pynode.v

        for bind_joint, fk_joint, ik_joint in zip(bind_chain, fk_joint_chain, ik_joint_chain):
            # Remove OG IK constraints to the bind joints.
            pm.delete(bind_joint.getChildren(type=pm.nt.Constraint))

            bind_constraint = constraint_utils.parent_constraint_safe([fk_joint, ik_joint], bind_joint)
            reverse_node.straight >> bind_constraint.getWeightAliasList()[1]
            reverse_node.inverse >> bind_constraint.getWeightAliasList()[0]

        frag_rig_node.connect_nodes(fk_flag_list+[switch_flag], 'flags', 'fragParent', merge_values=True)
        frag_rig_node.connect_nodes([ik_flag, pv_flag], 'ik_flags', 'fragParent')
        frag_rig_node.connect_nodes(fk_flag_list, 'fk_flags', 'fragParent')
        frag_rig_node.connect_node(switch_align, 'switch_align', 'fragParent')
        frag_rig_node.connect_node(switch_flag, 'switch_flag', 'fragParent')

        frag_rig_node.connect_nodes(fk_joint_chain, 'fk_chain', 'fragParent')
        frag_rig_node.connect_node(reverse_node, 'reverse_node', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        skel_hierarchy, return_list = super().attach_to_skeleton(root_joint, skel_hierarchy, *args, **kwargs)

        # There will always be 2 IK flags, then a number of FK flags, the switch flag, and if there is a reverse foot a ball flag.
        # This gets complicated but it allows us to inherit each step's attach to skeleton process.
        if self.frag_type == 'ReverseFootComponent':
            fk_flag_list = self.flags[2:-2]
        else:
            fk_flag_list = self.flags[2:-1]
        bind_chain = skel_hierarchy.get_full_chain(self.side, self.region)
        for bind_joint, fk_flag in zip(bind_chain, fk_flag_list):
            return_list.append(constraint_utils.parent_constraint_safe(bind_joint, fk_flag.pynode))

        return skel_hierarchy, return_list
    
    @ma_decorators.undo_decorator
    def switch_align(self):
        flag_list = self.flags
        ik_flag, pv_flag = flag_list[:2]
        if self.frag_type == 'ReverseFootComponent':
            # We should have a toe flag and every other flag is a fk_flag
            fk_flag_list = flag_list[2:-2]
            switch_flag = flag_list[-2]
            ik_ball_flag = flag_list[-1]
        else:
            fk_flag_list = flag_list[2:-1]
            switch_flag = flag_list[-1]
            ik_ball_flag = None

        # What's the active switch type.
        return_list = []
        switch_val = switch_flag.pynode.ikfk_switch.get()
        if switch_val == 1:
            # We're in IK so match fk to IK
            # We'll get the Ik chain which is 3 joints +1 for the ball if it's there.
            ik_joint_chain = self.pynode.ik_chain.get()
            if ik_ball_flag:
                ik_joint_chain+[ik_ball_flag.pynode]
            
            for node, fk_flag in zip(ik_joint_chain, fk_flag_list):
                return_list.append(constraint_utils.parent_constraint_safe(node, fk_flag.pynode))
            switch_flag.pynode.ikfk_switch.set(0)
        elif switch_val == 0:
            # We're in FK so match IK to FK
            return_list.append(constraint_utils.parent_constraint_safe(fk_flag_list[2].pynode, ik_flag.pynode))
            return_list.append(constraint_utils.parent_constraint_safe(self.pynode.switch_align.get(), pv_flag.pynode))
            if ik_ball_flag:
                return_list.append(constraint_utils.parent_constraint_safe(fk_flag_list[-1].pynode, ik_ball_flag.pynode))
            switch_flag.pynode.ikfk_switch.set(1)
        else:
            # We're somewhere in between do nothing.
            logger.error('This IKFK component is somewhere between states and will not be switched.')
            return
        return return_list

class TwoPointIKFKComponent(ik_component.TwoPointIKComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, stretch=False, **kwargs):
        """
        Creates a new TwoPointIKFK component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :param bool stretch: If the end joint should not retain its distance from the start.
        :return: The newly created frag node.
        :rtype: TwoPointIKFKComponent
        """
        # Initialize our FRAGNode
        scale = scale or 1.0
        wrapped_joint = joint_utils.JointMarkup(start_joint)

        frag_rig_node = super().create(frag_rig, start_joint, end_joint, scale, alignment_node, stretch, **kwargs)
        if not frag_rig_node:
            return

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()

        # Get our original build chain.
        bind_chain = frag_rig_node.joints

        # Setup our Fk Chain
        fk_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, 'fkc')
        fk_joint_chain[0].setParent(dnt_group)
        fk_results = fk_chain.build_fk_chain(fk_joint_chain, scale)
        fk_flag_list = fk_results.get('flags')
        
        start_fk_flag, end_fk_flag = fk_flag_list
        start_fk_flag.align_group.setParent(flags_group)
        start_fk_flag.set_attr_state(True, attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)
        if not stretch:
            end_fk_flag.set_attr_state(True, attr_list=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS)
            
        else:
            end_fk_flag.set_attr_state(True, attr_list=attr_utils.SCALE_ATTRS)
            

        # Get our OG component ik flags.
        ik_joint_chain = frag_rig_node.pynode.ik_chain.get()
        ik_flag = frag_rig_node.flags[0]

        # switch flag
        switch_flag = flags.Flag.create(f'f_{frag_rig_node.side}_{frag_rig_node.region}_ikfk_switch', bind_chain[-1], scale*.5, flag_path='triangle')
        switch_flag.side = wrapped_joint.side
        switch_flag.region = wrapped_joint.region

        # Get the distance of the chain to use to set our switch flag position, then place it based on the vector from origin to second joint.
        pt1, pt2 = [pm.xform(x, q=True, ws=True, t=True) for x in bind_chain]
        chain_length = pymaths.get_distance_between_points(pt1, pt2)
        # Cancel out the height here we we normalize the vector.
        origin_to_end_vector = pymaths.normalize_vector([pt2[0], 0, pt2[-1]])
        switch_flag_pos = pymaths.add_vectors(pt2, pymaths.scale_vector(origin_to_end_vector, (chain_length*.25)))

        switch_align_group = switch_flag.align_group
        switch_align_group.t.set(switch_flag_pos)
        # NOTE: lock the switch flag attrs here before we add the switch attr.
        switch_align_group.setParent(flags_group)
        constraint_utils.parent_constraint_safe(bind_chain[-1], switch_align_group, mo=True)
        switch_flag.set_attr_state()

        switch_flag.pynode.addAttr('ikfk_switch', k=True, at='double', min=0.0, max=1.0, dv=1.0)
        reverse_node = attr_utils.invert_attribute(switch_flag.pynode.ikfk_switch)

        # Set our flag visibilities.
        reverse_node.straight >> ik_flag.pynode.v
        for fk_flag in fk_flag_list:
            reverse_node.inverse >> fk_flag.pynode.v

        for bind_joint, fk_joint, ik_joint in zip(bind_chain, fk_joint_chain, ik_joint_chain):
            # Remove OG IK constraints to the bind joints.
            pm.delete(bind_joint.getChildren(type=pm.nt.Constraint))

            if ik_joint == ik_joint_chain[-1]:
                if stretch:
                    # If we're set to allow stretch constrain the end joint directly to the Ik flag instead of the ik joints.
                    bind_constraint = constraint_utils.parent_constraint_safe([fk_joint, ik_flag.pynode], bind_joint)
                else:
                    bind_constraint = constraint_utils.parent_constraint_safe([fk_joint, ik_joint], bind_joint)
            reverse_node.straight >> bind_constraint.getWeightAliasList()[1]
            reverse_node.inverse >> bind_constraint.getWeightAliasList()[0]

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(fk_flag_list+[switch_flag], 'flags', 'fragParent', merge_values=True)
        frag_rig_node.connect_nodes([ik_flag], 'ik_flags', 'fragParent')
        frag_rig_node.connect_nodes(fk_flag_list, 'fk_flags', 'fragParent')

        frag_rig_node.connect_nodes(fk_joint_chain, 'fk_chain', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return skel_hierarchy, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        joint_list = skel_hierarchy.get_full_chain(self.side, self.region)
        if not joint_list:
            return skel_hierarchy, []
        
        _, end_joint = joint_list
        ik_flag_pynode = self.pynode.getAttr('ik_flags')[0] # This will be the IK flag and the PV flag
        return_list = [constraint_utils.parent_constraint_safe(end_joint, ik_flag_pynode)]

        fk_flag_pynode_list = self.pynode.getAttr('fk_flags')
        for joint_node, fk_flag_pynode in zip(joint_list, fk_flag_pynode_list):
            return_list.append(constraint_utils.parent_constraint_safe(joint_node, fk_flag_pynode))
        return skel_hierarchy, return_list
        