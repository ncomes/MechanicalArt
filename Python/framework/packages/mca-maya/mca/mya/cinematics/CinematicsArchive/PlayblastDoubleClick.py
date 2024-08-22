#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
# PySide2 imports
# software specific imports
# mca python imports
import mca.mya.cinematics.CinematicsArchive.Playblast as pb
from mca.common.modifiers import decorators



def playblastDouble():
    resoH = 720
    resoW = 1720
    pb.playblast(resoH, resoW)