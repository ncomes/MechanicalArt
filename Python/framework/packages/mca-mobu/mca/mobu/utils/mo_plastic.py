#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os
# software specific imports
# mca python imports
from mca.common.modifiers import decorators
from mca.mobu.utils import scene
from mca.common.utils import fileio
from mca.common import log

logger = log.MCA_LOGGER


@decorators.track_fnc
def checkout_scene():
	"""
	Checks out a scene in Motion Builder.
	"""

	sn = scene.get_scene_name_and_path()
	fileio.touch_and_checkout(sn)
	