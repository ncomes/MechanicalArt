import os, imp
import maya.cmds as cmds
from functools import partial
import mca.mya.cinematics.CinematicsArchive.ShelfButtonCommands as SCom
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
from mca.mya.cinematics.CinematicsArchive.CineClasses import CineStaticClass as csc

shelfName = "Cinematics"
labelBackground = (0, 0, 0, 0)
labelColour = (.9, .9, .9)
openButtonName = 'open'
openVersionButtonName = 'openVersion'

def _null(*args):
    pass


class _shelf():
    '''A simple class to build shelves in mya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    def __init__(self, name="customShelf", iconPath=csc.iconPath, commandModule=SCom, *args):
        self.name = name

        self.iconPath = iconPath
        self.commandMod = commandModule

        self.labelBackground = (0, 0, 0, 0)
        self.labelColour = (.9, .9, .9)
        self._cleanOldShelf()
        cmds.setParent(self.name)
        self.build()

    def printTest(self):
        print('print test proc: successfully reloaded createCinematicShelf.py') 

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def addButton(self, label, icon="commandButton.png", command=_null, doubleCommand=_null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        cmds.setParent(self.name)
        if icon:
            icon = csc.iconPath + icon
        cmds.shelfButton(width=37, height=37, image=icon, l=label, 
                        command=command, dcc=doubleCommand, imageOverlayLabel=label, 
                        olb=self.labelBackground, olc=self.labelColour)    

    def addMenuItem(self, parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = csc.iconPath + icon
        return cmds.menuItem(p=parent, l=label, c=command, i="")

    def addSubMenu(self, parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = csc.iconPath + icon
        return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1)

    @staticmethod
    def addButtonStatic(label, icon="commandButton.png", command=_null, doubleCommand=_null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        cmds.setParent(shelfName)
        if icon:
            icon = csc.iconPath + icon
        cmds.shelfButton(width=37, height=37, image=icon, l=label, 
                        command=command, dcc=doubleCommand,
                        olb=labelBackground, olc=labelColour)

    @staticmethod
    def addMenuItemStatic(parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = csc.iconPath + icon
        return cmds.menuItem(p=parent, l=label, c=command, i="")

    @staticmethod
    def addSubMenuStatic(parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = csc.iconPath + icon
        return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1)

    def _cleanOldShelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if cmds.shelfLayout(self.name, ex=1):
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")

    def reloadShelfCommands(self):
        imp.reload(self.commandMod)

    def deferredCleanup(self):
        self._cleanOldShelf()
        cmds.setParent(self.name)
        self.build()

class dbCineStartShelf(_shelf):
    def build(self):
        self.addButton('Start', command=SCom.start)

class dbCinematicShelf(_shelf):
    def build(self):
        #print ("building self")
        #print('icon path: '+csc.iconPath)
        imp.reload(self.commandMod)
        #
        cmds.separator(style='single')
        #
        self.addButton("", icon="newShot.png", command=SCom.newShot)
        self.addButton("", icon="renameShot.png", command=SCom.renameShot)
        self.addButton("", icon="duplicateShot.png", command=SCom.duplicateShot)
        self.addButton("", icon='copyCam.png', command=SCom.copyCam)
        self.addButton("", icon="camCtrl.png", command=SCom.camControl)
        #
        cmds.separator(style='single')
        #
        self.addButton("", icon="loc.png", command=SCom.loc)
        self.addButton("", icon="bakeLoc.png", command=SCom.bakeLoc)
        self.addButton("", icon='sceneLoc.png', command=SCom.sceneMover)
        self.addButton("", icon="match.png", command=SCom.match)
        self.addButton("", icon="gp.png", command=SCom.grandP)
        self.addButton("", icon="rigProp.png", command=SCom.rigObj, doubleCommand=SCom.rigObjDouble)
        #
        cmds.separator(style='single')
        #
        self.addButton("", icon='editSeqNode.png', command=SCom.editSeqNode)
        self.layoutSubMenuTree()
        #
        cmds.separator(style='single')
        #
        self.addButton("", icon="playblast.png", command=SCom.playblastSingle)
        #
        cmds.separator(style='single')
        #
        self.addButton("", icon="save.png", command=SCom.save)
        self.openSubMenuTree()
        self.openVersionSubMenuTree()
        #
        cmds.separator(style='single')

    def layoutSubMenuTree(self):
        self.addButton("", icon='layout.png')
        p = cmds.popupMenu(b=1)
        self.addMenuItem(p, 'Break Out Selected Shot', command = SCom.breakOutShot)
        self.addMenuItem(p, 'Break Out Multiple Shots', command = SCom.batchBreakOut)
        self.addMenuItem(p, 'Send Scene to Animation', command = SCom.layoutToAnim)
    
    def openSubMenuTree(self):
        self.addButtonStatic("open", icon='open.png')
        p = cmds.popupMenu(b=1)
        mainDir = csc.sequencesFolderPath
        seqs = os.listdir(mainDir)
        stages = ['previs','layout','animation']

        for seq in seqs:
            seqMenuItem = self.addSubMenuStatic(p, seq)
            seqFileStages = ['previs', 'layout']
            for stage in stages[:-1]:
                seqFileDir = os.path.join(mainDir, "{}\\{}".format(seq, stage))
                if os.path.exists(seqFileDir):
                    #print '{} {} yes'.format(seq, stage)
                    latestSeqFile = csc.getLatestFileVersion(seqFileDir)
                    openSeqFileCommand = partial(SCom.openFile, latestSeqFile, True)
                    seqFileItem = self.addMenuItemStatic(seqMenuItem, 
                                                '{} sequence'.format(stage), command=openSeqFileCommand)
                    
            shotsDir = os.path.join(mainDir, "{}\\{}".format(seq, 'shots'))
            if os.path.exists(shotsDir):
                shots = os.listdir(shotsDir)
                if shots:
                    #print "shots in {} directory: {}".format(seq, shots)
                    for sht in shots:
                        shotMenuItem = self.addSubMenuStatic(seqMenuItem, '{}'.format(sht))
                        shotDir = os.path.join(shotsDir, sht)
                        for stage in stages:
                            fileDir = os.path.join(shotDir, stage)
                            if os.path.exists(fileDir):
                                #print '{} {} {} yes'.format(seq, sht, stage)
                                latestFile = csc.getLatestFileVersion(fileDir)
                                #print latestFile
                                openShotCommand = partial(SCom.openFile, latestFile, True)
                                shotItem = self.addMenuItemStatic(shotMenuItem, stage, command=openShotCommand)

            scenesDir = os.path.join(mainDir, "{}\\{}".format(seq, 'scenes'))
            if os.path.exists(scenesDir):
                scenes = os.listdir(scenesDir)
                if scenes:
                    #print "scenes in {} directory: {}".format(seq, scenes)
                    for scn in scenes:
                        sceneMenuItem = self.addSubMenuStatic(seqMenuItem, '{}'.format(scn))
                        sceneDir = os.path.join(scenesDir, scn)
                        for stage in stages:
                            fileDir = os.path.join(sceneDir, stage)
                            if os.path.exists(fileDir):
                                #print '{} {} {} yes'.format(seq, sht, stage)
                                latestFile = csc.getLatestFileVersion(fileDir)
                                #print latestFile
                                openShotCommand = partial(SCom.openFile, latestFile, True)
                                sceneItem = self.addMenuItemStatic(sceneMenuItem, stage, command=openShotCommand)
                                
    def openVersionSubMenuTree(self):
        self.addButtonStatic("openVersion", icon='openVersion.png')
        p = cmds.popupMenu(b=1)
        stageDir = csc.getShotDirDict()['stage']
        seqNodes = cmds.ls('*Sequence_Node')
        seqNode = None
        cineSeqNode = None
        if seqNodes:
            seqNode = seqNodes[0]
            if seqNode:
                cineSeqNode = csn.CineSequenceNode.getCineSeqNode(seqNode)
                if cineSeqNode.isShot and cineSeqNode.shotNumber==0:
                    seqFileDir = os.path.join(csc.sequencesFolderPath, "{}\\{}".format(
                        cineSeqNode.seq.name, cineSeqNode.stageString))
        #print('from open version sub menu tree: {}, {}'.format(stageDir, seqNode))
        if cineSeqNode and stageDir:
            files = os.listdir(stageDir)
            versionLimit = 15
            versionDict = {}
            for f in files[-versionLimit:]:
                fileNoExt = os.path.splitext(f)[0]
                versionNumber = fileNoExt[-3:]
                if versionNumber.isdigit():
                    versionNumber = int(versionNumber)
                    versionDict[versionNumber]=os.path.join(stageDir, f)
                    openVersionCommand = partial(SCom.openFile, versionDict[versionNumber], True)
                    if versionNumber == cineSeqNode.version:
                        versionMenuItem = self.addMenuItemStatic(
                                                p, "v{}".format(versionNumber))
                    else:
                        versionMenuItem = self.addMenuItemStatic(
                                                p, "v{}".format(versionNumber), 
                                                command=openVersionCommand)
    
    def refreshOpenMenus(self):
        #print('refreshing the open menu trees')
        cineShelfArray = cmds.shelfLayout(shelfName, q=1, ca=1)
        self.deleteOpenMenus(cineShelfArray)
        self.openSubMenuTree()
        self.openVersionSubMenuTree()
               
    def deleteOpenMenus(self, cineShelfArray):
        for each in cineShelfArray:
            try:
                #print(cmds.shelfButton(each, q=True, label=True))
                refreshButtons = [openButtonName, openVersionButtonName]
                if(cmds.shelfButton(each, q=True, label=True) in refreshButtons):
                    #print('found open button: {}'.format(each))
                    cmds.deleteUI(each)                    
            except:
                pass
def createStartShelf():
    #print('building start shelf')
    startShelf = dbCineStartShelf(name=shelfName)

def createCineShelf():
    #print("building cine shelf")
    cineShelf = dbCinematicShelf(name=shelfName)
    #print('adding singleton instance to cine static class')
    csc.shelfInstance = cineShelf