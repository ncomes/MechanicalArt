import maya.standalone
#initialize python in mya standalone
maya.standalone.initialize(name='python')
import os
import sys
import maya.cmds as cmds
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
from mca.mya.cinematics.CinematicsArchive.OpenCineFile import openMayaFile
import mca.mya.cinematics.CinematicsArchive.MayaExportProcess

fileName = sys.argv[1]
mayaNode = sys.argv[2]
stageString = sys.argv[3]

def getShotFiles(mayaNode):
    shotsDir = cc.CineStaticClass.getShotDirDict(fileName)['allShots']
    shotNames = sorted(os.listdir(shotsDir))
    shotFiles = []
    for shotName in shotNames:
        #print('found shot: {}'.format(shotName))
        stageDir = r'{}\\{}\\{}'.format(shotsDir, shotName, stageString).replace(os.sep, '/')
        latest = cc.CineStaticClass.getLatestFileVersion(stageDir)
        shotFiles.append(latest)
    
    #print(shotFiles)
    
    return shotFiles

def batchExportMayaSequence():
    shotFiles = getShotFiles(mayaNode)
    for shotPath in shotFiles:
        openMayaFile(shotPath, refresh=False)
        cmds.loadPlugin('fbxmaya')
        cmds.dgdirty(allPlugs=True)
        mayaSeqNodes = cmds.ls('*Sequence_Node')
        
        if mayaSeqNodes:
            mayaSeqNode = mayaSeqNodes[0]
            cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaSeqNode)
            mayaShots = cmds.ls(type='shot')
            if mayaShots:
                mayaShot = mayaShots[0]
                cineShot = cc.CineShot.getCineShotFromMayaShot(mayaShot, cineSeqNode)                
            else:
                cineShot = cc.CineShot.getCineShotFromSeqNode(cineSeqNode)
            exporter = MayaExportProcess.MayaExporter()
            exporter.exportAnimation(cineShot)                
        else:
            print('No Sequence Node found in shot: {}'.format(shotPath))

batchExportMayaSequence()