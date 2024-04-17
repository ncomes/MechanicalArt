#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Z leg setup for quadrupeds.
"""

# System global imports
from __future__ import print_function, division, absolute_import

# Software specific imports
import pymel.core as pm

# mca Python imports
from mca.common import log
from mca.mya.utils import attr_utils, constraint, dag
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import ik_utils, joint_utils, rig_utils, chain_markup, ikfk_switch, fk_chain as fk_utils
from mca.mya.rigging.flags import tek_flag
# internal module imports
from mca.mya.rigging.tek import keyable_component
from mca.mya.rigging import reverse_foot_rig

logger = log.MCA_LOGGER


class ZLegComponent(keyable_component.KeyableComponent):
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
               **kwargs):
        """
        Creates a z leg component.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param list[float, float, float] ik_flag_orient:
        :param list[float, float, float] ik_flag_pv_orient:
        :param ik_flag_rotate_order: Change IK object's rotate order, default is xyz
        :return: Returns an instance of IKFKComponent.
        :rtype: IKFKComponent
        """

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        leg_chain = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        skel_hierarchy = chain_markup.ChainMarkup(start_joint)

        if len(leg_chain) < 4:
            logger.warning('Joint chain is insufficient length.')
            return

        node = keyable_component.KeyableComponent.create(tek_parent,
                                                         ZLegComponent.__name__,
                                                         ZLegComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()
        nt_grp.v.unlock()
        nt_grp.v.set(True)

        skel_offset_grp = pm.group(n=f'{region}_{side}_joint_offset', em=True, w=True)
        skel_offset_grp.v.set(False)
        skel_offset_grp.setParent(nt_grp)
        pm.delete(constraint.parent_constraint_safe(leg_chain[0].getParent(), skel_offset_grp))
        # $FSchorsch Not sure why I added this originally, but it behaves weird with it.
        #constraint.orient_constraint_safe(nt_grp.getParent(), skel_offset_grp)

        # IK Setup
        ik_chain = joint_utils.duplicate_chain(leg_chain[0], leg_chain[-1], suffix='ik')
        ik_chain[0].setParent(skel_offset_grp)
        ik_drv_chain = joint_utils.duplicate_chain(leg_chain[0], leg_chain[-1], suffix='drv')
        ik_drv_chain[0].setParent(skel_offset_grp)

        # Collect rev foot contact joints.
        toe_contact_joint = skel_hierarchy.get_start(f'{region}_toe', side)
        ball_contact_joint = skel_hierarchy.get_start(f'{region}_ball', side)
        heel_contact_joint = skel_hierarchy.get_start(f'{region}_heel', side)
        interior_lean_joint = skel_hierarchy.get_start(f'{region}_interior', side)
        exterior_lean_joint = skel_hierarchy.get_start(f'{region}_exterior', side)

        # ik system flags
        ik_flag = tek_flag.Flag.create(ik_chain[3],
                                   label=f'{region}_{side}',
                                   orientation=ik_flag_orient,
                                   scale=scale)
        ik_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
        ik_flag_alignment_grp = ik_flag.get_align_transform()
        ik_flag_alignment_grp.setParent(flag_grp)

        ik_offset_flag = tek_flag.Flag.create(ik_chain[3],
                                          label=f'{region}_{side}_offset',
                                          orientation=ik_flag_orient,
                                          scale=scale*.85)
        ik_offset_flag.lock_and_hide_attrs(['v'] + attr_utils.TRANSLATION_ATTRS + attr_utils.SCALE_ATTRS)
        ik_offset_flag.set_as_detail()
        ik_offset_flag_alignment_grp = ik_offset_flag.get_align_transform()
        ik_offset_flag_alignment_grp.setParent(ik_flag)

        orient_str_val = {'xyz': 0, 'yzx': 1, 'zxy': 2, 'xzy': 3, 'yxz': 4, 'zyx': 5}

        if ik_flag_rotate_order and orient_str_val.keys():
            temp_loc = rig_utils.create_locator_at_object(ik_flag)
            ik_flag.rotateOrder.set(orient_str_val[ik_flag_rotate_order])
            pm.delete(constraint.orient_constraint_safe(temp_loc, ik_flag, w=True, mo=False))
            pm.delete(temp_loc)

        # build reverse foot.
        chain_rev_foot_result = reverse_foot_rig.reverse_foot_chain(ik_chain[3],
                                                                    ik_chain[-1],
                                                                    contact_joints=[toe_contact_joint,
                                                                                    ball_contact_joint,
                                                                                    exterior_lean_joint,
                                                                                    interior_lean_joint,
                                                                                    heel_contact_joint],
                                                                    side=side,
                                                                    region=region,
                                                                    ik_foot_flag=ik_flag,
                                                                    scale=scale)
        unit_conv_nodes = chain_rev_foot_result['unit_conv_nodes']
        rev_foot_chain = chain_rev_foot_result['chain']
        pm.parent(rev_foot_chain[0], nt_grp)

        rev_foot_chain = chain_rev_foot_result['reverse_chain']
        contact_alignment_grp = chain_rev_foot_result['reverse_foot_grp']
        contact_alignment_grp.v.set(False)
        contact_alignment_grp.setParent(nt_grp)

        ik_toe_flag = chain_rev_foot_result['ik_toe_flag']
        ik_toe_flag_alignment_grp = ik_toe_flag.get_align_transform()
        ik_toe_flag_alignment_grp.setParent(flag_grp)

        pm.delete(chain_rev_foot_result['alignment_constraint'])
        constraint.parent_constraint_safe(ik_offset_flag, contact_alignment_grp, mo=True)

        # add a new foot lift joint that hangs out with the driver chain and use it to drive our lift.
        foot_lift_joint = joint_utils.duplicate_joint(ik_drv_chain[2], f'{region}_{side}_foot_lift')
        foot_lift_joint.setParent(ik_drv_chain[3])
        foot_lift_joint.t.set([0, 0, 0])

        # Set up the aim constraint by finding the primary axis and offsetting the aim by one axis.
        # This means if X is the aim axis Y will be the up axis.
        primary_axis, axis_is_positive = rig_utils.find_primary_axis(ik_chain[2])
        ik_flag.addAttr('ankleLift', k=True, at='double')
        ik_flag.ankleLift >> foot_lift_joint.attr(f'r{"xyz"["XYZ".index(primary_axis) - 1]}')

        # Pole Vector position
        pv_point = ik_utils.get_pole_vector_position(ik_chain[:3])

        # Find pv point before ik, in case joints move
        pv_locator = pm.spaceLocator(n=f'{region}_{side}_pv_loc')
        pv_locator.t.set(pv_point)
        pv_flag = tek_flag.Flag.create(pv_locator,
                                            label=f'{region}_{side}_pv',
                                            add_align_transform=True,
                                            orientation=ik_flag_pv_orient,
                                            scale=scale)
        pv_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
        pv_flag_alignment_grp = pv_flag.get_align_transform()
        pv_flag_alignment_grp.setParent(flag_grp)
        pm.delete(pv_locator)

        pv_line = rig_utils.create_line_between(ik_chain[1], pv_flag, name=f'{side}_{region}_pv_line')
        pv_line.setParent(nt_grp)

        pm.mel.eval('ikSpringSolver;')

        # setup the IK handles and organize them appropriately.
        alignment_loc = pm.spaceLocator(n=f'{region}_{side}_alignment_loc')
        alignment_loc.v.set(False)
        alignment_loc.setParent(nt_grp)
        constraint.parent_constraint_safe(rev_foot_chain[0], alignment_loc)

        # $HACK FSchorsch start the main ik solver as a RP solver then convert it to a Spring
        # Maya has this stupid habit of adjusting the joints when you start it as a spring solver.
        main_ik_handle, _ = pm.ikHandle(sol='ikRPsolver', sj=ik_drv_chain[0], ee=ik_drv_chain[3])
        pm.connectAttr(pm.PyNode('ikSpringSolver.message'), main_ik_handle.ikSolver, force=True)
        main_ik_handle.rename(f'{region}_{side}_main_ik_handle')
        main_ik_handle.setParent(alignment_loc)
        main_ik_handle.twist.set(180)
        pv_constraint = pm.poleVectorConstraint(pv_flag, main_ik_handle, w=1)

        top_ik_handle, _ = pm.ikHandle(sol='ikRPsolver', sj=ik_chain[0], ee=ik_chain[2])
        top_ik_handle.rename(f'{region}_{side}_udrv_ik_handle')
        top_ik_handle.setParent(foot_lift_joint)

        bot_ik_handle, _ = pm.ikHandle(sol='ikSCsolver', sj=ik_chain[2], ee=ik_chain[3])
        bot_ik_handle.rename(f'{region}_{side}_ldrv_ik_handle')
        bot_ik_handle.setParent(ik_drv_chain[3])

        # FK Setup
        fk_chain = joint_utils.duplicate_chain(leg_chain[0], leg_chain[-1], suffix='fk')
        fk_chain[0].setParent(nt_grp)
        fk_chain[0].v.set(False)
        chain_fk_result = fk_utils.fk_joint_chain(fk_chain[0],
                                                  fk_chain[-1],
                                                  create_end_flag=True,
                                                  scale=scale)
        fk_flags = chain_fk_result['flags']
        fk_flag_alignment_grp = fk_flags[0].get_align_transform()
        fk_flag_alignment_grp.setParent(flag_grp)

        # Ik/Fk Switch and shared constraints.

        switch_joint = leg_chain[2]

        ikfk_switch_result = ikfk_switch.ikfk_switch(switch_joint, side, region, scale=scale)
        invert_node = ikfk_switch_result['invert_node']
        switch_flag = ikfk_switch_result['flag']
        switch_flag.lock_and_hide_attrs(['v'] + attr_utils.TRANSFORM_ATTRS)
        switch_flag_alignment_grp = switch_flag.get_align_transform()
        switch_flag_alignment_grp.setParent(flag_grp)
        switch_attr_name = ikfk_switch_result['name']

        # visibility switching
        invert_node.straight >> ik_flag.v
        ik_flag.lock_and_hide_attrs(['v'])
        invert_node.straight >> pv_flag.v
        invert_node.straight >> pv_line.v
        pv_flag.lock_and_hide_attrs(['v'])
        for index, fk_flag in enumerate(fk_flags):
            invert_node.inverse >> fk_flag.v
            fk_flag.v.lock()
            if index and fk_flag not in fk_flags[-2:]:
                fk_flag.lock_and_hide_attrs(['v', 'rx', 'ry'] + attr_utils.TRANSLATION_ATTRS + attr_utils.SCALE_ATTRS)
            else:
                fk_flag.lock_and_hide_attrs(['v'] + attr_utils.TRANSLATION_ATTRS + attr_utils.SCALE_ATTRS)

        for skel_joint, ik_joint, fk_joint in zip(leg_chain, ik_chain, fk_chain):
            shared_constraint = constraint.parent_constraint_safe([fk_joint, ik_joint], skel_joint, w=1)

            # IK
            invert_node.straight >> shared_constraint.getWeightAliasList()[1]
            invert_node.straight >> shared_constraint.getWeightAliasList()[1]
            # FK
            invert_node.inverse >> shared_constraint.getWeightAliasList()[0]
            invert_node.inverse >> shared_constraint.getWeightAliasList()[0]

        clamp_ext = chain_rev_foot_result['clamp']
        ik_sc_solver = bot_ik_handle.ikSolver.get()
        ik_spring_solver = main_ik_handle.ikSolver.get()
        unit_conv_nodes = unit_conv_nodes + ik_flag.listConnections(type=pm.nt.UnitConversion)
        # Meta Connections
        node.connect_nodes(ik_chain, 'ikChain', 'tekParent')
        node.connect_node(ik_flag, 'ikFlag', 'tekParent')
        node.connect_node(ik_offset_flag, 'ikFlagOffset', 'tekParent')
        node.connect_node(pv_flag, 'pvFlag', 'tekParent')
        node.connect_node(ik_toe_flag, 'ikToeFlag', 'tekParent')
        node.connect_node(pv_line, 'pvLine', 'tekParent')
        node.addAttr('switchAttrName', dt='string')
        node.attr('switchAttrName').set(switch_attr_name)
        node.connect_node(switch_flag, 'switchFlag', 'tekParent')
        node.connect_node(invert_node, 'invertNode', 'tekParent')
        node.connect_node(start_joint, 'startJoint')
        node.connect_node(end_joint, 'endJoint')
        node.connect_nodes(leg_chain, 'bindJoints')
        node.connect_nodes(fk_chain, 'fkChain', 'tekParent')
        node.connect_nodes(fk_flags, 'fkFlags', 'tekParent')
        node.connect_nodes([ik_sc_solver, ik_spring_solver], 'ikSolver', 'tekParent')
        node.connect_nodes(unit_conv_nodes, 'unitConvNodes', 'tekParent')
        node.connect_node(clamp_ext, 'clamp', 'tekParent')

        return node

    def get_flags(self):
        flags = self.fkFlags.listConnections()
        flags.append(self.ikFlag.get())
        flags.append(self.ikFlagOffset.get())
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

    def attach_component(self, parent_component_list, parent_object_list, point=True, orient=True):
        """
        Constrain the flag and no touch groups to a list of given parent objects for point and orient.

        :param list[TEKNode] parent_component_list: The TEK Nodes that should be registered as parents for attachment.
        :param list[Transform] parent_object_list: A list of transforms this component should be constrainted between.
        :param bool point: If this TEK component should constrain its translation.
        :param bool orient: If this TEK component should constrain its rotation.
        """
        # Little override here to pitch the orient constraints since that causes the P Vector constraint to fail.

        # Get local level groups
        if not parent_object_list or not parent_component_list or not any([point, orient]):
            return

        if not isinstance(parent_object_list, list):
            parent_object_list = [parent_object_list]

        if not isinstance(parent_component_list, list):
            parent_component_list = [parent_component_list]

        flag_grp = self.pynode.getAttr('flagGroup')
        nt_grp = self.pynode.getAttr('noTouch')

        for align_grp in [flag_grp, nt_grp]:
            # Reset the constraints by stripping the old ones.
            pm.delete(pm.listRelatives(align_grp, type=pm.nt.Constraint))

        attr_utils.set_attr_state(nt_grp, False, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

        if point:
            constraint.parent_constraint_safe(parent_object_list, flag_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])
            constraint.parent_constraint_safe(parent_object_list, nt_grp, mo=1, skip_rotate_attrs=['x', 'y', 'z'])

        self.pointParentAttachments.disconnect()
        for node in parent_component_list:
            if point:
                self._connect_parent(node, self.pointParentAttachments)

        for node in parent_object_list:
            if point:
                self._connect_parent(node, self.pointParentObjects)

        attr_utils.set_attr_state(nt_grp, True, attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS)

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
                constraint_node = constraint.parent_constraint_safe(joint_list[3], ik_flag_list[0], mo=mo)
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
