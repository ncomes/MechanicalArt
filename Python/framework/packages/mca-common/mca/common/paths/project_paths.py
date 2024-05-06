#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import ctypes
import ctypes.wintypes
import os
import winreg

# software specific imports

# mca python imports
from mca.common import log
from mca.common.textio import yamlio, jsonio
from mca.common.startup.configs import consts

logger = log.MCA_LOGGER


def get_documents_folder(absolute=True):
    """
    Returns the path to the user folder.

    :return: path to the user folder.
    :rtype: path
    """

    CSIDL_PERSONAL = 5  # My Documents
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

    documents_folder = os.path.normpath(os.path.abspath(buf.value) if absolute else buf.value)
    return documents_folder


def get_local_preferences_folder():
    """
    Returns the path to the user's mca preferences folder.

    :return: path to the user's mca preferences folder.
    :rtype: str
    """

    docs_folder = get_documents_folder()
    prefs_folder = os.path.join(docs_folder, consts.MCA_LOCAL_PREFS)  # 'mca_preferences'
    return os.path.normpath(prefs_folder)


def get_local_project_preferences():
    return os.path.join(get_local_preferences_folder(), 'prefs', 'project', consts.MCA_LOCAL_PREFS_FILE)


def get_mca_root_path():
    """
    Returns the root path if the prefs exist.

    :return: Returns the root path if the prefs exist.
    :rtype: str
    """

    prefs_file = get_local_project_preferences()
    if not os.path.exists(prefs_file):
        logger.error(f'Project Preferences not found! {prefs_file}')
        return
    prefs_data = yamlio.read_yaml_file(prefs_file)
    if not prefs_data.get(consts.MCA_PROJECT_PATH, None):
        logger.error(f'No Project Preferences Path Set!')
        return
    root = os.path.normpath(prefs_data[consts.MCA_PROJECT_PATH])
    if not os.path.exists(root):
        logger.error(f'No Root Path Preferences Set!')
        return

    return root


ROOT_PATH = get_mca_root_path()


def get_project_path():
    """
    Returns the path to the folder before the Python folder.  If the environment variable is not set, it will set it.

    :return: Returns the path to the folder before the Python folder.
    :rtype: str
    """

    return os.environ.get(consts.MCA_PROJECT_PATH, None)


MCA_PROJECT_ROOT = get_project_path()


def get_package_dict():
    """
    Returns the Project Info yaml file.

    :return: Returns the Project Info yaml file.
    :rtype: dictionary
    """

    config_file = os.path.normpath(os.path.join(MCA_PROJECT_ROOT, consts.MCA_PACKAGE_BOOTS))
    return jsonio.read_json_file(config_file)


def get_framework_path():
    """
    Returns the path to the framework folder.  If the environment variable is not set, it will set it.
    :return: Returns the path to the framework folder.
    :rtype: str
    """

    return os.getenv(consts.MCA_FRAMEWORK_PATH, None)


def get_mca_package_path():
    """
    Returns the path to the mca root folder.  If the environment variable is not set, it will set it.
    :return: Returns the path to the mca root folder.
    :rtype: path
    """

    return os.environ.get(consts.MCA_PACKAGES_PATH, None)


def get_common_root_path():
    """
    Returns the path to the common root folder.  If the environment variable is not set, it will set it.

    :return: Returns the path to the mca root folder.
    :rtype: path
    """

    common_path = os.environ.get(consts.MCA_COMMON_PATH, None)
    return os.path.dirname(os.path.dirname(common_path))


def get_dependencies_path():
    """
    Returns the path to the dependencies folder.  If the environment variable is not set, it will set it.

    :return: Returns the path to the dependencies folder.
    :rtype: path
    """
    depend_paths = os.environ.get(consts.MCA_DEPEND_PATH, None)
    depend_list = depend_paths.split(',')
    return depend_list


def get_package_python_config_path():
    """
    Returns the path to the master config file.

    :return: Returns the path to the master config file.
    :rtype: str
    """

    project_config = os.environ.get(consts.MCA_PACKAGES_PATH, None)
    project_config = os.path.join(project_config, consts.MCA_PACKAGE_BOOTS)
    if not os.path.exists(project_config):
        logger.error('Was not possible to retrieve the config path folder in the plastic directory.')
        return

    return os.path.normpath(project_config)


