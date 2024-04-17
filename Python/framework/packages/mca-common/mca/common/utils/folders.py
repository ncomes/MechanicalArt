#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import fnmatch

# software specific imports

# mca python imports
import os.path


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

