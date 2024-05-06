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
from mca.mya.rigging import ik_utils, joint_utils
from mca.mya.rigging import chain_markup, ik_chain, fk_chain, ikfk_switch
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class IKFKComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
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
                **kwargs):
        """
        Creates an ikfk component.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of IKFKComponent.
        :rtype: IKFKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['ik_flag_orient'] = ik_flag_orient
        kwargs_dict['ik_flag_pv_orient'] = ik_flag_pv_orient
        kwargs_dict['ik_flag_rotate_order'] = ik_flag_rotate_order
        kwargs_dict['lock_child_rotate_axes'] = lock_child_rotate_axes
        kwargs_dict['lock_child_translate_axes'] = lock_child_translate_axes
        kwargs_dict['lock_root_translate_axes'] = lock_root_translate_axes

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                                                IKFKComponent.__name__,
                                                                                IKFKComponent.VERSION,
                                                                                side=side,
                                                                                region=region,
                                                                                align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        if not (len(chain_between) == 3 or len(chain_between) == 4):
            raise RuntimeError('There can only be 3 joints between the start joint and the end joint.')

        middle_joint = chain_between[1]

        # Create the FK Chain ##############
        chain_fk = joint_utils.duplicate_chain(start_joint, end_joint, suffix='fk_chain')
        chain_fk[0].setParent(nt_grp)
        chain_fk_result = fk_chain.fk_joint_chain(chain_fk[0],
                                                    chain_fk[-1],
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

        #flags.pop(0)
        attrs_to_lock = attrs_to_lock + list(lock_child_rotate_axes) + list(lock_child_translate_axes)
        [x.lock_and_hide_attrs(attrs_to_lock) for x in flags if x != flags[0]]

        # Organize groups
        start_flag = fk_flags[0]
        flag_align_grp = start_flag.alignTransform.get()
        flag_align_grp.setParent(flag_grp)
        chain_fk[0].setParent(nt_grp)

        # Create the IK Chain ########################
        # Duplicate chain and set up the fk chain
        chain_ik = joint_utils.duplicate_chain(start_joint, end_joint, suffix='ik_chain')
        chain_ik[0].setParent(nt_grp)
        chain_ik_result = ik_chain.ik_joint_chain(chain_ik[0],
                                                    chain_ik[-1],
                                                    side=side,
                                                    region=region,
                                                    scale=scale,
                                                    ik_flag_orient=ik_flag_orient,
                                                    ik_flag_pv_orient=ik_flag_pv_orient,
                                                    ik_flag_rotate_order=ik_flag_rotate_order)

        # Edit results
        ik = chain_ik_result['ik_handle']
        ik_align_group = chain_ik_result['ik_zero']
        ik_align_group.visibility.set(0)

        pv_flag = chain_ik_result['pv_flag']
        ik_flag = chain_ik_result['ik_flag']
        ik_flag_offset = chain_ik_result['ik_flag_offset']
        pv_line = chain_ik_result['pv_line']
        line_clusters = chain_ik_result['line_clusters']
        ik_solver = chain_ik_result['ik_solver']
        unit_conv_nodes = chain_ik_result['unit_conv_nodes']

        # Transfer attributes
        end_joint.setAttr('side', ik_flag.getAttr('side'))
        end_joint.setAttr('type', ik_flag.getAttr('type'))
        end_joint.setAttr('otherType', ik_flag.getAttr('otherType'))

        end_joint.setAttr('side', ik_flag_offset.getAttr('side'))
        end_joint.setAttr('type', ik_flag_offset.getAttr('type'))
        end_joint.setAttr('otherType', ik_flag_offset.getAttr('otherType'))

        pv_flag.setAttr('side', ik_flag.getAttr('side'))
        pv_flag.setAttr('type', ik_flag.getAttr('type'))
        pv_flag.setAttr('otherType', ik_flag.getAttr('otherType'))


        pv_flag.visibility >> pv_line.visibility
        pv_flag.overrideVisibility >> pv_line.overrideVisibility
        pv_flag.overrideEnabled >> pv_line.overrideEnabled

        # Create IKFK Switch
        switch_joint = None
        if len(chain_between) == 3:
            switch_joint = chain_between[-1]
        if len(chain_between) == 4:
            switch_joint = chain_between[-2]

        ikfk_switch_result = ikfk_switch.ikfk_switch(switch_joint, side, region, scale=scale)
        invert_node = ikfk_switch_result['invert_node']
        switch_flag = ikfk_switch_result['flag']
        switch_attr_name = ikfk_switch_result['name']

        # visibility switching
        invert_node.straight >> ik_flag.v
        invert_node.straight >> ik_flag_offset.v
        invert_node.straight >> pv_flag.v
        for fk_flag in chain_fk_result['flags']:
            invert_node.inverse >> fk_flag.v
            fk_flag.v.lock()
        invert_node.inverse >> fk_flag_offset.v

        # Organize the groups
        ik_align_grp = ik_flag.alignTransform.get()
        pv_align_grp = pv_flag.alignTransform.get()
        switch_align_grp = switch_flag.alignTransform.get()

        pm.parent([pv_line, ik_align_group], nt_grp)
        pm.parent([ik_align_grp, pv_align_grp, switch_align_grp], flag_grp)

        # visibility setting, allows pv line to be seen
        chain_fk[0].v.set(0)
        chain_ik[0].v.set(0)
        nt_grp.v.unlock()
        nt_grp.v.set(1)
        nt_grp.v.lock()

        # lock attributes
        ik_flag.lock_and_hide_attrs(['sx', 'sy', 'sz', 'v'])
        ik_flag_offset.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        pv_flag.lock_and_hide_attrs(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        switch_flag.lock_and_hide_attrs(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'radius', 'v'])
        fk_flags[1].lock_and_hide_attrs(['rx', 'ry'])
        fk_flag_offset.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])

        # Meta Connections
        node.connect_nodes(chain_ik, 'ikChain', 'fragParent')
        node.connect_node(ik_flag, 'ikFlag', 'fragParent')
        node.connect_node(ik_flag_offset, 'ikFlagOffset', 'fragParent')
        node.connect_node(pv_flag, 'pvFlag', 'fragParent')
        node.connect_node(fk_flag_offset, 'fkFlagOffset', 'fragParent')
        node.connect_node(pv_line, 'pvLine', 'fragParent')
        node.connect_node(ik, 'ik_handle', 'fragParent')
        node.addAttr('switchAttrName', dt='string')
        node.attr('switchAttrName').set(switch_attr_name)
        node.connect_node(switch_flag, 'switchFlag', 'fragParent')
        node.connect_node(invert_node, 'invert_node', 'fragParent')
        node.connect_node(start_joint, 'start_joint')
        node.connect_node(end_joint, 'end_joint')
        node.connect_nodes(chain_between, 'bindJoints')
        node.connect_nodes(chain_fk, 'fkChain', 'fragParent')
        node.connect_nodes(fk_flags, 'fkFlags', 'fragParent')
        node.connect_nodes(line_clusters, 'lineClusters', 'fragParent')
        node.connect_nodes(unit_conv_nodes, 'unitConvNodes', 'fragParent')
        node.connect_node(ik_solver, 'ikSolver', 'fragParent')

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

        return node

    def get_flags(self):
        flags = self.fkFlags.listConnections()
        flags.append(self.ikFlag.get())
        flags.append(self.ikFlagOffset.get())
        flags.append(self.fkFlagOffset.get())
        flags.append(self.pvFlag.get())
        switch_flag = self.switchFlag.get()
        if switch_flag and switch_flag not in flags:
            flags.append(switch_flag)
        return [frag_flag.Flag(x) for x in flags]

    @property
    def fk_flags(self):
        flags = self.fkFlags.listConnections()
        return list(map(lambda x: frag_flag.Flag(x), flags))

    @property
    def ik_flags(self):
        flags = [self.ikFlag.get(), self.ikFlagOffset.get(), self.pvFlag.get()]
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

    @property
    def ik_flag(self):
        return frag_flag.Flag(self.ikFlag.get())

    @property
    def ik_flag_offset(self):
        return frag_flag.Flag(self.ikFlagOffset.get())

    @property
    def fk_flag_offset(self):
        return frag_flag.Flag(self.fkFlagOffset.get())

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

        fk_flag_list = self.fk_flags
        ik_flag_list = [self.ik_flag, self.pv_flag]

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
            if fk_flag_list and len(fk_flag_list) <= len(joint_list):
                # fk constraints
                for flag_node, joint_node in list(
                        zip(fk_flag_list, joint_list)):
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
                constraint_node = constraint.parent_constraint_safe(pv_locator, ik_flag_list[-1], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

        return constraint_list

