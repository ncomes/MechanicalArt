#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains PyMEL Maya specific decorators
"""

from __future__ import print_function, division, absolute_import

import traceback
from functools import wraps

import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

from mca.common import log

logger = log.MCA_LOGGER


def repeat_static_command_decorator(class_name, skip_arguments=False):
    """
    Decorator that will make static functions repeatable for Maya.

    :param str class_name: path to the Python module where function we want to repeat is located.
    :param bool skip_arguments: whether force the execution of the repeat function without passing any argument.
    """

    def repeat_command(fn):
        def wrapper(*args, **kwargs):
            arg_str = ''
            fn_return = None
            if args:
                for each in args:
                    arg_str += str(each) + ', '
                    arg_str += '"{}", '.format(each)
            if kwargs:
                for k, v in kwargs.items():
                    arg_str += str(k) + '=' + str(v) + ', '

            if not skip_arguments:
                cmd = 'python("' + class_name + '.' + fn.__name__ + '(' + arg_str + ')")'
            else:
                cmd = 'python("' + class_name + '.' + fn.__name__ + '()")'
            try:
                fn_return = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.repeatLast(ac=cmd, acl=fn.__name__)
            return fn_return

        return wrapper

    return repeat_command


def disable_cycle_check_decorator(fn):
    """
    Function decorator that disables the cycle check then restores it to previous values.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            cycle_check = pm.cycleCheck(q=True, e=True)
            pm.cycleCheck(e=False)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.cycleCheck(e=cycle_check)
            return result
        except Exception:
            raise
    return wrapper


def freeze_renderer_decorator(fn):
    """
    Function decorator that disables the panel renderer.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            pm.refresh(su=True)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.refresh(su=False)
            return result
        except Exception:
            raise
    return wrapper


def ignore_prompts_decorator(fn):
    """
    Function decorator that makes sure that disable maya import/open prompts.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            prompt_setting = cmds.file(prompt=True, q=True)
            cmds.file(prompt=False)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                cmds.file(prompt=prompt_setting)
            return result
        except Exception:
            raise

    return wrapper


def keep_autokey_decorator(fn):
    """
    Function decorator that makes sure that original autokey setting is kept after executing the wrapped function.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            autokey_setting = cmds.autoKeyframe(q=True, state=True)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.autoKeyframe(state=autokey_setting)
            return result
        except Exception:
            raise

    return wrapper


def keep_current_frame_decorator(fn):
    """
    Function decorator that makes sure that starting keyframe is kept after executing the wrapped function.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_frame = cmds.currentTime(q=True)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                cmds.currentTime(current_frame)
            return result
        except Exception:
            raise

    return wrapper


def keep_selection_decorator(fn):
    """
    Function decorator that makes sure that original selection is keep after executing the wrapped function.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            tmp_selection = pm.ls(sl=True, l=True)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.select(tmp_selection)
            return result
        except Exception:
            raise
    return wrapper


def keep_namespace_decorator(fn):
    """
    Function decorator that restores the active namespace after execution.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            original_namespace = pm.namespaceInfo(cur=True)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.namespace(set=':')
                pm.namespace(set=original_namespace)
            return result
        except Exception:
            raise
    return wrapper


def make_display_layers_visible_decorator(fn):
    """
    Function decorator that toggles on all display layers during execution then restores them.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            display_layer_dict = {}
            default_display_layer = pm.PyNode('defaultLayer') if pm.objExists('defaultLayer') else None
            result = None
            for display_layer in pm.ls(type='displayLayer'):
                if display_layer != default_display_layer:
                    display_layer_dict[display_layer] = display_layer.visibility.get()
                    display_layer.visibility.set(True)
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                for display_layer, value in display_layer_dict.items():
                    if pm.objExists(display_layer):
                        display_layer.visibility.set(value)
            return result
        except Exception:
            raise
    return wrapper


def undo_decorator(fn):
    """
    Function decorator that enables undo functionality using Maya Python commands.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        try:
            ret = fn(*args, **kwargs)
        except Exception:
            raise Exception(traceback.format_exc())
        finally:
            pm.undoInfo(closeChunk=True)
        return ret
    return wrapper


def not_undoable_decorator(fn):
    """
    Function decorator that prevents undoing a fnc call.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            is_swf_on = pm.undoInfo(q=True, swf=True)
            pm.undoInfo(swf=False)
            result = None
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                pm.undoInfo(swf=is_swf_on)
            return result
        except Exception:
            raise
    return wrapper


def unlock_animation_layers(fn):
    """
    Function decorator that makes sure all animation layers are unlocked during execution.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            lock_dict = {}
            animation_layer_list = pm.ls(type=pm.nt.AnimLayer)
            for x in animation_layer_list:
                lock_dict[x] = x.getLock()
                x.setLock(False)
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            finally:
                for x, lock_state in lock_dict.items():
                    if x.exists():
                        x.setLock(lock_state)
            return result
        except Exception:
            raise

    return wrapper


def viewport_off(fn):
    """
    Function decorator that turns off Maya display while the function is being executed.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        parallel = False
        maya_version = mel.eval("$mayaVersion = `getApplicationVersionAsFloat`")
        if maya_version >= 2016:
            if 'parallel' in cmds.evaluationManager(q=True, mode=True):
                cmds.evaluationManager(mode='off')
                parallel = True
                logger.info('Turning off Parallel evaluation...')
        # turn $gMainPane Off and hide the time slider (this is the important part):
        mel.eval('paneLayout -e -manage false $gMainPane')
        cmds.refresh(suspend=True)
        mel.eval('setTimeSliderVisible 0;')

        try:
            return fn(*args, **kwargs)
        except Exception:
            raise
        finally:
            pm.refresh(suspend=False)
            mel.eval('setTimeSliderVisible 1;')
            if parallel:
                pm.evaluationManager(mode='parallel')
                logger.info('Turning on Parallel evaluation...')
            mel.eval('paneLayout -e -manage true $gMainPane')
            pm.refresh()

    return wrapper

