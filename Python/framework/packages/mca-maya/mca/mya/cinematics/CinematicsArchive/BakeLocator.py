#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
from mca.mya.utils import attr_utils
from mca.mya.cinematics.CinematicsArchive.AddLocator import makeLoc



def bakeLocToSelection():
    selection = cmds.ls(sl=True)
    locs = []
    atList = attr_utils.TRANSFORM_ATTRS
    start = cmds.playbackOptions(q=True, min=True)
    stop = cmds.playbackOptions(q=True, max=True)
    for each in selection:
        loc = makeLoc(each)
   
        bakedLoc = cmds.rename(loc, f'{loc}_BAKED')
        locs.append(bakedLoc)
        con = cmds.parentConstraint(each, bakedLoc, mo=True)
        cmds.bakeResults(bakedLoc, sm=True, t=(start, stop), at=atList, hi='below')
        cmds.delete(con)
        
    return locs
    
