#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import constraint, dag, attr_utils
from mca.mya.rigging import ik_utils, joint_utils
from mca.mya.rigging import chain_markup, ik_chain
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class IKComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
                start_joint,
                end_joint,
                side,
                region,
                **kwargs):
        """
        Creates an ik component.
        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of IKComponent.
        :rtype: IKComponent
        """

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                                                IKComponent.__name__,
                                                                                IKComponent.VERSION,
                                                                                side=side,
                                                                                region=region,
                                                                                align_component=start_joint)

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        if not (len(chain_between) == 3 or len(chain_between) == 4):
            raise RuntimeError('There can only be 3 joints between start_joint and end_joint inclusively')

        middle_joint = chain_between[1]
        # Duplicate chain and set up the fk chain
        chain_ik = joint_utils.duplicate_chain(start_joint, end_joint, suffix='ik_chain')
        chain_ik[0].setParent(nt_grp)
        chain_ik_result = ik_chain.ik_joint_chain(chain_ik[0],
                                                    chain_ik[-1],
                                                    side=side,
                                                    region=region)

        # edit results
        ik = chain_ik_result['ik_handle']
        ik_align_group = chain_ik_result['ik_zero']
        ik_align_group.visibility.set(0)
        pv_flag = chain_ik_result['pv_flag']
        ik_flag = chain_ik_result['ik_flag']
        ik_flag_offset = chain_ik_result['ik_flag_offset']
        pv_line = chain_ik_result['pv_line']
        flags = chain_ik_result['flags']
        ik_solver = chain_ik_result['ik_solver']
        unit_conv_nodes = chain_ik_result['unit_conv_nodes']

        pv_flag.visibility >> pv_line.visibility
        pv_flag.overrideVisibility >> pv_line.overrideVisibility

        end_joint.setAttr('side', ik_flag.getAttr('side'))
        end_joint.setAttr('type', ik_flag.getAttr('type'))
        end_joint.setAttr('otherType', ik_flag.getAttr('otherType'))

        end_joint.setAttr('side', ik_flag_offset.getAttr('side'))
        end_joint.setAttr('type', ik_flag_offset.getAttr('type'))
        end_joint.setAttr('otherType', ik_flag_offset.getAttr('otherType'))

        middle_joint.setAttr('side', pv_flag.getAttr('side'))
        middle_joint.setAttr('type', pv_flag.getAttr('type'))
        middle_joint.setAttr('otherType', pv_flag.getAttr('otherType'))

        # parenting
        ik_align_grp = ik_flag.alignTransform.get()
        pv_align_grp = pv_flag.alignTransform.get()
        ik_chain_start = chain_ik_result['start_joint']
        pm.parent([pv_line, ik_align_group, ik_chain_start], nt_grp)
        pm.parent([ik_align_grp, pv_align_grp], flag_grp)

        node.connect_node(ik_flag, 'ikFlag', 'fragParent')
        node.connect_node(ik_flag_offset, 'ikFlagOffset', 'fragParent')
        node.connect_node(pv_flag, 'pvFlag', 'fragParent')
        node.connect_node(pv_line, 'pvLine', 'fragParent')
        node.connect_node(ik, 'ikHandle', 'fragParent')
        node.connect_nodes(chain_ik, 'ikChain', 'fragParent')
        node.connect_nodes(chain_between, 'bindJoints')
        node.connect_nodes(flags, 'flags', 'fragParent')
        node.connect_node(ik_solver, 'ikSolver', 'fragParent')
        node.connect_nodes(unit_conv_nodes, 'unitConvNodes', 'fragParent')

        # Lock attrs
        attr_utils.lock_and_hide_attrs(ik_flag, ['sx', 'sy', 'sz', 'v'])
        attr_utils.lock_and_hide_attrs(pv_flag, ['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])

        # Make the ik joints control the base joints
        pm.parentConstraint(chain_ik[0], start_joint, w=1, mo=1)
        pm.parentConstraint(chain_ik[1], middle_joint, w=1, mo=1)
        pm.parentConstraint(chain_ik[2], chain_between[2], w=1, mo=1)

        return node

    def get_flags(self):
        flags = self.flags.listConnections()
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

    @property
    def ik_flag(self):
        return frag_flag.Flag(self.ikFlag.get())

    @property
    def ik_flag_offset(self):
        return frag_flag.Flag(self.ikFlagOffset.get())

    @property
    def pv_flag(self):
        return frag_flag.Flag(self.pvFlag.get())

    @property
    def switch_flag(self):
        return frag_flag.Flag(self.switchFlag.get())

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

        flag_list = [self.ik_flag, self.pv_flag]

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
                constraint_node = constraint.parent_constraint_safe(joint_list[-1], flag_list[0], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

                pv_locator = ik_utils.create_pole_vector_locator(joint_list)
                pv_locator.setParent(joint_list[1])
                pv_locator.addAttr('bake_helper', at=bool, dv=True)
                constraint_node = constraint.parent_constraint_safe(pv_locator, flag_list[-1], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)
        return constraint_list
