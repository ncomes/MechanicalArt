#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains MotionBuilder generic utility/helpers functions and classes
"""

from __future__ import print_function, division, absolute_import

import pyfbsdk


def get_version():
    """
    Returns version of the executed MotionBuilder
    :return: int, version of MotionBuilder
    """

    path = pyfbsdk.__file__

    supported_versions = [i for i in range(2000, 2100)]
    for v in supported_versions:
        if str(v) in path:
            return v

    return None

