"""
Source data for working with the facial rigs.
"""

# python imports
import os
# software specific imports
#  python imports
from mca.common import log
from mca.common.textio import jsonio
from mca.common.utils import dict_utils
from mca.common.project import paths
from mca.mya.face import face_vertex_data, joints_data
from mca.mya.rigging import frag

logger = log.MCA_LOGGER


FACE_FILE_NAME = 'rig_source_data.json'

FACE_DATA_TYPES = {'rig_template': {},
					# Set the Race
					'race': {},
					# Setup initial vertex data
					'regions': {},
					# Setup source head data
					'source_head': {},
					# Setup world space or local data
					'flag_positions': {},
					# Set skeleton file
					'skeleton': {}}


REGION_DATA_TYPES = {'mirror_type': {},
						# Set up side
						'side': 'center',
						'region': {},
						'connection_type':'UvPin',
						# The named used for the mesh type
						'mesh_type_name': {},
						# The named used for the general category for the mesh
						# Ex: skin_mesh, blendshape_mesh, etc...
						'mesh_category': {},
						# Set up initial vertex data
						'vertex_data': {'vertex_mirror': {},
										'eye_shelf' : {},
										'eye_blink' : {},
										'eyelash_skin_map' : {},
										'vertex_default_regions': {}},
						# Set up initial parameter data
						'parameter_data': {'parameters' : {},
											'solve_parameters': {}},
						# Set up initial skinning data
						'skinning': {'saved':{},
									'initial':{},
									'final':{}},
						# Set up initial joints data
						'joints_data': {'skinned': {},
										'joints_uv':{},
										'anim_ctrls':{}},

						# Set up eye card data
						'eye_card_uv_data': {'eye_shadow': {},
											 'eye_tear': {}}}


