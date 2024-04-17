#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create shot - adds shot cam into new shot in sequencer, names things appropriately
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
import math


def getShotSeqStartTime():
    shots = cmds.ls(type='shot')
    lastShotEnd=0
    if len(shots)>0:
        lastShotEnd= int(max([cmds.shot(s, set=True, q=True) for s in shots]))
    
    return lastShotEnd+1
    
    
def makeShot(cineShot):
    seqStartTime = getShotSeqStartTime()     
    newShot = cmds.shot('shot_'+str(cineShot.cam.mayaCam), st=cineShot.start, et=cineShot.end, sst=seqStartTime, 
                        cc=cineShot.cam.mayaCam)
    cmds.shot(newShot, e=True, shotName=cineShot.name)
    cmds.sequenceManager(ct=seqStartTime)
    cmds.shotTrack(ret=True)


def groupCam(cam):
    if not cmds.objExists('cameras_grp'):
        cmds.group(name='cameras_grp', em=True)
    cmds.parent(cam, 'cameras_grp')


def getNewShotNumber():
    camNames = [c[-3:] for c in cmds.namespaceInfo(listOnlyNamespaces=True) if 'shot' in c]
    latestCamNumber = 10
    if camNames:
        latestCam = max(camNames)
        latestCamNumber = 10+(math.floor(int(latestCam[-3:])/10)*10)
    camNumber = "{0:0=3d}".format(latestCamNumber)
    
    return camNumber
    
    
def referenceCam(cineSeqNode):
    if cineSeqNode.shotNumber!=0:
        #if this file is not a sequence or scene file
        shotName = '{}_shot_{:0=3d}'.format(cineSeqNode.seq.name, cineSeqNode.shotNumber)
        cc.CineStaticClass.handleNamespaceConflict(shotName)
        camNumber = cineSeqNode.shotNumber
    else:
        camNumber = getNewShotNumber()

    camRef = cmds.file(cc.CineStaticClass.cameraPath, r=True, type="mayaAscii", 
                        ns="{}_shot_{}".format(cineSeqNode.seq.name, camNumber))
    cam = [c for c in cmds.referenceQuery(camRef, nodes=True) if cmds.objectType(c, isType='transform')][0]
    groupCam(cam)
    
    return cam


def getCineShotFromSeqNode(cineSeqNode):
    seq = cineSeqNode.seq
    shotNumber = getNewShotNumber()
    start = cmds.playbackOptions(query=True, minTime=True)
    end = cmds.playbackOptions(query=True, maxTime=True)
    cam = referenceCam(cineSeqNode)
    cineShot = cc.CineShot(seq, shotNumber, start, end, cam, 
                        cineSeqNode.stageNumber, cineSeqNode.version)

    return cineShot


@decorators.track_fnc
def makeNewShot():
    seqNodes = cmds.ls("*Sequence_Node")
    if not seqNodes:
        #print 'no sequence node'
        nodeUI = csn.MayaSequenceNodeUI()
        nodeUI.mayaCineStartUI(nodeUI)
    else:
        mayaNode = seqNodes[0]
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode)
        #if this is a shot file not a previs sequence
        #just bring in a new camera
        if cineSeqNode.isShot:
            cineShot = getCineShotFromSeqNode(cineSeqNode)
            makeShot(cineShot)
        else:
            referenceCam(cineSeqNode)
