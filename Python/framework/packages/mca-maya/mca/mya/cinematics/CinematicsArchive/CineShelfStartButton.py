#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates and includes a shelf with buttons in mya for Cinematics
"""

# mca python imports
import sys
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators


print("Hold on to your...")


@decorators.track_fnc
def startButtonCommand(*args):
    path = getProjectPath()
    #print(path)
    customPyDir = r'{}{}'.format(path,'\\Python\\framework\\mca\\mya\\cinematics')
    sys.path.append(customPyDir)
    setCinematicProjectPaths(path)
    import mca.mya.cinematics.CinematicShelf as cShelf
    cShelf.createCineShelf()


def getProjectPath(*args):    
    #Studio Specific import of tools to get the project
    from mca.common.paths import project_paths
    path = project_paths.MCA_PROJECT_ROOT
    ####

    return path


def setCinematicProjectPaths(path):
    from mca.mya.cinematics.CineClasses import CineStaticClass as csc
    csc.projectPath = path
    csc.customPyDir = r'{}{}'.format(csc.projectPath,'\\Python\\framework\\mca\\mya\\cinematics')
    csc.iconPath = r'{}{}'.format(csc.projectPath,'\\Python\\framework\\mca\\mya\\cinematics\\icons\\')
    csc.sequencesFolderPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Sequences')
    csc.cameraPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Assets\\camera\\shotCam_2point35_30fps_v1.ma')
    csc.scriptsPath = r'{}{}'.format(csc.projectPath,'\\Python\\framework\\mca\\mya\\cinematics')


@decorators.track_fnc
def makeCustomShelf():
    shelfName = "Cinematics"
    labelBackground = (0, 0, 0, 0)
    labelColour = (.9, .9, .9)
    cleanOldShelf(shelfName)
    cmds.setParent(shelfName)
    cmds.shelfButton(width=37, height=37, image='pythonFamily.png', l="Start", imageOverlayLabel="Start",
                    command="startButtonCommand()", parent=shelfName, olb=labelBackground,
                    olc=labelColour, style='textOnly', vis=True, ebg=True)


def cleanOldShelf(name):
    '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
    if cmds.shelfLayout(name, ex=1):
        if cmds.shelfLayout(name, q=1, ca=1):
            for each in cmds.shelfLayout(name, q=1, ca=1):
                cmds.deleteUI(each)
    else:
        s = cmds.shelfLayout(name, p="ShelfLayout")


print("...butts")
