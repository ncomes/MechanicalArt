"""
Pop up messaging for the launcher
"""

# System global imports
# PySide6 imports
from PySide6.QtWidgets import QApplication, QMessageBox
# Software specific imports
# mca python imports


M_OKAY = QMessageBox.Ok
M_OPEN = QMessageBox.Open
M_SAVE = QMessageBox.Save
M_CANCEL = QMessageBox.Cancel
M_CLOSE = QMessageBox.Close
M_DISCARD = QMessageBox.Discard
M_APPLY = QMessageBox.Apply
M_RESET = QMessageBox.Reset
M_RESTORE_DEFAULTS = QMessageBox.RestoreDefaults
M_HELP = QMessageBox.Help
M_SAVE_ALL = QMessageBox.SaveAll
M_YES = QMessageBox.Yes
M_YES_TO_ALL = QMessageBox.YesToAll
M_NO = QMessageBox.No
M_NO_TO_ALL = QMessageBox.NoToAll
M_ABORT = QMessageBox.Abort
M_RETRY = QMessageBox.Retry
M_IGNORE = QMessageBox.Ignore
M_NO_BUTTON = QMessageBox.NoButton


class MCAMessageBox(QMessageBox):
    """
    A custom message box with a title, text, and detail text.
    """

    INIT_WIDTH = 350
    INIT_HEIGHT = 200

    def __init__(self, title, text, detail_text=None, parent=None):
        super().__init__(parent=parent)
        self.setMinimumSize(self.INIT_WIDTH, self.INIT_HEIGHT)
        self.title = title
        self.mes_text = text
        self.detail_text = detail_text
        self.result = None

        self.setWindowTitle(f'MCA {self.title}')
        self.setText(self.mes_text)
        if self.detail_text:
            self.setDetailedText(self.detail_text)
        self.setStyleSheet("QLabel{min-width: 200px;min-height: 100px;}")
        self.setStyleSheet("QPushButton{padding: 10px};")

        QApplication.activeWindow()

        self.buttonClicked.connect(self.button_clicked)

    def button_clicked(self, i):
        self.result = i.text()


def question_message(title,
                        text,
                        detail_text=None,
                        parent=None,
                        tri_option=False):

    message_box = MCAMessageBox(title=title,
                                text=text,
                                detail_text=detail_text,
                                parent=parent)

    if tri_option:
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    else:
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    message_box.exec_()

    if message_box.result == '&Yes':
        message_box.result = 'Yes'
    return message_box.result


def error_message(title, text, detail_text=None, parent=None):
    '''
    Displays an error message box with a title, text, and detail text.
    '''

    message_box = MCAMessageBox(title=title,
                            text=text,
                            detail_text=detail_text,
                            parent=parent)

    message_box.setStandardButtons(M_OKAY)
    message_box.exec_()
    return message_box.result

