#! /usr/bin/env python
# -*- coding: utf-8 -*-

# MAT DCC Tools startup script for Autodesk MotionBuilder

import os
import sys
import subprocess
import json


def read_json(file_name):
    # Python program to read
    # json file
    
    path = file_name
    
    # Opening JSON file
    f = open(path)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()
    return data


def startup_get_plastic_paths():
    """
    Returns the path to the plastic art content folder.

    :return: Returns the path to the plastic art content folder.
    :rtype: str
    """

    process = subprocess.Popen('cm workspace list', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = process.communicate()
    output = list(map(lambda x: os.path.normpath(x).decode("utf-8"), output.split()[1::2]))
    art_depot = None
    dev_depot = None
    framework_path = None
    for path in output:
        result = os.listdir(path)
        if not 'mat_python.config' in result:
            continue
        mat_package = os.path.normpath(os.path.join(path, 'mat_python.config'))
        package_contents = read_json(mat_package)
        if package_contents['name'] == '# mca python importsART_DEPOT':
            art_depot = path
            os.environ['MAT_FRAMEWORK_ROOT'] = art_depot
            framework_path = package_contents.get('frameworkPath')
            print(f'Starting Framework:\n{framework_path}')
        elif package_contents['name'] == 'MAT_DEV_DEPOT':
            dev_depot = path
            os.environ['MAT_PLASTIC_DEV_ROOT'] = dev_depot
        else:
            continue
    return [art_depot, dev_depot, framework_path]


def init_mat():
    art_depot, dev_depot, framework_path = startup_get_plastic_paths()
    if not art_depot:
        return

    framework_path = os.path.join(art_depot, framework_path)
    common_root = os.path.join(framework_path, 'packages', 'mca-common')
    common_path = os.path.join(common_root, 'mca', 'common')
    dependencies_path = os.path.join(common_path, 'startup', 'dependencies', 'py3')
    os.environ['MAT_FRAMEWORK_ROOT'] = framework_path
    os.environ['MAT_DEPS_ROOT'] = dependencies_path
    os.environ['MAT_PLASTIC_ROOT'] = art_depot
    if dev_depot:
        os.environ['MAT_PLASTIC_DEV_ROOT'] = dev_depot
    else:
        os.environ['MAT_PLASTIC_DEV_ROOT'] = ''
    root_paths = [common_root, dependencies_path]

    for root_path in root_paths:
        root_path = os.path.abspath(root_path)
        if root_path not in sys.path:
            sys.path.append(root_path)

    from mca.common.startup import startup
    startup.init(dcc='ue', skip_dialog=False, hide_envs=True)

    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)


from importlib import reload

init_mat()


