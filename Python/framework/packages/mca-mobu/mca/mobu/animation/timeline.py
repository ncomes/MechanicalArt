#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions that interact with the timeline
"""

# mca python imports

# software specific imports
from pyfbsdk import FBSystem, FBPlayerControl
# mca python imports



def get_current_frame():
    """
    Return current Maya frame set in time slider.

    :return: current frame.
    :rtype: int
    """

    return FBSystem().LocalTime.GetFrame()


def get_active_frame_range():
    """
    Returns current animation frame range.

    :return: tuple with the start frame in the first index (0) and end frame in the second index (1)
    :rtype: tuple(int, int)
    """

    return FBPlayerControl().LoopStart.GetFrame(), FBPlayerControl().LoopStop.GetFrame()


def get_start_frame():
    """
    Returns current start frame.

    :return: start frame.
    :rtype: int
    """

    return get_active_frame_range()[0]


def get_end_frame():
    """
    Returns current end frame
    :return: end frame.
    :rtype: int
    """

    return get_active_frame_range()[1]