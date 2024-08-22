"""
Tool for working with cinematic shots and sequences
"""

# python imports
import os
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui
# software specific imports
import pymel.core as pm
import maya.cmds as cmds

# mca python imports
from mca.common import log
from mca.common.pyqt import common_windows, messages
from mca.common.resources import resources
from mca.common.utils import fileio

from mca.mya.animation import camera_utils, time_utils
from mca.mya.cinematics import cine_sequence_nodes, shot_utils, cine_file_utils
from mca.mya.rigging.frag import cine_sequence_component
from mca.mya.pyqt.utils import ma_main_window
from mca.mya.utils import namespace_utils

logger = log.MCA_LOGGER
MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()

class CineShotEditor(common_windows.MCADockableWindow):
	VERSION = '1.0.3'

	def __init__(self):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'cine_shot_editor_ui_main.ui')
		super().__init__(title='CineShotEditor',
						 ui_path=ui_path,
						 version=CineShotEditor.VERSION,
						 parent=MAYA_MAIN_WINDOW,
						 area=qtcore.Qt.RightDockWidgetArea)
		MAYA_MAIN_WINDOW.addDockWidget(qtcore.Qt.RightDockWidgetArea, self)
		self.vertical_spacer = None
		self.cine_seq_data = None
		self.container_layout = None
		self.shot_widgets_dict = {}
		self.initialize_shot_widgets()
		self.setup_signals()

	def initialize_shot_widgets(self):
		"""
		Initializes shot widgets within main layout.

		"""

		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		self.ui.stage_comboBox.clear()
		self.ui.stage_comboBox.addItems(['layout', 'animation'])
		self.ui.sequence_name_lineEdit.setText('')
		if cine_seq_node:
			seq_node_stage = cine_seq_node.stage()
			seq_name = cine_seq_node.seq_name()
			seq_node_num = 1 if str(seq_node_stage) == 'animation' else 0

			self.ui.stage_comboBox.setCurrentIndex(seq_node_num)
			self.ui.sequence_name_lineEdit.setText(seq_name)

		self.shot_widgets_dict = {}
		self.clear_layout(self.ui.main_verticalLayout)

		scroll_area = qtwidgets.QScrollArea()
		scroll_area.setObjectName('MainScrollFrame')
		scroll_area.setFrameStyle(qtwidgets.QFrame.WinPanel | qtwidgets.QFrame.Sunken)
		scroll_area.setContentsMargins(0, 0, 4, 0)
		scroll_area.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
		scroll_area.setVerticalScrollBarPolicy(qtcore.Qt.ScrollBarAsNeeded)
		scroll_area.setHorizontalScrollBarPolicy(qtcore.Qt.ScrollBarAlwaysOff)
		scroll_area.setWidgetResizable(True)
		scroll_area_widget_contents = qtwidgets.QWidget()
		scroll_area.setWidget(scroll_area_widget_contents)

		self.container_layout = qtwidgets.QVBoxLayout(scroll_area_widget_contents)

		if cine_seq_node:
			scene_shot_list = cine_seq_node.shots()
			self.cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
			shot_node_sorted = sorted(scene_shot_list, key=lambda x: int(x.shotName.get()[-3:]))
			for shot in shot_node_sorted:
				shot_data = cine_sequence_nodes.CineShotData.get_shot_data_from_node(shot, self.cine_seq_data)
				shot_widget = self.add_shot(self.container_layout, shot_data=shot_data)
				self.shot_widgets_dict[shot_widget] = shot_data

		self.vertical_spacer = qtwidgets.QSpacerItem(0, 2000, qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
		self.container_layout.addItem(self.vertical_spacer)
		self.ui.main_verticalLayout.addWidget(scroll_area)

	def setup_signals(self):
		"""
		Signal hookup.

		"""

		self.ui.refresh_shots_pushButton.pressed.connect(self.initialize_shot_widgets)
		self.ui.new_shot_pushButton.pressed.connect(self._new_shot_button_pressed)
		self.ui.ubercam_pushButton.pressed.connect(self._on_ubercam_button_pressed)
		self.ui.playblast_sequence_pushButton.pressed.connect(self._on_playblast_sequence_button_pressed)
		self.ui.break_out_selected_pushButton.pressed.connect(self._on_break_out_selected_button_pressed)
		self.ui.sequence_name_lineEdit.editingFinished.connect(self._on_sequence_name_edited)
		self.ui.stage_comboBox.currentTextChanged.connect(self._on_stage_changed)
		self.ui.remove_ubercam_pushButton.pressed.connect(self._on_remove_ubercam_button_pressed)
		self.ui.look_thru_ubercam_pushButton.pressed.connect(self._on_look_thru_button_pressed)
		self.ui.select_all_checkBox.stateChanged.connect(self._on_select_all_checkbox_changed)

	def _on_select_all_checkbox_changed(self):
		"""
		Selects all checkboxes when select all checkbox is changed.

		"""

		check_state = self.ui.select_all_checkBox.isChecked()
		for shot_widget in self.shot_widgets_dict.keys():
			shot_widget.ui.shot_select_checkBox.setChecked(check_state)

	def _on_stage_changed(self, stage):
		"""
		Sets the stage on sequence node and in data when changed by user in combobox.

		:param str stage: New stage selected by user.

		"""
		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		if self.cine_seq_data:
			self.cine_seq_data.stage = stage
		if cine_seq_node:
			cine_seq_node.pynode.stage.set(stage)
		if self.shot_widgets_dict:
			for shot_data in self.shot_widgets_dict.values():
				shot_data.stage = stage

	def _on_sequence_name_edited(self):
		"""
		Changes the sequence name and updates shots accordingly.

		"""

		if not self.ui.sequence_name_lineEdit.isModified():
			return

		text = self.ui.sequence_name_lineEdit.text()
		if not len(text) == 3:
			messages.info_message('Edit Sequence Name', 'Sequence name must be 3 characters long.')
			self.ui.sequence_name_lineEdit.setText(self.cine_seq_data.seq_name)
			return
		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		if not cine_seq_node:
			self.ui.sequence_name_lineEdit.setText(self.cine_seq_data.seq_name)
			messages.info_message('Change Sequence Name', 'CineSequenceComponent node not found.')
			return
		if not text.isupper():
			text = text.upper()
			self.ui.sequence_name_lineEdit.setText(text)
		question_result = messages.question_message('Edit Sequence Name', f'Change the sequence name to {text}?')
		if not question_result == 'Yes':
			self.ui.sequence_name_lineEdit.setText(self.cine_seq_data.seq_name)
			return

		if self.shot_widgets_dict:
			for shot_widget, shot_data in self.shot_widgets_dict.items():
				new_shot_name = shot_data.shot_name.replace(f'{shot_data.shot_name[:3]}_', f'{text}_')
				new_shot_data = shot_utils.rename_shot(shot_data, new_shot_name)
				self.shot_widgets_dict[shot_widget] = new_shot_data
		cine_seq_node.pynode.sequenceName.set(text)
		self.cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
		self.initialize_shot_widgets()

	def get_selected_shot_data(self):
		"""
		Returns data classes for selected shots.

		"""

		selected_shot_widgets = [x for x in self.shot_widgets_dict.keys() if x.ui.shot_select_checkBox.isChecked()]
		shot_data_list = []
		for shot_widget in selected_shot_widgets:
			shot_data = self.shot_widgets_dict.get(shot_widget)
			if shot_data:
				shot_data_list.append(shot_data)
		return shot_data_list


	def _on_playblast_sequence_button_pressed(self, skip_dialog=False):
		"""
		Playblasts selected shots.

		:param bool skip_dialog: If we want to skip the message dialog about playblasted shots.

		"""

		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		if not cine_seq_node:
			logger.warning('CineSequenceComponent node not found.')
			return
		shot_data_list = self.get_selected_shot_data()
		for shot_data in shot_data_list:
			if not pm.objExists(shot_data.shot_camera):
				logger.warning(f'Camera {shot_data.shot_camera} does not exist.')
				return
			shot_utils.create_cine_playblast(cine_seq_node.seq_name(),
											 shot_data.shot_name,
											 shot_data.stage,
											 [shot_data.shot_start, shot_data.shot_end],
											 pm.PyNode(shot_data.shot_camera))

		if not skip_dialog:
			if len(shot_data_list) > 1:
				broken_out_shots_sorted = list(sorted(shot_data_list, key=lambda x: x.shot_number))
				broken_out_shots = '\n'.join(list(map(lambda x: x.shot_name, broken_out_shots_sorted)))
			else:
				broken_out_shots = shot_data_list[0].shot_name
			messages.info_message('Playblast Selected Shots', f'Shots playblasted: \n{broken_out_shots}.')

	
	def _on_break_out_selected_button_pressed(self):
		"""
		Breaks out selected shots.

		"""

		shot_data_list = self.get_selected_shot_data()
		broken_out_shots = cine_file_utils.batch_breakout(shot_data_list)
		if broken_out_shots:
			if len(broken_out_shots) > 1:
				broken_out_shots_sorted = list(sorted(shot_data_list, key=lambda x: x.shot_number))
				broken_out_shots = '\n'.join(list(map(lambda x: x.shot_name, broken_out_shots_sorted)))
			messages.info_message('Break Out Selected Shots', f'Shots broken out:\n{broken_out_shots}')

	def clear_layout(self, layout):
		"""
		Removes all items from the given layout.
		:param qtwidgets.QVBoxLayout layout: Layout to clear.

		"""

		while layout.count():
			item = layout.takeAt(0)
			widget = item.widget()
			if widget is not None:
				widget.deleteLater()
			else:
				self.clear_layout(item.layout())

	
	def _on_ubercam_button_pressed(self):
		"""
		Creates ubercam.

		"""

		camera_utils.create_mca_ubercam_cmd()

	
	def _on_remove_ubercam_button_pressed(self):
		"""
		Removes ubercam.

		"""

		camera_utils.remove_ubercam_cmd()

	
	def _on_look_thru_button_pressed(self):
		"""
		Looks through ubercam in active viewport.

		"""

		ubercam = [x for x in pm.ls(type=pm.nt.Camera) if x.getTransform().hasAttr('MCAUberCam')]
		if ubercam:
			ubercam_xform = ubercam[0]
			if ubercam_xform:
				pm.lookThru(ubercam_xform)
		else:
			camera_utils.create_mca_ubercam_cmd()

	def _add_vertical_spacer(self):
		"""
		This removes and then adds the vertical spacer to the main layout.

		"""
		if self.vertical_spacer:
			self.container_layout.removeWidget(self.vertical_spacer.widget())
		new_vertical_spacer = qtwidgets.QSpacerItem(0, 2000, qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)
		self.container_layout.addItem(new_vertical_spacer)
		self.vertical_spacer = new_vertical_spacer

	
	def _new_shot_button_pressed(self):
		"""
		Adds a new shot to the sequence.

		"""

		shot_list = pm.ls(type=pm.nt.Shot)
		shot_utils.make_new_shot_cmd()
		new_shot_node = [x for x in pm.ls(type=pm.nt.Shot) if x not in shot_list][0]
		new_shot_data = cine_sequence_nodes.CineShotData.get_shot_data_from_node(new_shot_node, self.cine_seq_data)
		self.add_shot(self.container_layout, shot_data=new_shot_data)

		# refresh ubercam
		ubercam = [x for x in pm.ls(type=pm.nt.Camera) if x.getTransform().hasAttr('MCAUberCam')]
		if ubercam:
			camera_utils.create_mca_ubercam_cmd()

	def add_shot(self, layout, shot_data):
		"""
		Add a new shot widget to the given layout.

		:param qtwidgets.QVBoxLayout layout: Layout to add the new shot widget to.
		:param CineShotData shot_data: Data class for the new shot.
		:return: The widget that represents the new shot that was added.
		:rtype: CineShotWidget

		"""

		shot_frame = ShotFrameButton(parent=self.ui, parent_layout=layout, shot_data=shot_data, parent_class=self)
		sequence_widget = shot_frame.sequence_widget
		self.container_layout.addWidget(shot_frame)
		self.shot_widgets_dict[sequence_widget] = shot_data
		self._add_vertical_spacer()

		return sequence_widget


class ShotFrameButton(qtwidgets.QFrame):
	def __init__(self, parent=None, parent_layout=None, shot_data=None, parent_class=None):
		super().__init__(parent=parent)
		self.main_ui = parent
		self.parent_layout = parent_layout
		self.shot_camera_list = []
		for cam in pm.ls(type=pm.nt.Camera):
			if cine_file_utils.is_shot_cam(cam):
				self.shot_camera_list.append(cam.getTransform().name())
		self.shot_data = shot_data
		self.setContentsMargins(1, 0, 0, 1)
		self.setSizePolicy(qtwidgets.QSizePolicy.MinimumExpanding, qtwidgets.QSizePolicy.Fixed)
		self.setMinimumHeight(210)
		self.setMaximumHeight(210)
		self.setMinimumWidth(195)

		self.tool_v_layout = qtwidgets.QVBoxLayout(self)
		self.tool_v_layout.setContentsMargins(0, 0, 0, 0)

		self.tool_button = qtwidgets.QToolButton(self)
		self.tool_button.setSizePolicy(qtwidgets.QSizePolicy.MinimumExpanding, qtwidgets.QSizePolicy.Expanding)
		self.tool_button.setArrowType(qtcore.Qt.RightArrow)
		self.tool_button.setText(self.shot_data.shot_name)
		self.tool_button.setToolButtonStyle(qtcore.Qt.ToolButtonTextBesideIcon)
		self.tool_button.setContentsMargins(2, 0, 0, 1)
		self.tool_button.setMaximumHeight(25)
		self.tool_button.setMinimumHeight(25)
		self.tool_button.setMinimumWidth(180)
		self.tool_button.setParent(self)
		self.tool_v_layout.addWidget(self.tool_button)

		self.q_frame = qtwidgets.QFrame(self)
		self.q_frame.setContentsMargins(2, 0, 1, 0)
		self.q_frame.setMinimumHeight(25)
		self.tool_v_layout.addWidget(self.q_frame)
		self.q_frame.setVisible(0)
		self.q_frame.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Fixed)

		self.sequence_layout = qtwidgets.QVBoxLayout(self.q_frame)
		self.q_frame.setSizePolicy(qtwidgets.QSizePolicy.Expanding, qtwidgets.QSizePolicy.Expanding)

		self.sequence_widget = CineShotWidget(parent, self, shot_data=self.shot_data, parent_class=parent_class)
		self.sequence_layout.addWidget(self.sequence_widget.ui)

		self.open_button()
		self.tool_button.pressed.connect(self.button_pressed)

		self.sequence_widget.ui.shot_number_lineEdit.setText(str(self.shot_data.shot_number))
		self.sequence_widget.ui.start_frame_lineEdit.setText(str(self.shot_data.shot_start))
		self.sequence_widget.ui.end_frame_lineEdit.setText(str(self.shot_data.shot_end))
		self.sequence_widget.ui.camera_comboBox.addItems(self.shot_camera_list)
		self.sequence_widget.ui.camera_comboBox.setCurrentText(self.shot_data.shot_camera)
		self.sequence_widget.setup_signals()

	def remove_frame(self):
		"""
		Removes the frame from the layout.

		"""

		self.parent_layout.removeWidget(self)
		self.deleteLater()

	def button_pressed(self):
		"""
		Opens or closes the QToolbarButton

		"""

		if self.q_frame and not self.q_frame.isVisible():
			self.open_button()
		else:
			self.close_button()

	def open_button(self):
		"""
		Opens the QToolbarButton

		"""

		self.tool_button.setArrowType(qtcore.Qt.DownArrow)
		self.q_frame.setVisible(1)
		self.setMinimumHeight(195)

	def close_button(self):
		"""
		Closes the QToolbarButton

		"""

		self.tool_button.setArrowType(qtcore.Qt.RightArrow)
		self.q_frame.setVisible(0)
		self.setMinimumHeight(25)


