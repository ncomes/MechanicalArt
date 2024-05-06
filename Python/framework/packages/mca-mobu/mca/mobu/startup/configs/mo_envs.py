#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca import mobu
from mca.common import log
from mca.mobu.startup.configs import mo_consts


logger = log.MCA_LOGGER


def create_mobu_envs(skip_dialog=True):
	"""
	Sets up the Mobu depot environment variables

	:param bool skip_dialog: If True, nothing will be written to the console.
	"""
	
	# Set base Mobu paths env.
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-monu\\mca\\mobu\\configs
	configs_folder = os.path.join(mobu.MOBU_PATH, 'configs')
	os.environ[mo_consts.CONFIGS_PATH] = configs_folder
	if not skip_dialog:
		logger.info(f'{mo_consts.CONFIGS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{configs_folder}')
	
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-monu\\mca\\mobu\\tools
	tools_folder = os.path.join(mobu.MOBU_PATH, 'tools')
	os.environ[mo_consts.TOOLS_PATH] = tools_folder
	if not skip_dialog:
		logger.info(f'{mo_consts.TOOLS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{tools_folder}')
		
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-mya\\mca\\mya\\tools
	deps_folder = os.path.join(mobu.MOBU_PATH, 'configs', 'dependencies', '2022')
	if not os.path.exists(deps_folder):
		return
	os.environ[mo_consts.DEPS_ROOT] = deps_folder
	if not skip_dialog:
		logger.info(f'{mo_consts.DEPS_ROOT} environment variable -path to the configs folder- set to:'
						f'\n{deps_folder}')