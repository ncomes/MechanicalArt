#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
UI to create or edit Sequence Nodes for Cinematics
"""


# python imports
import os
from PySide2.QtWidgets import QButtonGroup
from PySide2.QtGui import QIntValidator
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.utils import process
from mca.common.modifiers import decorators
from mca.common.tools.dcctracking import dcc_tracking
from mca.mya.pyqt import mayawindows
from mca.mya.cinematics import cine_sequence_nodes, cine_file_utils
from mca.mya.rigging.tek import cine_sequence_component
from mca.common.paths import paths
logger = log.MCA_LOGGER


class CineSequenceNodeEditor(mayawindows.MCAMayaWindow):
	VERSION = '1.1.0'

	def __init__(self):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'sequence_node_editor_ui.ui')
		super().__init__(title='Sequence Node Editor',
						 ui_path=ui_path,
						 version=CineSequenceNodeEditor.VERSION)
		self.seq_node = cine_sequence_component.find_cine_seq_component()

		process.cpu_threading(dcc_tracking.ddc_tool_entry(CineSequenceNodeEditor))
		self.ui.stage_comboBox.addItems(['layout', 'animation'])

		if self.seq_node:
			seq_node_stage = self.seq_node.stage()
			seq_name = self.seq_node.seq_name()
			scene_name = self.seq_node.scene_name()
			seq_node_num = 1 if str(seq_node_stage) == 'animation' else 0

			self.ui.stage_comboBox.setCurrentIndex(seq_node_num)
			self.ui.sequence_code_lineEdit.setText(seq_name)
			self.ui.scene_name_lineEdit.setText(scene_name)


		self.ui.save_pushButton.clicked.connect(self._on_save_button_clicked)
		self.ui.cancel_pushButton.clicked.connect(self._on_cancel_button_clicked)


	@decorators.track_fnc
	def _on_save_button_clicked(self):
		stage = self.ui.stage_comboBox.currentText().lower()
		seq_code = self.ui.sequence_code_lineEdit.text()

		scene_name = self.ui.scene_name_lineEdit.text()
		if not any([stage, seq_code]):
			logger.warning('Please fill out all fields.')
			return

		if self.seq_node:
			version_number = int(self.seq_node.version_num()) + 1
			self.seq_node.pynode.versionNumber.set(str(version_number))
			self.seq_node.pynode.sequenceName.set(seq_code)
			self.seq_node.pynode.stage.set(stage)
		else:
			version_number = 1
			seq_node_data = cine_sequence_nodes.CineSequenceData.create(seq_code,
																		version_number,
																		stage,
																		scene_name=scene_name)
			seq_node_data.fill_cine_shot_data()
			self.seq_node = cine_sequence_component.CineSequenceComponent.create(seq_node_data.data)
		seq_dir = os.path.join(paths.get_cine_seq_path(), seq_code)
		if not os.path.exists(seq_dir):
			cine_file_utils.make_initial_folder_structure(seq_dir)

		try:
			cine_file_utils.save_new_version(seq_code, stage)

		except Exception as e:
			logger.warning(e)
		self.destroy()

	def _on_cancel_button_clicked(self):
		self.destroy()
