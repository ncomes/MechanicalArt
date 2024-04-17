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


def makeSceneMover(locName, topGroups):
    loc = cmds.spaceLocator(n=locName)
    scale = 250
    color = 20
    cmds.xform(loc, a=True,s=(scale, scale, scale))
    cmds.setAttr('{}.overrideEnabled'.format(locName), 1)
    cmds.setAttr('{}.overrideColor'.format(locName), color)
    for each in topGroups:
        cmds.parentConstraint(loc, each)

    return loc


def deleteSceneMover(loc, topGroups):
    for each in topGroups:
        cmds.setKeyframe(each)
    cmds.delete(loc)


@decorators.track_fnc
def makeSceneMoverButtonClick(*args):
    targetGroups = ['cameras', 'props', 'chars', 'layout', 'env']
    topGroups = [x for x in cmds.ls('*_grp') if x[:-4] in targetGroups]
    locName = 'sceneMover_locator'
    #print(topGroups)
    if not cmds.objExists(locName):
        makeSceneMover(locName, topGroups)
    else:
        deleteSceneMover(locName, topGroups)
        for each in topGroups:
            cmds.setKeyframe(each)
            cmds.cutKey(each, cl=True)
