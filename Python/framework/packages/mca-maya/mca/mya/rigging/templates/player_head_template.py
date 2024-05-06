"""
Template for human players and npcs
"""

# System global imports
import os
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup, mesh_markup_rig, rig_utils
from mca.mya.rigging.frag import face_mesh_component
from mca.common.paths import paths
from mca.common.utils import fileio
from mca.mya.face import source_data, source_meshes
from mca.mya.modeling import face_model, blendshape_node
from mca.mya.face.face_utils import face_util, face_import_export, face_skinning
from mca.mya.utils import attr_utils
from mca.common.tools.progressbar import progressbar_ui
from mca.common import log

logger = log.MCA_LOGGER


class BaseHeadTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'head'
	
	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE, source_head_name=None):
		super(BaseHeadTemplate, self).__init__(asset_id, asset_type)
		self.source_head_name = source_head_name
		self.generate_shapes = True if source_head_name != None else False
		
	def build(self, finalize=True):
		ui = progressbar_ui.ProgressBarStandard()
		ui.update_status(0, 'Starting Up')
		
		ui.update_status(5, 'Creating Face Rig')
		
		pm.namespace(set=':')
		
		# Get Source Data - The Json file with all the face data
		source_face = get_source_data(self.asset_id)
		if not source_face:
			logger.warning(f'No source data found for {self.asset_id}, using common.')
			source_face = face_util.get_common_face_data()

		# Create blendshape meshes
		face_util.create_all_counter_part_meshes(self.asset_id)
		
		parameter_list = source_face.get_primary_parameters().get_parameters_list()
		world_root = pm.PyNode('root')
		
		# Progress Bar
		ui.update_status(10, 'Gathering Data and Creating Base FRAG Nodes')
		
		# create the rig core frag nodes
		frag_root = frag.FRAGRoot.create(world_root, 'head', self.asset_id)
		skeletal_mesh = frag.SkeletalMesh.create(frag_root)
		
		# get the meshes and the markups
		mesh_markup = mesh_markup_rig.RigMeshMarkup.create(skeletal_mesh.namespace())
		mesh_dict = mesh_markup.get_dict()
		face_mesh_comp = frag.FaceMeshComponent.create(skeletal_mesh, mesh_dict)
		
		frag_rig = frag.FRAGRig.create(frag_root)
		
		parameter_node = frag.FragFaceParameters.create(frag_rig, parameter_list)
		
		# Need to compare to list of meshes in the scene/namespace
		
		# Progress Bar
		ui.update_status(15, 'Importing Blendshapes')
		
		# import blend shapes and create blendnodes
		shape_results = handle_blendshapes(asset_id=self.asset_id,
											source_head_name=self.source_head_name,
											generate_shapes=self.generate_shapes,
											source_face_data=source_face)
		if not shape_results:
			return
		mesh_markup = mesh_markup_rig.RigMeshMarkup.create()
		mesh_dict = mesh_markup.get_dict()

		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
		if self.generate_shapes:
			face_util.set_head_rig_jnts(self.asset_id, chain)
			face_util.set_common_flag_positions(face_mesh_comp.head_blendshape.mesh, chain)
			eye_joints = [chain.get_start('eye', 'right'), chain.get_start('eye', 'left')]
			eye_meshes = [mesh_markup.get_mesh_list_in_region(f'eye_right_mesh')[0],
			              mesh_markup.get_mesh_list_in_region(f'eye_left_mesh')[0]]
			for eye_joint, eye_mesh in list(zip(eye_joints, eye_meshes)):
				pm.delete(pm.pointConstraint(eye_mesh, eye_joint))

			updated_data = update_source_head_data(asset_id=self.asset_id, source_head_name=self.source_head_name)
			if not updated_data:
				new_source_head_data(self.asset_id, self.source_head_name)
		
		# Move the pose grp under all flags
		if shape_results:
			pose_grp = shape_results.get('pose_grp')
			pm.parent(pose_grp, frag_rig.do_not_touch)
		
		# Remove the source mesh for now.  It will get re-loaded if the checkbox is checked.
		if self.generate_shapes:
			source_meshes = shape_results.get('meshes', None)
			if source_meshes:
				[pm.delete(x) for x in source_meshes]
		
		# Get the head blendnode
		head_blendshape = face_mesh_comp.head_blendshape
		head_blendnode_inst = head_blendshape.get_blendnode()
		
		head_blendnode = head_blendnode_inst.blendnode
		# Get the mouth blendnode
		mouth_blendshape = face_mesh_comp.mouth_blendshape
		mouth_blendshape_inst = mouth_blendshape.get_blendnode()
		
		mouth_blendnode = mouth_blendshape_inst.blendnode
		
		# Progress Bar
		ui.update_status(20, 'Connecting Joints')
		
		# Connect the joints
		rivets = head_blendshape.connect_joints(self.asset_id)
		if rivets:
			pm.parent(pm.PyNode(rivets[0]).getParent(), frag_rig.do_not_touch)
			frag_rig.connect_nodes(rivets, 'rivets', 'fragParent')
		mouth_rivets = mouth_blendshape.connect_joints(self.asset_id, delete_old_rivet_grp=False)
		if mouth_rivets:
			pm.parent(pm.PyNode(mouth_rivets[0]).getParent(), frag_rig.do_not_touch)
			frag_rig.connect_nodes(mouth_rivets, 'rivets', 'fragParent')

		#### Skin Meshes #####
		mesh_dict.keys()
		for category, mesh_data in mesh_dict.items():
			if category == frag.FACE_SOURCE_CATEGORY:
				continue
			for type_mesh, mesh in mesh_dict[category].items():
				if category == frag.FACE_BLENDSHAPE_CATEGORY and self.generate_shapes:
					type_minus_mesh = type_mesh.split('mesh')[0]
					face_skinning.apply_common_skinning(mesh, f'{type_minus_mesh}blendshape')
				else:
					face_skinning.apply_face_skinning_from_file(self.asset_id, mesh)

		### Mesh Component End ###
		
		# Progress Bar
		ui.update_status(25, 'Creating Components - World and Neck')

		# world
		
		world_component = frag.WorldComponent.create(frag_rig,
															root,
															'center',
															'world',
															orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()

		spine = chain.get_end('spine', 'center')
		spine_component = frag.FKComponent.create(frag_rig,
														   spine,
														   spine,
														   side='center',
														   region='spine',
														   lock_root_translate_axes=[],
														   lock_child_translate_axes=[])
		spine_flag = spine_component.get_end_flag()
		spine_flag.set_as_sub()
		spine_flag.rename(f'{spine_flag}_sub')
		spine_component.attach_component(world_component, root)

# Neck
		neck_chain = chain.get_chain('neck', 'center')
		neck_component = frag.RFKComponent.create(frag_rig,
														neck_chain[0],
														neck_chain[1],
														'center',
														'neck',
														False)
		neck_component.attach_component(spine_component, spine)
		head_flag = neck_component.end_flag
		neck_flag = neck_component.start_flag
		neck_flag.set_as_sub()
		mid_neck_flag = neck_component.mid_flags[0]
		mid_neck_flag.set_as_detail()
		
		head_flag = head_flag.node
		###############################
		# Tongue controls and Phonemes
		###############################
		# Progress Bar
		ui.update_status(30, 'Creating Components - Tongue')

		### Eyes ####
		# Progress Bar
		ui.update_status(40, 'Creating Components - Eyes')
		
		l_eye_component = frag.EyeComponent.create(frag_rig,
															bind_joint=pm.PyNode('l_eye'),
															side='left',
															region='eye')
		l_eye_component.attach_component(neck_component, head_flag)
		l_rotate_obj = l_eye_component.get_rotate_object()
		
		parameter_node.config_input(l_rotate_obj, 'rotateZ', 0, 45, 'left_eye_left')
		parameter_node.config_output_blendnode(head_blendnode.left_eye_left, 'left_eye_left')
		parameter_node.config_input(l_rotate_obj, 'rotateZ', 0, -45, 'left_eye_right')
		parameter_node.config_output_blendnode(head_blendnode.left_eye_right, 'left_eye_right')
		parameter_node.config_input(l_rotate_obj, 'rotateX', 0, -25, 'left_eye_up')
		parameter_node.config_output_blendnode(head_blendnode.left_eye_up, 'left_eye_up')
		parameter_node.config_input(l_rotate_obj, 'rotateX', 0, 25, 'left_eye_down')
		parameter_node.config_output_blendnode(head_blendnode.left_eye_down, 'left_eye_down')

		r_eye_component = frag.EyeComponent.create(frag_rig,
															bind_joint=pm.PyNode('r_eye'),
															side='right',
															region='eye')
		r_eye_component.attach_component(neck_component, head_flag)
		r_rotate_obj = r_eye_component.get_rotate_object()
		
		parameter_node.config_input(r_rotate_obj, 'rotateZ', 0, 45, 'right_eye_left')
		parameter_node.config_output_blendnode(head_blendnode.right_eye_left, 'right_eye_left')
		parameter_node.config_input(r_rotate_obj, 'rotateZ', 0, -45, 'right_eye_right')
		parameter_node.config_output_blendnode(head_blendnode.right_eye_right, 'right_eye_right')
		parameter_node.config_input(r_rotate_obj, 'rotateX', 0, -25, 'right_eye_up')
		parameter_node.config_output_blendnode(head_blendnode.right_eye_up, 'right_eye_up')
		parameter_node.config_input(r_rotate_obj, 'rotateX', 0, 25, 'right_eye_down')
		parameter_node.config_output_blendnode(head_blendnode.right_eye_down, 'right_eye_down')

		# center
		center_eye_component = frag.EyeCenterComponent.create(frag_parent=frag_rig,
																	side='center',
																	region='eyes',
																	components=[l_eye_component, r_eye_component])
		center_eye_component.attach_component(neck_component, head_flag)
		center_eye_flag = center_eye_component.get_flag()
		
		#### Brows ####
		ui.update_status(50, 'Creating Components - Brows')
		
		# Left
		l_outer_brow = frag.FaceFKComponent.create(frag_parent=frag_rig,
													joint=pm.PyNode('l_outer_brow_null'),
													side='left',
													region='outer_brow',
													flag_scale=1,
													limit_point=((-10, 0), (-10, 10), (None, None)),
													limit_orient=((None, None), (None, None), (-60, 60)),
													translate_scale=(10, 10, 10))
		l_outer_brow.attach_component(neck_component, head_flag)
		l_outer_brow_flag = l_outer_brow.get_start_flag()
		
		# Connect blend shapes to parameter node
		parameter_node.config_input(l_outer_brow_flag, 'translateY', 0, 10, 'left_outer_brow_up')
		parameter_node.config_output_blendnode(head_blendnode.left_outer_brow_up, 'left_outer_brow_up')
		parameter_node.config_input(l_outer_brow_flag, 'translateY', 0, -10, 'left_outer_brow_down')
		parameter_node.config_output_blendnode(head_blendnode.left_outer_brow_down, 'left_outer_brow_down')
		
		parameter_node.config_input(l_outer_brow_flag, 'translateX', 0, -10, 'left_outer_brow_in')
		parameter_node.config_output_blendnode(head_blendnode.left_outer_brow_in, 'left_outer_brow_in')
		
		parameter_node.config_input(l_outer_brow_flag, 'rotateZ', 0, 60, 'left_outer_brow_tilt_anger')
		parameter_node.config_output_blendnode(head_blendnode.left_outer_brow_tilt_anger, 'left_outer_brow_tilt_anger')
		parameter_node.config_input(l_outer_brow_flag, 'rotateZ', 0, -60, 'left_outer_brow_tilt_sad')
		parameter_node.config_output_blendnode(head_blendnode.left_outer_brow_tilt_sad, 'left_outer_brow_tilt_sad')
		
		l_inner_brow = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_inner_brow_null'),
															side='left',
															region='inner_brow',
															flag_scale=1,
															limit_point=((-10, 0), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		l_inner_brow.attach_component(neck_component, head_flag)
		l_inner_brow_flag = l_inner_brow.get_start_flag()
		
		# Connect blend shapes to parameter node
		parameter_node.config_input(l_inner_brow_flag, 'translateY', 0, 10, 'left_inner_brow_up')
		parameter_node.config_output_blendnode(head_blendnode.left_inner_brow_up, 'left_inner_brow_up')
		parameter_node.config_input(l_inner_brow_flag, 'translateY', 0, -10, 'left_inner_brow_down')
		parameter_node.config_output_blendnode(head_blendnode.left_inner_brow_down, 'left_inner_brow_down')
		
		parameter_node.config_input(l_inner_brow_flag, 'translateX', 0, -10, 'left_brow_squeeze')
		parameter_node.config_output_blendnode(head_blendnode.left_brow_squeeze, 'left_brow_squeeze')
		
		parameter_node.config_input(l_inner_brow_flag, 'rotateZ', 0, 60, 'left_inner_brow_tilt_anger')
		parameter_node.config_output_blendnode(head_blendnode.left_inner_brow_tilt_anger, 'left_inner_brow_tilt_anger')
		parameter_node.config_input(l_inner_brow_flag, 'rotateZ', 0, -60, 'left_inner_brow_tilt_sad')
		parameter_node.config_output_blendnode(head_blendnode.left_inner_brow_tilt_sad, 'left_inner_brow_tilt_sad')
		
		# Right
		r_outer_brow = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_outer_brow_null'),
															side='right',
															region='outer_brow',
															flag_scale=1,
															limit_point=((-10, 0), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		r_outer_brow.attach_component(neck_component, head_flag)
		r_outer_brow_flag = r_outer_brow.get_start_flag()
		
		# Connect blend shapes to parameter node
		parameter_node.config_input(r_outer_brow_flag, 'translateY', 0, 10, 'right_outer_brow_up')
		parameter_node.config_output_blendnode(head_blendnode.right_outer_brow_up, 'right_outer_brow_up')
		parameter_node.config_input(r_outer_brow_flag, 'translateY', 0, -10, 'right_outer_brow_down')
		parameter_node.config_output_blendnode(head_blendnode.right_outer_brow_down, 'right_outer_brow_down')
		
		parameter_node.config_input(r_outer_brow_flag, 'translateX', 0, -10, 'right_outer_brow_in')
		parameter_node.config_output_blendnode(head_blendnode.right_outer_brow_in, 'right_outer_brow_in')
		
		parameter_node.config_input(r_outer_brow_flag, 'rotateZ', 0, 60, 'right_outer_brow_tilt_anger')
		parameter_node.config_output_blendnode(head_blendnode.right_outer_brow_tilt_anger, 'right_outer_brow_tilt_anger')
		parameter_node.config_input(r_outer_brow_flag, 'rotateZ', 0, -60, 'right_outer_brow_tilt_sad')
		parameter_node.config_output_blendnode(head_blendnode.right_outer_brow_tilt_sad, 'right_outer_brow_tilt_sad')
		
		r_inner_brow = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_inner_brow_null'),
															side='right',
															region='inner_brow',
															flag_scale=1,
															limit_point=((-10, 0), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		r_inner_brow.attach_component(neck_component, head_flag)
		r_inner_brow_flag = r_inner_brow.get_start_flag()
		
		parameter_node.config_input(r_inner_brow_flag, 'translateY', 0, 10, 'right_inner_brow_up')
		parameter_node.config_output_blendnode(head_blendnode.right_inner_brow_up, 'right_inner_brow_up')
		parameter_node.config_input(r_inner_brow_flag, 'translateY', 0, -10, 'right_inner_brow_down')
		parameter_node.config_output_blendnode(head_blendnode.right_inner_brow_down, 'right_inner_brow_down')
		
		parameter_node.config_input(r_inner_brow_flag, 'translateX', 0, -10, 'right_brow_squeeze')
		parameter_node.config_output_blendnode(head_blendnode.right_brow_squeeze, 'right_brow_squeeze')
		
		parameter_node.config_input(r_inner_brow_flag, 'rotateZ', 0, 60, 'right_inner_brow_tilt_anger')
		parameter_node.config_output_blendnode(head_blendnode.right_inner_brow_tilt_anger, 'right_inner_brow_tilt_anger')
		parameter_node.config_input(r_inner_brow_flag, 'rotateZ', 0, -60, 'right_inner_brow_tilt_sad')
		parameter_node.config_output_blendnode(head_blendnode.right_inner_brow_tilt_sad, 'right_inner_brow_tilt_sad')
		
		#### Cheeks ####
		ui.update_status(60, 'Creating Components - Cheeks')
		
		# Left
		l_outer_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_cheek_outer_null'),
															side='left',
															region='outer_cheek',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		l_outer_cheek.attach_component(neck_component, head_flag)
		l_outer_cheek_flag = l_outer_cheek.get_start_flag()
		
		parameter_node.config_input(l_outer_cheek_flag, 'translateY', 0, 10, 'left_cheek_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_outer_up, 'left_cheek_outer_up')
		parameter_node.config_input(l_outer_cheek_flag, 'translateY', 0, -10, 'left_cheek_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_outer_down, 'left_cheek_outer_down')
		
		l_inner_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_cheek_inner_null'),
															side='left',
															region='inner_cheek',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		l_inner_cheek.attach_component(neck_component, head_flag)
		l_inner_cheek_flag = l_inner_cheek.get_start_flag()
		
		parameter_node.config_input(l_inner_cheek_flag, 'translateY', 0, 10, 'left_cheek_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_inner_up, 'left_cheek_inner_up')
		parameter_node.config_input(l_inner_cheek_flag, 'translateY', 0, -10, 'left_cheek_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_inner_down, 'left_cheek_inner_down')
		
		l_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
													joint=pm.PyNode('l_cheek_null'),
													side='left',
													region='cheek',
													flag_scale=1,
													limit_point=((-10, 10), (-10, 10), (-10, 10)),
													limit_orient=((None, None), (None, None), (None, None)),
													translate_scale=(10, 10, 10))
		l_cheek.attach_component(neck_component, head_flag)
		l_cheek_flag = l_cheek.get_start_flag()
		
		parameter_node.config_input(l_cheek_flag, 'translateZ', 0, 10, 'left_cheek_shift_out')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_shift_out, 'left_cheek_shift_out')
		parameter_node.config_input(l_cheek_flag, 'translateZ', 0, -10, 'left_cheek_shift_in')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_shift_in, 'left_cheek_shift_in')
		
		parameter_node.config_input(l_cheek_flag, 'translateX', 0, -10, 'left_blow')
		parameter_node.config_output_blendnode(head_blendnode.left_blow, 'left_blow')
		parameter_node.config_input(l_cheek_flag, 'translateX', 0, 10, 'left_suck')
		parameter_node.config_output_blendnode(head_blendnode.left_suck, 'left_suck')

		parameter_node.config_input(l_cheek_flag, 'translateY', 0, -10, 'left_cheek_down')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_down, 'left_cheek_down')
		parameter_node.config_input(l_cheek_flag, 'translateY', 0, 10, 'left_cheek_up')
		parameter_node.config_output_blendnode(head_blendnode.left_cheek_up, 'left_cheek_up')

		# Right
		r_outer_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_cheek_outer_null'),
															side='right',
															region='outer_cheek',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		r_outer_cheek.attach_component(neck_component, head_flag)
		r_outer_cheek_flag = r_outer_cheek.get_start_flag()
		
		parameter_node.config_input(r_outer_cheek_flag, 'translateY', 0, 10, 'right_cheek_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_outer_up, 'right_cheek_outer_up')
		parameter_node.config_input(r_outer_cheek_flag, 'translateY', 0, -10, 'right_cheek_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_outer_down, 'right_cheek_outer_down')
		
		r_inner_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_cheek_inner_null'),
															side='right',
															region='inner_cheek',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		r_inner_cheek.attach_component(neck_component, head_flag)
		r_inner_cheek_flag = r_inner_cheek.get_start_flag()
		
		parameter_node.config_input(r_inner_cheek_flag, 'translateY', 0, 10, 'right_cheek_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_inner_up, 'right_cheek_inner_up')
		parameter_node.config_input(r_inner_cheek_flag, 'translateY', 0, -10, 'right_cheek_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_inner_down, 'right_cheek_inner_down')
		
		r_cheek = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('r_cheek_null'),
														side='right',
														region='cheek',
														flag_scale=1,
														limit_point=((-10, 10), (-10, 10), (-10, 10)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		r_cheek.attach_component(neck_component, head_flag)
		r_cheek_flag = r_cheek.get_start_flag()
		
		parameter_node.config_input(r_cheek_flag, 'translateZ', 0, 10, 'right_cheek_shift_out')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_shift_out, 'right_cheek_shift_out')
		parameter_node.config_input(r_cheek_flag, 'translateZ', 0, -10, 'right_cheek_shift_in')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_shift_in, 'right_cheek_shift_in')
		
		parameter_node.config_input(r_cheek_flag, 'translateX', 0, 10, 'right_blow')
		parameter_node.config_output_blendnode(head_blendnode.right_blow, 'right_blow')
		parameter_node.config_input(r_cheek_flag, 'translateX', 0, -10, 'right_suck')
		parameter_node.config_output_blendnode(head_blendnode.right_suck, 'right_suck')

		parameter_node.config_input(r_cheek_flag, 'translateY', 0, -10, 'right_cheek_down')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_down, 'right_cheek_down')
		parameter_node.config_input(r_cheek_flag, 'translateY', 0, 10, 'right_cheek_up')
		parameter_node.config_output_blendnode(head_blendnode.right_cheek_up, 'right_cheek_up')
		
		#### Nasolabial ####
		ui.update_status(70, 'Creating Components - Nose')
		
		# Left
		l_nasolabial = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_nasolabial_null'),
															side='left',
															region='nasolabial',
															flag_scale=1,
															limit_point=((None, None), (0, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		l_nasolabial.attach_component(neck_component, head_flag)
		l_nasolabial_flag = l_nasolabial.get_start_flag()
		
		parameter_node.config_input(l_nasolabial_flag, 'translateY', 0, 10, 'left_nasolabial_out')
		parameter_node.config_output_blendnode(head_blendnode.left_nasolabial_out, 'left_nasolabial_out')
		
		# Right
		r_nasolabial = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_nasolabial_null'),
															side='right',
															region='nasolabial',
															flag_scale=1,
															limit_point=((None, None), (0, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		r_nasolabial.attach_component(neck_component, head_flag)
		r_nasolabial_flag = r_nasolabial.get_start_flag()
		
		parameter_node.config_input(r_nasolabial_flag, 'translateY', 0, 10, 'right_nasolabial_out')
		parameter_node.config_output_blendnode(head_blendnode.right_nasolabial_out, 'right_nasolabial_out')
		
		#### Nose ####
		# Center
		c_nose = frag.FaceFKComponent.create(frag_parent=frag_rig,
													joint=pm.PyNode('nose_null'),
													side='center',
													region='nose',
													flag_scale=1,
													limit_point=((-10, 10), (-10, 10), (None, None)),
													limit_orient=((None, None), (None, None), (None, None)),
													translate_scale=(10, 10, 10))
		c_nose.attach_component(neck_component, head_flag)
		c_nose_flag = c_nose.get_start_flag()
		
		parameter_node.config_input(c_nose_flag, 'translateY', 0, 10, 'nose_tip_up')
		parameter_node.config_output_blendnode(head_blendnode.nose_tip_up, 'nose_tip_up')
		parameter_node.config_input(c_nose_flag, 'translateY', 0, -10, 'nose_tip_down')
		parameter_node.config_output_blendnode(head_blendnode.nose_tip_down, 'nose_tip_down')
		
		parameter_node.config_input(c_nose_flag, 'translateX', 0, -10, 'nose_tip_right')
		parameter_node.config_output_blendnode(head_blendnode.nose_tip_right, 'nose_tip_right')
		parameter_node.config_input(c_nose_flag, 'translateX', 0, 10, 'nose_tip_left')
		parameter_node.config_output_blendnode(head_blendnode.nose_tip_left, 'nose_tip_left')
		
		# Left
		l_nose = frag.FaceFKComponent.create(frag_parent=frag_rig,
													joint=pm.PyNode('l_nose_null'),
													side='left',
													region='nostril',
													flag_scale=1,
													limit_point=((-10, 10), (-10, 10), (None, None)),
													limit_orient=((None, None), (None, None), (None, None)),
													translate_scale=(10, 10, 10))
		l_nose.attach_component(neck_component, head_flag)
		l_nose_flag = l_nose.get_start_flag()
		
		parameter_node.config_input(l_nose_flag, 'translateY', 0, 10, 'left_nose_sneer')
		parameter_node.config_output_blendnode(head_blendnode.left_nose_sneer, 'left_nose_sneer')
		parameter_node.config_input(l_nose_flag, 'translateY', 0, -10, 'left_nose_down')
		parameter_node.config_output_blendnode(head_blendnode.left_nose_down, 'left_nose_down')
		
		parameter_node.config_input(l_nose_flag, 'translateX', 0, 10, 'left_nose_flare')
		parameter_node.config_output_blendnode(head_blendnode.left_nose_flare, 'left_nose_flare')
		parameter_node.config_input(l_nose_flag, 'translateX', 0, -10, 'left_nose_suck')
		parameter_node.config_output_blendnode(head_blendnode.left_nose_suck, 'left_nose_suck')
		
		# Right
		r_nose = frag.FaceFKComponent.create(frag_parent=frag_rig,
													joint=pm.PyNode('r_nose_null'),
													side='right',
													region='nostril',
													flag_scale=1,
													limit_point=((-10, 10), (-10, 10), (None, None)),
													limit_orient=((None, None), (None, None), (None, None)),
													translate_scale=(10, 10, 10))
		r_nose.attach_component(neck_component, head_flag)
		r_nose_flag = r_nose.get_start_flag()
		
		parameter_node.config_input(r_nose_flag, 'translateY', 0, 10, 'right_nose_sneer')
		parameter_node.config_output_blendnode(head_blendnode.right_nose_sneer, 'right_nose_sneer')
		parameter_node.config_input(r_nose_flag, 'translateY', 0, -10, 'right_nose_down')
		parameter_node.config_output_blendnode(head_blendnode.right_nose_down, 'right_nose_down')
		
		parameter_node.config_input(r_nose_flag, 'translateX', 0, 10, 'right_nose_flare')
		parameter_node.config_output_blendnode(head_blendnode.right_nose_flare, 'right_nose_flare')
		parameter_node.config_input(r_nose_flag, 'translateX', 0, -10, 'right_nose_suck')
		parameter_node.config_output_blendnode(head_blendnode.right_nose_suck, 'right_nose_suck')
		
		#### Lips ####
		ui.update_status(80, 'Creating Components - Mouth')
		
		# Center
		center_lips = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('c_lips_null'),
															side='center',
															region='lips',
															flag_scale=1,
															limit_point=((-10, 10), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		center_lips.attach_component(neck_component, head_flag)
		center_lips.flag_follow_mesh(head_blendshape.mesh)
		center_lips_flag = center_lips.get_start_flag()
		
		parameter_node.config_input(center_lips_flag, 'translateY', 0, 10, 'lips_up')
		parameter_node.config_output_blendnode(head_blendnode.lips_up, 'lips_up')
		parameter_node.config_input(center_lips_flag, 'translateY', 0, -10, 'lips_down')
		parameter_node.config_output_blendnode(head_blendnode.lips_down, 'lips_down')
		
		parameter_node.config_input(center_lips_flag, 'translateX', 0, 10, 'left_lips')
		parameter_node.config_output_blendnode(head_blendnode.left_lips, 'left_lips')
		parameter_node.config_input(center_lips_flag, 'translateX', 0, -10, 'right_lips')
		parameter_node.config_output_blendnode(head_blendnode.right_lips, 'right_lips')
		
		parameter_node.config_input(center_lips_flag, 'lips_upper_forward_back', 0, 10, 'upper_lip_forward')
		parameter_node.config_output_blendnode(head_blendnode.upper_lip_forward, 'upper_lip_forward')
		parameter_node.config_input(center_lips_flag, 'lips_upper_forward_back', 0, -10, 'upper_lip_back')
		parameter_node.config_output_blendnode(head_blendnode.upper_lip_back, 'upper_lip_back')
		
		parameter_node.config_input(center_lips_flag, 'lips_lower_forward_back', 0, 10, 'lower_lip_forward')
		parameter_node.config_output_blendnode(head_blendnode.lower_lip_forward, 'lower_lip_forward')
		parameter_node.config_input(center_lips_flag, 'lips_lower_forward_back', 0, -10, 'lower_lip_back')
		parameter_node.config_output_blendnode(head_blendnode.lower_lip_back, 'lower_lip_back')
		
		parameter_node.config_input(center_lips_flag, 'lips_upper_funnel_curl', 0, 10, 'upper_lip_funnel')
		parameter_node.config_output_blendnode(head_blendnode.upper_lip_funnel, 'upper_lip_funnel')
		parameter_node.config_input(center_lips_flag, 'lips_upper_funnel_curl', 0, -10, 'upper_lip_curl')
		parameter_node.config_output_blendnode(head_blendnode.upper_lip_curl, 'upper_lip_curl')
		
		parameter_node.config_input(center_lips_flag, 'lips_lower_funnel_curl', 0, 10, 'lower_lip_funnel')
		parameter_node.config_output_blendnode(head_blendnode.lower_lip_funnel, 'lower_lip_funnel')
		parameter_node.config_input(center_lips_flag, 'lips_lower_funnel_curl', 0, -10, 'lower_lip_curl')
		parameter_node.config_output_blendnode(head_blendnode.lower_lip_curl, 'lower_lip_curl')
		
		parameter_node.config_input(center_lips_flag, 'lips_pucker_left', 0, 10, 'left_pucker')
		parameter_node.config_output_blendnode(head_blendnode.left_pucker, 'left_pucker')
		parameter_node.config_input(center_lips_flag, 'lips_pucker_right', 0, 10, 'right_pucker')
		parameter_node.config_output_blendnode(head_blendnode.right_pucker, 'right_pucker')
		
		parameter_node.config_input(center_lips_flag, 'natural_lips', 0, 10, 'natural_lips')
		parameter_node.config_output_blendnode(head_blendnode.natural_lips, 'natural_lips')

		parameter_node.config_input(center_lips_flag, 'center_mouth_close', 0, 10, 'center_mouth_close')
		parameter_node.config_output_blendnode(head_blendnode.center_mouth_close, 'center_mouth_close')

		# Left
		l_mouth_corner = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_mouth_corner_null'),
															side='left',
															region='outer_lips',
															flag_scale=1,
															limit_point=((-10, 10), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		l_mouth_corner.attach_component(neck_component, head_flag)
		l_mouth_corner_flag = l_mouth_corner.get_start_flag()
		
		parameter_node.config_input(l_mouth_corner_flag, 'translateY', 0, 10, 'left_mouth_up')
		parameter_node.config_output_blendnode(head_blendnode.left_mouth_up, 'left_mouth_up')
		parameter_node.config_input(l_mouth_corner_flag, 'translateY', 0, -10, 'left_mouth_down')
		parameter_node.config_output_blendnode(head_blendnode.left_mouth_down, 'left_mouth_down')
		
		parameter_node.config_input(l_mouth_corner_flag, 'translateX', 0, 10, 'left_mouth_stretch')
		parameter_node.config_output_blendnode(head_blendnode.left_mouth_stretch, 'left_mouth_stretch')
		parameter_node.config_input(l_mouth_corner_flag, 'translateX', 0, -10, 'left_mouth_oo')
		parameter_node.config_output_blendnode(head_blendnode.left_mouth_oo, 'left_mouth_oo')
		
		# Upper
		upper_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('upper_lip_null'),
														side='center',
														region='upper_lip',
														flag_scale=1,
														limit_point=((None, None), (-10, 10), (None, None)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		upper_lip.attach_component(neck_component, head_flag)
		upper_lip_flag = upper_lip.get_start_flag()
		
		parameter_node.config_input(upper_lip_flag, 'translateY', 0, 10, 'center_upper_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.center_upper_lip_up, 'center_upper_lip_up')
		parameter_node.config_input(upper_lip_flag, 'translateY', 0, -10, 'center_upper_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.center_upper_lip_down, 'center_upper_lip_down')
		
		l_upper_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_upper_lip_null'),
															side='left',
															region='upper_mid_lip',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		l_upper_lip.attach_component(neck_component, head_flag)
		l_upper_lip_flag = l_upper_lip.get_start_flag()
		
		parameter_node.config_input(l_upper_lip_flag, 'translateY', 0, 10, 'left_upper_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_lip_up, 'left_upper_lip_up')
		parameter_node.config_input(l_upper_lip_flag, 'translateY', 0, -10, 'left_upper_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_lip_down, 'left_upper_lip_down')
		
		parameter_node.config_input(l_upper_lip_flag, 'rotateZ', 0, 10, 'left_upper_corner_adjust_up')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_corner_adjust_up, 'left_upper_corner_adjust_up')
		parameter_node.config_input(l_upper_lip_flag, 'rotateZ', 0, -10, 'left_upper_corner_adjust_down')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_corner_adjust_down, 'left_upper_corner_adjust_down')
		
		# Lower
		lower_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('lower_lip_null'),
														side='center',
														region='lower_lip',
														flag_scale=1,
														limit_point=((None, None), (-10, 10), (None, None)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		lower_lip.attach_component(neck_component, head_flag)
		lower_lip.flag_follow_mesh(head_blendshape.mesh)
		lower_lip_flag = lower_lip.get_start_flag()
		
		parameter_node.config_input(lower_lip_flag, 'translateY', 0, 10, 'center_lower_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.center_lower_lip_up, 'center_lower_lip_up')
		parameter_node.config_input(lower_lip_flag, 'translateY', 0, -10, 'center_lower_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.center_lower_lip_down, 'center_lower_lip_down')
		
		l_lower_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('l_lower_lip_null'),
															side='left',
															region='lower_mid_lip',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		l_lower_lip.attach_component(neck_component, head_flag)
		l_lower_lip.flag_follow_mesh(head_blendshape.mesh)
		l_lower_lip_flag = l_lower_lip.get_start_flag()
		
		parameter_node.config_input(l_lower_lip_flag, 'translateY', 0, 10, 'left_lower_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_lip_up, 'left_lower_lip_up')
		parameter_node.config_input(l_lower_lip_flag, 'translateY', 0, -10, 'left_lower_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_lip_down, 'left_lower_lip_down')
		
		parameter_node.config_input(l_lower_lip_flag, 'rotateZ', 0, 10, 'left_lower_corner_adjust_up')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_corner_adjust_up, 'left_lower_corner_adjust_up')
		parameter_node.config_input(l_lower_lip_flag, 'rotateZ', 0, -10, 'left_lower_corner_adjust_down')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_corner_adjust_down, 'left_lower_corner_adjust_down')
		
		# Right
		r_mouth_corner = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_mouth_corner_null'),
															side='right',
															region='outer_lips',
															flag_scale=1,
															limit_point=((-10, 10), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (None, None)),
															translate_scale=(10, 10, 10))
		r_mouth_corner.attach_component(neck_component, head_flag)
		r_mouth_corner_flag = r_mouth_corner.get_start_flag()
		
		parameter_node.config_input(r_mouth_corner_flag, 'translateY', 0, 10, 'right_mouth_up')
		parameter_node.config_output_blendnode(head_blendnode.right_mouth_up, 'right_mouth_up')
		parameter_node.config_input(r_mouth_corner_flag, 'translateY', 0, -10, 'right_mouth_down')
		parameter_node.config_output_blendnode(head_blendnode.right_mouth_down, 'right_mouth_down')
		
		parameter_node.config_input(r_mouth_corner_flag, 'translateX', 0, 10, 'right_mouth_stretch')
		parameter_node.config_output_blendnode(head_blendnode.right_mouth_stretch, 'right_mouth_stretch')
		parameter_node.config_input(r_mouth_corner_flag, 'translateX', 0, -10, 'right_mouth_oo')
		parameter_node.config_output_blendnode(head_blendnode.right_mouth_oo, 'right_mouth_oo')
		
		# Upper
		r_upper_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
																joint=pm.PyNode('r_upper_lip_null'),
																side='right',
																region='upper_mid_lip',
																flag_scale=1,
																limit_point=((None, None), (-10, 10), (None, None)),
																limit_orient=((None, None), (None, None), (-60, 60)),
																translate_scale=(10, 10, 10))
		r_upper_lip.attach_component(neck_component, head_flag)
		r_upper_lip_flag = r_upper_lip.get_start_flag()
		
		parameter_node.config_input(r_upper_lip_flag, 'translateY', 0, 10, 'right_upper_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_lip_up, 'right_upper_lip_up')
		parameter_node.config_input(r_upper_lip_flag, 'translateY', 0, -10, 'right_upper_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_lip_down, 'right_upper_lip_down')
		
		parameter_node.config_input(r_upper_lip_flag, 'rotateZ', 0, 10, 'right_upper_corner_adjust_up')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_corner_adjust_up, 'right_upper_corner_adjust_up')
		parameter_node.config_input(r_upper_lip_flag, 'rotateZ', 0, -10, 'right_upper_corner_adjust_down')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_corner_adjust_down, 'right_upper_corner_adjust_down')
		
		r_lower_lip = frag.FaceFKComponent.create(frag_parent=frag_rig,
															joint=pm.PyNode('r_lower_lip_null'),
															side='right',
															region='lower_mid_lip',
															flag_scale=1,
															limit_point=((None, None), (-10, 10), (None, None)),
															limit_orient=((None, None), (None, None), (-60, 60)),
															translate_scale=(10, 10, 10))
		r_lower_lip.attach_component(neck_component, head_flag)
		r_lower_lip.flag_follow_mesh(head_blendshape.mesh)
		
		r_lower_lip_flag = r_lower_lip.get_start_flag()
		
		parameter_node.config_input(r_lower_lip_flag, 'translateY', 0, 10, 'right_lower_lip_up')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_lip_up, 'right_lower_lip_up')
		parameter_node.config_input(r_lower_lip_flag, 'translateY', 0, -10, 'right_lower_lip_down')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_lip_down, 'right_lower_lip_down')
		
		parameter_node.config_input(r_lower_lip_flag, 'rotateZ', 0, 10, 'right_lower_corner_adjust_up')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_corner_adjust_up, 'right_lower_corner_adjust_up')
		parameter_node.config_input(r_lower_lip_flag, 'rotateZ', 0, -10, 'right_lower_corner_adjust_down')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_corner_adjust_down, 'right_lower_corner_adjust_down')
		
		# Mouth
		c_mouth = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('mouth_null'),
														side='center',
														region='mouth',
														flag_scale=1,
														limit_point=((None, None), (-10, 10), (-10, 10)),
														limit_orient=((-15, 20), (-15, 15), (-15, 15)),
														translate_scale=(10, 10, 10))
		c_mouth.attach_component(neck_component, head_flag)
		c_mouth_flag = c_mouth.get_start_flag()
		
		# jaw
		parameter_node.config_input(c_mouth_flag, 'rotateX', 0, 20, 'jaw_open')
		parameter_node.config_output_blendnode(head_blendnode.jaw_open, 'jaw_open')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_open, 'jaw_open')
		parameter_node.config_input(c_mouth_flag, 'rotateX', 0, -15, 'jaw_clench')
		parameter_node.config_output_blendnode(head_blendnode.jaw_clench, 'jaw_clench')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_clench, 'jaw_clench')
		
		parameter_node.config_input(c_mouth_flag, 'rotateZ', 0, 15, 'left_jaw_tilt')
		parameter_node.config_output_blendnode(head_blendnode.left_jaw_tilt, 'left_jaw_tilt')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left_jaw_tilt, 'left_jaw_tilt')
		parameter_node.config_input(c_mouth_flag, 'rotateZ', 0, -15, 'right_jaw_tilt')
		parameter_node.config_output_blendnode(head_blendnode.right_jaw_tilt, 'right_jaw_tilt')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right_jaw_tilt, 'right_jaw_tilt')
		
		parameter_node.config_input(c_mouth_flag, 'rotateY', 0, 15, 'left_jaw')
		parameter_node.config_output_blendnode(head_blendnode.left_jaw, 'left_jaw')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left_jaw, 'left_jaw')
		parameter_node.config_input(c_mouth_flag, 'rotateY', 0, -15, 'right_jaw')
		parameter_node.config_output_blendnode(head_blendnode.right_jaw, 'right_jaw')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right_jaw, 'right_jaw')
		
		parameter_node.config_input(c_mouth_flag, 'translateY', 0, 10, 'jaw_up')
		parameter_node.config_output_blendnode(head_blendnode.jaw_up, 'jaw_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_up, 'jaw_up')
		parameter_node.config_input(c_mouth_flag, 'translateY', 0, -10, 'jaw_down')
		parameter_node.config_output_blendnode(head_blendnode.jaw_down, 'jaw_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_down, 'jaw_down')

		parameter_node.config_input(c_mouth_flag, 'translateZ', 0, 10, 'jaw_forward')
		parameter_node.config_output_blendnode(head_blendnode.jaw_forward, 'jaw_forward')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_forward, 'jaw_forward')
		parameter_node.config_input(c_mouth_flag, 'translateZ', 0, -10, 'jaw_back')
		parameter_node.config_output_blendnode(head_blendnode.jaw_back, 'jaw_back')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_back, 'jaw_back')

		# chin
		parameter_node.config_input(c_mouth_flag, 'chin_up_down', 0, 10, 'chin_up')
		parameter_node.config_output_blendnode(head_blendnode.chin_up, 'chin_up')
		parameter_node.config_input(c_mouth_flag, 'chin_up_down', 0, -10, 'chin_down')
		parameter_node.config_output_blendnode(head_blendnode.chin_down, 'chin_down')

		c_upper_jaw = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('upper_jaw_null'),
														side='center',
														region='upper_jaw',
														flag_scale=1,
														limit_point=((None, None), (None, None), (-10, 10)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		c_upper_jaw.attach_component(neck_component, head_flag)
		c_upper_jaw.flag_follow_mesh(head_blendshape.mesh)
		c_upper_jaw_flag = c_upper_jaw.get_start_flag()
		c_upper_jaw_flag.set_as_detail()

		parameter_node.config_input(c_upper_jaw_flag, 'translateZ', 0, 10, 'tongue_upper_jaw_forward')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_upper_jaw_forward, 'tongue_upper_jaw_forward')
		parameter_node.config_input(c_upper_jaw_flag, 'translateZ', 0, -10, 'tongue_upper_jaw_back')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_upper_jaw_back, 'tongue_upper_jaw_back')

		c_lower_jaw = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('lower_jaw_null'),
														side='center',
														region='lower_jaw',
														flag_scale=1,
														limit_point=((None, None), (None, None), (-10, 10)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		c_lower_jaw.attach_component(neck_component, head_flag)
		c_lower_jaw.flag_follow_mesh(head_blendshape.mesh)
		c_lower_jaw_flag = c_lower_jaw.get_start_flag()
		c_lower_jaw_flag.set_as_detail()

		parameter_node.config_input(c_lower_jaw_flag, 'translateZ', 0, 10, 'tongue_lower_jaw_forward')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_lower_jaw_forward, 'tongue_lower_jaw_forward')
		parameter_node.config_input(c_lower_jaw_flag, 'translateZ', 0, -10, 'tongue_lower_jaw_back')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_lower_jaw_back, 'tongue_lower_jaw_back')

		c_jaw_squash = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('jaw_squash_null'),
														side='center',
														region='squash_stretch',
														flag_scale=1,
														limit_point=((-10, 10), (-10, 10), (None, None)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		c_jaw_squash.attach_component(neck_component, head_flag)
		c_jaw_squash.flag_follow_mesh(head_blendshape.mesh)
		c_jaw_squash_flag = c_jaw_squash.get_start_flag()
		
		parameter_node.config_input(c_jaw_squash_flag, 'translateY', 0, -10, 'jaw_stretch')
		parameter_node.config_output_blendnode(head_blendnode.jaw_stretch, 'jaw_stretch')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_stretch, 'jaw_stretch')
		parameter_node.config_input(c_jaw_squash_flag, 'translateY', 0, 10, 'jaw_squash')
		parameter_node.config_output_blendnode(head_blendnode.jaw_squash, 'jaw_squash')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_jaw_squash, 'jaw_squash')
		
		parameter_node.config_input(c_jaw_squash_flag, 'translateX', 0, 10, 'left_jaw_squash_tilt')
		parameter_node.config_output_blendnode(head_blendnode.left_jaw_squash_tilt, 'left_jaw_squash_tilt')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left_jaw_squash_tilt, 'left_jaw_squash_tilt')
		parameter_node.config_input(c_jaw_squash_flag, 'translateX', 0, -10, 'right_jaw_squash_tilt')
		parameter_node.config_output_blendnode(head_blendnode.right_jaw_squash_tilt, 'right_jaw_squash_tilt')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right_jaw_squash_tilt, 'right_jaw_squash_tilt')

		# Eyelids Up/Down

		l_eyelid_upper = frag.FaceFKComponent.create(frag_parent=frag_rig,
													  joint=pm.PyNode('l_eyelid_upper_null'),
													  side='left',
													  region='eyelid_upper',
													  flag_scale=1,
													  limit_point=((None, None), (-10, 10), (None, None)),
													  limit_orient=((None, None), (None, None), (None, None)),
													  translate_scale=(10, 10, 10))
		l_eyelid_upper.attach_component(neck_component, head_flag)
		l_eyelid_upper_flag = l_eyelid_upper.get_start_flag()

		parameter_node.config_input(l_eyelid_upper_flag, 'translateY', 0, -10, 'left_upper_eyelid_down')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_down, 'left_upper_eyelid_down')
		parameter_node.config_input(l_eyelid_upper_flag, 'translateY', 0, 10, 'left_upper_eyelid_up')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_up, 'left_upper_eyelid_up')

		l_eyelid_lower = frag.FaceFKComponent.create(frag_parent=frag_rig,
													  joint=pm.PyNode('l_eyelid_lower_null'),
													  side='left',
													  region='eyelid_lower',
													  flag_scale=1,
													  limit_point=((None, None), (-10, 10), (None, None)),
													  limit_orient=((None, None), (None, None), (None, None)),
													  translate_scale=(10, 10, 10))
		l_eyelid_lower.attach_component(neck_component, head_flag)
		l_eyelid_lower_flag = l_eyelid_lower.get_start_flag()
		parameter_node.config_input(l_eyelid_lower_flag, 'translateY', 0, -10, 'left_lower_eyelid_up')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_up, 'left_lower_eyelid_up')
		parameter_node.config_input(l_eyelid_lower_flag, 'translateY', 0, 10, 'left_lower_eyelid_down')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_down, 'left_lower_eyelid_down')

		r_eyelid_upper = frag.FaceFKComponent.create(frag_parent=frag_rig,
													  joint=pm.PyNode('r_eyelid_upper_null'),
													  side='right',
													  region='eyelid_upper',
													  flag_scale=1,
													  limit_point=((None, None), (-10, 10), (None, None)),
													  limit_orient=((None, None), (None, None), (None, None)),
													  translate_scale=(10, 10, 10))
		r_eyelid_upper.attach_component(neck_component, head_flag)
		r_eyelid_upper_flag = r_eyelid_upper.get_start_flag()
		parameter_node.config_input(r_eyelid_upper_flag, 'translateY', 0, -10, 'right_upper_eyelid_down')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_down, 'right_upper_eyelid_down')
		parameter_node.config_input(r_eyelid_upper_flag, 'translateY', 0, 10, 'right_upper_eyelid_up')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_up, 'right_upper_eyelid_up')

		r_eyelid_lower = frag.FaceFKComponent.create(frag_parent=frag_rig,
													  joint=pm.PyNode('r_eyelid_lower_null'),
													  side='right',
													  region='eyelid_lower',
													  flag_scale=1,
													  limit_point=((None, None), (-10, 10), (None, None)),
													  limit_orient=((None, None), (None, None), (None, None)),
													  translate_scale=(10, 10, 10))
		r_eyelid_lower.attach_component(neck_component, head_flag)
		r_eyelid_lower_flag = r_eyelid_lower.get_start_flag()
		parameter_node.config_input(r_eyelid_lower_flag, 'translateY', 0, -10, 'right_lower_eyelid_up')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_up, 'right_lower_eyelid_up')
		parameter_node.config_input(r_eyelid_lower_flag, 'translateY', 0, 10, 'right_lower_eyelid_down')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_down, 'right_lower_eyelid_down')


		# Eye Lids
		l_eyelids = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('l_eyelid_null'),
														side='left',
														region='eyelids',
														flag_scale=1,
														limit_point=((None, None), (None, None), (None, None)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		l_eyelids.attach_component(neck_component, head_flag)
		l_eyelids_flag = l_eyelids.get_start_flag()
		
		parameter_node.config_input(l_eyelids_flag, 'lower_eyelid_twist', 0, 10, 'left_lower_eyelid_twist_anger')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_twist_anger,'left_lower_eyelid_twist_anger')
		parameter_node.config_input(l_eyelids_flag, 'lower_eyelid_twist', 0, -10, 'left_lower_eyelid_twist_sad')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_twist_sad, 'left_lower_eyelid_twist_sad')
		
		parameter_node.config_input(l_eyelids_flag, 'upper_eyelid_twist', 0, 10, 'left_upper_eyelid_twist_anger')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_twist_anger,'left_upper_eyelid_twist_anger')
		parameter_node.config_input(l_eyelids_flag, 'upper_eyelid_twist', 0, -10, 'left_upper_eyelid_twist_sad')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_twist_sad, 'left_upper_eyelid_twist_sad')
		
		parameter_node.config_input(l_eyelids_flag, 'upper_inner_up_down', 0, -10, 'left_upper_eyelid_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_inner_up, 'left_upper_eyelid_inner_up')
		parameter_node.config_input(l_eyelids_flag, 'upper_inner_up_down', 0, 10, 'left_upper_eyelid_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_inner_down, 'left_upper_eyelid_inner_down')
		
		parameter_node.config_input(l_eyelids_flag, 'upper_outer_up_down', 0, -10, 'left_upper_eyelid_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_outer_up, 'left_upper_eyelid_outer_up')
		parameter_node.config_input(l_eyelids_flag, 'upper_outer_up_down', 0, 10, 'left_upper_eyelid_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.left_upper_eyelid_outer_down, 'left_upper_eyelid_outer_down')
		
		parameter_node.config_input(l_eyelids_flag, 'lower_inner_up_down', 0, -10, 'left_lower_eyelid_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_inner_up, 'left_lower_eyelid_inner_up')
		parameter_node.config_input(l_eyelids_flag, 'lower_inner_up_down', 0, 10, 'left_lower_eyelid_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_inner_down, 'left_lower_eyelid_inner_down')
		
		parameter_node.config_input(l_eyelids_flag, 'lower_outer_up_down', 0, -10, 'left_lower_eyelid_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_outer_up, 'left_lower_eyelid_outer_up')
		parameter_node.config_input(l_eyelids_flag, 'lower_outer_up_down', 0, 10, 'left_lower_eyelid_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.left_lower_eyelid_outer_down, 'left_lower_eyelid_outer_down')
		
		r_eyelids = frag.FaceFKComponent.create(frag_parent=frag_rig,
														joint=pm.PyNode('r_eyelid_null'),
														side='right',
														region='eyelids',
														flag_scale=1,
														limit_point=((None, None), (None, None), (None, None)),
														limit_orient=((None, None), (None, None), (None, None)),
														translate_scale=(10, 10, 10))
		r_eyelids.attach_component(neck_component, head_flag)
		r_eyelids_flag = r_eyelids.get_start_flag()
		
		parameter_node.config_input(r_eyelids_flag, 'lower_eyelid_twist', 0, 10, 'right_lower_eyelid_twist_anger')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_twist_anger,'right_lower_eyelid_twist_anger')
		parameter_node.config_input(r_eyelids_flag, 'lower_eyelid_twist', 0, -10, 'right_lower_eyelid_twist_sad')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_twist_sad, 'right_lower_eyelid_twist_sad')
		
		parameter_node.config_input(r_eyelids_flag, 'upper_eyelid_twist', 0, 10, 'right_upper_eyelid_twist_anger')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_twist_anger,'right_upper_eyelid_twist_anger')
		parameter_node.config_input(r_eyelids_flag, 'upper_eyelid_twist', 0, -10, 'right_upper_eyelid_twist_sad')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_twist_sad, 'right_upper_eyelid_twist_sad')
		
		parameter_node.config_input(r_eyelids_flag, 'upper_inner_up_down', 0, -10, 'right_upper_eyelid_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_inner_up, 'right_upper_eyelid_inner_up')
		parameter_node.config_input(r_eyelids_flag, 'upper_inner_up_down', 0, 10, 'right_upper_eyelid_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_inner_down,'right_upper_eyelid_inner_down')
		
		parameter_node.config_input(r_eyelids_flag, 'upper_outer_up_down', 0, -10, 'right_upper_eyelid_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_outer_up, 'right_upper_eyelid_outer_up')
		parameter_node.config_input(r_eyelids_flag, 'upper_outer_up_down', 0, 10, 'right_upper_eyelid_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.right_upper_eyelid_outer_down,'right_upper_eyelid_outer_down')
		
		parameter_node.config_input(r_eyelids_flag, 'lower_inner_up_down', 0, -10, 'right_lower_eyelid_inner_up')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_inner_up, 'right_lower_eyelid_inner_up')
		parameter_node.config_input(r_eyelids_flag, 'lower_inner_up_down', 0, 10, 'right_lower_eyelid_inner_down')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_inner_down,'right_lower_eyelid_inner_down')
		
		parameter_node.config_input(r_eyelids_flag, 'lower_outer_up_down', 0, -10, 'right_lower_eyelid_outer_up')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_outer_up, 'right_lower_eyelid_outer_up')
		parameter_node.config_input(r_eyelids_flag, 'lower_outer_up_down', 0, 10, 'right_lower_eyelid_outer_down')
		parameter_node.config_output_blendnode(head_blendnode.right_lower_eyelid_outer_down,'right_lower_eyelid_outer_down')
		
		### Multi Constraints ###############
		# Eye Look
		frag.MultiConstraint.create(frag_rig,
											side='center',
											region='eye_look',
											source_object=center_eye_flag,
											target_list=[head_flag, world_flag],
											switch_attr='follow')
		
		ui.update_status(90, 'Finalizing Rig')
		
		connect_poses_to_root(frag_rig=frag_rig, parameter_node=parameter_node)
		
		flag_path = os.path.join(paths.get_asset_rig_path(self._asset_id), 'Flags')

		frag_rig.finalize_rig(flag_path)
		
		ui.update_status(100, 'Rig Complete')
		
		return frag_rig

class PlayerHeadTemplate(BaseHeadTemplate):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'head'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(PlayerHeadTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		pm.namespace(set=':')

		frag_rig = super(PlayerHeadTemplate, self).build(finalize=False)
		neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')[0]
		head_flag = neck_component.end_flag
		parameter_node = frag_rig.get_frag_children(of_type=frag.FragFaceParameters)[0]
		frag_root = frag.get_frag_root(frag_rig)
		skeletal_mesh_comp = frag_root.get_skeletal_mesh()
		face_mesh_comp = skeletal_mesh_comp.get_frag_children(of_type=frag.FaceMeshComponent)[0]
		head_blendshape = face_mesh_comp.head_blendshape
		head_blendnode_inst = head_blendshape.get_blendnode()

		head_blendnode = head_blendnode_inst.blendnode
		# Get the mouth blendnode
		mouth_blendshape = face_mesh_comp.mouth_blendshape
		mouth_blendshape_inst = mouth_blendshape.get_blendnode()

		mouth_blendnode = mouth_blendshape_inst.blendnode
		tongue_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('tongue_null'),
		                                               side='left',
		                                               region='tongue',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (None, None), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		tongue_component.attach_component(neck_component, head_flag)
		tongue_flag = tongue_component.get_start_flag()

		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, -10, 'tongue_curl_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_down, 'tongue_curl_down')
		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, 10, 'tongue_curl_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_up, 'tongue_curl_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, 10, 'tongue_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_up, 'tongue_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, -10, 'tongue_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_down, 'tongue_down')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, 10, 'tongue_out')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_out, 'tongue_out')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, -10, 'tongue_in')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_in, 'tongue_in')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, 10, 'tongue_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left, 'tongue_left')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, -10, 'tongue_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right, 'tongue_right')
		parameter_node.config_input(tongue_flag, 'tongue_roof_mouth', 0, 10, 'tongue_roof')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_roof, 'tongue_roof')
		parameter_node.config_input(tongue_flag, 'tongue_between_teeth', 0, 10, 'tongue_teeth')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_teeth, 'tongue_teeth')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, 10, 'tongue_twist_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_left, 'tongue_twist_left')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, -10, 'tongue_twist_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_right, 'tongue_twist_right')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, 10, 'tongue_wide')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_wide, 'tongue_wide')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, -10, 'tongue_narrow')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_narrow, 'tongue_narrow')

		parameter_node.config_input(tongue_flag, 'p', 0, 10, 'p')
		parameter_node.config_output_blendnode(head_blendnode.p, 'p')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_p, 'p')
		parameter_node.config_input(tongue_flag, 'td', 0, 10, 'td')
		parameter_node.config_output_blendnode(head_blendnode.td, 'td')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_td, 'td')
		parameter_node.config_input(tongue_flag, 'k', 0, 10, 'k')
		parameter_node.config_output_blendnode(head_blendnode.k, 'k')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_k, 'k')
		parameter_node.config_input(tongue_flag, 'flap', 0, 10, 'flap')
		parameter_node.config_output_blendnode(head_blendnode.flap, 'flap')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_flap, 'flap')
		parameter_node.config_input(tongue_flag, 'fph', 0, 10, 'fph')
		parameter_node.config_output_blendnode(head_blendnode.fph, 'fph')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_fph, 'fph')
		parameter_node.config_input(tongue_flag, 'th', 0, 10, 'th')
		parameter_node.config_output_blendnode(head_blendnode.th, 'th')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_th, 'th')
		parameter_node.config_input(tongue_flag, 'ss', 0, 10, 'ss')
		parameter_node.config_output_blendnode(head_blendnode.ss, 'ss')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ss, 'ss')
		parameter_node.config_input(tongue_flag, 'shch', 0, 10, 'shch')
		parameter_node.config_output_blendnode(head_blendnode.shch, 'shch')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_shch, 'shch')
		parameter_node.config_input(tongue_flag, 'rr', 0, 10, 'rr')
		parameter_node.config_output_blendnode(head_blendnode.rr, 'rr')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_rr, 'rr')
		parameter_node.config_input(tongue_flag, 'er', 0, 10, 'er')
		parameter_node.config_output_blendnode(head_blendnode.er, 'er')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_er, 'er')
		parameter_node.config_input(tongue_flag, 'y', 0, 10, 'y')
		parameter_node.config_output_blendnode(head_blendnode.y, 'y')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_y, 'y')
		parameter_node.config_input(tongue_flag, 'ww', 0, 10, 'ww')
		parameter_node.config_output_blendnode(head_blendnode.ww, 'ww')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ww, 'ww')
		parameter_node.config_input(tongue_flag, 'h', 0, 10, 'h')
		parameter_node.config_output_blendnode(head_blendnode.h, 'h')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_h, 'h')
		parameter_node.config_input(tongue_flag, 'ee', 0, 10, 'ee')
		parameter_node.config_output_blendnode(head_blendnode.ee, 'ee')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ee, 'ee')
		parameter_node.config_input(tongue_flag, 'ei', 0, 10, 'ei')
		parameter_node.config_output_blendnode(head_blendnode.ei, 'ei')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ei, 'ei')
		parameter_node.config_input(tongue_flag, 'eh', 0, 10, 'eh')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'eh')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'eh')
		parameter_node.config_input(tongue_flag, 'ah', 0, 10, 'ah')
		parameter_node.config_output_blendnode(head_blendnode.ah, 'ah')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ah, 'ah')
		parameter_node.config_input(tongue_flag, 'ao', 0, 10, 'ao')
		parameter_node.config_output_blendnode(head_blendnode.ao, 'ao')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ao, 'ao')
		parameter_node.config_input(tongue_flag, 'oo', 0, 10, 'oo')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'oo')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'oo')
		frag_rig.rigTemplate.set(PlayerHeadTemplate.__name__)
		if finalize:
			frag_rig.finalize_rig(self.get_flags_path())
			

