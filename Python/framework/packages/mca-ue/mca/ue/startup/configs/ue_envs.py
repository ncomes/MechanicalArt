#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca import ue
from mca.common import log
from mca.ue.startup.configs import ue_consts

logger = log.MCA_LOGGER


def create_unreal_envs(skip_dialog=True):
	"""
	Sets up the Unreal depot environment variables

	:param bool skip_dialog: If True, nothing will be written to the console.
	"""
	
	# Set base unreal paths env.
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\mca\\ue\\configs
	configs_folder = os.path.join(ue.UNREAL_PATH, 'configs')
	os.environ[ue_consts.CONFIGS_PATH] = configs_folder
	if not skip_dialog:
		logger.info(f'{ue_consts.CONFIGS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{configs_folder}')
	
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\mca\\ue\\tools
	tools_folder = os.path.join(ue.UNREAL_PATH, 'tools')
	os.environ[ue_consts.TOOLS_PATH] = tools_folder
	if not skip_dialog:
		logger.info(f'{ue_consts.TOOLS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{tools_folder}')
		
