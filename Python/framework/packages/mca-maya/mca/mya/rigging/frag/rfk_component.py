#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import attr_utils, constraint, dag
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils
from mca.mya.rigging import chain_markup, rfk_chain
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class RFKComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
               start_joint,
               end_joint,
               side,
               region,
               scale=1.0,
               create_sub_flags=True,
               **kwargs):
        """
        Creates a reverse fk chain.
        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns the component.
        :rtype: RFKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['create_sub_flags'] = create_sub_flags

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                         RFKComponent.__name__,
                                                         version=RFKComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get in between joints
        between_joints = dag.get_between_nodes(first=start_joint, last=end_joint, node_type=pm.nt.Joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        # Create a duplicate chain and build rfk chain with dup joints
        dup_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='rfk_chain')
        chain_dict = rfk_chain.rfk_chain(start_joint=dup_chain[0],
                                         end_joint=dup_chain[-1],
                                         scale=scale,
                                         side=side,
                                         region=region,
                                         create_sub_flags=create_sub_flags,
                                         suffix='rfk_chain')

        # Set results
        mid_flags = chain_dict['mid_flags']
        end_twist_flag = chain_dict['end_twist_flag']
        start_twist_flag = chain_dict['start_twist_flag']
        mid_groups = chain_dict['mid_groups']
        chain_flag_groups = chain_dict['flags_groups']
        sub_flags = chain_dict['sub_flags']
        mid_offset_groups = chain_dict['mid_offset_groups']
        reverse_nodes = chain_dict['reverse_nodes']

        # Parent the duplicate chain to the Do Not Touch group
        dup_chain[0].setParent(nt_grp)

        # Clean up the with the groups
        for grp in mid_groups:
            grp.setParent(nt_grp)

        for fl in chain_flag_groups:
            fl.setParent(flag_grp)

        # Add Component Attributes and Connect
        node.connect_nodes(mid_flags, 'midFlags', 'fragParent')
        node.connect_nodes(dup_chain, 'rfkChain', 'fragParent')
        node.connect_node(end_twist_flag, 'topFlag', 'fragParent')
        node.connect_node(start_twist_flag, 'bottomFlag', 'fragParent')
        node.connect_nodes(between_joints, 'bindJoints')
        node.connect_nodes(mid_groups, 'midGroups', 'fragParent')
        node.connect_nodes(mid_offset_groups, 'midOffsetGroups', 'fragParent')
        node.connect_nodes(reverse_nodes, 'reverseNodes', 'fragParent')
        if sub_flags:
            node.connect_nodes(sub_flags, 'subFlags', 'fragParent')

        # Connect the rfk_joints to the base_joints
        for base, rfk in list(zip(between_joints, dup_chain)):
            pm.parentConstraint(rfk, base, w=True, mo=True)

        attr_utils.lock_and_hide_attrs(start_twist_flag, ['tx','ty','tz','sx','sy','sz','v'])
        attr_utils.lock_and_hide_attrs(end_twist_flag, ['tx','ty','tz','sx','sy','sz','v'])
        for mid_flag in mid_flags:
            attr_utils.lock_and_hide_attrs(mid_flag, ['tx','ty','tz','sx','sy','sz','v'])
        for sub_flag in sub_flags:
            attr_utils.lock_and_hide_attrs(sub_flag, ['tx','ty','tz','sx','sy','sz','v'])

        return node

    def get_flags(self):
        # primary flags need to be returned in order.
        flags = [self.getAttr('bottomFlag')]
        flags += self.midFlags.listConnections()
        flags.append(self.getAttr('topFlag'))

        if self.hasAttr('subFlags') and self.subFlags.listConnections():
            flags += self.subFlags.listConnections()
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

    @property
    def start_flag(self):
        return frag_flag.Flag(self.bottomFlag.get())

    @property
    def end_flag(self):
        return frag_flag.Flag(self.topFlag.get())

    @property
    def mid_flags(self):
        flags = sorted(self.midFlags.listConnections())
        return list(map(lambda x: frag_flag.Flag(x), flags))

    @property
    def sub_flags(self):
        if not self.hasAttr('subFlags') or not self.subFlags.listConnections():
            return
        return self.subFlags.listConnections()

    @property
    def mid_groups(self):
        return self.midGroups.listConnections()

    @property
    def mid_offset_groups(self):
        return self.midOffsetGroups.listConnections()

    def attach_to_skeleton(self, attach_skeleton_root, mo=True):
        """
        Drive the component with a given skeleton.

        :param Joint attach_skeleton_root: Top level joint of the hierarchy to drive the component.
        :param bool mo: If object offsets should be maintained.
        :return: A list of all created constraints.
        :rtype list[Constraint]:
        """

        target_root_hierarchy = chain_markup.ChainMarkup(attach_skeleton_root)
        constraint_list = []

        flag_list = [self.start_flag]+self.mid_flags+[self.end_flag]
        bind_joint_list = self.bind_joints

        skel_region = None
        skel_side = None
        if bind_joint_list:
            wrapped_node = chain_markup.JointMarkup(bind_joint_list[0])
            skel_region = wrapped_node.region
            skel_side = wrapped_node.side

        skel_region = skel_region or self.region
        skel_side = skel_side or self.side

        joint_list = target_root_hierarchy.get_full_chain(skel_region, skel_side)
        if joint_list:
            if flag_list:
                if len(flag_list) == len(joint_list):
                    for flag_node, joint_node in list(zip(flag_list, joint_list)):
                        constraint_node = constraint.parent_constraint_safe(joint_node, flag_node, mo=mo)
                        if constraint_node:
                            constraint_list.append(constraint_node)
        return constraint_list
