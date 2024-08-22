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


def makeLoc(obj, name=None):
    if name:
        locName = name
    else:
        locName = "{}_locator".format(str(obj))
    nonShapes = [x for x in (cmds.ls("{}*".format(locName))) if 'Shape' not in x]
    n = len(nonShapes)
    if n:
        locName = "{}_{}".format(locName, n)
    loc = cmds.spaceLocator(name=locName)
    loc = loc[0]
    con = cmds.parentConstraint(obj, loc, mo=False)
    cmds.delete(con)
    groupLoc(loc)
    
    return loc


def groupLoc(loc):
    layoutGrp = 'layout_grp'
    if loc:
        if not cmds.objExists(layoutGrp):
            cmds.group(n=layoutGrp, em=True)
        cmds.parent(loc, layoutGrp)



def addLocators():
    selection = cmds.ls(sl=True)
    for each in selection:
        makeLoc(each)