#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MCA
"""

# mca python imports
import os

# software specific imports
# mca python imports
from mca.common.paths import paths


def maya_default_preferences_path():
    prefs_folder = paths.get_dcc_prefs_folder('maya')
    default_paths = os.path.join(prefs_folder, 'default_options')
    if not os.path.exists(default_paths):
        os.makedirs(default_paths)
    return os.path.normpath(default_paths)


def get_default_preferences_file():
    default_path = maya_default_preferences_path()
    file_path = os.path.join(default_path, 'maya_default_options.prefs')
    return os.path.normpath(file_path)

