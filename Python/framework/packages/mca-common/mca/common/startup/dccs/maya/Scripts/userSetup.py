#! /usr/bin/env python
# -*- coding: utf-8 -*-

# MAT DCC Tools startup script for Autodesk Maya

import os
import sys
import subprocess
import json
#
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

try:
    import pymel.core as pm
    OpenMaya.MGlobal.displayInfo("\n\nPyMel was found and is installed!\n\n")
except:
    OpenMaya.MGlobal.displayInfo("PyMel was not found!  Attempting to install...")
    path = os.path.dirname(sys.executable)
    subprocess.check_call(['mayapy', '-m', 'pip', 'install', 'pymel'],
                            cwd=path,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)
try:
    import pymel.core as pm
except:
    OpenMaya.MGlobal.displayInfo("PyMel Not able to be installed!  Please see Rigging Tech Art!")
    pass


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


def get_common_root():
    """
    Returns the path to the plastic art content folder.

    :return: Returns the path to the plastic art content folder.
    :rtype: str
    """

    this_path = os.path.dirname(os.path.realpath(__file__))
    common_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(this_path))))
    common_root = os.path.dirname(os.path.dirname(common_path))
    return [common_root, common_path]


def init_mca():
    root_paths = [os.path.dirname(os.path.dirname(os.getenv('COMMON_ROOT'))),
                  os.getenv('DEP_PATH')]
    
    for root_path in root_paths:
        root_path = os.path.abspath(root_path)
        if root_path not in sys.path:
            sys.path.append(root_path)

    OpenMaya.MGlobal.displayInfo("Initializing MCA Python framework, please wait!")
    OpenMaya.MGlobal.displayInfo(f'MCA Python framework Root Path: \n"{root_paths[0]}"')
    from mca.common.startup import startup
    startup.init(dcc='maya', skip_dialog=False, hide_envs=True)
    

def sl1():
    selection = pm.selected()
    if not selection:
        return
    return selection[0]

from importlib import reload



if __name__ == '__main__':
     cmds.evalDeferred(init_mca)

