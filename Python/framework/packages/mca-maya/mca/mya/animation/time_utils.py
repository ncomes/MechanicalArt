#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Build a component building information.

"""

# python imports
import os
import re

# software specific imports
import maya.cmds as cmds
from maya.plugin.timeSliderBookmark.timeSliderBookmark import createBookmark
import pymel.core as pm


# mca python imports
from mca.common.utils import pymaths
from mca.mya.utils import plugins
from mca.mya.utils.om import om_utils

plugins.load_plugin('timeSliderBookmark')

from mca.common import log
logger = log.MCA_LOGGER


def get_visible_start_time():
    """
    Get the first visible frame of the timeline.

    :return: The first frame of the visible timeline.
    :rtype int:
    """
    
    return pm.playbackOptions(q=1, min=1)


def get_visible_end_time():
    """
    Get the last visible frame of the timeline.

    :return: The last frame of the visible timeline.
    :rtype int:
    """
    
    return pm.playbackOptions(q=1, max=1)


def get_visible_range():
    """
    Get the start and end frame of the visible timeline.

    :return: The start and end frame of the visible timeline.
    :rtype int, int:
    """
    
    return get_visible_start_time(), get_visible_end_time()


def get_scene_start_time():
    """
    Get the first frame of the scene timeline.

    :return: The first frame of the scene timeline.
    :rtype int:
    """
    
    return pm.playbackOptions(q=1, ast=1)


def get_scene_end_time():
    """
    Get the last frame of the scene timeline.

    :return: The last frame of the scene timeline.
    :rtype int:
    """
    
    return pm.playbackOptions(q=1, aet=1)


def get_scene_range():
    """
    Get the start and end frame of the scene timeline.

    :return:  The start and end frame of the scene timeline.
    :rtype int, int:
    """
    
    return get_scene_start_time(), get_scene_end_time()


def get_scene_first_keyframe():
    """
    returns time of first keyframe in the entire scene. Does not rely on animation time range.

    :return: frame of first keyframe
    :rtype int:
    """
    
    scene_start, scene_end = om_utils.get_om2_keyframe_range_from_scene()
    return round(scene_start, 4) if scene_start else scene_start


def get_scene_last_keyframe():
    """
    returns time of last keyframe in the entire scene. Does not rely on animation time range.

    :return: frame of last keyframe
    :rtype int:
    """
    
    scene_start, scene_end = om_utils.get_om2_keyframe_range_from_scene()
    return round(scene_end, 4) if scene_end else scene_end


def get_keyframe_range_from_scene():
    """
    From all scene animation curves get the first and last keyframe.

    :return: The start and end frame of all animation in the scene.
    :rtype int, int:
    """
    scene_start, scene_end = om_utils.get_om2_keyframe_range_from_scene()
    scene_start = round(scene_start, 4) if scene_start else scene_start
    scene_end = round(scene_end, 4) if scene_end else scene_end
    return scene_start, scene_end


def get_keyframe_range_from_nodes(node_list):
    """
    Returns the keyframe range from a group of nodes. This will return None if there are no valid keyframes on the nodes.

    :param list node_list: List of dag nodes with keyframes.
    :return: The start and end frame of the keyframes of the passed list.
    :rtype int, int:
    """
    key_frame_list = om_utils.get_om2_keyframes_from_pynode_list(node_list)
    start_frame = round(key_frame_list[0], 4) if key_frame_list[0] else key_frame_list[0]
    end_frame = round(key_frame_list[-1], 4) if key_frame_list[-1] else key_frame_list[-1]
    return start_frame, end_frame


def get_selected_range_from_timeline():
    """
    Returns a selection on the timeline else None if there is no selection.

    :return: The start and end frame of the timeline selection.
    :rtype int, int:
    """
    
    try:
        gPlayBackSlider = pm.mel.eval('$tmpVar=$gPlayBackSlider')  # vollects timeslider
        if pm.timeControl(gPlayBackSlider, q=True, rv=True):  # is a selection visible
            min_frame, max_frame = pm.timeControl(gPlayBackSlider, q=True, ra=True)  # collect frame array.
        else:
            return None, None
    except Exception as exc:
        # failed to find the playback slider.
        return None, None
    
    return min_frame, max_frame


def get_range_from_attribute_curves(attr_curve_list):
    """
    From a list of attribute curves find the first and last keyframes.

    :param list[AttrCurve] attr_curve_list:
    :return: The start and end frame of the passed curves.
    :rtype int, int:
    """
    
    selected_keys = sorted(pm.keyframe(attr_curve_list, q=True, sl=True))
    if selected_keys:
        return min(selected_keys), max(selected_keys)
    return None, None


def set_timeline_range(visible_start_time, visible_end_time, scene_start_time=None, scene_end_time=None):
    """
    Set the visible, and scene ranges for the timeline.

    :param int visible_start_time: The first frame on the visible timeline.
    :param int visible_end_time: The last frame on the visible timeline.
    :param int scene_start_time: The first frame of the scene timeline
    :param int scene_end_time: The last frame of the scene timeline
    """
    
    if not scene_start_time:
        scene_start_time = visible_start_time
    if not scene_end_time:
        scene_end_time = visible_end_time
    pm.playbackOptions(edit=True, animationStartTime=scene_start_time, minTime=visible_start_time,
                       maxTime=visible_end_time, animationEndTime=scene_end_time)


def get_times(node_list=None, min_selected_frames=1, ignore_selection=True):
    """
    Returns the frame range in cascading order of importance.

    #1 Selected Timeline
    #2 (Optional) Curve Editor Selection
    #3 (Optional) Node list
    #4 Animation curves in scene
    #5 Greatest of zoomed timeline or scene timeline

    :param list[PyNode] node_list: List of objects we should use to derive time range.
    :param int min_selected_frames: Minimum number of required selected frames.
    :param bool ignore_selection: This ignores the logic for deriving keyframe range from a selection of attribute curves.
    :return: The best choice of first and last frame values.
    :rtype int, int:
    """
    
    frame_range = get_selected_range_from_timeline()  # 1 selected timeline
    log_str = '#1 Using user selected timeline.'
    
    if not any(x is None for x in frame_range):
        selected_frames = frame_range[-1] - frame_range[0]
    else:
        selected_frames = 0
    
    if any(x is None for x in frame_range) or selected_frames < min_selected_frames:
        # check returned frame range, if the range is less than the expected min. Cascade.
        if not ignore_selection:
            # 2 curve editor
            attr_curves = pm.keyframe(q=True, selected=True, name=True)
            if attr_curves:
                frame_range = get_range_from_attribute_curves(attr_curves)
                log_str = '#2.1 Using user selected attr curves.'
        
        if any(x is None for x in frame_range) and node_list:
            # 3 passed objects with keys
            frame_range = get_keyframe_range_from_nodes(node_list)
            log_str = '#2.2 Using passed objects.'
        
        if any(x is None for x in frame_range):
            # 4 if we didn't get anything from our passed objects, see if we have any animation in the scene.
            frame_range = get_keyframe_range_from_scene()
            log_str = '#3 Using scene animation curves'
        
        if any(x is None for x in frame_range):
            # 5 if we didn't get a valid selection use the greatest of scene or visible timeline.
            frame_range = min(get_scene_start_time(), get_visible_start_time()), max(get_scene_end_time(),
                                                                                     get_visible_end_time())
            log_str = '#3 Using scene zoomed timeline.'
    
    logger.debug(log_str)
    return frame_range


def reframe_visible_range():
    """
    Reframe the scene visible range, from keyframes or the default of 0-100

    """
    
    # reframe our scene to the length of the new animation.
    min_frame = get_scene_first_keyframe()
    min_frame = round(min_frame) if min_frame else 0
    max_frame = get_scene_last_keyframe()
    max_frame = round(max_frame) if max_frame else 100
    set_timeline_range(min_frame, max_frame)


def set_padded_keys(obj_attr, frame, value):
    """
    Sets the keys on the object's attribute, but pads it, so it is zero before and after.

    :param pm.nt.attribute obj_attr: attribute name
    :param float frame: frame number
    :param float value: value the flag attribute is set to.
    """
    
    obj_attr.set(value)
    pm.setKeyframe(obj_attr, t=[frame])
    keyed_frames = pm.keyframe(obj_attr, q=True)
    if not frame - 1 in keyed_frames:
        obj_attr.set(0)
        pm.setKeyframe(obj_attr, t=[frame - 1])
    if not frame + 1 in keyed_frames:
        obj_attr.set(0)
        pm.setKeyframe(obj_attr, t=[frame + 1])


def create_bookmark(name='timeSliderBookmark', frame_range=None, color=None):
    """
    Creates a colored timeSliderBookmark

    :param str name: The name of the new bookmark.
    :param list[int, int] frame_range: Start and end frame range to represent. The max value is not inclusive.
    :param list[float, float, float] color: Float 3 of values between 0-1
    :return: The newly created timeslider bookmark
    :rtype: TimeSliderBookmark
    """
    frame_range = frame_range or get_times()
    color = color or pymaths.create_random_list()
    return pm.PyNode(createBookmark(name=name, start=frame_range[0], stop=frame_range[1], color=color))

