#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Maya generic utility/helpers functions and classes
"""

# System global imports
import os
# python imports
import pymel.core as pm
import maya.mel as mel
#  python imports
from mca.common import log


logger = log.MCA_LOGGER


def get_float_version():
    """
    Returns the Maya version as a float value.

    :return: version of Maya as float value.
    :rtype: float
    """

    return mel.eval('getApplicationVersionAsFloat')


def is_plugin_loaded(plugin_name):
    """
    Return whether given plugin is loaded or not.

    :param str plugin_name: name of the plugin to load
    :return: True if the plugin is already loaded; False otherwise.
    :rtype: bool
    """

    return pm.pluginInfo(plugin_name, query=True, loaded=True)


def load_plugin(plugin_name, quiet=True):
    """
    Loads plugin with the given name (full path).

    :param str plugin_name: name or path of the plugin to load.
    :param bool quiet: Whether to show info to user that plugin has been loaded or not.
    :return: True if the plugin was loaded successfully; False otherwise.
    :rtype: bool
    """

    if not is_plugin_loaded(plugin_name):
        try:
            pm.loadPlugin(plugin_name, quiet=quiet)
        except Exception as exc:
            if not quiet:
                logger.error('Impossible to load plugin: {} | {}'.format(plugin_name, exc))
            return False

    return True


def unload_plugin(plugin_name):
    """
    Unloads the given plugin.

    :param str plugin_name: name or path of the plugin to unload.
    :return: True if the plugin was unloaded successfully; False otherwise.
    :rtype: boo
    """

    if not is_plugin_loaded(plugin_name):
        return False

    return pm.unloadPlugin(plugin_name)


def add_trusted_plugin_location_path(allowed_path):
    """
    Adds the given path to the list of trusted plugin locations.

    :param str allowed_path: path to add do trusted plugin locations list.
    :return: True if the operation was successfull; False otherwise.
    :rtype: bool
    """

    if get_float_version() < 2022:
        return False

    allowed_path = os.path.normpath(allowed_path)
    allowed_paths = pm.optionVar(query='SafeModeAllowedlistPaths')
    if allowed_path in allowed_paths:
        return False

    pm.optionVar(stringValueAppend=('SafeModeAllowedlistPaths', allowed_path))

    return True