def get_registry_value(sub_key, key_name, from_user_register=False):
    """
    Returns a value from the Windows register.

    :param str sub_key: register sub key.
    :param str key_name: register name.
    :param bool from_user_register: whether to retrieve the registry value from user register or from local machine.
    :return: register value.
    :rtype: str
    """

    try:
        register = winreg.HKEY_LOCAL_MACHINE if not from_user_register else winreg.HKEY_CURRENT_USER
        key = winreg.OpenKey(register, sub_key, 0, winreg.KEY_READ)
        value = winreg.QueryValueEx(key, key_name)[0]
    except Exception as exc:
        logger.warning(f'Was not possible to retrieve value from register: {sub_key} ({key_name}) | {exc}')
        return None

    return value


class MCAProjectPrefs:
    def __init__(self, data=None):
        self._data = data
        if not self._data:
            self._data = self.default_preferences()

    def default_preferences(self):
        depend_path = os.path.join(r'boot\dependencies', consts.MCA_DEPEND_FOLDER)
        prefs = {}
        prefs.update({consts.MCA_PROJECT_PATH: r''})
        prefs.update({consts.MCA_FRAMEWORK_PATH: r'Python\framework'})
        prefs.update({consts.MCA_PACKAGES_PATH: r'packages'})
        prefs.update({consts.MCA_COMMON_PATH: r'mca-common\mca\common'})
        prefs.update({consts.MCA_DEPEND_PATH: [depend_path]})
        prefs.update({consts.MCA_MAYA_PATH: r'mca-maya\mca\mya'})
        prefs.update({consts.MCA_MOBU_PATH: r'mca-mobu\mca\mobu'})
        prefs.update({consts.MCA_BLENDER_PATH: r'mca-blender\mca\blnd'})
        prefs.update({consts.MCA_UNREAL_PATH: r'mca-ue\mca\ue'})
        prefs.update({consts.MCA_RESOURCES_PATH: r'resources'})
        prefs.update({consts.MCA_ICONS_PATH: r'icons'})
        prefs.update({consts.MCA_IMAGES_PATH: r'images'})
        prefs.update({consts.MCA_STYLES_PATH: r'styles'})
        prefs.update({consts.MCA_FONTS_PATH: r'fonts'})
        prefs.update({consts.MCA_COMMON_STARTUP: r'startup\startup.py'})
        prefs.update({consts.MCA_COMMON_FOLDER: r'Common'})
        prefs.update({consts.MCA_COMMON_TOOLS: r'Tools'})
        prefs.update({consts.MCA_ART_DEPOT: r'Art'})
        prefs.update({consts.MCA_PROJECT_NAME: r'MechanicalArt'})
        prefs.update({consts.MCA_ENGINE_DEPOT: r'UE5'})

        return prefs

    @property
    def data(self):
        return self._data

    @property
    def project_name(self):
        return self._data.get(consts.MCA_PROJECT_NAME, None)

    @project_name.setter
    def project_name(self, value):
        self._data.update({consts.MCA_PROJECT_NAME: value})

    @property
    def project_path(self):
        return self._data.get(consts.MCA_PROJECT_PATH, None)

    @project_path.setter
    def project_path(self, value):
        self._data.update({consts.MCA_PROJECT_PATH: value})

    @property
    def engine_path(self):
        path = self._data.get(consts.MCA_ENGINE_DEPOT, None)
        return os.path.normpath(os.path.join(self.project_path, path))

    @engine_path.setter
    def engine_path(self, value):
        relative_path = self.to_relative_path(value, self.project_path)
        self._data.update({consts.MCA_ENGINE_DEPOT: relative_path})

    @property
    def common_folder(self):
        path = self._data.get(consts.MCA_COMMON_FOLDER, None)
        return os.path.normpath(os.path.join(self.project_path, path))

    @common_folder.setter
    def common_folder(self, value):
        relative_path = self.to_relative_path(value, self.project_path)
        self._data.update({consts.MCA_COMMON_FOLDER: relative_path})

    @property
    def common_tools(self):
        path = self._data.get(consts.MCA_COMMON_TOOLS, None)
        return os.path.normpath(os.path.join(self.common_folder, path))

    @common_tools.setter
    def common_tools(self, value):
        relative_path = self.to_relative_path(value, self.common_folder)
        self._data.update({consts.MCA_COMMON_TOOLS: relative_path})

    @property
    def framework_path(self):
        framework_path = self._data.get(consts.MCA_FRAMEWORK_PATH, None)
        return os.path.normpath(os.path.join(self.project_path, framework_path))

    @framework_path.setter
    def framework_path(self, value):
        relative_path = self.to_relative_path(value, self.project_path)
        self._data.update({consts.MCA_FRAMEWORK_PATH: relative_path})

    @property
    def packages_path(self):
        packages_path = self._data.get(consts.MCA_PACKAGES_PATH, None)
        return os.path.normpath(os.path.join(self.framework_path, packages_path))

    @packages_path.setter
    def packages_path(self, value):
        relative_path = self.to_relative_path(value, self.framework_path)
        self._data.update({consts.MCA_PACKAGES_PATH: relative_path})

    @property
    def common_path(self):
        path = self._data.get(consts.MCA_COMMON_PATH, None)
        return os.path.normpath(os.path.join(self.packages_path, path))

    @common_path.setter
    def common_path(self, value):
        relative_path = self.to_relative_path(value, self.packages_path)
        self._data.update({consts.MCA_COMMON_PATH: relative_path})

    @property
    def depend_paths(self):
        paths = self._data.get(consts.MCA_DEPEND_PATH, None)
        depend_paths = []
        for path in paths:
            depend_paths.append(os.path.join(self.common_path, path))
        return depend_paths

    @depend_paths.setter
    def depend_paths(self, value):
        depend_paths = []
        for path in value:
            depend_paths.append(self.to_relative_path(path, self.common_path))
        self._data.update({consts.MCA_DEPEND_PATH: depend_paths})

    @property
    def maya_path(self):
        path = self._data.get(consts.MCA_MAYA_PATH, None)
        return os.path.normpath(os.path.join(self.packages_path, path))

    @maya_path.setter
    def maya_path(self, value):
        relative_path = self.to_relative_path(value, self.packages_path)
        self._data.update({consts.MCA_MAYA_PATH: relative_path})

    @property
    def mobu_path(self):
        path = self._data.get(consts.MCA_MOBU_PATH, None)
        return os.path.normpath(os.path.join(self.packages_path, path))

    @mobu_path.setter
    def mobu_path(self, value):
        relative_path = self.to_relative_path(value, self.packages_path)
        self._data.update({consts.MCA_MOBU_PATH: relative_path})

    @property
    def ue_path(self):
        path = self._data.get(consts.MCA_UNREAL_PATH, None)
        return os.path.normpath(os.path.join(self.packages_path, path))

    @ue_path.setter
    def ue_path(self, value):
        relative_path = self.to_relative_path(value, self.packages_path)
        self._data.update({consts.MCA_UNREAL_PATH: relative_path})

    @property
    def resources_path(self):
        path = self._data.get(consts.MCA_RESOURCES_PATH, None)
        return os.path.normpath(os.path.join(self.common_path, path))

    @resources_path.setter
    def resources_path(self, value):
        relative_path = self.to_relative_path(value, self.common_path)
        self._data.update({consts.MCA_RESOURCES_PATH: relative_path})

    @property
    def icons_path(self):
        path = self._data.get(consts.MCA_ICONS_PATH, None)
        return os.path.normpath(os.path.join(self.resources_path, path))

    @icons_path.setter
    def icons_path(self, value):
        relative_path = self.to_relative_path(value, self.resources_path)
        self._data.update({consts.MCA_ICONS_PATH: relative_path})

    @property
    def images_path(self):
        path = self._data.get(consts.MCA_IMAGES_PATH, None)
        return os.path.normpath(os.path.join(self.resources_path, path))

    @images_path.setter
    def images_path(self, value):
        relative_path = self.to_relative_path(value, self.resources_path)
        self._data.update({consts.MCA_IMAGES_PATH: relative_path})

    @property
    def styles_path(self):
        path = self._data.get(consts.MCA_STYLES_PATH, None)
        return os.path.normpath(os.path.join(self.resources_path, path))

    @styles_path.setter
    def styles_path(self, value):
        relative_path = self.to_relative_path(value, self.resources_path)
        self._data.update({consts.MCA_STYLES_PATH: relative_path})

    @property
    def fonts_path(self):
        path = self._data.get(consts.MCA_FONTS_PATH, None)
        return os.path.normpath(os.path.join(self.resources_path, path))

    @fonts_path.setter
    def fonts_path(self, value):
        relative_path = self.to_relative_path(value, self.resources_path)
        self._data.update({consts.MCA_FONTS_PATH: relative_path})

    @property
    def startup_path(self):
        path = self._data.get(consts.MCA_COMMON_STARTUP, None)
        return os.path.normpath(os.path.join(self.common_path, path))

    @startup_path.setter
    def startup_path(self, value):
        relative_path = self.to_relative_path(value, self.common_path)
        self._data.update({consts.MCA_COMMON_STARTUP: relative_path})

    @property
    def art_depot_paths(self):
        path = self._data.get(consts.MCA_ART_DEPOT, None)
        return os.path.normpath(os.path.join(self.project_path, path))

    @art_depot_paths.setter
    def art_depot_paths(self, value):
        relative_path = self.to_relative_path(value, self.project_path)
        self._data.update({consts.MCA_ART_DEPOT: relative_path})

    def to_relative_path(self, file_path, relative_path):
        """
        Convert a path to a project relative path by replacing the project path start.

        :param str file_path: A full path to a given file.
        :return: A path replacing the project path.
        :rtype: str
        """

        if not file_path:
            return None
        file_path = os.path.normpath(file_path)
        # strip the leading slashes here or we won't be able to join the paths later.
        seperator = relative_path
        split_path = file_path.split(seperator)[-1]
        return split_path if not split_path.startswith('\\') else split_path[1:]

    def save(self):
        prefs_path = os.path.join(get_local_preferences_folder(), 'prefs', 'project')
        if not os.path.exists(prefs_path):
            os.makedirs(prefs_path)
        prefs_file =  os.path.join(prefs_path, consts.MCA_LOCAL_PREFS_FILE)
        yamlio.write_to_yaml_file(self._data, prefs_file)

    @classmethod
    def load(cls):
        prefs_path = os.path.join(get_local_preferences_folder(), 'prefs', 'project')
        if not os.path.exists(prefs_path):
            return cls()

        prefs_file = os.path.join(prefs_path, consts.MCA_LOCAL_PREFS_FILE)
        return cls(yamlio.read_yaml_file(prefs_file))

    def set_as_envs(self):

        depend_paths = ','.join(self.depend_paths)

        os.environ[consts.MCA_PROJECT_PATH] = self.project_path
        os.environ[consts.MCA_FRAMEWORK_PATH] = self.framework_path
        os.environ[consts.MCA_PACKAGES_PATH] = self.packages_path
        os.environ[consts.MCA_COMMON_PATH] = self.common_path
        os.environ[consts.MCA_DEPEND_PATH] = depend_paths
        os.environ[consts.MCA_MAYA_PATH] = self.maya_path
        os.environ[consts.MCA_MOBU_PATH] = self.mobu_path
        os.environ[consts.MCA_UNREAL_PATH] = self.ue_path
        os.environ[consts.MCA_RESOURCES_PATH] = self.resources_path
        os.environ[consts.MCA_ICONS_PATH] = self.icons_path
        os.environ[consts.MCA_IMAGES_PATH] = self.images_path
        os.environ[consts.MCA_STYLES_PATH] = self.styles_path
        os.environ[consts.MCA_COMMON_STARTUP] = self.startup_path
        os.environ[consts.MCA_FONTS_PATH] = self.fonts_path
        os.environ[consts.MCA_ART_DEPOT] = self.art_depot_paths
        os.environ[consts.MCA_COMMON_FOLDER] = self.common_folder
        os.environ[consts.MCA_COMMON_TOOLS] = self.common_tools
        os.environ[consts.MCA_PROJECT_NAME] = self.project_name
        os.environ[consts.MCA_ENGINE_DEPOT] = self.engine_path
