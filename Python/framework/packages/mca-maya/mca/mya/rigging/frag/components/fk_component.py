#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the fk rig component.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import joint_utils
from mca.mya.utils import attr_utils, dag_utils, constraint_utils

from mca.mya.rigging.frag.build import fk_chain
from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class FKComponent(frag_rig.FRAGAnimatedComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, start_joint, end_joint, scale=None, alignment_node=None,
               lock_child_rotate_axes=[],
               lock_child_translate_axes=attr_utils.TRANSLATION_ATTRS,
               lock_child_scale_axes=attr_utils.SCALE_ATTRS,
               lock_root_rotate_axes=[],
               lock_root_translate_axes=attr_utils.TRANSLATION_ATTRS,
               lock_root_scale_axes=attr_utils.SCALE_ATTRS,
               constrain_rotate=None,
               constrain_translate=None,
               constrain_scale=None,
               **kwargs):
        """
        Creates a new FK component on the provided chain of joints from start to end.

        :param FRAGRig frag_rig: The parent FRAGRig this new component should be registered to.
        :param Joint start_joint: The first joint in the given chain.
        :param Joint end_joint: The last joint in the given chain. Both start and end should match the joint markup.
        :param float scale: Scale value the flags should be generated at. This will default to one otherwise.
        :param PyNode alignment_node: And object to align the DNT/Flag groups to.
        :param list(str, ...) lock_child_rotate_axes: A list of axes that should be locked on the flags after the first.
        :param list(str, ...) lock_child_translate_axes: A list of axes that should be locked on the flags after the first.
        :param list(str, ...) lock_child_scale_axes: A list of axes that should be locked on the flags after the first.
        :param list(str, ...) lock_root_rotate_axes: A list of axes that should be locked on the first flag.
        :param list(str, ...) lock_root_translate_axes: A list of axes that should be locked on the first flag.
        :param list(str, ...) lock_root_scale_axes: A list of axes that should be locked on the first flag.
        :param bool constrain_rotate: If rotation will be driven by this system.
        :param bool constrain_translate: If translation will be driven by this system.
        :param bool constrain_scale: If scale will be driven by this system.
        :return: The newly created frag node.
        :rtype: FKComponent
        """
        # Initialize our FRAGNode
        if not start_joint:
            logger.error('No start joint provided will abort build')
            return

        wrapped_joint = joint_utils.JointMarkup(start_joint)
        rig_side = wrapped_joint.side
        rig_region = wrapped_joint.region

        if not rig_side or not rig_region:
            logger.error('Missing joint markup and will abort build.')
            return

        frag_rig_node = super().create(frag_rig, rig_side, rig_region, alignment_node, **kwargs)

        # Save kwargs to node attrs we'll use these for serializing.
        kwargs_dict = {}
        kwargs_dict['lock_child_rotate_axes'] = lock_child_rotate_axes
        kwargs_dict['lock_child_translate_axes'] = lock_child_translate_axes
        kwargs_dict['lock_child_scale_axes'] = lock_child_scale_axes
        kwargs_dict['lock_root_rotate_axes'] = lock_root_rotate_axes
        kwargs_dict['lock_root_translate_axes'] = lock_root_translate_axes
        kwargs_dict['lock_root_scale_axes'] = lock_root_scale_axes
        kwargs_dict['constrain_rotate'] = constrain_rotate
        kwargs_dict['constrain_scale'] = constrain_scale
        kwargs_dict['constrain_translate'] = constrain_translate

        attr_utils.set_compound_attribute_groups(frag_rig_node.pynode, 'buildKwargs', kwargs_dict)

        # Get our organization groups
        flags_group = frag_rig_node.add_flags_group()
        dnt_group = frag_rig_node.add_do_not_touch_group()
        align_node = alignment_node or start_joint
        pm.delete(pm.pointConstraint(align_node, flags_group))
        pm.delete(pm.pointConstraint(align_node, dnt_group))

        # Start building shiet.
        scale = scale or 1.0

        bind_chain = dag_utils.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

        fk_joint_chain = joint_utils.duplicate_chain(start_joint, end_joint, 'fkc')
        fk_joint_chain[0].setParent(dnt_group)
        fk_results = fk_chain.build_fk_chain(fk_joint_chain, scale)

        for index, new_flag in enumerate(fk_results.get('flags')):
            if not index:
                # Parent the first alignment group to the flags group and set root locks
                new_flag.align_group.setParent(flags_group)
                new_flag.set_attr_state(attr_list=lock_root_translate_axes + lock_root_rotate_axes + lock_root_scale_axes)
            else:
                new_flag.set_attr_state(attr_list=lock_child_translate_axes + lock_child_rotate_axes + lock_child_scale_axes)

        # Check Constraints
        for bind_joint_node, fk_joint_node in zip(bind_chain, fk_joint_chain):
            skip_rotate_attrs = attr_utils.ROTATION_ATTRS if not constrain_rotate else []
            skip_translate_attrs = attr_utils.TRANSLATION_ATTRS if not constrain_translate else []

            constraint_utils.parent_constraint_safe(fk_joint_node, bind_joint_node, skip_rotate_attrs, skip_translate_attrs)
            if constrain_scale:
                # Use a direct attr connection it handles scaled parents better than a scale constraint.
                bind_joint_node.s >> fk_joint_node.s

        # After building connect our new nodes.
        # This should be used in all animated components.
        frag_rig_node.connect_nodes(bind_chain, 'joints')
        frag_rig_node.connect_nodes(fk_results.get('flags'), 'flags', 'fragParent')

        frag_rig_node.connect_nodes(fk_joint_chain, 'fk_chain', 'fragParent')

        frag_rig_node.set_scale()
        return frag_rig_node
        