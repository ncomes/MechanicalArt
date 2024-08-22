#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
import os
from functools import partial
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
from mca.mya.cinematics.CinematicsArchive.MayaSaveVersion import saveNewVersion
from mca.common.modifiers import decorators



#Maya Shelf Button Press



def seqNodeButtonPress(*args):
        UI = MayaSequenceNodeUI()
        seqNodes = cmds.ls("*Sequence_Node")
        if seqNodes:
            UI.editSequenceNode()
        else:
            UI.mayaCineStartUI()

class CineSequenceNode:
    #python class for the mya node that lives in scene and holds information
    def __init__(self, seq, isShot, version, stageNumber,
                 notes=None, sceneName=None, shotNumber=None):
        self.seq = seq
        self.isShot = isShot
        self.sceneName = sceneName
        self.shotNumber = shotNumber
        self.version = version
        self.stageNumber = stageNumber
        stages = ["previs", "layout", "animation"]
        self.stageString = stages[self.stageNumber]
        self.notes = notes
        self.name = "{}_Sequence_Node".format(self.seq.name)

    #-----------------------------------------------------------------------()
    
    #Maya Node
    
    @staticmethod
    def getCineSeqNode(mayaNode):
        seqName = cmds.getAttr('{}.sequenceName'.format(mayaNode))
        version = CineSequenceNode.getVersionNumber(mayaNode)
        stage = cmds.getAttr('{}.stage'.format(mayaNode))
        isShot = cmds.getAttr('{}.isShotFile'.format(mayaNode))
        shn = cmds.getAttr('{}.shotNumber'.format(mayaNode))
        scn = cmds.getAttr('{}.sceneName'.format(mayaNode))
        seqsDir = cc.CineStaticClass.sequencesFolderPath
        path = os.path.join(seqsDir, seqName)
        seq = cc.CineSequence(seqName, path)
        cineSeqNode = CineSequenceNode(seq, isShot, version, stage, 
                                    notes=CineSequenceNode.getNotes(mayaNode), sceneName=scn, shotNumber=shn)
       
        return cineSeqNode
    @staticmethod
    def getVersionNumber(mayaNode):
        fName = cmds.file(q=True, sn=True, shn=True)
        noExt = os.path.splitext(fName)[0]
        vNumber = noExt[-3:]
        version = 0
        try:
            version = int(vNumber)
        except ValueError as e:
            #print(e)
            version = cmds.getAttr('{}.versionNumber'.format(mayaNode))
        
        return version
    
    @staticmethod
    def getNotes(mayaNode):
        if cmds.attributeQuery("notes", node=mayaNode, ex=True):
            notes = cmds.getAttr("{}.notes".format(mayaNode))

            return notes
        else:
            #print('no notes')
            
            return None

    @staticmethod
    def setNotes(mayaNode, nts):
        if cmds.attributeQuery("notes", node=mayaNode, ex=True):
            cmds.lockNode(mayaNode, l=False)
            cmds.setAttr("{}.notes".format(mayaNode), l=False)
            cmds.setAttr("{}.notes".format(mayaNode), nts, type='string')
            cmds.setAttr("{}.notes".format(mayaNode), l=True)
            cmds.lockNode(mayaNode, l=True)

    def getNewMayaSequenceNode(self):
        mayaNode = cmds.group(n="Sequence_Node", em=True)
        self.addNodeAttributes(mayaNode)

        return mayaNode
    
    def setMayaNode(self, mayaNode):
        cmds.select(mayaNode, r=True)
        cmds.setAttr('{}.sequenceName'.format(mayaNode), self.seq.name, type='string')
        cmds.setAttr('{}.shotNumber'.format(mayaNode), self.shotNumber)
        cmds.setAttr('{}.sceneName'.format(mayaNode), self.sceneName, type='string')
        cmds.setAttr('{}.versionNumber'.format(mayaNode), self.version)
        cmds.setAttr('{}.isShotFile'.format(mayaNode), self.isShot)
        cmds.setAttr('{}.stage'.format(mayaNode), self.stageNumber)
        cmds.setAttr('{}.notes'.format(mayaNode), self.notes, type='string')
        mayaNode = cmds.rename(self.name)
        cmds.select(cl=True)
        self.lockSequenceNode(mayaNode)
        
        return mayaNode
            
    def addNodeAttributes(self, mayaNode):
        cmds.select(mayaNode, r=True)
        cmds.addAttr(sn='sequenceName', dt='string', k=True)
        stages = 'previs:layout:animation'
        cmds.addAttr(sn='stage', at='enum', en=stages, k=True)
        cmds.addAttr(sn='isShotFile', at='bool', k=False)
        cmds.addAttr(sn='shotNumber', at='short', k=True)
        cmds.addAttr(sn='sceneName', dt='string', k=True)
        cmds.addAttr(sn='versionNumber', at='short', k=True)
        cmds.addAttr(sn='notes', dt='string', k=True)
        #Hide unnecessary attributes
        cmds.setAttr('%s.translateX' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.translateY' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.translateZ' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.rotateX' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.rotateY' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.rotateZ' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.scaleX' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.scaleY' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.scaleZ' %(mayaNode), k=False, cb=False, l=True)
        cmds.setAttr('%s.visibility' %(mayaNode), k=False, cb=False, l=True)
        cmds.select(cl=True)
        
    def lockSequenceNode(self, mayaNode):
        cmds.setAttr('%s.sequenceName' %(mayaNode), l=True)
        cmds.setAttr('%s.stage' %(mayaNode), l=True)
        cmds.setAttr('%s.shotNumber' %(mayaNode), l=True)
        cmds.setAttr('%s.sceneName' %(mayaNode), l=True)
        cmds.setAttr('%s.isShotFile' %(mayaNode), l=True)
        cmds.setAttr('%s.versionNumber' %(mayaNode), l=True)
        cmds.setAttr('%s.notes' %(mayaNode), l=True)
        cmds.lockNode(mayaNode)
        
    def unlockSequenceNode(self, mayaNode):
        cmds.lockNode(mayaNode, l=False)
        cmds.setAttr('%s.sequenceName' %(mayaNode), l=False)
        cmds.setAttr('%s.stage' %(mayaNode), l=False)
        cmds.setAttr('%s.shotNumber' %(mayaNode), l=False)
        cmds.setAttr('%s.sceneName' %(mayaNode), l=False)
        cmds.setAttr('%s.versionNumber' %(mayaNode), l=False)
            
    def setEnumWithString(self, mayaNode, attr, value):
        enumString = cmds.attributeQuery(attr, n=mayaNode, listEnum=True)[0]
        enumList = enumString.split(":")
        index = enumList.index(value)
        cmds.setAttr(mayaNode+"."+attr,index)  
        
