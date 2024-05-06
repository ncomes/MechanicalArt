#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template for human players and npcs
"""

# System global imports
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup


# Internal module imports


class PlayerMaleTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = 'concept_ruby'
	ASSET_TYPE = 'player'
	
	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(PlayerMaleTemplate, self).__init__(asset_id, asset_type)
	
	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		# pm.newFile(f=True)
		# skm_file = paths.get_asset_skeletal_mesh_path()
		
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		world_root = pm.PyNode('root')
		
		frag_root = frag.FRAGRoot.create(world_root, self.asset_type, self.asset_id)
		frag.SkeletalMesh.create(frag_root)
		frag_rig = frag.FRAGRig.create(frag_root)
		
		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
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
		
		# Cog
		pelvis_joint = chain.get_start('pelvis', 'center')
		cog_component = frag.CogComponent.create(frag_rig,
													   pelvis_joint,
													   pelvis_joint,
													   'center',
													   'cog',
													   orientation=[-90, 0, 0])
		cog_component.attach_component(world_component, pm.PyNode(offset_flag))
		cog_flag = cog_component.get_flags()[0]
		
		# Pelvis
		start_joint = pm.PyNode('pelvis')
		head_chain = chain.get_start('head', 'center')
		pelvis_component = frag.PelvisComponent.create(frag_rig,
															 start_joint,
															 head_chain,
															 'center',
															 'pelvis',
															 orientation=[-90, 0, 0])
		pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
		pelvis_flag = pelvis_component.get_flags()[0]
		
		# head
		head_component = frag.FKComponent.create(frag_rig,
													   head_chain,
													   head_chain,
													   side='center',
													   region='head',
													   lock_child_translate_axes=[],
													   lock_root_translate_axes=['v'])
		head_component.attach_component(cog_component, pelvis_joint)
		head_flag = head_component.get_flags()[0]
		
		# Left gun
		l_gun_chain = chain.get_chain('gun', 'left')
		l_gun_component = frag.FKComponent.create(frag_rig,
														l_gun_chain[0],
														l_gun_chain[1],
														side='left',
														region='gun',
														lock_child_translate_axes=[],
														lock_root_translate_axes=['v'])
		l_gun_component.attach_component(head_component, head_chain)
		l_gun_flags = l_gun_component.get_flags()
		
		# Right gun
		r_gun_chain = chain.get_chain('gun', 'right')
		r_gun_component = frag.FKComponent.create(frag_rig,
														r_gun_chain[0],
														r_gun_chain[1],
														side='right',
														region='gun',
														lock_child_translate_axes=[],
														lock_root_translate_axes=['v'])
		r_gun_component.attach_component(head_component, head_chain)
		r_gun_flags = r_gun_component.get_flags()
		
		# left leg ball
		l_leg_ball_chain = chain.get_start('leg_ball', 'left')
		l_leg_ball_component = frag.FKComponent.create(frag_rig,
															 l_leg_ball_chain,
															 l_leg_ball_chain,
															 side='left',
															 region='leg_ball',
															 lock_child_translate_axes=[],
															 lock_root_translate_axes=['v'])
		l_leg_ball_component.attach_component(cog_component, pelvis_joint)
		l_leg_ball_flags = l_leg_ball_component.get_flags()[0]
		
		# right leg ball
		r_leg_ball_chain = chain.get_start('leg_ball', 'right')
		r_leg_ball_component = frag.FKComponent.create(frag_rig,
															 r_leg_ball_chain,
															 r_leg_ball_chain,
															 side='right',
															 region='leg_ball',
															 lock_child_translate_axes=[],
															 lock_root_translate_axes=['v'])
		r_leg_ball_component.attach_component(cog_component, pelvis_joint)
		r_leg_ball_flags = r_leg_ball_component.get_flags()[0]
		
		# left leg
		l_leg_chain = chain.get_chain('leg', 'left')
		l_leg_component = frag.IKFKComponent.create(frag_rig,
														  l_leg_chain[0],
														  l_leg_chain[1],
														  side='left',
														  region='leg',
														  ik_flag_pv_orient=[-90, 0, 0])
		l_leg_component.attach_component(l_leg_ball_component, l_leg_ball_chain)
		l_leg_flags = l_leg_component.get_flags()
		l_leg_ik_flag = l_leg_component.ik_flag
		l_leg_switch_flag = l_leg_component.switch_flag
		l_leg_fk_flag = l_leg_component.fk_flags
		
		# right leg
		r_leg_chain = chain.get_chain('leg', 'right')
		r_leg_component = frag.IKFKComponent.create(frag_rig,
														  r_leg_chain[0],
														  r_leg_chain[1],
														  side='right',
														  region='leg',
														  ik_flag_pv_orient=[-90, 0, 0])
		r_leg_component.attach_component(r_leg_ball_component, r_leg_ball_chain)
		r_leg_flags = r_leg_component.get_flags()
		r_leg_ik_flag = r_leg_component.ik_flag
		r_leg_switch_flag = r_leg_component.switch_flag
		r_leg_fk_flag = r_leg_component.fk_flags
		
		# left foot
		l_foot_chain = chain.get_start('foot', 'left')
		l_foot_component = frag.FKComponent.create(frag_rig,
														 l_foot_chain,
														 l_foot_chain,
														 side='left',
														 region='foot',
														 lock_child_translate_axes=[],
														 lock_root_translate_axes=['v'])
		l_foot_component.attach_component(l_leg_component, l_leg_chain[1])
		l_foot_flags = l_foot_component.get_flags()[0]
		
		# right foot
		r_foot_chain = chain.get_start('foot', 'right')
		r_foot_component = frag.FKComponent.create(frag_rig,
														 r_foot_chain,
														 r_foot_chain,
														 side='right',
														 region='foot',
														 lock_child_translate_axes=[],
														 lock_root_translate_axes=['v'])
		r_foot_component.attach_component(r_leg_component, r_leg_chain[1])
		r_foot_flags = r_foot_component.get_flags()[0]
		
		####
		# Toes
		####
		# Left
		l_toe_outer_chain = chain.get_chain('outer_toe', 'left')
		l_toe_outer_component = frag.FKComponent.create(frag_rig,
															  l_toe_outer_chain[0],
															  l_toe_outer_chain[1],
															  side='left',
															  region='outer_toe',
															  lock_root_translate_axes=['v'])
		l_toe_outer_component.attach_component(l_foot_component, l_foot_chain)
		l_toe_outer_flags = l_toe_outer_component.get_flags()
		
		l_toe_mid_chain = chain.get_chain('mid_toe', 'left')
		l_toe_mid_component = frag.FKComponent.create(frag_rig,
															l_toe_mid_chain[0],
															l_toe_mid_chain[1],
															side='left',
															region='mid_toe',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		l_toe_mid_component.attach_component(l_foot_component, l_foot_chain)
		l_toe_mid_flags = l_toe_mid_component.get_flags()
		
		l_toe_inner_chain = chain.get_chain('inner_toe', 'left')
		l_toe_inner_component = frag.FKComponent.create(frag_rig,
															  l_toe_inner_chain[0],
															  l_toe_inner_chain[1],
															  side='left',
															  region='mid_toe',
															  lock_child_translate_axes=[],
															  lock_root_translate_axes=['v'])
		l_toe_inner_component.attach_component(l_foot_component, l_foot_chain)
		l_toe_inner_flags = l_toe_mid_component.get_flags()
		
		# Right
		r_toe_outer_chain = chain.get_chain('outer_toe', 'right')
		r_toe_outer_component = frag.FKComponent.create(frag_rig,
															  r_toe_outer_chain[0],
															  r_toe_outer_chain[1],
															  side='right',
															  region='outer_toe',
															  lock_child_translate_axes=[],
															  lock_root_translate_axes=['v'])
		r_toe_outer_component.attach_component(r_foot_component, r_foot_chain)
		r_toe_outer_flags = r_toe_outer_component.get_flags()
		
		r_toe_mid_chain = chain.get_chain('mid_toe', 'right')
		r_toe_mid_component = frag.FKComponent.create(frag_rig,
															r_toe_mid_chain[0],
															r_toe_mid_chain[1],
															side='right',
															region='mid_toe',
															lock_child_translate_axes=[],
															lock_root_translate_axes=['v'])
		r_toe_mid_component.attach_component(r_foot_component, r_foot_chain)
		r_toe_mid_flags = r_toe_mid_component.get_flags()
		
		r_toe_inner_chain = chain.get_chain('inner_toe', 'right')
		r_toe_inner_component = frag.FKComponent.create(frag_rig,
															  r_toe_inner_chain[0],
															  r_toe_inner_chain[1],
															  side='right',
															  region='mid_toe',
															  lock_child_translate_axes=[],
															  lock_root_translate_axes=['v'])
		r_toe_inner_component.attach_component(r_foot_component, r_foot_chain)
		r_toe_inner_flags = r_toe_mid_component.get_flags()
		
		dog_chain = chain.get_chain('dog', 'center')
		dog_component = frag.FKComponent.create(frag_rig,
															  dog_chain[0],
															  dog_chain[1],
															  side='center',
															  region='dog',
															  lock_child_translate_axes=[],
															  lock_root_translate_axes=['v'])
		dog_component.attach_component(cog_component, pelvis_joint)
		dog_flags = dog_component.get_flags()
		
		# Multi Constraint
		# Head
		frag.MultiConstraint.create(frag_rig,
											side='center',
											region='head',
											source_object=head_flag,
											target_list=[offset_flag,
															cog_flag,
															world_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow')
		
		# IKFK Right Foot
		frag.MultiConstraint.create(frag_rig,
											side='right',
											region='leg',
											source_object=r_leg_ik_flag,
											target_list=[offset_flag, pelvis_flag, cog_flag],
											switch_obj=r_leg_switch_flag)
		
		frag.MultiConstraint.create(frag_rig,
											side='left',
											region='leg',
											source_object=l_leg_ik_flag,
											target_list=[offset_flag, pelvis_flag, cog_flag],
											switch_obj=l_leg_switch_flag)
		# IKFK Left Foot PV
		frag.MultiConstraint.create(frag_rig,
											side='left',
											region='leg_pv',
											source_object=l_leg_component.pv_flag,
											target_list=[offset_flag, l_leg_ik_flag, cog_flag],
											switch_obj=None)
		
		# Right Leg PV
		frag.MultiConstraint.create(frag_rig,
											side='right',
											region='leg_pv',
											source_object=r_leg_component.pv_flag,
											target_list=[offset_flag, r_leg_ik_flag, cog_flag],
											switch_obj=None)
		
		frag.MultiConstraint.create(frag_rig,
											side='left',
											region='gun',
											source_object=l_gun_flags[0],
											target_list=[head_flag,
															offset_flag,
															cog_flag,
															world_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow')
		
		frag.MultiConstraint.create(frag_rig,
											side='right',
											region='gun',
											source_object=r_gun_flags[0],
											target_list=[head_flag,
															offset_flag,
															cog_flag,
															world_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow')
		
		if finalize:
			frag_rig.rigTemplate.set(PlayerMaleTemplate.__name__)
			frag_rig.finalize_rig(self.get_flags_path())
		
		return frag_rig


class SuperHeroTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = '6tys-ops6i-t0j7r-vx03'
	ASSET_TYPE = 'player'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(SuperHeroTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		world_root = pm.PyNode('root')

		frag_root = frag.FRAGRoot.create(world_root, self.asset_type, self.asset_id)
		frag.SkeletalMesh.create(frag_root)
		frag_rig = frag.FRAGRig.create(frag_root)

		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
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

		# Cog
		pelvis_joint = chain.get_start('pelvis', 'center')
		cog_component = frag.CogComponent.create(frag_rig,
												 pelvis_joint,
												 pelvis_joint,
												 'center',
												 'cog',
												 orientation=[-90, 0, 0])
		cog_component.attach_component(world_component, pm.PyNode(offset_flag))
		cog_flag = cog_component.get_flags()[0]

		# Pelvis
		start_joint = pm.PyNode('pelvis')
		spine_01_chain =  pm.PyNode('spine_01')
		pelvis_component = frag.PelvisComponent.create(frag_rig,
													   start_joint,
													   spine_01_chain,
													   'center',
													   'pelvis',
													   orientation=[-90, 0, 0])
		pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
		pelvis_flag = pelvis_component.get_flags()[0]

		# Spine
		spine_start = pm.PyNode('spine_02')
		spine_end = pm.PyNode('spine_03')
		spine_component = frag.FKComponent.create(frag_rig,
													spine_start,
													spine_end,
													'center',
													'spine',
													lock_root_translate_axes=['v'])
		spine_component.attach_component(cog_component, [pm.PyNode(cog_flag)])
		spine_flags = spine_component.get_flags()

		# head
		head_chain = pm.PyNode('head')
		head_component = frag.FKComponent.create(frag_rig,
												 head_chain,
												 head_chain,
												 side='center',
												 region='head',
												 lock_child_translate_axes=[],
												 lock_root_translate_axes=['v'])
		head_component.attach_component(spine_component, spine_end)
		head_flag = head_component.get_flags()[0]

		# Left arm
		l_arm_chain = pm.PyNode('upperarm_l')
		l_arm_component = frag.FKComponent.create(frag_rig,
												  l_arm_chain,
												  l_arm_chain,
												  side='left',
												  region='arm',
												  lock_child_translate_axes=[],
												  lock_root_translate_axes=['v'])
		l_arm_component.attach_component(spine_component, spine_end)
		l_arm_flags = l_arm_component.get_flags()

		# right arm
		r_arm_chain = pm.PyNode('upperarm_r')
		r_arm_component = frag.FKComponent.create(frag_rig,
												  r_arm_chain,
												  r_arm_chain,
												  side='right',
												  region='arm',
												  lock_child_translate_axes=[],
												  lock_root_translate_axes=['v'])
		r_arm_component.attach_component(spine_component, spine_end)
		r_arm_flags = r_arm_component.get_flags()

		# Left leg
		l_thigh_chain = pm.PyNode('thigh_l')
		l_thigh_component = frag.FKComponent.create(frag_rig,
												  l_thigh_chain,
												  l_thigh_chain,
												  side='left',
												  region='thigh',
												  lock_child_translate_axes=[],
												  lock_root_translate_axes=['v'])
		l_thigh_component.attach_component(cog_component, pm.PyNode(cog_flag))
		l_thigh_flags = l_thigh_component.get_flags()

		# Left knee
		l_knee_chain = pm.PyNode('knee_l')
		l_knee_component = frag.FKComponent.create(frag_rig,
													l_knee_chain,
													l_knee_chain,
													side='left',
													region='knee',
													lock_child_translate_axes=[],
													lock_root_translate_axes=['v'])
		l_knee_component.attach_component(l_thigh_component, l_thigh_flags)
		l_knee_flags = l_thigh_component.get_flags()

		# right leg
		r_thigh_chain = pm.PyNode('thigh_r')
		r_thigh_component = frag.FKComponent.create(frag_rig,
												  r_thigh_chain,
												  r_thigh_chain,
												  side='right',
												  region='thigh',
												  lock_child_translate_axes=[],
												  lock_root_translate_axes=['v'])
		r_thigh_component.attach_component(cog_component, pm.PyNode(cog_flag))
		r_thigh_flags = r_thigh_component.get_flags()

		# right knee
		r_knee_chain = pm.PyNode('knee_r')
		r_knee_component = frag.FKComponent.create(frag_rig,
													r_knee_chain,
													r_knee_chain,
													side='right',
													region='knee',
													lock_child_translate_axes=[],
													lock_root_translate_axes=['v'])
		r_knee_component.attach_component(r_thigh_component, r_thigh_flags)
		r_knee_flags = r_knee_component.get_flags()


		# Cape
		cape_chain = pm.PyNode('cape')
		cape_component = frag.FKComponent.create(frag_rig,
												  cape_chain,
												  cape_chain,
												  side='center',
												  region='cape',
												  lock_child_translate_axes=[],
												  lock_root_translate_axes=['v'])
		cape_component.attach_component(spine_component, spine_end)
		cape_flags = cape_component.get_flags()
		cape_flags[0].set_as_sub()

		if finalize:
			frag_rig.rigTemplate.set(SuperHeroTemplate.__name__)
			frag_rig.finalize_rig(self.get_flags_path())

		return frag_rig
