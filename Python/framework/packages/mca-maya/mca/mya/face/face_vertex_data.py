#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Face vertex handlers.
"""

# python imports
import json
import os
from collections import deque

# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

#  python imports
from mca.common.utils import pyutils
from mca.mya.modifiers import ma_decorators
from mca.mya.modeling import vert_utils
from mca.common.tools.progressbar import progressbar_ui


class SourceVertexData:
	def __init__(self, data):
		self.data = pyutils.ObjectDict(data)

	@staticmethod
	def build_vertex_name(mesh_name, vertex_number):
		"""
		Builds the vertex name.
		
		:param str mesh_name: Name of the mesh.
		:param int/str vertex_number: The vertex number.
		:return: Returns the full name of a vertex.
		:rtype: str
		"""

		return '{0}.vtx[{1}]'.format(mesh_name, vertex_number)

	def export(self, file_path, data=None):
		"""
		Exports a json file for face vertex data.
		
		:param str file_path: The full path of the file being created.
		:param dictionary data: Vertex data that is being exported.
		"""

		if not data:
			data = self.data
		if '.json' not in file_path:
			file_path = os.path.join(file_path + '.json')
		with open(file_path, 'w') as fp:
			json.dump(data, fp, indent=2)

	@classmethod
	def load(cls, file_path):
		"""
		Loads the vertex data from a json file.
		
		:param str file_path: The full path of the json file.
		:return: Returns the class instance.
		:rtype: SourceVertexData
		"""

		if '.json' not in file_path:
			file_path = os.path.join(file_path + '.json')
		if not os.path.exists(file_path):
			return
		with open(file_path, 'r') as f:
			data = json.load(f)
			if not data:
				raise RuntimeError('Import failed. No data was imported')
		return cls(data)

	def export_data_section(self, data_section, file_path, data_section_name):
		"""
		
		Exports json data for face vertices in a specific data section.
		:param dictionary data_section: Dictionary with listed vertices.
		:param str file_path: File name and path.
		:param str data_section_name: Name of the top key to export.
		"""

		data = self.load(file_path)

		data[data_section_name] = data_section
		self.export(file_path, data)

	def select_vertices(self, mesh_name, vert_list):
		"""
		Selects the saved vertex position on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		:param list(str) vert_list: List of vertices.
		"""

		vert_list = list(map(lambda x: self.build_vertex_name(mesh_name, x), vert_list))

		cmds.select(mesh_name, vert_list)
		cmds.selectMode(co=True)

	@classmethod
	def load_data_section(cls, file_path, data_section_name):
		"""
		Loads a data a specific data section.
		
		:param str file_path: File name and path.
		:param str data_section_name: Name of the key to return.
		:return: Returns a dictionary with mapped vertices.
		:rtype: dictionary
		"""

		data = SourceVertexData.load(file_path)
		return data.data[data_section_name]

	@classmethod
	def load_vertex_data(cls, file_path, mesh_region):
		data = SourceVertexData.load(file_path)
		regions_data = data.data.get('regions')
		mesh_region_data = regions_data.get(mesh_region)
		region_vertex_data = mesh_region_data.get('vertex_data')
		return cls(region_vertex_data)

	@classmethod
	def load_default_regions_data(cls, file_path, mesh_region):
		data = SourceVertexData.load(file_path)
		regions_data = data.data.get('regions')
		mesh_region_data = regions_data.get(mesh_region)
		region_vertex_data = mesh_region_data.get('vertex_data')
		face_region_vertex_data = region_vertex_data.get('vertex_default_regions')
		return cls(face_region_vertex_data)


class RegionVertices(SourceVertexData):
	def __init__(self, data):
		self.data = pyutils.ObjectDict(data)
		super(RegionVertices, self).__init__(data)

	@classmethod
	def create(cls, neck_verts=None,
				jaw_verts=None,
				brows_verts=None,
				mouth_bag_verts=None,
				mouth_bag_top_verts=None,
				mouth_bag_bottom_verts=None,
				deform_area=None,
				non_deform=None,
			   	lips_verts=None):
		"""
		Creates a dictionary for mapping vertex regions of the face.
		
		:param list(str) neck_verts: A list of vertices that define the neck region.
		:param list(str) jaw_verts: A list of vertices that define the jaw region.
		:param list(str) brows_verts: A list of vertices that define the brow region.
		:param list(str) mouth_bag_verts: A list of vertices that define the whole mouth bag region.
		:param list(str) mouth_bag_top_verts: A list of vertices that define the top of the mouth bag region.
		:param list(str) mouth_bag_bottom_verts: A list of vertices that define the bottom of the mouth bag region.
		:param list(str) deform_area: A list of vertices that define the deformable region.
		:param list(str) non_deform: A list of vertices that define the non-deformable region.
		:return: Returns the class instance for the data.
		:rtype: RegionVertices
		"""

		# ToDo ncomes: this is not complete yet.  Should pass in a list for each and build the dictionary.
		data = {'neck': neck_verts,
				'jaw': jaw_verts,
				'brows': brows_verts,
				'mouth_bag_verts': mouth_bag_verts,
				'mouth_bag_top': mouth_bag_top_verts,
				'mouth_bag_bottom': mouth_bag_bottom_verts,
				'deform_area': deform_area,
				'non_deform': non_deform,
				'lips_verts': lips_verts}
		return cls(data)

	@property
	def full_mesh(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['full_mesh']

	@full_mesh.setter
	def full_mesh(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'full_mesh', reset=True)

	def add_full_mesh(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'full_mesh')

	def select_full_mesh(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.full_mesh.keys()))

	@property
	def non_deform(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['non_deform']

	@non_deform.setter
	def non_deform(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'non_deform', reset=True)

	def add_non_deform(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'non_deform')

	def select_non_deform(self, mesh_name):
		"""
		Selects the stored vertices.
		
		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.non_deform.keys()))

	@property
	def brows(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['brows']

	@brows.setter
	def brows(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'brows', reset=True)

	def add_brows(self, vert_list):
		"""
		Adds a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'brows')

	def select_brows(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.brows.keys()))

	@property
	def jaw(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('jaw', None)

	@jaw.setter
	def jaw(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'jaw', reset=True)

	def add_jaw(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'jaw')

	def select_jaw(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.jaw.keys()))

	@property
	def neck(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('neck', None)

	@neck.setter
	def neck(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'neck', reset=True)

	def add_neck(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'neck')

	def select_neck(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.neck.keys()))

	@property
	def mouth_bag(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('mouth_bag', None)

	@mouth_bag.setter
	def mouth_bag(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag', reset=True)

	def add_mouth_bag(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag')

	def select_mouth_bag(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.mouth_bag.keys()))

	@property
	def mouth_bag_top(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('mouth_bag_top', None)

	@mouth_bag_top.setter
	def mouth_bag_top(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag_top', reset=True)

	def add_mouth_bag_top(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag_top')

	def select_mouth_bag_top(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.mouth_bag_top.keys()))

	@property
	def mouth_bag_bottom(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('mouth_bag_bottom', None)

	@mouth_bag_bottom.setter
	def mouth_bag_bottom(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag_bottom', reset=True)

	def add_mouth_bag_bottom(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'mouth_bag_bottom')

	def select_mouth_bag_bottom(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.mouth_bag_bottom.keys()))

	@property
	def deform_area(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.
		
		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('deform_area', None)

	@deform_area.setter
	def deform_area(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.
		
		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'deform_area', reset=True)

	def add_deform_area(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'deform_area')

	def select_deform_area(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.deform_area.keys()))

	@property
	def lips(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data.get('lips', None)

	@lips.setter
	def lips(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'lips', reset=True)

	def add_lips(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'lips')

	def select_lips(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.lips.keys()))

	@property
	def left_brow(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['left_brow']

	@left_brow.setter
	def left_brow(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'left_brow', reset=True)

	def add_left_brow(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'left_brow')

	def select_left_brow(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.left_brow.keys()))

	@property
	def right_brow(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['right_brow']

	@right_brow.setter
	def right_brow(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_brow', reset=True)

	def add_right_brow(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_brow')

	def select_right_brow(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.right_brow.keys()))

	@property
	def left_eye(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['left_eye']

	@left_eye.setter
	def left_eye(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'left_eye', reset=True)

	def add_left_eye(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'left_eye')

	def select_left_eye(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.left_eye.keys()))

	@property
	def right_eye(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['right_eye']

	@right_eye.setter
	def right_eye(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_eye', reset=True)

	def add_right_eye(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_eye')

	def select_right_eye(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.right_eye.keys()))

	@property
	def left_cheek(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['left_cheek']

	@left_cheek.setter
	def left_cheek(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'left_cheek', reset=True)

	def add_left_cheek(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_eye')

	def select_left_cheek(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.left_cheek.keys()))

	@property
	def right_cheek(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['right_cheek']

	@right_cheek.setter
	def right_cheek(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_cheek', reset=True)

	def add_right_cheek(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'right_cheek')

	def select_right_cheek(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.right_cheek.keys()))
	@property
	def chin(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['chin']

	@chin.setter
	def chin(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'chin', reset=True)

	def add_chin(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'chin')

	def select_chin(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.chin.keys()))

	@property
	def nose(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['nose']

	@nose.setter
	def nose(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'nose', reset=True)

	def add_nose(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'chin')

	def select_nose(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.nose.keys()))

	@property
	def outer_mouth(self):
		"""
		Returns a dictionary of vertices that define a region and the local space position.

		:return: Returns a dictionary of vertices that define a region and the local space position.
		:rtype: dictionary
		"""

		return self.data['outer_mouth']

	@outer_mouth.setter
	def outer_mouth(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'outer_mouth', reset=True)

	def add_outer_mouth(self, vert_list):
		"""
		Sets a dictionary of vertices that define a region and the local space position.

		:param str vert_list: List of vertices.  Should be full name.
		"""

		self.add_vertices(vert_list, 'outer_mouth')

	def select_outer_mouth(self, mesh_name):
		"""
		Selects the stored vertices.

		:param str mesh_name: name of the mesh.
		"""

		self.select_vertices(mesh_name=mesh_name, vert_list=list(self.outer_mouth.keys()))

	def add_vertices(self, vert_list, str_value, reset=False):
		"""
		Adds a dictionary of vertices that define a region and the local space position.
		
		:param list(str) vert_list: List of vertices.
		:param str str_value: Name of the region.
		"""

		if reset:
			self.data[str_value] = {}

		vert_list = cmds.ls(vert_list, fl=True)
		for vert in vert_list:
			str_vert = vert_utils.get_vertices_as_numbers(vert, as_string=True)[0]
			self.data[str_value][str_vert] = cmds.xform(vert, q=True, t=True)

	def set_vertices(self, mesh_name, vert_list, positions):
		"""
		Sets the saved vertex position on a mesh.
		
		:param str mesh_name: Name of the mesh that the vertices will be set.
		:param list(str) vert_list: List of vertices.
		:param list(vector) positions: Local position of the of the listed vertices.
		"""

		vert_list = list(map(lambda x: self.build_vertex_name(mesh_name, x), vert_list))
		for x in range(len(vert_list)):
			position = positions[x]
			cmds.xform(vert_list[x], t=(position[0], position[1], position[2]))

	def set_non_deform(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.
		
		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.non_deform)
		positions = list(self.non_deform.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_mouth_bag(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.
		
		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.mouth_bag)
		positions = list(self.mouth_bag.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_mouth_bag_top(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.mouth_bag_top)
		positions = list(self.mouth_bag_top.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_mouth_bag_bottom(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.mouth_bag_bottom)
		positions = list(self.mouth_bag_bottom.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_brows(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.brows)
		positions = list(self.brows.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_jaw(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.jaw)
		positions = list(self.jaw.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_neck(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.neck)
		positions = list(self.neck.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_deform_area(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.deform_area)
		positions = list(self.deform_area.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_lips(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.lips)
		positions = list(self.lips.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_full_mesh(self, mesh_name):
		"""
		Sets the saved vertex position for a region on a mesh.

		:param str mesh_name: Name of the mesh that the vertices will be set.
		"""

		vert_list = list(self.full_mesh)
		positions = list(self.full_mesh.values())
		self.set_vertices(mesh_name, vert_list, positions)

	def set_selected_vertices(self, mesh_name, vert_list):
		"""
		
		:param str mesh_name: Name of the mesh that the vertices will be set.
		
		:param list(str) vert_list: list of vertices to set
		:return:
		"""

		vertices = vert_utils.get_vertices_as_numbers(vert_list, as_string=True)
		positions = []
		for vert in vertices:
			positions.append(self.full_mesh[vert])
		self.set_vertices(mesh_name, vertices, positions)


#################################
# Vertex Mirroring
#################################
class SourceVertexMirror(SourceVertexData):
	def __init__(self, data=None):
		self.data = {}
		if data:
			self.data = data

		super(SourceVertexMirror, self).__init__(data)

	@classmethod
	def create(cls, left, middle):
		"""
		Creates the vertex mirror data.

		:param string list[str] left: List of left side vertices. String numbers only..
		:param string list[str] middle: List of middle vertices. String numbers only..
		:return Returns an instance of the class.
		:rtype: SourceFaceVertexMirror
		"""

		right = vert_utils.get_opposite_vertices(left)
		right = list(map(lambda x: str(x), right))

		data = {'left': {}, 'mirror_map': {}, 'right': {}}

		if any('.vtx' in str(string) for string in left):
			left = list(map(lambda x: str(x), left))
			left = vert_utils.get_vertices_as_numbers(left, as_string=True)
		if any('.vtx' in str(string) for string in right):
			right = list(map(lambda x: str(x), right))
			right = vert_utils.get_vertices_as_numbers(right, as_string=True)
		if any('.vtx' in str(string) for string in middle):
			middle = list(map(lambda x: str(x), middle))
			middle = vert_utils.get_vertices_as_numbers(middle, as_string=True)

		for x in range(len(left)):
			data['left'][left[x]] = right[x]
			data['mirror_map'][left[x]] = right[x]
			data['right'][right[x]] = left[x]
			data['mirror_map'][right[x]] = left[x]

		data['middle'] = middle
		return cls(data)

	@classmethod
	def create_all(cls, left, right, middle):
		"""
		Creates the vertex mirror data.
		
		:param string list[str] left: List of left side vertices. String numbers only..
		:param string list[str] right: List of right side vertices. String numbers only..
		:param string list[str] middle: List of middle vertices. String numbers only..
		:return Returns an instance of the class.
		:rtype: SourceFaceVertexMirror
		"""

		data = {'left': {}, 'mirror_map': {}, 'right': {}}

		if any('.vtx' in str(string) for string in left):
			left = list(map(lambda x: str(x), left))
			left = vert_utils.get_vertices_as_numbers(left, as_string=True)
		if any('.vtx' in str(string) for string in right):
			right = list(map(lambda x: str(x), right))
			right = vert_utils.get_vertices_as_numbers(right, as_string=True)
		if any('.vtx' in str(string) for string in middle):
			middle = list(map(lambda x: str(x), middle))
			middle = vert_utils.get_vertices_as_numbers(middle, as_string=True)

		for x in range(len(left)):
			data['left'][left[x]] = right[x]
			data['mirror_map'][left[x]] = right[x]
			data['right'][right[x]] = left[x]
			data['mirror_map'][right[x]] = left[x]

		data['middle'] = middle
		return cls(data)

	def data_check(self):
		"""
		Makes sure the dictionary is set up correctly.
		"""

		if not self.data or not isinstance(self.data, dict):
			data = {}
		if not 'left' in self.data:
			self.data['left'] = {}
		if not 'mirror_map' in self.data:
			self.data['mirror_map'] = {}
		if not 'right' in self.data:
			self.data['right'] = {}
		self.data = pyutils.ObjectDict(self.data)

	@property
	def left(self):
		"""
		Returns a list of all the left vertices.  String numbers only..
		
		:return list: Returns a list of all the left vertices.  String numbers only..
		"""

		return self.data.get('left', None)

	@left.setter
	def left(self, vertices):
		"""
		Sets a list of all the left vertices.  String numbers only..
		
		:param list(str) vertices: a list of all the left vertices.  String numbers only..
		"""

		self.data.update({'left': vertices})

	@property
	def right(self):
		"""
		Returns a list of all the right vertices.  String numbers only..
		
		:return list(str): Returns a list of all the left vertices.  String numbers only..
		"""

		return self.data.get('right', None)

	@right.setter
	def right(self, vertices):
		"""
		Sets a list of all the right vertices.  String numbers only..
		
		:param list(str) vertices: a list of all the right vertices.  String numbers only..
		"""

		self.data.update({'right': vertices})

	@property
	def middle(self):
		"""
		Returns a list of all the middle vertices.  String numbers only..
		
		:return list(str): Returns a list of all the middle vertices.  String numbers only..
		"""

		return self.data.get('middle', None)

	@middle.setter
	def middle(self, vertices):
		"""
		Sets a list of all the middle vertices.  String numbers only.
		
		:param list(str) vertices: Sets a list of all the middle vertices.  String numbers only..
		"""

		self.data.update({'middle': vertices})

	@property
	def mirror_map(self):
		"""
		Returns a list of all the left and right vertices.  String numbers only.
		
		:return list(str): Returns a list of all the left and right vertices.  String numbers only.
		"""

		return self.data.get('mirror_map', None)

	@mirror_map.setter
	def mirror_map(self, vertices):
		"""
		Sets a list of all the left and right vertices.  String numbers only.
		
		:param list(str) vertices: a list of all the left and right vertices.  String numbers only..
		:return:
		"""

		self.data.update({'mirror_map': vertices})

	def get_left_full_name(self, mesh_name):
		"""
		Returns the full vertex name.
		
		:param string mesh_name: name of the mesh.
		:return list(str): List of left vertices.
		"""

		return list(map(lambda x: self.build_vertex_name(mesh_name, x), self.left))

	def get_right_full_name(self, mesh_name):
		"""
		Returns the full vertex name.
		
		:param string mesh_name: name of the mesh.
		:return list(str): List of right vertices.
		"""

		# return map(lambda x: mesh_name+'.vtx['+x+']', self.right)
		return list(map(lambda x: self.build_vertex_name(mesh_name, x), self.right))

	def get_middle_full_name(self, mesh_name):
		"""
		Returns the full vertex name.
		
		:param string mesh_name: name of the mesh.
		:return List: List of vertices.
		"""

		return list(map(lambda x: self.build_vertex_name(mesh_name, x), self.middle))

	@ma_decorators.undo_decorator
	def mirror_vertices(self, mesh, vertices, axis=(-1, 1, 1), world=False):
		"""
		Mirrors selected vertices on a mesh.
		
		:param str mesh: Name of the mesh that will be mirrored.
		:param list(str) vertices: List of vertices to be mirrored.
		:param vector axis: The axis it will be mirrored.
		:param bool world: If True, the vertices will be mirrored in world space, else in local space.
		"""

		vert_utils.mirror_vertices(mesh, self.mirror_map, vertices, axis=axis, world=world)

	def mirror_left_to_right(self, mesh_name):
		"""
		Mirrors Left Vertices to the right side.
		
		:param string mesh_name: name of the mesh.
		"""

		left_list = self.get_left_full_name(mesh_name)
		self.mirror_vertices(mesh_name, left_list)

	def mirror_right_to_left(self, mesh_name):
		"""
		Mirrors Right Vertices to the left side.
		
		:param string mesh_name: name of the mesh.
		"""

		right_list = self.get_right_full_name(mesh_name)
		self.mirror_vertices(mesh_name, right_list)

	def mirror_mesh(self, mesh_name, axis=(-1, 1, 1), world=False):
		"""
		Mirrors a full mapped mesh.
		
		:param str mesh_name: Name of the mesh that will be mirrored.
		:param vector axis: The axis it will be mirrored.
		:param bool world: If True, the vertices will be mirrored in world space, else in local space.
		"""

		left = list(self.left.keys())
		right = list(self.left.values())

		vert_utils.mirror_mesh(left, right, self.middle, mesh_name, axis=axis, world=world)


#################################
# Eye Shelf
#################################
# ToDo separate the top_bottom(blinks) and front_back(eye shelf)
class SourceFaceEyelashShelf(SourceVertexData):
	"""
	Eyelash Shelf is the set of vertices that circle the eye.  They are the last two edge loops and should form a
	shelf around the eye.  The last edge loop should be directly behind and inline with the 2nd to last edge loop
	making a shelf.
	"""

	def __init__(self, data=None):
		"""
		This is a dictionary of the vertices around the eyelid shelf, string String numbers only..
		The mesh info should not be included.
		{front_back: {NAME_OR_SIDE: List(str) of vertices}}
		{top_bottom: {NAME_OR_SIDE: List(str) of vertices}}
		
		:param dictionary data: dictionary of the vertices around the eyelid shelf
		"""

		self.data = data
		self.data_check()
		super(SourceFaceEyelashShelf, self).__init__(self.data)

	def data_check(self):
		"""
		Makes sure the dictionary is set up correctly.
		
		"""

		if not self.data or not isinstance(self.data, dict):
			self.data = {}
		if not 'eye_blink' in self.data:
			self.data['eye_blink'] = {}
		if not 'eye_shelf' in self.data:
			self.data['eye_shelf'] = {}
		if not 'lip_snap' in self.data:
			self.data['lip_snap'] = {}
		self.data = pyutils.ObjectDict(self.data)

	@classmethod
	def create(cls, eye_blink, eye_shelf, lip_snap):
		"""
		Maps Vertices for each set of eyelids.
		
		:param dict eye_blink: {NAME_OR_SIDE: List(str) of vertices}
		:param dict eye_shelf: {NAME_OR_SIDE: List(str) of vertices}
		:param dict lip_snap: Vertex numbers with keys being top vert and values being bottom counterpart for snapping
		:return: Returns the CLS instance for the eyelids
		:rtype: SourceFaceEyelashShelf
		"""

		# toDo Change the args to lists.  EX: blink_eye_name, top_bottom, shelf_eye_name, front_back
		# get the side or eye names
		eye_blink_sides = list(eye_blink.keys())
		eye_shelf_sides = list(eye_shelf.keys())

		# Convert the pm or string vertex names to string numbers.
		# We are converting to numbers to we can replace the name later with any mesh
		# with the same topology.
		for side in eye_blink_sides:
			if any('.vtx' in str(string) for string in eye_blink[side]):

				# Convert the lists to strings
				side_keys = list(map(lambda x: str(x), list(eye_blink[side].keys())))
				# Extract the numbers
				side_keys = vert_utils.get_vertices_as_numbers(side_keys, as_string=True)

				side_values = list(map(lambda x: str(x), list(eye_blink[side].values())))
				side_values = vert_utils.get_vertices_as_numbers(side_values, as_string=True)

				for x in range(len(side_keys)):
					eye_blink[side] = {side_keys[x]: side_values[x]}

		for side in eye_shelf_sides:
			if any('.vtx' in str(string) for string in eye_shelf[side]):

				side_keys = list(map(lambda x: str(x), list(eye_shelf[side].keys())))
				side_keys = vert_utils.get_vertices_as_numbers(side_keys, as_string=True)

				side_values = list(map(lambda x: str(x), list(eye_shelf[side].values())))
				side_values = vert_utils.get_vertices_as_numbers(side_values, as_string=True)

				for x in range(len(side_keys)):
					eye_shelf[side] = {side_keys[x]: side_values[x]}

		if any('.vtx' in str(string) for string in lip_snap):

			side_keys = list(map(lambda x: str(x), list(lip_snap.keys())))
			side_keys = vert_utils.get_vertices_as_numbers(side_keys, as_string=True)

			side_values = list(map(lambda x: str(x), list(lip_snap.values())))
			side_values = vert_utils.get_vertices_as_numbers(side_values, as_string=True)

			for x in range(len(side_keys)):
				lip_snap = {side_keys[x]: side_values[x]}

		# Build the dictionary
		data = {'eye_blink': eye_blink, 'eye_shelf': eye_shelf, 'lip_snap': lip_snap}

		return cls(data)

	def add_selected_eye_blink(self, side):
		"""
		Adds selected vertices to the top and bottom dictionary to map eye blinks.
		
		:param string side: Name or side of the eye you are mapping.
		"""

		if not cmds.selectPref(tso=True, q=True):
			cmds.selectPref(tso=True)

		if not side in self.eye_blink_sides:
			self.eye_blink[side] = {}

		vertices = cmds.ls(orderedSelection=True)
		vertices = deque(vert_utils.get_vertices_as_numbers(vertices, as_string=True))

		for x in range(int(len(vertices) / 2)):
			top_vert = vertices.popleft()
			bottom_vert = vertices.popleft()
			self.eye_blink[side][top_vert] = bottom_vert

	def add_selected_eye_shelf(self, side):
		"""
		Adds selected vertices to the front and back dictionary to map the eye shelf.
		
		:param string side: Name or side of the eye you are mapping.
		"""

		if not cmds.selectPref(tso=True, q=True):
			cmds.selectPref(tso=True)

		if not side in self.eye_shelf_sides:
			self.eye_shelf[side] = {}

		vertices = cmds.ls(orderedSelection=True)
		vertices = deque(vert_utils.get_vertices_as_numbers(vertices, as_string=True))

		for x in range(int(len(vertices) / 2)):
			front_vert = vertices.popleft()
			back_vert = vertices.popleft()
			self.eye_shelf[side][front_vert] = back_vert

	@property
	def eye_blink(self):
		"""
		Returns a dict of top vertices as keys and bottom as values.
		
		:return: Returns a dict of top vertices as keys and bottom as values.
		:rtype: dictionary
		"""

		return self.data.get('eye_blink', None)

	@eye_blink.setter
	def eye_blink(self, vertex_dict):
		"""
		Sets the top and bottom dictionary.
		:param dictionary vertex_dict: Key is the top vertex, value is the bottom Vertex.
		"""
		self.data.update({'eye_blink': vertex_dict})

	@property
	def eye_shelf(self):
		"""
		Returns a dict of top vertices as keys and bottom as values.
		:return: Returns a dict of top vertices as keys and bottom as values.
		:rtype: dictionary
		"""
		return self.data.get('eye_shelf', None)

	@eye_shelf.setter
	def eye_shelf(self, vertex_dict):
		"""
		Returns a dictionary of top vertices as keys and bottom as values.
		
		:return: Returns a list of all the left vertices.
		:rtype: list(str)
		"""
		self.data.update({'eye_shelf': vertex_dict})

	@property
	def eye_shelf_sides(self):
		"""
		Returns a list of all the eye names or sides.
		
		:return:Returns a list of all the eye names or sides.
		:rtype: list(str)
		"""

		return list(self.eye_shelf.keys())

	@property
	def eye_blink_sides(self):
		"""
		Returns a list of all the eye names or sides.
		
		:return:Returns a list of all the eye names or sides.
		:rtype: list(str)
		"""

		return list(self.eye_blink.keys())

	def align_eye_shelf_side_shelf(self, side, mesh_name):
		"""
		Align the back vertex to the front vertex.  Flattens and straightens the eye shelf.

		:param string mesh_name: name of the mesh.
		"""

		self.align_shelf(self.eye_shelf[side], mesh_name)

	# @ma_decorators.undo_decorator
	def align_shelf(self, vert_dict, mesh_name):
		"""
		Align the back vertex to the front vertex.  Flattens and straightens the eye shelf.

		:param dictionary vert_dict: Dictionary of the front and back vertices.
		:param string mesh_name: name of the mesh.
		"""

		for vert_01, vert_02 in vert_dict.items():
			vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
			pos_a = pm.pointPosition(vertex_01, l=True)
			vertex_02 = self.build_vertex_name(mesh_name, str(vert_02))
			pos_b = pm.pointPosition(vertex_02, l=True)

			pm.xform(vertex_02, t=(pos_a[0], pos_a[1], pos_b[2]))

	##############
	# For winks and blinks
	##############
	@ma_decorators.undo_decorator
	def snap_side_top_blink(self, side, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps top eye shelf to the bottom eye shelf.

		:param string side: mesh side (right or left)
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_top_verts(self.eye_blink[side], mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	@ma_decorators.undo_decorator
	def snap_side_bottom_blink(self, side, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps bottom eye shelf to the top eye shelf.

		:param string side: mesh side (right or left)
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_bottom_verts(self.eye_blink[side], mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	@ma_decorators.undo_decorator
	def snap_eye_blink_to_middle(self, side, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps eye shelf to midpoint between top and bottom verts.

		:param string side: mesh side (right or left)
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_verts_to_middle(self.eye_blink[side], mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	@property
	def lip_snap(self):
		"""
		Returns a dict of top vertices as keys and bottom as values.

		:return: Returns a dict of top vertices as keys and bottom as values.
		:rtype: dictionary
		"""

		return self.data.get('lip_snap', None)

	@lip_snap.setter
	def lip_snap(self, vertex_dict):
		"""
		Sets the top and bottom dictionary. Should be a dict for top and a dict for bottom.

		:param dictionary vertex_dict: Key is the vertex being snapped, value is the vertex snapping to.
		"""

		self.data.update({'lip_snap': vertex_dict})

	def snap_lips_top_to_bottom(self, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps lips top verts to bottom verts.

		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_top_verts(self.lip_snap.get('top'), mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	def snap_lips_bottom_to_top(self, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps lips bottom verts to top verts.

		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_bottom_verts(self.lip_snap.get('top'), mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	def snap_lips_to_middle(self, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps lips to midpoint between top and bottom verts.

		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		self.snap_verts_to_middle(self.lip_snap.get('top'), mesh_name, smooth=smooth, smooth_amount=smooth_amount)

	@ma_decorators.undo_decorator
	def snap_verts_to_middle(self, vert_dict, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps verts from top and bottom to a midpoint between them.

		:param dict vert_dict: Dictionary of vertices with top verts as keys and bottom as values.
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		for vert_01, vert_02 in vert_dict.items():
			vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
			pos_a = pm.pointPosition(vertex_01, l=True)
			vertex_02 = self.build_vertex_name(mesh_name, str(vert_02))
			pos_b = pm.pointPosition(vertex_02, l=True)

			pos_c = [(pos_a[0] + pos_b[0])/2,
					 (pos_a[1] + pos_b[1])/2,
					 (pos_a[2] + pos_b[2])/2]

			pm.xform(vertex_01, t=(pos_c[0], pos_c[1], pos_c[2]))
			pm.xform(vertex_02, t=(pos_c[0], pos_c[1], pos_c[2]))
		if smooth:
			self.smooth_snapped_verts(vert_dict, mesh_name, 'middle', smooth_amount=smooth_amount)

	@ma_decorators.undo_decorator
	def snap_bottom_verts(self, vert_dict, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps bottom verts to top verts.

		:param dict vert_dict: Dictionary of vertices with top verts as keys and bottom as values.
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		for vert_01, vert_02 in vert_dict.items():
			vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
			pos_a = pm.pointPosition(vertex_01, l=True)
			vertex_02 = self.build_vertex_name(mesh_name, str(vert_02))

			pm.xform(vertex_02, t=(pos_a[0], pos_a[1], pos_a[2]))
		if smooth:
			self.smooth_snapped_verts(vert_dict, mesh_name, 'bottom', smooth_amount=smooth_amount)

	@ma_decorators.undo_decorator
	def snap_top_verts(self, vert_dict, mesh_name, smooth=False, smooth_amount=1):
		"""
		Snaps top verts to bottom verts.

		:param dict vert_dict: Dictionary of vertices with top verts as keys and bottom as values.
		:param string mesh_name: name of the mesh.
		:param bool smooth: Whether to smooth vertices around snapped vertices after snapping
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		for vert_01, vert_02 in vert_dict.items():
			vertex_02 = self.build_vertex_name(mesh_name, str(vert_02))
			pos_a = pm.pointPosition(vertex_02, l=True)
			vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))

			pm.xform(vertex_01, t=(pos_a[0], pos_a[1], pos_a[2]))
		if smooth:
			self.smooth_snapped_verts(vert_dict, mesh_name, 'top', smooth_amount=smooth_amount)

	def smooth_snapped_verts(self, vert_dict, mesh_name, side, smooth_amount=1):
		"""
		Smooths verts around those that were snapped.

		:param dict vert_dict: Dictionary of vertices with top verts as keys and bottom as values.
		:param string mesh_name: name of the mesh.
		:param string side: Side of verts being snapped (top, bottom)
		:param int smooth_amount: Times to repeat smoothing procedure
		"""

		snapped_verts = []

		if side == 'top':
			for vert_01 in vert_dict.keys():
				vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
				snapped_verts.append(vertex_01)
		elif side == 'bottom':
			for vert_01 in vert_dict.values():
				vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
				snapped_verts.append(vertex_01)
		else:
			for vert_01, vert_02 in vert_dict.items():
				vertex_01 = self.build_vertex_name(mesh_name, str(vert_01))
				vertex_02 = self.build_vertex_name(mesh_name, str(vert_02))
				snapped_verts.append(vertex_01)
				snapped_verts.append(vertex_02)

		cmds.select(snapped_verts, r=True)
		mel.eval('PolySelectTraverse 1')
		cmds.select(snapped_verts, d=True)
		verts_to_smooth = cmds.ls(sl=True, fl=True)
		prog_ui = progressbar_ui.ProgressBarStandard()
		prog_ui.update_status(0, 'Starting Up')

		i = 100.0 / smooth_amount
		for x in range(smooth_amount):
			step = x * i
			prog_ui.update_status(step, f'Smoothing around snapped vertices...')
			for vert_to_smooth in verts_to_smooth:
				if vert_to_smooth not in snapped_verts:
					cmds.select(vert_to_smooth, r=True)
					mel.eval('PolySelectTraverse 5')
					cmds.select(vert_to_smooth, d=True)
					pos_verts = cmds.ls(sl=True, fl=True)
					pos_a = cmds.pointPosition(pos_verts[0], l=True)
					pos_b = cmds.pointPosition(pos_verts[1], l=True)
					pos_c = cmds.pointPosition(pos_verts[2], l=True)
					pos_d = cmds.pointPosition(pos_verts[3], l=True)
					pos_e = cmds.pointPosition(vert_to_smooth, l=True)

					pos_f = [(pos_a[0] + pos_b[0] + pos_c[0] + pos_d[0] + pos_e[0]) / 5,
							 (pos_a[1] + pos_b[1] + pos_c[1] + pos_d[1] + pos_e[1]) / 5,
							 (pos_a[2] + pos_b[2] + pos_c[2] + pos_d[2] + pos_e[2]) / 5]

					cmds.xform(vert_to_smooth, t=(pos_f[0], pos_f[1], pos_f[2]))
		cmds.select(cl=True)
		prog_ui.update_status(100, 'Finished')