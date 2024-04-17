#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an fk chain
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.utils import dag, constraint
from mca.mya.rigging.flags import tek_flag


def fk_joint_chain(start_joint,
                   end_joint,
                   scale=1.0,
                   root_align_transform=True,
                   children_align_transforms=True,
                   create_end_flag=False,
                   offset_flag=False,
                   use_scale=False,
                   suffix='fk_chain'):
    """
    Builds an ik chain with rotation plane solver.

    :param pm.nt.Joint start_joint: The start joint of the chain.
    :param pm.nt.Joint end_joint: The end joint of the chain.
    :param float scale: Scales the flag.
    :param bool root_align_transform: Creates an extra align node for the flag.
    :param bool children_align_transforms: Creates an extra align node for the children flags.
    :param str suffix: Name to add to the end of the joints.
    :return: Returns a dictionary with all of the built nodes.
    :rtype: dictionary
    """

    if not pm.objExists(start_joint):
        raise pm.MayaNodeError("start_joint given, {0} , doesn't exist".format(start_joint))
    if not pm.objExists(end_joint):
        raise pm.MayaNodeError("end_joint given, {0} , doesn't exist".format(end_joint))
    start_joint = pm.PyNode(start_joint)
    end_joint = pm.PyNode(end_joint)
    chain = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)

    # Create flags
    flags = []
    parent_consts = []
    last = None
    chain_to_rig = chain if create_end_flag else chain[:-1]
    new_offset_flag = None
    for inc, jnt in enumerate(chain_to_rig):
        label = jnt.nodeName()
        label = label.split(':')[-1].replace('_' + suffix, "")

        if inc == 0:
            flag_node = tek_flag.Flag.create_ratio(jnt, label=label, add_align_transform=root_align_transform, scale=scale)
        elif create_end_flag and inc == (len(chain_to_rig)):
            flag_node = tek_flag.Flag.create(jnt, label=label, add_align_transform=root_align_transform, scale=scale)
        else:
            flag_node = tek_flag.Flag.create_ratio(jnt, label=label, add_align_transform=children_align_transforms, scale=scale)

        flag_align_transform = flag_node.alignTransform.get()
        if flag_align_transform:
            flag_align_transform.setParent(last)
        else:
            flag_node.setParent(last)

        if offset_flag and chain_to_rig[inc] == chain_to_rig[-1]:
            new_offset_flag = tek_flag.Flag.create(jnt,
                                                    scale=scale*.75,
                                                    label=label+'_offset',
                                                    add_align_transform=True,
                                                    is_detail=True)
            pm.parent(new_offset_flag.get_align_transform(), flag_node)
            parent_const = pm.parentConstraint(new_offset_flag, jnt, w=1, mo=1)
            #flags.append(new_offset_flag)
        else:
            parent_const = pm.parentConstraint(flag_node, jnt, w=1, mo=1)
        if use_scale:
            flag_node.s >> jnt.s

        last = flag_node
        flags.append(flag_node)
        parent_consts.append(parent_const)

    # create dictionary
    return_dictionary = {}
    return_dictionary['chain'] = chain
    return_dictionary['start_joint'] = start_joint
    return_dictionary['end_joint'] = end_joint
    return_dictionary['flags'] = flags
    return_dictionary['parent_constaints'] = parent_consts
    return_dictionary['offset_flag'] = new_offset_flag
    return return_dictionary
