
# python imports
import os
import math
from PySide2.QtGui import QIntValidator

# Software specific imports
import pymel.core as pm

# mca Python imports
from mca.common import log
from mca.common.paths import project_paths
from mca.common.pyqt import messages
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.utils import process
from mca.common.modifiers import decorators
from mca.mya.pyqt import mayawindows
from mca.mya.animation import time_utils, baking
from mca.mya.rigging.tek import tek_rig
from mca.mya.cinematics import cine_file_utils, shot_utils
from mca.mya.utils import optionvars

logger = log.MCA_LOGGER

POSE_LIB_PATH = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Cinematics', 'Facial', 'MocapX', 'PoseLib')
AMB_PATH = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Cinematics', 'Facial', 'Ambient')


class MCAFacialMocapProcessor(optionvars.MCAOptionVars):
	"""
	Option vars for the Facial Mocap Processor.
	"""
	MCABakeAnimation = {'default_value': 1, 'docstring': 'Bake animation on process.'}
	MCAFacialTypeDir = {'default_value': 1, 'docstring': 'Whether directory to look in is ambients'}
	MCAMocapXHeadSelection = {'default_value': 0, 'docstring': 'Latest head selected.'}

	@property
	def mocapx_head_selection(self):
		"""
		Returns Source head index in combo box.
		:rtype: Int
		"""

		return self.MCAMocapXHeadSelection

	@mocapx_head_selection.setter
	def mocapx_head_selection(self, value):
		"""
		Sets source head index in combo box.
		:rtype: Int
		"""

		self.MCAMocapXHeadSelection = value


