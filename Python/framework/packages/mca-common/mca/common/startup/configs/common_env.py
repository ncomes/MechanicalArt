#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca import common
from mca.common import log
from mca.common.textio import packages, yamlio
from mca.common.paths import project_paths
from mca.common.startup.configs import consts, config


logger = log.MCA_LOGGER


def read_package(key, package_file=None):
    if not package_file:
        package_file = common.MCA_PACKAGE

    package_dict = config.read_config_file(package_file)
    package_result = package_dict.get(key)
    package_path = os.path.normpath(package_result.replace('{self}', project_paths.get_mca_package_path()))
    return package_path


def create_path_envs():
    """
    Creates all the path envs from the project paths in the documents preference files.
    """

    prefs = project_paths.MCAProjectPrefs.load()
    if not os.path.exists(prefs.project_path):
        return
    prefs.set_as_envs()


def create_project_envs(skip_dialog=True):
    """
    Sets up the projects main environment variables

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    # Set project root env.
    project_root = project_paths.get_mca_package_path()
    if not skip_dialog:
        logger.info(f'MCA_PROJECT_ROOT environment variable -path to the art depot folder- set to:\n{project_root}')


def create_tools_envs(skip_dialog=True):
    """
    Sets up the framework environment variables

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    # Set project root env.
    package_path = project_paths.get_mca_package_path()
    if not skip_dialog:
        logger.info(f'MCA_PACKAGE_PATH environment variable -path to the package folder- set to:\n{package_path}')


def create_common_envs(skip_dialog=True):
    """
    Sets up the Common depot environment variables

    :param bool skip_dialog: If True, nothing will be written to the console.
    """

    package_manager = packages.ProjectPackageManager()

    # Set base Common path env.
    os.environ[consts.MCA_COMMON_PATH] = common.TOP_ROOT
    if not skip_dialog:
        logger.info(f'{consts.MCA_COMMON_PATH} environment variable -path to the base common folder- set to:'
                    f'\n{common.TOP_ROOT}')

    # Set base Common path env.
    configs_folder = os.path.join(common.COMMON_PATH, 'configs')
    os.environ[consts.MCA_COMMON_PATH] = configs_folder
    if not skip_dialog:
        logger.info(f'{consts.MCA_CONFIGS_PATH} environment variable -path to the configs folder- set to:'
                    f'\n{configs_folder}')


def remove_all_mca_envs():
    """
    Removes all MCA Environment Variables

    :return: Returns a list of environment variables that get removed.
    :rtype: list[]
    """

    env_list = []
    for k, v in sorted(os.environ.items()):
        if 'MCA_' in k:
            env_list.append(k)
            del os.environ[k]
    return env_list

