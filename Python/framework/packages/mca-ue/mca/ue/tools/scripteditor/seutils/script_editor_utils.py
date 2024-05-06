# -*- coding: utf-8 -*-

"""
Saving preferences for the script_editor
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca.common.paths import paths
from mca.common.textio import yamlio
from mca.common.startup.configs import consts


LOCAL_PREFS_FILE = 'script_editor.config'


def get_local_prefs_folder(dcc):
    """
    Returns the folder where the local script_editor prefs lives.

    :param str dcc: the dcc software
    :return: Returns the folder where the local script_editor prefs lives.
    :rtype: str
    """

    prefs_folder = paths.get_dcc_prefs_folder(dcc=dcc)
    dcc_folder = os.path.join(prefs_folder, f'ScriptEditor')
    return os.path.normpath(dcc_folder)


def create_local_prefs_folder(dcc):
    """
    Creates the folder where the local script_editor prefs lives.

    :param str dcc: the dcc software
    :return: Returns the folder where the local script_editor prefs lives.
    :rtype: str
    """

    script_editor_folder = get_local_prefs_folder(dcc=dcc)
    if not os.path.exists(script_editor_folder):
        os.makedirs(script_editor_folder)
    return script_editor_folder


def get_local_prefs_file(dcc):
    """
    Creates the File where the local script_editor prefs lives.

    :param str dcc: the dcc software
    :return: Returns the file where the local script_editor prefs lives.
    :rtype: str
    """

    prefs_folder = create_local_prefs_folder(dcc=dcc)
    prefs_file = os.path.join(prefs_folder, LOCAL_PREFS_FILE)
    if not os.path.isfile(prefs_file):
        yamlio.write_to_yaml_file([], prefs_file)
    return os.path.normpath(prefs_file)
