"""
Module that contains utilities functions to verify dccs.
"""

# python imports
import os
import sys
import math
from collections import OrderedDict
# software specific imports
# mca python imports
from mca.common import log


# cached current DCC name. It should not be modified during a session.
CURRENT_DCC = None
DEFAULT_DCC_PORT = 65500

# cached used to store all the reroute paths done during a session. It should not be modified during a session.
DCC_REROUTE_CACHE = dict()


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


logger = log.MCA_LOGGER


class CallbackTypes(object):
    """
    Class that defines all the different supported callback types
    """

    Shutdown = 'Shutdown'
    Tick = 'Tick'
    ScenePreCreated = 'ScenePreCreated'
    ScenePostCreated = 'ScenePostCreated'
    SceneNewRequested = 'SceneNewRequested'
    SceneNewFinished = 'SceneNewFinished'
    SceneSaveRequested = 'SceneSaveRequested'
    SceneSaveFinished = 'SceneSaveFinished'
    SceneOpenRequested = 'SceneOpenRequested'
    SceneOpenFinished = 'SceneOpenFinished'
    UserPropertyPreChanged = 'UserPropertyPreChanged'
    UserPropertyPostChanged = 'UserPropertyPostChanged'
    NodeSelect = 'NodeSelect'
    NodeAdded = 'NodeAdded'
    NodeDeleted = 'NodeDeleted'
    ReferencePreLoaded = 'ReferencePreLoaded'
    ReferencePostLoaded = 'ReferencePostLoaded'


class Dccs(object):
    """
    Class that defines all available Dccs
    """

    Standalone = 'standalone'
    Maya = 'mya'
    MotionBuilder = 'mobu'
    Unreal = 'unreal'
    Houdini = 'houdini'
    Max = '3dsmax'
    Blender = 'blender'
    SubstancePainter = 'painter'

    ALL = [Maya, MotionBuilder, Unreal, Houdini, Blender, SubstancePainter]

    names = OrderedDict([
        (Maya, 'Maya'),
        (MotionBuilder, 'MotionBuilder'),
        (Unreal, 'Unreal'),
        (Houdini, 'Houdini'),
        (Max, '3dsMax'),
        (Blender, 'Blender'),
        (SubstancePainter, 'SubstancePainter')
    ])

    packages = OrderedDict([
        ('mya', Maya),
        ('pyfbsdk', MotionBuilder),
        ('unreal', Unreal),
        ('hou', Houdini),
        ('MaxPlus', Max),
        ('pymxs', Max),
        ('bpy', Blender),
        ('substance_painter', SubstancePainter)
    ])

    executables = {
        Maya: {'Windows': ['mya.exe']},
        MotionBuilder: {'Windows': ['motionbuilder.exe']},
        Unreal: {'Windows': ['UE4Editor.exe']},
        Houdini: {'Windows': ['hou.exe']},
        Max: {'Windows': ['3dsmax.exe']},
        Blender: {'Windows': ['blender.exe']},
        SubstancePainter: {'Windows': ['painter.exe']}
    }

    ports = {
        Standalone: DEFAULT_DCC_PORT,               # 65500
        Maya: DEFAULT_DCC_PORT + 1,                 # 65501
        MotionBuilder: DEFAULT_DCC_PORT + 2,        # 65502
        Houdini: DEFAULT_DCC_PORT + 3,              # 65503
        Max: DEFAULT_DCC_PORT + 4,                  # 65504
        Blender: DEFAULT_DCC_PORT + 5,              # 65505
        SubstancePainter: DEFAULT_DCC_PORT + 6,     # 65506
        Unreal: 30010                               # Default Unreal Remote Server Plugin port
    }


class DccCallbacks(object):
    """
    Class that defines all available Dcc callbacks
    """

    Shutdown = (CallbackTypes.Shutdown, {'type': 'simple'})
    Tick = (CallbackTypes.Tick, {'type': 'simple'})
    ScenePreCreated = (CallbackTypes.ScenePreCreated, {'type': 'simple'})
    ScenePostCreated = (CallbackTypes.ScenePostCreated, {'type': 'simple'})
    SceneNewRequested = (CallbackTypes.SceneNewRequested, {'type': 'simple'})
    SceneNewFinished = (CallbackTypes.SceneNewFinished, {'type': 'simple'})
    SceneSaveRequested = (CallbackTypes.SceneSaveRequested, {'type': 'simple'})
    SceneSaveFinished = (CallbackTypes.SceneSaveFinished, {'type': 'simple'})
    SceneOpenRequested = (CallbackTypes.SceneOpenRequested, {'type': 'simple'})
    SceneOpenFinished = (CallbackTypes.SceneOpenFinished, {'type': 'simple'})
    UserPropertyPreChanged = (CallbackTypes.UserPropertyPreChanged, {'type': 'filter'})
    UserPropertyPostChanged = (CallbackTypes.UserPropertyPostChanged, {'type': 'filter'})
    NodeSelect = (CallbackTypes.NodeSelect, {'type': 'filter'})
    NodeAdded = (CallbackTypes.NodeAdded, {'type': 'filter'})
    NodeDeleted = (CallbackTypes.NodeDeleted, {'type': 'filter'})
    ReferencePreLoaded = (CallbackTypes.ReferencePreLoaded, {'type': 'simple'})
    ReferencePostLoaded = (CallbackTypes.ReferencePostLoaded, {'type': 'simple'})


