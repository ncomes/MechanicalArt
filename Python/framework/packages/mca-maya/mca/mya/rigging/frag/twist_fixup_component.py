#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Twist component for the FRAG system.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import twist_setup
# Internal module imports
from mca.mya.rigging.frag import rig_component


class TwistFixUpComponent(rig_component.RigComponent):
    VERSION = 2

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
               joint_list,
               side,
               region,
               **kwargs):
        """
        Creates a twist component.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param list[Joint] joint_list: The list of twist joints which will be driven by this twist drive system.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of TwistFixUpComponent.
        :rtype: TwistFixUpComponent
        """

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = rig_component.RigComponent.create(frag_parent,
                                                 TwistFixUpComponent.__name__,
                                                 TwistFixUpComponent.VERSION,
                                                 side=side,
                                                 region=region,
                                                 align_component=joint_list[0].getParent().getParent())
        nt_grp = node.noTouch.get()

        twist_grp, build_dict = twist_setup.twist_setup(joint_list)
        if not twist_grp:
            return node
        twist_grp.setParent(nt_grp)

        # Meta Connections
        node.connect_nodes(joint_list, 'bindJoints')
        node.connect_nodes(build_dict['mirror_chain'], 'mirrorChain')
        node.connect_nodes(build_dict['ik_chain'], 'ikChain')
        node.connect_nodes(build_dict['ik_handle'], 'ikHandle')
        node.connect_nodes(build_dict['multi_node'], 'multiNode')
        node.connect_nodes(build_dict['offset_loc'], 'offsetLoc')
        node.connect_nodes(build_dict['unit_conv_nodes'], 'unitConvNodes', 'fragParent')
        node.connect_nodes(twist_grp, 'twistGroups', 'fragParent')

        return node
