#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Test tool implementation.
"""

# System global imports
# Software specific imports
# PySide2 imports
from PySide2.QtWidgets import QCheckBox
# mca python imports


def get_checkbox_text(checkbox_list, only_true=True):
    """
    Returns the text for each Checkbox listed

    :param list(QWidget) checkbox_list:
    :param bool only_true: If True,
    :return:  Returns the text for each Checkbox listed
    :rtype: list(str)
    """
    
    if not isinstance(checkbox_list, (tuple, list)):
        checkbox_list = [checkbox_list]

    checkbox_list = [x for x in checkbox_list if isinstance(x, QCheckBox)]
    
    text = []
    for checkbox in checkbox_list:
        if not only_true:
            text.append(checkbox.text())
        elif only_true and checkbox.isChecked():
            text.append(checkbox.text())
    return text
