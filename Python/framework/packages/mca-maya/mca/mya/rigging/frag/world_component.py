#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists
from mca.mya.utils import attr_utils, dag, constraint
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import joint_utils
from mca.mya.rigging import world_chain_rig, chain_markup
from mca.mya.rigging.flags import frag_flag
# Internal module imports
from mca.mya.rigging.frag import keyable_component
from mca.mya.utils import namespace


class WorldComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent,
                start_joint,
                side,
                region,
                attrs_to_lock=(),
                scale=1.0,
                orientation=(-90, 0, 0),
                **kwargs):
        """
        Creates an COG component.

        :param FRAGNode frag_parent: FRAG Rig FRAGNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :return: Returns an instance of WorldComponent.
        :rtype: WorldComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['attrs_to_lock'] = attrs_to_lock
        kwargs_dict['scale'] = scale
        kwargs_dict['orientation'] = orientation

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        namespace.set_namespace(root_namespace, check_existing=False)

        node = keyable_component.KeyableComponent.create(frag_parent,
                                                            WorldComponent.__name__,
                                                            WorldComponent.VERSION,
                                                            side=side,
                                                            region=region,
                                                            align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, start_joint, pm.nt.Joint)

        # Create the Reverse Chain
        world_chain = joint_utils.duplicate_chain(start_joint, start_joint, suffix='world_chain')
        world_chain[0].setParent(nt_grp)
        chain_world_result = world_chain_rig.world_chain(world_chain[0],
                                                            scale=scale,
                                                            orientation=orientation)

        # Organize the groups
        flags = chain_world_result["flags"]
        world_flag = chain_world_result["world_flag"]
        root_flag = chain_world_result["root_flag"]
        root_flag.set_as_sub()
        world_joint = chain_world_result["joint"]
        align_group = chain_world_result["align_group"]
        align_group.setParent(flag_grp)
        offset_flag = chain_world_result["offset_flag"]
        offset_flag.set_as_detail()

        # Add attributes and connect
        node.connect_nodes([world_flag, offset_flag, root_flag], 'flags', 'fragParent')
        node.connect_nodes(world_chain, 'worldChain', 'fragParent')
        node.connect_node(world_flag, 'worldFlag', 'fragParent')
        node.connect_node(root_flag, 'rootFlag', 'fragParent')
        node.connect_node(offset_flag, 'offsetFlag', 'fragParent')
        node.connect_nodes([start_joint], 'bindJoints')

        # Lock and hide attrs
        if attrs_to_lock:
            [flag_node.lock_and_hide_attrs(attrs_to_lock) for flag_node in node.get_flags()]

        # Make the reverse Joints control the base Joints
        for base_jnt, reverse_jnt in zip(chain_between, world_chain):
            pm.parentConstraint(reverse_jnt, base_jnt, w=1)

        return node

    def get_flags(self):
        return [frag_flag.Flag(x) for x in self.pynode.flags.get()]

    @property
    def world_flag(self):
        return frag_flag.Flag(self.worldFlag.get())

    @property
    def root_flag(self):
        return frag_flag.Flag(self.rootFlag.get())

    @property
    def offset_flag(self):
        return frag_flag.Flag(self.offsetFlag.get())

    def attach_to_skeleton(self, attach_skeleton_root, mo=True):
        """
        Drive the component with a given skeleton.

        :param Joint attach_skeleton_root: Top level joint of the hierarchy to drive the component.
        :param bool mo: If object offsets should be maintained.
        :return: A list of all created constraints.
        :rtype list[Constraint]:
        """

        target_root_hierarchy = chain_markup.ChainMarkup(attach_skeleton_root)

        root_flag = self.root_flag
        bind_joint_list = self.bind_joints

        skel_region = None
        skel_side = None
        if bind_joint_list:
            wrapped_node = chain_markup.JointMarkup(bind_joint_list[0])
            skel_region = wrapped_node.region
            skel_side = wrapped_node.side

        skel_region = skel_region or self.region
        skel_side = skel_side or self.side

        joint_node = lists.get_first_in_list(target_root_hierarchy.get_full_chain(skel_region, skel_side))
        constraint_node = constraint.parent_constraint_safe(joint_node, root_flag, mo=mo)

        return [constraint_node]