class SourceFaceData:
	def __init__(self, data=None):
		data = data_check(FACE_DATA_TYPES, data)
		self.data = dict_utils.ObjectDict(data)
	
	################
	# regions
	################
	@property
	def regions(self):
		"""
		Returns the regions for the face.
		
		:return: Returns the regions for the face.
		:rtype: list(str)
		
		"""
		return self.data.get('regions', None)
	
	@regions.setter
	def regions(self, value):
		"""
		Sets the regions for the face.
		
		:param value:
		:return:
		"""
		
		self.data.regions = value
	
	@property
	def regions_list(self):
		"""
		Returns the regions for the face.
		
		:return: Returns the regions for the face.
		:rtype: list(str)
		"""
		
		return list(self.data.regions.keys())
	
	@property
	def blendshape_regions_list(self):
		"""
		Returns the regions for the face.

		:return: Returns the regions for the face.
		:rtype: list(str)
		"""
		
		regions = list(self.data.regions.keys())
		blend_shapes = []
		for region in regions:
			region_category = self.data.regions[region].get('mesh_category', None)
			if region_category == frag.FACE_BLENDSHAPE_CATEGORY:
				blend_shapes.append(region)
		return blend_shapes
	
	@property
	def skinned_regions_list(self):
		"""
		Returns the regions for the face.

		:return: Returns the regions for the face.
		:rtype: list(str)
		"""
		
		regions = list(self.data.regions.keys())
		blend_shapes = []
		for region in regions:
			region_category = self.data.regions[region].get('mesh_category', None)
			if region_category == frag.FACE_BLENDSHAPE_CATEGORY:
				blend_shapes.append(region)
		skinned_regions = [x for x in regions if not x in blend_shapes]
		return skinned_regions
	
	################
	# Race
	################
	@property
	def race(self):
		"""
		Returns the name of the Race for the character.
		
		:return: Returns the name of the Race for the character.
		:rtype: str
		"""
		
		return self.data.race
	
	@race.setter
	def race(self, value):
		"""
		Sets the Race of the character.
		:param str value: Name of the character race.
		"""
		
		self.data.race = value
		
	################
	# Rig Template
	################
	@property
	def rig_template(self):
		"""
		Returns the rig template being used to build the rig.  EX. player_head_template.PlayerHeadTemplate
		Name of the .py and the class.
		
		:return: Returns the rig template being used to build the rig.
		:rtype: str
		"""
		
		return self.data.rig_template
	
	@rig_template.setter
	def rig_template(self, value):
		"""
		Sets the rig template being used to build the rig. EX. player_head_template.PlayerHeadTemplate
		Name of the .py and the class.
		
		:param str value: The rig template being used to build the rig.
		"""
		
		self.data.rig_template = value
		
	################
	# Source Head
	################
	@property
	def source_head(self):
		"""
		Returns the source head to generate blend shapes from.
		
		:return: Returns the source head to generate blend shapes from.
		:rtype: str
		"""
		
		return self.data.source_head
	
	@source_head.setter
	def source_head(self, value):
		"""
		Sets the source head to generate blend shapes from.
		
		:param str value: The source head to generate blend shapes from.
		"""
		
		self.data.source_head = value
	
	################
	# Flag Positions
	################
	@property
	def flag_positions(self):
		"""
		Returns a keyword on how the flag positions should be set. Examples: 'World Space', 'UV Space'
		
		:return: Returns a keyword on how the flag positions should be set.
		:rtype: str
		"""
		
		return self.data.flag_positions
	
	@flag_positions.setter
	def flag_positions(self, value):
		"""
		Sets a keyword on how the flag positions should be set. Examples: 'World Space', 'UV Space'
		
		:param str value: A keyword on how the flag positions should be set.
		"""
		
		self.data.flag_positions = value
	
	################
	# Flag Positions
	################
	@property
	def skeleton(self):
		"""
		Returns the file name of the stored skeleton data.
		
		:return: Returns the file name of the stored skeleton data.
		:rtype: str
		"""
		
		return self.data.get('skeleton', None)
	
	@skeleton.setter
	def skeleton(self, value):
		"""
		Sets the file name of the stored skeleton data.
		
		:param str value: The file name of the stored skeleton data.
		"""
		
		self.data.skeleton = value
	
	@property
	def primary_parameters(self):
		"""
		Returns the primary parameters dict.

		:return: Returns the primary parameters dict.
		:rtype: dictionary
		"""
		
		return self.data.get('primary_parameters', None)
	
	@primary_parameters.setter
	def primary_parameters(self, value):
		"""
		Sets the primary parameters dict.

		:param dict value: The primary parameters dict.
		"""
		
		self.data.update({'primary_parameters': value})
	
	def get_primary_parameters(self):
		"""
		Returns an instance of ParameterData.
		
		:return: Returns an instance of ParameterData.
		:rtype: ParameterData
		"""
		return frag.ParameterData(self.primary_parameters)
	
	def get_counterpart(self, type_name, region_name):
		"""
		Returns the opposite region.  Ex: head_mesh - skin_mesh: returns head_mesh - blendshape_mesh
		
		:param str type_name: a description of the type of mesh.
		:param str region_name: a type of category for where the data lives.
		:return: Returns the opposite region.
		:rtype: str
		"""
		
		regions_list = self.regions_list
		for source_region in regions_list:
			if not self.regions.get(source_region, None):
				return
			mesh_type_name = self.regions[source_region]['mesh_type_name']
			if mesh_type_name == type_name:
				if not region_name == source_region:
					return source_region
		return
	
	def duplicate_region(self, region_name, new_region_name):
		"""
		Duplicates the region dictionary and stores it under a new region.
		
		:param str region_name: a type of category for where the data lives.
		:param str new_region_name: The name of the new region being added.
		:return: Returns an instance of the new region data.
		:rtype: FaceMeshRegionData
		"""
		
		old_region = self.regions.get(region_name, None)
		if not old_region:
			return
		self.regions.update({new_region_name: old_region})
		return FaceMeshRegionData(new_region_name, self.data)
	
	def export(self, file_path):
		"""
		Exports the data to a json file.
		
		:param str file_path: Full path to the file.
		"""
		
		jsonio.write_to_json_file(data=self.data, filename=file_path)
	
	def export_with_asset_id(self, asset_id):
		"""
		Exports the data to a json file.

		:param str asset_id: id of the asset.
		"""
		
		file_path = os.path.join(paths.get_face_data_path(asset_id), FACE_FILE_NAME)
		jsonio.write_to_json_file(data=self.data, filename=file_path)
	
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


