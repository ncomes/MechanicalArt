#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the IK rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.utils import pymaths

from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils

from mca.mya.rigging.frag.build import ik_chain
from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class IKComponent(frag_rig.FRAGAnimatedComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, **kwargs):
        """
        Creates a new IK component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :return: The newly created frag node.
        :rtype: IKComponent
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
        if not frag_rig_node:
            return

        # Save kwargs to node attrs we'll use these for serializing.
        # None here.

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()
        pv_group = pm.group(n=f'{rig_side}_{rig_region}_pv_group',em=True, w=True)
        pv_group.setParent(dnt_group.getParent())
        align_node = alignment_node or start_joint
        pm.delete(pm.pointConstraint(align_node, flags_group))
        pm.delete(pm.pointConstraint(align_node, dnt_group))
        pm.delete(pm.pointConstraint(align_node, pv_group))

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = dag_utils.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        if len(bind_chain) < 3:
            logger.error('Chain must be length of 3 or greater, and only the first three joints will be used.')
            frag_rig_node.remove()
            return

        ik_joint_chain = joint_utils.duplicate_chain(bind_chain[0], bind_chain[-1], 'ikc')
        ik_joint_chain[0].setParent(dnt_group)
        ik_results = ik_chain.build_ik_chain(ik_joint_chain[0:3], scale)

        # Bail if we failed to build.
        if not ik_results:
            logger.error('build failure occured.')
            try:
                frag_rig_node.remove()
                pm.delete(ik_joint_chain)
            except:
                pass
            return

        # Parent flag alignment groups into the flags group.
        ik_flag, pv_flag = ik_results.get('flags')
        for new_flag in [ik_flag, pv_flag]:
            new_flag.align_group.setParent(flags_group)

        # Parent pv and ik handle alignment group to dnt.
        ik_align_group = ik_results.get('ik_align_group')
        pv_curve = ik_results.get('pv_curve')
        pv_curve.setParent(pv_group)
        pm.parent(ik_align_group, dnt_group)

        # Check Constraints
        for bind_joint_node, ik_joint_node in zip(bind_chain, ik_joint_chain):
            constraint_utils.parent_constraint_safe(ik_joint_node, bind_joint_node)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes(ik_results.get('flags'), 'flags', 'fragParent')

        frag_rig_node.connect_nodes(ik_joint_chain, 'ik_chain', 'fragParent')

        frag_rig_node.connect_node(ik_flag, 'ik_flag', 'fragParent')
        frag_rig_node.connect_node(pv_flag, 'pv_flag', 'fragParent')
        frag_rig_node.connect_node(pv_curve, 'pv_curve', 'fragParent')
        frag_rig_node.connect_node(pv_group, 'pv_group', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('ik_constraint'), 'ik_constraint', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('ik_handle'), 'ik_handle', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('ik_solver'), 'ik_solver', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('switch_align'), 'switch_align', 'fragParent')
        frag_rig_node.connect_nodes(ik_results.get('unit_conv_nodes'), 'unit_conv_nodes', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
    
    def remove(self):
        if self.pynode.hasAttr('pv_group'):
            pm.delete(self.pynode.getAttr('pv_group'))
        pm.delete([self.do_not_touch_group, self.flags_group, self.pynode])

    def attach_to_skeleton(self, root_joint, skel_hierarchy=None, *args, **kwargs):
        if not root_joint:
            return skel_hierarchy, []
        
        if not skel_hierarchy:
            skel_hierarchy = joint_utils.SkeletonHierarchy(root_joint)

        joint_list = skel_hierarchy.get_full_chain(self.side, self.region)
        if not joint_list:
            return skel_hierarchy, []
        start_joint, mid_joint, end_joint, *_ = joint_list
        ik_flag, pv_flag, *_ = self.flags # This will be the IK flag and the PV flag
        return_list = [constraint_utils.parent_constraint_safe(end_joint, ik_flag.pynode)]

        # Create a temporary PV locator and parent it into the skeleton.
        pole_vector_pos = pymaths.get_pole_vector_pos(*[pm.xform(x, q=True, t=True, ws=True) for x in [start_joint, mid_joint, end_joint]])
        pv_locator = pm.Locator(n=f'bake_attach_pv').getParent()
        return_list.append(pv_locator)
        pv_locator.t.set(pole_vector_pos)
        pv_locator.setParent(mid_joint)

        return_list.append(constraint_utils.parent_constraint_safe(pv_locator, pv_flag.pynode))
        return skel_hierarchy, return_list
    
class TwoPointIKComponent(frag_rig.FRAGAnimatedComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None, stretch=False, **kwargs):
        """
        Creates a new TwoPointIk component on the provided chain of joints.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :param bool stretch: If the end joint should retain its distance from the start.
        :return: The newly created frag node.
        :rtype: TwoPointIKComponent
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
        kwargs_dict = {}
        kwargs_dict['stretch'] = stretch
        attr_utils.set_compound_attribute_groups(frag_rig_node.pynode, 'buildKwargs', kwargs_dict)

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()
        align_node = alignment_node or start_joint
        pm.delete(pm.pointConstraint(align_node, flags_group))
        pm.delete(pm.pointConstraint(align_node, dnt_group))

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = dag_utils.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        if len(bind_chain) != 2:
            logger.error('Chain must be length of 2.')
            frag_rig_node.remove()
            return
        
        ik_joint_chain = joint_utils.duplicate_chain(bind_chain[0], bind_chain[-1], 'ikc')
        ik_joint_chain[0].setParent(dnt_group)
        ik_results = ik_chain.build_twopointik_chain(ik_joint_chain, scale)

        # Bail if we failed to build.
        if not ik_results:
            logger.error('build failure occured.')
            try:
                frag_rig_node.remove()
                pm.delete(ik_joint_chain)
            except:
                pass
            return

        # Parent flag alignment groups into the flags group.
        ik_flag = ik_results.get('flags')[0]
        ik_flag.align_group.setParent(flags_group)

        # Parent pv and ik handle alignment group to dnt.
        ik_align_group = ik_results.get('ik_align_group')
        pm.parent(ik_align_group, dnt_group)

        # Check Constraints
        for bind_joint_node, ik_joint_node in zip(bind_chain, ik_joint_chain):
            if ik_joint_node == ik_joint_chain[-1]:
                if stretch:
                    # If we're set to allow stretch constrain the end joint directly to the Ik flag instead of the ik joints.
                    constraint_utils.parent_constraint_safe(ik_flag.pynode, bind_joint_node)
                    continue
                else:
                    constraint_utils.orient_constraint_safe(ik_flag.pynode, ik_joint_node)
            constraint_utils.parent_constraint_safe(ik_joint_node, bind_joint_node)

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes(ik_results.get('flags'), 'flags', 'fragParent')

        frag_rig_node.connect_nodes(ik_joint_chain, 'ik_chain', 'fragParent')

        frag_rig_node.connect_node(ik_results.get('ik_constraint'), 'ik_constraint', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('ik_handle'), 'ik_handle', 'fragParent')
        frag_rig_node.connect_node(ik_results.get('ik_solver'), 'ik_solver', 'fragParent')

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
        ik_flag = self.flags[0] # This will be the IK flag and the PV flag
        return_list = [constraint_utils.parent_constraint_safe(end_joint, ik_flag.pynode)]

        return skel_hierarchy, return_list
        