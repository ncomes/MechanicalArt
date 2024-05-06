# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import os

# Qt imports
from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QTextCharFormat, QColor

# software specific imports
# mca python imports
from mca.common.pyqt import common_windows


# display text formatting
ERROR_FORMAT = QTextCharFormat()
ERROR_FORMAT.setForeground(QBrush(Qt.red))

WARNING_FORMAT = QTextCharFormat()
WARNING_FORMAT.setForeground(QBrush(Qt.yellow))

INFO_FORMAT = QTextCharFormat()
INFO_FORMAT.setForeground(QBrush(QColor('#21cc3d')))

REGULAR_FORMAT = QTextCharFormat()
REGULAR_FORMAT.setForeground(QBrush(QColor(200, 200, 200)))


class OutputTextWidget(common_windows.MCAMainWindow):
    """
    Text Widget to display output information from Unreal command execution
    """
    VERSION = '1.0.0'

    def __init__(self, parent=None):
        """
        Initialization
        """
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'output_text_widget.ui')
        super().__init__(title='Output Log',
                         ui_path=ui_path,
                         version=OutputTextWidget.VERSION,
                         parent=parent)

    def clear(self):
        """
        Clear the all text
        """
        self.ui.ui_log_edit.clear()

    def update_logger(self, message, mtype=None):
        """
        Append plain message to display text widget

        :param message: str. message
        :param mtype: str. message type, this determines the message format/style
        """
        if mtype == 'info':
            self.ui.ui_log_edit.setCurrentCharFormat(INFO_FORMAT)
            self.ui.ui_log_edit.insertPlainText(f'# Result: {message}')
            self.ui.ui_log_edit.insertPlainText('\n')
        elif mtype == 'warning':
            self.ui.ui_log_edit.setCurrentCharFormat(WARNING_FORMAT)
            self.ui.ui_log_edit.insertPlainText(f'# {message}')
            self.ui.ui_log_edit.insertPlainText('\n')
        elif mtype == 'error':
            self.ui.ui_log_edit.setCurrentCharFormat(ERROR_FORMAT)
            self.ui.ui_log_edit.insertPlainText(f'# {message}')
            self.ui.ui_log_edit.insertPlainText('\n')
        else:
            self.ui.ui_log_edit.setCurrentCharFormat(REGULAR_FORMAT)
            self.ui.ui_log_edit.insertPlainText(f'{message}')
            self.ui.ui_log_edit.insertPlainText('\n')

        scroll = self.ui.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def update_logger_html(self, html):
        """
        Append html message to display text widget

        :param html: str. message as html
        """
        self.ui.ui_log_edit.insertHtml(html)
        self.ui.ui_log_edit.insertHtml('<br>')

        scroll = self.ui.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())