class FaceMeshRegionData(SourceFaceData):
	def __init__(self, region_name, data=None):
		self.region_name = region_name
		data = self.data_check(region_name, data)
		self.data = dict_utils.ObjectDict(data)
		super(FaceMeshRegionData, self).__init__(self.data)
		
	@classmethod
	def create(cls, region_name,
					data,
					mesh_type_name=None,
					mesh_category=None,
					mirror_type=None,
					side=None,
					vertex_data=None,
					mirror=None,
					joints=None,
					parameter_data=None):
		"""
		Creates an initial dict for setting source data.
		
		:param str region_name: Name of the region.
		:param str mesh_type_name: Type of meshes in this region.
		:param str mesh_category: Type of category the meshes belong to in this region.
		:param str mirror_type: Mirror type for the meshes in this region
		:param str side: Side in which the meshes in this region are on
		:param dict vertex_data: Mapped vertex data for different zones of the face.
		:param str mirror: The mirror type.  Either mirror_self or mirror_dup.
		:param dict joints: Data about the joints.  Names, uv positions, orientation, translation, and rotation.
		:param dict skinning: A dictionary of all the skinning data.
		:param parameter_data: A dictionary of all the face poses.
		:return: Returns an instance of FaceMeshRegionData
		:rtype: dictionary
		"""
		data['regions'].setdefault(region_name, REGION_DATA_TYPES)
		data['regions'].update({region_name: {'vertex_data': vertex_data or {},
							'mirror': mirror or {},
							'mesh_type_name': mesh_type_name or {},
							'mesh_category': mesh_category or {},
							'joints': joints or {},
							'skinning': joints or {},
							'parameter_data': parameter_data or {},
							'mirror_type': mirror_type or {},
							'side': side or {}}})
		
		return cls(region_name, data)
	
	@staticmethod
	def data_check(region_name, data):
		"""
		Checks to make sure the dictionary has all base keys and values.
		
		:param str region_name: Name of the region.
		:param dict data: Dictionary of all the face data.
		:return: Dictionary of all the face data.
		:rtype: Dictionary
		"""
		
		if not data:
			data = FACE_DATA_TYPES
		if region_name not in data:
			data['regions'].setdefault(region_name, REGION_DATA_TYPES)
		return data
	
	##################
	# Region Name
	##################
	@property
	def region(self):
		"""
		Returns the name of the region.
		
		:return: Returns the name of the region.
		:rtype: dict
		"""
		
		return self.data['regions'][self.region_name]
	
	@region.setter
	def region(self, value):
		"""
		Sets the name of the region.
		
		:param dict value: The name of the region.
		"""
		self.data['regions'].update({self.region_name: value})
		
	##################
	# Vertex Data
	##################
	@property
	def vertex_data(self):
		"""
		Returns mapped vertex data for different zones of the face.
		
		:return: Returns mapped vertex data for different zones of the face.
		:rtype: dictionary
		"""
		
		return self.region['vertex_data']
	
	@vertex_data.setter
	def vertex_data(self, value):
		"""
		Sets mapped vertex data for different zones of the face.
		
		:param dict value: Mapped vertex data for different zones of the face.
		"""
		
		self.region.update({'vertex_data': value})
	
	@property
	def vertex_mirror(self):
		"""
		Returns vertex numbers for each side of the face.  (Left, Right, Middle)
		
		:return: Returns vertex numbers for each side of the face.  (Left, Right, Middle)
		:rtype: dictionary
		"""
		
		return self.vertex_data.get('vertex_mirror', None)
	
	@vertex_mirror.setter
	def vertex_mirror(self, value):
		"""
		Sets vertex numbers for each side of the face.  (Left, Right, Middle)
		
		:param dict value: Vertex numbers for each side of the face.  (Left, Right, Middle)
		"""
		
		self.vertex_data.update({'vertex_mirror': value})

	@property
	def eye_card_uv_data(self):
		"""
		Returns UV data for different zones of the face.

		:return: Returns UV data for different zones of the face.
		:rtype: dictionary
		"""

		return self.region.get('eye_card_uv_data', None)

	@eye_card_uv_data.setter
	def eye_card_uv_data(self, value):
		"""
		Sets UV data for different zones of the face.

		:param dict value: UV data for different zones of the face.
		"""

		self.region.update({'eye_card_uv_data': value})

	# Returns the class
	def get_mirror_data(self):
		"""
		Returns an instance of SourceVertexMirror to interact with the mirror vertex data.
		
		:return: Returns an instance of SourceVertexMirror.
		:rtype: SourceVertexMirror
		"""
		
		return face_vertex_data.SourceVertexMirror(self.vertex_mirror)
	
	@property
	def vertex_eye_shelf(self):
		"""
		Returns vertex map of the eye shelf.
		
		:return: Returns vertex map of the eye shelf.
		:rtype: dictionary
		"""
		
		return self.vertex_data.get('eye_shelf', None)
	
	@vertex_eye_shelf.setter
	def vertex_eye_shelf(self, value):
		"""
		Sets vertex map of the eye shelf.
		
		:param dict value: Vertex map of the eye shelf.
		"""
		
		self.vertex_data.update({'eye_shelf': value})

	@property
	def vertex_lip_snap(self):
		"""
		Returns vertex map of the eye shelf.

		:return: Returns vertex map of the eye shelf.
		:rtype: dictionary
		"""

		return self.vertex_data.get('lip_snap', None)

	@vertex_lip_snap.setter
	def vertex_lip_snap(self, value):
		"""
		Sets vertex map of the eye shelf.

		:param dict value: Vertex map of the eye shelf.
		"""

		self.vertex_data.update({'lip_snap': value})

	@property
	def vertex_eye_blink(self):
		"""
		Returns vertex map for the eye blink.
		
		:return: Returns vertex map for the eye blink.
		:rtype: dictionary
		"""
		
		return self.vertex_data.get('eye_blink', None)
	
	@vertex_eye_blink.setter
	def vertex_eye_blink(self, value):
		"""
		Sets vertex map for the eye blink.
		
		:param dict value: Vertex map for the eye blink.
		"""
		
		self.vertex_data.update({'eye_blink': value})
	
	# Returns the class
	def get_eyelids(self):
		"""
		Returns an instance of SourceFaceEyelashShelf to handle the eyelids data.
		
		:return: Returns an instance of SourceFaceEyelashShelf to handle the eyelids data.
		:rtype: dictionary
		"""
		
		return face_vertex_data.SourceFaceEyelashShelf.create(self.vertex_eye_blink,
		                                                      self.vertex_eye_shelf,
		                                                      self.vertex_lip_snap)
	
	@property
	def vertex_eyelash_skin_map(self):
		"""
		Returns vertex map for snapping the eyelashes to a mesh.
		
		:return: Returns vertex map for snapping the eyelashes to a mesh.
		:rtype: dictionary
		"""
		
		return self.vertex_data.get('eyelash_skin_map', None)
	
	@vertex_eyelash_skin_map.setter
	def vertex_eyelash_skin_map(self, value):
		"""
		Sets vertex map for snapping the eyelashes to a mesh.
		
		:param dict value: Vertex map for snapping the eyelashes to a mesh.
		"""
		
		self.vertex_data.update({'eyelash_skin_map': value})
	
	@property
	def vertex_default_regions(self):
		"""
		Returns vertex map for snapping the eyelashes to a mesh.
		
		:return: Returns vertex map for snapping the eyelashes to a mesh.
		:rtype: dictionary
		"""
		
		return self.vertex_data.get('vertex_default_regions', None)
	
	@vertex_default_regions.setter
	def vertex_default_regions(self, value):
		"""
		Sets vertex map for snapping the eyelashes to a mesh.
		
		:param dict value: Vertex map for snapping the eyelashes to a mesh.
		"""
		
		self.vertex_data.update({'vertex_default_regions': value})
		
	# Returns the class
	def get_vertex_default_regions(self):
		"""
		Returns an instance of SourceFaceEyelashShelf to handle the eyelids data.
		
		:return: Returns an instance of SourceFaceEyelashShelf to handle the eyelids data.
		:rtype: dictionary
		"""
		
		return face_vertex_data.RegionVertices(self.vertex_default_regions)
	
	##################
	# Side
	##################
	@property
	def side(self):
		"""
		Returns the side in which the meshes in this region are on.
		
		:return: Returns the side in which the meshes in this region are on.
		:rtype: str
		"""
		
		return self.region['side']
	
	@side.setter
	def side(self, value):
		"""
		Sets the side in which the meshes in this region are on.
		
		:param str value: The side in which the meshes in this region are on.
		"""
		
		self.region['side'] = value
	
	##################
	# Mesh Type Name
	##################
	@property
	def mesh_type_name(self):
		"""
		Returns a key word on what type of meshes are in this region.  Examples: head_mesh, jaw_mesh, etc...
		
		:return: Returns a key word on what type of meshes are in this region.
		:rtype: str
		"""
		
		return self.region['mesh_type_name']
	
	@mesh_type_name.setter
	def mesh_type_name(self, value):
		"""
		Sets a key word on what type of meshes are in this region.  Examples: head_mesh, jaw_mesh, etc...
		
		:param str value: A key word on what type of meshes are in this region.
		"""
		
		self.region['mesh_type_name'] = value
		
	##################
	# Mesh Category
	##################
	@property
	def mesh_category(self):
		"""
		Returns a key word on what type of category the meshes belong to in this region.  Examples: skin_mesh,
		blendshape_mesh, etc...
		
		:return: Returns a key word on what type of category the meshes belong to in this region.
		:rtype: str
		"""
		
		return self.region['mesh_category']
	
	@mesh_category.setter
	def mesh_category(self, value):
		"""
		Sets a key word on what type of category the meshes belong to in this region.  Examples: skin_mesh,
		blendshape_mesh, etc...
		
		:param str value: A key word on what type of category the meshes belong to in this region.
		"""
		
		self.region['mesh_category'] = value
	
	##################
	# Mirror Data
	##################
	@property
	def mirror_type(self):
		"""
		Returns the mirror type for the meshes in this region.
		
		:return: Returns the mirror type for the meshes in this region.
		:rtype: str
		"""
		
		return self.region['mirror_type']
	
	@mirror_type.setter
	def mirror_type(self, value):
		"""
		Sets the mirror type.  Either mirror_self or mirror_dup.
		mirror_self will mirror the mesh.
		MirrorDup will duplicate the mesh, then flip across an axis to mirror.
		
		:param str value: Either mirror_self or mirror_dup.
		"""
		
		self.region['mirror_type'] = value
	
	##################
	# Joints connection type
	##################
	@property
	def connection_type(self):
		"""
		Returns a key word on how to attach the joints to the meshes in this region.
		
		:return: Returns a key word on how to attach the joints to the meshes in this region.
		:rtype: str
		"""
		
		return self.region.get('connection_type', None)
	
	@connection_type.setter
	def connection_type(self, value):
		"""
		Sets a key word on how to attach the joints to the meshes in this region.
		
		:param str value: A key word on how to attach the joints to the meshes in this region.
		"""
		
		self.region.update({'connection_type': value})
	
	@property
	def clown_mask(self):
		"""
		Returns a key word on how to attach the joints to the meshes in this region.

		:return: Returns a key word on how to attach the joints to the meshes in this region.
		:rtype: str
		"""
		
		return self.region.get('clown_mask', None)
	
	@clown_mask.setter
	def clown_mask(self, value):
		"""
		Sets a key word on how to attach the joints to the meshes in this region.

		:param str value: A key word on how to attach the joints to the meshes in this region.
		"""
		
		self.region.update({'clown_mask': value})
	
	##################
	# Skinning
	##################
	@property
	def skinning(self):
		"""
		Returns a dictionary of all the skinning data.
		
		:return: Returns a dictionary of all the skinning data.
		:rtype: dictionary
		"""
		
		return self.region['skinning']
	
	@skinning.setter
	def skinning(self, value):
		"""
		Sets a dictionary with all the skinning data.
		
		:param dict value: S dictionary with all the skinning data. {{'process':{},'saved':{},'initial':{},'final':{}}
		"""
		
		self.region['skinning'] = value
	
	@property
	def skinning_final(self):
		"""
		Returns a key word on how to process the final skinning of the meshes in this region.
		
		:return: Returns a key word on how to process the final skinning of the meshes in this region.
		:rtype: str
		"""
		
		return self.skinning['final']
	
	@skinning_final.setter
	def skinning_final(self, value):
		"""
		Sets a key word on how to process the final skinning of the meshes in this region.
		
		:param str value: A key word on how to process the final skinning of the meshes in this region.
		"""
		
		self.skinning['final'] = value
	
	@property
	def skinning_saved(self):
		"""
		Returns saved skinning data.
		
		:return: Returns saved skinning data.
		:rtype: dict
		"""
		
		return self.skinning['saved']
	
	@skinning_saved.setter
	def skinning_saved(self, value):
		"""
		Sets saved skinning data.
		
		:param dict value: Saved skinning data.
		"""
		
		self.skinning['saved'] = value
	
	@property
	def skinning_initial(self):
		"""
		Returns a key word on how to process the initial skinning of the meshes in this region.
		
		:return: Returns a key word on how to process the initial skinning of the meshes in this region.
		:rtype: str
		"""
		
		return self.skinning['initial']
	
	@skinning_initial.setter
	def skinning_initial(self, value):
		"""
		Sets a key word on how to process the initial skinning of the meshes in this region.
		
		:param str value: A key word on how to process the initial skinning of the meshes in this region.
		"""
		
		self.skinning['initial'] = value

	@property
	def non_deform_skinning(self):
		"""
		Returns a key word on how to process the initial skinning of the meshes in this region.

		:return: Returns a key word on how to process the initial skinning of the meshes in this region.
		:rtype: str
		"""

		return self.skinning['non_deform_skinning']

	##################
	# Joints and UV Positions
	##################
	@property
	def joints(self):
		"""
		Returns a dictionary of all the joint data for this region.
		
		:return: Returns a dictionary of all the joint data for this region.
		:rtype: dictionary
		"""
		
		return self.region['joints_data']
	
	@joints.setter
	def joints(self, value):
		"""
		Sets a dictionary of all the joint data for this region.
		
		:param dict value: A dictionary of all the joint data for this region.
		"""
		
		self.region['joints_data'] = value
	
	@property
	def joints_uv(self):
		"""
		Returns a dictionary that has data on the joints and uv positions.
		
		:return: Returns a dictionary that has data on the joints and uv positions.
		:rtype: dictionary
		"""
		
		return self.joints.get('joints_uv', None)
	
	@joints_uv.setter
	def joints_uv(self, value):
		"""
		Sets a dictionary that has data on the joints and uv positions.
		
		:param dict value: A dictionary that has data on the joints and uv positions.
		"""
		
		self.joints.update({'joints_uv': value})
	
	@property
	def anim_ctrls(self):
		"""
		Returns a dictionary that has data on the joints for animation controls and their uv positions.
		
		:return: Returns a dictionary that has data on the joints for animation controls and their uv positions.
		:rtype: dictionary
		"""
		
		return self.joints.get('anim_ctrls', None)
	
	@anim_ctrls.setter
	def anim_ctrls(self, value):
		"""
		Sets a dictionary that has data on the joints for animation controls and their uv positions.
		
		:param dict value: A dictionary that has data on the joints for animation controls and their uv positions.
		"""
		
		self.joints.update({'anim_ctrls': value})
	
	@property
	def joints_skinned(self):
		"""
		Returns a list of joints that get skinned to the meshes in this region.
		
		:return: Returns a list of joints that get skinned to the meshes in this region.
		:rtype: list(str)
		"""
		
		return self.joints.get('skinned', None)
	
	@joints_skinned.setter
	def joints_skinned(self, value):
		"""
		Sets a list of joints that get skinned to the meshes in this region.
		
		:param list(str) value: A list of joints that get skinned to the meshes in this region.
		"""
		
		self.joints.update({'skinned': value})
	
	def get_joints_uv(self):
		"""
		Returns an instance of the class FaceJointData for handling joint data.
		
		:return: Returns an instance of the class FaceJointData for handling joint data.
		:rtype: FaceJointData
		"""
		
		return joints_data.FaceJointData(self.joints_uv)
	
	def get_anim_ctrls(self):
		"""
		Returns an instance of the class FaceJointData for handling Animation Control data.
		
		:return: Returns an instance of the class FaceJointData for handling joint data.
		:rtype: FaceJointData
		"""
		
		return joints_data.FaceJointData(self.anim_ctrls)
	
	##################
	# Parameter Data
	##################
	@property
	def parameter_data(self):
		"""
		Returns a dictionary that has pose data for the face.
		
		:return: Returns a dictionary that has pose data for the face.
		:rtype: dictionary
		"""
		
		return self.region['parameter_data']
	
	@parameter_data.setter
	def parameter_data(self, value):
		"""
		Sets a dictionary that has pose data for the face.
		
		:param dict value: A dictionary that has pose data for the face.
		"""
		
		self.region['parameter_data'] = value
	
	@property
	def parameters(self):
		"""
		Returns a dictionary that has pose data for the main poses.
		
		:return: Returns a dictionary that has pose data for the main poses.
		:rtype: dictionary
		"""
		
		return self.parameter_data.get('parameters', None)
	
	@parameters.setter
	def parameters(self, value):
		"""
		Sets a dictionary that has pose data for the main poses.
		
		:param dict value: A dictionary that has pose data for the main poses.
		"""
		if not value:
			del self.parameter_data['parameters']
		self.parameter_data.update({'parameters': value})
	
	def get_parameters(self):
		"""
		Returns an instance of ParameterData based on the parameters dictionary.
		
		:return: Returns an instance of ParameterData based on the parameters dictionary.
		:rtype: ParameterData
		"""
		
		return frag.ParameterData(self.parameters)
	
	@property
	def solve_parameters(self):
		"""
		Returns a dictionary that has pose data for the helper poses.
		
		:return: Returns a dictionary that has pose data for the helper poses.
		:rtype: dictionary
		"""
		
		return self.parameter_data.get('solve_parameters', None)
	
	@solve_parameters.setter
	def solve_parameters(self, value):
		"""
		Sets a dictionary that has pose data for the helper poses.
		
		:param dict value: A dictionary that has pose data for the helper poses.
		"""
		
		self.parameter_data['solve_parameters'] = value
	
	def get_mesh_dict(self):
		"""
		Returns the string tags that gets added to a mesh for identification.
		
		:return:  Returns the string tags that gets added to a mesh for identification.
		:rtype: dict
		"""
		
		markup = {'region': self.region_name,
				'type_name': self.mesh_type_name,
				'category': self.mesh_category,
				'side': self.side,
				'mirror_type':self.mirror_type,
				'race': self.race,
				'joint_connection_type': self.connection_type}
		return markup
	
	@classmethod
	def load(cls, file_path, region_name):
		"""
		Loads a json file and Returns the instance of the class.
		
		:param str file_path: Full path to the file.
		:param str region_name: Name of the region.
		:return: Returns the instance of the class SourceFaceData.
		:rtype: SourceFaceData
		"""
		
		data = jsonio.read_json_file(file_path)
		return cls(region_name=region_name, data=data)


def data_check(empty_data, existing_data=None):
	"""
	Checks a dictionary against another and adds missing keys.
	
	:param dict empty_data: A default set of values for a dictionary.
	:param dict existing_data: a dictionary with existing data.
	:return: Returns a combined dictionary without overwriting existing data.
	:rtype: dictionary
	"""
	
	if not existing_data:
		existing_data = {}
		logger.warning('No data exists.  Creating base dictionary.')
	
	# Compare the 2 dictionaries and add missing keys
	updated_data = dict(list(empty_data.items()) + list(existing_data.items()))
	
	# Add missing nested keys
	for key, value in empty_data.items():
		if isinstance(value, dict) and value.keys():
			sub_data = dict(list(empty_data[key].items()) + list(updated_data[key].items()))
			updated_data[key] = sub_data
	return dict_utils.ObjectDict(updated_data)
			