def callbacks():
    """
    Return a full list of callbacks based on DccCallbacks dictionary.

    :return: list of available callbacks.
    :rtype: list(str)
    """

    new_list = list()
    for k, v in DccCallbacks.__dict__.items():
        if k.startswith('__') or k.endswith('__'):
            continue
        new_list.append(v[0])

    return new_list


def is_python2():
    """
    Returns whether current version is Python 2

    :return: bool
    """

    return sys.version_info[0] == 2


def is_python3():
    """
    Returns whether current version is Python 3

    :return: bool
    """

    return sys.version_info[0] == 3


def is_in_maya(executable=None):
    """
    Returns whether current running executable is Maya

    :param str executable: optional executable name.
    :return: True if we are running Maya executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("maya", "maya.exe", "maya.bin")
    return os.path.basename(executable).endswith(ends_with_key)


def is_mayapy(executable=None):
    """
    Returns whether current running executable is Mayapy.

    :param str executable: optional executable name.
    :return: True if we are running MayaPy executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("mayapy", "mayapy.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def is_maya_batch(executable=None):
    """
    Returns whether current running executable is Maya batch.

    :param str executable: optional executable name.
    :return: True if we are running MayaBatch executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("mayabatch", "mayabatch.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def is_maya(executable=None):
    """
    Combines all Maya executable checkers.

    :param str executable: optional executable name.
    :return: True if we are running Maya (or its variant) executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("maya", "maya.exe", "maya.bin", "mayapy", "mayapy.exe", "mayabatch", "mayabatch.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def is_in_3dsmax(executable=None):
    """
    Returns whether current running executable is 3ds Max.

    :param str executable: optional executable name.
    :return: True if we are running 3ds Max executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("3dsmax", "3dsmax.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def is_in_motionbuilder(executable=None):
    """
    Returns whether current running executable is MotionBuilder.

    :param str executable: optional executable name.
    :return: True if we are running MotionBulder executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("motionbuilder", "motionbuilder.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def is_in_houdini(executable=None):
    """
    Returns whether current running executable is Houdini.

    :param str executable: optional executable name.
    :return: True if we are running Houdini executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = ("houdini", "houdinifx", "houdinicore", "happrentice")
    return os.path.basename(executable).endswith(ends_with_key)


def is_in_blender(executable=None):
    """
    Returns whether current running executable is Blender.

    :param str executable: optional executable name.
    :return: True if we are running Blender executable; False otherwise.
    :rtype: bool
    """

    try:
        import bpy
        if type(bpy.app.version) == tuple:
            return True
    except ImportError or AttributeError:
        return False


def is_in_unreal(executable=None):
    """
    Returns whether current running executable is Unreal.

    :param str executable: optional executable name.
    :return: True if we are running Unreal executable; False otherwise.
    :rtype: bool
    """

    executable = (executable or sys.executable).lower()
    ends_with_key = (
        "unreal", "unreal.exe", "ue4_editor", "ue4_editor.exe", "ue5_editor", "ue5_editor.exe", "unrealeditor.exe")
    return os.path.basename(executable).endswith(ends_with_key)


def application():
    """
    Returns the currently running application.

    :return: application manager is running on.
    """

    if any((is_in_maya(), is_mayapy(), is_maya_batch())):
        return "Maya"
    elif is_in_3dsmax():
        return "3dsmax"
    elif is_in_motionbuilder():
        return "Mobu"
    elif is_in_houdini():
        return "Houdini"
    elif is_in_blender():
        return "Blender"
    elif is_in_unreal():
        return "Unreal"
    return "standalone"


def application_version(dcc_name=None):
    """
    Returns the version of the currently running application.

    :return: version as a string.
    :rtype: str
    """

    dcc_name = dcc_name or application()

    version = ''
    if dcc_name.lower() == 'maya':
        import maya.cmds
        version = int(maya.cmds.about(version=True))
    elif dcc_name.lower() == 'mobu':
        import pyfbsdk
        version =  int(2000 + math.ceil(pyfbsdk.FBSystem().Version / 1000.0))
    elif dcc_name.lower() == 'unreal':
        import unreal
        version = '.'.join(unreal.SystemLibrary.get_engine_version().split('+++')[0].split('-')[0].split('.')[:-1])

    return str(version)


def get_venv_linked_packages_paths(venv_path):
    """
    Returns all linked paths located within a created Python virtual environment.

    :param str venv_path: root folder where virtual environment folder should be located
    :return:
    """

    dependency_paths = list()

    if not os.path.isdir(venv_path):
        return dependency_paths

    packages_folder = os.path.join(venv_path, 'Lib', 'site-packages')
    if not os.path.isdir(packages_folder):
        return dependency_paths

    dependency_paths = [packages_folder]

    for file_name in os.listdir(packages_folder):
        if not file_name.endswith('.egg-link'):
            continue
        egg_path = os.path.join(packages_folder, file_name)
        with open(egg_path) as egg_file:
            dependency_path = egg_file.readline().rstrip()
            if dependency_path in dependency_paths:
                continue
            if not os.path.isdir(dependency_path):
                logger.warning(
                    'Dependency found in egg-link file points to an invalid directory: {}. Skipping...'.format(
                        dependency_path))
                continue
            dependency_paths.append(dependency_path)

    return dependency_paths

