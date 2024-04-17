#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.BreakoutProcess as bp
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
from mca.mya.pyqt import dialogs


logger = log.MCA_LOGGER


@decorators.track_fnc
def layoutToAnim(*args):
    if cmds.ls('*Sequence_Node'):
        mayaNode = cmds.ls('*Sequence_Node')[0]
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode)
        if cineSeqNode.stageNumber==2:
            print("This file is already an animation file")
        elif cineSeqNode.isShot and cineSeqNode.shotNumber==0:
            print("Cannot send sequence file to Animation")
        else:
            #if there is a shot in the scene, set the playback time to the shot
            if cmds.ls(type='shot'):
                sht = cmds.ls(type='shot')[0]
                cmds.playbackOptions(minTime=cmds.shot(sht, q=True, st=True))
                cmds.playbackOptions(maxTime=cmds.shot(sht, q=True, et=True))
            #
            if cineSeqNode.isShot:
                cineShot = cc.CineShot.getCineShotFromSeqNode(cineSeqNode)
                bp.breakOut(cineShot, cineSeqNode, mayaNode, cleanAnim=True)
            else:
                cineScene = cc.CineScene.getCineSceneFromSeqNode(cineSeqNode)
                bp.breakOut(cineScene, cineSeqNode, mayaNode, cleanAnim=True)
    else:
        logger.warning("No Sequence Node in Scene, Create a Sequence Node to Break Out Shots")
        dialogs.info_prompt('No Sequence', 'No Sequence Node in Scene, Create a Sequence Node to Break Out Shots')

