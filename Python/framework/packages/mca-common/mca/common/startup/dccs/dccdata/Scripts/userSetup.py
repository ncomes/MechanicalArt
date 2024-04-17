#! /usr/bin/env python
# -*- coding: utf-8 -*-

# MAT DCC Tools startup script for Autodesk Maya

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
    for path in output:
        result = os.listdir(path)
        if not 'mat_python.config' in result:
            continue
        mat_package = os.path.normpath(os.path.join(path, 'mat_python.config'))
        package_contents = read_json(mat_package)
        if package_contents['name'] == '# mca python importsART_DEPOT':
            art_depot = path
            os.environ['MAT_FRAMEWORK_ROOT'] = art_depot
        elif package_contents['name'] == 'MAT_DEV_DEPOT':
            dev_depot = path
            os.environ['MAT_PLASTIC_DEV_ROOT'] = dev_depot
        else:
            continue
    return [art_depot, dev_depot]


def init_mat():
    art_depot, dev_depot = startup_get_plastic_paths()
    framework_path = os.path.join(art_depot, 'DarkWinter', 'Python', 'framework')
    dependencies_path = os.path.join(framework_path, 'mca', 'dependencies', 'py3')
    os.environ['MAT_FRAMEWORK_ROOT'] = framework_path
    os.environ['MAT_DEPS_ROOT'] = dependencies_path
    os.environ['MAT_PLASTIC_ROOT'] = art_depot
    if dev_depot:
        os.environ['MAT_PLASTIC_DEV_ROOT'] = dev_depot
    else:
        os.environ['MAT_PLASTIC_DEV_ROOT'] = ''
    root_paths = [framework_path, dependencies_path]
    
    for root_path in root_paths:
        root_path = os.path.abspath(root_path)
        if root_path not in sys.path:
            sys.path.append(root_path)
    
    # python_exe_path = os.path.normpath(os.path.join(python_standalone_path, 'python.exe'))
    # print(python_exe_path)
    # venv_python = f'python -m venv {python_exe_path}'
    #
    # subprocess.Popen(venv_python, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    #
    from mca.common.startup import startup
    startup.init(dcc='dccdata', skip_dialog=False, hide_envs=True)


