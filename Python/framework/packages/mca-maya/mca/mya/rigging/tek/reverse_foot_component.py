#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import constraint, dag
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import ik_utils, joint_utils
from mca.mya.rigging import chain_markup, ik_chain, fk_chain, ikfk_switch, reverse_foot_rig
from mca.mya.rigging.flags import tek_flag
# Internal module imports
from mca.mya.rigging.tek import keyable_component


class ReverseFootComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
                start_joint,
                end_joint,
                side,
                region,
                scale=1.0,
                ik_flag_orient=None,
                ik_flag_pv_orient=None,
                ik_flag_rotate_order=None,
                lock_child_rotate_axes=(),
                lock_child_translate_axes=('tx', 'ty', 'tz'),
                lock_root_translate_axes=('tx', 'ty', 'tz'),
                ankle_as_primary=True,
                **kwargs):
        """
        Creates an ikfk component.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of IKFKComponent.
        :rtype: IKFKComponent
        """

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(tek_parent,
                                                         ReverseFootComponent.__name__,
                                                         ReverseFootComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        middle_joint = chain_between[1]

        # Create the FK Chain ##############
        chain_fk = joint_utils.duplicate_chain(start_joint, end_joint, suffix='fk_chain')
        chain_fk[0].setParent(nt_grp)
        chain_fk_result = fk_chain.fk_joint_chain(chain_fk[0],
                                                  chain_fk[2],
                                                  scale=scale,
                                                  children_align_transforms=True,
                                                  create_end_flag=True,
                                                  offset_flag=True)

        # Lock Attributes
        fk_flags = chain_fk_result['flags']
        flags = chain_fk_result['flags']
        fk_flag_offset = chain_fk_result['offset_flag']

        [x.v.set(keyable=False, channelBox=False) for x in flags]

        attrs_to_lock = ['sx', 'sy', 'sz'] + list(lock_root_translate_axes)
        flags[0].lock_and_hide_attrs(attrs_to_lock)

        # Create the FK toe flag
        ball_joint = chain_fk[3]
        label = ball_joint.replace('_fk_chain', '')
        fk_ball_flag = tek_flag.Flag.create_ratio(ball_joint,
                                                   scale=scale,
                                                   label=label,
                                                   add_align_transform=True)
        fk_ball_align = fk_ball_flag.get_align_transform()
        fk_ball_flag.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz'])
        pm.parentConstraint(fk_ball_flag, ball_joint, w=True, mo=False)


        # flags.pop(0)
        attrs_to_lock = attrs_to_lock + list(lock_child_rotate_axes) + list(lock_child_translate_axes)
        [x.lock_and_hide_attrs(attrs_to_lock) for x in flags if x != flags[0]]

        # Organize groups
        start_flag = fk_flags[0]
        flag_align_grp = start_flag.alignTransform.get()
        flag_align_grp.setParent(flag_grp)
        chain_fk[0].setParent(nt_grp)
        end_flag = fk_flags[-1]
        pm.parent(fk_ball_align, end_flag)
        if fk_flag_offset:
            pm.parentConstraint(fk_flag_offset, fk_ball_align, w=True, mo=True)
        fk_flags.append(fk_ball_flag)

        # Create the IK Chain ########################
        # Duplicate chain and set up the fk chain
        chain_ik = joint_utils.duplicate_chain(start_joint, end_joint, suffix='ik_chain')
        chain_ik[0].setParent(nt_grp)
        chain_ik_result = ik_chain.ik_joint_chain(chain_ik[0],
                                                  chain_ik[2],
                                                  scale=scale,
                                                  side=side,
                                                  region=region,
                                                  ik_flag_orient=ik_flag_orient,
                                                  ik_flag_pv_orient=ik_flag_pv_orient,
                                                  ik_flag_rotate_order=ik_flag_rotate_order)

        # Edit results
        ik = chain_ik_result['ik_handle']
        pm.delete(chain_ik_result['offset_constraint'])
        ik_align_group = chain_ik_result['ik_zero']
        ik_align_group.visibility.set(0)

        pv_flag = chain_ik_result['pv_flag']
        ik_flag = chain_ik_result['ik_flag']
        if not ankle_as_primary:
            ik_constraint = chain_ik_result['ik_constraint']
            pm.delete(ik_constraint)
            ik_align_transform = ik_flag.alignTransform.get()
            pm.delete(constraint.point_constraint_safe(chain_ik[3], ik_align_transform))
            constraint.parent_constraint_safe(ik_flag, ik_align_group, w=True, mo=True)
        ik_flag_offset = chain_ik_result['ik_flag_offset']
        pv_line = chain_ik_result['pv_line']
        line_clusters = chain_ik_result['line_clusters']
        ik_solver = chain_ik_result['ik_solver']
        unit_conv_nodes = chain_ik_result['unit_conv_nodes']

        pv_flag.visibility >> pv_line.visibility
        pv_flag.overrideVisibility >> pv_line.overrideVisibility
        pv_flag.overrideEnabled >> pv_line.overrideEnabled

        # Create Reverse Foot ##############

        skel_hierarchy = chain_markup.ChainMarkup(start_joint)

        wrapped_joint = chain_markup.JointMarkup(start_joint)
        region_markup = wrapped_joint.region

        toe_contact_joint = skel_hierarchy.get_start(f'{region_markup}_toe', side)
        ball_contact_joint = skel_hierarchy.get_start(f'{region_markup}_ball', side)
        heel_contact_joint = skel_hierarchy.get_start(f'{region_markup}_heel', side)
        interior_lean_joint = skel_hierarchy.get_start(f'{region_markup}_interior', side)
        exterior_lean_joint = skel_hierarchy.get_start(f'{region_markup}_exterior', side)

        chain_rev_foot_result = reverse_foot_rig.reverse_foot_chain(chain_ik[2],
                                                                    chain_ik[-1],
                                                                    scale=scale,
                                                                    contact_joints=[toe_contact_joint, ball_contact_joint, exterior_lean_joint, interior_lean_joint, heel_contact_joint],
                                                                    side=side,
                                                                    region=region,
                                                                    ik_foot_flag=ik_flag)
        rev_foot_chain = chain_rev_foot_result['chain']
        pm.parent(rev_foot_chain[0], nt_grp)
        reverse_foot_grp = chain_rev_foot_result['reverse_foot_grp']
        rev_foot_chain = chain_rev_foot_result['reverse_chain']
        ik_toe_flag = chain_rev_foot_result['ik_toe_flag']
        clamp = chain_rev_foot_result['clamp']
        unit_conv_nodes = unit_conv_nodes + chain_rev_foot_result['unit_conv_nodes']
        # If we have an offset flag reset the constraints to handle the IK main vs offset flag.
        pm.delete(chain_rev_foot_result['alignment_constraint'])
        constraint.parent_constraint_safe(ik_flag_offset, reverse_foot_grp, mo=True)

        # Parent to IK and Organize
        pm.parent(ik, rev_foot_chain[0])
        pm.parent(reverse_foot_grp, nt_grp)
        reverse_foot_grp.v.set(0)

        # Create IKFK Switch
        switch_joint = chain_between[2]

        ikfk_switch_result = ikfk_switch.ikfk_switch(switch_joint, side, region, scale=scale)
        invert_node = ikfk_switch_result['invert_node']
        switch_flag = ikfk_switch_result['flag']
        switch_attr_name = ikfk_switch_result['name']

        # visibility switching
        invert_node.straight >> ik_flag.v
        invert_node.straight >> pv_flag.v
        for fk_flag in chain_fk_result['flags']:
            invert_node.inverse >> fk_flag.v
            fk_flag.v.lock()
        invert_node.inverse >> fk_flag_offset.v

        # Organize the groups
        ik_align_grp = ik_flag.alignTransform.get()
        toe_align_grp = ik_toe_flag.alignTransform.get()
        pv_align_grp = pv_flag.alignTransform.get()
        switch_align_grp = switch_flag.alignTransform.get()

        pm.parent([pv_line, ik_align_group], nt_grp)
        pm.parent([ik_align_grp, toe_align_grp, pv_align_grp, switch_align_grp], flag_grp)

        # visibility setting, allows pv line to be seen
        chain_fk[0].v.set(0)
        chain_ik[0].v.set(0)
        nt_grp.v.unlock()
        nt_grp.v.set(1)
        nt_grp.v.lock()

        # lock attributes
        ik_flag.lock_and_hide_attrs(['sx', 'sy', 'sz', 'v'])
        ik_flag_offset.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        fk_flag_offset.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        pv_flag.lock_and_hide_attrs(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        switch_flag.lock_and_hide_attrs(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'radius', 'v'])
        fk_flags[1].lock_and_hide_attrs(['rx', 'ry'])
        unit_conv_nodes = [x for x in ik_flag.listConnections() if isinstance(x, pm.nt.UnitConversion)] + unit_conv_nodes

        # Meta Connections
        node.connect_nodes(chain_ik, 'ikChain', 'tekParent')
        node.connect_node(ik_flag, 'ikFlag', 'tekParent')
        node.connect_node(ik_flag_offset, 'ikFlagOffset', 'tekParent')
        node.connect_node(fk_flag_offset, 'fkFlagOffset', 'tekParent')
        node.connect_node(pv_flag, 'pvFlag', 'tekParent')
        node.connect_node(ik_toe_flag, 'ikToeFlag', 'tekParent')
        node.connect_node(pv_line, 'pvLine', 'tekParent')
        node.connect_node(ik, 'ikHandle', 'tekParent')
        node.connect_nodes(line_clusters, 'lineClusters', 'tekParent')
        node.addAttr('switchAttrName', dt='string')
        node.attr('switchAttrName').set(switch_attr_name)
        node.connect_node(switch_flag, 'switchFlag', 'tekParent')
        node.connect_node(invert_node, 'invertNode', 'tekParent')
        node.connect_node(start_joint, 'startJoint')
        node.connect_node(end_joint, 'endJoint')
        node.connect_nodes(chain_between, 'bindJoints')
        node.connect_nodes(chain_fk, 'fkChain', 'tekParent')
        node.connect_nodes(fk_flags, 'fkFlags', 'tekParent')
        node.connect_node(clamp, 'clamp', 'tekParent')
        node.connect_node(ik_solver, 'ik_solver', 'tekParent')
        node.connect_nodes(unit_conv_nodes, 'unitConvNodes', 'tekParent')

        # Make the ik joints and fk joints control the base joints
        for x in range(len(chain_between)):
            orientConst = pm.orientConstraint(chain_fk[x], chain_ik[x], chain_between[x], w=1, mo=0)
            pointConst = pm.pointConstraint(chain_fk[x], chain_ik[x], chain_between[x], w=1, mo=1)

            # IK
            invert_node.straight >> orientConst.getWeightAliasList()[1]
            invert_node.straight >> pointConst.getWeightAliasList()[1]
            # FK
            invert_node.inverse >> orientConst.getWeightAliasList()[0]
            invert_node.inverse >> pointConst.getWeightAliasList()[0]


        # Create the Reverse Foot

        return node

    def get_flags(self):
        flags = self.fkFlags.listConnections()
        flags.append(self.ikFlag.get())
        flags.append(self.ikFlagOffset.get())
        flags.append(self.fkFlagOffset.get())
        flags.append(self.pvFlag.get())
        flags.append(self.ikToeFlag.get())
        switch_flag = self.switchFlag.get()
        if switch_flag and switch_flag not in flags:
            flags.append(switch_flag)
        return [tek_flag.Flag(x) for x in flags]

    @property
    def fk_flags(self):
        flags = self.fkFlags.listConnections()
        return list(map(lambda x: tek_flag.Flag(x), flags))

    @property
    def ik_flags(self):
        flags = [self.ikFlag.get(), self.ikFlagOffset.get(), self.pvFlag.get(), self.ikToeFlag.get()]
        return list(map(lambda x: tek_flag.Flag(x), flags))

    @property
    def ik_flag(self):
        return tek_flag.Flag(self.ikFlag.get())

    @property
    def ik_flag_offset(self):
        return tek_flag.Flag(self.ikFlagOffset.get())

    @property
    def fk_flag_offset(self):
        return tek_flag.Flag(self.fkFlagOffset.get())

    @property
    def pv_flag(self):
        return tek_flag.Flag(self.pvFlag.get())

    @property
    def switch_flag(self):
        return tek_flag.Flag(self.switchFlag.get())

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

        fk_flag_list = self.fk_flags
        ik_flag_list = [self.ik_flag, self.pv_flag, self.ikToeFlag.get()]

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
            if len(fk_flag_list) < 4:
                # ToDo FSchorsch Hack: ball flag isn't listed in the flag objects, so lets go looking for it.
                found_flags = pm.listRelatives(fk_flag_list[-1], ad=True, type=pm.nt.Joint)
                for flag_node in found_flags:
                    if 'ball' in flag_node.name():
                        fk_flag_list.append(flag_node)
                # End Hack
            if fk_flag_list and len(fk_flag_list) <= len(joint_list):
                # fk constraints
                for flag_node, joint_node in list(zip(fk_flag_list, joint_list)):
                    constraint_node = constraint.parent_constraint_safe(joint_node, flag_node, mo=mo)
                    if constraint_node:
                        constraint_list.append(constraint_node)

            if ik_flag_list:
                # ik constraints
                constraint_node = constraint.parent_constraint_safe(joint_list[2], ik_flag_list[0], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

                pv_locator = ik_utils.create_pole_vector_locator(joint_list[:3])
                pv_locator.setParent(joint_list[1])
                pv_locator.addAttr('bake_helper', at=bool, dv=True)
                constraint_node = constraint.parent_constraint_safe(pv_locator, ik_flag_list[1], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

                constraint_node = constraint.parent_constraint_safe(joint_list[-1], ik_flag_list[-1], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

        return constraint_list