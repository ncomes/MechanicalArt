#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Asset manager UI
"""

# mca python imports
from mca.common.tools.assetregister import asset_register_tool
from mca.common import log
from mca.mya.pyqt.utils import ma_main_window

MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()

logger = log.MCA_LOGGER


class MayaAssetRegister(asset_register_tool.AssetRegister):

	def __init__(self, parent=MAYA_MAIN_WINDOW):
		super().__init__(parent=parent)
