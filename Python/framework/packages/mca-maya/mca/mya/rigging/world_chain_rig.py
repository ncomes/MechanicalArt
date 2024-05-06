#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an cog rig
"""

from __future__ import print_function, division, absolute_import

import pymel.core as pm

from mca.mya.utils import dag
from mca.mya.rigging.flags import frag_flag


def world_chain(joint, scale=1.0, orientation=(-90, 0, 0)):
    """
    Creates a reverse chain.

    :param pm.nt.Joint joint: The start joint of the chain.
    :param float scale: Scale size of the flag.
    :param list(float) orientation: Orientation of the flag.
    :return: Returns a dictionary of the chain data.
    :rtype: Dictionary
    """

    chain = dag.get_between_nodes(joint, joint, pm.nt.Joint)

    # create flags

    world_flag = frag_flag.Flag.create(joint, label='world', scale=scale, orientation=orientation)
    root_flag = frag_flag.Flag.create(joint, label='root', scale=scale*.85, orientation=orientation)
    offset_flag = frag_flag.Flag.create(joint, label='world_offset', scale=scale*.65, orientation=orientation)

    offset_align_transform = offset_flag.get_align_transform()
    pm.parent(offset_align_transform, world_flag)

    root_align_transform = root_flag.get_align_transform()
    pm.parent(root_align_transform, world_flag)

    pm.parentConstraint(root_flag, joint, w=1, mo=True)

    for flag_node in [world_flag, root_flag, offset_flag]:
        flag_node.lock_and_hide_attrs(['sx', 'sy', 'sz'])

    # create dictionary
    return_dictionary = dict()
    return_dictionary['chain'] = chain
    return_dictionary['joint'] = joint
    return_dictionary['align_group'] = world_flag.getParent()
    return_dictionary['flags'] = [world_flag, root_flag]
    return_dictionary['world_flag'] = world_flag
    return_dictionary['root_flag'] = root_flag
    return_dictionary['offset_flag'] = offset_flag

    return return_dictionary
