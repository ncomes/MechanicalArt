#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utils for working with Cinematic shots
"""
# python imports
import traceback
import os
import math
import time

# PySide2 imports

# software specific imports
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

# mca python imports
from mca.common.modifiers import decorators
from mca.common import log
from mca.common.paths import paths, project_paths
from mca.common.pyqt import messages
from mca.common.utils import fileio
from mca.mya.utils import naming, constraint, camera_utils, namespace, plugins
from mca.mya.modifiers import ma_decorators
from mca.mya.rigging import rig_utils, frag
from mca.mya.rigging.frag import cine_sequence_component, frag_rig
from mca.mya.animation import baking, time_utils
from mca.mya.cinematics import cine_sequence_nodes, cine_file_utils
from mca.mya.thirdpartytools.mocapx.lib import utils as mcpx_utils
from mca.mya.thirdpartytools.mocapx import commands as mcpx_cmds
from mca.mya.thirdpartytools.mocapx.lib import nodes as mcpx_nodes

logger = log.MCA_LOGGER


def get_shot_seq_start_time():
	"""
	Gets a start time for a shot at the end of the current shots in scene

	"""

	shots = pm.ls(type='shot')
	last_shot_end = 0
	if len(shots) > 0:
		last_shot_end = int(max([pm.shot(x, set=True, q=True) for x in shots]))
	return last_shot_end + 1


def make_shot(cine_shot):
	"""
	Makes a new shot at the end of the current shots in scene

	:param CineShotData cine_shot: Instance of CineShotData class that stores information about the shot.

	"""

	seq_start_time = get_shot_seq_start_time()
	pm.sequenceManager(ct=seq_start_time)

	new_shot = pm.shot(f'shot_{cine_shot.shot_camera}',
					   st=int(cine_shot.shot_start),
					   et=int(cine_shot.shot_end),
					   cc=cine_shot.shot_camera)
	new_shot.addAttr('sequenceNode', at='message')
	pm.shot(new_shot, e=True, shotName=cine_shot.shot_name)
	pm.shotTrack(ret=True)
	return new_shot

def get_new_shot_number():
	"""
	Gets new shot number using the last 3 characters on the string name of the shot namespaces in scene.

	"""

	cam_names = [c[-3:] for c in cmds.namespaceInfo(listOnlyNamespaces=True) if 'shot' in c]
	latest_cam_number = 10
	if cam_names:
		latest_cam = max(cam_names)
		latest_cam_number = 10 + (math.floor(int(latest_cam[-3:]) / 10) * 10)
	cam_number = f"{latest_cam_number:0=3d}"

	return cam_number


def make_new_shot(cine_seq_node, shot_number):
	"""
	Makes a new shot using information on a sequence node in the scene.

	:param CineSequenceComponent cine_seq_node: Instance of CineSequenceComponent
	:param int shot_number: New shot number.

	"""
	cine_seq_data = cine_sequence_nodes.CineSequenceData.get_cine_seq_data(cine_seq_node.pynode)

	cine_shot = create_reference_cam_cine_shot(cine_seq_data, shot_number)
	new_shot = make_shot(cine_shot)
	cine_seq_node.pynode.shots >> new_shot.sequenceNode

	return cine_seq_data


def copy_all_animation(cine_shot, new_start_time):
	"""
	Copies all animation curves in scene and pastes them at a new time.

	:param CineShotData cine_shot: Instance of CineShotData class that stores information about the shot.
	:param int new_start_time: New frame to paste the copied animation to.

	"""

	anim_curves = pm.ls(type=pm.nt.animCurve)
	new_end_time = cine_shot.end + new_start_time
	if not anim_curves:
		logger.warning(f'No animation in {cine_shot.name}')
		return
	for curve in anim_curves:
		pm.setKeyframe(curve, time=(cine_shot.start, cine_shot.end), insert=True)
		pm.copyKey(curve, time=(cine_shot.start, cine_shot.end))
		try:
			pm.setKeyframe(curve, time=(new_start_time - 1), insert=True)
			pm.pasteKey(curve, time=(new_start_time, new_end_time), option='replace')
		except RuntimeError as e:
			# Check if error was due to not having a key, in which case we do nothing. Otherwise,
			# give info about the error
			e = str(e).rstrip()
			if e in ["Nothing to paste from"]:
				pass
			else:
				logger.warning(traceback.format_exc())
				raise

	logger.info("All Done!")


def create_cine_cam(seq_name):
	"""
	References in a camera saved in a common folder and groups it

	:param str seq_name: Three letter sequence code name
	:return: Returns the referenced camera
	:rtype: pm.nt.Transform

	"""
	proj_path = project_paths.get_project_path()
	ref_cam_path = os.path.normpath(os.path.join(proj_path, 'Cinematics\\Assets\\camera\\shotCam_2point35_30fps_v1.ma'))
	cam_number = get_new_shot_number()
	cam_ref = cmds.file(os.path.normpath(ref_cam_path),
						r=True,
						type="mayaAscii",
						ns=f"{seq_name}_shot_{cam_number}")
	cam = [c for c in pm.referenceQuery(cam_ref, nodes=True) if pm.attributeQuery('focalLength', node=c, exists=True)]
	if not cam:
		logger.warning('Problem importing camera reference.')
		return
	cam = pm.PyNode(cam[0])
	if isinstance(cam, pm.nt.Camera):
		cam = cam.getParent()
	camera_grp = None
	for node in pm.ls(type=pm.nt.Transform):
		if node.hasAttr('cameraGrp'):
			camera_grp = node
			break
	if not camera_grp:
		if pm.objExists('cameras_grp'):
			camera_grp = pm.PyNode('cameras_grp')
			if not camera_grp.hasAttr('cameraGrp'):
				camera_grp.addAttr('cameraGrp', at='bool')
		else:
			camera_grp = pm.group(name='cameras_grp', em=True)
			camera_grp.addAttr('cameraGrp', at='bool')
	cam.setParent(camera_grp)

	return cam


@decorators.track_fnc
def make_cine_locators_at_sel_cmd():
	"""
	Toolbox command to create locators at current selection.

	"""

	for obj in pm.selected():
		make_cine_locator(obj)


def make_cine_locator(obj, loc_name=None):
	"""
	Creates a locator at an objects position and parents it under the layout group.

	:param pm.nt.Transform obj: Object to match
	:param str loc_name: Name to give to the locator, if None use the objects name + _locator suffix
	:return: Returns the created locator.
	:rtype: pm.nt.Transform

	"""

	if not loc_name:
		loc_name = f'{naming.get_basename(obj)}_locator'
	loc = rig_utils.create_locator_at_object(obj, label=loc_name)
	if not pm.objExists('layout_grp'):
		cmds.group(n='layout_grp', em=True)
	loc.setParent(pm.PyNode('layout_grp'))

	return loc


@decorators.track_fnc
def bake_locators_to_selection_cmd():
	"""
	Command for baking locators to selection.
	"""

	selection = pm.selected()
	start_frame, end_frame = time_utils.get_visible_range()
	bake_locators(selection, start_frame, end_frame)


def bake_locators(object_list, start_frame, end_frame):
	"""
	Bakes locators to a list of animated objects for current visible frame range.

	:param list(pm.nt.Transform) object_list: List of objects to have a baked locator created for.
	:param int start_frame: Start frame to bake.
	:param int end_frame: End frame to bake.
	:return: Returns the created locators.
	:rtype: pm.nt.Transform

	"""

	locs = []
	constraints = []

	for obj in object_list:
		loc = make_cine_locator(obj)
		loc.rename(f'{loc}_BAKED')
		locs.append(loc)
		con = constraint.parent_constraint_safe(obj, loc)
		constraints.append(con)

	baking.bake_objects(locs, bake_range=[start_frame, end_frame])
	pm.delete(constraints)
	return locs


def match_objects(child_node, parent_node):
	"""
	Matches the position of one object to the position of the second and sets a keyframe if any on snapped object.

	:param pm.nt.Transform child_node: Object to be moved.
	:param pm.nt.Transform parent_node: Object whose position we want to match.

	"""

	con = constraint.parent_constraint_safe(parent_node, child_node, mo=False)
	if pm.keyframe(child_node, q=True, kc=True):
		pm.setKeyframe(child_node)
	if con:
		pm.delete(con)
	else:
		logger.warning(f'Issue creating constraint between parent {parent_node} and child {child_node}')


def handle_shot_namespace_conflict(name):
	"""
	Creates a temp namespace if there is a conflict and puts all associated shots into it

	:param str name: Namespace to check

	"""

	if pm.namespace(ex=name):
		# name_number is the number of temp shots existent
		name_number = 1 + len([x for x in map(str, cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True))
							  if "temp_name" in x])
		temp_name = f't{name_number}_tempName_{name}'
		pm.namespace(set=':')
		pm.namespace(ren=[name, temp_name])
		associated_shots = [x for x in pm.ls(type='shot') if name in pm.shot(x, q=True, cc=True)]
		if associated_shots:
			pm.shot(associated_shots[0], e=True, sn=temp_name)


def create_cine_playblast(seq_name, shot_name, stage, time_range, cam):
	"""
	Creates a playblast and exports to cinematic folder.

	:param str seq_name: Three letter sequence code name.
	:param str shot_name: Name of the shot. Should be formatted code name_shot_shot number (ex: TST_shot_010)
	:param str stage: Stage of the sequence or shot, either layout or animation.
	:param list(int) time_range: Frame range we should playblast.
	:param pm.nt.Transform cam: Camera to use for playblast perspective.

	"""

	seq_dir = os.path.join(paths.get_cine_seq_path(), seq_name)
	# Using perspective cam as default, but having a camera or shot selected will use that one
	pb_dir = os.path.normpath(os.path.join(seq_dir, 'video', 'playblasts'))

	time_range = [int(x) for x in time_range]
	set_hud()
	pb_name = f'{shot_name}_{stage}.mp4'
	pb_file_path = os.path.join(pb_dir, pb_name)
	resolution = [860, 360] if time_range[1] - time_range[0] > 1000 else [1720, 720]
	blast_path = camera_utils.capture_and_compress_video(pb_file_path,
														 camera_node=cam,
														 time_range=time_range,
														 resolution=resolution,
														 delete_uncompressed=True,
														 background=None,
														 hud=True,
														 lighting_style='default')
	logger.info(f'Created playblast: {blast_path}')
	return blast_path

def set_hud():
	"""
	Sets up the HUD for a playblast to contain relevant information about the camera/scene

	"""

	visible_huds = [h for h in pm.headsUpDisplay(listHeadsUpDisplays=True)
				   if pm.headsUpDisplay(h, q=True, visible=True)]
	for hud in visible_huds:
		cmds.headsUpDisplay(hud, edit=True, visible=False)
	# put focal length in section 5
	cmds.headsUpDisplay('HUDFocalLength',
					  edit=True,
					  visible=True,
					  lfs='large',
					  dfs='large',
					  section=5,
					  block=1)

	# put camera name in section 7
	cmds.headsUpDisplay('HUDCameraNames',
					  edit=True,
					  visible=True,
					  lfs='large',
					  dfs='large')

	# put frame count in section 9
	cmds.headsUpDisplay('HUDCurrentFrame',
					  edit=True,
					  visible=True,
					  lfs='large',
					  dfs='large')


@decorators.track_fnc
def playblast_single_cmd():
	"""
	Command to create a playblast and export it to cinematic folder.

	"""

	current_file = os.path.normpath(cmds.file(q=True, sceneName=True))
	# Override this shot name later if we have a shot node with a shot name
	shot_name = os.path.basename(current_file).split('.')[0]
	time_range = time_utils.get_visible_range()

	selected_nodes = pm.selected()
	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	if cine_seq_node:
		seq_name = cine_seq_node.seq_name()
		stage = cine_seq_node.stage()
	else:
		split_path = current_file.split(paths.get_cine_seq_path() + '\\')[-1].split('\\')
		seq_name = split_path[0]
		stage = 'animation' if split_path[2].isdigit() else 'layout'

	if selected_nodes:
		for selected_node in selected_nodes:
			if isinstance(selected_node, pm.nt.Shot):
				shot_name = selected_node.shotName.get()
				start_time = selected_node.startFrame.get()
				end_time = selected_node.endFrame.get()
				time_range = [start_time, end_time]
				cam = selected_node.currentCamera.get()
				if not cam:
					logger.warning(f'No camera associated with shot: {selected_node}')
					continue

			elif isinstance(selected_node, pm.nt.Transform):
				if selected_node.hasAttr('focalLength'):
					cam = selected_node
				else:
					logger.warning(f'Selected node is not a shot or camera.')
					continue
				connected_shot = selected_node.getShape().message.listConnections(type=pm.nt.Shot)
				if connected_shot:
					connected_shot = connected_shot[0]
					shot_name = connected_shot.shotName.get()
					start_time = connected_shot.startFrame.get()
					end_time = connected_shot.endFrame.get()
					time_range = [start_time, end_time]
			else:
				logger.warning(f'Selected node is not a shot or camera.')
				continue
			create_cine_playblast(seq_name, shot_name, stage, time_range, cam)
	else:
		default_cam_names = ['perspShape', 'frontShape', 'sideShape', 'topShape', 'leftShape', 'bottomShape',
							 'backShape']

		cams = pm.ls(type=pm.nt.Camera)
		scene_shot = pm.ls(type=pm.nt.Shot)
		cam = None
		if scene_shot:
			shot_name = scene_shot[0].shotName.get()
			cam = scene_shot[0].currentCamera.get()
		if not cam:
			shot_cams = [x for x in cams if x.name() not in default_cam_names]
			if shot_cams:
				cam = shot_cams[0]
			else:
				cam = pm.PyNode(default_cam_names[0])
		create_cine_playblast(seq_name, shot_name, stage, time_range, cam)


@ma_decorators.keep_namespace_decorator
def playblast_sequence(cine_seq_node):
	"""
	Creates a temporary ubercam and playsblasts all shots in the sequence.

	:param CineSequenceComponent cine_seq_node: Instance of CineSequenceComponent.

	"""

	shot_list = cine_seq_node.shots()
	end_time = max([x.endFrame.get() for x in shot_list])
	start_time = min([x.startFrame.get() for x in shot_list])
	time_utils.set_timeline_range(start_time, end_time)
	namespace.set_namespace('TempUbercam')
	ubercam = camera_utils.create_mca_ubercam(shot_list)
	blast_path = create_cine_playblast(cine_seq_node.seq_name(),
						 f'{cine_seq_node.seq_name()}_Sequence_v{cine_seq_node.version_num()}',
						 cine_seq_node.stage(),
						 [int(start_time), int(end_time)],
						 ubercam)
	namespace.purge_namespace('TempUbercam')
	namespace.set_namespace('')
	return blast_path


def batch_playblast(seq_name, shot_number_list, stage):
	"""
	Goes through broken out shots of a sequence, opens latest version, and playblasts.

	:param str seq_name: Three letter sequence code name.
	:param list(str/int) shot_number_list: List of shot numbers to playblast.
	:param str stage: Stage of the sequence or shot, either layout or animation.

	"""

	sequence_dir = os.path.join(paths.get_cine_seq_path(), seq_name)
	all_shots_dir = os.path.join(sequence_dir, 'shots')

	for shot_number in shot_number_list:
		shot_dir = os.path.join(all_shots_dir, str(shot_number))
		if os.path.exists(shot_dir):
			shot_stage_dir = os.path.join(shot_dir, stage)
			if os.path.exists(shot_stage_dir):

				latest_shot_verion = cine_file_utils.get_latest_version(shot_stage_dir)
				latest_file_path = os.path.join(shot_stage_dir, latest_shot_verion)
				if os.path.exists(latest_file_path):
					cmds.file(latest_file_path, o=True, f=True)
					start_time = time_utils.get_scene_start_time()
					end_time = time_utils.get_scene_end_time()
					shot_node = pm.ls(type=pm.nt.Shot)[0]
					create_cine_playblast(seq_name,
										  shot_node.shotName.get(),
										  stage,
										  [start_time, end_time],
										  shot_node.currentCamera.get())


@decorators.track_fnc
def playblast_sequence_cmd():
	"""
	Command to playblast all shots in a sequence through an ubercam.

	"""

	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	if not cine_seq_node:
		logger.warning('No sequence node found.')
		return
	playblast_sequence(cine_seq_node)


@decorators.track_fnc
def make_new_shot_cmd():
	"""
	Command to create a new shot in a sequence.

	"""

	shot_number = get_new_shot_number()

	cine_seq_node = cine_sequence_component.find_cine_seq_component()
	if not cine_seq_node:
		logger.warning('No sequence node found.')
		return

	make_new_shot(cine_seq_node, shot_number)


def create_reference_cam_cine_shot(cine_seq_data, shot_number):
	"""
	Import reference cam and creates new CineShot class instance

	:param CineSequenceData cine_seq_data: Instance of CineSequenceData class that stores information about the sequence.
	:param int/str shot_number: Number of the shot to create.
	:return: Returns an instance of CineShotData class that stores information about the shot.
	:rtype: CineShotData

	"""

	start = cmds.playbackOptions(query=True, minTime=True)
	end = cmds.playbackOptions(query=True, maxTime=True)
	cam = create_cine_cam(cine_seq_data.seq_name)
	shot_name = f'{cine_seq_data.seq_name}_shot_{int(shot_number):0=3d}'
	chars = frag_rig.get_frag_rigs()

	cine_shot = cine_sequence_nodes.CineShotData.create(shot_number,
														cine_seq_data.data,
														shot_name=shot_name,
														shot_camera=cam,
														shot_start=start,
														shot_end=end,
														shot_stage=cine_seq_data.stage,
														shot_version=1,
														chars=chars)

	return cine_shot


def rename_shot(shot_data, new_shot_name):
	"""
	Renames a shot by updating the shot name attr and namespace then reloading the referenced camera in that NS.

	:param CineShotData shot_data: Data class that stores information about the shot to rename.
	:param str new_shot_name: New name for the shot.
	:return: Updated data class that stores information about the renamed shot.
	:rtype: CineShotData

	"""

	if pm.objExists(shot_data.node_name):
		old_shot_cam_name = shot_data.shot_camera
		shot_node = pm.PyNode(shot_data.node_name)
		shot_node.shotName.set(new_shot_name)
		old_ns = namespace.get_namespace(old_shot_cam_name, check_node=False)

		if pm.namespace(exists=old_ns):
			ns_nodes = namespace.get_all_nodes_in_namespace(old_ns)
			if pm.namespace(exists=new_shot_name):
				list(map(lambda x: namespace.move_node_to_namespace(x, new_shot_name), ns_nodes))
			else:
				pm.namespace(ren=[old_ns, new_shot_name])

			ns_nodes = namespace.get_all_nodes_in_namespace(new_shot_name)
			real_ns_nodes = [x for x in ns_nodes if not pm.objExists(x)]
			for ns_node in real_ns_nodes:
				if ns_node.isReferenced():
					ref_path = pm.referenceQuery(ns_node, filename=True)
					if ref_path:
						ref_node = pm.FileReference(ref_path)
						cmds.file(ref_path, loadReference=ref_node)

			new_shot_cam = old_shot_cam_name.replace(old_ns, new_shot_name)
			shot_data.shot_camera = new_shot_cam
		shot_data.shot_name = new_shot_name

	return shot_data

def load_mocap(mocap_path, bake_anim=False):
	"""
	Loads MocapX data onto  head rig in scene.

	:param str mocap_path: Path to MocapX data file.
	:param bool bake_anim: Whether or not to bake animation.

	"""

	t1 = time.time()

	head_rig = frag_rig.get_frag_rigs()
	if not head_rig:
		return
	head_rig = head_rig[0]

	plugin_loaded = plugins.load_plugin('mocapx_plugin')
	if not plugin_loaded:
		messages.warning_message('Load Face Mocap', 'MocapX plugin not found.')
		logger.warning('MocapX plugin not found.')
		return

	clip_reader = mcpx_cmds.create_clipreader(adapter_name=None)
	mcpx_utils.clipreader_load_clip(clip_reader, mocap_path)
	for attr_name in mcpx_nodes.list_attrs(clip_reader, connectable=True):
		found = mcpx_nodes.find_pose_nodes(attr_name)
		if found:
			found = list(filter((lambda el: ':' not in el), found))
			pose_node = found[0]
			possible_source = clip_reader + "." + attr_name

			if mcpx_utils.is_attr_type_valid(possible_source):
				mcpx_nodes.connect_attrs(possible_source, pose_node + ".weight", verbose=True)

	neck_component = head_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')[0]
	head_flag = neck_component.end_flag
	for attr in ['X', 'Y', 'Z']:
		pm.connectAttr(f'{clip_reader}.transformRotate{attr}', f'{head_flag}.rotate.rotate{attr}')

	head_flags = head_rig.get_flags()
	if bake_anim:
		last_frame = get_last_pose_change(100, 3000)
		if last_frame == 100:
			last_frame = get_last_pose_change(0, 100)
		baking.bake_objects(head_flags, bake_range=[0, last_frame])

	t2 = time.time()
	logger.info(f'Face Mocap loaded in {round(t2-t1)} seconds.')


def get_last_pose_change(start_frame, end_frame):
	"""
	Finds the last frame with a pose change in the given range.

	:param int start_frame: Frame to start searching from.
	:param int end_frame: Frame to stop searching at.
	:return: Returns the last frame with a pose change in the given range.
	:rtype: int

	"""

	poses = pm.ls(type='MCPXPose')
	addition_node = pm.createNode('plusMinusAverage')
	for x, pose in enumerate(poses):
		pm.connectAttr(f'{pose}.weight', f'{addition_node}.input1D[{x}]')
	last_val = 0
	for x in range(start_frame, 3000):
		pm.currentTime(x)
		val = addition_node.output1D.get()
		if val != last_val:
			last_val = val
			end_frame = x
		elif x == end_frame + 10 and val == last_val:
			break
	pm.delete(addition_node)

	return end_frame


def load_sounds(sounds_path):
	"""
	Imports audio from a path to audio file then sets the timeline range to audio length and sets the playback slider.
	:param str sounds_path: Path to audio file.
	:return: Returns the sound node that was created.
	:rtype: pm.nt.Audio

	"""

	sound_node_name = pm.sound(file=sounds_path)
	pb_slider = mel.eval('$tmpVar=$gPlayBackSlider')
	pm.timeControl(pb_slider, edit=True, sound=sound_node_name)
	sound_node = pm.PyNode(sound_node_name)
	start_time = round(sound_node.sourceStart.get())
	end_time = round(sound_node.sourceEnd.get())
	time_utils.set_timeline_range(start_time, end_time)

	return sound_node


def load_facial_mocap(sounds_path, mocap_path, bake_anim=True):
	"""
	Loads facial mocap data onto head rig in scene and sets save name.
	:param str sounds_path: Path to audio file.
	:param str mocap_path: Path to facial mocap data file.
	:param bool bake_anim: Whether or not to bake animation.
	:return: Returns the sound node that was created.
	:rtype: pm.nt.Audio

	"""

	load_mocap(mocap_path[0], bake_anim=bake_anim)
	sound_node = load_sounds(sounds_path[0])
	sound_file_name = os.path.basename(sounds_path[0]).split('.wav')[0]
	save_file_name = f'Anim{sound_file_name.split(sound_file_name[:2])[-1]}'
	current_cdw_path = sounds_path[0].split('Audio')[0]
	fileio.touch_path(f'{os.path.join(current_cdw_path, save_file_name)}.ma')
	cmds.file(rn=os.path.join(current_cdw_path, save_file_name))

	return sound_node
