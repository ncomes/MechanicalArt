#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import pathlib
import os
# software specific imports

# MCA python imports
from mca.common.paths import project_paths
from mca.common import log


logger = log.MCA_LOGGER


def get_sub_dirs(rootdir):
    """
    Returns a directory and all it's subdirectories.

    :param path rootdir: A directory with sub folders.
    :return: Returns a directory and all it's subdirectories.
    :rtype: list[str]
    """

    dirs = []
    for path in pathlib.Path(rootdir).iterdir():
        if path.is_dir():
            dirs.append(os.path.normpath(path))
            get_sub_dirs(path)
    return dirs


def all_folders_in_directory(rootdir, folder_name=None):
    """
    Returns a full path of folders that are embedded in directories.
    if you provide a folder name, it will prove you with that folder name

    :param path rootdir: A directory with sub folders.
    str folder_name: A folder name without the full path.  Just the name
    :return: Returns a full path of folders that are embedded in directories.
    :rtype: list[path] or path
    """

    all_folders = []
    for root, dirs, files in os.walk(rootdir):
        # select file name
        for folder in dirs:
            if folder_name and folder_name in folder:
                return os.path.join(root, folder)
            all_folders.append(os.path.join(root, folder))
    return all_folders


def all_files_in_directory(rootdir, file_name=None):
    """
    Returns a full path of folders that are embedded in directories.

    :param path rootdir: A directory with sub folders.
    :param str file_name: A file name without the full path.  Just the name
    :return: Returns a full path of folders that are embedded in directories.
    :rtype: list[path] or path
    """

    all_files = []
    for root, dirs, files in os.walk(rootdir):
        # select file name
        for file in files:
            if file_name and file_name in file:
                return os.path.join(root, file)
            all_files.append(os.path.join(root, file))
    if file_name and file_name not in all_files:
        return
    return all_files


def all_file_types_in_directory(rootdir, file_ext):
    """
    Returns a full path files that are embedded in directories.

    :param path rootdir: A directory with sub folders.
    :param str file_ext: file type.
    :return: Returns a full path files that are embedded in directories.
    :rtype: list[path]
    """

    all_files = []
    for root, dirs, files in os.walk(rootdir):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith(file_ext):
                # print whole path of files
                all_files.append(os.path.join(root, file))
    return all_files


def to_relative_path(file_path):
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
    seperator = os.path.split(project_paths.get_mca_root_path())[-1]
    split_path = file_path.split(seperator)[-1]
    return split_path if not split_path.startswith('\\') else split_path[1:]


def to_full_path(file_path):
    """
    Convert a path to a full path relative our project path start.

    :param str file_path: A relative file path from our project path.
    :return: The full file path using the project path as the start.
    :rtype: str
    """

    if not file_path:
        return ''
    file_path = os.path.normpath(file_path)
    if not file_path.startswith(os.path.normpath(project_paths.MCA_PROJECT_ROOT)):
        # Make sure it's not a full path before we return it.
        seperator = os.path.split(project_paths.MCA_PROJECT_ROOT)[-1]
        split_path = file_path.split(seperator)[-1]
        split_path = split_path if not split_path.startswith('\\') else split_path[1:]
        return os.path.join(os.path.normpath(project_paths.MCA_PROJECT_ROOT), split_path)
    else:
        return file_path

