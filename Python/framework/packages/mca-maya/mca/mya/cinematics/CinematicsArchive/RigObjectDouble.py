#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates and includes a shelf with buttons in mya for Cinematics
"""

# mca python imports
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.RigObject as ro



def rigObjectDouble():
    bones = ro.rigObject()
    #print("double clicked button. here are the bones: {}".format(bones))
    rootCtrl = ro.addRigControllers(bones[0])
    ns = rootCtrl.rpartition(':')[0]
    cmds.parent(rootCtrl, '{}:prop_all'.format(ns))
    