"""
Module that functions to retrieve info from running processes
"""

# System global imports
from __future__ import print_function, division, absolute_import
import threading
import os
import ctypes
# mca python imports
from mca.common import log

PSUTIL_AVAILABLE = True
try:
    import psutil
except ImportError:
    PSUTIL_AVAILABLE = False

logger = log.MCA_LOGGER


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

def check_if_process_is_running(process_name):
    """
    Returns whether a process with given name is running.

    :param str process_name: name of the process we want to check.
    :return: True if a process with given name is running; False otherwise.
    :rtype: bool
    """

    if not PSUTIL_AVAILABLE:
        logger.warning(
            'Impossible to run "check_if_process_is_running" function because psutil module is not available!')
        return False

    for process in psutil.process_iter():
        try:
            if process_name.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


def get_processes_by_name(process_name):
    """
    Returns a list with all running processes with given name.

    :param str process_name: name of the process to retrieve.
    :return: list of found processes with given name.
    :rtype: list
    """

    if not PSUTIL_AVAILABLE:
        logger.warning('Impossible to run "get_processes_by_name" function because psutil module is not available!')
        return False

    return [process for process in psutil.process_iter() if process_name.lower() == process.name().lower()]


def kill_processes_by_name(process_name):
    """
    Kill processes with given name.

    :param str process_name: name of th process to kill.
    :return: True if process was killed; False otherwise.
    :rtype: bool
    """

    if not PSUTIL_AVAILABLE:
        logger.warning('Impossible to run "kill_process_by_name" function because psutil module is not available!')
        return False

    found_processes = get_processes_by_name(process_name)
    if not found_processes:
        return False

    for found_process in found_processes:
        found_process.kill()

    return True


def get_current_process_name():
    """
    Returns the name of the current process.

    :return: current process name.
    :rtype: str
    """

    if not PSUTIL_AVAILABLE:
        logger.warning(
            'Impossible to run "get_current_process_name" function because psutil module is not available!')
        return ''

    return psutil.Process().name()


def cpu_threading(fn):
    """
    Runs a function on a separate CPU thread
    :param callable fn: Threaded function.
    """

    t = threading.Thread(target=fn)
    t.start()

