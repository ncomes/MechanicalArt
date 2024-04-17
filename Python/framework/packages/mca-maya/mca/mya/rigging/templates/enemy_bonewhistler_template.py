#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm

from mca.mya.rigging import tek, chain_markup
from mca.mya.rigging.templates import rig_templates


class BaseWhistlerTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(BaseWhistlerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):

		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')

		tek_root = tek.TEKRoot.create(root_joint, self.asset_type, self.asset_id)
		skel_mesh = tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)

		flags_all = tek_rig.flagsAll.get()

		# world
		start_joint = pm.PyNode('root')
		world_component = tek.WorldComponent.create(tek_rig,
															start_joint,
															'center',
															'world',
															orientation=[-90, 0, 0])
		root_flag = world_component.root_flag
		world_flag = world_component.world_flag
		offset_flag = world_component.offset_flag

		chain = chain_markup.ChainMarkup(start_joint)

		# Root Multiconstraint
		tek.MultiConstraint.create(tek_rig,
										  side='center',
										  region='root',
										  source_object=root_flag,
										  target_list=[world_flag,
													   offset_flag],
										  switch_attr='follow')

		# Cog
		start_joint, end_joint = chain.get_chain('pelvis', 'center')
		cog_component = tek.CogComponent.create(tek_rig,
														start_joint,
														end_joint,
														'center',
														'cog',
														orientation=[-90, 0, 0])
		cog_component.attach_component(world_component, pm.PyNode('root'))
		cog_flag = cog_component.get_flags()[0]

		# Pelvis
		start_joint = chain.get_start('pelvis', 'center')
		end_joint = chain.get_start('spine', 'center')
		pelvis_component = tek.PelvisComponent.create(tek_rig,
																start_joint,
																end_joint,
																'center',
																'pelvis',
																orientation=[-90, 0, 0])
		pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
		pelvis_flag = pelvis_component.get_flags()[0]

		# Spine
		start_joint, end_joint = chain.get_chain('spine', 'center')
		spine_component = tek.RFKComponent.create(tek_rig,
															start_joint,
															end_joint,
															'center',
															'spine')
		spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
		spine_flags = spine_component.get_flags()
		spine_sub_flags = spine_component.sub_flags


		# Left Clavicle
		start_joint, end_joint = chain.get_chain('clav', 'left')
		l_clav_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='left',
															region='clav',
															lock_root_translate_axes=['v'])
		l_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
		l_clav_flag = l_clav_component.get_flags()[0]

		# Right Clavicle
		start_joint, end_joint = chain.get_chain('clav', 'right')
		r_clav_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='right',
															region='clav',
															lock_root_translate_axes=['v'])
		r_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
		r_clav_flag = r_clav_component.get_flags()[0]

		# IKFK Left leg
		start_joint, end_joint = chain.get_chain('leg', 'left')
		l_leg_component = tek.ReverseFootComponent.create(tek_rig,
																	start_joint,
																	end_joint,
																	side='left',
																	region='leg',
																	ik_flag_pv_orient=[-90, 0, 0],
																	ik_flag_orient=[-90, 0, 0])
		l_leg_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
		l_leg_flags = l_leg_component.get_flags()
		l_leg_ik_flag = l_leg_component.ik_flag
		l_leg_switch_flag = l_leg_component.switch_flag

		# IKFK Right leg
		start_joint, end_joint = chain.get_chain('leg', 'right')
		r_leg_component = tek.ReverseFootComponent.create(tek_rig,
																	start_joint,
																	end_joint,
																	side='right',
																	region='leg',
																	ik_flag_pv_orient=[-90, 0, 0],
																	ik_flag_orient=[-90, 0, 0])
		r_leg_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
		r_leg_flags = r_leg_component.get_flags()
		r_leg_ik_flag = r_leg_component.ik_flag
		r_leg_switch_flag = r_leg_component.switch_flag
		# Floor constraints

		# util warp
		util_warp_joint = chain.get_start('utility_warp', 'center')
		util_warp_component = tek.FKComponent.create(tek_rig,
													  util_warp_joint,
													  util_warp_joint,
													  side='center',
													  region='util_warp',
													  lock_root_translate_axes=[])
		util_warp_component.attach_component([world_component], [root_joint])
		util_warp_flag = util_warp_component.get_end_flag()
		util_warp_flag.set_as_util()

		# Center
		floor_joint = chain.get_start('floor', 'center')
		floor_component = tek.FKComponent.create(tek_rig,
												  floor_joint,
												  floor_joint,
												  side='center',
												  region='floor_contact',
												  lock_root_translate_axes=[])
		floor_component.attach_component([world_component], [root_joint])
		floor_flag = floor_component.get_end_flag()
		floor_flag.set_as_contact()

		# Floor constraints
		# Pelvis
		contact_joint = chain.get_start('pelvis_contact', 'center')
		pelvis_contact_component = tek.FKComponent.create(tek_rig,
														   contact_joint,
														   contact_joint,
														   side='center',
														   region='pelvis_contact',
														   lock_root_translate_axes=[])
		pelvis_contact_component.attach_component([floor_component], [floor_joint])
		pelvis_contact_flag = pelvis_contact_component.get_end_flag()
		pelvis_contact_flag.set_as_contact()

		# Left
		l_foot_contact = chain.get_start('foot_contact', 'left')
		l_foot_contact_component = tek.FKComponent.create(tek_rig,
																 l_foot_contact,
																 l_foot_contact,
																 side='left',
																 region='foot_contact',
																 lock_root_translate_axes=[])
		l_foot_contact_component.attach_component([floor_component], [pm.PyNode('floor')])
		l_foot_contact_flag = l_foot_contact_component.get_end_flag()
		l_foot_contact_flag.set_as_contact()

		# Right
		r_foot_contact = chain.get_start('foot_contact', 'right')
		r_foot_contact_component = tek.FKComponent.create(tek_rig,
																 r_foot_contact,
																 r_foot_contact,
																 side='right',
																 region='foot_contact',
																 lock_root_translate_axes=[])
		r_foot_contact_component.attach_component([floor_component], [pm.PyNode('floor')])
		r_foot_contact_flag = r_foot_contact_component.get_end_flag()
		r_foot_contact_flag.set_as_contact()

		### Multi Constraints ###############

		# Center Cog Multi
		tek.MultiConstraint.create(tek_rig,
											side='center',
											region='cog',
											source_object=cog_flag,
											target_list=[world_flag, flags_all],
											switch_obj=None)

		tek.MultiConstraint.create(tek_rig,
											side='right',
											region='foot',
											source_object=r_leg_ik_flag,
											target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
											switch_obj=r_leg_switch_flag)

		tek.MultiConstraint.create(tek_rig,
											side='left',
											region='foot',
											source_object=l_leg_ik_flag,
											target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
											switch_obj=l_leg_switch_flag)

		tek.MultiConstraint.create(tek_rig,
											side='left',
											region='leg_pv',
											source_object=l_leg_component.pv_flag,
											target_list=[world_flag, l_leg_ik_flag, cog_flag, flags_all],
											switch_obj=None)

		tek.MultiConstraint.create(tek_rig,
											side='right',
											region='leg_pv',
											source_object=r_leg_component.pv_flag,
											target_list=[world_flag, r_leg_ik_flag, cog_flag, flags_all],
											switch_obj=None)

		tek.MultiConstraint.create(tek_rig,
											side='center',
											region='spine_top',
											source_object=spine_sub_flags[1],
											target_list=[spine_component.end_flag,
															spine_component.mid_flags[1],
															cog_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow',
											default_name='default')

		tek.MultiConstraint.create(tek_rig,
											side='center',
											region='spine_mid_top',
											source_object=spine_component.mid_flags[1],
											target_list=[spine_component.mid_offset_groups[1],
															spine_component.mid_flags[0],
															cog_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow',
											default_name='default')

		tek.MultiConstraint.create(tek_rig,
											side='center',
											region='spine_mid_bottom',
											source_object=spine_component.mid_flags[0],
											target_list=[spine_component.mid_offset_groups[0],
															spine_component.start_flag,
															cog_flag],
											switch_obj=None,
											translate=False,
											switch_attr='rotateFollow',
											default_name='default')
		# floor
		tek.MultiConstraint.create(tek_rig,
									side='center',
									region='floor_contact',
									source_object=floor_flag,
									target_list=[root_flag,
												 offset_flag],
									switch_attr='follow')
		# Pelvis Contact
		tek.MultiConstraint.create(tek_rig,
									side='center',
									region='pelvis_contact',
									source_object=pelvis_contact_flag,
									target_list=[floor_flag,
												 offset_flag],
									switch_attr='follow')
		if finalize:
			tek_rig.rigTemplate.set(BaseWhistlerTemplate.__name__)
			tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig



class SplitWhistlerTemplate(BaseWhistlerTemplate):
	VERSION = 1
	ASSET_ID = 'splitwhistler'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(SplitWhistlerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):

		pm.namespace(set=':')

		tek_rig = super(SplitWhistlerTemplate, self).build(finalize=False)
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')
		pelvis_component = tek_rig.get_tek_children(of_type=tek.PelvisComponent)
		root_component = tek_rig.get_tek_parent()

		if not spine_component:
			self.log.error('No Spine Component found!')
			return
		spine_component = spine_component[0]

		if not pelvis_component:
			self.log.error('No Pelvis Component found!')
			return
		pelvis_component = pelvis_component[0]

		if not root_component:
			self.log.error('No Root Component found!')
			return

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)
		back_cloth = chain.get_chain('back_cloth', 'center')
		back_cloth_component = tek.FKComponent.create(tek_rig,
														 back_cloth[0],
														 back_cloth[1],
														 side='center',
														 region='back_cloth')
		back_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
		if finalize:
			tek_rig.rigTemplate.set(SplitWhistlerTemplate.__name__)
			tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig



class BoneWhistlerTemplate(BaseWhistlerTemplate):
	VERSION = 1
	ASSET_ID = 'bonewhistler'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(BoneWhistlerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):

		pm.namespace(set=':')

		tek_rig = super(BoneWhistlerTemplate, self).build(finalize=False)
		pelvis_component = tek_rig.get_tek_children(of_type=tek.PelvisComponent)
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')[0]

		root_component = tek_rig.get_tek_parent()

		if not pelvis_component:
			self.log.error('No Pelvis Component found!')
			return
		pelvis_component = pelvis_component[0]

		if not root_component:
			self.log.error('No Root Component found!')
			return

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)

		# Neck
		start_joint, end_joint = chain.get_chain('neck', 'center')
		neck_component = tek.FKComponent.create(tek_rig,
														start_joint,
														start_joint,
														'center',
														'neck')
		neck_component.attach_component(spine_component, pm.PyNode('spine_04'))

		back_cloth = chain.get_chain('back_cloth', 'center')
		back_cloth_component = tek.FKComponent.create(tek_rig,
														 back_cloth[0],
														 back_cloth[1],
														 side='center',
														 region='back_cloth')
		back_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

		if finalize:
			tek_rig.rigTemplate.set(BoneWhistlerTemplate.__name__)
			tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig
