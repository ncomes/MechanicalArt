import maya.cmds as cmds
import os
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc

def saveNewVersion(cineSeqNode, mayaNode, seqsDir=None, *args):
    print('Saving {} Version {} of {}'.format(
            cineSeqNode.stageString, cineSeqNode.version, cineSeqNode.name))
    if not seqsDir:
        seqsDir = cc.CineStaticClass.sequencesFolderPath
    seqDir = os.path.join(seqsDir, cineSeqNode.seq.name)
    if not os.path.exists(seqDir):
        makeInitialFolderStructure(seqDir)
    saveDir = getSaveDir(cineSeqNode, seqDir)
    version = getVersionNumber(saveDir)
    updateMayaVersion(mayaNode, version)
    handleStartNotes(cineSeqNode, mayaNode, version)
    cineSeqNode.version = int(version)
    saveFile(saveDir, cineSeqNode)

def makeInitialFolderStructure(seqDir):
    #if no sequence directory, make one and shots dir
    os.mkdir(seqDir)
    dirs = ['mocap', 'assets', 'audio', 'video', 'reference']
    for dir in dirs:
        d = os.path.join(seqDir, dir)
        os.mkdir(d)

def getSaveDir(cineSeqNode, seqDir):
    if cineSeqNode.isShot:
        if cineSeqNode.shotNumber !=0:
            #if file is a shot file with a number
            shotsDir = os.path.join(seqDir, 'shots')
            if not os.path.exists(shotsDir):
                os.mkdir(shotsDir)
            #print('saving shot {} in shots directory'.format(cineSeqNode.shotNumber))
            shotDir = os.path.join(shotsDir, '{0:0=3d}'.format(cineSeqNode.shotNumber))
            if not os.path.exists(shotDir):
                os.mkdir(shotDir)
            stageDir = os.path.join(shotDir, cineSeqNode.stageString)
            if not os.path.exists(stageDir):
                os.mkdir(stageDir)
                
            return stageDir
        else:
            #if file is a shot with a zero number
            ##print('saving in {} directory'.format(cineSeqNode.stageString))
            sequenceFileDir = os.path.join(seqDir, cineSeqNode.stageString)
            if not os.path.exists(sequenceFileDir):
                os.mkdir(sequenceFileDir)

            return sequenceFileDir
    else:
        #if file is a scene
        #print('saving {} in scenes directory'.format(cineSeqNode.sceneName))
        scenesDir = os.path.join(seqDir, 'scenes')
        if not os.path.exists(scenesDir):
            os.mkdir(scenesDir)
        sceneDir = os.path.join(scenesDir, str(cineSeqNode.sceneName))
        if not os.path.exists(sceneDir):
            os.mkdir(sceneDir)
        stageDir = os.path.join(sceneDir, cineSeqNode.stageString)
        if not os.path.exists(stageDir):
            os.mkdir(stageDir)

        return stageDir

def saveFile(location, cineSeqNode):
    if not cineSeqNode.isShot: 
        saveAs = '{}_{}_{}_v{}.ma'.format(cineSeqNode.seq.name, cineSeqNode.sceneName, 
                                    cineSeqNode.stageString, '{0:0=3d}'.format(cineSeqNode.version))
    elif cineSeqNode.isShot and cineSeqNode.shotNumber == 0:
        saveAs = '{}_{}_v{}.ma'.format(cineSeqNode.seq.name, 
                                cineSeqNode.stageString, '{0:0=3d}'.format(cineSeqNode.version))
    else:
        saveAs = '{}_shot_{}_{}_v{}.ma'.format(cineSeqNode.seq.name, '{0:0=3d}'.format(cineSeqNode.shotNumber), 
                                            cineSeqNode.stageString, '{0:0=3d}'.format(cineSeqNode.version))
    newFileName = os.path.join(location, saveAs)
    cmds.file(rename=newFileName)
    #save the file
    cmds.file(save=1, type='mayaAscii', f=1)
    #print('resulting file: {}'.format(newFileName))

def getVersionNumber(selDir):
    listFiles = os.listdir(selDir)
    fileVersions = []
    latestVersionNumber = 0

    for f in listFiles:
        #print('found files in directory')
        fileNoExt = os.path.splitext(f)[0]
        versionNumber = fileNoExt[-3:]
        #print(versionNumber)
        if versionNumber.isnumeric():
            #print 'found version number'
            fileVersions.append(int(versionNumber))
    if fileVersions:
        #print('found file versions')
        latestVersionNumber = max(fileVersions)

    return '{0:0=3d}'.format(latestVersionNumber+1)

def updateMayaVersion(mayaNode, version):
    cmds.lockNode(mayaNode, l=False)
    cmds.setAttr("{}.versionNumber".format(mayaNode), l=False)
    cmds.setAttr("{}.versionNumber".format(mayaNode), int(version))
    cmds.setAttr("{}.versionNumber".format(mayaNode), l=True)
    cmds.lockNode(mayaNode, l=True)



def handleStartNotes(cineSeqNode, mayaNode, version):
    notes = cineSeqNode.getNotes(mayaNode)
    if int(version)>1 and notes == "Start File":
        cineSeqNode.setNotes(mayaNode, "")