#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to building a simple FK chain.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging import flags, joint_utils
from mca.mya.utils import constraint_utils, dag_utils, naming

def build_fk_chain(joint_chain, scale=None, use_scale=False):
    scale = scale or 1.0

    wrapped_joint = joint_utils.JointMarkup(joint_chain[0])

    flag_list = []
    constraint_list = []
    for index, joint_node in enumerate(joint_chain):
        joint_name = naming.get_basename(joint_node).replace('_fkc', '')
        if joint_name.startswith('b_'):
            joint_name = joint_name[2:]
        flag_name = f'f_{joint_name}_fk'
        new_flag = flags.Flag.create(flag_name, joint_node, scale, flag_path='rotation')
        new_flag.side = wrapped_joint.side
        new_flag.region = wrapped_joint.region
        flag_pynode = new_flag.pynode
        constraint_list.append(constraint_utils.parent_constraint_safe(flag_pynode, joint_node))
        if use_scale:
            # Don't use a constraint here or it messes with rig scaling.
            flag_pynode.s >> joint_node.s
        if index:
            new_flag.align_group.setParent(flag_list[-1].pynode)
        flag_list.append(new_flag)

    # Fill out return dict.
    return_dict = {}
    return_dict['chain'] = joint_chain
    return_dict['start_joint'] = joint_chain[0]
    return_dict['end_joint'] = joint_chain[-1]
    return_dict['flags'] = flag_list
    return_dict['constraints'] = constraint_list
    return return_dict

def build_reverse_fk_chain(joint_chain, scale=None, use_scale=False):
    return build_fk_chain(joint_utils.reverse_joint_chain(joint_chain), scale, use_scale)

        