class AngelHeadTemplate(BaseHeadTemplate):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'head'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(AngelHeadTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		pm.namespace(set=':')

		frag_rig = super(AngelHeadTemplate, self).build(finalize=False)
		neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent,
		                                            region='neck')[0]
		mouth_corner_r_component = frag_rig.get_frag_children(of_type=frag.FaceFKComponent,
		                                                      region='outer_lips',
		                                                      side='right')[0]
		mouth_corner_l_component = frag_rig.get_frag_children(of_type=frag.FaceFKComponent,
		                                                      region='outer_lips',
		                                                      side='left')[0]

		head_flag = neck_component.end_flag
		mouth_corner_l_flag = mouth_corner_l_component.get_start_flag()
		mouth_corner_r_flag = mouth_corner_r_component.get_start_flag()
		parameter_node = frag_rig.get_frag_children(of_type=frag.FragFaceParameters)[0]
		face_mesh_comp = face_mesh_component.get_face_mesh_component(head_flag)
		head_blendshape = face_mesh_comp.head_blendshape
		head_blendnode_inst = head_blendshape.get_blendnode()
		for mouth_corner_flag in (mouth_corner_l_flag, mouth_corner_r_flag):
			mouth_corner_flag.rx.set(keyable=True, channelBox=True, lock=False)
			mouth_corner_flag.rx.setLocked(False)
			mouth_corner_flag.rx.setKeyable(True)
			attr_utils.set_limits(rig_flag=mouth_corner_flag,
			                      limit_point=((-10, 10), (-10, 10), (None, None)),
			                      limit_orient=((-10, 10), (None, None), (None, None)))


		head_blendnode = head_blendnode_inst.blendnode
		# Get the mouth blendnode
		mouth_blendshape = face_mesh_comp.mouth_blendshape
		mouth_blendshape_inst = mouth_blendshape.get_blendnode()

		mouth_blendnode = mouth_blendshape_inst.blendnode
		tongue_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('tongue_null'),
		                                               side='left',
		                                               region='tongue',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (None, None), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		tongue_component.attach_component(neck_component, head_flag)
		tongue_flag = tongue_component.get_start_flag()

		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, -10, 'tongue_curl_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_down, 'tongue_curl_down')
		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, 10, 'tongue_curl_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_up, 'tongue_curl_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, 10, 'tongue_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_up, 'tongue_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, -10, 'tongue_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_down, 'tongue_down')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, 10, 'tongue_out')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_out, 'tongue_out')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, -10, 'tongue_in')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_in, 'tongue_in')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, 10, 'tongue_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left, 'tongue_left')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, -10, 'tongue_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right, 'tongue_right')
		parameter_node.config_input(tongue_flag, 'tongue_roof_mouth', 0, 10, 'tongue_roof')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_roof, 'tongue_roof')
		parameter_node.config_input(tongue_flag, 'tongue_between_teeth', 0, 10, 'tongue_teeth')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_teeth, 'tongue_teeth')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, 10, 'tongue_twist_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_left, 'tongue_twist_left')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, -10, 'tongue_twist_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_right, 'tongue_twist_right')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, 10, 'tongue_wide')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_wide, 'tongue_wide')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, -10, 'tongue_narrow')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_narrow, 'tongue_narrow')

		parameter_node.config_input(tongue_flag, 'fph', 0, 10, 'fph')
		parameter_node.config_output_blendnode(head_blendnode.fph, 'fph')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_fph, 'fph')
		parameter_node.config_input(tongue_flag, 'th', 0, 10, 'th')
		parameter_node.config_output_blendnode(head_blendnode.th, 'th')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_th, 'th')
		parameter_node.config_input(tongue_flag, 'ss', 0, 10, 'ss')
		parameter_node.config_output_blendnode(head_blendnode.ss, 'ss')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ss, 'ss')
		parameter_node.config_input(tongue_flag, 'shch', 0, 10, 'shch')
		parameter_node.config_output_blendnode(head_blendnode.shch, 'shch')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_shch, 'shch')
		parameter_node.config_input(tongue_flag, 'rr', 0, 10, 'rr')
		parameter_node.config_output_blendnode(head_blendnode.rr, 'rr')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_rr, 'rr')
		parameter_node.config_input(tongue_flag, 'er', 0, 10, 'er')
		parameter_node.config_output_blendnode(head_blendnode.er, 'er')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_er, 'er')
		parameter_node.config_input(tongue_flag, 'y', 0, 10, 'y')
		parameter_node.config_output_blendnode(head_blendnode.y, 'y')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_y, 'y')
		parameter_node.config_input(tongue_flag, 'ww', 0, 10, 'ww')
		parameter_node.config_output_blendnode(head_blendnode.ww, 'ww')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ww, 'ww')
		parameter_node.config_input(tongue_flag, 'h', 0, 10, 'h')
		parameter_node.config_output_blendnode(head_blendnode.h, 'h')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_h, 'h')
		parameter_node.config_input(tongue_flag, 'ee', 0, 10, 'ee')
		parameter_node.config_output_blendnode(head_blendnode.ee, 'ee')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ee, 'ee')
		parameter_node.config_input(tongue_flag, 'ei', 0, 10, 'ei')
		parameter_node.config_output_blendnode(head_blendnode.ei, 'ei')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ei, 'ei')
		parameter_node.config_input(tongue_flag, 'eh', 0, 10, 'eh')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'eh')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'eh')
		parameter_node.config_input(tongue_flag, 'ah', 0, 10, 'ah')
		parameter_node.config_output_blendnode(head_blendnode.ah, 'ah')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ah, 'ah')
		parameter_node.config_input(tongue_flag, 'ao', 0, 10, 'ao')
		parameter_node.config_output_blendnode(head_blendnode.ao, 'ao')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ao, 'ao')
		parameter_node.config_input(tongue_flag, 'oo', 0, 10, 'oo')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'oo')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'oo')

		parameter_node.config_input(mouth_corner_l_flag, 'rx', 0, 10, 'p')
		parameter_node.config_output_blendnode(head_blendnode.p, 'p')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_p, 'p')
		parameter_node.config_input(mouth_corner_l_flag, 'rx', 0, -10, 'td')
		parameter_node.config_output_blendnode(head_blendnode.td, 'td')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_td, 'td')

		parameter_node.config_input(mouth_corner_r_flag, 'rx', 0, 10, 'k')
		parameter_node.config_output_blendnode(head_blendnode.k, 'k')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_k, 'k')
		parameter_node.config_input(mouth_corner_r_flag, 'rx', 0, -10, 'flap')
		parameter_node.config_output_blendnode(head_blendnode.flap, 'flap')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_flap, 'flap')
		frag_rig.rigTemplate.set(AngelHeadTemplate.__name__)
		if finalize:
			frag_rig.finalize_rig(self.get_flags_path())

