#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
import os
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
from mca.mya.cinematics.CinematicsArchive.MayaSaveVersion import saveNewVersion
from mca.common.modifiers import decorators



def saveButtonPress(*args):
    #print("save button pressed")
    mayaNode = getMayaSeqNode()
    if mayaNode:
        #print('found mya node')
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode)
        if cmds.attributeQuery('notes', node=mayaNode, ex=True):
            #print('found notes')
            cineSeqNode.notes = cmds.getAttr("{}.notes".format(mayaNode))
        saveNewVersion(cineSeqNode, mayaNode)

def getMayaSeqNode():
    foundNode = None
    seqNodes = cmds.ls("*Sequence_Node")
    if seqNodes:
        seqNode = seqNodes[0]
        foundNode = seqNode
    else:
        #print("No Sequence Node Found in Scene")
        nodeUI = csn.MayaSequenceNodeUI()
        nodeUI.mayaCineStartUI(nodeUI)

    return foundNode

