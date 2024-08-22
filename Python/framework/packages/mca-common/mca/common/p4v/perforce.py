"""
Module that contains functions for interacting with p4v.
"""

# mca python imports
import subprocess
import winreg
# software specific imports
# Project python imports
from mca.common.modifiers import singleton


class P4Info(singleton.SimpleSingleton):
    """
    Singleton class that handles the user/workspace/port information of a given user. Singleton usage reduces the time
    To get this information on each p4 op. Which are slow to begin with.
    """
    user = None
    workspace = None
    port = None

    def __init__(self):
        key_val = r'SOFTWARE\Perforce\Environment'
        sub_key_list = [['P4CLIENT', 'workspace'], ['P4USER', 'user'], ['P4PORT', 'port']]
        try:
            key = winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), key_val)
            for sub_key, dict_key in sub_key_list:
                try:
                    found_data = [x for x in winreg.QueryValueEx(key, sub_key)][0].split(', ')
                    if not found_data:
                        found_data = [x for x in winreg.QueryValueEx(key, sub_key.lower())][0].split(', ')
                    if found_data:
                        setattr(self, dict_key, found_data[0])
                except:
                    logger.error(f'CRITICAL ERROR: Open and close your Connection >> Environment Settings in p4, ensure "Use current connection for environment settings" is checked. Unable to find registry key. {sub_key}')
                    return
        except:
            logger.debug(f'CRITICAL ERROR: Install perforce, primary registry key is missing.')
            return

def p4_describe_cl(cl_val):
    p4_info = P4Info()
    if not p4_info:
        return {}

    p4_cmd = f'P4 describe {cl_val}'
    cl_info = subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read().decode()
    replace_str_list = [' ...', '... ', '\t']
    for replace_str in replace_str_list:
        cl_info = cl_info.replace(replace_str, '')
    cl_info = [x for x in cl_info.split('\r\n') if x]
    info_dict = {}
    try:
        info_dict['changelist'] = cl_info[0].split(' ')[1]
        info_dict['description'] = cl_info[1]
        info_dict['files'] = [x.split('#')[0] for x in cl_info[3:]]
    except:
        pass
    return info_dict

def p4_get_pending():
    """
    Grab a dictionary of all local pending changelists.

    :return: A dictionary containing all pending changelists.
    :rtype: dict
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    cl_info_dict = {}
    p4_cmd = f'P4 -p {p4_info.port} changes -c {p4_info.workspace} -s pending'
    cl_info = subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()
    for x in cl_info:
        entry_str = x.decode("utf-8")
        cl_number = entry_str.split(' ')[1]
        info_dict = p4_describe_cl(cl_number)
        cl_info_dict[cl_number] = info_dict.get('description')
    return cl_info_dict


def p4_add(cl_val, file_path):
    """
    Adds a file to a given changelist as an add.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param str file_path: The absolute path to a given file.
    """
    p4_info = P4Info()
    if not p4_info:
        return

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} add -c {cl_val} {file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def p4_delete(cl_val, file_path):
    """
    Adds a file to a given changelist as a delete.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param str file_path: The absolute path to a given file.
    """
    p4_info = P4Info()
    if not p4_info:
        return

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} delete -c {cl_val} {file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def p4_edit(cl_val, file_path):
    """
    Adds a file to a given changelist as an edit.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param str file_path: The absolute path to a given file.
    """
    p4_info = P4Info()
    if not p4_info:
        return

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} edit -c {cl_val} {file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def p4_reopen(cl_val, file_path):
    """
    Moves a checked out file from one changelist to another.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param str file_path: The absolute path to a given file.
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} reopen -c {cl_val} {file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def p4_reconcile(cl_val, file_path):
    """
    Correctly checks out a file using the appropriate operation to a given changelist.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param str file_path: The absolute path to a given file.
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} reconcile -c {cl_val} {file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def p4_revert(file_path, safe=True):
    """
    Reverts a file if it is checked out.

    :param str file_path: The absolute path to a given file.
    :param bool safe: If only safe reverts should be performed. Will only revert unchanged files.
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} revert -k {"-a " if safe else ""}{file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def p4_sync(file_path, force=False):
    """
    Correctly checks out a file using the appropriate operation to a given changelist.

    :param str file_path: The absolute path to a given file.
    :param bool force: If the file should be forcefully sunk. (revert, force to head)
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    if force:
        # If we're forcing this revert the file before syncing.
        p4_revert(file_path, safe=False)

    p4_cmd = f'P4 -p {p4_info.port} -c {p4_info.workspace} sync {"-f " if force else ""}{file_path}'
    subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def p4_create_cl(cl_discript='pysc: New Pending Changelist'):
    """
    Create a new changelist or find an existing changelist with the same description.

    :param str cl_discript: The description of the new changelist.
    :return: The CL number of the found or newly created changelist.
    :rtype: str
    """
    p4_info = P4Info()
    if not p4_info:
        return {}

    for cl_num, description in p4_get_pending().items():
        if cl_discript == description:
            return cl_num

    p4_cmd = f'p4 -p {p4_info.port} -c {p4_info.workspace} --field "Description={cl_discript}" --field "Files=" change -o | p4 change -i'
    return subprocess.Popen(p4_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()[0].decode("utf-8").split(' ')[1]

def checkout(cl_val, file_path_list, force=True):
    """
    Using p4 reconcile preform the correct operation on a given file and add it to the passed CL.
    Easy onestop shop to handle all p4 commands on a list of files.

    NOTES: You need to edit a file for this to trigger an add or edit. It will not mark a file if it is unchanged.

    :param str cl_val: Unique int value as a string which represents a changelist.
    :param list(str) file_path_list: A list of the absolute path to a given file.
    :param bool force: If files should be moved to the specified changelist even if already checked out on a different one.
    """
    if not isinstance(file_path_list, list):
        file_path_list = [file_path_list]

    for file_path in file_path_list:
        p4_reconcile(cl_val, file_path)
        if force:
            p4_reopen(cl_val, file_path)

def sync_files(file_path_list, force=False):
    """
    Sync the list of files to the head revision, optionally forcibly doing so.

    :param list(str) file_path_list: A list of absolute paths to be sunk.
    :param bool force: Forcibly revert and sync the files to the head revision.
    """
    if not isinstance(file_path_list, list):
        file_path_list = [file_path_list]

    for file_path in file_path_list:
        p4_sync(file_path, force)