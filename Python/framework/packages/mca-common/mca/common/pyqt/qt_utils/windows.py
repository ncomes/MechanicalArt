#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactions with Qt Windows
"""

# mca python imports
from PySide2.QtWidgets import QApplication, QDockWidget

# software specific imports

# mca python imports
from mca.common import log

logger = log.MCA_LOGGER


def get_main_qt_window():
    """
    Returns QWidget representing the top most window.

    :return: Main window found
    :rtype: QWidget or QMainWindow
    """

    parent = QApplication.activeWindow()
    grand_parent = parent
    while grand_parent is not None:
        parent = grand_parent
        grand_parent = parent.parent()

    return parent


def get_all_open_windows(skip_dialog=True):
    """
    Returns all open windows in PySide2
    
    :return: Returns all open windows in PySide2
    :rtype: list[PySide2]
    """
    
    wins = []
    top_level_widgets = QApplication.topLevelWidgets()
    for widget in top_level_widgets:
        try:
            if widget.isWindow() and not widget.isHidden():
                wins.append(widget)
        except:
            if not skip_dialog:
                logger.warning(f'was not able to find window a window to close.')
    return wins


def get_all_mca_windows():
    """
    Returns all open MAT windows in PySide2
    
    :return: Returns all open MAT windows in PySide2
    :rtype: list[PySide2]
    """
    
    all_windows = get_all_open_windows()
    if not all_windows:
        return
    mat_windows = [x for x in all_windows if 'MAT ' in x.windowTitle()]
    return mat_windows


def get_mca_window_by_name(name):
    """
    Returns a QMainWindow by its name

    :param str name: Name of a window
    :return: Returns a QMainWindow by its name
    :rtype: PySide2.QMainWindow
    """

    windows = get_all_mca_windows()
    for win in windows:
        if win == name:
            return win
    return


def close_all_mca_windows():
    """
    Closes all MAT Windows
    """
    
    mat_windows = get_all_mca_windows()
    if not mat_windows:
        return
    [x.close() for x in mat_windows]
    [x.deleteLater() for x in mat_windows]


def get_all_docked_windows(parent_window):
    """
    Gets all docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """
    
    docked_windows = parent_window.findChildren(QDockWidget)
    return docked_windows


def get_all_mca_docked_windows(parent_window):
    """
    Gets all MAT docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """
    
    docked_windows = get_all_docked_windows(parent_window)
    if not docked_windows:
        return
    mat_docked_windows = [x for x in docked_windows if 'MAT' in x.windowTitle()]
    return mat_docked_windows


def close_all_mca_docked_windows(parent_window):
    """
    Closes all MAT docked windows attached to a parent window.
    
    :param QMainWindow parent_window: The main window that the dock gets attached.
    """

    mat_docked_windows = get_all_mca_docked_windows(parent_window)
    if not mat_docked_windows:
        return
    [x.close() for x in mat_docked_windows]
    [x.deleteLater() for x in mat_docked_windows]
    
    