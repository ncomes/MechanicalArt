#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules to interact with animation curves.
"""

# System global imports
# python imports
import pymel.core as pm
import maya.cmds as cmds

# mca python imports
from mca.common import log
from mca.common.utils import lists

from mca.mya.animation import keyframes, time_utils
from mca.mya.modifiers import ma_decorators

# Internal module imports

logger = log.MCA_LOGGER

@ma_decorators.unlock_animation_layers
def crop_time_range(min_time, max_time, node_list=None, start_to_zero=False):
    """
    Trims the animation on all or given objects to inclusively be the given time range.

    :param PyNode node_list: Objects with animation curves.
    :param float min_time: New 1st frame.
    :param float max_time: New last frame.
    """

    cmds.select(None)
    min_range, max_range = time_utils.get_times()
    animcurve_list = pm.ls(type=pm.nt.AnimCurve) if not node_list else time_utils.get_keyframe_range_from_nodes(node_list)
    pm.setKeyframe(animcurve_list, t=min_time)
    pm.setKeyframe(animcurve_list, t=max_time)
    pm.cutKey(animcurve_list, cl=True, t=[min_range, min_time - 1])
    pm.cutKey(animcurve_list, cl=True, t=[max_time + 1, max_range])
    if start_to_zero:
        change_curve_start_time(animcurve_list, shift_length=min_time * -1)

@ma_decorators.unlock_animation_layers
def change_curve_start_time(node_list, shift_length=None):
    """
    Shifts all keyframes on a set of objects by a given value. If no shift length is given it will zero the animation.

    :param PyNode node_list: A list of objects to shift the keyframes on.
    :param int shift_length: How much the animation should be shifted by.
    """

    if not node_list:
        logger.warning('A valid node list is required to shift keys from.')
        return

    if not shift_length:
        if not isinstance(node_list, list):
            node_list = [node_list]
        min_frame, max_frame = time_utils.get_times(node_list)
        if min_frame != 0:
            shift_length = min_frame*-1

    if shift_length:
        pm.keyframe(node_list, timeChange=shift_length, relative=True)
    else:
        logger.warning('No keyframes were shifted as none were found.')


def replace_into_curve(curve_a, curve_b, delete_curve=False):
    """
    Copies on anim curve onto another.

    :param pm.nt.AnimCurve curve_a: The animation curve that is being copied.
    :param pm.nt.AnimCurve curve_b: The animation curve that is receiving the copied curves.
    :param delete_curve:  Deletes the animation curve that is being copied from.
    """

    pm.copyKey(curve_a)
    key_time = pm.keyframe(curve_a, q=True)
    pm.pasteKey(curve_b, o='replace', t=[key_time[0], key_time[-1]])
    if delete_curve:
        pm.delete(curve_a)


def merge_curves(curve_a, curve_b, delete_curves=False):
    """
    Merges two animation curves.

    :param pm.nt.AnimCurve curve_a: The animation curve that is being copied.
    :param pm.nt.AnimCurve curve_b: The animation curve that is receiving the copied curves.
    :param delete_curve:  Deletes the animation curve that is being copied from.
    """

    merged_curve = pm.duplicate(curve_b)[0]
    keyframes = [keyframe for keyframe in pm.keyframe([curve_a, curve_b], query=True)]
    max_keyframe = max(keyframes)

    for x in range(int(max_keyframe) + 1):
        value = lists.get_first_in_list(pm.keyframe(curve_a, q=True, t=x, vc=True))
        if value and value != 0:
            pm.setKeyframe(merged_curve, t=x, v=value)

    if delete_curves:
        pm.delete(curve_a, curve_b)
    return merged_curve


def multiply_curve_values(animation_curve, multi=1.0):
    """
    Multiplies all the anim values.

    :param pm.nt.AnimCurve animation_curve: The animation curve that is being changed.
    :param float multi: multiplies all the anim values.
    """

    for frame in pm.keyframe(animation_curve, q=True):
        value = pm.keyframe(animation_curve, q=True, vc=True, t=frame)[0] * multi
        pm.keyframe(animation_curve, t=frame, vc=value)


def restore_from_anim_curves(anim_curve,
                             object_attribute,
                             keep_curves=False,
                             delete_old_curves=False,
                             start_time=None):
    """
    Restores animation curves.  Takes existing curves and connects it to an object attribute.

    :param pm.nt.AnimCurve anim_curve: The animation curve node.
    :param pm.nt.Attribute object_attribute:  THe attribute on an object that you are attaching animation.
    :param bool keep_curves: If True, The animation curve will be duplicated before connecting.
    :param bool delete_old_curves: If True, If there is an existing animation curve on the object attribute it will
    delete it first.
    :param float/None start_time: the start time of the animation.  It will adjust the animation curve times.
    :return:  The end frame of the animation curve.
    :rtype: float
    """

    if keep_curves:
        anim_curve = pm.duplicate(anim_curve)[0]

    # adjust time range to match the selected timeline
    end_frame = None
    if start_time:
        change_curve_start_time(anim_curve, start_time)
        end_frame = pm.keyframe(anim_curve, q=True)[-1]

    # If there is a curve already connected to that object attribute.  Delete it.
    obj_curve = object_attribute.listConnections(d=False, s=True)
    if not obj_curve:
        # Swap the animation curve from the node to the object.
        anim_curve.output >> object_attribute
    elif obj_curve and delete_old_curves:
        # Delete the old curves 1st, then swap the animation curve from the node to the object.
        pm.delete(obj_curve)
        anim_curve.output >> object_attribute
    elif obj_curve and not delete_old_curves:
        pm.copyKey(anim_curve)
        key_time = pm.keyframe(anim_curve, q=True)
        # One frame animation uses "merge", a full animation uses replace.
        if len(key_time) == 1:
            pm.pasteKey(obj_curve, o='merge', t=[key_time[0], key_time[-1]])
        else:
            pm.pasteKey(obj_curve, o='replace', t=[key_time[0], key_time[-1]])
    return end_frame


def reanimate_from_anim_curves(anim_curve,
                            object_attribute,
                            start_time=None,
                            end_time=None):
    """
    Restores animation curves.  Takes existing curves and connects it to an object attribute.

    :param pm.nt.AnimCurve anim_curve: The animation curve node.
    :param pm.nt.Attribute object_attribute:  The attribute on an object that you are attaching animation.
    :param float/None start_time: the start time of the animation
    :param float/None end_time: the end time of the animation
    """

    if not anim_curve:
        return

    if end_time:
        keyframes = pm.keyframe(anim_curve, query=True, timeChange=True)
        delete_keyframes = [keyframe for keyframe in keyframes if keyframe < start_time or keyframe > end_time]
        list(map(lambda x: pm.cutKey(anim_curve, time=x, option='keys'), delete_keyframes))

    obj_curve = object_attribute.listConnections(d=False, s=True)
    if obj_curve:
        anim_curve = merge_curves(anim_curve, obj_curve[0], delete_curves=True)

    anim_curve.output >> object_attribute