class AngeloHeadTemplate(BaseHeadTemplate):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'head'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(AngeloHeadTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		pm.namespace(set=':')

		frag_rig = super(AngeloHeadTemplate, self).build(finalize=False)
		neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent,
		                                            region='neck')[0]

		l_eye_component = frag_rig.get_frag_children(of_type=frag.EyeComponent,
		                                            region='eye',
		                                             side='left')[0]

		r_eye_component = frag_rig.get_frag_children(of_type=frag.EyeComponent,
		                                            region='eye',
		                                             side='right')[0]

		c_eye_component = frag_rig.get_frag_children(of_type=frag.EyeCenterComponent,
		                                            region='eyes',
		                                             side='center')[0]
		l_rotate_obj = l_eye_component.get_rotate_object()

		r_rotate_obj = r_eye_component.get_rotate_object()

		c_eye_flag = c_eye_component.get_flag()
		head_flag = neck_component.end_flag
		parameter_node = frag_rig.get_frag_children(of_type=frag.FragFaceParameters)[0]
		face_mesh_comp = face_mesh_component.get_face_mesh_component(head_flag)
		head_blendshape = face_mesh_comp.head_blendshape
		head_blendnode_inst = head_blendshape.get_blendnode()

		head_blendnode = head_blendnode_inst.blendnode
		# Get the mouth blendnode
		mouth_blendshape = face_mesh_comp.mouth_blendshape
		mouth_blendshape_inst = mouth_blendshape.get_blendnode()

		mouth_blendnode = mouth_blendshape_inst.blendnode
		tongue_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('tongue_null'),
		                                               side='left',
		                                               region='tongue',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (None, None), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		tongue_component.attach_component(neck_component, head_flag)
		tongue_flag = tongue_component.get_start_flag()

		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, -10, 'tongue_curl_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_down, 'tongue_curl_down')
		parameter_node.config_input(tongue_flag, 'tongue_curl_up_down', 0, 10, 'tongue_curl_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_curl_up, 'tongue_curl_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, 10, 'tongue_up')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_up, 'tongue_up')
		parameter_node.config_input(tongue_flag, 'tongue_up_down', 0, -10, 'tongue_down')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_down, 'tongue_down')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, 10, 'tongue_out')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_out, 'tongue_out')
		parameter_node.config_input(tongue_flag, 'tongue_in_out', 0, -10, 'tongue_in')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_in, 'tongue_in')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, 10, 'tongue_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_left, 'tongue_left')
		parameter_node.config_input(tongue_flag, 'tongue_left_right', 0, -10, 'tongue_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_right, 'tongue_right')
		parameter_node.config_input(tongue_flag, 'tongue_roof_mouth', 0, 10, 'tongue_roof')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_roof, 'tongue_roof')
		parameter_node.config_input(tongue_flag, 'tongue_between_teeth', 0, 10, 'tongue_teeth')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_teeth, 'tongue_teeth')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, 10, 'tongue_twist_left')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_left, 'tongue_twist_left')
		parameter_node.config_input(tongue_flag, 'tongue_twist_left_right', 0, -10, 'tongue_twist_right')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_twist_right, 'tongue_twist_right')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, 10, 'tongue_wide')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_wide, 'tongue_wide')
		parameter_node.config_input(tongue_flag, 'tongue_width', 0, -10, 'tongue_narrow')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_narrow, 'tongue_narrow')
		driven_attrs = {'start': {}, 'end': {}}
		driven_attrs['start']['ty'] = 0.0
		driven_attrs['end']['ty'] = 0.15

		l_eye_align_grp = rig_utils.create_align_transform(l_rotate_obj)
		l_eye_sdk = frag.SingleSDKComponent.create(frag_parent=frag_rig,
		                                         drive_attr=c_eye_flag.ty,
		                                         driven_obj=l_eye_align_grp,
		                                         side='left',
		                                         region='eye',
		                                         driven_attrs=driven_attrs,
		                                         drive_attr_values=(10,20))
		parameter_node.config_input(l_rotate_obj, 'rx', -25, -55, 'th')
		parameter_node.config_output_blendnode(head_blendnode.th, 'th')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_th, 'th')

		r_eye_align_grp = rig_utils.create_align_transform(r_rotate_obj)
		r_eye_sdk = frag.SingleSDKComponent.create(frag_parent=frag_rig,
		                                         drive_attr=c_eye_flag.ty,
		                                         driven_obj=r_eye_align_grp,
		                                         side='right',
		                                         region='eye',
		                                         driven_attrs=driven_attrs,
		                                         drive_attr_values=(10,20))
		parameter_node.config_input(r_rotate_obj, 'rx', -25, -55, 'ss')
		parameter_node.config_output_blendnode(head_blendnode.ss, 'ss')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ss, 'ss')

		parameter_node.config_input(tongue_flag, 'shch', 0, 10, 'shch')
		parameter_node.config_output_blendnode(head_blendnode.shch, 'shch')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_shch, 'shch')
		parameter_node.config_input(tongue_flag, 'rr', 0, 10, 'rr')
		parameter_node.config_output_blendnode(head_blendnode.rr, 'rr')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_rr, 'rr')
		parameter_node.config_input(tongue_flag, 'er', 0, 10, 'er')
		parameter_node.config_output_blendnode(head_blendnode.er, 'er')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_er, 'er')
		parameter_node.config_input(tongue_flag, 'y', 0, 10, 'y')
		parameter_node.config_output_blendnode(head_blendnode.y, 'y')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_y, 'y')
		parameter_node.config_input(tongue_flag, 'ww', 0, 10, 'ww')
		parameter_node.config_output_blendnode(head_blendnode.ww, 'ww')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ww, 'ww')
		parameter_node.config_input(tongue_flag, 'h', 0, 10, 'h')
		parameter_node.config_output_blendnode(head_blendnode.h, 'h')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_h, 'h')
		parameter_node.config_input(tongue_flag, 'ee', 0, 10, 'ee')
		parameter_node.config_output_blendnode(head_blendnode.ee, 'ee')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ee, 'ee')
		parameter_node.config_input(tongue_flag, 'ei', 0, 10, 'ei')
		parameter_node.config_output_blendnode(head_blendnode.ei, 'ei')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ei, 'ei')
		parameter_node.config_input(tongue_flag, 'eh', 0, 10, 'eh')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'eh')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'eh')
		parameter_node.config_input(tongue_flag, 'ah', 0, 10, 'ah')
		parameter_node.config_output_blendnode(head_blendnode.ah, 'ah')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ah, 'ah')
		parameter_node.config_input(tongue_flag, 'ao', 0, 10, 'ao')
		parameter_node.config_output_blendnode(head_blendnode.ao, 'ao')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_ao, 'ao')
		parameter_node.config_input(tongue_flag, 'oo', 0, 10, 'oo')
		parameter_node.config_output_blendnode(head_blendnode.eh, 'oo')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_eh, 'oo')

		jaw_break_right_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('r_jaw_break_null'),
		                                               side='right',
		                                               region='jaw_break',
		                                               flag_scale=1,
		                                               limit_point=((0, 10), (None, None), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		jaw_break_right_component.attach_component(neck_component, head_flag)
		jaw_break_right_flag = jaw_break_right_component.get_start_flag()
		parameter_node.config_input(jaw_break_right_flag, 'tx', 0, 10, 'fph')
		parameter_node.config_output_blendnode(head_blendnode.fph, 'fph')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_fph, 'fph')

		jaw_break_left_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('l_jaw_break_null'),
		                                               side='left',
		                                               region='jaw_break',
		                                               flag_scale=1,
		                                               limit_point=((0, 10), (None, None), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		jaw_break_left_component.attach_component(neck_component, head_flag)
		jaw_break_left_flag = jaw_break_left_component.get_start_flag()
		parameter_node.config_input(jaw_break_left_flag, 'tx', 0, 10, 'flap')
		parameter_node.config_output_blendnode(head_blendnode.flap, 'flap')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_flap, 'flap')

		jaw_break_center_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('c_jaw_break_null'),
		                                               side='center',
		                                               region='jaw_break',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (-10, 0), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		jaw_break_center_component.attach_component(neck_component, head_flag)
		jaw_break_center_flag = jaw_break_center_component.get_start_flag()
		parameter_node.config_input(jaw_break_center_flag, 'ty', 0, -10, 'k')
		parameter_node.config_output_blendnode(head_blendnode.k, 'k')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_k, 'k')

		face_melt_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('c_face_melt_null'),
		                                               side='center',
		                                               region='face_melt',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (-10, 0), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		face_melt_component.attach_component(neck_component, head_flag)
		face_melt_flag = face_melt_component.get_start_flag()
		parameter_node.config_input(face_melt_flag, 'ty', 0, -10, 'td')
		parameter_node.config_output_blendnode(head_blendnode.td, 'td')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_td, 'td')

		eyes_deflate_component = frag.FaceFKComponent.create(frag_parent=frag_rig,
		                                               joint=pm.PyNode('c_eyes_deflate_null'),
		                                               side='center',
		                                               region='eyes_deflate',
		                                               flag_scale=1,
		                                               limit_point=((None, None), (-10, 0), (None, None)),
		                                               limit_orient=((None, None), (None, None), (None, None)),
		                                               translate_scale=(10, 10, 10))
		eyes_deflate_component.attach_component(neck_component, head_flag)
		eyes_deflate_flag = eyes_deflate_component.get_start_flag()
		parameter_node.config_input(eyes_deflate_flag, 'ty', 0, -10, 'p')
		parameter_node.config_output_blendnode(head_blendnode.p, 'p')
		parameter_node.config_output_blendnode(mouth_blendnode.tongue_p, 'p')

		frag_rig.rigTemplate.set(AngeloHeadTemplate.__name__)
		if finalize:
			frag_rig.finalize_rig(self.get_flags_path())