class FacialMocapProcessor(mayawindows.MCAMayaWindow):
	VERSION = '1.0.0'

	def __init__(self):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'facial_mocap_processor_ui.ui')
		super().__init__(title='Facial Mocap Processor',
						 ui_path=ui_path,
						 version=FacialMocapProcessor.VERSION)
		self.optionvars = MCAFacialMocapProcessor()
		process.cpu_threading(dcc_tracking.ddc_tool_entry(FacialMocapProcessor))

		for head in os.listdir(POSE_LIB_PATH):
			file_name = os.path.basename(head)
			display_name = file_name.split('_MocapX_PoseLib.ma')
			self.ui.heads_comboBox.addItem(display_name[0])

		self.ui.audio_offset_lineEdit.setValidator(QIntValidator())
		audio_node = pm.ls(type=pm.nt.Audio)
		if audio_node:
			self.ui.audio_offset_lineEdit.setText(str(int(audio_node[0].offset.get())))

		self.ui.process_mocap_pushButton.clicked.connect(self._on_process_mocap_button_clicked)
		self.ui.export_file_pushButton.clicked.connect(self._on_export_file_button_clicked)
		self.ui.batch_export_pushButton.clicked.connect(self._on_batch_export_button_clicked)
		self.ui.audio_offset_lineEdit.editingFinished.connect(self._on_audio_offset_line_editing_finished)
		self.ui.bake_visible_range_pushButton.clicked.connect(self._on_bake_visible_range_button_clicked)
		self.ui.smooth_curves_pushButton.clicked.connect(self._on_smooth_curves_button_clicked)
		self.ui.frame_audio_pushButton.clicked.connect(self._on_frame_audio_button_clicked)
		self.ui.ambient_radioButton.toggled.connect(self._ambient_radio_button_toggled)

		self.ui.bake_animation_checkBox.setChecked(self.optionvars.MCABakeAnimation)
		self.ui.heads_comboBox.setCurrentIndex(self.optionvars.mocapx_head_selection)
		self.ui.ambient_radioButton.setChecked(self.optionvars.MCAFacialTypeDir)
		self.ui.clickable_radioButton.setChecked(not self.optionvars.MCAFacialTypeDir)
		self._ambient_radio_button_toggled()
		self.ui.bake_animation_checkBox.clicked.connect(self._set_bake_animation)
		self.ui.heads_comboBox.currentIndexChanged.connect(self._set_mocapx_head_selection_optionvars)
		self.ui.ambient_radioButton.toggled.connect(self._set_facial_type_dir_optionvars)

	def _ambient_radio_button_toggled(self):
		"""
		Sets up export head combo box.

		"""

		if self.ui.ambient_radioButton.isChecked():
			path_to_check = os.path.join(AMB_PATH, 'Ambients')
		else:
			path_to_check = os.path.join(AMB_PATH, 'Clickables')

		char_dirs = [x for x in os.listdir(path_to_check) if os.path.isdir(os.path.join(path_to_check, x))]
		self.ui.export_head_comboBox.clear()
		self.ui.export_head_comboBox.addItems(char_dirs)

	def _set_facial_type_dir_optionvars(self):
		"""
		Set the optionvar for source head selection.

		"""

		self.optionvars.MCAFacialTypeDir = self.ui.ambient_radioButton.isChecked()

	def _set_mocapx_head_selection_optionvars(self):
		"""
		Set the optionvar for source head selection.

		"""

		self.optionvars.mocapx_head_selection = self.ui.heads_comboBox.currentIndex()

	def _set_bake_animation(self):
		"""
		Set the optionvar checkbox to bake animation on process.

		"""

		self.optionvars.MCABakeAnimation = self.ui.bake_animation_checkBox.isChecked()

	@decorators.track_fnc
	def _on_process_mocap_button_clicked(self):
		"""
		Loads mocap and audio based on user selections.

		"""

		message_result = messages.question_message('Process Facial Mocap', 'This will open a new scene, continue?')
		if not message_result == 'Yes':
			return
		selected_head = self.ui.heads_comboBox.currentText()

		head_path = os.path.join(POSE_LIB_PATH, f'{selected_head}_MocapX_PoseLib.ma')
		# Select and load mocap
		pm.newFile(force=True)
		pm.openFile(head_path, open=True, esn=True)

		mocap_dir = AMB_PATH
		mocap_path = pm.fileDialog2(fileFilter="MocapX Files (*.mcpx)", dialogStyle=1, fm=1, dir=mocap_dir,
										cap='Import Mocap')
		if not mocap_path:
			return
		sounds_dir = os.path.join(mocap_path[0].split('MocapX')[0], 'Audio')
		if os.path.exists(sounds_dir):
			mocap_dir = sounds_dir
		sounds_path = pm.fileDialog2(fileFilter="WAV Files (*.wav)", dialogStyle=1, fm=1, dir=mocap_dir,
										cap='Import Audio')
		if not sounds_path:
			return

		bake_anim = self.ui.bake_animation_checkBox.isChecked()
		sound_node = shot_utils.load_facial_mocap(sounds_path, mocap_path, bake_anim=bake_anim)
		self.ui.audio_offset_lineEdit.setText(str(int(sound_node.offset.get())))

	@decorators.track_fnc
	def _on_export_file_button_clicked(self):
		"""
		Exports face animation as FBX.

		"""

		export_path = cine_file_utils.export_face_anim_cmd()
		messages.info_message('Export FBX', f'Face animation exported to:\n{export_path}.')

	@decorators.track_fnc
	def _on_batch_export_button_clicked(self):
		"""
		Batch exports selected CDW

		"""

		message_result = messages.question_message('Batch Export', 'This will open a new scene, continue?')
		if not message_result == 'Yes':
			return
		selected_dir = 'Ambients' if self.ui.ambient_radioButton.isChecked() else 'Clickables'
		selected_char = self.ui.export_head_comboBox.currentText()
		char_dir = os.path.join(AMB_PATH, selected_dir, selected_char)
		for char_file in os.listdir(char_dir):
			if os.path.splitext(char_file)[-1] == '.ma':
				pm.newFile(force=True)
				pm.openFile(os.path.join(char_dir, char_file), open=True, esn=True)
				cine_file_utils.export_face_anim_cmd()

	def _on_audio_offset_line_editing_finished(self):
		"""
		Sets the audio offset.

		"""

		if not self.ui.audio_offset_lineEdit.isModified():
			return
		new_offset = self.ui.audio_offset_lineEdit.text()
		audio_node = pm.ls(type=pm.nt.Audio)
		if not audio_node:
			messages.info_message('Set Audio Offset', 'No audio node found in scene.')
			logger.warning('No audio node found in scene.')
			return
		audio_node[0].offset.setLocked(False)
		audio_node[0].offset.set(int(new_offset))

	@decorators.track_fnc
	def _on_smooth_curves_button_clicked(self):
		"""
		Smooths animation curves using an AnimBot command.

		"""

		try:
			curve_list = pm.ls(type=pm.nt.AnimCurve)
			pm.select(curve_list, r=True)
			list(map(lambda x: pm.selectKey(x, add=True), curve_list))
			exec('from animBot._api.core import CORE as ANIMBOT_CORE; ANIMBOT_CORE.trigger.keySlider_smoothRough_neg100()')
		except ModuleNotFoundError:
			messages.info_message('Smooth Curves', 'Please ensure you have AnimBot installed.')
			logger.warning('AnimBot module not found.')
			return

	@decorators.track_fnc
	def _on_bake_visible_range_button_clicked(self):
		"""
		Bakes the visible range of a head rig.

		"""

		head_rig = tek_rig.get_tek_rigs()
		if head_rig:
			head_rig = head_rig[0]
			head_flags = head_rig.get_flags()
			range = time_utils.get_visible_range()
			baking.bake_objects(head_flags, bake_range=range)

	@decorators.track_fnc
	def _on_frame_audio_button_clicked(self):
		"""
		Frames the range on the audio file with a 30 frame handle on either side in the timeline.

		"""

		audio_node = pm.ls(type=pm.nt.Audio)
		if not audio_node:
			messages.info_message('Frame Audio Range', 'No audio node found in scene.')
			logger.warning('No audio node found in scene.')
			return

		audio_node = audio_node[0]
		audio_start_frame = round(audio_node.offset.get())
		audio_end_frame = math.ceil(audio_node.duration.get() + audio_start_frame)

		time_utils.set_timeline_range(audio_start_frame - 30, audio_end_frame + 30)

