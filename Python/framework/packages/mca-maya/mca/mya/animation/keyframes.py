#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related with keyframes in Maya
"""

# System global imports
# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log

logger = log.MCA_LOGGER


def fix_single_keyframe_layers():
    """
    Find all animation layers with a single keyframe and place a second keyframe 1 frame after the first for all objects in the layer.

    """
    anim_lyr_list = pm.ls(type='animLayer')
    if not len(anim_lyr_list) > 1:
        return
    for anim_layer in anim_lyr_list:
        anim_curve_list = pm.animLayer(anim_layer, query=True, animCurves=True)
        # Ignore anim layers with no animation
        single_keyframe = True if anim_curve_list else False
        keyed_frame = None
        for anim_curve in anim_curve_list:
            if anim_curve.numKeyframes() > 1:
                single_keyframe = False
                break
            else:
                keyed_frame = anim_curve.getTime(0)
        if single_keyframe:
            layer_obj_list = list(set(anim_layer.dagSetMembers.listConnections()))
            if layer_obj_list:
                pm.copyKey(layer_obj_list, animLayer=anim_layer, t=keyed_frame)
                pm.pasteKey(layer_obj_list, animLayer=anim_layer, t=keyed_frame+1)