def get_source_data(asset_id):
	"""
	Returns source head data for an asset if it exists, False if not

	:param str asset_id: Asset ID whose rig source data to look for
	:return: dict or False
	"""

	source_data_path = os.path.join(paths.get_face_data_path(asset_id), source_data.FACE_FILE_NAME)
	if not os.path.exists(source_data_path):
		return False
	source_face = source_data.SourceFaceData.load(source_data_path)
	return source_face


def update_source_head_data(asset_id, source_head_name):
	"""
	Exports rig source data as json file for the asset to their Face_Data folder.

	:param str asset_id: Asset ID whose rig source data we are exporting
	:param str source_head_name: Source head for this asset.
	:return: True if data was exported, False if path not found
	"""

	path = os.path.join(paths.get_face_data_path(asset_id), source_data.FACE_FILE_NAME)
	if not os.path.exists(path):
		return False
	source_face = source_data.SourceFaceData.load(path)
	source_face.source_head = source_head_name
	source_face.export(path)
	return True


def new_source_head_data(asset_id, source_head_name):
	"""
	Creates Face_Data folder if needed and source data json file before exporting.

	:param asset_id: Asset ID whose rig source data we are exporting
	:param source_head_name: Source head for this asset.
	"""
	if not os.path.exists(paths.get_face_data_path(asset_id)):
		os.makedirs(paths.get_face_data_path(asset_id))
		
	path = fileio.create_file(source_data.FACE_FILE_NAME, directory=paths.get_face_data_path(asset_id))
	source_face = face_util.get_common_face_data()
	source_face.source_head = source_head_name
	source_face.export(path)


