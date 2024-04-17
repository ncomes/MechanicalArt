#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Test tool implementation.
"""

# System global imports
# Software specific imports
# PySide2 imports
# mca python imports


def get_qwidget_text(qwidget_list):
    """
    Returns the text for each QWidget listed
    
    :param list(QWidget) qwidget_list:
    :return:  Returns the text for each QWidget listed
    :rtype: list(str)
    """
    
    if not isinstance(qwidget_list, (tuple, list)):
        qwidget_list = [qwidget_list]
        
    text = []
    for qwidget in qwidget_list:
        text.append(qwidget.text())
    return text

