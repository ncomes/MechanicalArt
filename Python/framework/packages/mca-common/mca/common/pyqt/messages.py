#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""
import os.path

# mca python imports
# PySide2 imports
from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide2.QtWidgets import QApplication, QMessageBox, QLineEdit, QFrame
from PySide2.QtCore import Qt
# software specific imports
# mca python imports
from mca.common.resources import resources
from mca.common.utils import sounds


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

        QApplication.activeWindow()

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
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    else:
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
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
    message_box.setStandardButtons(QMessageBox.Ok)
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
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
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
    prompt_lineEdit = QLineEdit()
    message_box_layout.addWidget(prompt_lineEdit, 2, 0, 1, -1)
    if starting_text:
        prompt_lineEdit.setText(starting_text)
    message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    horizontal_layout = QHBoxLayout()
    message_box_layout.addLayout(horizontal_layout, 3, 0, 1, -1)
    for prompt_button in message_box.buttons():
        horizontal_layout.addWidget(prompt_button)
    message_box.exec_()
    return prompt_lineEdit.text() if message_box.result != 'Cancel' else ''

