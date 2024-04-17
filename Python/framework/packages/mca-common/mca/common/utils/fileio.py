#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# software specific imports

# mca python imports


# mca python imports
import os
import shutil
import stat
import time
from tempfile import mkstemp
from datetime import datetime
import subprocess

import pytz
# software specific imports

# mca python imports
from mca.common import log
from mca.common.utils import pyutils, strings

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


def get_file_text(file_path):
    """
    Returns the text stored in a file in a unique string (without parsing).
    
    :param str file_path: absolute path where the text file we want to read text from is located in disk.
    :return: read text file.
    :rtype: str
    """
    
    try:
        with open(file_path, 'r') as open_file:
            file_text = open_file.read()
    except Exception:
        return ''
    
    return file_text


def get_file_lines(file_path):
    """
    Returns the text lines from given file path in disk.
    
    :param str file_path: str, absolute file path of the file we want to read file lines from.
    :return: list of lines within given text file.
    :rtype: list(str)
    """
    
    text = get_file_text(file_path)
    if not text:
        return list()
    
    text = text.replace('\r', '')
    lines = text.split('\n')
    
    return lines


def get_file_size(file_path, round_value=2):
    """
    Returns the size of the given file.
    
    :param str file_path: path pointing to a valid file in disk.
    :param int round_value: value to round size to.
    :return: file size.
    :rtype: float
    """
    
    size = os.path.getsize(file_path)
    size_format = round(size * 0.000001, round_value)
    
    return size_format


def get_file_timestamp_in_utc(file_path):
    """
    Returns the given file stamp in UTC time (Universal Time Coordinated)
    :param str file_path: file path UTC time stamp we want to retrieve.
    :return: utc time stamp
    :rtype: str
    """
    
    local_time = datetime.utcfromtimestamp(os.path.getmtime(file_path))
    return pytz.UTC.localize(local_time)


def get_last_modified_date(file_path, reverse_date=False):
    """
    Returns the last date given file was modified.
    
    :param str file_path: file path UTC time stamp we want to retrieve.
    :param bool reverse_date: whether or not to reverse date order.
    :return: formatted date and time.
    :rtype: str
    """
    
    mtime = os.path.getatime(file_path)
    
    date_value = datetime.fromtimestamp(mtime)
    year = date_value.year
    month = date_value.month
    day = date_value.day
    
    hour = str(date_value.hour)
    minute = str(date_value.minute)
    second = str(int(date_value.second))
    
    if len(hour) == 1:
        hour = '0' + hour
    if len(minute) == 1:
        minute = '0' + minute
    if len(second) == 1:
        second = second + '0'
    
    if reverse_date:
        return '{}-{}-{}  {}:{}:{}'.format(year, month, day, hour, minute, second)
    else:
        return '{}-{}-{}  {}:{}:{}'.format(day, month, year, hour, minute, second)


def create_file(file_name, directory=None):
    """
    Creates a new file with given name inside a directory in disk.
    
    :param str file_name: name or absolute path of the new file.
    :param str or None directory: directroy where we want to create new file.
    :param bool make_unique: whether or not to make the name unique.
    :return: newly created absolute file path or None if the file was not created successfully.
    :rtype: str or None
    """
    
    directory = directory or os.path.dirname(file_name)
    file_name = os.path.basename(file_name)
    
    if directory:
        file_name = strings.clean_file_string(file_name)
        full_path = os.path.join(directory, file_name)
    else:
        file_dir = os.path.dirname(file_name)
        clean_file_name = strings.clean_file_string(os.path.basename(file_name))
        full_path = os.path.join(file_dir, clean_file_name)


    open_file = None
    try:
        open_file = open(full_path, 'a')
        open_file.close()
    except Exception:
        if open_file:
            open_file.close()
        return False
    
    #osplatform.get_permission(full_path)
    
    return full_path


