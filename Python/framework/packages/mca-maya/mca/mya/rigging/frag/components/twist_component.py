#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related the twist fixup component.
"""

# python imports

# software specific imports

# Project python imports
from mca.mya.rigging import joint_utils

from mca.mya.rigging.frag.build import twist_joints
from mca.mya.rigging.frag.components import frag_rig

from mca.common import log
logger = log.MCA_LOGGER

class TwistComponent(frag_rig.FRAGComponent):
    _version = 1.0

    @classmethod
    def create(cls, frag_rig, joint_list, **kwargs):
        if not joint_list:
            'No start joint provided will abort build'
            logger.error('No start joint provided will abort build')
            return

        wrapped_joint = joint_utils.JointMarkup(joint_list[0])
        if not wrapped_joint:
            logger.error('Joint could not be wrapped.')
            return
        rig_side = wrapped_joint.side
        rig_region = wrapped_joint.region

        if not rig_side or not rig_region:
            logger.error('Missing joint markup and will abort build.')
            return

        frag_rig_node = super().create(frag_rig, rig_side, rig_region, **kwargs)

        # Get our organization groups
        dnt_group = frag_rig_node.add_do_not_touch_group()

        twist_grp, build_dict = twist_joints.twist_setup(joint_list)
        if not twist_grp:
            return frag_rig_node
        twist_grp.setParent(dnt_group)

        # Meta Connections
        frag_rig_node.connect_nodes(joint_list, 'joints')
        frag_rig_node.connect_nodes(twist_grp, 'twist_groups', 'fragParent')

        return frag_rig_node

