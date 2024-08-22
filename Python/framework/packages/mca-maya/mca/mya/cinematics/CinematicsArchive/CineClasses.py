#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
import os
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
from mca.common.project import project_paths


class CineStaticClass:
    mayaPyPath = r'{}{}'.format(os.environ['MAYA_LOCATION'], '\\bin\\mayapy')
    doNotSaveName = "DO NOT SAVE"
    shelfInstance = None
    projectPath = project_paths.MCA_PROJECT_ROOT
    customPyDir = ""
    iconPath = r'{}{}'.format(projectPath, '\\Python\\framework_2-1-0\\packages\\mca-mya\\mca\\mya\\cinematics\\icons')
    sequencesFolderPath = r'{}{}'.format(projectPath,'\\Cinematics\\Sequences')
    cameraPath = r'{}{}'.format(projectPath,'\\Cinematics\\Assets\\camera\\shotCam_2point35_30fps_v1.ma')
    scriptsPath = r'{}{}'.format(projectPath, '\\Python\\framework_2-1-0\\packages\\mca-mya\\mca\\mya\\cinematics')

    
    @staticmethod    
    def setProjectPaths():
        #print('setting project paths')
        CineStaticClass.customPyDir = r'{}{}'.format(
                                    CineStaticClass.projectPath, 
                                    '\\Python\\framework_2-1-0\\packages\\mca-mya\\mca\\mya\\cinematics')
        CineStaticClass.iconPath = r'{}{}'.format(
                                    CineStaticClass.projectPath,CineStaticClass.projectPath, 
                                    '\\Python\\framework_2-1-0\\packages\\mca-mya\\mca\\mya\\cinematics\\icons')
        CineStaticClass.sequencesFolderPath = r'{}{}'.format(
                                    CineStaticClass.projectPath,'\\Cinematics\\Sequences')
        CineStaticClass.cameraPath = r'{}{}'.format(
                                    CineStaticClass.projectPath,'\\Cinematics\\Assets\\camera\\shotCam_2point35_30fps_v1.ma')
        CineStaticClass.scriptsPath = r'{}{}'.format(
                                    CineStaticClass.projectPath, 
                                    '\\Python\\framework_2-1-0\\packages\\mca-mya\\mca\\mya\\cinematics')
        
    @staticmethod
    def getShotDirDict(filePath=None, maya=True):
        if maya and not filePath:
            filePath = cmds.file(q=True, sn=True)
        
        stageDir = os.path.dirname(filePath).replace(os.sep, '/')
        shotNumDir = os.path.dirname(stageDir).replace(os.sep, '/')
        exportDir = "{}/{}".format(shotNumDir, "exports").replace(os.sep, '/')
        shotsDir = os.path.dirname(shotNumDir).replace(os.sep, '/')
        seqDir = os.path.dirname(shotsDir).replace(os.sep, '/')
        videoDir = os.path.join(seqDir, "video").replace(os.sep, '/')
        playBlastDir = os.path.join(videoDir, "playblasts").replace(os.sep, '/')
        previsVideoDir = os.path.join(shotNumDir, "video").replace(os.sep, '/')
        previsPlayblastDir = os.path.join(previsVideoDir, "playblasts").replace(os.sep, '/')
        mainDir = os.path.dirname(seqDir).replace(os.sep, '/')
        
        shotDirDict = {
            'file':filePath,
            'stage': stageDir,
            'shot': shotNumDir,
            'exports': exportDir,
            'allShots': shotsDir,
            'video' : videoDir,
            'playblast' : playBlastDir,
            'previsPlayblast' : previsPlayblastDir,
            'sequence': seqDir,
            'main' : mainDir}
        
        return shotDirDict

    @staticmethod
    def getLatestFileVersion(stageDir):
        if os.path.exists(stageDir):
            shotStageFiles = os.listdir(stageDir)
            #print shotStageFiles
            fileVersions = {}
            for shotFile in shotStageFiles:
                filePath = "{}/{}".format(stageDir, shotFile)
                #print aFilePath
                fileName = os.path.splitext(shotFile)[0]
                versionNumber = fileName[-3:]
                #print versionNumber
                try:
                    n = int(versionNumber)
                    fileVersions[filePath] = versionNumber
                except ValueError:
                    pass
            if fileVersions:
                latestShotPath = max(fileVersions, key=fileVersions.get)

                return latestShotPath
        else:
            return None

    @staticmethod
    def handleNamespaceConflict(name):
        if cmds.namespace(ex=name):
            #nameNumber is the number of temp shots existant
            nameNumber = 1 + len([x for x in map(str, cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)) 
                                    if "tempName" in x])
            tempName = 't{}_tempName_{}'.format(nameNumber, name)
            #print('renaming namespace {} to {}'.format(name, tempName))
            cmds.namespace(set=':')
            cmds.namespace(ren=[name, tempName])
            associatedShots = [x for x in cmds.ls(type='shot') if name in cmds.shot(x, q=True, cc=True)]
            if associatedShots:
                cmds.shot(associatedShots[0], e=True, sn=tempName)

    @staticmethod
    def isShotCam(obj):
        defCams = ['perspShape', 'frontShape',  'sideShape', 'topShape', 'leftShape',  
                    'bottomShape', 'backShape']
        if cmds.objectType(obj) == 'camera' and obj not in defCams:
            return True
        else:
            sList = cmds.listRelatives(obj, s=True)
            if sList:
                s=sList[0]
                if cmds.objectType(s) == 'camera' and s not in defCams:
                    return True
                else:
                    return False
            else:
                return False
    @staticmethod
    def getMayaSeqNode():
        seqNodes = cmds.ls("*Sequence_Node")
        if seqNodes:
            seqNode = seqNodes[0]

            return seqNode
        else:
            return None

