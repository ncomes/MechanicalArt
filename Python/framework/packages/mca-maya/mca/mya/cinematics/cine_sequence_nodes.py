#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class for handling Cinematic Sequence Nodes
"""

# python imports
import os
# PySide2 imports
# software specific imports
import maya.cmds as cmds
import pymel.core as pm
# mca python imports
from mca.common.utils import dict_utils
from mca.common.textio import jsonio
from mca.mya.rigging.frag import frag_rig


CINE_SEQ_DATA = {'seq_name': '',
				 'scene_name': '',
				 'version_num': '',
				 'stage': '',
				 'shots': {}}

CINE_SHOT_DATA = {'shot_number': {},
				  'shot_name': {},
				  'shot_camera': {},
				  'shot_start': {},
				  'shot_end': {},
				  'shot_stage': {},
				  'shot_version': {},
				  'chars': {},
                  'node_name': {},
				  'props': {}}

CINE_SEQ_NODE_ATTRS = ['sequenceName', 'stage', 'shotNumber', 'sceneName', 'isShotFile', 'versionNumber', 'notes']

class CineSequenceData:
	# python class for the mya node that lives in scene and holds information
	def __init__(self, data=None):
		data = data_check(CINE_SEQ_DATA, data)
		self.data = dict_utils.ObjectDict(data)
	# -----------------------------------------------------------------------()
	@classmethod
	def create(cls, seq_name, version_num, stage, scene_name='', shots=None):
		seq_data = {'seq_name': seq_name,
						 'scene_name': scene_name,
						 'version_num': version_num,
						 'stage': stage,
						 'shots': shots or {}}

		return cls(data=seq_data)


	@classmethod
	def get_cine_seq_data(cls, maya_node):
		"""
		Gets data from Sequence Node in Maya and creates instance of CineSequenceData

		:param pm.nt.Transform maya_node: Sequence (group) node in Maya
		:return: Returns an instance of CineSequenceData
		:rtype: CineSequenceData
		"""

		seq_name = maya_node.sequenceName.get()
		version_num = get_version_number()
		stage = maya_node.stage.get()
		if stage != 'layout' and stage != 'animation':
			if stage == 0:
				stage = 'layout'
			elif stage == 1 or stage == 2:
				stage = 'animation'
		scene_name = maya_node.sceneName.get()
		seq_data = {'seq_name': seq_name,
					'scene_name': scene_name,
					'version_num': version_num,
					'stage': stage,
					'shots': {}}
		return cls(data=seq_data)

	@property
	def seq_name(self):
		return self.data.get('seq_name')

	@seq_name.setter
	def seq_name(self, value):
		self.data.seq_name = value

	@property
	def scene_name(self):
		return self.data.get('scene_name')

	@scene_name.setter
	def scene_name(self, value):
		self.data.scene_name = value

	@property
	def version_num(self):
		return self.data.get('version_num')

	@version_num.setter
	def version_num(self, value):
		self.data.version_num = value

	@property
	def stage(self):
		return self.data.get('stage')

	@stage.setter
	def stage(self, value):
		self.data.stage = value

	@property
	def shots(self):
		return self.data.get('shots')

	@shots.setter
	def shots(self, value):
		self.data.shots = value

	@classmethod
	def load(cls, file_path):
		"""
		Loads a json file and Returns the instance of the class.

		:param str file_path: Full path to the file.
		:return: Returns the instance of the class SourceFaceData.
		:rtype: SourceFaceData
		"""

		data = jsonio.read_json_file(file_path)
		return cls(data)

	def export(self, file_path):
		"""
		Exports the data to a json file.

		:param str file_path: Full path to the file.
		"""

		jsonio.write_to_json_file(data=self.data, filename=file_path)

	def fill_cine_shot_data(self):
		"""
		Fills the CineShotData class with data from the Shot nodes in the scene.
		:param seq_node:
		:return:
		"""
		all_maya_shots = pm.ls(type=pm.nt.Shot)
		for maya_node in all_maya_shots:
			CineShotData.get_shot_data_from_node(maya_node, self)


class CineShotData(CineSequenceData):
	def __init__(self, shot_number, data=None):
		self.shot_number = shot_number
		data = self.data_check(shot_number, data)
		self.data = dict_utils.ObjectDict(data) if data else dict_utils.ObjectDict()
		super(CineShotData, self).__init__(self.data)

	@classmethod
	def create(cls, shot_number,
			   data,
			   shot_name=None,
			   shot_camera=None,
			   shot_start=None,
			   shot_end=None,
			   shot_stage=None,
			   shot_version=None,
			   chars=None,
	           node_name=None,
			   props=None):
		"""
		Creates an initial dict for setting source data.

		:rtype: dictionary
		"""
		data['shots'].setdefault(shot_number, CINE_SHOT_DATA)
		data['shots'].update({shot_number: {'shot_number': shot_number,
		                                    'shot_name': shot_name or {},
		                                    'shot_camera': shot_camera or {},
		                                    'shot_start': shot_start,
		                                    'shot_end': shot_end or {},
		                                    'shot_stage': shot_stage or {},
		                                    'shot_version': shot_version or {},
		                                    'chars': chars or {},
											'node_name': node_name or {},
											'props': props or {}}})

		return cls(shot_number=shot_number, data=data)

	@classmethod
	def get_shot_data_from_node(cls, maya_node, seq_node):
		shot_name = maya_node.shotName.get()
		shot_number = shot_name[-3:]
		shot_camera = maya_node.currentCamera.get()
		if shot_camera:
			shot_camera = shot_camera.name()
		shot_start = int(maya_node.startFrame.get())
		shot_end = int(maya_node.endFrame.get())
		shot_chars = frag_rig.get_frag_rigs()
		node_name = maya_node.name()

		props = None

		stage = get_stage_from_path()
		shot_version = get_version_number()
		return cls(shot_number, seq_node.data).create(shot_number, seq_node.data,
																	shot_name, shot_camera, shot_start,
																	shot_end, stage, shot_version,
																	shot_chars, node_name, props)

	@staticmethod
	def data_check(shot_number, data):
		"""
		Checks to make sure the dictionary has all base keys and values.

		:param str region_name: Name of the region.
		:param dict data: Dictionary of all the face data.
		:return: Dictionary of all the face data.
		:rtype: Dictionary
		"""

		if not data:
			data = CINE_SHOT_DATA
		if shot_number not in data:
			data['shots'].setdefault(shot_number, CINE_SHOT_DATA)
		return data

	@property
	def shot_data(self):
		return self.data.get('shots').get(self.shot_number)

	@shot_data.setter
	def shot_data(self, value):
		self.data.shots[self.shot_number] = value

	@property
	def shot_name(self):
		return self.shot_data.get('shot_name')

	@shot_name.setter
	def shot_name(self, value):
		self.shot_data['shot_name'] = value

	@property
	def shot_camera(self):
		return self.shot_data.get('shot_camera')

	@shot_camera.setter
	def shot_camera(self, value):
		self.shot_data['shot_camera'] = value

	@property
	def shot_start(self):
		return self.shot_data.get('shot_start')

	@shot_start.setter
	def shot_start(self, value):
		self.shot_data['shot_start'] = value

	@property
	def shot_end(self):
		return self.shot_data.get('shot_end')

	@shot_end.setter
	def shot_end(self, value):
		self.shot_data['shot_end'] = value

	@property
	def shot_stage(self):
		return self.shot_data.get('shot_stage')

	@shot_stage.setter
	def shot_stage(self, value):
		self.shot_data['shot_stage'] = value

	@property
	def shot_version(self):
		return self.shot_data.get('shot_version')

	@shot_version.setter
	def shot_version(self, value):
		self.shot_data['shot_version'] = value

	@property
	def chars(self):
		return self.shot_data.get('chars')

	@chars.setter
	def chars(self, value):
		self.shot_data['chars'] = value

	@property
	def props(self):
		return self.shot_data.get('props')

	@props.setter
	def props(self, value):
		self.shot_data['props'] = value

	@property
	def node_name(self):
		return self.shot_data.get('node_name')

	@node_name.setter
	def node_name(self, value):
		self.shot_data['node_name'] = value

	@classmethod
	def load(cls, file_path, shot_number):
		"""
		Loads a json file and Returns the instance of the class.

		:param str file_path: Full path to the file.
		:param str region_name: Name of the region.
		:return: Returns the instance of the class SourceFaceData.
		:rtype: SourceFaceData
		"""

		data = jsonio.read_json_file(file_path)
		return cls(shot_number=shot_number, data=data)


def get_stage_from_path():
	"""
	Gets stage from file path is possible, returns None if not.

	:return: Stage name
	:rtype: str or None

	"""
	current_file_path = cmds.file(q=True, sceneName=True)
	stages = ['layout', 'animation']
	stage = [x for x in stages if x in current_file_path]
	if stage:
		stage = stage[0]
		return stage
	else:
		return None


def get_version_number():
	"""
	Gets version number from file name if possible, if not uses data on sequence node provided.
	:param pm.nt.Transform maya_node: Sequence (group) node in Maya
	:return: Returns the version number of the scene.
	:rtype: int
	"""

	f_name = cmds.file(q=True, sn=True, shn=True)
	no_ext = os.path.splitext(f_name)[0]
	v_number = no_ext[-3:]
	version_num = 0
	try:
		version_num = int(v_number)
	except ValueError as e:
		return None

	return version_num


def data_check(empty_data, existing_data=None):
	"""
	Checks a dictionary against another and adds missing keys.

	:param dict empty_data: A default set of values for a dictionary.
	:param dict existing_data: a dictionary with existing data.
	:return: Returns a combined dictionary with out overwriting existing data.
	:rtype: dictionary
	"""

	if not existing_data:
		existing_data = {}

	# Compare the 2 dictionaries and add missing keys
	updated_data = dict(list(empty_data.items()) + list(existing_data.items()))

	# Add missing nested keys
	for key, value in empty_data.items():
		if isinstance(value, dict) and value.keys():
			sub_data = dict(list(empty_data[key].items()) + list(updated_data[key].items()))
			updated_data[key] = sub_data
	return dict_utils.ObjectDict(updated_data)

