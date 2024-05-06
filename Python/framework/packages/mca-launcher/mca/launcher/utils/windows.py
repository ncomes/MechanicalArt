#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactions with Qt Windows
"""

# mca python imports
import os

from PySide2.QtWidgets import QApplication, QDockWidget, QMainWindow, QWidget, QVBoxLayout
from PySide2.QtGui import QIcon
from PySide2 import QtUiTools
from PySide2.QtCore import QFile, QSettings

# software specific imports
from mca.launcher.utils import config_paths


class MCAMainWindow(QMainWindow):
    INITIAL_WIDTH_FALLBACK = 150
    INITIAL_HEIGHT_FALLBACK = 100

    def __init__(self, title, ui_path=None, version='1.0.0', style=None, parent=None, show_window=True):
        super().__init__(parent=parent)
        self.title = f'MCA {title}'
        self.single_window_instance()

        self.setWindowTitle(f'{self.title} {version}')
        mca_icon = os.path.join(config_paths.ICONS_PATH, 'mca.png')
        self.setWindowIcon(QIcon(mca_icon))

        self.ui = None

        self.setMinimumHeight(MCAMainWindow.INITIAL_HEIGHT_FALLBACK)
        self.setMinimumWidth(MCAMainWindow.INITIAL_WIDTH_FALLBACK)
        self.setContentsMargins(0, 0, 0, 0)
        if ui_path:
            loader = QtUiTools.QUiLoader()
            file = QFile(os.path.abspath(ui_path))
            if file.open(QFile.ReadOnly):
                self.ui = loader.load(file, parent)
                file.close()
                self.setCentralWidget(self.ui)
        else:
            self.central_widget = QWidget(self)
            self.main_layout = QVBoxLayout(self.central_widget)
            self.setCentralWidget(self.central_widget)
            self.main_layout.setContentsMargins(0, 0, 0, 0)

        if not style:
            style = 'incrypt'
        if style != 'custom':
            stylesheet = read_stylesheet(style)
            self.setStyleSheet(stylesheet)

        username = os.getlogin()
        self.settings = QSettings(username, self.title)
        geometry = self.settings.value('geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        if show_window:
            self.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        super().closeEvent(event)

    def single_window_instance(self):
        all_windows = get_all_mca_windows()
        if not all_windows:
            return
        for win in all_windows:
            if self.title in win.windowTitle():
                win.close()
                win.deleteLater()
                break


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
                print(f'was not able to find window a window to close.')
    return wins


def get_all_mca_windows():
    """
    Returns all open MCA windows in PySide2

    :return: Returns all open MCA windows in PySide2
    :rtype: list[PySide2]
    """

    all_windows = get_all_open_windows()
    if not all_windows:
        return
    mca_windows = [x for x in all_windows if 'MCA ' in x.windowTitle()]
    return mca_windows


def close_all_mca_windows():
    """
    Closes all MCA Windows
    """

    mca_windows = get_all_mca_windows()
    if not mca_windows:
        return
    [x.close() for x in mca_windows]
    [x.deleteLater() for x in mca_windows]


def get_all_docked_windows(parent_window):
    """
    Gets all docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """

    docked_windows = parent_window.findChildren(QDockWidget)
    return docked_windows


def get_all_mca_docked_windows(parent_window):
    """
    Gets all MCA docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """

    docked_windows = get_all_docked_windows(parent_window)
    if not docked_windows:
        return
    mca_docked_windows = [x for x in docked_windows if 'MCA' in x.windowTitle()]
    return mca_docked_windows


def close_all_mca_docked_windows(parent_window):
    """
    Closes all MCA docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """

    mca_docked_windows = get_all_mca_docked_windows(parent_window)
    if not mca_docked_windows:
        return
    [x.close() for x in mca_docked_windows]
    [x.deleteLater() for x in mca_docked_windows]


def read_stylesheet(stylesheet):
    """
    Reads and Returns the stylesheet.

    :return: Returns the stylesheet.
    :rtype: str
    """

    stylesheet = stylesheet.split('.')[0]
    style_path = os.path.join(config_paths.STYLESHEET_PATH, f'{stylesheet}.css')
    if os.path.isfile(style_path):
        with open(style_path, 'r') as f:
            return f.read()
    return
