"""
Utils for cinematic files/scenes
"""
# python imports
import os
import math

# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
from mca.common.paths import paths
from mca.common.utils import fileio
from mca.common.pyqt import messages

from mca.mya.cinematics import cine_sequence_nodes
from mca.mya.utils import scene_utils, namespace, fbx_utils, constraint, camera_utils
from mca.mya.animation import time_utils, baking
from mca.mya.rigging import rig_utils
from mca.mya.rigging import tek
from mca.mya.rigging.tek import tek_rig, cine_sequence_component
from mca.mya.tools.animationexporter import animationexporter_utils as ae_utils

logger = log.MCA_LOGGER


def make_initial_folder_structure(seq_dir):
	"""
	Creates folders for new sequence.

	:param str seq_dir: Path to directory to be created.

	"""

	os.mkdir(seq_dir)
	directories = ['mocap', 'layout', 'assets', 'audio', 'video', 'reference', 'exports', 'shots']
	for directory in directories:
		directory_path = os.path.join(seq_dir, directory)
		os.mkdir(directory_path)


def get_save_dir(stage, seq_dir, shot_number=None):
	"""
	Gets the directory where we want to save a Maya scene.

	:param str stage: Stage for this sequence or shot, layout or animation
	:param str seq_dir: Path to sequences directory
	:param str shot_number: Shot number to save, if None we assume this is a layout sequence.
	:return: Returns either the shot directory for the shot number or layout directory for the sequence.
	:rtype: str

	"""

	if shot_number:
		shots_dir = os.path.join(seq_dir, 'shots')
		if not os.path.exists(shots_dir):
			os.mkdir(shots_dir)
		shot_dir = os.path.normpath(os.path.join(shots_dir, shot_number))
		if not os.path.exists(shot_dir):
			os.mkdir(shot_dir)
		stage_dir = os.path.join(shot_dir, stage)
		if not os.path.exists(stage_dir):
			os.mkdir(stage_dir)
		return stage_dir

	else:
		layout_dir = os.path.join(seq_dir, 'layout')
		if not os.path.exists(layout_dir):
			os.mkdir(layout_dir)
		return layout_dir


def save_new_version(seq_name, stage, shot_number=None):
	"""
	Updates a sequence node and saves out a new version of a sequence.

	:param str seq_name: Name of the sequence.
	:param str stage: Stage for this sequence or shot, layout or animation
	:param str shot_number: Shot number to save, if None we assume this is a layout sequence

	"""

	seq_dir = os.path.join(paths.get_cine_seq_path(), seq_name)
	if not os.path.exists(seq_dir):
		make_initial_folder_structure(seq_dir)

	save_dir = get_save_dir(stage, seq_dir, shot_number=shot_number)

	version = get_version_number(save_dir)
	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	if cine_seq_node:
		cine_seq_node.pynode.versionNumber.set(version)
		cine_seq_node.pynode.stage.set(stage)
	save_file(save_dir, seq_name, stage, version, shot_number=shot_number)


def save_file(directory_path, seq_name, stage, version_number, shot_number=None):
	"""
	Uses CineSequenceNode to determine a name for a Maya scene then saves the scene to a provided path.

	:param str directory_path: Path to directory where we want to save the Maya scene.
	:param str seq_name: Name of the sequence.
	:param str stage: Stage for this sequence or shot, layout or animation
	:param str/int version_number: Version number for this sequence.
	:param str shot_number: Shot number to save, if None we assume this is a layout sequence.

	"""

	version_num = f'{int(version_number):0=3d}'
	if not shot_number:
		save_as = f'{seq_name}_{stage}_v{version_num}.ma'
	else:
		save_as = f'{seq_name}_shot_{shot_number}_{stage}_v{version_num}.ma'

	new_file_name = os.path.join(directory_path, save_as)
	cmds.file(rename=new_file_name)
	# save the file
	cmds.file(save=1, type='mayaAscii', f=1)


