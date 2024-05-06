#! /usr/bin/env python
# -*- coding: utf-8 -*-

# MCA DCC Tools startup script for Autodesk MotionBuilder

from __future__ import print_function, division, absolute_import

import os
import sys
import subprocess
import json

try:
    from PySide.QtGui import QApplication, QMenuBar
except ImportError:
    from PySide2.QtWidgets import QApplication, QMenuBar

from pyfbsdk import FBSystem


fbsys = FBSystem()


def get_main_qt_window():
    parent = QApplication.activeWindow()
    grand_parent = parent
    while grand_parent is not None:
        parent = grand_parent
        grand_parent = parent.parent()

    return parent


def try_init_mat(*args, **kwargs):
    main_window = get_main_qt_window()
    if not main_window:
        return
    parent_menubar = main_window.findChild(QMenuBar)
    if not parent_menubar:
        return


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
    print('Starting MoBu!')
    root_paths = [os.path.dirname(os.path.dirname(os.getenv('COMMON_ROOT'))),
                  os.getenv('DEP_PATH')]

    for root_path in root_paths:
        root_path = os.path.abspath(root_path)
        if root_path not in sys.path:
            sys.path.append(root_path)

    print("Initializing MCA Python framework, please wait!")
    print(f'MCA Python framework Root Path: \n"{root_paths[0]}"')
    from mca.common.startup import startup
    startup.init(dcc='mobu', skip_dialog=False, hide_envs=True)


init_mca()