#-----------------------------------------------------------------------

#Maya UI
class MayaSequenceNodeUI:
    
    #MAIN METHODS
    
    def mayaCineStartUI(self, *args):
        #MAYA UI WINDOW IS CREATED AND POPS UP TO START A CINE FILE
        windowName = 'makeCineFile'
        UIHeader = 'Enter Data and Click OK to Start a Cinematic File'
        UITitle = 'Start Cinematic File'
        
        if cmds.window(windowName, ex=True):
            cmds.deleteUI(windowName, window=True)
            
        UITuple = self.seqNodeUILayout(windowName, UIHeader, UITitle)

        cmds.showWindow(windowName)
    
    def editSequenceNode(self, *args):
        #MAYA UI WINDOW IS CREATED AND POPS UP TO EDIT THE SEQUENCE NODE
        seqNodes = cmds.ls('*Sequence_Node')
        if seqNodes:
            seqNode = seqNodes[0]
            #print("Editing Sequence Node {}".format(seqNode))
            self.editSeqNodeUI(seqNode)
        else:
            #print("No Sequence Node Found in Scene")
            self.mayaCineStartUI()
    
    #-------------------------------------
    
    #BUTTON COMMANDS
    
    def cancelButtonCommandPartial(self, windowName, *args):
        #print("cancel button clicked")
        cmds.deleteUI(windowName, window=True)

    def okButtonCommandPartial(self, seqCodeField, sceneNameField, sceneRadioButton,
                            shotNumberField, shotSceneRadioCollection, stageRadioCollection, 
                            notesField, windowName, *args):
        #print("OK button clicked")
        
        #Check if all fields are filled out
        if self.checkFields(seqCodeField, sceneNameField, shotNumberField,
                            sceneRadioButton, shotSceneRadioCollection, stageRadioCollection):
            #Delete Existing Sequence Nodes
            self.deleteSequenceNodes()
            #Make a seq node class from UI
            cineSeqNode = self.getCineSeqNodeFromUI(seqCodeField, sceneRadioButton, sceneNameField, 
                                            shotNumberField, stageRadioCollection, notesField)
            #Make the mya node
            mayaNode = cineSeqNode.getNewMayaSequenceNode()
            #Set and lock the mya node
            mayaNode = cineSeqNode.setMayaNode(mayaNode)
            #Save a new version in the correct location
            saveNewVersion(cineSeqNode, mayaNode)
            cmds.deleteUI(windowName)
        else:
            print("Not all fields filled out")
        
    def shotChangeCommand(self, shotRadioButton, shotNumberField, *args):
            if cmds.radioButton(shotRadioButton, q=True, sl=True):
                #print('shot radio button selected')
                cmds.intField(shotNumberField, e=True, en=True)
            else:
                #print('shot radio button not selected')
                cmds.intField(shotNumberField, e=True, en=False)
                
    def sceneChangeCommand(self, sceneRadioButton, sceneNameField, *args):
        if cmds.radioButton(sceneRadioButton, q=True, sl=True):
            #print(sceneRadioButton)
            cmds.textField(sceneNameField, e=True, en=True)
        else:
            #print('scene radio button not selected')
            cmds.textField(sceneNameField, e=True, tx=None, en=False)
            
    def checkFields(self, seqCodeField, sceneNameField, shotNumberField,
                    sceneRadioButton, shotSceneRadioCollection, stageRadioCollection):
        seqName = cmds.textField(seqCodeField, q=True, tx=True)
        shotNumber = cmds.intField(shotNumberField, q=True, v=True)
        shotSceneSelection = cmds.radioCollection(shotSceneRadioCollection, q=True, sl=True)
        stageSelection = cmds.radioCollection(stageRadioCollection, q=True, sl=True)
        stageString = self.getRadioButtonSelection(stageRadioCollection)
        
        if len(seqName)>=3 and shotSceneSelection!='NONE' and stageSelection!='NONE':
            selected = cmds.radioButton(sceneRadioButton, q=True, sl=True)
            sceneName = cmds.textField(sceneNameField, q=True, tx=True)
            if selected:
                if not sceneName:
                    return False
                else:
                    return True
            else:
                #shot file
                if stageString == 'animation' and shotNumber == 0:
                    return False
                else:
                    return True
        else:
            return False
            
    #-------------------------------------
    def deleteSequenceNodes(self):
        seqNodes = cmds.ls("*Sequence_Node")
        for seqNode in seqNodes:
            cmds.lockNode(seqNode, l=False)
            cmds.delete(seqNode)
        
    def getCineSeqNodeFromUI(self, seqCodeField, sceneRadioButton, sceneNameField,
                            shotNumberField, stageRadioCollection, notesField):
        seqName = cmds.textField(seqCodeField, q=True, text=True)[:3].upper()
        if cmds.radioButton(sceneRadioButton, q=True, sl=True):
            isShot = False
        else:
            isShot = True
        sceneString = cmds.textField(sceneNameField, q=True, text=True)
        splitList = sceneString.split()
        sceneNameJoin = "_".join(splitList)
        shotInt = cmds.intField(shotNumberField, q=True, v=True)
        stageString = self.getRadioButtonSelection(stageRadioCollection)
        stages = ["previs", "layout", "animation"]
        stage = stages.index(stageString)
        seqsDir = cc.CineStaticClass.sequencesFolderPath
        path = os.path.join(seqsDir, seqName)
        seq = cc.CineSequence(seqName, path)
        version = 1
        nts = "Start File"
        #print("notes field: {}".format(notesField))
        if notesField:
            nts = cmds.textField(notesField, q=True, text=True)
            #print("found notes field, notes are: {}".format(nts))
        cineSeqNode = CineSequenceNode(seq, isShot, version, stage, 
                                    notes=nts, sceneName=sceneNameJoin, shotNumber=shotInt)
        
        return cineSeqNode

    def editSeqNodeUI(self, mayaNode, *args):
        windowName = 'editSeqNode'
        UIHeader = 'Edit The Sequence Node in Scene and Save'
        UITitle = 'Edit Sequence Node'
        if cmds.window(windowName, ex=True):
            cmds.deleteUI(windowName, window=True)
        sc, shn, sn, shr, snr, pr, lr, ar, nf = self.seqNodeUILayout(windowName, UIHeader, UITitle, edit=True)
        cineSeqNode = CineSequenceNode.getCineSeqNode(mayaNode)        
        self.fillEditUI(cineSeqNode, sc, shn, sn, shr, snr, pr, lr, ar)
        
        cmds.showWindow(windowName)
    
    def fillEditUI(self, cineSeqNode, seqCodeField, shotNumberField, sceneNameField, shotRadio, sceneRadio, 
                    previsRadioButton, layoutRadioButton, animationRadioButton):
        cmds.textField(seqCodeField, e=True, tx=cineSeqNode.seq.name)
        if cineSeqNode.shotNumber==None:
            #print('cine seq node has shot value of None')
            cineSeqNode.shotNumber = 0
        #print(shotNumberField)
        cmds.intField(shotNumberField, e=True, v=cineSeqNode.shotNumber)
        cmds.textField(sceneNameField, e=True, tx=cineSeqNode.sceneName)

        if cineSeqNode.isShot:
            cmds.radioButton(shotRadio, e=True, sl=True)
            cmds.intField(shotNumberField, e=True, en=True)
        else:
            cmds.radioButton(sceneRadio, e=True, sl=True)
            cmds.textField(sceneNameField, e=True, en=True)
        if cineSeqNode.stageNumber == 0:
            cmds.radioButton(previsRadioButton, e=True, sl=True)
        if cineSeqNode.stageNumber == 1:
            cmds.radioButton(layoutRadioButton, e=True, sl=True)
        if cineSeqNode.stageNumber == 2:
            cmds.radioButton(animationRadioButton, e=True, sl=True)
            
    def getRadioButtonSelection(self, radButtonCollection):
        radButton = (cmds.radioCollection(radButtonCollection, q=True, sl=True))
        radButtonLabel = cmds.radioButton(radButton, q=True, label=True)
        #print(radButton, radButtonLabel)
        
        return radButtonLabel.lower()
        
    #-------------------------------------
        
    def seqNodeUILayout(self, windowName, UIHeader, UITitle,
                        edit=False):
        #LAYOUT FOR SEQ NODE WINDOW
        UIwidth = 300
        UIheight = 500
        smallChunk = int(UIwidth/10)
        mediumChunk = int(UIwidth/7)
        
        UI = cmds.window(windowName, mnb=False, mxb=False, s=False,
                    title=UITitle, menuBar=False, menuBarVisible=False)
        #new layout
        rootLayout = cmds.columnLayout(rowSpacing=15, adjustableColumn=True, cat=['both', 15])
        cmds.text("\n{}".format(UIHeader))

        #new layout
        seqCodeLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)

        cmds.text(label="", w=smallChunk)
        cmds.text("3-Letter Sequence Code: ")
        cmds.text(label="")
        seqCodeField = cmds.textField(width=50)
        cmds.text(label="", w=smallChunk)

        #new layout
        sceneShotLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)
        sceneShotRadioCollection = cmds.radioCollection()

        cmds.text(label="", w=mediumChunk)
        shotRadioButton = cmds.radioButton(label='Shot File')
        cmds.text(label="")
        sceneRadioButton = cmds.radioButton(label='Scene File')
        cmds.text(label="", w=mediumChunk)

        #new layout
        shotNumLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)

        cmds.text(label="", w=smallChunk*2)
        cmds.text("Shot Number: ")
        cmds.text(label="")
        shotNumberField = cmds.intField(width=50, en=False)
        cmds.text(label="", w=smallChunk)
        
        #new layout
        sceneNameLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)

        cmds.text(label="", w=smallChunk/4)
        cmds.text("Scene Name: ")
        cmds.text(label="")
        sceneNameField = cmds.textField(width=150, en=False, tx=None)
        cmds.text(label="", w=smallChunk)

        #Add change commands to radio buttons after existence of text and int fields
        cmds.radioButton(sceneRadioButton, e=True, cc=partial(self.sceneChangeCommand, sceneRadioButton, sceneNameField))
        cmds.radioButton(shotRadioButton, e=True, cc=partial(self.shotChangeCommand, shotRadioButton, shotNumberField))
        
        #new layout
        stageLayout = cmds.columnLayout(rowSpacing=15, 
                                        adjustableColumn=True, cat=['both', 15], p=rootLayout)                        
        cmds.text("\n{}".format("Stage"), al='center', p=stageLayout)

        #new layout
        stageRadioLayout = cmds.rowLayout(numberOfColumns=5, p=stageLayout, ad5=3)
        stageRadioCollection = cmds.radioCollection()

        previsRadioButton = cmds.radioButton( label='Previs')
        cmds.text(label="", w=smallChunk/1.5)
        layoutRadioButton = cmds.radioButton( label='Layout')
        cmds.text(label="", w=smallChunk/1.5)
        animationRadioButton = cmds.radioButton( label='Animation')

        cmds.text(label="", p=rootLayout)

        #new layout for editing notes
        notesField = None
        if edit:
            cmds.text(label="Notes", p=rootLayout)
            notesField = cmds.textField(width=300, tx=None, p=rootLayout)

        #new layout
        buttonLayout = cmds.rowLayout(numberOfColumns=5, p=rootLayout, ad5=3)

        cmds.text(label="", w=smallChunk)
        okC = partial(self.okButtonCommandPartial, seqCodeField, sceneNameField, sceneRadioButton,
                    shotNumberField, sceneShotRadioCollection,stageRadioCollection, notesField, windowName)
        okButton = cmds.button(label="Save", w=75, command=okC)
        cmds.text(label="")
        cancelC = partial(self.cancelButtonCommandPartial, windowName)
        cancelButton = cmds.button(label="Cancel", w=75, command=cancelC)
        cmds.text(label="", w=smallChunk)
        
        #new layout
        cmds.text(label="", p=rootLayout)

        cmds.showWindow(windowName)
        return (seqCodeField, shotNumberField, sceneNameField, shotRadioButton, sceneRadioButton,
                previsRadioButton, layoutRadioButton, animationRadioButton, notesField)


#MayaSequenceNodeUI().seqNodeButtonPress()

        
      