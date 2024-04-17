# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains a wrapper for the bakeResults command and other baking related utils.
"""
import pymel.core as pm

from mca.common import log

from mca.mya.utils import attr_utils, optionvars
from mca.mya.animation import time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.animation import keyframes

logger = log.MCA_LOGGER


class MCABakeOptionVars(optionvars.MCAOptionVars):
    # Helios Misc
    MCAFrameOverride = {'default_value': False, 'docstring': 'If baking overrides should be used.'}
    MCAStartFrame = {'default_value': 0, 'docstring': 'The current start frame for baking.'}
    MCAEndFrame = {'default_value': 100, 'docstring': 'The current end frame for baking.'}


@ma_decorators.make_display_layers_visible_decorator
@ma_decorators.disable_cycle_check_decorator
@ma_decorators.freeze_renderer_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_selection_decorator
@ma_decorators.unlock_animation_layers
def bake_objects(node_list,
                 translate=True,
                 rotate=True,
                 scale=True,
                 custom_attrs=None,
                 bake_range=None,
                 pok=True,
                 **kwargs):
    """
    Wrapper around pm.bakeResults cleans up some common errors before baking.
    A key is set at -1337 to handle rotation filtering and removed after.

    :param list[PyNode] node_list: A list of objects to bake.
    :param bool translate: Whether translation attrs should be baked.
    :param bool rotate: Whether rotation attrs should be baked.
    :param bool scale: Whether scale attrs should be baked.
    :param list[str] custom_attrs: A list of attribute string names if they should be baked.
    :param list[int, int] bake_range: Range of frames to bake across.
    :param bool pok: Whether to preserve outside keys.
    :param dict{} kwargs: Dict of additional args used in the bakeResults command.
    """

    if not node_list:
        logger.warning('No bakable objects were passed, aborting bake.')
        return

    attr_list = []
    if translate:
        attr_list += attr_utils.TRANSLATION_ATTRS
    if rotate:
        attr_list += attr_utils.ROTATION_ATTRS
    if scale:
        attr_list += attr_utils.SCALE_ATTRS
    if custom_attrs:
        attr_list += custom_attrs

    if not attr_list:
        logger.warning('No bakable attrs were passed, aborting bake.')
        return

    keyframes.fix_single_keyframe_layers()

    time_range = bake_range if bake_range is not None else time_utils.get_times(node_list, ignore_selection=True)

    # enable simulation or Maya will hang.
    pm.bakeResults(node_list, simulation=True, at=attr_list, t=time_range, preserveOutsideKeys=pok, **kwargs)

    pm.setKeyframe(node_list, t=-1337, at='rotate', v=0)
    pm.filterCurve(node_list)
    pm.cutKey(node_list, t=-1337)


@ma_decorators.make_display_layers_visible_decorator
@ma_decorators.disable_cycle_check_decorator
@ma_decorators.freeze_renderer_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_selection_decorator
def merge_all_animation_layers():
    base_animation = pm.animLayer(q=1, root=1)
    if not base_animation or not pm.objExists(base_animation): return
    layers = pm.animLayer(base_animation, q=True, children=True)

    if layers:
        attr_list = []
        for layer in layers:
            layer_attributes = pm.animLayer(layer, q=True, attribute=True)
            if layer_attributes:
                for attr in layer_attributes:
                    if attr and attr not in attr_list:
                        attr_list.append(attr)

        frame_range = (pm.playbackOptions(q=True, ast=True), pm.playbackOptions(q=True, aet=True))
        if attr_list:
            pm.bakeResults(attr_list, simulation=True, dic=False, removeBakedAttributeFromLayer=1, sampleBy=1,
                           time=frame_range, resolveWithoutLayer=layers, shape=False)
        pm.delete(layers)

    layers = pm.animLayer(base_animation, q=True, children=True)
    if layers:
        layer = layers[0]

        pm.animLayer(base_animation, edit=True, extractAnimation=layer)
        pm.delete(layer)

    if pm.objExists(base_animation):
        pm.delete(base_animation)

    return
