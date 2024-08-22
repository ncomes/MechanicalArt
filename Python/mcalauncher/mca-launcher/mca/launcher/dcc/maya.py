#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains installer related functions for Autodesk Maya
"""

# System global imports
import os
import sys
import logging
import subprocess
# software specific imports
# mca python imports
from mca.launcher.utils import path_utils

logger = logging.getLogger('mca-launcher')


def get_install_path(version):
    """
    Returns directory where Maya executable file is located within the user machine.

    :param str version: Maya version we want to retrieve install directory of.
    :return: Maya absolute installation directory.
    :rtype: strs
    """

    sub_key = r'SOFTWARE\Autodesk\Maya\{}\Setup\InstallPath'.format(version)
    install_path = path_utils.get_registry_value(sub_key, 'MAYA_INSTALL_LOCATION')
    if not install_path:
        return
    return os.path.normpath(install_path)


def get_exe_path(version):
    """
    Returns path where Maya executable file is located within the user machine.

    :param str version: Maya version we want to retrieve install path of.
    :return: Maya absolute executable file path.
    :rtype: str
    """

    install_path = get_install_path(version)
    if not install_path:
        return
    exe_path = os.path.join(install_path, 'bin', 'maya.exe')
    return os.path.normpath(exe_path)


def get_interpreter_path(version):
    """
    Returns path where Maya Python interpreter is located within the user machine.

    :param str version: Maya version we want to retrieve interpreter path of.
    :return: Maya absolute interpreter path.
    :rtype: str
    """

    python_executable = sys.executable
    if os.path.basename(python_executable) == 'mayapy.exe':
        return python_executable
    elif os.path.basename(python_executable) == 'maya.exe':
        maya_py_path = os.path.join(os.path.dirname(python_executable), 'mayapy.exe')
        if os.path.isfile(maya_py_path):
            return maya_py_path

    maya_install_path = get_install_path(version)
    if not maya_install_path or not os.path.isdir(maya_install_path):
        return ''

    return os.path.join(maya_install_path, 'bin', 'mayapy.exe')


def launch(version, common_path, dependencies_folder):
    """
    Launches a new DCC executable instance.

    :param str version: Maya version we want to launch instance of
    :param str common_path: Local path to where the common folder lives
    :param str dependencies_folder: Local path to where the Dependency folder lives
    :return: Returns if the launch was successful or not
    :rtype: bool
    """

    def _launch():
        """
        A private function that launches a specific DCC App

        :return: Returns if the launch was successful or not
        :rtype: bool
        """

        interpreter_path = get_interpreter_path(version)
        if not interpreter_path or not os.path.isfile(interpreter_path):
            logger.warning('Was not possible to launch Maya because Maya interpreter was not found. Make sure Maya {} '
                           'is installed in your machine! {}'.format(version, interpreter_path))
            return False

        exe_path = get_exe_path(version)
        if not exe_path or not os.path.isfile(exe_path):
            logger.warning('Was not possible to launch Maya because Maya executable was not found. Make sure Maya {} '
                           'is installed in your machine! {}'.format(version, exe_path))
            return False

        os.environ.pop('QT_PLUGIN_PATH', None)
        os.environ.pop('QML2_IMPORT_PATH', None)
        os.environ.pop('__COMPAT_LAYER', None)
        dcc_user_folder = os.path.join(common_path, 'startup', 'dccs', 'maya', 'Scripts')

        if version <= '2024':
            depend_folder = os.path.join(dependencies_folder, 'python310')
        elif version >= '2025':
            depend_folder = os.path.join(dependencies_folder, 'python311')
        else:
            depend_folder = os.path.join(dependencies_folder, 'python310')

        script_path = os.environ.copy()
        script_path['PYTHONPATH'] = dcc_user_folder
        script_path['COMMON_ROOT'] = common_path
        script_path['DEP_PATH'] = depend_folder
        script_path['MAYA_DEP_PATH'] = os.path.join(path_utils.get_maya_dep_path(), str(version))
        subprocess.Popen([exe_path], env=script_path, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        return True

    return _launch()

