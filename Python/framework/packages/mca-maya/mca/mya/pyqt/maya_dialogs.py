#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions for Blend nodes and shapes
"""

# python imports

# software specific imports
import pymel.core as pm

#  python imports
from mca.common import log
from mca.common.pyqt import messages
from mca.mya.pyqt.utils import ma_main_window
logger = log.MCA_LOGGER


MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()


def display_view_message(text='No text given', mode='good', header='', fade_time=110):
    """
    Displays a popup message with relevant information.

    :param str text: text to display.
    :param str mode: mode to define text color ('good' = green; 'error' = red)
    :param str header: prefix before the message.
    :param float fade_time: the time the message is on the screen.
    """

    fade_time = len(text) * fade_time
    if fade_time >= 10000:
        fade_time = 10000

    if mode == 'good':
        pm.inViewMessage(
            assistMessage=(u"<span style=\"color:#21C4F5;\">{}:</span> {}").format(header, text),
            pos='topRight', fade=True, fadeStayTime=fade_time)
    elif mode == 'error':
        pm.inViewMessage(
            assistMessage=(u"<span style=\"color:#f52121;\">{}:</span> {}").format(header, text),
            pos='topRight', fade=True, fadeStayTime=fade_time)


def error_prompt(title, text, detail_text=None, style=None, sound=None, icon='error', parent=None):
    return messages.error_message(title=title,
                                        text=text,
                                        detail_text=detail_text,
                                        style=style,
                                        sound=sound,
                                        icon=icon,
                                        parent=parent)


def info_prompt(title, text, detail_text=None, style=None, sound=None, icon='info', parent=None):
    return messages.info_message(title=title,
                                        text=text,
                                        detail_text=detail_text,
                                        style=style,
                                        sound=sound,
                                        icon=icon,
                                        parent=parent)


def question_prompt(title, text, detail_text=None, style=None, sound=None, icon='question', parent=None):
    return messages.question_message(title=title,
                                        text=text,
                                        detail_text=detail_text,
                                        style=style,
                                        sound=sound,
                                        icon=icon,
                                        parent=parent)


def open_file_dialog(title, filters=None, start_dir=None, dialog_style=None):
    """
    Basic Maya file dialog.  It will look up the users saved dialog style.

    :param str title: the title of the file dialog.
    :param str filters: the filters to apply to the file dialog.
    :param str start_dir: the starting directory for the file dialog.
    :param int dialog_style: 1 is OS native, 2 is Maya Native window style.
    :return: the path to the selected file.
    :rtype: str
    """

    if not filters:
        filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    if not dialog_style:
        dialog_style = pm.optionVar(query='FileDialogStyle')

    path = pm.fileDialog2(fileFilter=filters, dialogStyle=dialog_style, fm=1, dir=start_dir, cap=title)
    if not path:
        return
    return path[0]


def save_file_dialog(title, filters=None, start_dir=None, dialog_style=None):
    """
    Basic Maya file dialog.  It will look up the users saved dialog style.

    :param str title: the title of the file dialog.
    :param str filters: the filters to apply to the file dialog.
    :param str start_dir: the starting directory for the file dialog.
    :param int dialog_style: 1 is OS native, 2 is Maya Native window style.
    :return: the path to the selected file.
    :rtype: str
    """

    if not filters:
        filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"

    if not dialog_style:
        dialog_style = pm.optionVar(query='FileDialogStyle')

    path = pm.fileDialog2(fileFilter=filters, dialogStyle=dialog_style, fm=0, dir=start_dir, cap=title, okc=True)
    if not path:
        return
    return path[0]

