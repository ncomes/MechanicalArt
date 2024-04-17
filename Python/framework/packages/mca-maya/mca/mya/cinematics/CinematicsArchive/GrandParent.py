#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
from mca.mya.pyqt import dialogs

logger = log.MCA_LOGGER


@decorators.track_fnc
def parentMultiple(*args):
    sel = cmds.ls(sl=True)
    if len(sel)>1:
        gp = sel.pop(0)
        for each in sel:
            cmds.parentConstraint(gp, each, mo=True)
    else:
        logger.warning("Select at least two objects to parent")
        dialogs.error_prompt('Selection Error', 'Select at least two objects to parent')

