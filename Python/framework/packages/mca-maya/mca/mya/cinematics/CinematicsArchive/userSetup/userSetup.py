#Author: Christian Sherden
#Creates and includes a shelf with buttons in mya for Cinematics

import sys
import maya
import maya.cmds as cmds

print("Hold on to your...")

def startButtonCommand(*args):
	path = getProjectPath()
	#print(path)
	customPyDir = r'{}{}'.format(path,'\\Cinematics\\Scripts')
	sys.path.append(customPyDir)
	setCinematicProjectPaths(path)
	import CinematicShelf as cShelf
	cShelf.createCineShelf()

def getProjectPath(*args):    
	#Studio Specific import of tools to get the project
	from mca.common import paths as path_utils
	path = path_utils.get_project_path()
	####
	#print(path)

	return path

def setCinematicProjectPaths(path):
	from CineClasses import CineStaticClass as csc
	csc.projectPath = path
	csc.customPyDir = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Scripts')
	csc.iconPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Scripts\\icons\\')
	csc.sequencesFolderPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Sequences')
	csc.cameraPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Assets\\camera\\shotCam_2point35_30fps_v1.ma')
	csc.scriptsPath = r'{}{}'.format(csc.projectPath,'\\Cinematics\\Scripts')

def makeCustomShelf():
	shelfName = "Cinematics"
	labelBackground = (0, 0, 0, 0)
	labelColour = (.9, .9, .9)
	cleanOldShelf(shelfName)
	cmds.setParent(shelfName)
	cmds.shelfButton(width=37, height=37, image='pythonFamily.png', l="Start", imageOverlayLabel="Start", 
					command="startButtonCommand()", parent=shelfName, olb=labelBackground, 
					olc=labelColour, style='textOnly', vis=True, ebg=True) 
	#print("making start shelf")

def cleanOldShelf(name):
	'''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
	if cmds.shelfLayout(name, ex=1):
		#print('found shelf: '+name)
		if cmds.shelfLayout(name, q=1, ca=1):
			for each in cmds.shelfLayout(name, q=1, ca=1):
				cmds.deleteUI(each)
	else:
		s = cmds.shelfLayout(name, p="ShelfLayout")
		#print(s)

maya.utils.executeDeferred(makeCustomShelf)

print("...butts")