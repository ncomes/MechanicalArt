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


def getMatchSelection():
    selection = cmds.ls(sl=True)
    if len(selection)>1:
        follow = selection[0]
        lead = selection[1]   
        return lead, follow
    else:
        print("Select two objects to match")
        return None


def matchPos(lead, follow):
    con = cmds.parentConstraint(lead, follow, mo=False)
    if cmds.keyframe(follow, q=True, kc=True):
        cmds.setKeyframe(follow)
    cmds.delete(con)



def matchObjs():
    if getMatchSelection():
        lead, follow = getMatchSelection()
        #print(lead, follow)
        matchPos(lead, follow)
        
