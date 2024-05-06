#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with Maya scene
"""

from __future__ import print_function, division, absolute_import

import os

import pyfbsdk


def get_scene_name():
    """
    Returns the name of the current opened MotionBuilder scene.

    :return: MotionBuilder scene opened name.
    :rtype: str
    """

    path_drive, path_tail = os.path.split(pyfbsdk.FBApplication().FBXFileName)
    return path_tail.split('.')[0]


def get_scene_name_and_path():
    """
    Returns the name and path of the current opened MotionBuilder scene.

    :return: MotionBuilder scene opened file path.
    :rtype: str
    """

    return pyfbsdk.FBApplication().FBXFileName