class CineSequence:
    def __init__(self, name,
                 shots=None, scenes=None):
        self.name = name
        #self.path = os.path.join(CineStaticClass.sequencesFolderPath, name)
        self.shots = shots
        self.scenes = scenes
        
class CineShot:
    def __init__(self, seq, number, start, end, cam, stage, version, 
                 omit=False, chars=None, props=None):
        self.isShot = True
        self.seq = seq
        self.number = number 
        self.name = "{}_shot_{:0>3}".format(self.seq.name, self.number)
        self.cam = CineCamera(seq, number, cmds.getAttr('{}.focalLength'.format(cam)), cam, version)
        self.start = start
        self.end = end
        self.stages = ["previs", "layout", "animation"]
        if stage>(len(self.stages)-1):
            stage = 0
        self.stageNumber = stage
        self.stageString = self.stages[stage]
        self.version = version
        self.omit = omit
        self.chars = chars
        self.props = props

    def getMayaShotFromCineShot(self):
        shots = cmds.ls(type='shot')
        foundMayaShot = None
        if shots:
            sht = [s for s in shots if self.name in cmds.shot(s, q=True, sn=True)]
            if sht:
                foundMayaShot = sht[0]
        
        return foundMayaShot
            
    
    @staticmethod
    def getCineShotFromMayaShot(mayaShot, cineSeqNode):
        seq = cineSeqNode.seq
        shotNumber = int(cmds.shot(mayaShot, q=True, sn=True)[-3:])
        start = cmds.shot(mayaShot, q=True, st=True)
        end = cmds.shot(mayaShot, q=True, et=True)
        cam = cmds.shot(mayaShot, q=True, cc=True)
        cineShot = CineShot(seq, shotNumber, start, end, cam, 
                            cineSeqNode.stageNumber, cineSeqNode.version)

        return cineShot

    @staticmethod
    def getCineShotFromSeqNode(cineSeqNode):
        seq = cineSeqNode.seq
        shotNumber = cineSeqNode.shotNumber
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)
        cams = [c for c in cmds.listCameras(p=True) if CineStaticClass.isShotCam(c)]
        if cams:
            cam=cams[0]
        else:
            cam=None
        cineShot = CineShot(seq, shotNumber, start, end, cam, 
                            cineSeqNode.stageNumber, cineSeqNode.version)

        return cineShot
    

class CineScene:
    def __init__(self, seq, nameElementsList, stage, version, 
                 start=None, end=None, omit=False, chars=None, props=None):
        self.isShot = False
        self.seq = seq
        self.nameList = nameElementsList
        self.stages = ["previs", "layout", "animation"]
        if int(stage)>(len(self.stages)-1):
            stage = 0
        self.stage = self.stages[stage]
        self.version = version
        self.start = start
        self.end = end
        self.omit = omit
        self.chars = chars
        self.props = props
        #need a way to join all the elements in the list separated by underscores
        self.name = '_'.join(self.nameList)

    @staticmethod
    def getCineSceneFromSeqNode(cineSeqNode):
        seq = cineSeqNode.seq
        sceneName = cineSeqNode.sceneName
        nameList = sceneName.split("_")
        start = cmds.playbackOptions(query=True, minTime=True)
        end = cmds.playbackOptions(query=True, maxTime=True)
        cineScene = CineScene(seq, nameList, cineSeqNode.stageNumber, cineSeqNode.version,
                                start=start, end=end)

        return cineScene      
              
class CineCharacter:
    def __init__(self, name, version
                 ): 
      self.name = name
      self.displayName = name.rpartition(':')[0]
      self.version = version

class CineProp:
    def __init__(self, name, attachment, version, 
                 char=None, rigged=False):
        self.name = name
        self.displayName = name.rpartition(':')[0]
        self.char = char
        self.attachments = ["world", "weapon_r", "weapon_l", "utility", "other"]
        if attachment>(len(self.attachments)-1):
            attachment = 0
        self.attachment = self.attachments[attachment]
        self.rigged = rigged
        self.version = version
    
    @staticmethod
    def getCinePropFromElementName(mayaName, cineShot):
        #print('mayaPropName: {}'.format(mayaName))
        rootCtrl = '{}:root_ctrl'.format(mayaName.rpartition(':')[0])
        if cmds.objExists(rootCtrl):
            rig = True
        else:
            rig = False
        
        if cmds.parentConstraint(mayaName, q=True, tl=True):
            #print('prop is constrained')
            constrainedParent = cmds.parentConstraint(mayaName, q=True, tl=True)[0]
            parentNameList = constrainedParent.rpartition(':')
            #character
            if parentNameList:
                character = CineCharacter(constrainedParent, cineShot.version)
            else:
                character = None
            #attachment
            if 'weapon_r' in constrainedParent:
                attachment = 1
            elif 'weapon_l' in constrainedParent:
                attachment = 2
            elif 'utility' in constrainedParent:
                attachment = 3
            else:
                #reads as 'other'
                attachment = 4
        else:
            #print('prop in world space')
            attachment = 0
            character = None
        prop = CineProp(mayaName, attachment, cineShot.version, char=character, rigged=rig)
        
        return prop
      
class CineCamera:
    def __init__(self, seq, number, focalLength, mayaCam, version
                 ):
        self.seq = seq
        self.number = number
        self.displayName = "{}_shot_{:0>3}_cam".format(seq.name, number)
        self.focalLength = focalLength
        self.mayaCam = mayaCam
        self.version = version
      
