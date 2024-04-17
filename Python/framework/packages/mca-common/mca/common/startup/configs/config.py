#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reads the configs file and sets the sys.paths
"""

# mca python imports
import os
import sys

# software specific imports

# mca python imports
from mca.common import log
from mca.common.textio import yamlio
from mca.common.paths import project_paths, path_utils
from mca.common.startup.configs import consts

logger = log.MCA_LOGGER
CONFIG_DICT = None


def read_config_file(config_file):
    """
    Reads the config file - This is a file that states what directories should be loaded.
    :param config_file:
    :return: Returns a dictionary of the config file
    :rtype: Dictionary
    """

    if not os.path.exists(config_file):
        logger.warning(f'the config file: {config_file} - does not exist')
        return

    config_data = yamlio.read_yaml_file(config_file)
    return config_data


def get_config_packages(config_file, dcc='maya', skip_dialog=False):
    """
    Returns the paths that need to be registered in the sys paths.

    :param str config_file: a yaml file with the directories data.
    :param bool skip_dialog: if true, the warning will not be displayed.
    :return: Returns the paths that need to be registered in the sys paths.
    :rtype: list[list[str], list[str]]
    """

    # get the config file.  Should be located at the top level directory
    if not config_file:
        config_file = project_paths.get_package_python_config_path()

    # make sure the config file is in yaml format
    if not isinstance(config_file, dict):
        config_file = yamlio.read_yaml_file(config_file)

    # The yaml file starts with mca_directories.  Lets strip that namespace out.
    directories = config_file.get('mca_directories', None)

    if not directories:
        if not skip_dialog:
            logger.warning('The config file does not have the directories data.')
        return False

    # Get the root path to the pacakges
    package_folder = project_paths.get_mca_package_path()

    loaded = []
    dir_paths = []

    # Now we loop through and find the software we want to load and put together the package paths
    # that need to be loaded
    package_name = None
    for software in directories.keys():
        if software == dcc:
            package_name = software
            break
    if not package_name:
        return [None, None]

    depots = directories[package_name].get('depots', None)
    if depots:
        loaded = loaded + depots
    for depot in depots:
        dir_path = os.path.normpath(os.path.join(package_folder, depot))
        if not os.path.exists(dir_path):
            continue
        dir_paths.append(dir_path)
    return [dir_paths, loaded]


def create_sys_packages(config_file, dcc='maya', skip_dialog=False):
    """
    Sets the sys paths

    :param str config_file: a yaml file with the directories data.
    :param bool skip_dialog: if true, the warning will not be displayed.
    :return: Returns a list of package paths that get registered.
    :rtype: list[str]
    """

    directories, loaded = get_config_packages(config_file, dcc=dcc, skip_dialog=False)
    dir_paths = []
    for dir_path in directories:
        if dir_path not in sys.path:
            sys.path.append(dir_path)
        dir_paths.append(dir_path)

    if loaded:
        if not skip_dialog:
            logger.warning(f'These packages were loaded and ready to be imported.\n'
                            f'{loaded}')
    return dir_paths


def remove_sys_packages(config_file, dcc='maya', skip_dialog=False):
    """

    :param str config_file: a yaml file with the directories data.
    :param bool skip_dialog: if true, the warning will not be displayed.
    :return: Returns a list of environment variables that get removed.
    :rtype: list[]
    """

    directories, loaded = get_config_packages(config_file, dcc=dcc, skip_dialog=False)

    unloaded = []
    for dir_path in directories:
        if os.path.exists(dir_path) and dir_path in sys.path:
            unloaded.append(dir_path)
            sys.path.remove(dir_path)

    deps_path = os.environ[consts.MCA_DEPEND_PATH]

    if deps_path and os.path.isdir(deps_path):
        if deps_path in sys.path:
            sys.path.remove(deps_path)
            if not skip_dialog:
                logger.info(f'Dependencies path unregistered: {path_utils.to_relative_path(deps_path)}')

    if unloaded:
        if not skip_dialog:
            logger.info(f'Unloading Packages: {", ".join(unloaded)}')
    else:
        if not skip_dialog:
            logger.info(f'No Packages were unloaded.  No packages found in the sys.path')

    return unloaded


def remove_sys_path(path_list, skip_dialog=False):
    """
    Removes paths from the sys.path

    :param list[path]/path path_list:
    :param bool skip_dialog: if true, the warning will not be displayed.
    """

    if not isinstance(path_list, (list, tuple)):
        path_list = [path_list]
    for path in path_list:
        if path and os.path.isdir(path):
            if path in sys.path:
                sys.path.remove(path)
                if not skip_dialog:
                    logger.info(f'System path unregistered: {path_utils.to_relative_path(path)}')


def reload_modules():
    """
    Function that forces the reloading of all MAT related modules
    """

    modules_to_reload = ('mca', 'studioqt', 'studiolibrary', 'studiovendor')

    for k in sys.modules.copy().keys():
        found = False
        for mod in modules_to_reload:
            if mod == k:
                del sys.modules[mod]
                found = True
                break
        if found:
            continue
        if k.startswith(modules_to_reload):
            del sys.modules[k]


class ProjectPackageManager:
    def __init__(self, package_file):
        self.package_dict = read_config_file(package_file)

    @property
    def get_env_paths(self):
        return self.package_dict.get('environment')

    @property
    def mca_path(self):
        return os.path.normpath(self.get_env_paths['MCA_PATH'].replace('{self}', project_paths.get_mca_package_path()))

    @property
    def common_path(self):
        return os.path.normpath(self.get_env_paths['MCA_COMMON_PATH'].replace('{self}', self.mca_path))

    @property
    def dependencies_path(self):
        return os.path.normpath(self.get_env_paths['MCA_DEPEND_PATH'].replace('{self}', self.mca_path))

    @property
    def maya_path(self):
        return os.path.normpath(self.get_env_paths['MCA_MAYA_PATH'].replace('{self}', self.mca_path))

    @property
    def mobu_path(self):
        return os.path.normpath(self.get_env_paths['MCA_MOBU_PATH'].replace('{self}', self.mca_path))

    @property
    def resources_path(self):
        return os.path.normpath(self.get_env_paths['MCA_RESOURCES_PATH'].replace('{self}', self.mca_path))

    @property
    def icons_path(self):
        return os.path.normpath(self.get_env_paths['MCA_ICONS_PATH'].replace('{self}', self.mca_path))

    @property
    def images_path(self):
        return os.path.normpath(self.get_env_paths['MCA_IMAGES_PATH'].replace('{self}', self.mca_path))

    @property
    def styles_path(self):
        return os.path.normpath(self.get_env_paths['MCA_STYLES_PATH'].replace('{self}', self.mca_path))

    @property
    def fonts_path(self):
        return os.path.normpath(self.get_env_paths['MCA_FONTS_PATH'].replace('{self}', self.mca_path))

    @property
    def common_startup_path(self):
        return os.path.normpath(self.get_env_paths['MCA_COMMON_STARTUP'].replace('{self}', self.mca_path))

    @property
    def project_url(self):
        return self.package_dict.get('project_url')

    @property
    def animation_url(self):
        return self.package_dict.get('animation_url')

    @property
    def modeling_url(self):
        return self.package_dict.get('modeling_url')

    @property
    def rigging_url(self):
        return self.package_dict.get('rigging_url')

    @property
    def jira_url(self):
        return self.package_dict.get('jira_url')

    @property
    def dcc_setup_url(self):
        return self.package_dict.get('dcc_setup_url')
