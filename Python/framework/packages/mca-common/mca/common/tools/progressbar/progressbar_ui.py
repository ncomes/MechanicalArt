#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source data for faces.

"""
# mca python imports
import os
import inspect
import time
# software specific imports
# PySide2 imports
from PySide2.QtWidgets import QApplication, QMainWindow, QFrame, QSizePolicy, QVBoxLayout
# mca python imports
from mca.common.pyqt.qt_utils import uiloaders
from mca.common.pyqt import common_windows
from mca.common.modifiers import decorators, singleton


from mca.common import log
logger = log.MCA_LOGGER


@decorators.add_metaclass(singleton.Singleton)
class ProgressBarStandard:
    VERSION = '1.0.0'
    
    def __init__(self, title='Progressbar', style=None, parent=None):
        
        self.ui = None
        self.progressbar_list = []
        self.title = title
        self.style = style
        self.parent = parent
        if not self.progressbar_list:
            self.ui = self.open_window(title=self.title,
                                       version=ProgressBarStandard.VERSION,
                                       style=self.style)
            self.add_progressbar()
        #print(f'THIS IS THE PROGRESSBAR LIST\n{self.progressbar_list}')
        self.ui.setFixedWidth(435)
        self.ui.setFixedHeight(200)

    def open_window(self, title, version, style=None):
        """
        Opens the Progressbar window.
        
        :param str title: Title of the Window without the "MAT"
        :param str version: Version number as a string
        :param str style: Name of the stylesheet
        :return:  returns the .ui file
        :rtype: QMainWindow
        """
        
        self.ui = common_windows.ProgressBarWindow(title=title,
                                                    version=version,
                                                    pb_inst=self,
                                                    style=style,
                                                    parent=self.parent)
        self.ui.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return self.ui
    
    def add_progressbar(self):
        """
        Adds a progressbar
        """
        
        pgb_frame = ProgressBarFrame(parent=self.ui)
        self.ui.main_layout.addWidget(pgb_frame)
        self.progressbar_list.append(pgb_frame)
        self.ui.setFixedHeight(len(self.progressbar_list) * 200)
    
    def remove_progressbar(self):
        """
        Removes a progressbar
        """
        
        last_bar = self.progressbar_list[-1]
        self.progressbar_list.pop(-1)
        last_bar.deleteLater()
        #last_bar.close()
        last_bar.setParent(None)
        self.ui.setFixedHeight(len(self.progressbar_list) * 100)

    def update_label(self, value):
        """
        Updates the label/message for the progress bar.

        :param str value: label/message for the progress bar.
        """
    
        self.progressbar_list[-1].ui.status_label.setText(value)
    
    def update_value(self, value):
        """
        Updates the progress bar by the given value.  The value should be a percentage from 0-100.

        :param float value: Progress bar percentage.
        """
        
        if value < 0:
            logger.warning(f'Value is less then 0.  Value is: {value}')
            return
        self.progressbar_list[-1].ui.main_progressBar.setValue(value)
        QApplication.processEvents()
        if value >= 100:
            time.sleep(0.5)
            if len(self.progressbar_list) > 1:
                self.remove_progressbar()
            else:
                self.close_window()

    def update_status(self, value, message):
        """
        Updates both the label and the percentage

        :param float value: Progress bar percentage.
        :param str message: label/message for the progress bar.
        """
    
        self.update_label(message)
        self.update_value(value)
    
    def close_window(self):
        self.ui.close()
        singleton.clear_cls(self)


class ProgressBarFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        # Load the .ui file
        root_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        ui_path = os.path.join(root_path, 'ui', 'progressbar_widget.ui')
        self.ui = uiloaders.ui_importer(ui_path)
        
        self.setContentsMargins(1, 0, 0, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        
        self.progress_layout = QVBoxLayout(self)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.addWidget(self.ui)


