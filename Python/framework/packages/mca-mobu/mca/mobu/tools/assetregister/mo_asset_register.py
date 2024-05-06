#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asset manager UI
"""

# mca python imports
from mca.mobu.pyqt.utils import mo_main_windows
from mca.common.tools.assetregister import asset_register_tool
from mca.common import log

MOBU_MAIN_WINDOW = mo_main_windows.get_mobu_window()
logger = log.MCA_LOGGER


class MobuAssetRegister(asset_register_tool.AssetRegister):

	def __init__(self, parent=MOBU_MAIN_WINDOW):
		super().__init__(parent=parent)