def get_latest_version(directory):
	"""
	Looks through a provided directory and returns a new file version based on the names of the files.

	:param str directory: Directory to look through.
	:return: Returns a value 1 higher than the highest version value within the directory.
	:rtype: str

	"""
	latest_version = 0
	highest_version_file = None
	for f in os.listdir(directory):
		f_name = f.split('.')[0]
		version_number = f_name[-3:]
		if version_number.isdigit():
			version_number = int(version_number)
			if version_number > latest_version:
				latest_version = version_number
				highest_version_file = f

	return highest_version_file


def get_version_number(directory):
	"""
	Looks through a provided directory and returns a new file version based on the names of the files.

	:param str directory: Directory to look through.
	:return: Returns a value 1 higher than the highest version value within the directory.
	:rtype: str

	"""

	file_list = os.listdir(directory)
	file_versions = []
	latest_version = 0

	for f in file_list:
		version_number = os.path.splitext(f)[0][-3:]
		if version_number.isdigit():
			file_versions.append(int(version_number))
	if file_versions:
		latest_version = max(file_versions)
	return f'{(latest_version + 1):0=3d}'


def open_maya_file(file_path):
	"""
	Opens a new files and sets playback options

	:param str file_path: Path of the file we want to open.

	"""

	pm.newFile(force=True)
	pm.openFile(file_path, open=True)
	start_frame = cmds.playbackOptions(q=True, min=True)
	end_frame = cmds.playbackOptions(q=True, max=True)

	pm.evalDeferred(f'cmds.playbackOptions(min={start_frame})')
	pm.evalDeferred(f'cmds.playbackOptions(ast={start_frame})')
	pm.evalDeferred(f'cmds.playbackOptions(max={end_frame})')
	pm.evalDeferred(f'cmds.playbackOptions(aet={end_frame})')


def break_out(shot_node, shot_number, cine_seq_node):
	"""
	Breaks a shot out into its own Maya scene

	:param pm.nt.Shot shot_node: Shot node that we want to clean the file around.
	:param CineSequenceComponent cine_seq_node: Instance of CineSequenceComponent
	:param str/int shot_number: Number for the shot

	"""

	cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
	stage = cine_seq_data.stage
	seq_name = cine_seq_data.seq_name
	clean_shot_node = clean_cine_file(shot_node, cine_seq_node=cine_seq_node)
	cine_sequence_nodes.CineShotData.get_shot_data_from_node(clean_shot_node, cine_seq_data)
	save_new_version(seq_name, stage, shot_number=shot_number)


def set_seq_node(cine_seq_node, cine_class, maya_node, clean_anim=False):
	"""
	Sets sequence node to either layout or animation, updating both the CineSequenceNode class and sequence node in Maya.

	:param CineSequenceNode cine_seq_node: Instance of CineSequenceNode class that stores information about the sequence.
	:param CineShot/CineScene cine_class: Cinematic python class containing information about the shot and/or scene.
	:param pm.nt.Transform maya_node: Sequence node in Maya to be updated.
	:param bool clean_anim: If True, set stage to animation. Otherwise, set to layout.
	:return: Returns the class and Maya node that were updated.
	:rtype: CineSequenceNode, pm.nt.Transform
	"""

	stage = maya_node.stage.get()
	if stage != 2:
		if clean_anim:
			stage_num = 2
		else:
			stage_num = 1

		maya_node.setLocked(False)
		maya_node.stage.setLocked(False)
		maya_node.stage.set(stage_num)
		# set stage to layout
		cine_seq_node.stage_number = maya_node.stage.get()
		cine_seq_node.stage = maya_node.stage.get(asString=True)
		maya_node.stage.setLocked(True)

		if cine_seq_node.is_shot:
			# set shot number
			cine_seq_node.shot_number = cine_class.number
			maya_node.shotNumber.setLocked(False)
			maya_node.shotNumber.set(int(cine_class.number))
			maya_node.shotNumber.setLocked(True)

		maya_node.setLocked(True)
	else:
		logger.info("This is already an animation file")

	return cine_seq_node, maya_node


