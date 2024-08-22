"""
MCA DCC Tools startup script for Autodesk Maya
"""

import os
import sys
import subprocess
import json
# maya imports
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya


root_paths = [os.path.dirname(os.path.dirname(os.getenv('COMMON_ROOT'))), os.getenv('DEP_PATH'),
              os.getenv('MAYA_DEP_PATH')]

for root_path in root_paths:
    root_path = os.path.abspath(root_path)
    if root_path not in sys.path:
        sys.path.append(root_path)


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


def init_mca():
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

