#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI tool to export flags
"""

# python imports
import os
# software specific imports
import pymel.core as pm
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# mca python imports
from mca.common import log
from mca.common.paths import project_paths
from mca.common.utils import lists
from mca.mya.rigging.flags import serialize_flag

global LAST_SELECTED_FLAG_EXPORT_FOLDER

logger = log.MCA_LOGGER


def export_flag(flag_node=None, export_directory=None, export_color=True):

	global LAST_SELECTED_FLAG_EXPORT_FOLDER

	valid_nodes = list()
	nodes = lists.force_list(flag_node) or pm.ls(sl=True)
	valid_nodes = [found_node for found_node in nodes if found_node and pm.objExists(found_node)]
	if not valid_nodes:
		logger.warning('No flag node to export selected')
		return False

	selected_dir = export_directory if os.path.exists(export_directory) else None
	if not selected_dir:
		default_folder = project_paths.MCA_PROJECT_ROOT
		try:
			default_folder = LAST_SELECTED_FLAG_EXPORT_FOLDER
		except Exception:
			pass
		selected_dir = QFileDialog.getExistingDirectory(
			None, 'Select directory where you want to export flag', default_folder, QFileDialog.ShowDirsOnly)
	if not selected_dir:
		logger.info('Flag export operation aborted by user!')
		return False
	LAST_SELECTED_FLAG_EXPORT_FOLDER = selected_dir

	for node_to_export in valid_nodes:
		flag_name = node_to_export.nodeName(stripNamespace=True)
		result = serialize_flag.export_flag(node_to_export, selected_dir, export_color=export_color, flag_name=flag_name)
		if not result:
			logger.warning('Flag node "{}" was not exported!'.format(node_to_export))

	return True
