#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains library implementation for mca-mobu-stayonfloor
"""

from __future__ import print_function, division, absolute_import

from pyfbsdk import FBTangentMode


def process_animation_node(anim_node, curr_time, start_time, stop_time, blend_time):
    for node in anim_node.Nodes:
        if node.FCurve:
            process_f_curve(node.FCurve, curr_time, start_time, stop_time, blend_time)


def process_f_curve(curve, curr_time, start_time, stop_time, blend_time):
    value = curve.Evaluate(curr_time)

    start_time_blend = start_time - blend_time
    stop_time_blend = stop_time + blend_time

    if curve:
        curve.KeyDeleteByTimeRange(start_time_blend, stop_time_blend, True)

    start_ndx = curve.KeyAdd(start_time, value)
    stop_ndx = curve.KeyAdd(stop_time, value)

    if start_ndx >= 0:
        curve.Keys[start_ndx].TangentMode = FBTangentMode.kFBTangentModeUser
        curve.Keys[start_ndx].LeftDerivative = 0.0
        curve.Keys[start_ndx].RightDerivative = 0.0

    if stop_ndx >= 0:
        curve.Keys[stop_ndx].TangentMode = FBTangentMode.kFBTangentModeUser
        curve.Keys[stop_ndx].LeftDerivative = 0.0
        curve.Keys[stop_ndx].RightDerivative = 0.0