def clean_cine_file(shot_node, cine_seq_node=None):
	"""
	Sets animation to frame zero, shifts audio accordingly, and can do file cleanup.

	:param pm.nt.Shot shot_node: Shot node that we want to clean the file around.
	:param CineSequenceComponent cine_seq_node: Instance of CineSequenceComponent
	:return: Returns a clean shot node.
	:rtype: pm.nt.Shot

	"""

	start_frame = shot_node.startFrame.get()
	end_frame = shot_node.endFrame.get()
	shot_name = shot_node.shotName.get()
	cam = shot_node.currentCamera.get()
	handle_anim_layers()
	anim_curve_list = pm.ls(type=pm.nt.AnimCurve)
	clean_animation(anim_curve_list, start_frame, end_frame, post_anim_handle=30, pre_anim_handle=30)

	scene_utils.delete_empty_display_layers()
	shift_animation(start_frame, end_frame)
	offset_audio(shot_node)

	delete_extra_cameras(cam)
	# delete all shots and recreate clean shot node
	all_shots = pm.ls(type=pm.nt.Shot)

	sht = pm.shot(sn=shot_name,
				  st=0,
				  et=end_frame - start_frame,
				  cc=cam,
				  sst=0)
	if cine_seq_node:
		sht.addAttr('sequenceNode', at='message')
		cine_seq_node.pynode.shots >> sht.sequenceNode
	pm.shot(sht, e=True, lock=True)

	for s in all_shots:
		pm.shot(s, e=True, lck=False)
	pm.delete(all_shots)

	return sht


def is_shot_cam(obj):
	"""
	Checks an object to see if it is a shot camera
	:param obj: Object to check
	:return: Returns True if the object is a shot camera, else False
	:rtype: bool

	"""
	if isinstance(obj, str):
		obj = pm.PyNode(obj)
	if not isinstance(obj, pm.nt.Camera):
		obj = obj.getShape()
		if not isinstance(obj, pm.nt.Camera):
			return False
	def_cams = ['perspShape', 'frontShape', 'sideShape', 'topShape', 'leftShape',
			   'bottomShape', 'backShape', 'MCAUberCam:MCAUberCamShape']
	if obj.name() in def_cams:
		return False
	elif obj.hasAttr('MCAUberCam'):
		return False
	else:
		return True


def delete_extra_cameras(safe_cam):
	"""
	Deletes extra cameras from the scene.

	:param pm.nt.Transform safe_cam: Camera to not delete.

	"""

	scene_cams = pm.ls(type=pm.nt.Camera)
	for cam in scene_cams:
		xform = cam.getTransform()
		if is_shot_cam(xform.name()) and xform != safe_cam:
			try:
				ref_path = pm.referenceQuery(xform, filename=True)
				if ref_path:
					ref_node = pm.FileReference(ref_path)
					# remove the reference and its contents including namespace
					ref_node.remove(f=True)
			except RuntimeError:
				logger.info(f'Reference node not found for {xform}')
				pm.delete(xform)
		elif xform.hasAttr('MCAUberCam'):
			camera_utils.remove_ubercam_cmd()
	foster_parent_nodes = pm.ls(type=pm.nt.FosterParent)
	if foster_parent_nodes:
		pm.delete(foster_parent_nodes)


def handle_anim_layers():
	"""
	Merges all animation layers in scene.

	"""

	anim_layers = pm.ls(type=pm.nt.AnimLayer)
	if anim_layers:
		for layer in anim_layers:
			pm.animLayer(layer, e=True, l=False)
		mel.eval('source "performAnimLayerMerge.mel"')
		mel.eval('animLayerMerge(`ls -type animLayer`)')


