#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
import subprocess
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn


"""
def runTestBatch():
    print('running batch test')
    print(cc.CineStaticClass.scriptsPath)
    print(cc.CineStaticClass.mayaPyPath)
    scriptPath = "{}\\{}".format(cc.CineStaticClass.scriptsPath, 'BreakoutStandalone.py')
    command = r'{} {}'.format(cc.CineStaticClass.mayaPyPath, scriptPath)

    mya = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = mya.communicate()
    exitcode = mya.returncode
    if str(exitcode) != '0':
        print(err)
        print('error running batch test')
    else:
        print('batch test successful')
"""


def executeBatchBreakout():
    mayaSeqNodes = cmds.ls('*Sequence_Node')
    if mayaSeqNodes:
        mayaNode = mayaSeqNodes[0]
        fileName = r'{}'.format(cmds.file(q=1, sn=1))
        print(fileName)
        scriptPath = "{}\\{}".format(cc.CineStaticClass.scriptsPath, 'BreakoutStandalone.py')
        seqsDir = cc.CineStaticClass.sequencesFolderPath
        command = [cc.CineStaticClass.mayaPyPath, scriptPath, fileName, mayaNode, seqsDir]
        ###
        maya = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = maya.communicate()
        exitcode = maya.returncode
        if str(exitcode) != '0':
            print(err)
            print('error running batch breakout')
        else:
            print('batch breakout successful')
            cc.CineStaticClass.shelfInstance.refreshOpenMenus()
        ###
    else:
        nodeUI = csn.MayaSequenceNodeUI()
        nodeUI.mayaCineStartUI(nodeUI)    


@decorators.track_fnc
def promptBreakoutWindow(*args):
    result = cmds.confirmDialog( title='Batch Break Out Shots', 
        message='WARNING:\n\nThis process will lock your Maya until it is finished.'+
                '\nBreak out Camera Sequencer Shots into individual'+
                '\nLayout files?',
        button=['Yes','No'], 
        messageAlign = 'center',
        defaultButton='Yes', 
        cancelButton='No', 
        dismissString='No' )
    if result == 'Yes':
        #print 'clicked yes'
        executeBatchBreakout()