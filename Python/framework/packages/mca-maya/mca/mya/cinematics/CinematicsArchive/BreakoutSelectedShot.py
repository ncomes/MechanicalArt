#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
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

logger = log.MCA_LOGGER


@decorators.track_fnc
def breakOutSelectedShot(*args):
    if cmds.ls('*Sequence_Node'):
        mayaNode = cmds.ls('*Sequence_Node')[0]
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode)
        if cineSeqNode.isShot:
            selectedShots = [s for s in cmds.ls(sl=True) if cmds.objectType(s)=='shot']
            if selectedShots:
                sht = selectedShots[0]
                if cineSeqNode.stageNumber!=2:
                    cineShot = cc.CineShot.getCineShotFromMayaShot(sht, cineSeqNode)
                    bp.breakOut(cineShot, cineSeqNode, mayaNode)
                    logger.warning("{} broken out successfully".format(cineShot.name))
                else:
                    logger.warning("Cannot break out a shot from an animation file")
            else:
                logger.warning("No shots selected")
        else:
            logger.warning("This is a Scene File not a Shot File")
    else:
        logger.warning("No Sequence Node in Scene, Create a Sequence Node to make shots to Break Out Shots")