def clean_animation(anim_curve_list, shot_start, shot_end, post_anim_handle=0, pre_anim_handle=0):
	"""
	Cleans animation by merging animation layers and keying the first and last keys of the curves in scene.

	:param list(pm.nt.AnimCurve) anim_curve_list: List of animation curves to be cleaned
	:param int shot_start: Start time of the shot
	:param int shot_end: End time of the shot
	:param int post_anim_handle: Number of frames to leave untouched after shot end.
	:param int pre_anim_handle: Number of frames to leave untouched before shot start.

	"""

	for anim_curve in anim_curve_list:
		# KEY EVERYTHING IN ANIMATION AT THE START AND THE STOP TIME OF THE SHOT + HANDLES
		pm.setKeyframe(anim_curve, time=(shot_start, shot_end), i=True)
		pm.setKeyframe(anim_curve, time=shot_start-pre_anim_handle, i=True)
		pm.setKeyframe(anim_curve, time=shot_end+post_anim_handle, i=True)
		pm.cutKey(anim_curve, t=f':{shot_start-pre_anim_handle-1}', cl=True)
		# Leave handle at end of shot so animators can easily adjust the +1 frame needed to match up frames in UE
		pm.cutKey(anim_curve, t=f'{shot_end+post_anim_handle+1}:', cl=True)
	time_utils.set_timeline_range(shot_start, shot_end)

def offset_audio(maya_shot):
	"""
	Sets audio in scene to start time of shot

	:param pm.nt.Shot maya_shot: Shot node whose audio we want to offset.

	"""

	audio_list = pm.ls(type=pm.nt.Audio)
	if audio_list:
		audio = audio_list[0]
		offset_time = pm.shot(maya_shot, q=True, sst=True)
		audio.offset.set(-offset_time)


def shift_animation(start_frame, end_frame):
	"""
	Shifts animation to frame 0 and updates the cine class instance with new start and end time.

	:param int start_frame: Start time of the shot
	:param int end_frame: End time of the shot

	"""

	end_time = end_frame - start_frame
	# set mya timeline
	pm.playbackOptions(min=0)
	pm.playbackOptions(ast=0)
	pm.playbackOptions(max=end_time)
	pm.playbackOptions(aet=end_time)
	# offset animation to frame 0
	anim = pm.ls(type=pm.nt.AnimCurve)
	if anim:
		try:
			pm.keyframe(anim,
						  hi='below', edit=True, r=True, iub=True, option='over', timeChange=(-start_frame))
		except RuntimeError:
			pass


def reload_references():
	"""
	Command to reload file references in a scene.

	"""

	file_refs = cmds.file(q=True, r=True)
	for ref in file_refs:
		if cmds.referenceQuery(ref, isLoaded=True):
			cmds.file(ref, loadReference=True)


@decorators.track_fnc
def break_out_selected_shot_cmd():
	"""
	Command to break out the selected shot.

	"""

	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
	if not cine_seq_node:
		messages.info_message('Break Out Selected Shot', 'Cine sequence node not found.')
		return
	selected_shots = [s for s in pm.selected() if isinstance(s, pm.nt.Shot)]
	if not selected_shots:
		messages.info_message('Break Out Selected Shot', 'No shots selected.')
		return
	shot_data_list = [cine_sequence_nodes.CineShotData.get_shot_data_from_node(x, cine_seq_data)
					  for x in selected_shots]
	if selected_shots:
		broken_out_shots = None
		if len(selected_shots) > 1:
			broken_out_shots = batch_breakout(shot_data_list)

		elif len(selected_shots) == 1:
			shot_data = shot_data_list[0]
			shot_number = shot_data.shot_number
			shot_node = pm.PyNode(shot_data.node_name)
			break_out(shot_node, shot_number, cine_seq_node)
			broken_out_shots = shot_data.shot_name
		if broken_out_shots:
			if len(broken_out_shots) > 1:
				broken_out_shots_sorted = list(sorted(shot_data_list, key=lambda x: x.shot_number))
				broken_out_shots = '\n'.join(list(map(lambda x: x.shot_name, broken_out_shots_sorted)))
			messages.info_message('Break Out Selected Shot', f'Shots broken out:\n \n{broken_out_shots}')


