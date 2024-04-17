#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import os
import ctypes

# software specific imports
# mca python imports


def get_user_display_name():
    """
    Returns the full name of the user.

    :return: Returns the full name of the user.
    :rtype: str
    """
    
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3
    
    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)
    
    nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
    GetUserNameEx(NameDisplay, nameBuffer, size)
    return nameBuffer.value


def split_path(path):
    """
    Split the given path into directory, basename and extension.

    :param path: path we want to split.
    :return: list with the directory, file name and extension of the given path.
    :rtype: list(str)
    """

    path = os.path.normpath(path)
    filename, extension = os.path.splitext(path)

    return os.path.dirname(filename), os.path.basename(filename), extension


class ObjectDict(dict):
    """
    Wrapper of the standard Python dictionary to operate like an object.

    .. code-block:: python

            test = ObjectDict({'hello': False, 'world': u''})
            a.hello
            a.world
    """

    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        try:
            value = self[item]
            if value and isinstance(value, dict):
                return ObjectDict(**value)
            return value
        except KeyError:
            return super(ObjectDict, self).__getattribute__(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        if item in self:
            del self[item]
            return
        super(ObjectDict, self).__delattr__(item)
        

def append_path_env_var(name, value, skip_if_exists=True):
    """
    Append string path value to the end of the environment variable.

    :param str name: name of the environment variable to set.
    :param str value: value to initialize environment variable with, empty string by default.
    :param bool skip_if_exists: whether or not env var should not be added if value already exists in env var.
    """

    env_value = os.environ.get(name) or ''
    if not env_value:
        try:
            env_value = str(value)
        except Exception:
            pass
    else:
        paths = env_value.split(os.pathsep)
        if skip_if_exists and value in paths:
            return
        try:
            env_value = env_value + os.pathsep + str(value)
        except Exception:
            pass

    os.environ[name] = str(env_value)