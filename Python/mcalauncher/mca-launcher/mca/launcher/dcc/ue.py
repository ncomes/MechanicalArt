"""
Module that contains installer related functions for Autodesk Maya
"""

# System global imports
import os
import logging
import subprocess
# software specific imports
# mca python imports

logger = logging.getLogger('mca-launcher')


def launch(path, common_path, dependencies_folder):
    """
    Launches a new DCC executable instance.

    :param str version: Maya version we want to launch instance of
    :param str common_path: Local path to where the common folder lives
    :param str dependencies_folder: Local path to where the Dependency folder lives
    :return: Returns if the launch was successful or not
    :rtype: bool
    """

    def _launch(path):
        """
        A private function that launches a specific DCC App

        :return: Returns if the launch was successful or not
        :rtype: bool
        """

        if not path or not os.path.isfile(path):
            logger.warning(f'Unreal Project not found!  Cannot find Project file'.format(path))
            return False

        path = os.path.normpath(path)

        dcc_user_folder = os.path.join(common_path, 'startup', 'dccs', 'unreal', 'Scripts')

        script_path = os.environ.copy()
        script_path['UE_PYTHONPATH'] = dcc_user_folder
        script_path['COMMON_ROOT'] = common_path
        script_path['DEP_PATH'] = dependencies_folder
        script_path['UE_PROJECT_PATH'] = path
        subprocess.Popen([path], env=script_path, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

        return True

    return _launch(path)
