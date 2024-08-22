#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
import sys
# PySide2 imports
# software specific imports
import maya.standalone
# initialize python in mya standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn


fileName = sys.argv[1]
mayaNode = sys.argv[2]
seqsDir = sys.argv[3]



def batchBreakout():
    #open file
    cmds.file(fileName, o=True, f=True)
    #find sequence node
    cineShots = []
    mayaShots = []
    cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode) 
    if cineSeqNode.isShot and cineSeqNode.stageNumber!=2:
        mayaShots = cmds.ls(type='shot')
        selectedShots = [s for s in cmds.ls(sl=True) if s in mayaShots]
        if selectedShots:
            mayaShots = selectedShots
    for sht in mayaShots:
        cineShots.append(cc.CineShot.getCineShotFromMayaShot(sht, cineSeqNode))
    #close main file
    cmds.quit(f=True)
    #
    breakoutShots(cineShots, cineSeqNode)
    
    
def breakoutShots(cineShots, cineSeqNode):
    from BreakoutProcess import breakOut
    for sht in cineShots:
        cmds.file(fileName, o=True, f=True)
        #testDestination = r'C:\\Users\\ctshe\\Desktop\\pipelineRedux\\testBatchOutput'
        #cmds.file(rename=testDestination+'\\testExport_'+str(cineShots.index(sht))+'.ma')
        #cmds.file(save=True)
        breakOut(sht, cineSeqNode, mayaNode, seqsDir=seqsDir)
        cmds.quit(f=True)

batchBreakout()
