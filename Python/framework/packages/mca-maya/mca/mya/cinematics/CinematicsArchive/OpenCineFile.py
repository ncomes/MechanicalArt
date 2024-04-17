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
from mca.common.modifiers import decorators
from mca.mya.cinematics.CinematicsArchive.CineClasses import CineStaticClass as csc


@decorators.track_fnc
def openMayaFile(filePath, refresh=True, *args):
    #print('opening {} file'.format(os.path.basename(filePath)))
    cmds.file( new = True, force = True )
    cmds.file(filePath, open=True, esn=True)
    start = cmds.playbackOptions(q=True, min=True)
    end = cmds.playbackOptions(q=True, max=True)
    #reloadReferences()
    #print('refresh value: '+str(refresh))
    #print("setting timeline new")
    cmds.evalDeferred("cmds.playbackOptions(min={})".format(start))
    cmds.evalDeferred("cmds.playbackOptions(ast={})".format(start))
    cmds.evalDeferred("cmds.playbackOptions(max={})".format(end))
    cmds.evalDeferred("cmds.playbackOptions(aet={})".format(end))
    
    

def reloadReferences():
    fileRefs = cmds.file(q=True, r=True)
    for ref in fileRefs:
        if cmds.referenceQuery(ref, isLoaded=True):
            cmds.file(ref, loadReference=True)

