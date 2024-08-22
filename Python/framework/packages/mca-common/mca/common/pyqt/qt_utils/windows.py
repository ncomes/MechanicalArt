"""
Interactions with Qt Windows
"""

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets
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

    parent = qtwidgets.QApplication.activeWindow()
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
    top_level_widgets = qtwidgets.QApplication.topLevelWidgets()
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
    Returns all open MCA windows in PySide2
    
    :return: Returns all open MCA windows in PySide2
    :rtype: list[PySide2]
    """
    
    all_windows = get_all_open_windows()
    if not all_windows:
        return
    mca_windows = [x for x in all_windows if 'MCA ' in x.windowTitle()]
    return mca_windows


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
    
    docked_windows = parent_window.findChildren(qtwidgets.QDockWidget)
    return docked_windows


def get_all_mca_docked_windows(parent_window):
    """
    Gets all MCA docked windows attached to a parent window.

    :param QMainWindow parent_window: The main window that the dock gets attached.
    """
    
    docked_windows = get_all_docked_windows(parent_window)
    if not docked_windows:
        return
    MCA_docked_windows = [x for x in docked_windows if 'MCA' in x.windowTitle()]
    return MCA_docked_windows


def close_all_mca_docked_windows(parent_window):
    """
    Closes all MCA docked windows attached to a parent window.
    
    :param QMainWindow parent_window: The main window that the dock gets attached.
    """

    MCA_docked_windows = get_all_mca_docked_windows(parent_window)
    if not MCA_docked_windows:
        return
    [x.close() for x in MCA_docked_windows]
    [x.deleteLater() for x in MCA_docked_windows]
    
    