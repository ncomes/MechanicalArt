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
import mca.mya.cinematics.CinematicsArchive.CineControlCurve as cineCurve
import mca.mya.cinematics.CinematicsArchive.MatchObjs as mo
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc


def makeCameraController(cam):
    ns = cam.rpartition(':')[0]
    if not cmds.objExists("{}:head_ctrl".format(ns)):
        #print('making initial control')
        ctrl = makeInitialCameraControllers(cam, ns)
    else:
        #print('adding controls')
        ctrl = cineCurve.addControlToRig(cam)
    cmds.select(cl=True)
    cmds.select(ctrl)


def makeInitialCameraControllers(cam, ns):
    camShape = cmds.listRelatives(cam, s=True)[0]
    cmds.namespace(set=ns)
    scl = cmds.getAttr("{}.locatorScale".format(camShape))
    loc = getCamPivotLoc(cam, scl)
    headCtrl = cineCurve.makeCurve("head_ctrl", 0, 0, scl)
    #set rotation order on head control
    cmds.xform(headCtrl, p=True, roo='zxy')
    top = cmds.group(n="rig_grp", em=True)    
    mo.matchPos(loc, headCtrl)
    cmds.parent(headCtrl, top)
    cmds.parentConstraint(headCtrl, cam, mo=True)
    cmds.camera(camShape, e=True, lt=True)
    cmds.delete(loc)
    if not cmds.objExists('cameras_grp'):
        cmds.group(name='cameras_grp', em=True)
    cmds.parent(top, 'cameras_grp')
    cineCurve.addControlToRig(cam)
    cmds.namespace(set=":")
    
    return headCtrl
    

def getCamPivotLoc(cam, scl):
    loc = cmds.spaceLocator()[0]
    null = cmds.group(em=True)
    mo.matchPos(cam, null)
    mo.matchPos(null, loc)
    cmds.parent(loc, null)
    cmds.setAttr("{}.translateZ".format(loc), .75*scl)
    cmds.setAttr("{}.translateY".format(loc), -.3*scl)
    cmds.parent(loc, w=True)
    cmds.delete(null)
 
    return loc


@decorators.track_fnc
def addCameraController():
    selectedCams = [c for c in cmds.ls(sl=True) if cc.CineStaticClass.isShotCam(c)]
    for cam in selectedCams:
        #print 'unlocking camera {}'.format(cam)
        cmds.lockNode(cam, l=False)
        cmds.camera(cam, e=True, lt=False)
        makeCameraController(cam)
        cmds.camera(cam, e=True, lt=True)