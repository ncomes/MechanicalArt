"""
Defined paths for the Launcher
"""

# System global imports
import ctypes.wintypes
import logging
import os
import winreg
# PySide2 imports
# Software specific imports
# mca python imports
from mca.launcher.utils import yamlio, consts


logger = logging.getLogger('mca-launcher')


SEPARATOR = '/'
BAD_SEPARATOR = '\\'
PATH_SEPARATOR = '//'
SERVER_PREFIX = '\\'
RELATIVE_PATH_PREFIX = './'
BAD_RELATIVE_PATH_PREFIX = '../'
WEB_PREFIX = 'https://'


def get_documents_folder(absolute=True):
    """
    Returns the path to the user folder.

    :return: path to the user folder.
    :rtype: str
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


def get_prefs_file():
    return os.path.join(get_local_preferences_folder(), consts.MCA_LOCAL_PREFS_PATH, consts.MCA_LOCAL_PREFS_FILE)


def get_mca_python_root_path():
    prefs_file = get_prefs_file()
    if not os.path.exists(prefs_file):
        logger.error(f'Project Preferences not found! {prefs_file}')
        return
    prefs_data = yamlio.read_yaml(prefs_file)
    if not prefs_data.get(consts.MCA_PROJECT_PATH, None):
        logger.error(f'No Project Preferences Path Set!')
        return
    root = os.path.normpath(prefs_data[consts.MCA_PROJECT_PATH])
    if not os.path.exists(root):
        logger.error(f'No Root Path Preferences Set!')
        return

    return root


def get_mca_root_path():
    return os.path.dirname(get_mca_python_root_path())


def get_framework_path():
    """
    Returns the path to the Framework folder.  The folder above the packages folders.

    :return: Returns the path to the Framework folder.  The folder above the packages folders.
    :rtype: str
    """

    framework_path = os.path.normpath(os.path.join(get_mca_python_root_path(), 'Python', 'framework'))
    if not os.path.exists(framework_path):
        logger.warning(f'Could not find the framework folders. {framework_path}')
        return

    paths = os.path.normpath(framework_path)
    return paths


def get_package_path():
    """
    Returns the path to the packages folder.

    :return: Returns the path to the packages folder.
    :rtype: str
    """

    path = os.path.normpath(os.path.join(get_framework_path(), 'packages'))
    if not os.path.exists(path):
        logger.warning(f'Could not find the packages folders. {path}')
        return

    paths = os.path.normpath(path)
    return paths


def get_common_root():

    package_path = get_package_path()
    common_root = os.path.join(package_path, 'mca-common')
    return os.path.normpath(common_root)


def get_common_path():
    package_path = get_common_root()
    common_path = os.path.join(package_path, 'mca', 'common')
    return os.path.normpath(common_path)


def get_launcher_path():
    """
    Returns the path to the top level of the launcher directory.  - This directory.

    :return: Returns the path to the top level of the launcher directory.  - This directory.
    :rtype: str
    """

    package_path = get_package_path()
    if not package_path:
        return
    launcher_path = os.path.join(package_path, 'mca-launcher', 'mca', 'launcher')
    return os.path.normpath(launcher_path)


def get_dependencies_path():
    """
    Returns the path to the dependencies package/folder.

    :return: Returns the path to the dependencies package/folder.
    :rtype: str
    """

    common_path = get_common_path()
    if not common_path:
        return
    dependency_path = os.path.join(common_path, 'startup', 'dependencies', 'python310')
    if not os.path.isdir(dependency_path):
        logger.error(f'Was not possible to retrieve the dependencies folder.  {dependency_path}')
        raise RuntimeError()
    return os.path.normpath(dependency_path)


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


def get_launcher_local_prefs_folder():
    """
    Returns the folder where the local Launcher prefs lives.

    :return: Returns the folder where the local Launcher prefs lives.
    :rtype: str
    """

    prefs_folder = get_local_preferences_folder()
    dcc_folder = os.path.join(prefs_folder, f'Launcher')
    return os.path.normpath(dcc_folder)


def create_launcher_local_prefs_folder():
    """
    Creates the folder where the local toolbox prefs lives.

    :return: Returns the folder where the local toolbox prefs lives.
    :rtype: str
    """

    launcher_folder = get_launcher_local_prefs_folder()
    if not os.path.exists(launcher_folder):
        os.makedirs(launcher_folder)
    return launcher_folder


def clean_path(path):
    """
    Cleans a path. Useful to resolve problems with slashes

    :param str path: A str path
    :return:clean path
    :rtype: str
    """

    if not path:
        return

    # We convert '~' Unix character to user's home directory
    path = os.path.expanduser(str(path))

    # Remove spaces from path and fixed bad slashes
    path = os.path.normpath(path.strip())

    # Fix server paths
    is_server_path = path.startswith(SERVER_PREFIX)
    while SERVER_PREFIX in path:
        path = path.replace(SERVER_PREFIX, PATH_SEPARATOR)
    if is_server_path:
        path = PATH_SEPARATOR + path

    # Fix web paths
    if not path.find(WEB_PREFIX) > -1:
        path = path.replace(PATH_SEPARATOR, SEPARATOR)

    return path


def get_mobu_install_path(version):
    """
    Returns directory where MotionBuilder executable file is located within the user machine.

    :param str version: version of MotionBuilder we want to retrieve install directory of.
    :return: MotionBuilder absolute installation directory.
    :rtype: str
    """

    sub_key = r'SOFTWARE\Autodesk\MotionBuilder\{}'.format(version)
    install_path = get_registry_value(sub_key, 'InstallPath')
    if not install_path:
        return
    return os.path.normpath(install_path)


def get_maya_install_path(version):
    """
    Returns directory where Maya executable file is located within the user machine.

    :param str version: Maya version we want to retrieve install directory of.
    :return: Maya absolute installation directory.
    :rtype: strs
    """

    sub_key = r'SOFTWARE\Autodesk\Maya\{}\Setup\InstallPath'.format(version)
    install_path = get_registry_value(sub_key, 'MAYA_INSTALL_LOCATION')
    if not install_path:
        return
    return os.path.normpath(install_path)


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
        yamlio.write_yaml(self._data, prefs_file)

    @classmethod
    def load(cls):
        prefs_path = os.path.join(get_local_preferences_folder(), 'prefs', 'project')
        if not os.path.exists(prefs_path):
            return cls()

        prefs_file = os.path.join(prefs_path, consts.MCA_LOCAL_PREFS_FILE)
        return cls(yamlio.read_yaml(prefs_file))

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