def handle_blendshapes(asset_id, source_head_name, generate_shapes=False, source_face_data=None):
	"""
	Either imports or generates blendshapes
	
	:param str asset_id: Asset Identifier.
	:param str source_head_name: name of the source head
	:param bool generate_shapes: If True, will generate the blend shapes, rather than import them.
	:param source_data.SourceFaceData source_face_data: Instance of the face data
	:return:  Returns a dictionary of what was created.
	:rtype: Dictionary
	"""
	
	if not source_face_data:
		source_face_data = get_source_data(asset_id=asset_id)
		
	# Get regions
	regions = source_face_data.regions_list
	
	# Gather all the meshes in the scene with markup
	rig_mesh_markup = mesh_markup_rig.RigMeshMarkup.create()
	
	# Get all of the blend shapes and the region they are in.
	region_blendshape_dict = rig_mesh_markup.get_blendshape_region_dict()
	mesh_regions = list(region_blendshape_dict.keys())
	
	region_list = [x for x in regions if x in mesh_regions]
	
	blendnodes = []
	shape_results = {}
	shapes = []
	_dict = {}
	imported_source_list = []
	
	if not generate_shapes:
		for region in region_list:
			meshes = rig_mesh_markup.get_mesh_dict_list_in_region(region)
			# If not generating shapes, import them from the asset location
			for mesh, markup_inst in meshes.items():
				mesh = face_model.FaceModel(mesh)
				_dict = face_import_export.import_all_blendshapes(asset_id, region)
				if not _dict:
					return
				shape_results.update(_dict)
				shapes = shape_results.get('shapes')
				blend = blendshape_node.BlendShapeNode.create(shapes=shapes,
																mesh=mesh.mesh,
																label=mesh.part_type_name)
				blendnodes.append(blend)
			
		# If generating, import the source head and got through all the meshes and tranfer the blend shapes.
	elif generate_shapes:
		imported_meshes = source_meshes.import_source_head(source_head_name)
		imported_source_list = [x for x in imported_meshes if isinstance(x, pm.nt.Transform)]
		[x.tx.set(-25) for x in imported_source_list]
		# Get a list of all the meshes in the scene with markup
		target_meshes = face_util.get_all_scene_face_meshes()
		if not target_meshes:
			return
		
		target_meshes = list(map(lambda x: face_model.FaceModel(x), target_meshes))
		
		# Go through each mesh and generate the blend shapes
		for mesh in imported_source_list:
			mesh = face_model.FaceModel(mesh)
			type_name = mesh.type_name
			target_mesh = [x for x in target_meshes if x.type_name == type_name and x.category == frag.FACE_BLENDSHAPE_CATEGORY]
			if not target_mesh:
				continue
			_dict = source_meshes.generate_blendshapes(mesh.mesh, target_mesh[0].mesh)
			shape_results.update(_dict)
			shapes = shape_results.get('shapes')
			shapes = list(map(lambda x: str(x), shapes))

			blend = blendshape_node.BlendShapeNode.create(shapes=shapes,
															mesh=target_mesh[0].mesh,
															label=target_mesh[0].part_type_name)
			blendnodes.append(blend)
				
	pose_dict = {}
	pose_dict['shapes'] = shapes
	pose_dict['pose_grp'] = shape_results.get('pose_grp', None)
	pose_dict['blendnodes'] = blendnodes
	pose_dict['meshes'] = imported_source_list
	return pose_dict


def connect_poses_to_root(frag_rig, parameter_node):
	pose_names = parameter_node.get_parameter_names()
	pose_attributes = [parameter_node.pynode.attr(x).attr('value') for x in pose_names]
	
	channel_dicts = []
	for x, pose in enumerate(pose_attributes):
		channel_dicts.append(frag.create_channel_float_dict(obj_attr_name=pose,
																	joint_attr_name=pose_names[x],
																	attr_min=0.0,
																	attr_max=1.0,
																	default_value=0.0,
																	keyable=True))
	
	channel_component = frag.ChannelFloatComponent.create(frag_parent=frag_rig,
															obj=parameter_node.pynode,
															joint=pm.PyNode('root'),
															channel_dict_list=channel_dicts,
															component_name='face_parameters')






