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
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
from  mca.mya.cinematics.CinematicsArchive.CineSequenceNodes import CineSequenceNode as csn
from functools import partial



def renameShot():
    selShot = [x for x in cmds.ls(sl=True) if x in cmds.ls(type='shot')]
    if not selShot:
        sel = cmds.ls(sl=True)
        if sel:
            cam = sel[0]
            if cc.CineStaticClass.isShotCam(cam):
                renameCameraUI(cam)
    else:
        sht = selShot[0]
        renameShotUI(sht)


def renameShotUI(mayaShot):
    cineSeqNode = csn.getCineSeqNode(cc.CineStaticClass.getMayaSeqNode())
    cineShot = cc.CineShot.getCineShotFromMayaShot(mayaShot, cineSeqNode)
    UITitle = 'Rename Shot'
    UIHeader = "Rename Shot: {}".format(cmds.shot(mayaShot, q=True, sn=True))
    renameUI(mayaShot, UITitle, UIHeader, cineShot, True)


def renameCameraUI(cam):
    cineSeqNode = csn.getCineSeqNode(cc.CineStaticClass.getMayaSeqNode())
    cineShot = cc.CineShot.getCineShotFromSeqNode(cineSeqNode)
    UITitle = 'Rename Camera'
    UIHeader = "Rename Camera: {}".format(cam)
    renameUI(cam, UITitle, UIHeader, cineShot, False)


def renameButtonCommandPartial(obj, newNumberField, cineShot, windowName, isMayaShot, *args):
    newNumberInput = cmds.intField(newNumberField, q=True, v=True)
    if newNumberInput<=0:
        print("shot number must be positive")
    else:
        formattedNewNumber = "{0:0=3d}".format(newNumberInput)
        newShotName = '{}_shot_{}'.format(cineShot.seq.name, formattedNewNumber)
        shotCameraNameSpaceList = cineShot.cam.mayaCam.rpartition(':')
        if shotCameraNameSpaceList:
            shotCameraNameSpace = shotCameraNameSpaceList[0]
            if newShotName != shotCameraNameSpace:
                cc.CineStaticClass.handleNamespaceConflict(newShotName)
                print('rename {} to {}'.format(shotCameraNameSpace, newShotName))
                cmds.namespace(set=':')  
                cmds.namespace(ren=[shotCameraNameSpace, newShotName])
        else:
            print('no namespace to change on camera {}'.format(cineShot.cam.mayaCam))
            
        if isMayaShot:
            #change the shot name
            #print('this is a mya shot')
            if(cmds.shot(obj, q=True, lck=True)):
                cmds.shot(obj, e=True, lck=False)
            cmds.shot(obj, e=True, sn=newShotName)
            
        cmds.deleteUI(windowName, window=True)


def cancelButtonCommandPartial(windowName, *args):
        #print("cancel button clicked")
        cmds.deleteUI(windowName, window=True)


def renameUI(obj, UITitle, UIHeader, cineShot, isMayaShot):
    #LAYOUT FOR RENAME SHOT WINDOW
    windowName = 'renameShotWindow'
    if cmds.window(windowName, ex=True):
            cmds.deleteUI(windowName, window=True)
    UIwidth = 10
    UIheight = 500
    smallChunk = 5
    mediumChunk = 50

    UI = cmds.window(windowName, mnb=False, mxb=False, s=False,
                    title=UITitle, menuBar=False, menuBarVisible=False)
    #new layout
    rootLayout = cmds.columnLayout(rowSpacing=15, adjustableColumn=True, cat=['both', 25])
    cmds.text("\n{}".format(UIHeader))

    #new layout
    buttonLayout = cmds.rowLayout(numberOfColumns=3, p=rootLayout, ad5=2)
    cmds.text(label="", w=mediumChunk)
    newNumberField = cmds.intField()
    cmds.text(label="", w=mediumChunk)

    #new layout
    buttonLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)
    cmds.text(label="", w=smallChunk)
    okC = partial(renameButtonCommandPartial, obj, newNumberField, cineShot, windowName, isMayaShot)
    okButton = cmds.button(label="Rename", w=75, command=okC)
    cmds.text(label="")
    cancelC = partial(cancelButtonCommandPartial, windowName)
    cancelButton = cmds.button(label="Cancel", w=75, command=cancelC)
    cmds.text(label="", w=smallChunk)

    cmds.text("", parent=rootLayout)

    cmds.showWindow(windowName)
