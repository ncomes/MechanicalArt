# python imports
import os
import logging
import re
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# mca imports
from mca.launcher.utils import path_utils, yamlio


logger = logging.getLogger('mca-launcher')


def prefs_check():
    """
    Checks if the preferences have been set.
    """

    prefs_file = path_utils.get_mca_python_root_path()
    if prefs_file:
        return True
    return False


def get_python_path_dialog():
    """
    Opens a file dialog to set the mca main python folder.
    """

    default_folder = r'C:'
    mca_dir = QFileDialog.getExistingDirectory(None,
                                                'Select directory where you want to export flag',
                                                default_folder,
                                                QFileDialog.ShowDirsOnly)
    return mca_dir


def write_prefs_path_file(mac_root_path):
    """
    Writes the preference in the documents folder.

    :param str mac_root_path: Path to the python root folder.
    """

    prefs_path = path_utils.get_prefs_file()
    if not os.path.exists(prefs_path):
        _dict = {}
        _dict['project_path'] = mac_root_path
        os.makedirs(os.path.dirname(prefs_path))
        yamlio.write_yaml(_dict, prefs_path)
        return mac_root_path

    prefs_file = yamlio.read_yaml(prefs_path)
    prefs_file['project_path'] = mac_root_path
    return mac_root_path


def read_prefs_file():
    """
    Returns the MCA python root folder from the preference in the documents folder.

    :return: Returns the MCA python root folder from the preference in the documents folder.
    :rtype: str
    """

    prefs_path = path_utils.get_prefs_file()
    prefs_data = yamlio.read_yaml(prefs_path)
    return prefs_data.get('project_path', None)


def verify_mca_project_path(mac_root_path):
    """
    Verifies that the preferences have been set correctly in the documents folder.

    :param str mac_root_path: Path to the python root folder.
    :return: If True, the preferences have been set correctly.
    :rtype: bool
    """

    if not os.path.exists(mac_root_path):
        return False
    if not os.path.exists(os.path.join(mac_root_path, 'mca_python.config')):
        return False
    return True


def verify_mca_engine_path(mac_root_path):
    """
    Verifies that the preferences have been set correctly in the documents folder.

    :param str mac_root_path: Path to the python root folder.
    :return: If True, the preferences have been set correctly.
    :rtype: bool
    """

    if not os.path.exists(mac_root_path):
        return False
    if not os.path.exists(os.path.join(mac_root_path, 'mca_dev_python.config')):
        return False
    return True


def get_autodesk_version(autodesk_app, approved_versions):
    """
    Returns all the versions of a specific autodesk product installed on this machine.

    :param str autodesk_app: Name of a specific autodesk product.
    :param list(int) approved_versions: List of all approved versions.
    :return: Returns all the versions of a specific autodesk product installed on this machine.
    :rtype: list[str]
    """

    versions = []
    path = None
    for version in approved_versions:
        path = path_utils.get_maya_install_path(version)
        if path:
            break
    if not path:
        path = r'C:\Program Files\Autodesk'
    else:
        path = os.path.dirname(path)

    dirs = [x for x in os.listdir(path) if autodesk_app in x and 'USD' not in x]
    for _dir in dirs:
        versions.append(re.findall(r'\d+', _dir)[0])
    return versions


def get_maya_versions():
    """
    Returns all the versions of Maya installed on this machine.

    :return: Returns all the versions of Maya installed on this machine.
    :rtype: list[str]
    """

    approved_versions = get_dcc_versions('maya')
    verified_versions = []
    versions = get_autodesk_version('Maya', approved_versions)
    versions = [x for x in versions if x in approved_versions]
    for version in versions:
        bin_path = os.path.join(path_utils.get_maya_install_path(version), 'bin')
        if not os.path.exists(bin_path):
            continue
        exe = [x for x in os.listdir(bin_path) if 'maya.exe' == str(x)]
        if exe:
            verified_versions.append(version)

    return verified_versions


def get_mobu_versions():
    """
    Returns all the versions of MotionBuilder installed on this machine.

    :return: Returns all the versions of MotionBuilder installed on this machine.
    :rtype: list[str]
    """

    approved_versions = get_dcc_versions('mobu')
    verified_versions = []
    versions = get_autodesk_version('MotionBuilder', approved_versions)
    versions = [x for x in versions if x in approved_versions]
    for version in versions:
        bin_path = os.path.join(path_utils.get_mobu_install_path(version), 'bin', 'x64')
        if not os.path.exists(bin_path):
            continue
        exe = [x for x in os.listdir(bin_path) if 'motionbuilder.exe' == str(x)]
        if exe:
            verified_versions.append(version)

    return verified_versions


def get_dcc_versions(dcc_name):
    """
    Gets the dcc versions from the package.yaml file.

    :param str dcc_name: Name of the DCC software
    :return: Returns the compatible dcc versions.
    :rtype: str
    """

    from mca.launcher.utils import config_paths
    mat_package_dict = yamlio.read_yaml(config_paths.INFO_PACKAGE)
    versions = mat_package_dict['dcc_versions'].get(dcc_name, None)
    return versions
