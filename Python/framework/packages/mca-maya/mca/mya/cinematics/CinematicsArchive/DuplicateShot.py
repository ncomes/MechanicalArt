#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates and includes a shelf with buttons in mya for Cinematics
"""

# mca python imports
import traceback
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
from mca.mya.cinematics.CinematicsArchive.CreateShot import referenceCam


def duplicateSequencerShot(cineShot, newStartTime, cineSeqNode):
    newStopTime = cineShot.end-cineShot.start+newStartTime
    seqStart = int(max([cmds.shot(s, set=True, q=True) for s in cmds.ls(type = 'shot')]))+1
    duplicateNumber = getNewDuplicateNumber(cineShot)
    newName = "d{}_duplicate_{}".format(duplicateNumber, cineShot.name)
    newCam = referenceCam(cineSeqNode)
    cmds.shot(startTime=newStartTime, endTime=newStopTime, sequenceStartTime=seqStart, 
              sn=newName, cc=newCam)
    ns = newCam.rpartition(':')[0]
    cmds.namespace(ren=[ns, newName])


def getNewDuplicateNumber(cineShot):
    duplicateNumber = 1
    dups = [cmds.shot(s, q=True, sn=True) for s in cmds.ls(type='shot') 
            if 'duplicate' in cmds.shot(s, q=True, sn=True) 
            and str(cineShot.number) in cmds.shot(s, q=True, sn=True)]
    if dups:
        duplicateNumber = int(max(dups)[0])+1

    return duplicateNumber


def getNewStartTime():
    lastShotEnd = int(max([cmds.shot(s, et=True, q=True) for s in cmds.ls(type='shot')]))
    newStartTime = lastShotEnd + 1000   
    
    return newStartTime
    
    
def copyAllAnimation(cineShot, newStartTime):
    anim = cmds.ls(type="animCurve")
    newEndTime = cineShot.end+newStartTime
    #
    if anim:
        for each in anim:
            cmds.setKeyframe(each, time=(cineShot.start, cineShot.end), insert=True)
            cmds.copyKey(each, time=(cineShot.start, cineShot.end))
            try:
                cmds.setKeyframe(each, time=(newStartTime-1), insert=True)
                cmds.pasteKey(each, time=(newStartTime, newEndTime), option='replace')
            except RuntimeError(e):
                e = str(e).rstrip()
                if e in ["Nothing to paste from"]:
                    pass
                else:
                    print(traceback.format_exc())
                    raise
    else:
        print("No animation in " + cineShot.name)
        pass
    print("All Done!")


@decorators.track_fnc
def duplicateShot():
    seqNodes = cmds.ls("*Sequence_Node")
    if seqNodes:
        mayaSeqNode = seqNodes[0]
        selShot = [x for x in cmds.ls(sl=True) if x in cmds.ls(type='shot')]
        if selShot:
            cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaSeqNode)
            cineShot = cc.CineShot.getCineShotFromMayaShot(selShot[0], cineSeqNode)
            newStartTime = getNewStartTime()
            duplicateSequencerShot(cineShot, newStartTime, cineSeqNode)
            copyAllAnimation(cineShot, newStartTime)
        else:
            print('No Shot Selected')
    else:
        nodeUI = csn.MayaSequenceNodeUI()
        nodeUI.mayaCineStartUI(nodeUI)
    
