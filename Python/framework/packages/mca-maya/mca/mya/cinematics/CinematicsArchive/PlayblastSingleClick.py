#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a parent constraint
"""

# mca python imports
# PySide2 imports
# software specific imports
import mca.mya.cinematics.CinematicsArchive.Playblast as pb
from mca.common.modifiers import decorators


@decorators.track_fnc
def playblastSingle():
    resoH = 720
    resoW = 1720
    pb.playblast(resoH, resoW)