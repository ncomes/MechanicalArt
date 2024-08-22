"""
Module that contains functions related to accessing files and directories.
"""

# python imports
import os
import stat
import time
import subprocess
# software specific imports
# mca python imports
from mca.common import log

logger = log.MCA_LOGGER


def touch_path(path, remove=False):
    """
    For a given path, make sure the file or directory is valid to use. This will mark files as writable, and validate
    the directory exists to write to if the file does not exist.
    
    :param str path: A full path to a given file or directory.
    :param bool remove: If the file should be removed if it exists.
    """
    
    directory_path = os.path.dirname(path)
    if os.path.exists(directory_path):
        if os.path.isfile(path):
            os.chmod(path, stat.S_IWRITE)
            if remove:
                os.remove(path)
                time.sleep(.002)
    else:
        os.makedirs(directory_path)


def touch_and_checkout(full_path, plastic_checkout=True, remove=False):
    """
    Attempts to check out the file in plastic.

    :param str full_path: A full path to a given file or directory.
    :param bool plastic_checkout: If True, it will attempt to check out the file in plastic.
    :param bool remove: If the file should be removed if it exists.
    """
    
    if not os.path.exists(full_path):
        logger.warning(f'The path does not exist:\n{full_path}')
        return
    
    touch_path(full_path, remove)
    full_path = os.path.normpath(full_path)
    if plastic_checkout and not remove:
        cmd = f'cm co {full_path}'
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        msg = f'Attempting to checkout: {os.path.basename(full_path)}'
        logger.warning(msg)


def explore_to_path(file_path):
    """
    Touches path then opens a file browser to that directory.
    
    :param str file_path: path pointing to a file or directory.
    """
    touch_path(file_path)
    explore_path = file_path
    if os.path.isfile(file_path) or '.' in file_path:
        explore_path = os.path.dirname(file_path)

    subprocess.Popen(f'explorer "{explore_path}"')


def get_files(root_folder, full_path=False, recursive=False, pattern="*"):
    """
    Returns files found in the given folder.

    :param str root_folder: folder we want to search files on.
    :param bool full_path: whether full path to the files will be returned otherwise file names will be returned.
    :param bool recursive: whether files should be retrieved recursively.
    :param str pattern: specific pattern to filter files to retrieve by name.
    :return: list of files found in the given root folder and sub folders (if recursively is True).
    :rtype: list(str)
    """

    found = list()

    if not os.path.exists(root_folder):
        return found

    if recursive:
        for dir_path, dir_names, file_names in os.walk(root_folder):
            for file_name in fnmatch.filter(file_names, pattern):
                if full_path:
                    found.append(os.path.join(dir_path, file_name))
                else:
                    found.append(file_name)
    else:
        file_names = os.listdir(root_folder)
        for file_name in fnmatch.filter(file_names, pattern):
            file_path = os.path.join(root_folder, file_name)
            if os.path.exists(file_path):
                if full_path:
                    found.append(file_path)
                else:
                    found.append(file_name)

    return found