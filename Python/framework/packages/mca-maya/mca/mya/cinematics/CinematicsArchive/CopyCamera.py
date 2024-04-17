#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates and includes a shelf with buttons in mya for Cinematics
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.MatchObjs as mo
from mca.mya.cinematics.CinematicsArchive.CineClasses import CineStaticClass as csc


@decorators.track_fnc
def copyCamera(*args):
    sel = cmds.ls(sl=True)
    if len(sel)>1:
        thisCam = sel[0]
        copyCam = sel[1]
        cams = [x for x in sel if csc.isShotCam(x)]
        if csc.isShotCam(thisCam) and csc.isShotCam(copyCam):
            focalLength = cmds.getAttr('{}.focalLength'.format(copyCam))
            cmds.setAttr('{}.focalLength'.format(thisCam), focalLength)
            mo.matchPos(copyCam, thisCam)
        else:
            print('Selection does not include two SHOT cameras to copy one to the other')
    else:
        print("Select at least two cameras to copy one to the other")