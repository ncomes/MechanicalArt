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
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
from mca.common.modifiers import decorators



def getBoundingInfo(obj):    
    bboxMinX = cmds.getAttr(obj+".boundingBoxMinX")
    bboxMinY = cmds.getAttr(obj+".boundingBoxMinY")
    bboxMinZ = cmds.getAttr(obj+".boundingBoxMinZ")
    bboxMaxX = cmds.getAttr(obj+".boundingBoxMaxX")
    bboxMaxY = cmds.getAttr(obj+".boundingBoxMaxY")
    bboxMaxZ = cmds.getAttr(obj+".boundingBoxMaxZ")
    scaleX =  bboxMaxX - bboxMinX  
    scaleY =  bboxMaxY - bboxMinY 
    scaleZ =  bboxMaxZ - bboxMinZ
    allScales = [scaleX, scaleY, scaleZ]
    largestScale = max(allScales)

    return largestScale, bboxMinY, scaleX, scaleY, scaleZ


def makeCurve(name, r, c, s):
    axisDict = {
        'x':(1,0,0),
        'y':(0,1,0),
        'z':(0,0,1)
    }
    axis = cmds.upAxis(ax=1, q=1)
    normal = axisDict[axis]
    #print('normal axis: {}'.format(normal))    
    radius = (1.25+r)*s
    color = 17+c*2
    if color>31:
        color-=31
    ctrl = cmds.circle(n=name, nr=normal, r=radius)[0]
    cmds.setAttr("{}.overrideEnabled".format(ctrl), 1)
    cmds.setAttr("{}.overrideColor".format(ctrl), color)
    
    return ctrl


def addControlToRig(obj):
    rigGroup, ns = getRigGroup(obj)
    firstOffset = cmds.pickWalk(rigGroup, d='down')[0]
    ctrlNumber = getControlNumber(firstOffset)
    n, r, c, s = getCurveParameters(obj, ns, ctrlNumber)
    #print('looking for namespace: {}'.format(ns))
    if cmds.namespace(exists=ns):
        cmds.namespace(set=ns)
    else:
        #print('could not find namespace: {}'.format(ns))
        cmds.namespace(set=':')
    ctrl = makeCurve(n, r, c, s)
    makeHierarchy(obj, ns, ctrl, ctrlNumber, firstOffset, rigGroup)
    cmds.namespace(set=":")

    return ctrl


def makeHierarchy(obj, ns, ctrl, ctrlNumber, firstOffset, rigGroup):
    if ns:
        nullName = "offset_grp_{}".format(ctrlNumber)
    else:
        nullName = "{}_offset_grp_{}".format(obj, ctrlNumber)
    null = cmds.group(n=nullName, em=True)
    pointCon1 = cmds.pointConstraint(firstOffset, null)
    cmds.delete(pointCon1)
    pointCon2 = cmds.pointConstraint(null, ctrl)
    cmds.delete(pointCon2)
    cmds.parent(firstOffset, ctrl)
    cmds.parent(ctrl, null)
    cmds.parent(null, rigGroup)

def getCurveParameters(obj, ns, ctrlNumber):
    camShape = cmds.listRelatives(obj, s=True)[0]
    s = cmds.getAttr("{}.locatorScale".format(camShape))
    r = .25*(ctrlNumber)
    c = -1*(ctrlNumber)
    if ns:
        n = "ctrl_{}".format(ctrlNumber)
    else:
        n = "{}_ctrl_{}".format(obj, ctrlNumber)

    return n, r, c, s

def getObjectScale(obj, ctrlNumber):
    if cc.CineStaticClass.isShotCam(obj):
        camShape = cmds.listRelatives(obj, s=True)[0]
        s = cmds.getAttr("{}.locatorScale".format(camShape))
    elif 'ctrl' in obj:
        #print('control selected for curve creator')
        s = cmds.getAttr
    else:
        s = ctrlNumber+1

    return s

def getRigGroup(obj):
    ns = obj.rpartition(':')[0]
    if ns:
        rigGroup = "{}:rig_grp".format(ns)
        #print('namespace: '+ns)
    else:
        rigGroup = "{}_rig_grp".format(obj)
        ns = ""

    return rigGroup, ns

def getControlNumber(firstOffset):
    topCtrl = cmds.pickWalk(firstOffset, d='down')[0]
    ctrlNumber = 1
    try:
        ctrlNumber = int(topCtrl[-1])+1
    except ValueError:
        pass

    return ctrlNumber