def batch_breakout(shot_data_list):
	"""
	Batch breakout of all shots in shot data list.

	:param list(CineShotData) shot_data_list: List of CineShotData objects which contain data about the shot
	:return: List of shot names which were broken out or None if no shots were broken out.
	:rtype: list(str) or None

	"""

	file_name = str(cmds.file(q=1, sn=1))
	save_answer = messages.question_message('Breakout Shots',
											'Batch breaking out shots involves reopening the scene, save now?',
											tri_option=True)
	if save_answer == 'Yes':
		fileio.touch_path(file_name)
		cmds.file(save=True, force=True)
	elif save_answer == '&No':
		pass
	else:
		return None

	logger.info(f'Breaking out {file_name}')
	for shot_data in shot_data_list:
		cmds.file(file_name, o=True, f=True)
		cine_seq_node = cine_sequence_component.find_cine_seq_component()
		shot_node = pm.PyNode(shot_data.node_name)
		shot_number = shot_data.shot_number
		break_out(shot_node, shot_number, cine_seq_node)
	return [x.shot_name for x in shot_data_list]


@decorators.track_fnc
def execute_batch_breakout():
	"""
	Command to execute batch breakout of all shots in a scene.

	"""

	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)
	if cine_seq_node:
		shot_data_list = [cine_sequence_nodes.CineShotData.get_shot_data_from_node(x, cine_seq_data)
						  for x in cine_seq_node.shots()]
		batch_breakout(shot_data_list)


def get_seq_file_list(sequence_name):
	"""
	Returns a list of files and directories for a sequence.

	:param str sequence_name: Three letter sequence name.
	:return: Returns a dictionary of files
	and directories for a sequence.
	:rtype: dict

	"""

	file_dir = None
	files = []
	layout_dirs = []
	sequence_dir = os.path.normpath(os.path.join(paths.get_cine_seq_path(), sequence_name))
	previs_dir = os.path.normpath(os.path.join(sequence_dir, 'previs'))
	layout_dir = os.path.normpath(os.path.join(sequence_dir, 'layout'))
	shots_dir = os.path.normpath(os.path.join(sequence_dir, 'shots'))
	scenes_dir = os.path.normpath(os.path.join(sequence_dir, 'scenes'))
	if os.path.exists(previs_dir):
		layout_dirs.append(previs_dir)
	if os.path.exists(layout_dir):
		layout_dirs.append(layout_dir)
	if os.path.exists(shots_dir):
		file_dir = shots_dir
		files += os.listdir(shots_dir)
	elif os.path.exists(scenes_dir):
		file_dir = scenes_dir
		files += os.listdir(scenes_dir)
	if len(files) < 1:
		logger.warning('No Files Found')

	return {'files': files, 'file_dir': file_dir, 'layout_dirs': layout_dirs}


def rename_sequence_files(old_name, new_name):
	"""
	Renames sequence files to new three letter sequence name.

	:param str old_name: Name to replace
	:param str new_name: Name to replace with

	"""

	sequence_dir = os.path.join(paths.get_cine_seq_path(), old_name)
	if not os.path.exists(sequence_dir):
		logger.warning(f'Could not find sequence directory: {sequence_dir}')
		return

	main_dir = os.path.dirname(sequence_dir)
	fileio.touch_path(sequence_dir)
	rename_cine_files(sequence_dir, old_name, new_name)
	os.rename(sequence_dir, os.path.join(main_dir, new_name))


def rename_shot_files(old_shot_number, new_shot_number, shot_dir):
	"""
	Renames shot files in a sequence shot directory.

	:param str shot_dir: Path to shot directory to search for files.
	:param str old_shot_number: Number to replace
	:param str new_shot_number: Number to replace with

	"""

	if not os.path.exists(shot_dir):
		return
	fileio.touch_path(shot_dir)
	rename_cine_files(shot_dir, f'_{old_shot_number}', f'_{new_shot_number}')
	os.rename(shot_dir, os.path.join(os.path.dirname(shot_dir), new_shot_number))


