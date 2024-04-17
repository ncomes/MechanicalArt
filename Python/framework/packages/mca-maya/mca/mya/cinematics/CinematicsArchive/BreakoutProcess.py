#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools that help with cleaning up a scene
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.mya.cinematics.CinematicsArchive.MayaSaveVersion import saveNewVersion
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import maya.mel as mm


def breakOut(cineClass, cineSeqNode, mayaNode, cleanAnim=False, seqsDir=None):
    cleanFile(cineSeqNode, cineClass, cleanAnim)
    csn, mn = setSeqNode(cineSeqNode, cineClass, mayaNode, cleanAnim)
    saveNewVersion(csn, mn, seqsDir=seqsDir)


def setSeqNode(cineSeqNode, cineClass, mayaNode, cleanAnim):
    stage = cmds.getAttr('{}.stage'.format(mayaNode))
    if stage != 2:
        if cleanAnim:
            s = 2
        else:
            s = 1
        cmds.lockNode(mayaNode, l=False)
        # set stage to layout
        cmds.setAttr('{}.stage'.format(mayaNode), l=False)
        cmds.setAttr('{}.stage'.format(mayaNode), s)
        cineSeqNode.stageNumber = cmds.getAttr('{}.stage'.format(mayaNode))
        cineSeqNode.stageString = cmds.getAttr('{}.stage'.format(mayaNode), asString=True)
        cmds.setAttr('{}.stage'.format(mayaNode), l=True)
        if cineSeqNode.isShot:
            # set shot number
            cineSeqNode.shotNumber = cineClass.number
            cmds.setAttr('{}.shotNumber'.format(mayaNode), l=False)
            cmds.setAttr('{}.shotNumber'.format(mayaNode), cineClass.number)
            cmds.setAttr('{}.shotNumber'.format(mayaNode), l=True)
            cmds.lockNode(mayaNode, l=True)
    else:
        print("This is already an animation file")

    return cineSeqNode, mayaNode


def cleanFile(cineSeqNode, cineClass, cleanAnim):
    if cleanAnim:
        cleanAnimation(cineClass)
        deleteExtraLayout()
        deleteEmptyDisplayLayers()
    shiftAnimation(cineClass)
    offsetAudio(cineClass)
    
    if cineSeqNode.isShot:
        #lock camera
        if cleanAnim and not cmds.camera(cineClass.cam.mayaCam, q=True, lt=True):
            cmds.camera(cineClass.cam.mayaCam, e=True, lt=True)
        deleteExtraCameras(cineClass)
        #delete all shots
        allShots = cmds.ls(type = 'shot')
        for s in allShots:
            cmds.shot(s, e=True, lck=False)
        cmds.delete(allShots)
        #recreate shot
        #print('recreating shot')
        sht = cmds.shot(sn=cineClass.name, st=cineClass.start, 
                    et=cineClass.end, cc=cineClass.cam.mayaCam, sst=0)
        if cleanAnim:
            cmds.shot(sht, e=True, lock=True)


def deleteEmptyDisplayLayers():
    dlayers = cmds.ls(type='displayLayer')
    #print(dlayers)
    for l in dlayers:
        dlayerMembers = cmds.editDisplayLayerMembers(l, q=True)
        if not dlayerMembers and 'default' not in l:
            try:
                cmds.delete(l)
            except RuntimeError:
                print('cannot delete display layer {}'.format(l))
                pass


def deleteExtraLayout():
    layoutGrp = 'layout_grp'
    if cmds.objExists(layoutGrp):
        layoutRel = cmds.listRelatives(layoutGrp)
        if layoutRel:
            for each in layoutRel:
                cmds.lockNode(each, l=0)
        cmds.delete(layoutGrp)


def deleteExtraCameras(cineShot):
    camGrp = 'cameras_grp'
    if cmds.objExists(camGrp):
        for obj in cmds.listRelatives(camGrp):
            if cmds.objExists(obj) and cc.CineStaticClass.isShotCam(obj):
                match = False
                if 'Shape' in cineShot.cam.mayaCam and cmds.listRelatives(obj, s=True)[0] == cineShot.cam.mayaCam:
                    match = True
                elif obj == cineShot.cam.mayaCam:
                    match = True
                    
                if not match:                
                    #print(obj, sht.cam.mayaCam)
                    refPath = cmds.referenceQuery(obj, filename=True)
                    ns = ":{}".format(cmds.file(refPath, q=True, namespace=True))
                    #remove the reference and its contents
                    cmds.file(refPath, rr=True, f=True)
                    #attempt to remove camera namespace
                    try:
                        cmds.namespace(mv=[ns,':'], f=True)
                        if ns in cmds.namespaceInfo(lon=1):
                            cmds.namespace(rm=ns)
                    except RuntimeError:
                        pass
                    
                    
def handleAnimLayers():
    animLayers = cmds.ls(type='animLayer')
    #print animLayers
    if animLayers:
        for layer in animLayers:
            cmds.animLayer(layer, e=True, l=False)
            #print 'unlocked anim layers'
        mm.eval('source "performAnimLayerMerge.mel"')
        mm.eval('animLayerMerge(`ls -type animLayer`)')
        #print('baked anim layers')


def cleanAnimation(cineClass):
    handleAnimLayers()
    handles = 50
    anim = cmds.ls(type='animCurve')
    if anim:
        animStart = min([cmds.findKeyframe(x, which='first') for x in anim ])
        #print animStart
        animEnd = max([cmds.findKeyframe(x, which='last') for x in anim])
        #print animEnd
        for a in anim:
            #KEY EVERYTHING IN ANIMATION AT THE START AND THE STOP TIME OF THE SHOT + HANDLES
            cmds.setKeyframe(a, time=(cineClass.start, cineClass.end), i=True)
            cmds.setKeyframe(a, time=(cineClass.start-handles, cineClass.end+handles), i=True)
            cmds.cutKey(a, time=(animStart, cineClass.start-handles), cl=True)
            cmds.cutKey(a, time=(animEnd, cineClass.end+handles), cl=True)


def offsetAudio(cineClass):
    audio = cmds.ls(type='audio')
    if audio:
        a = audio[0]
        if cineClass.isShot:
            mayaShot = cineClass.getMayaShotFromCineShot()
            if mayaShot:
                offsetTime = cmds.shot(mayaShot, q=True, sst=True)
        else:
            offsetTime = cineClass.start
        if offsetTime!=0:
            cmds.setAttr('{}.offset'.format(a), -offsetTime)
            

def shiftAnimation(cineClass):
    endTime = cineClass.end-cineClass.start
    #set mya timeline
    cmds.playbackOptions(min=0)
    cmds.playbackOptions(ast=0)
    cmds.playbackOptions(max=endTime)
    cmds.playbackOptions(aet=endTime)    
    #offset animation to frame 0
    anim = cmds.ls(type='animCurve')
    if anim:
        try:
            cmds.keyframe(anim, 
                hi='below', edit=True, r=True, iub=True, option='over', timeChange=(-cineClass.start))
        except RuntimeError:
            #print('cannot move keys for some stupid reason')
            pass

    #change cine start and end times
    cineClass.start = 0
    cineClass.end = endTime