class CineShotWidget(common_windows.ParentableWidget):
	def __init__(self, parent=None, parent_frame=None, shot_data=None, parent_class=None):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'cine_shot_editor_ui_sub.ui')
		super().__init__(parent=parent,
						 ui_path=ui_path)
		self.shot_data = shot_data
		self.parent_frame = parent_frame
		int_validator = qtgui.QIntValidator()
		self.ui.start_frame_lineEdit.setValidator(int_validator)
		self.ui.end_frame_lineEdit.setValidator(int_validator)
		self.ui.shot_number_lineEdit.setValidator(int_validator)
		self.ui.camera_comboBox.setFocusPolicy(qtcore.Qt.ClickFocus)

		eye_icon = resources.icon(r'default\eye.png')
		visible_range_button = self.ui.set_timeline_pushButton
		visible_range_button.setIcon(eye_icon)

		unlock_icon = resources.icon(r'default\unlock.png')
		lock_button = self.ui.lock_camera_pushButton
		lock_button.setIcon(unlock_icon)
		self.ui.camera_comboBox.setEnabled(False)

		self.parent_class = parent_class

	def setup_signals(self):
		"""
		Connects buttons to functions.

		"""
		self.ui.set_timeline_pushButton.pressed.connect(self._on_frame_timeline_button_pressed)
		self.ui.remove_shot_pushButton.pressed.connect(self._on_remove_shot_button_pressed)
		self.ui.start_frame_lineEdit.editingFinished.connect(self._on_shot_start_edited)
		self.ui.end_frame_lineEdit.editingFinished.connect(self._on_shot_end_edited)
		self.ui.camera_comboBox.currentIndexChanged.connect(self._on_shot_camera_edited)
		self.ui.shot_number_lineEdit.editingFinished.connect(self._on_shot_number_edited)
		self.ui.playblast_shot_pushButton.pressed.connect(self._on_playblast_shot_button_pressed)
		self.ui.break_out_pushButton.pressed.connect(self._on_break_out_button_pressed)
		self.ui.lock_camera_pushButton.pressed.connect(self._on_lock_camera_button_pressed)

	
	def _on_break_out_button_pressed(self):
		"""
		Breaks out the shot.

		"""

		if not pm.objExists(self.shot_data.node_name):
			messages.info_message('Break Out Shot', f'{self.shot_data.shot_name} does not exist.')
			return
		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		if not cine_seq_node:
			messages.info_message('Break Out Shot', 'CineSequenceComponent node not found.')
			return

		save_answer = messages.question_message('Break Out Shot',
												'Breaking out will remove other shots from scene, save now?',
												tri_option=True)
		if save_answer == 'Yes':
			file_name = str(cmds.file(q=1, sn=1))
			fileio.touch_path(file_name)
			cmds.file(save=True, force=True)
		elif save_answer == '&No':
			pass
		else:
			return

		shot_node = pm.PyNode(self.shot_data.node_name)
		shot_number = self.shot_data.shot_number
		cine_file_utils.break_out(shot_node, shot_number, cine_seq_node)

	
	def _on_playblast_shot_button_pressed(self):
		"""
		Playblasts the shot.

		:param bool skip_dialog: If we should skip message dialog about created playblast.

		"""

		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		if not cine_seq_node:
			logger.warning('CineSequenceComponent node not found.')
			return
		if not pm.objExists(self.shot_data.shot_camera):
			logger.warning(f'Camera {self.shot_data.shot_camera} does not exist.')
			return
		blast_path = shot_utils.create_cine_playblast(cine_seq_node.seq_name(),
										 self.shot_data.shot_name,
										 self.shot_data.stage,
										 [self.shot_data.shot_start, self.shot_data.shot_end],
										 pm.PyNode(self.shot_data.shot_camera))

	
	def _on_frame_timeline_button_pressed(self):
		"""
		Sets the timeline range.

		"""

		time_utils.set_timeline_range(int(self.ui.start_frame_lineEdit.text()), int(self.ui.end_frame_lineEdit.text()))

	
	def _on_remove_shot_button_pressed(self):
		"""
		Removes a shot from the sequence and deletes the widget for it.

		"""

		question_result = messages.question_message('Remove Shot?',
													f'Are you sure you want to remove {self.shot_data.shot_name}?')
		if not question_result == 'Yes':
			return
		try:
			ref_path = pm.referenceQuery(self.shot_data.shot_camera, filename=True)
			if ref_path:
				ref_node = pm.FileReference(ref_path)
				maya_ref_node = ref_node.refNode.name()
				# remove the reference and its contents including namespace
				ref_node.remove(f=True)
				foster_p_list = pm.ls(f'{maya_ref_node}fosterPar*', type=pm.nt.FosterParent)
				if foster_p_list:
					foster_p = foster_p_list[0]
					pm.delete(foster_p)
		except RuntimeError:
			logger.info(f'Reference node not found for {self.shot_data.shot_camera}')
			pm.delete(self.shot_data.shot_camera)

		if pm.objExists(self.shot_data.node_name):
			pm.delete(self.shot_data.node_name)
		if pm.namespace(exists=self.shot_data.shot_name):
			namespace_utils.purge_namespace(self.shot_data.shot_name)
		del self.parent_class.shot_widgets_dict[self]
		ubercam = [x for x in pm.ls(type=pm.nt.Camera) if x.getTransform().hasAttr('MCAUberCam')]
		if ubercam:
			camera_utils.create_mca_ubercam_cmd()
		self.ui.close()
		self.parent_frame.remove_frame()
		self.deleteLater()

	def _on_shot_start_edited(self):
		"""
		Sets the start frame of the shot.

		"""

		self.shot_data.shot_start = self.ui.start_frame_lineEdit.text()
		if pm.objExists(self.shot_data.node_name):
			shot_node = pm.PyNode(self.shot_data.node_name)
			shot_node.startFrame.set(float(self.shot_data.shot_start))

	def _on_shot_end_edited(self):
		"""
		Sets the end frame of the shot.

		"""

		self.shot_data.shot_end = self.ui.end_frame_lineEdit.text()
		if pm.objExists(self.shot_data.node_name):
			shot_node = pm.PyNode(self.shot_data.node_name)
			shot_node.endFrame.set(float(self.shot_data.shot_end))

	def _on_shot_camera_edited(self):
		"""
		Sets the shot camera.

		"""

		self.shot_data.shot_camera = self.ui.camera_comboBox.currentText()
		if pm.objExists(self.shot_data.node_name):
			shot_node = pm.PyNode(self.shot_data.node_name)
			pm.shot(shot_node, e=True, cc=self.shot_data.shot_camera)

	def _on_shot_number_edited(self):
		"""
		Sets the shot number.

		"""

		if not self.ui.shot_number_lineEdit.isModified():
			return
		old_shot_cam_name = self.shot_data.shot_camera

		new_shot_number = self.ui.shot_number_lineEdit.text()
		new_shot_number_forced_format = f'{int(new_shot_number):0=3d}'
		if not new_shot_number == new_shot_number_forced_format:
			self.ui.shot_number_lineEdit.setText(new_shot_number_forced_format)
			new_shot_number = new_shot_number_forced_format

		shot_node = pm.PyNode(self.shot_data.node_name)
		new_shot_name = shot_node.shotName.get().replace(self.shot_data.shot_number, new_shot_number)
		new_shot_data = shot_utils.rename_shot(self.shot_data, new_shot_name)

		self.ui.camera_comboBox.blockSignals(True)
		for i in range(self.ui.camera_comboBox.count()):
			if self.ui.camera_comboBox.itemText(i) == old_shot_cam_name:
				self.ui.camera_comboBox.removeItem(i)
				break
		camera_items = []
		for index in range(self.ui.camera_comboBox.count()):
			camera_items.append(self.ui.camera_comboBox.itemText(index))
		if new_shot_data.shot_camera not in camera_items:
			self.ui.camera_comboBox.addItem(new_shot_data.shot_camera)
		self.ui.camera_comboBox.setCurrentText(new_shot_data.shot_camera)
		self.parent_frame.tool_button.setText(new_shot_data.shot_name)
		self.ui.camera_comboBox.blockSignals(False)

		self.parent_class.shot_widgets_dict[self] = new_shot_data
		self.shot_data = new_shot_data
		self.parent_class.initialize_shot_widgets()

	
	def _on_lock_camera_button_pressed(self):
		"""
		Locks or unlocks the camera combobox.

		"""

		is_enabled = self.ui.camera_comboBox.isEnabled()
		if not is_enabled:
			self.ui.camera_comboBox.setEnabled(True)
			lock_icon = resources.icon(r'default\lock.png')
			self.ui.lock_camera_pushButton.setIcon(lock_icon)

		else:
			self.ui.camera_comboBox.setEnabled(False)
			lock_icon = resources.icon(r'default\unlock.png')
			self.ui.lock_camera_pushButton.setIcon(lock_icon)
