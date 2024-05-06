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
from mca.mya.utils import attr_utils, constraint, dag, naming
from mca.mya.modeling import rivets
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils
from mca.mya.rigging import rig_utils, fk_chain, chain_markup
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component


class PinComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
               bind_joint,
               pin_mesh,
               side,
               region,
               lock_root_translate_axes=['tx', 'ty', 'tz'],
               **kwargs):
        """

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param Joint bind_joint: The joint to be used as the start of the pin component.
        :param Transform pin_mesh: The shaped transform the pin will be attached to.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param list[str] lock_root_translate_axes: A list of the string names of attrs which should be locked on the component's flags.
        :return: Returns an instance of PinComponent
        :rtype: PinComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['pin_mesh'] = pin_mesh
        kwargs_dict['side'] = side
        kwargs_dict['region'] = region
        kwargs_dict['lock_root_translate_axes'] = lock_root_translate_axes

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                         PinComponent.__name__,
                                                         PinComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=bind_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        pin_joint = joint_utils.duplicate_joint(bind_joint, duplicate_name=f'{naming.get_basename(bind_joint)}_pin')
        pin_joint.setParent(nt_grp)
        constraint.parent_constraint_safe(pin_joint, bind_joint)
        fk_result = fk_chain.fk_joint_chain(pin_joint,
                                            pin_joint,
                                            create_end_flag=True)

        pin_flag = frag_flag.Flag(fk_result['flags'][0])
        attr_utils.lock_and_hide_attrs(pin_flag, ['v']+lock_root_translate_axes)
        pin_align_transform = pin_flag.get_align_transform()

        pin_offset_grp = pm.group(em=True, w=True, n=f'{side}_{region}_pin_offset_grp')
        pin_offset_grp.setParent(flag_grp)

        pm.delete(constraint.parent_constraint_safe(pin_joint, pin_offset_grp))

        pin_node = rivets.create_uv_pin(pin_mesh, pin_offset_grp)

        pin_align_transform.setParent(pin_offset_grp)

        node.connect_nodes(pin_flag, 'flags', 'fragParent')
        node.connect_nodes(pin_joint, 'pinJoint', 'fragParent')
        node.connect_nodes(bind_joint, 'bindJoints')
        node.connect_nodes(pin_node, 'pinNode', 'fragParent')

        return node

    def get_flags(self):
        """
        Returns all the flags connected to the component.

        :return: Returns all the flags connected to the component.
        :rtype: list(flag.Flag)
        """

        flags = self.fkFlags.listConnections()
        flags = list(map(lambda x: frag_flag.Flag(x), flags))
        return flags

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
        pin_flag = flag_list[0] if flag_list else None
        bind_joint_list = self.bind_joints

        skel_region = None
        skel_side = None
        if bind_joint_list:
            wrapped_node = chain_markup.JointMarkup(bind_joint_list[0])
            skel_region = wrapped_node.region
            skel_side = wrapped_node.side

        skel_region = skel_region or self.region
        skel_side = skel_side or self.side

        pin_joint = target_root_hierarchy.get_start(skel_region, skel_side)
        if pin_joint and pin_flag:
            constraint_node = constraint.parent_constraint_safe(pin_joint, pin_flag, mo=mo)
            if constraint_node:
                constraint_list.append(constraint_node)
        return constraint_list
