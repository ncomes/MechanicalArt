"""
code for the main output text widget
"""

import os

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2 import QtUiTools


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.basename(MODULE_PATH)
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'output_text_widget.ui')

# display text formatting
ERROR_FORMAT = QtGui.QTextCharFormat()
ERROR_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.red))

WARNING_FORMAT = QtGui.QTextCharFormat()
WARNING_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.yellow))

INFO_FORMAT = QtGui.QTextCharFormat()
INFO_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor('#6897bb')))

REGULAR_FORMAT = QtGui.QTextCharFormat()
REGULAR_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))


class OutputTextWidget(QtWidgets.QWidget):
    """
    Text Widget to display output information from Unreal command execution
    """

    def __init__(self, parent=None):
        """
        Initialization
        """
        super(OutputTextWidget, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(os.path.abspath(UI_PATH))

        if file.open(QtCore.QFile.ReadOnly):
            self.ui = loader.load(file, parent)
            file.close()
            self.main_layout.addWidget(self.ui)
            self.ui.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def clear(self):
        """
        Clear the all text
        """
        self.ui_log_edit.clear()

    def update_logger(self, message, mtype=None):
        """
        Append plain message to display text widget

        :param message: str. message
        :param mtype: str. message type, this determines the message format/style
        """
        if mtype == 'info':
            self.ui_log_edit.setCurrentCharFormat(INFO_FORMAT)
        elif mtype == 'warning':
            self.ui_log_edit.setCurrentCharFormat(WARNING_FORMAT)
        elif mtype == 'error':
            self.ui_log_edit.setCurrentCharFormat(ERROR_FORMAT)
        else:
            self.ui_log_edit.setCurrentCharFormat(REGULAR_FORMAT)

        self.ui_log_edit.insertPlainText(message)
        self.ui_log_edit.insertPlainText('\n')

        scroll = self.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def update_logger_html(self, html):
        """
        Append html message to display text widget

        :param html: str. message as html
        """
        self.ui_log_edit.insertHtml(html)
        self.ui_log_edit.insertHtml('<br>')

        scroll = self.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())
