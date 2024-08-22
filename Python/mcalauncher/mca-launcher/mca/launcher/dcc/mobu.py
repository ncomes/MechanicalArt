
"""
Module that contains installer related functions for Autodesk MotionBuilder
"""

import os
import logging
import subprocess

from mca.launcher.utils import path_utils, config_paths, yamlio

logger = logging.getLogger('mca-launcher')


def get_install_path(version):
    """
    Returns directory where MotionBuilder executable file is located within the user machine.

    :param str version: version of MotionBuilder we want to retrieve install directory of.
    :return: MotionBuilder absolute installation directory.
    :rtype: str
    """

    sub_key = r'SOFTWARE\Autodesk\MotionBuilder\{}'.format(version)
    install_path = path_utils.get_registry_value(sub_key, 'InstallPath')
    if not install_path:
        return
    return os.path.normpath(install_path)


def get_exe_path(version):
    """
    Returns path where MotionBuilder executable file is located within the user machine.

    :param str version: MotionBuilder version we want to retrieve install path of.
    :return: Maya absolute executable file path.
    :rtype: str
    """

    install_path = get_install_path(version)
    if not install_path:
        return
    return os.path.join(install_path, 'bin', 'x64', 'motionbuilder.exe')


def launch(version, common_path, dependencies_folder):
    """
    Launches a new MotionBuilder executable instance.

    :param str version: MotionBuilder version we want to launch instance of.
    """

    def _launch(startup_file=None):
        exe_path = get_exe_path(version)
        if not exe_path or not os.path.isfile(exe_path):
            logger.warning('Was not possible to launch MotionBuilder because Mobu executable was not found. Make sure '
                           'MotionBuilder {} is installed in your machine! {}'.format(version, exe_path))
            return False

        if startup_file and os.path.isfile(startup_file):
            cmd = [exe_path, path_utils.clean_path(startup_file)]
        else:
            cmd = [exe_path]

        # those inherited env vars were causing problems with Mobu 2022
        os.environ.pop('QT_PLUGIN_PATH', None)
        os.environ.pop('QML2_IMPORT_PATH', None)
        os.environ.pop('__COMPAT_LAYER', None)
        dcc_user_folder = os.path.join(common_path, 'startup', 'dccs', 'mobu', 'Scripts')

        script_path = os.environ.copy()
        script_path['PYTHONPATH'] = dcc_user_folder
        script_path['COMMON_ROOT'] = common_path
        script_path['DEP_PATH'] = dependencies_folder
        subprocess.Popen([exe_path, path_utils.clean_path(startup_file)], env=script_path, stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)

        return True

    dcc_user_folder = os.path.join(common_path, 'startup', 'dccs', 'mobu', 'Scripts')
    dcc_user_folder = os.path.normpath(dcc_user_folder)
    if not os.path.isdir(dcc_user_folder):
        logger.warning(f'Was not possible to launch Mobu {version} '
                       f'because Mobu bootstrap folder was not found: {dcc_user_folder}')
        logger.debug('Launching Mobu without loading MCA DCC framework ...')

        return _launch()
    startup_file = os.path.join(dcc_user_folder, 'startup.py')
    return _launch(startup_file)


def get_mca_package():
    """
    Gets the package.yaml file.

    :return: Returns the mca_package file.
    :rtype: dictionary
    """

    mca_package_path = os.path.join(config_paths.ROOT_PATH, 'mca_package.yaml')
    mca_package_dict = yamlio.read_yaml(mca_package_path)
    return mca_package_dict

