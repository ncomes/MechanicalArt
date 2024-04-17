#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module starts Maya
"""

# mca python imports
import os
import psutil
import requests
import subprocess

# software specific imports
from mca.common.startup.configs import consts
from mca.common.textio import jsonio

# mca python imports

API_URL = 'http://localhost:9090/api/v1'

class _REST(object):

    def _get(url, *args, **kwargs):
        # response.status_code == 200
        response = requests.get(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def GET(url, rest=_get):
        def decorate(fn):
            fn.REST = (url, rest)
            return fn
        return decorate


def is_plastic_server_running():
    """
    Returns whether Plastic server is running.

    :return: True if Plastic server is running; False otherwise.
    :rtype: bool
    """

    server_running = False
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == 'cm.exe':
                server_running = True
                print('Killing Plastic Server')
                proc.kill()
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return server_running


def run_plastic_server():
    """
    Runs a new plastic server if it is not already running.
    """
    print('Checking Plastic Server')
    server_running = is_plastic_server_running()
    #if not server_running:
    subprocess.Popen(['cm', 'api'], stdout=subprocess.PIPE, creationflags=0x08000000)
    print('Started Plastic Server')


def get_plastic_content_path(create_env=True):
    """
    Returns the path to the plastic art content folder.  If the environment variable is not set, it will set it.

    :param bool create_env: If True, the path will be registered into an env var.
    :return: Returns the path to the plastic art content folder.
    :rtype: str
    """

    art_depot = os.environ.get(consts.PLASTIC_ROOT, None)
    dev_depot = os.environ.get(consts.PLASTIC_DEV_ROOT, None)
    if not art_depot or not dev_depot:
        output = subprocess.check_output('cm workspace list', shell=True)
        output = list(map(lambda x: os.path.normpath(x).decode("utf-8"), output.split()[1::2]))
        for project_root in output:
            result = os.listdir(project_root)
            if not consts.START_CONFIG in result:
                continue
            mat_package = os.path.normpath(os.path.join(project_root, consts.START_CONFIG))
            package_contents = jsonio.read_json_file(mat_package)
            if package_contents['name'] == '# mca python importsART_DEPOT':
                art_depot = project_root
            elif package_contents['name'] == '# mca python importsDEV_DEPOT':
                dev_depot = project_root
            else:
                continue
            if create_env:
                os.environ[consts.PLASTIC_ROOT] = art_depot
                if dev_depot:
                    os.environ[consts.PLASTIC_DEV_ROOT] = dev_depot
    return [art_depot, dev_depot]
