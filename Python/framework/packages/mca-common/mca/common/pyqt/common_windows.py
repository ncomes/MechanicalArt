"""
Module that contains the mca decorators at a base python level
"""

# python imports
import os
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtuitools
# software specific imports
# mca python imports
from mca.common import log
from mca.common.resources import resources
from mca.common.pyqt.qt_utils import windows


logger = log.MCA_LOGGER

RESOURCES_REGISTERED = False
try:
    resources.register_resources()
    RESOURCES_REGISTERED = True
except:
    logger.warning('Unable to register resources.')
    

class MCADockableWindow(qtwidgets.QDockWidget):
    INITIAL_WIDTH_FALLBACK = 150
    INITIAL_HEIGHT_FALLBACK = 100

    def __init__(self, title,
                        ui_path=None,
                        version='1.0.0',
                        style=None,
                        isfloating=False,
                        area='left',
                        single_insta=True,
                        parent=None):

        super().__init__(parent=parent)
        self.setAttribute(qtcore.Qt.WA_DeleteOnClose)
        self.title = f'MCA {title}'
        if single_insta:
            self.single_window_instance()
        self.single_dock_instance(parent)
        self.setWindowTitle(f'{self.title} {version}')
        if RESOURCES_REGISTERED:
            self.setWindowIcon(resources.icon(r'software\mca.png'))
        area = self.get_area(area)

        self.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)

        minsize = self.minimumSize()
        self.setMinimumSize(minsize)

        self.setAllowedAreas(qtcore.Qt.RightDockWidgetArea|qtcore.Qt.LeftDockWidgetArea)
        if parent:
            parent.addDockWidget(area, self)
            childs = parent.findChildren(MCADockableWindow)
            if len(childs) > 1:
                parent.tabifyDockWidget(childs[0], self)
                self.raise_()

        if isfloating:
            self.setFloating(True)

        self.setContentsMargins(0, 2, 0, 0)

        self.main_frame = qtwidgets.QFrame(self)
        self.main_frame.setMinimumSize(minsize)
        self.main_frame.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
        self.main_frame.setContentsMargins(0, 2, 0, 0)
        self.setWidget(self.main_frame)

        self.main_layout = qtwidgets.QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(0, 2, 0, 0)

        if ui_path:
            loader = qtuitools.QUiLoader()
            file = qtcore.QFile(os.path.abspath(ui_path))
            if file.open(qtcore.QFile.ReadOnly):
                self.ui = loader.load(file, parent)
                file.close()
                self.main_layout.addWidget(self.ui)
                self.ui.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)

        if not style:
            style = 'incrypt'
        if style != 'custom':
            stylesheet = resources.read_stylesheet(style)
            self.setStyleSheet(stylesheet)
        
        username = os.getlogin()
        self.settings = qtcore.QSettings(username, self.title)
        geometry = self.settings.value('geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)

        self.show()

    def single_dock_instance(self, parent):
        if not parent:
            return
        for dock in parent.findChildren(qtwidgets.QDockWidget):
            if self.title in dock.windowTitle():
                dock.close()
                logger.info(f'A duplicate of "{dock.windowTitle()}" was closed')
                break

    def single_window_instance(self):
        all_windows = windows.get_all_mca_windows()
        if not all_windows:
            return
        for win in all_windows:
            if self.title in win.windowTitle():
                win.close()
                win.deleteLater()
                break

    def get_area(self, value):
        if isinstance(value, qtcore.Qt):
            return value
        elif isinstance(value, str):
            if value.lower() == 'left':
                return qtcore.Qt.LeftDockWidgetArea
            elif value.lower() == 'right':
                return qtcore.Qt.RightDockWidgetArea
            else:
                return qtcore.Qt.LeftDockWidgetArea
        else:
            return qtcore.Qt.LeftDockWidgetArea

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        super().closeEvent(event)


class MCAMainWindow(qtwidgets.QMainWindow):
    INITIAL_WIDTH_FALLBACK = 150
    INITIAL_HEIGHT_FALLBACK = 100

    def __init__(self, title, ui_path=None, version='1.0.0', style=None, parent=None, show_window=True):
        super().__init__(parent=parent)
        self.title = f'MCA {title}'
        self.single_window_instance()

        self.setWindowTitle(f'{self.title} {version}')
        if RESOURCES_REGISTERED:
            self.setWindowIcon(resources.icon(r'software\mca.png'))

        self.ui = None

        self.setMinimumHeight(MCAMainWindow.INITIAL_HEIGHT_FALLBACK)
        self.setMinimumWidth(MCAMainWindow.INITIAL_WIDTH_FALLBACK)
        self.setContentsMargins(0,0,0,0)
        if ui_path:
            loader = qtuitools.QUiLoader()
            file = qtcore.QFile(os.path.abspath(ui_path))
            if file.open(qtcore.QFile.ReadOnly):
                self.ui = loader.load(file, parent)
                file.close()
                self.setCentralWidget(self.ui)
        else:
            self.central_widget = qtwidgets.QWidget(self)
            self.main_layout = qtwidgets.QVBoxLayout(self.central_widget)
            self.setCentralWidget(self.central_widget)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        if not style:
            style = 'incrypt'
        if style != 'custom':
            stylesheet = resources.read_stylesheet(style)
            self.setStyleSheet(stylesheet)
        
        username = os.getlogin()
        self.settings = qtcore.QSettings(username, self.title)
        geometry = self.settings.value('geometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        if show_window:
            self.show()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        super().closeEvent(event)

    def single_window_instance(self):
        all_windows = windows.get_all_mca_windows()
        if not all_windows:
            return
        for win in all_windows:
            if self.title in win.windowTitle():
                win.close()
                win.deleteLater()
                break


class ParentableWidget(qtwidgets.QWidget):
    def __init__(self, ui_path=None, style=None, parent=None):
        super().__init__(parent=parent)

        self.ui = None

        if not style:
            style = 'incrypt'
        if RESOURCES_REGISTERED:
            stylesheet = resources.read_stylesheet(style)
            self.setStyleSheet(stylesheet)
        if ui_path:
            loader = qtuitools.QUiLoader()
            file = qtcore.QFile(os.path.abspath(ui_path))
            if file.open(qtcore.QFile.ReadOnly):
                self.ui = loader.load(file, parent)
                file.close()
        else:
            self.main_layout = qtwidgets.QVBoxLayout(self)
            self.setLayout(self.main_layout)
            self.main_layout.setContentsMargins(0, 0, 0, 0)


class ProgressBarWindow(qtwidgets.QMainWindow):
    INITIAL_WIDTH_FALLBACK = 435
    INITIAL_HEIGHT_FALLBACK = 200

    def __init__(self, title, version, pb_inst, style=None, parent=None):
        super().__init__(parent=parent)
        self.title = f'MCA {title}'
        self.pgb_inst = pb_inst
        #self.single_window_instance()

        self.setWindowTitle(f'{self.title} {version}')
        if RESOURCES_REGISTERED:
            self.setWindowIcon(resources.icon(r'logos\mech-art-blue.png'))

        self.ui = None

        if not style:
            style = 'incrypt'
        if RESOURCES_REGISTERED:
            stylesheet = resources.read_stylesheet(style)
            self.setStyleSheet(stylesheet)

        self.setMinimumHeight(MCAMainWindow.INITIAL_HEIGHT_FALLBACK)
        self.setMinimumWidth(MCAMainWindow.INITIAL_WIDTH_FALLBACK)
        self.setContentsMargins(0, 0, 0, 0)

        self.central_widget = qtwidgets.QWidget(self)
        self.main_layout = qtwidgets.QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # username = os.getlogin()
        # self.settings = qtcore.QSettings(username, self.title)
        # geometry = self.settings.value('geometry', bytes('', 'utf-8'))
        # self.restoreGeometry(geometry)
        self.show()

    # def closeEvent(self, event):
    #     geometry = self.saveGeometry()
    #     self.settings.setValue('geometry', geometry)
    #     self.pgb_inst.close_window()
    #     super().closeEvent(event)
    #
    # def single_window_instance(self):
    #     all_windows = windows.get_all_mca_windows()
    #     for win in all_windows:
    #         if self.title in win.windowTitle():
    #             win.close()
    #             win.deleteLater()
    #             break


def getOpenFilesAndDirs(parent=None, caption='', directory='', filter='', initialFilter='', options=None):
    def updateText():
        # update the contents of the line edit widget with the selected files
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        lineEdit.setText(' '.join(selected))

    dialog = qtwidgets.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    # by default, if a directory is opened in file listing mode,
    # qtwidgets.QFileDialog.accept() shows the contents of that directory, but we
    # need to be able to "open" directories as we can do with files, so we
    # just override accept() with the default qtwidgets.QDialog implementation which
    # will just return exec_()
    dialog.accept = lambda: qtwidgets.QDialog.accept(dialog)

    # there are many item views in a non-native dialog, but the ones displaying
    # the actual contents are created inside a qtwidgets.QStackedWidget; they are a
    # QTreeView and a qtwidgets.QListView, and the tree is only used when the
    # viewMode is set to qtwidgets.QFileDialog.Details, which is not this case
    stackedWidget = dialog.findChild(qtwidgets.QStackedWidget)
    view = stackedWidget.findChild(qtwidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(qtwidgets.QLineEdit)
    # clear the line edit contents whenever the current directory changes
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()


