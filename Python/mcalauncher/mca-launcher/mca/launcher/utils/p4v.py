"""
A window that sets the default preferences for the launcher.
"""

# System global imports
import os
import subprocess
# mca python imports
# PySide6 imports
# mca imports


def get_p4_workspaces():
    """
    Returns the workspaces from Perforce

    :return: Returns the workspaces from Perforce
    :rtype: list[str]
    """

    p4_command = 'p4 login'
    result = subprocess.Popen(p4_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    (output, error) = result.communicate()

    username = None
    user_list = list(map(lambda x: os.path.normpath(x).decode("utf-8"), output.split()[1:]))
    if user_list:
        username = user_list[0]

    if not username:
        return

    wk_cmd = f'p4 clients -u {username}'
    process = subprocess.Popen(wk_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    (output, error) = process.communicate()

    new_output = list(map(lambda x: os.path.normpath(x).decode("utf-8"), output.split()[1::1]))

    paths = []

    for path in new_output:
        if os.path.exists(path):
            paths.append(path)

    if not paths:
        return

    art_depot = None

    for path in paths:
        result = os.listdir(path)
        if 'mca_python.config' in result and art_depot is None:
            art_depot = path

    return art_depot
