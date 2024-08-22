#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI for opening, exporting, saving, adding, and editing cinematic sequences and shots.
"""

# System global imports
import os
# software specific imports
# Qt imports
from mca.common.pyqt.pygui import qtcore
# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
from mca.common.resources import resources
from mca.common.pyqt.qt_utils import listwidget_utils
from mca.mya.pyqt import mayawindows
from mca.mya.utils import optionvars
from mca.mya.cinematics import cine_file_utils, shot_utils, cine_sequence_nodes
from mca.mya.tools.sequencenodeeditor import sequence_node_editor_tool
from mca.common.pyqt import messages
from mca.common.project import paths
#from mca.mya.rigging.frag import cine_sequence_component

logger = log.MCA_LOGGER


class MCAOpenCineShotOptionVars(optionvars.MCAOptionVars):
	"""
	Option vars for the Open Cine Shot UI.
	"""

	MCASelectedStage = {'default_value': 0, 'docstring': 'Selected stage.'}


class CineOpenShotWindow(mayawindows.MCAMayaWindow):
	VERSION = '1.0.0'

	def __init__(self):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'Open_Cine_Shot_GUI.ui')
		super().__init__(title='Open Cinematic File',
						 ui_path=ui_path,
						 version=CineOpenShotWindow.VERSION)
		sequence_path = paths.get_cine_seq_path()
		if os.path.exists(sequence_path):
			self.sequences = [x for x in os.listdir(sequence_path) if len(x) == 3]
			self.ui.sequence_listWidget.addItems(self.sequences)

		else:
			self.sequences = None
		self.optionvars = MCAOpenCineShotOptionVars()
		self.file_dir = 'None'
		self.shot_dir = 'None'
		self.version_dir = 'None'
		self.seq_data_dir = None

		#########################################
		# Signals
		#########################################
		self.ui.stage_comboBox.addItems(['Animation', 'Layout'])
		self.ui.stage_comboBox.setCurrentIndex(self.optionvars.MCASelectedStage)
		self.ui.stage_comboBox.currentTextChanged.connect(self._set_stage_selection)
		self.ui.sequence_listWidget.itemSelectionChanged.connect(self._on_sequence_selected)
		self.ui.shot_listWidget.itemSelectionChanged.connect(self._on_shot_selected)
		self.ui.stage_comboBox.currentTextChanged.connect(self._on_refresh_button_press)

		self.ui.open_file_pushButton.clicked.connect(self._on_open_button_press)
		self.ui.refresh_button.clicked.connect(self._on_refresh_button_press)
		self.ui.save_new_version_pushButton.clicked.connect(self._on_save_new_version_button_clicked)
		self.ui.rename_shot_pushButton.clicked.connect(self._on_rename_shot_button_clicked)
		self.ui.rename_sequence_pushButton.clicked.connect(self._on_rename_sequence_button_clicked)
		self.ui.rename_file_pushButton.clicked.connect(self._on_rename_file_button_clicked)
		self.ui.make_new_sequence_pushButton.clicked.connect(self._on_make_new_sequence_button_clicked)
		self.ui.export_file_pushButton.clicked.connect(self._on_export_file_button_clicked)
		self.ui.export_sequence_pushButton.clicked.connect(self._on_export_sequence_button_clicked)
		self.ui.playblast_sequence_pushButton.clicked.connect(self._on_playblast_sequence_button_clicked)

		add_file_icon = resources.icon(r'white\add_file.png')
		self.ui.make_new_sequence_pushButton.setIcon(add_file_icon)

		rename_icon = resources.icon(r'white\rename.png')
		self.ui.rename_shot_pushButton.setIcon(rename_icon)
		self.ui.rename_sequence_pushButton.setIcon(rename_icon)
		rnm_file_button = self.ui.rename_file_pushButton
		rnm_file_button.setIcon(rename_icon)
		rnm_file_button.setIconSize(qtcore.QSize(rnm_file_button.width() - 10, rnm_file_button.height() - 10))

		clapperboard_icon = resources.icon(r'white\clapperboard.png')
		self.ui.playblast_sequence_pushButton.setIcon(clapperboard_icon)

		export_icon = resources.icon(r'white\export.png')
		self.ui.export_sequence_pushButton.setIcon(export_icon)
		expt_file_button = self.ui.export_file_pushButton
		expt_file_button.setIcon(export_icon)
		expt_file_button.setIconSize(qtcore.QSize(expt_file_button.width() - 10, expt_file_button.height() - 10))

		open_file_icon = resources.icon(r'white\open.png')
		open_file_button = self.ui.open_file_pushButton
		open_file_button.setIcon(open_file_icon)
		open_file_button.setIconSize(qtcore.QSize(open_file_button.width() - 10, open_file_button.height() - 10))

		save_file_icon = resources.icon(r'white\save.png')
		save_file_button = self.ui.save_new_version_pushButton
		save_file_button.setIcon(save_file_icon)
		save_file_button.setIconSize(qtcore.QSize(save_file_button.width() - 10, save_file_button.height() - 10))

	####################################
	# Slots
	####################################
	def _set_stage_selection(self):
		"""
		Set the optionvar combobox value for stage selection.
		"""

		self.optionvars.MCASelectedStage = self.ui.stage_comboBox.currentIndex()

	
	def _on_playblast_sequence_button_clicked(self):
		"""
		Playblasts latests versions of selected shots in selected sequence

		"""

		selected_sequence = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
		if selected_sequence:
			selected_sequence = selected_sequence[0]
			selected_shots = listwidget_utils.get_qlist_widget_selected_items(self.ui.shot_listWidget)
			stage = self.ui.stage_comboBox.currentText().lower()
			message_result = messages.question_message('Playblast Sequence', 'This will open a new scene, continue?')
			if not message_result == 'Yes':
				return
			if not selected_shots:
				sequence_dir = os.path.join(paths.get_cine_seq_path(), selected_sequence)
				all_shots_dir = os.path.join(sequence_dir, 'shots')
				selected_shots = [x for x in os.listdir(all_shots_dir) if x.isdigit()]
			if selected_shots:
				shot_utils.batch_playblast(selected_sequence, selected_shots, stage)

	
	def _on_export_file_button_clicked(self):
		"""
		Exports selected shot file

		"""

		selected_shot_file = listwidget_utils.get_qlist_widget_selected_items(self.ui.file_listWidget)
		if selected_shot_file:
			selected_shot_file = selected_shot_file[0]
			file_path = os.path.join(self.version_dir, selected_shot_file)
			if os.path.exists(file_path):
				seq_name = selected_shot_file[:3]
				shot_number = os.path.basename(self.shot_dir)
				message_result = messages.question_message('Export Shot', 'This will open a new scene, continue?')
				if not message_result == 'Yes':
					return
				throw_warning = False
				try:
					cine_file_utils.open_maya_file(file_path)
				except Exception as e:
					logger.warning(e)
					throw_warning = True
				cine_file_utils.export_cine_shot(seq_name, shot_number)
				if not throw_warning:
					messages.info_message('Export Shot', f'{selected_shot_file} exported.')
				else:
					messages.info_message('Export Shot', f'Error encountered when opening {selected_shot_file}\n'
														 f'Please ensure file exported correctly.')

	
	def _on_export_sequence_button_clicked(self):
		"""
		Exports the latest versions of selected shots in selected sequence

		"""

		stage = self.ui.stage_comboBox.currentText().lower()
		selected_sequence = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
		if selected_sequence:
			selected_sequence = selected_sequence[0]
			selected_shots = listwidget_utils.get_qlist_widget_selected_items(self.ui.shot_listWidget)
			if not selected_shots:
				widget_items = listwidget_utils.get_qlist_widget_items(self.ui.shot_listWidget)
				selected_shots = [x for x in widget_items if x.isdigit()]
			if not selected_shots:
				messages.info_message('Export Sequence', 'No shots found in the selected sequence.')
				return
			message_result = messages.question_message('Export Sequence', 'This will open a new scene, continue?')
			if not message_result == 'Yes':
				return
			cine_file_utils.export_sequence(selected_sequence, selected_shots, stage)
			exported_shots_sorted = list(sorted(selected_shots))
			exported_shots = ',\n'.join(exported_shots_sorted)
			messages.info_message('Export Sequence', f'Shots exported from {selected_sequence}:\n{exported_shots}.')

	
	def _on_make_new_sequence_button_clicked(self):
		"""
		Opens sequence node editor

		"""

		sequence_node_editor_tool.CineSequenceNodeEditor()

	
	def _on_rename_shot_button_clicked(self):
		"""
		Renames files in selected shot directory

		"""

		new_shot_num = messages.text_prompt_message('Rename Shot', 'Please enter a new number for the shot.')
		if new_shot_num and new_shot_num != '':
			if not new_shot_num.isnumeric():
				logger.warning('New shot number must be an integer.')
				return
			selected_shot = listwidget_utils.get_qlist_widget_selected_items(self.ui.shot_listWidget)
			if selected_shot:
				selected_shot = selected_shot[0]
				cine_file_utils.rename_shot_files(selected_shot, new_shot_num, os.path.normpath(self.shot_dir))

	
	def _on_rename_sequence_button_clicked(self):
		"""
		Renames files in selected sequence directory

		"""

		new_name = messages.text_prompt_message('Rename Sequence', 'Please enter a new name for the sequence.')
		if new_name and new_name != '':
			selected_sequence = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
			if selected_sequence:
				old_name = selected_sequence[0]
				cine_file_utils.rename_sequence_files(old_name, new_name)

	
	def _on_rename_file_button_clicked(self):
		"""
		Renames selected file

		"""

		new_name = messages.text_prompt_message('Rename File', 'Please enter a new name for the file.')
		if new_name and new_name != '':
			selected_file = listwidget_utils.get_qlist_widget_selected_items(self.ui.file_listWidget)
			if selected_file:
				cine_file_utils.rename_file(self.version_dir, selected_file[0], new_name)

	
	def _on_save_new_version_button_clicked(self):
		"""
		Saves new version of current file

		"""

		cine_seq_node = None #cine_sequence_component.find_cine_seq_component()
		if cine_seq_node:
			cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
			cine_seq_data.fill_cine_shot_data()

		if os.path.basename(self.shot_dir).isdigit():
			shot_number = os.path.basename(self.shot_dir)
		else:
			shot_number = None

		stage = self.ui.stage_comboBox.currentText().lower()
		seq_name = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
		if seq_name:
			seq_name = seq_name[0]
		else:
			logger.warning('Please select a sequence.')
			return
		cine_file_utils.save_new_version(seq_name, stage, shot_number=shot_number)

	def _on_sequence_selected(self):
		"""
		Updates data and sets listwidget items

		"""
		anim_stage = True if self.ui.stage_comboBox.currentText() == 'Animation' else False
		selected_items = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
		if selected_items:
			selected_sequence = selected_items[0]

			self.ui.file_listWidget.clear()
			self.ui.shot_listWidget.clear()
			if anim_stage:
				file_list = [x for x in self._get_file_list(selected_sequence) if x.isdigit()]
			else:
				file_list = self._get_file_list(selected_sequence)
			self.ui.shot_listWidget.addItems(file_list)
			self.seq_data_dir = os.path.join(self.sequence_dir, f'{selected_sequence}_sequence_data.json')

	def _on_shot_selected(self):
		"""
		Updates data and sets listwidget items

		"""

		layout = False
		selected_stage = self.ui.stage_comboBox.currentText().lower()
		selected_shot = listwidget_utils.get_qlist_widget_selected_items(self.ui.shot_listWidget)
		if selected_shot:
			selected_file = selected_shot[0]
			self.ui.file_listWidget.clear()
			# If the selected "shot" (which is a directory) is actually one of the layout sequence folders,
			# make sure stage combobox is set accordingly.
			if selected_file == 'previs' or selected_file == 'layout':
				layout = True
			self._get_stage_list(selected_file)

		if selected_stage:
			file_list = self._get_version_list(selected_stage, layout=layout)
			self.ui.file_listWidget.clear()
			if file_list:
				self.ui.file_listWidget.addItems(file_list)

	
	def _on_open_button_press(self):
		"""
		Opens a selected file

		"""

		selected_items = listwidget_utils.get_qlist_widget_selected_items(self.ui.file_listWidget)
		if selected_items:
			selected_shot_file = selected_items[0]
			file_path = os.path.join(self.version_dir, selected_shot_file)
			if os.path.exists(file_path):
				cine_file_utils.open_maya_file(file_path)
			else:
				logger.warning('No File Exists At Path To Open. Path: ' + file_path)

	def _on_refresh_button_press(self):
		"""
		Refreshes listwidget items

		"""

		sel_seq, sel_shot, sel_file = self._get_selection_list()
		seq_items = [self.ui.sequence_listWidget.item(x) for x in range(self.ui.sequence_listWidget.count())]
		seq_item = [x for x in seq_items if x.text() == sel_seq]
		if seq_item:
			self.ui.sequence_listWidget.setCurrentItem(seq_item[0])
		shot_items = [self.ui.shot_listWidget.item(x) for x in range(self.ui.shot_listWidget.count())]
		shot_item = [x for x in shot_items if x.text() == sel_shot]
		if shot_item:
			self.ui.shot_listWidget.setCurrentItem(shot_item[0])

	def _get_file_list(self, selected_sequence):
		"""
		Returns a list of files to display

		:param str selected_sequence: Three letter sequence name
		:return: Returns a list of files to display
		:rtype: list(str)

		"""

		file_dict = cine_file_utils.get_seq_file_list(selected_sequence)
		files = file_dict.get('files')
		self.sequence_dir = os.path.join(paths.get_cine_seq_path(), selected_sequence)
		self.file_dir = file_dict.get('file_dir')
		layout_dirs = list(set(file_dict.get('layout_dirs')))

		return files + [os.path.basename(x) for x in layout_dirs]

	def _get_stage_list(self, selected_file):
		"""
		Returns a list of stages for selected file to display

		:param str selected_file: Shot directory
		:return: Returns stage list
		:rtype: list(str)

		"""

		stage_list = []
		if not selected_file.isdigit():
			self.shot_dir = os.path.join(self.sequence_dir, selected_file)
		else:
			stages = ['previs', 'layout', 'animation']
			for stage in stages:
				self.shot_dir = os.path.join(self.file_dir, selected_file)
				stage_dir = os.path.join(self.shot_dir, stage)
				if os.path.exists(stage_dir):
					stage_list.append(stage)
		return stage_list

	def _get_version_list(self, selected_stage, layout=False):
		"""
		Gets list of files to display for a version

		:param selected_stage: Layout or animation
		:param layout: If this is a layout sequence, not a shot
		:return: Returns a list of files to display
		:rtype: list(str)

		"""

		if layout:
			version_dir = self.shot_dir
		else:
			version_dir = os.path.normpath(os.path.join(self.shot_dir, selected_stage))
		self.version_dir = version_dir
		if os.path.exists(version_dir):
			versions = [x for x in os.listdir(version_dir) if '.ma' in x or '.mb' in x]
			versions.reverse()
			return versions
		else:
			return []

	def _refresh_lists(self):
		"""
		Resets lists


		"""

		self.ui.sequence_listWidget.clear()
		self.ui.file_listWidget.clear()
		self.ui.shot_listWidget.clear()
		self.sequences = [x for x in os.listdir(paths.get_cine_seq_path()) if len(x) == 3]
		self.ui.sequence_listWidget.addItems(self.sequences)

	def _get_selection_list(self):
		"""
		Gets currently selected items in listWidgets

		:return: Returns selected items
		:rtype: list(str)

		"""
		seq_sel = listwidget_utils.get_qlist_widget_selected_items(self.ui.sequence_listWidget)
		seq = None if not seq_sel else seq_sel[0]
		shot_sel = listwidget_utils.get_qlist_widget_selected_items(self.ui.shot_listWidget)
		shot = None if not shot_sel else shot_sel[0]
		file_sel = listwidget_utils.get_qlist_widget_selected_items(self.ui.file_listWidget)
		file = None if not file_sel else file_sel[0]
		self._refresh_lists()
		return seq, shot, file

