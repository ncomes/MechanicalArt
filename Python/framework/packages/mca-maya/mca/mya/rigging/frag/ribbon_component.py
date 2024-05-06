#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ribbon rigging component. This is often driven with a ik/fk switching chain.
"""

# System global imports
import math
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists, pymaths
from mca.mya.utils import attr_utils, constraint, dag, namespace, naming
from mca.mya.modifiers import ma_decorators
from mca.mya.modeling import follicle
from mca.mya.rigging import chain_markup, fk_chain, ik_chain, ik_utils, ikfk_switch, joint_utils, ribbon_setup, rig_utils
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class IKFKRibbonComponent(keyable_component.KeyableComponent):
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
                                                         IKFKRibbonComponent.__name__,
                                                         IKFKRibbonComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Create the ribbon drive chain
        chain_ribbon = joint_utils.duplicate_chain(start_joint, end_joint, suffix='ribbon_chain')
        chain_ribbon[0].setParent(nt_grp)

        # Attach ribbon drivers to original joints.
        detail_flags = []
        for original_joint, chain_ribbon_joint in zip(chain_between, chain_ribbon):
            if original_joint != chain_between[-1]:
                chain_fk_result = fk_chain.fk_joint_chain(original_joint,
                                                          original_joint,
                                                          scale=scale*.85,
                                                          create_end_flag=True)
                detail_flag = chain_fk_result['flags'][0]
                detail_flag.set_as_detail()
                align_transform = detail_flag.get_align_transform()
                align_transform.setParent(flag_grp)
                constraint.parent_constraint_safe(chain_ribbon_joint, align_transform)
                detail_flags.append(detail_flag)
            else:
                constraint.point_constraint_safe(chain_ribbon_joint, original_joint)

        list_length = len(chain_ribbon)

        ribbon_node = ribbon_setup.create_ribbon_along_nodes(chain_ribbon)
        ribbon_group = pm.group(n=f'ribbon_group_{side}_{region}', em=True, w=True)
        ribbon_group.setParent(nt_grp.getParent())
        ribbon_node.setParent(ribbon_group)
        ribbon_node.v.set(False)
        ribbon_shape = ribbon_node.getShape()

        # create fk/ik joint chain based on ribbon chain
        ribbon_start = joint_utils.duplicate_joint(chain_ribbon[0], 'chain_ribbon_start')
        ribbon_start.setParent(nt_grp)
        ribbon_mid = joint_utils.duplicate_joint(chain_ribbon[math.floor(list_length/2)], 'chain_ribbon_mid')
        ribbon_mid.setParent(ribbon_start)
        ribbon_end = joint_utils.duplicate_joint(chain_ribbon[list_length-1], 'chain_ribbon_end')
        ribbon_end.setParent(ribbon_mid)
        constraint.orient_constraint_safe(ribbon_end, chain_between[-1])

        ribbon_simp_list = [ribbon_start, ribbon_mid, ribbon_end]

        pm.makeIdentity([ribbon_start, ribbon_mid, ribbon_end], t=True, r=True, s=True, n=False, pn=True, apply=True)

        # skin ribbon
        skin_cluster_node = pm.skinCluster(ribbon_node, [ribbon_start, ribbon_mid, ribbon_end], tsb=True,
                                           normalizeWeights=1, maximumInfluences=3,
                                           obeyMaxInfluences=True, removeUnusedInfluence=False)

        # add follicles and adjust the skin weights
        follicle_group = pm.group(n='ribbon_follicles', em=True, w=True)
        follicle_group.setParent(nt_grp)
        previous_v_pos = 0
        for index, joint_node in enumerate(chain_ribbon):
            pos = pm.xform(joint_node, q=True, ws=True, t=True)
            new_follicle = follicle.create_surface_follicle(ribbon_node, hide_follicle=False)
            v_pos = ribbon_shape.closestPoint(pos, space='world')[-1]
            new_follicle[-1].parameterU.set(.5)
            new_follicle[-1].parameterV.set(v_pos)
            new_follicle[0].setParent(follicle_group)
            constraint.parent_constraint_safe(new_follicle[0], joint_node, mo=True)

            blend_joint = ribbon_start if index <= math.floor(list_length / 2) else ribbon_end

            if index:
                # If not the first.
                v_mid = previous_v_pos + (v_pos - previous_v_pos) / 2
                if index <= math.floor(list_length / 2):
                    middle_influence = v_pos * 2
                    blend_influence = 1 - middle_influence

                    mid_middle_influence = v_mid * 2
                    mid_blend_influence = 1 - mid_middle_influence
                    # First Half
                    # Moving towards the mid joint
                    mid_influence_list = [(ribbon_mid, mid_middle_influence), (blend_joint, mid_blend_influence)]
                    influence_list = [(ribbon_mid, middle_influence), (blend_joint, blend_influence)]
                else:
                    middle_influence = (1 - v_pos) * 2
                    blend_influence = 1 - middle_influence

                    mid_middle_influence = (1 - v_mid) * 2
                    mid_blend_influence = 1 - mid_middle_influence
                    # Second Half
                    # Moving away frm the mid joint
                    mid_influence_list = [(ribbon_mid, mid_middle_influence), (blend_joint, mid_blend_influence)]
                    influence_list = [(ribbon_mid, middle_influence), (blend_joint, blend_influence)]
            if not index:
                # If the first
                influence_list = [(ribbon_start, 1)]
            elif index + 1 == list_length:
                # If the last
                influence_list = [(ribbon_end, 1)]
            for i in range(4):
                pm.skinPercent(skin_cluster_node, ribbon_node.cv[i][index * 2], transformValue=influence_list)

                if index:
                    pm.skinPercent(skin_cluster_node, ribbon_node.cv[i][index * 2 - 1], transformValue=mid_influence_list)

            previous_v_pos = v_pos

        # Setup fk chain
        chain_fk = joint_utils.duplicate_chain(ribbon_start, ribbon_end, suffix='fk_chain')
        chain_fk[0].setParent(nt_grp)
        chain_fk_result = fk_chain.fk_joint_chain(chain_fk[0],
                                                  chain_fk[-1],
                                                  children_align_transforms=True,
                                                  create_end_flag=True,
                                                  offset_flag=True)

        # Lock Attributes
        fk_flags = chain_fk_result['flags']
        fk_flag_offset = chain_fk_result['offset_flag']
        [x.v.set(keyable=False, channelBox=False) for x in fk_flags]

        attrs_to_lock = ['sx', 'sy', 'sz'] + list(lock_root_translate_axes)
        fk_flags[0].lock_and_hide_attrs(attrs_to_lock)

        # chain_ribbon.pop(0)
        attrs_to_lock = attrs_to_lock + list(lock_child_rotate_axes) + list(lock_child_translate_axes)
        [x.lock_and_hide_attrs(attrs_to_lock) for x in fk_flags if x != fk_flags[0]]

        # Organize groups
        start_flag = fk_flags[0]
        flag_align_grp = start_flag.alignTransform.get()
        flag_align_grp.setParent(flag_grp)
        chain_fk[0].setParent(nt_grp)

        # Create the IK Chain ########################
        # Duplicate chain and set up the fk chain
        chain_ik = joint_utils.duplicate_chain(ribbon_start, ribbon_end, suffix='ik_chain')
        chain_ik[0].setParent(nt_grp)
        chain_ik_result = ik_chain.ik_joint_chain(chain_ik[0],
                                                  chain_ik[-1],
                                                  side=side,
                                                  region=region,
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
        if len(ribbon_simp_list) == 3:
            switch_joint = ribbon_simp_list[-1]
        if len(ribbon_simp_list) == 4:
            switch_joint = ribbon_simp_list[-2]

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

        ik_align_group.setParent(nt_grp)
        pv_line.setParent(ribbon_group)
        pm.parent([ik_align_grp, pv_align_grp, switch_align_grp], flag_grp)

        # visibility setting, allows pv line to be seen
        chain_fk[0].v.set(0)
        chain_ik[0].v.set(0)

        # lock attributes
        ik_flag.lock_and_hide_attrs(['sx', 'sy', 'sz', 'v'])
        ik_flag_offset.lock_and_hide_attrs(['tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'v'])
        pv_flag.lock_and_hide_attrs(['rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'])
        switch_flag.lock_and_hide_attrs(['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'radius', 'v'])
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
        node.connect_nodes(detail_flags, 'detailFlags', 'fragParent')
        node.connect_node(skin_cluster_node, 'ribbonSkinCluster', 'fragParent')

        # Make the ik joints and fk joints control the base joints
        for x in range(len(ribbon_simp_list)):
            orientConst = pm.orientConstraint(chain_fk[x], chain_ik[x], ribbon_simp_list[x], w=1, mo=0)
            pointConst = pm.pointConstraint(chain_fk[x], chain_ik[x], ribbon_simp_list[x], w=1, mo=1)

            # IK
            invert_node.straight >> orientConst.getWeightAliasList()[1]
            invert_node.straight >> pointConst.getWeightAliasList()[1]
            # FK
            invert_node.inverse >> orientConst.getWeightAliasList()[0]
            invert_node.inverse >> pointConst.getWeightAliasList()[0]

        node.set_scale()

        return node

    def get_flags(self):
        flags = self.fkFlags.listConnections()
        flags.append(self.ikFlag.get())
        flags.append(self.ikFlagOffset.get())
        flags.append(self.fkFlagOffset.get())
        flags.append(self.pvFlag.get())
        flags += self.detailFlags.listConnections()
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
    def detail_flags(self):
        flags = self.detailFlags.listConnections()
        return list(map(lambda x: frag_flag.Flag(x), flags))

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
        detail_flag_list = self.detail_flags

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
            for detail_flag, joint_node in zip(detail_flag_list, joint_list):
                constraint_node = constraint.parent_constraint_safe(joint_node, detail_flag, mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

            if fk_flag_list:
                fk_joint_list = self.ikChain.get()
                for fk_flag, fk_joint in zip(fk_flag_list, fk_joint_list):
                    constraint_node = constraint.parent_constraint_safe(fk_joint, fk_flag, mo=mo)
                    if constraint_node:
                        constraint_list.append(constraint_node)

            if ik_flag_list:
                # ik constraints
                constraint_node = constraint.parent_constraint_safe(joint_list[-1], ik_flag_list[0], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

                pv_locator = ik_utils.create_pole_vector_locator(joint_list[:3])
                pv_locator.setParent(joint_list[math.floor(len(joint_list)/2)])
                pv_locator.addAttr('bake_helper', at=bool, dv=True)
                constraint_node = constraint.parent_constraint_safe(pv_locator, ik_flag_list[-1], mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

        return constraint_list

    @ma_decorators.keep_namespace_decorator
    def set_scale(self):
        """
        Use the inverse scale value to adjust the build group.

        """
        rig_namespace = self.namespace()
        frag_rig = self.get_frag_parent()

        namespace.set_namespace(rig_namespace)
        multi_node = lists.get_first_in_list(pm.ls(f'{rig_namespace}:rig_scale_multi', r=True, type=pm.nt.MultiplyDivide))
        if not multi_node:
            multi_node = pm.createNode(pm.nt.MultiplyDivide, n='rig_scale_multi')

        multi_node.input1X.set(1)
        multi_node.operation.set(2)

        multi_node.input2X.disconnect()
        frag_rig.rigScale >> multi_node.input2X

        ribbon_grp = self.pvLine.get().getParent()

        for axis in attr_utils.SCALE_ATTRS:
            ribbon_grp.attr(axis).disconnect()
            ribbon_grp.attr(axis).unlock()
            multi_node.outputX >> ribbon_grp.attr(axis)

    def remove(self):
        ribbon_grp = self.ribbon.get().getParent()
        pm.delete([self.no_touch_grp, self.flag_group, ribbon_grp, self.pynode])


class SplineIKRibbonComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
               start_joint,
               end_joint,
               side,
               region,
               scale=1.0,
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
        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                         SplineIKRibbonComponent.__name__,
                                                         SplineIKRibbonComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)
        skel_hierarchy = chain_markup.ChainMarkup(start_joint.getParent())

        wrapped_joint = chain_markup.JointMarkup(start_joint)
        joint_side = wrapped_joint.side
        joint_region = wrapped_joint.region

        mid_helper_joint = skel_hierarchy.get_start(f'{joint_region}_mid', joint_side) or skel_hierarchy.get_start(f'{joint_region}_helper', joint_side)
        if mid_helper_joint and not mid_helper_joint.hasAttr('twist'):
            mid_helper_joint.addAttr('twist', keyable=True)
        rig_mid_helper_joint = joint_utils.duplicate_joint(mid_helper_joint, f'{side}_{region}_mid')
        rig_mid_helper_joint.setParent(nt_grp)
        constraint.parent_constraint_safe(rig_mid_helper_joint, mid_helper_joint)

        end_helper_joint = skel_hierarchy.get_start(f'{joint_region}_end', joint_side)
        rig_end_helper_joint = joint_utils.duplicate_joint(end_helper_joint, f'{side}_{region}_end')
        rig_end_helper_joint.setParent(nt_grp)
        constraint.parent_constraint_safe(rig_end_helper_joint, end_helper_joint)

        primary_axis, is_positive = rig_utils.find_primary_axis(chain_between[1])

        # Create the ribbon drive chain
        ribbon_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='ribbon_chain')
        ribbon_chain[0].setParent(nt_grp)

        ribbon_group = pm.group(n=f'ribbon_group_{side}_{region}', em=True, w=True)
        # Need to set the splineik_chain in the ribbon group to allow for scaling of the component.
        splineik_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='splineik_chain')
        splineik_chain[0].setParent(ribbon_group)

        # Attach ribbon drivers to original joints.
        detail_flags = []
        for original_joint, ribbon_joint, splineik_joint in zip(chain_between, ribbon_chain, splineik_chain):
            if original_joint not in [chain_between[0], chain_between[-1]]:
                chain_fk_result = fk_chain.fk_joint_chain(original_joint,
                                                          original_joint,
                                                          scale=scale * .85,
                                                          create_end_flag=True)
                detail_flag = chain_fk_result['flags'][0]
                detail_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
                detail_flag.set_as_detail()
                align_transform = detail_flag.get_align_transform()
                align_transform.setParent(flag_grp)
                # constraint.parent_constraint_safe(splineik_joint, align_transform)
                constraint.parent_constraint_safe(detail_flag, ribbon_joint)

                constraint.parent_constraint_safe(ribbon_joint, original_joint)
                detail_flags.append(detail_flag)

        list_length = len(ribbon_chain)

        ribbon_node = ribbon_setup.create_ribbon_along_nodes(ribbon_chain)
        ribbon_group.setParent(nt_grp.getParent())
        ribbon_group.v.set(False)
        ribbon_node.setParent(ribbon_group)
        ribbon_shape = ribbon_node.getShape()

        # create fk/ik joint chain based on ribbon chain
        ribbon_start = joint_utils.duplicate_joint(ribbon_chain[0], 'chain_ribbon_start')
        ribbon_start.setParent(nt_grp)
        constraint.parent_constraint_safe(ribbon_start, start_joint)
        ribbon_mid = joint_utils.duplicate_joint(ribbon_chain[math.floor(list_length / 2)], 'chain_ribbon_mid')
        ribbon_mid.setParent(nt_grp)
        constraint.parent_constraint_safe(ribbon_mid, rig_mid_helper_joint)
        ribbon_end = joint_utils.duplicate_joint(ribbon_chain[list_length - 1], 'chain_ribbon_end')
        ribbon_end.setParent(nt_grp)
        constraint.parent_constraint_safe(ribbon_end, end_joint)
        constraint.parent_constraint_safe(ribbon_end, rig_end_helper_joint)
        #constraint.orient_constraint_safe(ribbon_chain, chain_between[-1])

        ribbon_simp_list = [ribbon_start, ribbon_mid, ribbon_end]

        pm.makeIdentity([ribbon_start, ribbon_mid, ribbon_end], t=True, r=True, s=True, n=False, pn=True, apply=True)

        # skin ribbon
        ribbon_skin_cluster = pm.skinCluster(ribbon_node, splineik_chain, tsb=True,
                       normalizeWeights=1, maximumInfluences=3,
                       obeyMaxInfluences=True, removeUnusedInfluence=False)

        # add follicles and adjust the skin weights
        follicle_group = pm.group(n='ribbon_follicles', em=True, w=True)
        follicle_group.setParent(nt_grp)
        for index, (joint_node, detail_flag) in enumerate(zip(ribbon_chain[1:-1], detail_flags)):
            pos = pm.xform(joint_node, q=True, ws=True, t=True)
            new_follicle = follicle.create_surface_follicle(ribbon_node, hide_follicle=False)
            v_pos = ribbon_shape.closestPoint(pos, space='world')[-1]
            new_follicle[-1].parameterU.set(.5)
            new_follicle[-1].parameterV.set(v_pos)
            new_follicle[0].setParent(follicle_group)
            constraint.parent_constraint_safe(new_follicle[0], detail_flag.get_align_transform(), mo=True)

        # create curve
        # When generating the curve there are two additional points added approx 2/3 of the distance between the first
        # two and last two points
        curve_pt_list = []
        for joint_node in ribbon_simp_list:
            pos = pm.xform(joint_node, q=True, ws=True, t=True)
            curve_pt_list.append(pos)

        v1 = pymaths.sub_vectors(*reversed(curve_pt_list[0:2]))
        v1_mod = pymaths.scale_vector(v1, .33)
        v1_float = pymaths.add_vectors(curve_pt_list[0], v1_mod)
        curve_pt_list.insert(1, v1_float)

        v2 = pymaths.sub_vectors(*reversed(curve_pt_list[-2:]))
        v2_mod = pymaths.scale_vector(v2, .666)
        v2_float = pymaths.add_vectors(curve_pt_list[-2], v2_mod)
        curve_pt_list.insert(-1, v2_float)

        # for a deg 3 curve the first 3 knots and last 3 nots are repeated.
        knot_list = [0, 0, 0, 1, 2, 2, 2]
        spline_curve = pm.curve(n=f'{side}_{region}_curve', p=curve_pt_list, k=knot_list)
        # If the rig is scaled we should not scale a driver object let it hang out with the ribbon.
        spline_curve.setParent(ribbon_group)

        # setup spline IK
        spline_ik_handle, end_effector = pm.ikHandle(sol='ikSplineSolver', ccv=False, roc=False, pcv=False, ns=2,
                                                     startJoint=splineik_chain[0], endEffector=splineik_chain[-1],
                                                     curve=spline_curve)
        spline_ik_handle.rename(f'{side}_{region}_ikspline_handle')
        spline_ik_handle.setParent(nt_grp)
        pm.ikHandle(spline_ik_handle, e=True, solver='ikSplineSolver')

        curve_skin_cluster = pm.skinCluster(spline_curve, [ribbon_start, ribbon_mid, ribbon_end], tsb=True,
                                           normalizeWeights=1, maximumInfluences=3,
                                           obeyMaxInfluences=True, removeUnusedInfluence=False)

        # setup stretch
        info_node = pm.createNode("curveInfo", n=f'{region}_{side}_curve_info')
        spline_curve.getShape().worldSpace >> info_node.inputCurve
        multi_nodes = []
        stretch_multi_node = pm.createNode("multiplyDivide", n=f'{region}_{side}_multi_stretch')
        multi_nodes.append(stretch_multi_node)
        stretch_multi_node.setAttr('input2X', info_node.getAttr('arcLength'))
        info_node.arcLength >> stretch_multi_node.input1X
        stretch_multi_node.setAttr('operation', 2)
        for joint_node in splineik_chain:
            multi_node = pm.createNode("multiplyDivide", n=f'{naming.get_basename(joint_node)}_multi_stretch')
            multi_nodes.append(multi_node)
            multi_node.setAttr('input1X', joint_node.getAttr(f't{primary_axis}'.lower()))
            stretch_multi_node.outputX >> multi_node.input2X
            multi_node.outputX >> joint_node.attr(f't{primary_axis}'.lower())

        # setup primary controls
        primary_flags = []
        for joint_node, identifier in zip(ribbon_simp_list, ['start', 'mid', 'end']):
            primary_flag = frag_flag.Flag.create(joint_node, label=f'{side}_{region}_{identifier}', scale=scale)
            primary_flag.get_align_transform().setParent(flag_grp)
            constraint.parent_constraint_safe(primary_flag, joint_node, mo=True)
            primary_flag.lock_and_hide_attrs(attr_utils.SCALE_ATTRS)
            primary_flags.append(primary_flag)

            if identifier == 'end':
                primary_flag.node.addAttr('twist', keyable=True)
                primary_flag.node.twist >> spline_ik_handle.twist
                primary_flag.node.twist >> mid_helper_joint.twist
        ribbon_tweak = ribbon_shape.listConnections(type=pm.nt.Tweak)[0]
        make_plane_node = [x for x in ribbon_shape.listHistory() if isinstance(x, pm.nt.MakeNurbPlane)]
        spline_solver = spline_ik_handle.ikSolver.get()
        unit_conversion_node = primary_flags[-1].listConnections(type=pm.nt.UnitConversion)

        # Meta Connections
        node.connect_node(start_joint, 'start_joint')
        node.connect_node(end_joint, 'end_joint')
        node.connect_nodes(chain_between, 'bindJoints')
        node.connect_nodes(detail_flags, 'detailFlags', 'fragParent')
        node.connect_nodes(primary_flags, 'flags', 'fragParent')
        node.connect_node(ribbon_node, 'ribbon', 'fragParent')
        node.connect_node(spline_ik_handle, 'ikHandle', 'fragParent')
        node.connect_node(info_node, 'infoNode', 'fragParent')
        node.connect_nodes(multi_nodes, 'multiNodes', 'fragParent')
        node.connect_nodes([ribbon_skin_cluster, curve_skin_cluster], 'ribbonSkinCluster', 'fragParent')
        node.connect_node(ribbon_tweak, 'ribbonTweak', 'fragParent')
        node.connect_nodes(make_plane_node, 'makePlaneNode', 'fragParent')
        node.connect_node(spline_solver, 'ikSolver', 'fragParent')
        node.connect_nodes(unit_conversion_node, 'unitConvNodes', 'fragParent')

        node.set_scale()

        return node

    def get_flags(self):
        flags = self.pynode.flags.get()
        flags += self.pynode.detailFlags.get()
        return [frag_flag.Flag(x) for x in flags]

    @property
    def primary_flags(self):
        flags = self.pynode.flags.get()
        return list(map(lambda x: frag_flag.Flag(x), flags))

    @property
    def detail_flags(self):
        flags = self.pynode.detailFlags.get()
        return list(map(lambda x: frag_flag.Flag(x), flags))

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

        primary_flag_list = self.get_flags()
        detail_flag_list = self.detail_flags

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
        mid_helper_joint = target_root_hierarchy.get_start(f'{skel_region}_mid', skel_side) or target_root_hierarchy.get_start(f'{skel_region}_helper', skel_side)
        end_helper_joint = target_root_hierarchy.get_start(f'{skel_region}_end', skel_side)
        if joint_list:
            for detail_flag, joint_node in zip(detail_flag_list, joint_list[1:-1]):
                constraint_node = constraint.parent_constraint_safe(joint_node, detail_flag, mo=mo)
                if constraint_node:
                    constraint_list.append(constraint_node)

        if primary_flag_list:
            constraint_list.append(constraint.parent_constraint_safe(joint_list[0], primary_flag_list[0], mo=mo))
            constraint_list.append(constraint.parent_constraint_safe(mid_helper_joint, primary_flag_list[1], mo=mo))
            if mid_helper_joint.hasAttr('twist'):
                mid_helper_joint.twist >> primary_flag_list[2].node.twist
            constraint_list.append(constraint.parent_constraint_safe(end_helper_joint, primary_flag_list[2], mo=mo))
        return constraint_list

    def remove(self):
        ribbon_grp = self.ribbon.get().getParent()
        pm.delete([self.no_touch_grp, self.flag_group, ribbon_grp, self.pynode])

    @ma_decorators.keep_namespace_decorator
    def set_scale(self):
        """
        Use the inverse scale value to adjust the build group.

        """
        rig_namespace = self.namespace()
        frag_rig = self.get_frag_parent()

        namespace.set_namespace(rig_namespace)
        multi_node = lists.get_first_in_list(pm.ls(f'{rig_namespace}:rig_scale_multi', r=True, type=pm.nt.MultiplyDivide))
        if not multi_node:
            multi_node = pm.createNode(pm.nt.MultiplyDivide, n='rig_scale_multi')

        multi_node.input1X.set(1)
        multi_node.operation.set(2)

        multi_node.input2X.disconnect()
        frag_rig.rigScale >> multi_node.input2X

        ribbon_grp = self.ribbon.get().getParent()

        for axis in attr_utils.SCALE_ATTRS:
            ribbon_grp.attr(axis).disconnect()
            ribbon_grp.attr(axis).unlock()
            multi_node.outputX >> ribbon_grp.attr(axis)