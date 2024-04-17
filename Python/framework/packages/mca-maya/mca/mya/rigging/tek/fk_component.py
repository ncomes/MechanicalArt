#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
FK Component
"""

# System global imports

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common.utils import lists

from mca.mya.modifiers import ma_decorators

from mca.mya.utils import attr_utils, constraint, dag, namespace

from mca.mya.rigging import chain_markup, fk_chain
from mca.mya.rigging.flags import tek_flag
from mca.mya.rigging import joint_utils
# internal module imports
from mca.mya.rigging.tek import keyable_component
from mca.mya.utils import namespace


class FKComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
               start_joint,
               end_joint,
               side,
               region,
               scale=1.0,
               flag_group_pivot=None,
               lock_child_rotate_axes=(),
               lock_child_translate_axes=attr_utils.TRANSLATION_ATTRS,
               lock_child_scale_axes=attr_utils.SCALE_ATTRS,
               lock_root_rotate_axes=(),
               lock_root_translate_axes=attr_utils.TRANSLATION_ATTRS,
               lock_root_scale_axes=attr_utils.SCALE_ATTRS,
               children_align_transforms=True,
               constrain_translate=True,
               constrain_rotate=True,
               constrain_scale=False,
               offset_flag=False, **kwargs):
        
        """
        Creates a FK Component.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param pm.nt.DagNode flag_group_pivot: Aligns all the group nodes to an object.
        :param list(str) lock_child_rotate_axes: Axis to lock.
        :param list(str) lock_child_translate_axes: Axis to lock.
        :param list(str) lock_child_scale_axes: Axis to lock.
        :param list(str) lock_root_rotate_axes: Axis to lock.
        :param list(str) lock_root_translate_axes: Axis to lock.
        :param list(str) lock_root_scale_axes: Axis to lock.
        :param children_align_transforms: Aligns the align_transform node to an object.
        :param bool constrain_translate: If true, it will constrain the new joint chain to the existing in translate.
        :param bool constrain_rotate: If true, it will constrain the new joint chain to the existing in rotate.
        :param bool constrain_scale: If true, it will constrain the new joint chain to the existing in scale.
        :return: Returns an instance of FKComponent.
        :rtype: FKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['flag_group_pivot'] = flag_group_pivot.name() if flag_group_pivot else None
        kwargs_dict['lock_child_rotate_axes'] = lock_child_rotate_axes
        kwargs_dict['lock_child_translate_axes'] = lock_child_translate_axes
        kwargs_dict['lock_child_scale_axes'] = lock_child_scale_axes
        kwargs_dict['lock_root_rotate_axes'] = lock_root_rotate_axes
        kwargs_dict['lock_root_translate_axes'] = lock_root_translate_axes
        kwargs_dict['lock_root_scale_axes'] = lock_root_scale_axes
        kwargs_dict['allow_scale'] = constrain_scale
        kwargs_dict['children_align_transforms'] = children_align_transforms
        kwargs_dict['constrain_translate'] = constrain_translate
        kwargs_dict['constrain_rotate'] = constrain_rotate
        kwargs_dict['offset_flag'] = offset_flag

        lock_child_translate_axes = list(lock_child_translate_axes)
        lock_child_rotate_axes = list(lock_child_rotate_axes)
        lock_child_scale_axes = list(lock_child_scale_axes)
        lock_root_rotate_axes = list(lock_root_rotate_axes)
        lock_root_translate_axes = list(lock_root_translate_axes)
        lock_root_scale_axes = list(lock_root_scale_axes)

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        namespace.set_namespace(root_namespace, check_existing=False)

        node = keyable_component.KeyableComponent.create(tek_parent,
                                                            FKComponent.__name__,
                                                            FKComponent.VERSION,
                                                            side=side,
                                                            region=region,
                                                            align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        if pm.xform(start_joint, q=True, ws=True, t=True)[0] < 0:
            # Align flag group to the start joint this helps with multi parent attachments.
            # This seems to be an error with how Maya identifies objects in the -x space.
            # Honestly this feels like a Maya bug but. Or possibly something to do with gimbal lock.
            pm.delete(constraint.parent_constraint_safe(start_joint, flag_grp))
        nt_grp = node.noTouch.get()

        # Check to see if we want to move all groups to an object
        if flag_group_pivot:
            pm.delete(pm.parentConstraint(flag_group_pivot, flag_grp, w=True, mo=False))

        # Duplicate chain and set up the fk chain
        chain_fk = joint_utils.duplicate_chain(start_joint, end_joint, suffix='fk_chain')
        chain_fk[0].setParent(nt_grp)
        chain_fk_result = fk_chain.fk_joint_chain(chain_fk[0],
                                                  chain_fk[-1],
                                                  scale=scale,
                                                  children_align_transforms=children_align_transforms,
                                                  create_end_flag=True,
                                                  offset_flag=offset_flag,
                                                  use_scale=constrain_scale)

        start_flag = chain_fk_result['flags'][0]
        new_offset_flag = chain_fk_result['offset_flag']
        if new_offset_flag:
            new_offset_flag.lock_and_hide_attrs(['v']+lock_child_translate_axes+lock_child_rotate_axes+lock_child_scale_axes)
        flag_align_transform = start_flag.alignTransform.get()
        if flag_align_transform:
            flag_align_transform.setParent(flag_grp)
        else:
            start_flag.setParent(flag_grp)

        node.connect_nodes(chain_fk_result['flags'], 'fkFlags', 'tekParent')
        node.connect_nodes(chain_fk, 'chainFk', 'tekParent')
        node.connect_nodes(chain_between, 'bindJoints')

        node.addAttr('offsetFlag', at='message')
        if offset_flag:
            node.connect_nodes(new_offset_flag, 'offsetFlag', 'tekParent')

        ctrls = chain_fk_result['flags']
        for x in range(len(ctrls)):
            locked_attrs = ['v']
            if x == 0:
                locked_attrs = locked_attrs + lock_root_rotate_axes + lock_root_translate_axes + lock_root_scale_axes
            elif x > 0:
                locked_attrs = locked_attrs + lock_child_rotate_axes + lock_child_translate_axes + lock_child_scale_axes

            attr_utils.lock_and_hide_attrs(ctrls[x], locked_attrs)

        # Check Constraints
        for x, joint_node in enumerate(chain_fk_result['chain']):
            if constrain_translate and constrain_rotate:
                pm.parentConstraint(joint_node, chain_between[x])
            elif constrain_translate and not constrain_rotate:
                pm.pointConstraint(joint_node, chain_between[x])
            elif not constrain_translate and constrain_rotate:
                pm.orientConstraint(joint_node, chain_between[x])
            if constrain_scale:
                # Use a direct attr connection it handles scaled parents better than a scale constraint.
                joint_node.s >> chain_between[x].s

        node.set_scale()

        return node

    def get_flags(self):
        """
        Returns all the flags connected to the component.

        :return: Returns all the flags connected to the component.
        :rtype: list(tek_flag.Flag)
        """

        flags = self.fkFlags.listConnections()
        flags = list(map(lambda x: tek_flag.Flag(x), flags))
        return flags

    def get_start_flag(self):
        """
        Returns the first flag connected to the component.

        :return: Returns the first flag connected to the component.
        :rtype: tek_flag.Flag
        """

        flags = self.get_flags()
        return flags[-1]

    def get_offset_flag(self):
        """
        Returns the offset flag connected to the component.

        :return: Returns the offset flag connected to the component.
        :rtype: tek_flag.Flag
        """

        _flag = self.offsetFlag.get()
        if _flag:
            return _flag
        return

    def get_end_flag(self):
        """
        Returns the end flag connected to the component.

        :return: Returns the end flag connected to the component.
        :rtype: tek_flag.Flag
        """

        flags = self.get_flags()
        return flags[0]

    def select_flags(self):
        """
        Selected all the flags.
        """

        pm.select(self.get_flags())

    def key_flags(self):
        """
        Sets a keyframe on all the flags in the scene
        """

        flags = self.get_flags()
        pm.setKeyframe(flags)

    def to_default_pose(self):
        """
        Sets all the flags to there default position.
        """

        flags = self.get_flags()
        for _flag in flags:
            attr_utils.reset_attrs(_flag)

    @ma_decorators.keep_namespace_decorator
    def set_scale(self):
        """
        Use the inverse scale value to adjust the build group.

        """

        if not self.pynode.hasAttr('buildKwargs_allow_scale') or not self.pynode.getAttr('buildKwargs_allow_scale'):
            # If the FK component is not meant to scale do not setup scale for this component.
            return

        rig_namespace = self.namespace()
        tek_rig = self.get_tek_parent()

        namespace.set_namespace(rig_namespace)
        multi_node = lists.get_first_in_list(pm.ls(f'{rig_namespace}:rig_scale_multi', r=True, type=pm.nt.MultiplyDivide))
        if not multi_node:
            multi_node = pm.createNode(pm.nt.MultiplyDivide, n='rig_scale_multi')

        multi_node.input1X.set(1)
        multi_node.operation.set(2)

        multi_node.input2X.disconnect()
        tek_rig.rigScale >> multi_node.input2X

        nt_grp = self.no_touch_grp
        for axis in attr_utils.SCALE_ATTRS:
            nt_grp.attr(axis).disconnect()
            nt_grp.attr(axis).unlock()
            multi_node.outputX >> nt_grp.attr(axis)

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

        flag_list = self.get_flags()
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
            if flag_list and len(flag_list) <= len(joint_list):
                for flag_node, joint_node in list(
                        zip(flag_list, joint_list)):
                    constraint_node = constraint.parent_constraint_safe(joint_node, flag_node, mo=mo)
                    for attr_name in attr_utils.SCALE_ATTRS:
                        if flag_node.attr(attr_name).isSettable():
                            joint_node.attr(attr_name) >> flag_node.attr(attr_name)
                    if constraint_node:
                        constraint_list.append(constraint_node)
        return constraint_list
