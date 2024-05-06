#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
from PySide2.QtWidgets import QMenuBar

# software specific imports

# mca python imports
from mca.common.pyqt.qt_utils import windows


def get_mobu_window():
    """
    Return the MotionBuilder main window widget as a Python object
    :return: Maya Window
    """

    return windows.get_main_qt_window()


def get_main_menubar():
    """
    Returns Qt object that references to the main DCC menubar
    :return:
    """

    win = get_mobu_window()
    menu_bar = win.findChild(QMenuBar)

    return menu_bar

