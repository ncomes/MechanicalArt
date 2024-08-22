"""
Module that contains the mca decorators at a base python level
"""
# python imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets
# software specific imports
# mca python imports
from mca.common.resources import resources
from mca.common.utils import sounds


M_OKAY = qtwidgets.QMessageBox.Ok
M_OPEN = qtwidgets.QMessageBox.Open
M_SAVE = qtwidgets.QMessageBox.Save
M_CANCEL = qtwidgets.QMessageBox.Cancel
M_CLOSE = qtwidgets.QMessageBox.Close
M_DISCARD = qtwidgets.QMessageBox.Discard
M_APPLY = qtwidgets.QMessageBox.Apply
M_RESET = qtwidgets.QMessageBox.Reset
M_RESTORE_DEFAULTS = qtwidgets.QMessageBox.RestoreDefaults
M_HELP = qtwidgets.QMessageBox.Help
M_SAVE_ALL = qtwidgets.QMessageBox.SaveAll
M_YES = qtwidgets.QMessageBox.Yes
M_YES_TO_ALL = qtwidgets.QMessageBox.YesToAll
M_NO = qtwidgets.QMessageBox.No
M_NO_TO_ALL = qtwidgets.QMessageBox.NoToAll
M_ABORT = qtwidgets.QMessageBox.Abort
M_RETRY = qtwidgets.QMessageBox.Retry
M_IGNORE = qtwidgets.QMessageBox.Ignore
M_NO_BUTTON = qtwidgets.QMessageBox.NoButton


class MCAMessageBox(qtwidgets.QMessageBox):
    INIT_WIDTH = 350
    INIT_HEIGHT = 200

    def __init__(self, title, text, detail_text=None, style=None, sound=None, parent=None):
        super().__init__(parent=parent)
        self.title = title
        self.text = text
        self.sound = sound
        self.detail_text = detail_text
        self.result = None

        if sound:
            sounds.play_sound(self.sound)

        if not style:
            style = 'incrypt'
        stylesheet = resources.read_stylesheet(style)
        self.setStyleSheet(stylesheet)

        self.setWindowTitle(f'MCA {self.title}')
        self.setText(self.text)
        if self.detail_text:
            self.setDetailedText(self.detail_text)
        self.setStyleSheet("QLabel{min-width: 200px;min-height: 100px;}")
        self.setStyleSheet("QPushButton{padding: 10px};")

        qtwidgets.QApplication.activeWindow()

        self.buttonClicked.connect(self.button_clicked)

    def button_clicked(self, i):
        self.result = i.text()


def question_message(title,
                        text,
                        detail_text=None,
                        style=None,
                        sound=None,
                        icon=r'color\question.png',
                        parent=None,
                        tri_option=False):

    message_box = MCAMessageBox(title=title,
                                text=text,
                                detail_text=detail_text,
                                style=style,
                                sound=sound,
                                parent=parent)
    if icon:
        message_box.setIconPixmap(resources.icon(icon, typ=resources.ResourceTypes.PIXMAP))
    if tri_option:
        message_box.setStandardButtons(qtwidgets.QMessageBox.Yes | qtwidgets.QMessageBox.No | qtwidgets.QMessageBox.Cancel)
    else:
        message_box.setStandardButtons(qtwidgets.QMessageBox.Yes | qtwidgets.QMessageBox.Cancel)
    message_box.exec_()

    if message_box.result == '&Yes':
        message_box.result = 'Yes'
    return message_box.result


def info_message(title, text, detail_text=None, style=None, sound=None, icon=r'color\info.png', parent=None):
    message_box = MCAMessageBox(title=title,
                                text=text,
                                detail_text=detail_text,
                                style=style,
                                sound=sound,
                                parent=parent)
    if icon:
        message_box.setIconPixmap(resources.icon(icon, typ=resources.ResourceTypes.PIXMAP))
    message_box.setStandardButtons(qtwidgets.QMessageBox.Ok)
    message_box.exec_()
    return message_box.result


def error_message(title, text, detail_text=None, style=None, sound='notify.wav', icon=r'color\error.png', parent=None):
    message_box = MCAMessageBox(title=title,
                            text=text,
                            detail_text=detail_text,
                            style=style,
                            sound=sound,
                            parent=parent)
    if icon:
        message_box.setIconPixmap(resources.icon(icon, typ=resources.ResourceTypes.PIXMAP))
    message_box.setStandardButtons(qtwidgets.QMessageBox.Ok | qtwidgets.QMessageBox.Cancel)
    message_box.exec_()
    return message_box.result


def text_prompt_message(title,
                        text,
                        starting_text=None,
                        detail_text=None,
                        style=None,
                        sound=None,
                        icon=r'color\question.png',
                        parent=None):

    message_box = MCAMessageBox(title=title,
                            text=text,
                            detail_text=detail_text,
                            style=style,
                            sound=sound,
                            parent=parent)
    if icon:
        message_box.setIconPixmap(resources.icon(icon, typ=resources.ResourceTypes.PIXMAP))

    message_box_layout = message_box.layout()
    prompt_lineEdit = qtwidgets.QLineEdit()
    message_box_layout.addWidget(prompt_lineEdit, 2, 0, 1, -1)
    if starting_text:
        prompt_lineEdit.setText(starting_text)
    message_box.setStandardButtons(qtwidgets.QMessageBox.Ok | qtwidgets.QMessageBox.Cancel)
    horizontal_layout = qtwidgets.QHBoxLayout()
    message_box_layout.addLayout(horizontal_layout, 3, 0, 1, -1)
    for prompt_button in message_box.buttons():
        horizontal_layout.addWidget(prompt_button)
    message_box.exec_()
    return prompt_lineEdit.text() if message_box.result != 'Cancel' else ''

