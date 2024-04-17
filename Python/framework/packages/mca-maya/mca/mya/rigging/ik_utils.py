# #! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with IKs
"""

# System global imports

# python imports
import pymel.core as pm
#  python imports


def get_pole_vector_position(joint_chain, offset=None):
    """
    Returns the world position where a pole vector node should be located.

    :param list(pm.PyNode) joint_chain: list of joints.
    :return: world vector pole vector.
    :rtype: pm.dt.Vector
    """

    root_jnt_vec = pm.dt.Vector(pm.xform(joint_chain[0], worldSpace=True, q=True, translation=True))
    end_jnt_vec = pm.dt.Vector(pm.xform(joint_chain[-1], worldSpace=True, q=True, translation=True))

    if len(joint_chain) % 2:
        mid_index = (len(joint_chain) - 1) // 2
        mid_jnt_vec = pm.dt.Vector(pm.xform(joint_chain[mid_index], worldSpace=True, q=True, translation=True))
    else:
        prev_jnt_index = len(joint_chain) // 2
        next_jnt_index = prev_jnt_index + 1
        prev_jnt_vector = pm.dt.Vector(pm.xform(joint_chain[prev_jnt_index], worldSpace=True, q=True, translation=True))
        next_jnt_vector = pm.dt.Vector(pm.xform(joint_chain[next_jnt_index], worldSpace=True, q=True, translation=True))
        mid_jnt_vec = (next_jnt_vector + prev_jnt_vector) * 0.5  # find mid point between joints with close to mid

    # get projection vector
    line = (end_jnt_vec - root_jnt_vec)
    point = (mid_jnt_vec - root_jnt_vec)
    scale_value = (line * point) / (line * line)
    project_vec = line * scale_value + root_jnt_vec

    # get chain length
    root_to_mid_len = (mid_jnt_vec - root_jnt_vec).length()
    mid_to_end_len = (end_jnt_vec - mid_jnt_vec).length()
    total_len = offset if offset is not None else (root_to_mid_len + mid_to_end_len)

    pole_vec_pos = (mid_jnt_vec - project_vec).normal() * total_len + mid_jnt_vec

    return pole_vec_pos


def create_pole_vector_locator(joint_chain, name=None, offset=None):
    """
    Creates a new locator in a position that is coplanar for all the joints of the given joints chain.

    :param list(pm.PyNode) joint_chain: list of joints.
    :param str name: name of the pole vector locator.
    :param float offset: offset of the pole vector locator.
    """

    pol_vec_pos = get_pole_vector_position(joint_chain, offset=offset)
    pole_locator = pm.spaceLocator(n=name or 'poleVectorLoc')
    pole_locator.translate.set(list(pol_vec_pos))

    return pole_locator
