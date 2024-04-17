#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, constraint, dag
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import chain_markup, reverse_chain_rig
from mca.mya.rigging.flags import tek_flag
# Internal module imports
from mca.mya.rigging.tek import keyable_component


class PelvisComponent(keyable_component.KeyableComponent):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(tek_parent,
               start_joint,
               end_joint,
               side,
               region,
               attrs_to_lock=attr_utils.TRANSLATION_ATTRS+attr_utils.SCALE_ATTRS,
               scale=1.0,
               orientation=(-90, 0, 0),
               **kwargs):
        """
        Creates an COG component.

        :param TEKNode tek_parent: TEK Rig TEKNode.
        :param pm.nt.Joint start_joint: Start joint of the chain.
        :param pm.nt.Joint end_joint: End joint of the chain.
        :param str side: The side in which the component is on the body.
        :param str region: The name of the region.  EX: "Arm"
        :param list[str] attrs_to_lock: A list of attributes on this node to disable.
        :param float scale: Scale value for flag creation.
        :param list[float, float, float] orientation: A list of XYZ rot values to offset this component by.
        :return: Returns an instance of IKFKComponent.
        :rtype: IKFKComponent
        """

        # serialize build kwargs for later.
        kwargs_dict = {}
        kwargs_dict['attrs_to_lock'] = attrs_to_lock
        kwargs_dict['scale'] = scale
        kwargs_dict['orientation'] = orientation

        # Set Namespace
        root_namespace = tek_parent.namespace().split(':')[0]
        pm.namespace(set=f'{root_namespace}:')

        node = keyable_component.KeyableComponent.create(tek_parent,
                                                         PelvisComponent.__name__,
                                                         PelvisComponent.VERSION,
                                                         side=side,
                                                         region=region,
                                                         align_component=start_joint)

        # set serialized kwargs onto our network node we'll use this for serializing the exact build params.
        attr_utils.set_compound_attribute_groups(node, 'buildKwargs', kwargs_dict)

        # Get local level groups
        flag_grp = node.flagGroup.get()
        nt_grp = node.noTouch.get()

        chain_between = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        # Create the Reverse Chain
        rev_chain = joint_utils.duplicate_chain(start_joint, end_joint, suffix='rev_chain')
        rev_chain[0].setParent(nt_grp)
        chain_rev_result = reverse_chain_rig.reverse_chain(rev_chain[0],
                                                           rev_chain[-1],
                                                           suffix='rev_chain',
                                                           scale=scale,
                                                           orientation=orientation)

        # Organize the groups
        rev_chain[0].setParent(nt_grp)
        flag = chain_rev_result["flag"]
        rotate_joint = chain_rev_result["rotate_joint"]
        align_group = chain_rev_result["align_group"]
        align_group.setParent(flag_grp)
        rotate_joint.setParent(nt_grp)
        flag.isSub.set(1)

        # Add attributes and connect
        node.connect_node(chain_rev_result['flag'], 'pelvisFlag', 'tekParent')
        node.connect_nodes(rev_chain, 'pelvisChain', 'tekParent')
        node.connect_nodes([start_joint, end_joint], 'bindJoints')

        # Lock and hide attrs
        if attrs_to_lock:
            flag.lock_and_hide_attrs(attrs_to_lock)

        # Make the reverse Joints control the base Joints
        for base_jnt, reverse_jnt in zip(chain_between, rev_chain):
            pm.parentConstraint(reverse_jnt, base_jnt, w=1)
            break
        return node

    def get_flags(self):
        return [tek_flag.Flag(self.pelvisFlag.get())]

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
        flag_node = flag_list[0] if flag_list else None

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

        joint_node = joint_list[0] if joint_list else None
        if flag_node and joint_node:
            constraint_node = constraint.parent_constraint_safe(joint_node,
                                                                flag_node,
                                                                skip_translate_attrs=['x', 'y', 'z'],
                                                                mo=mo)
        return constraint_list