def rename_file(version_dir, old_name, new_name):
	"""
	Renames a file in a version directory.

	:param str version_dir: Path to version directory to search for files.
	:param str old_name: Name to replace
	:param str new_name: Name to replace with

	"""
	file_path = os.path.normpath(os.path.join(version_dir, old_name))
	ext = old_name.split('.')[-1]
	new_file_name = os.path.normpath(os.path.join(version_dir, f'{new_name}.{ext}'))

	fileio.touch_path(file_path)
	os.rename(file_path, new_file_name)


def rename_cine_files(sequence_dir, old_name, new_name):
	"""
	Renames files in a sequence directory.

	:param str sequence_dir: Path to directory to search for files.
	:param str old_name: Name to replace
	:param str new_name: Name to replace with

	"""

	for folder_name, sub_folders, file_names in os.walk(sequence_dir):
		for file_name in file_names:
			if f'{old_name}_' in file_name:
				old_path = os.path.join(folder_name, file_name)
				new_file_name = file_name.replace(f'{old_name}_', f'{new_name}_')
				new_path = os.path.join(folder_name, new_file_name)
				fileio.touch_path(old_path)
				os.rename(old_path, new_path)


def process_camera_for_export(cam_xform, shot_start, shot_end):
	"""
	Bakes the camera animation and prepares for export

	:param pm.nt.Transform cam_xform: Camera to process
	:param int shot_start: Start time of the shot
	:param int shot_end: End time of the shot

	"""
	temp_loc = pm.spaceLocator(n=f'{cam_xform.name()}_export_loc')
	loc_con = constraint.parent_constraint_safe(cam_xform, temp_loc, mo=False)
	pm.currentTime(shot_start)
	pm.refresh()

	baking.bake_objects(temp_loc, bake_range=[shot_start, shot_end])
	pm.delete(loc_con)
	cam_constraints = cam_xform.listConnections(type=pm.nt.Constraint)
	if cam_constraints:
		pm.delete(cam_constraints)
	cam_xform.setLocked(False)
	cam_xform.setParent(w=True)
	constraint.parent_constraint_safe(temp_loc, cam_xform, mo=False)

	pm.currentTime(shot_start)
	pm.refresh()
	baking.bake_objects(cam_xform, bake_range=[shot_start, shot_end], pok=False)

	pm.delete(temp_loc)

	# Double check/clean up animation on camera since Maya seems to ignore the range I am giving it when exporting FBX
	anim_curve_list = cam_xform.listConnections(type=pm.nt.AnimCurve) + cam_xform.getShape().listConnections(type=pm.nt.AnimCurve)
	clean_animation(anim_curve_list, shot_start, shot_end)

	remove_attr = ["focusDistance", "centerOfInterest", "fStop"]
	cam_shape = cam_xform.getShape()
	for each_attr in remove_attr:
		pm.cutKey(f'{cam_shape}.{each_attr}', cl=True)

	display_lyr = cam_xform.listConnections(type=pm.nt.DisplayLayer)
	if display_lyr:
		display_lyr[0].drawInfo // cam_xform.drawOverride


def get_export_name(seq_name, shot_number, name):
	"""
	Determines what the export name should be based on data in cine classes

	:param str seq_name: Three letter sequence name
	:param int/str shot_number: Number of the shot
	:param str name: Name of the shot
	:return: Returns the name that the scene should be exported as
	:rtype: str

	"""
	# naming convention: A_SEQ_010_Object
	export_dir = os.path.join(paths.get_cine_seq_path(), seq_name, 'exports')
	if not os.path.exists(export_dir):
		os.mkdir(export_dir)

	save_as = f'A_{seq_name}_{shot_number}_{name}'
	export_name = os.path.normpath(os.path.join(export_dir, save_as))

	return export_name


