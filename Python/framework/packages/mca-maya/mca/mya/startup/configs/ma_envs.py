#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that sets up the environment variables for MCA
"""

# mca python imports
import os

# software specific imports
import maya.cmds as cmds

# mca python imports
from mca import mya as mca_maya
from mca.common import log
from mca.mya.startup.configs import ma_consts

logger = log.MCA_LOGGER

MAYA_VERSION = cmds.about(version=True)


def create_maya_envs(skip_dialog=True):
	"""
	Sets up the Maya depot environment variables

	:param bool skip_dialog: If True, nothing will be written to the console.
	"""
	
	# Set base Maya paths env.
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-mya\\mca\\mya\\configs
	configs_folder = os.path.join(mca_maya.MAYA_PATH, 'configs')
	os.environ[ma_consts.CONFIGS_PATH] = configs_folder
	if not skip_dialog:
		logger.info(f'{ma_consts.CONFIGS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{configs_folder}')
	
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-mya\\mca\\mya\\tools
	tools_folder = os.path.join(mca_maya.MAYA_PATH, 'tools')
	os.environ[ma_consts.TOOLS_PATH] = tools_folder
	if not skip_dialog:
		logger.info(f'{ma_consts.TOOLS_PATH} environment variable -path to the configs folder- set to:'
					f'\n{tools_folder}')
		
	# ex: d:\\wkspaces\\DarkWinterArt\\DarkWinter\\framework\\packages\\mca-mya\\mca\\mya\\tools
	deps_folder = os.path.join(mca_maya.MAYA_PATH, 'startup', 'dependencies', MAYA_VERSION)
	if not os.path.exists(deps_folder):
		logger.warning(f'{deps_folder}\nPath does not exist')
	else:
		os.environ[ma_consts.DEPS_ROOT] = deps_folder
		if not skip_dialog:
			logger.info(f'{ma_consts.DEPS_ROOT} environment variable -path to the configs folder- set to:'
						f'\n{deps_folder}')
		
	# ex: d:\wkspaces\DarkWinterArt\DarkWinter\Python\framework\mca\mya\thirdpartytools\studiolibrary\src
	studiolibrary_folder = os.path.join(mca_maya.MAYA_PATH, 'thirdpartytools', 'studiolibrary', 'src')
	if not os.path.exists(studiolibrary_folder):
		logger.warning(f'{studiolibrary_folder}\nPath does not exist')
	else:
		os.environ[ma_consts.STUDIOLIBRARY] = studiolibrary_folder
		if not skip_dialog:
			logger.info(f'{ma_consts.STUDIOLIBRARY} environment variable -path to Studio Library folder- set to:'
							f'\n{studiolibrary_folder}')

	epic_pose_wrangler_folder = os.path.join(mca_maya.MAYA_PATH, 'thirdpartytools', 'PoseDriverConnect', 'PoseDriverConnect', 'python')
	if not os.path.exists(epic_pose_wrangler_folder):
		logger.warning(f'{epic_pose_wrangler_folder}\nPath does not exist')
	else:
		os.environ[ma_consts.POSE_WRANGLER] = epic_pose_wrangler_folder
		if not skip_dialog:
			logger.info(f'{ma_consts.POSE_WRANGLER} environment variable -path to Pose Wrangler folder- set to:'
						f'\n{epic_pose_wrangler_folder}')

	third_party_folder = os.path.join(mca_maya.MAYA_PATH, 'thirdpartytools')
	if not os.path.exists(third_party_folder):
		logger.warning(f'{third_party_folder}\nPath does not exist')
	else:
		os.environ[ma_consts.THRIDPARTY] = third_party_folder
		if not skip_dialog:
			logger.info(f'{ma_consts.THRIDPARTY} environment variable -path to Third party tools folder- set to:'
						f'\n{third_party_folder}')
