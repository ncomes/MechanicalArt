#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Auto skinner tool to apply an initial skinning pass on new characters of a pre-existing archetype.
"""

# python imports
import os
import time

# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.mya.utils import optionvars
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import skin_utils

logger = log.MCA_LOGGER


class MCAAutoSkinnerOptionVars(optionvars.MCAOptionVars):
	"""
	Option vars for the Face Staging UI
	"""

	# strings
	MCAAutoSkinnerArchetype = {'default_value': 'player_male', 'docstring': 'Archetype selection'}

	@property
	def archetype_selection(self):
		"""
		Returns archetype selection
		"""

		return self.MCAAutoSkinnerArchetype

	@archetype_selection.setter
	def archetype_selection(self, value):
		"""
		Sets archetype selection
		"""

		self.MCAAutoSkinnerArchetype = value


class AutoSkinner(mayawindows.MCAMayaWindow):
	VERSION = '1.0.0'

	def __init__(self):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'autoskinner_ui.ui')
		super().__init__(title='Auto Skinner',
						 ui_path=ui_path,
						 version=AutoSkinner.VERSION)
		self.optionvars = MCAAutoSkinnerOptionVars()

		# Will want to pull this info from asset list in the future
		archetypes = ['player_male', 'lumpy', 'possessed_striker', 'chaoscaster', 'nightstalker', 'hornedcharger',
		              'spinyfiend', 'lotusflowerleaper']

		self.ui.skin_pushButton.clicked.connect(self._on_skin_button_clicked)
		self.ui.archetype_comboBox.addItems(archetypes)
		self.ui.archetype_comboBox.currentTextChanged.connect(self._on_archetype_selection_changed)
		self.ui.archetype_comboBox.setCurrentText(self.optionvars.archetype_selection)

	def _on_archetype_selection_changed(self):
		"""
		Sets archetype comboBox
		"""

		self.optionvars.archetype_selection = self.ui.archetype_comboBox.currentText()

	def _on_skin_button_clicked(self):
		"""
		Skins selected mesh(es)
		"""

		if not pm.selected():
			logger.warning('Please select meshes to skin')
			return
		s = time.time()
		selected_type = self.ui.archetype_comboBox.currentText()
		if selected_type:
			for x in pm.selected():
				skin_utils.auto_skin(selected_type, x)
		else:
			logger.warning('Please select an archetype')
			return
		e = time.time()
		if e-s < 60:
			logger.info(f'Skinning completed in {round(e - s)} seconds')
		else:
			logger.info(f'Skinning completed in {round((e - s) / 60)} minutes')