def export_cine_shot(seq_name, shot_number):
	"""
	Exports animation from a CineShot and updates the XML doc for the sequence

	:param str seq_name: Three letter sequence name
	:param int/str shot_number: Number of the shot

	"""
	shot_node = pm.ls(type=pm.nt.Shot)[0]
	cam = shot_node.currentCamera.get()
	start_frame = shot_node.startFrame.get()
	end_frame = shot_node.endFrame.get()
	if cam:
		process_camera_for_export(cam, start_frame, end_frame+1)
		cam_export_name = get_export_name(seq_name, shot_number, 'cam')
		fileio.touch_path(f'{cam_export_name}.fbx')
		fbx_utils.export_fbx(cam_export_name,
							 cam,
							 start_frame=start_frame,
							 end_frame=end_frame+1)

	all_rigs = tek_rig.get_tek_rigs()
	for rig in all_rigs:
		tek_children = rig.get_tek_children()
		for tek_child in tek_children:
			if isinstance(tek_child, tek.CameraComponent):
				all_rigs.pop(all_rigs.index(rig))

	for char in all_rigs:
		export_name = get_export_name(seq_name,
									  shot_number,
									  namespace.get_namespace(char.pynode, check_node=False))
		export_char_anim(f'{export_name}.fbx', char, start_frame, end_frame)

	cmds.file(rn="DO NOT SAVE")


def export_sequence(seq_name, shot_number_list, stage):
	"""
	Batch exports the latest version of all broken out shots in a sequence

	:param str seq_name: Three letter sequence name
	:param list(int/str) shot_number_list: List of shot numbers to export
	:param str stage: Stage of the files to export, layout or animation

	"""

	sequence_dir = os.path.join(paths.get_cine_seq_path(), seq_name)
	all_shots_dir = os.path.join(sequence_dir, 'shots')
	errored_shots = []
	for shot_number in shot_number_list:

		shot_dir = os.path.join(all_shots_dir, str(shot_number))
		if os.path.exists(shot_dir):
			shot_stage_dir = os.path.join(shot_dir, stage)
			if os.path.exists(shot_stage_dir):
				latest_shot_verion = get_latest_version(shot_stage_dir)
				try:
					pm.openFile(os.path.join(shot_stage_dir, latest_shot_verion), o=True, f=True)
				except Exception as e:
					logger.warning(e)
					errored_shots.append(shot_number)
				export_cine_shot(seq_name, shot_number)

	if errored_shots:
		messages.info_message('Export Error',
		                      f'Error raised while opening shots: {errored_shots}, '
		                      f'please ensure they have exported correctly.')

def export_face_anim_cmd():
	"""
	Exports face animation

	"""

	audio_node = pm.ls(type=pm.nt.Audio)
	if not audio_node:
		logger.warning('No audio nodes found.')
		return

	audio_node = audio_node[0]
	audio_offset = audio_node.offset.get()
	start_time = round(audio_node.sourceStart.get()) + audio_offset
	end_time = math.ceil(audio_node.sourceEnd.get()) + audio_offset
	head_rig = tek_rig.get_tek_rigs()
	if not head_rig:
		logger.warning('No head rig found.')
		return

	audio_file_path = audio_node.filename.get()
	audio_name = os.path.basename(audio_file_path)
	head_rig = head_rig[0]
	export_name = f'A{audio_name.split(audio_name[:2])[-1].split(".wav")[0]}'
	export_path = os.path.join(audio_file_path.split('Audio')[0], 'Exports', f'{export_name}.fbx')

	# Adding 30 frame handle on either side of range per request from Cinematics team
	export_char_anim(export_path, head_rig, start_time-30, end_time+29)

	cmds.file(rn="DO NOT SAVE")
	return os.path.normpath(export_path)

def export_char_anim(export_path, char_rig, start_time, end_time):
	"""
	Exports face animation

	"""

	fileio.touch_path(export_path)

	export_root = rig_utils.bake_skeleton_from_rig(char_rig,
	                                               start_time,
	                                               end_time+1,
	                                               False)

	export_hierarchy = ae_utils._trim_export_hierarchy(export_root)
	export_start, export_end = time_utils.get_keyframe_range_from_nodes(export_hierarchy)

	fbx_utils.export_fbx(export_path,
	                     export_hierarchy,
	                     start_frame=export_start,
	                     end_frame=export_end)

	pm.delete(export_root)
