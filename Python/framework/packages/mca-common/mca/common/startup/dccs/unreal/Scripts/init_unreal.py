#! /usr/bin/env python
# -*- coding: utf-8 -*-

# MCA DCC Tools startup script for Unreal Engine

import os
import sys


def init_mca():
    root_paths = [os.path.dirname(os.path.dirname(os.getenv('COMMON_ROOT'))),
                  os.getenv('DEP_PATH')]

    for root_path in root_paths:
        root_path = os.path.abspath(root_path)
        if root_path not in sys.path:
            sys.path.append(root_path)

    from mca.common.startup import startup
    startup.init(dcc='ue', skip_dialog=False, hide_envs=True)

    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)


from importlib import reload

init_mca()