def replace(file_path, pattern, subst):
    """
    Replaces one string from another string in a given file.
    
    :param str file_path: path to the file.
    :param str pattern: search to be replaced.
    :param str subst: string that will replace the old one.
    """
    
    # create temp file
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # TODO: this can give error when working with non ascii codecs
                new_file.write(line.replace(pattern, subst))
    
    # remove original file and move new file
    os.remove(file_path)
    shutil.move(abs_path, file_path)


def remove_extension(file_path):
    """
    Removes extension of the given file path
    
    :Example:
    
    >>> remove_extension(r'C:/test/file.py')
    C:/test/file
    >>> remove_extension('file.py')
    file
    
    :param str file_path: path we want to remove extension of
    :return: path without the extension
    :rtype: str
    """
    
    split_path = file_path.split('.')
    new_name = file_path
    if len(split_path) > 1:
        new_name = '.'.join(split_path[:-1])
    
    return new_name


def copy_file(file_path, file_path_destination):
    """
    Copies the given file to a new given directory.
    
    :param str file_path: file to copy with full path.
    :param str file_path_destination: destination directory where we want to copy the file into.
    :return: the new copied path.
    :rtype: str
    """
    
    # osplatform.get_permission(file_path)
    
    if os.path.exists(file_path):
        if os.path.exists(file_path_destination):
            file_name = os.path.basename(file_path)
            file_path_destination = os.path.join(file_path_destination, file_name)
        shutil.copy2(file_path, file_path_destination)
    
    return file_path_destination


def move_file(path1, path2):
    """
    Moves the file pointed by path1 under the directory path2.
    
    :param str path1: file with full path.
    :param str path2: path where path1 should be move into.
    :return: the new moved path.
    :rtype: str
    """
    
    try:
        shutil.move(path1, path2)
    except Exception:
        logger.error('Failed to move {} to {}'.format(path1, path2))
        return ''
    
    return path2


def rename_file(name, directory, new_name):
    """
    Renames the give nfile in the directory with a new name.
    
    :param str name: name of the file to remove.
    :param str directory: directory where the file to rename is located.
    :param str new_name: new file name.
    :return: new file name path.
    :rtype: str
    """
    
    full_path = os.path.join(directory, name)
    if not os.path.exists(full_path):
        return full_path
    
    new_full_path = os.path.join(directory, new_name)
    if os.path.exists(new_full_path):
        logger.warning('A file named {} already exists in the directory: {}'.format(new_name, directory))
        return full_path
    
    os.chmod(full_path, 0o777)
    os.rename(full_path, new_full_path)
    
    return new_full_path


def write_lines(file_path, lines, append=False):
    """
    Writes a list of text lines to a file. Every entry in the list is a new line.
    
    :param str file_path: str, absolute file path of the file we want to write files in.
    :param list(str) lines: list of text lines in which each entry is a new line.
    :param bool append: whether or not to append the text or replace it.
    :return: True if the write lines operation was successful; False otherwise.
    :rtype: bool
    """
    
    # permission = osplatform.get_permission(file_path)
    # if not permission:
    #     return False
    
    write_string = 'a' if append else 'w'
    
    lines = pyutils.force_list(lines)
    text = '\n'.join(map(str, lines))
    if append:
        text = '\n' + text
    
    with open(file_path, write_string) as open_file:
        open_file.write(text)
    
    return True


def write_line(file_path, line, append=False):
    """
    Writes a text line to a file.
    
    :param str file_path: str, absolute file path of the file we want to write files in.
    :param str line: text line to write.
    :param bool append: whether or not to append the text or replace it.
    :return: True if the write lines operation was successful; False otherwise.
    :rtype: bool
    """
    
    # permission = osplatform.get_permission(file_path)
    # if not permission:
    #     return False
    
    write_string = 'a' if append else 'w'
    
    if append:
        text = '\n' + line
    
    with open(file_path, write_string) as open_file:
        open_file.write('%s\n' % line)
    
    return True
