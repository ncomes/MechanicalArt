#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains MotionBuilder configuration related functions.
"""

# mca python imports
import os
# software specific imports
from pyfbsdk import FBConfigFile
# mca python imports


def add_path_to_additional_plugin_paths(plugin_path):
    """
    Registers given path to MoBu application configuration file.
    :param plugin_path:
    :return:
    """

    if not plugin_path:
        return

    app_config = FBConfigFile("@Application.txt")

    current_paths = list()
    plugin_path = os.path.normpath(plugin_path)
    num_plugins = int(app_config.Get("AdditionnalPluginPath", "Count", "0")) - 1
    if num_plugins >= 0:
        for i in range(num_plugins):
            plug_value = 'PlugInPath{}'.format(i)
            plug_path = app_config.Get("AdditionnalPluginPath", plug_value, "")
            if not plug_path:
                continue
            current_paths.append(plug_path)
    else:
        num_plugins = 0
    current_paths = [os.path.normpath(pth) for pth in current_paths]
    if plugin_path in current_paths:
        return

    new_num_plugins = num_plugins + 1
    new_plug_value = 'PlugInPath{}'.format(new_num_plugins)
    app_config.Set("AdditionnalPluginPath", "Count", str(new_num_plugins))
    app_config.Set("AdditionnalPluginPath", new_plug_value, plugin_path, "Path Added by MAT DCC Framework")
