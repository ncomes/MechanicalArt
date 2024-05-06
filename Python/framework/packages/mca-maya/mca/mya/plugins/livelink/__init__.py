#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for Unreal Live Link plugin
"""

from __future__ import print_function, division, absolute_import

import os

import maya.cmds as cmds

from mca.common import log
from mca.common.utils import pyutils
from mca.mya.utils import plugins, maya_utils


logger = log.MCA_LOGGER


def load_plugin(reload=False):
    """
    Loads Unreal LiveLink Maya plugin.

    :param bool reload: whether to reload plugin.
    """

    root_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    scripts_path = os.path.join(root_path, 'scripts')
    cpp_plugin_name = 'MayaUnrealLiveLinkPlugin.mll'
    version_path = os.path.join(root_path, str(maya_utils.get_version()))
    py_plugin_path = os.path.join(version_path, 'MayaUnrealLiveLinkPluginUI.py')
    version_scripts_path = os.path.join(version_path, 'scripts')
    icons_path = os.path.join(version_path, 'icons')
    pyutils.append_path_env_var('MAYA_SCRIPT_PATH', scripts_path)
    pyutils.append_path_env_var('MAYA_SCRIPT_PATH', version_path)
    pyutils.append_path_env_var('MAYA_PLUG_IN_PATH', version_path)
    pyutils.append_path_env_var('PYTHONPATH', version_path)
    pyutils.append_path_env_var('MAYA_SCRIPT_PATH', version_scripts_path)

    if not plugins.is_plugin_loaded(cpp_plugin_name):
        plugins.load_plugin(cpp_plugin_name)
    elif plugins.is_plugin_loaded(cpp_plugin_name) and reload:
        plugins.unload_plugin(cpp_plugin_name)
        plugins.load_plugin(cpp_plugin_name)

    if not plugins.is_plugin_loaded(py_plugin_path):
        plugins.load_plugin(py_plugin_path)
    elif plugins.is_plugin_loaded(py_plugin_path) and reload:
        plugins.unload_plugin(os.path.basename(py_plugin_path))
        plugins.load_plugin(py_plugin_path)

    plugins.add_trusted_plugin_location_path(version_path)

    return True


def open_livelink_ui():
    """
    Opens LiveLink Maya UI
    """

    load_plugin(reload=False)
    cmds.MayaUnrealLiveLinkUI()
