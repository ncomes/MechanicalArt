
"""
Template for human players and npcs
"""

# System global imports
# Software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.rigging import tek
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup
from mca.common import log


logger = log.MCA_LOGGER


class BaseSummonerTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(BaseSummonerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self, finalize=True):

		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		world_root = pm.PyNode('root')

		tek_root = tek.TEKRoot.create(world_root, self.asset_type, self.asset_id)
		tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)

		root = pm.PyNode('root')
		chain = chain_markup.ChainMarkup(root)
		# world

		world_component = tek.WorldComponent.create(tek_rig,
														   root,
														   'center',
														   'world',
														   orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()
		# Root Multiconstraint
		tek.MultiConstraint.create(tek_rig,
									side='center',
									region='root',
									source_object=root_flag,
									target_list=[world_flag,
												 offset_flag])
		# Cog
		pelvis_joint = chain.get_start('pelvis', 'center')
		cog_component = tek.CogComponent.create(tek_rig,
													   pelvis_joint,
													   pelvis_joint,
													   'center',
													   'cog',
													   orientation=[-90, 0, 0])
		cog_component.attach_component(world_component, pm.PyNode(offset_flag))
		cog_flag = cog_component.get_flags()[0]

		# Pelvis
		start_joint = pm.PyNode('pelvis')
		end_joint = pm.PyNode('spine_01')
		pelvis_component = tek.PelvisComponent.create(tek_rig,
															 start_joint,
															 end_joint,
															 'center',
															 'pelvis',
															 orientation=[-90, 0, 0])
		pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
		pelvis_flag = pelvis_component.get_flags()[0]

		# Spine
		spine_chain = chain.get_chain('spine', 'center')
		spine_component = tek.RFKComponent.create(tek_rig,
														 spine_chain[0],
														 spine_chain[1],
														 'center',
														 'spine')
		spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
		spine_flags = spine_component.get_flags()
		spine_sub_flags = spine_component.sub_flags

		# Neck
		neck_chain = chain.get_chain('neck', 'center')
		neck_component = tek.RFKComponent.create(tek_rig,
														neck_chain[0],
														neck_chain[1],
														'center',
														'neck',
														False)
		neck_component.attach_component(spine_component, pm.PyNode('spine_04'))
		neck_flags = neck_component.get_flags()
		head_flag = neck_component.end_flag
		neck_flag = neck_component.start_flag
		neck_flag.set_as_sub()
		mid_neck_flag = neck_component.mid_flags[0]
		mid_neck_flag.set_as_detail()

		# Left Clavicle
		l_clav_chain = chain.get_chain('clav', 'left')
		l_clav_component = tek.FKComponent.create(tek_rig,
														 l_clav_chain[0],
														 l_clav_chain[1],
														 side='left',
														 region='clav',
														 lock_root_translate_axes=['v'])
		l_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
		l_clav_flag = l_clav_component.get_flags()[0]

		# Right Clavicle
		r_clav_chain = chain.get_chain('clav', 'right')
		r_clav_component = tek.FKComponent.create(tek_rig,
														 r_clav_chain[0],
														 r_clav_chain[1],
														 side='right',
														 region='clav',
														 lock_root_translate_axes=['v'])
		r_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
		r_clav_flag = r_clav_component.get_flags()[0]

		# IKFK Right arm
		r_arm_chain = chain.get_chain('arm', 'right')
		r_arm_component = tek.IKFKComponent.create(tek_rig,
														  r_arm_chain[0],
														  r_arm_chain[1],
														  side='right',
														  region='arm',
														  lock_root_translate_axes=(''),
														  ik_flag_pv_orient=[-90, 0, 0])
		r_arm_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
		r_arm_flags = r_arm_component.get_flags()
		r_arm_ik_flag = r_arm_component.ik_flag
		r_arm_switch_flag = r_arm_component.switch_flag
		r_arm_fk_flag = r_arm_component.fk_flags

		# IKFK Left arm
		l_arm_chain = chain.get_chain('arm', 'left')
		l_arm_component = tek.IKFKComponent.create(tek_rig,
														  l_arm_chain[0],
														  l_arm_chain[1],
														  side='left',
														  region='arm',
														  lock_root_translate_axes=(''),
														  ik_flag_pv_orient=[-90, 0, 0])
		l_arm_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
		l_arm_flags = l_arm_component.get_flags()
		l_arm_ik_flag = l_arm_component.ik_flag
		l_arm_switch_flag = l_arm_component.switch_flag
		l_arm_fk_flag = l_arm_component.fk_flags

		# Left Hand prop
		l_hand_contact = chain.get_start('hand_contact', 'left')
		l_prop_component = tek.FKComponent.create(tek_rig,
														 l_hand_contact,
														 l_hand_contact,
														 side='left',
														 region='hand_prop',
														 scale=0.1,
														 lock_root_translate_axes=[])
		l_prop_component.attach_component(l_arm_component, pm.PyNode('hand_l'))
		l_prop_flag = l_prop_component.get_flags()[0]
		l_prop_flag.set_as_sub()

		# Right Hand prop
		r_hand_contact = chain.get_start('hand_contact', 'right')
		r_prop_component = tek.FKComponent.create(tek_rig,
														 r_hand_contact,
														 r_hand_contact,
														 side='right',
														 region='hand_prop',
														 scale=0.1,
														 lock_root_translate_axes=[])
		r_prop_component.attach_component(r_arm_component, pm.PyNode('hand_r'))
		r_prop_flag = r_prop_component.get_flags()[0]
		r_prop_flag.set_as_sub()

		# Left Hand weapon
		l_weapon = chain.get_start('hand_prop', 'left')
		l_weapon_component = tek.FKComponent.create(tek_rig,
														   l_weapon,
														   l_weapon,
														   side='left',
														   region='hand_weapon',
														   scale=0.1,
														   lock_root_translate_axes=[])
		l_weapon_component.attach_component(l_arm_component, pm.PyNode('hand_l'))
		l_weapon_flag = l_weapon_component.get_flags()[0]
		l_weapon_flag.set_as_sub()

		# Right Hand weapon
		r_weapon = chain.get_start('hand_prop', 'right')
		r_weapon_component = tek.FKComponent.create(tek_rig,
														   r_weapon,
														   r_weapon,
														   side='right',
														   region='hand_weapon',
														   scale=0.1,
														   lock_root_translate_axes=[])
		r_weapon_component.attach_component(r_arm_component, pm.PyNode('hand_r'))
		r_weapon_flag = r_weapon_component.get_flags()[0]
		r_weapon_flag.set_as_sub()

		####  Left Fingers #######
		# left Index Finger
		l_index_chain = chain.get_chain('index_finger', 'left')
		l_index_component = tek.FKComponent.create(tek_rig,
														  l_index_chain[0],
														  l_index_chain[1],
														  side='left',
														  region='index_finger',
														  scale=0.1)
		l_index_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

		# left middle Finger
		l_middle_chain = chain.get_chain('middle_finger', 'left')
		l_middle_component = tek.FKComponent.create(tek_rig,
														   l_middle_chain[0],
														   l_middle_chain[1],
														   side='left',
														   region='middle_finger',
														   scale=0.1)
		l_middle_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

		# left ring Finger
		l_ring_chain = chain.get_chain('ring_finger', 'left')
		l_ring_component = tek.FKComponent.create(tek_rig,
														 l_ring_chain[0],
														 l_ring_chain[1],
														 side='left',
														 region='ring_finger',
														 scale=0.1)
		l_ring_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

		# left Pinky Finger
		l_pinky_chain = chain.get_chain('pinky_finger', 'left')
		l_pinky_component = tek.FKComponent.create(tek_rig,
														  l_pinky_chain[0],
														  l_pinky_chain[1],
														  side='left',
														  region='pinky_finger',
														  scale=0.1)
		l_pinky_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

		# left Thumb Finger
		start_joint = pm.PyNode('thumb_01_l')
		end_joint = pm.PyNode('thumb_03_l')
		l_thumb_chain = chain.get_chain('thumb', 'left')
		l_thumb_component = tek.FKComponent.create(tek_rig,
														  l_thumb_chain[0],
														  l_thumb_chain[1],
														  side='left',
														  region='thumb',
														  scale=0.1)
		l_thumb_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

		####  Right Fingers #######
		# left Index Finger
		r_index_chain = chain.get_chain('index_finger', 'right')
		r_index_component = tek.FKComponent.create(tek_rig,
														  r_index_chain[0],
														  r_index_chain[1],
														  side='right',
														  region='index_finger',
														  scale=0.1)
		r_index_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

		# left middle Finger
		r_middle_chain = chain.get_chain('middle_finger', 'right')
		r_middle_component = tek.FKComponent.create(tek_rig,
														   r_middle_chain[0],
														   r_middle_chain[1],
														   side='right',
														   region='middle_finger',
														   scale=0.1)
		r_middle_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

		# left ring Finger
		r_ring_chain = chain.get_chain('ring_finger', 'right')
		r_ring_component = tek.FKComponent.create(tek_rig,
														 r_ring_chain[0],
														 r_ring_chain[1],
														 side='right',
														 region='ring_finger',
														 scale=0.1)
		r_ring_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

		# left Pinky Finger
		r_pinky_chain = chain.get_chain('pinky_finger', 'right')
		r_pinky_component = tek.FKComponent.create(tek_rig,
														  r_pinky_chain[0],
														  r_pinky_chain[1],
														  side='right',
														  region='pinky_finger',
														  scale=0.1)
		r_pinky_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

		# Right Thumb Finger
		r_thumb_chain = chain.get_chain('thumb', 'right')
		r_thumb_component = tek.FKComponent.create(tek_rig,
														  r_thumb_chain[0],
														  r_thumb_chain[1],
														  side='right',
														  region='thumb',
														  scale=0.1)
		r_thumb_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

		# Utilities
		# # util
		# util_joint = chain.get_start('utility', 'center')
		# util_component = tek.FKComponent.create(tek_rig,
		#                                                util_joint,
		#                                                util_joint,
		#                                                side='center',
		#                                                region='utility',
		#                                                lock_root_translate_axes=[])
		# util_component.attach_component(world_component, root)
		# util_flag = util_component.get_end_flag()
		# util_flag.set_as_util()

		# util warp
		util_warp_joint = chain.get_start('utility_warp', 'center')
		util_warp_component = tek.FKComponent.create(tek_rig,
															util_warp_joint,
															util_warp_joint,
															side='center',
															region='util_warp',
															lock_root_translate_axes=[])
		util_warp_component.attach_component(world_component, root)
		util_warp_flag = util_warp_component.get_end_flag()
		util_warp_flag.set_as_util()

		# Floor constraints
		# Pelvis
		contact_joint = chain.get_start('pelvis_contact', 'center')
		pelvis_contact_component = tek.FKComponent.create(tek_rig,
																 contact_joint,
																 contact_joint,
																 side='center',
																 region='pelvis_contact',
																 lock_root_translate_axes=[])
		pelvis_contact_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
		pelvis_contact_flag = pelvis_contact_component.get_end_flag()
		pelvis_contact_flag.set_as_contact()

		# Center
		floor_joint = chain.get_start('floor', 'center')
		floor_component = tek.FKComponent.create(tek_rig,
														floor_joint,
														floor_joint,
														side='center',
														region='floor_contact',
														lock_root_translate_axes=[])
		floor_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
		floor_flag = floor_component.get_end_flag()
		floor_flag.set_as_contact()


		### Multi Constraints ###############
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

		# Left IK Arm Multi
		tek.MultiConstraint.create(tek_rig,
										  side='left',
										  region='arm',
										  source_object=l_arm_ik_flag,
										  target_list=[offset_flag,
													   l_clav_flag,
													   r_arm_ik_flag,
													   cog_flag,
													   spine_sub_flags[1],
													   floor_flag],
										  switch_obj=l_arm_switch_flag,
										  switch_attr='follow')
		# Right IK Arm Multi
		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='arm',
										  source_object=r_arm_ik_flag,
										  target_list=[offset_flag,
													   r_clav_flag,
													   l_arm_ik_flag,
													   cog_flag,
													   spine_sub_flags[1],
													   floor_flag],
										  switch_obj=r_arm_switch_flag)

		# Left FK Arm Multi
		tek.MultiConstraint.create(tek_rig,
										  side='left',
										  region='fk_arm',
										  source_object=l_arm_fk_flag[0],
										  target_list=[l_clav_flag,
													   spine_sub_flags[1],
													   offset_flag,
													   cog_flag],
										  t=False,
										  switch_attr='rotateFollow')
		# Right FK Arm Multi
		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='fk_arm',
										  source_object=r_arm_fk_flag[0],
										  target_list=[r_clav_flag,
													   spine_sub_flags[1],
													   offset_flag,
													   cog_flag],
										  t=False,
										  switch_attr='rotateFollow')

		# Head
		tek.MultiConstraint.create(tek_rig,
										  side='center',
										  region='head',
										  source_object=head_flag,
										  target_list=[offset_flag,
													   neck_flag,
													   mid_neck_flag,
													   cog_flag],
										  switch_obj=None,
										  translate=False,
										  switch_attr='rotateFollow')
		# PV Left Arm
		tek.MultiConstraint.create(tek_rig,
										  side='left',
										  region='arm_pv',
										  source_object=l_arm_component.pv_flag,
										  target_list=[offset_flag, l_clav_flag, spine_sub_flags[1], cog_flag],
										  switch_obj=None)
		# PV Right Arm
		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='arm_pv',
										  source_object=r_arm_component.pv_flag,
										  target_list=[offset_flag, r_clav_flag, spine_sub_flags[1], cog_flag],
										  switch_obj=None)

		# Spine Top
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

		# Left Hand Contact
		tek.MultiConstraint.create(tek_rig,
										  side='left',
										  region='hand_prop',
										  source_object=l_prop_flag,
										  target_list=[l_weapon_flag,
													   r_weapon_flag,
													   floor_flag,
													   cog_flag,
													   pm.PyNode('hand_l')],
										  switch_obj=None,
										  default_name='l_weapon')

		# Right Hand Contact
		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='hand_prop',
										  source_object=r_prop_flag,
										  target_list=[r_weapon_flag,
													   l_weapon_flag,
													   floor_flag,
													   cog_flag,
													   pm.PyNode('hand_r')],
										  switch_obj=None,
										  default_name='r_weapon')

		# Right Weapon
		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='weapon',
										  source_object=r_weapon_flag,
										  target_list=[pm.PyNode('hand_r'),
													   l_prop_flag,
													   r_prop_flag,
													   l_weapon_flag,
													   cog_flag,
													   head_flag,
													   offset_flag,
													   floor_flag],
										  switch_obj=None,
										  default_name='r_hand')

		# Left Weapon
		tek.MultiConstraint.create(tek_rig,
										  side='left',
										  region='weapon',
										  source_object=l_weapon_flag,
										  target_list=[pm.PyNode('hand_l'),
													   r_prop_flag,
													   l_prop_flag,
													   r_weapon_flag,
													   cog_flag,
													   head_flag,
													   offset_flag,
													   floor_flag],
										  switch_obj=None,
										  default_name='l_hand')

		if finalize:
			tek_rig.rigTemplate.set(BaseSummonerTemplate.__name__)
			tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig



class DemonicSummonerTemplate(BaseSummonerTemplate):
	VERSION = 1
	ASSET_ID = 'demonic_summoner'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(DemonicSummonerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self):

		pm.namespace(set=':')

		tek_rig = super(DemonicSummonerTemplate, self).build(finalize=False)
		root_component = tek_rig.get_tek_parent()
		neck_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='neck')
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')

		if not neck_component:
			logger.warning('No Right Clavicle Component found!')
			return
		if len(neck_component) > 1:
			neck_component = [x for x in neck_component if tek.TEKNode(x).region == 'neck']

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)
		# Tongue Spline
		tongue_start, tongue_end = chain.get_chain('tongue', 'center')
		start_helper_joint = chain.get_chain('tongue_start', 'center')[0]
		mid_helper_joint = chain.get_chain('tongue_helper', 'center')[0]
		end_helper_joint = chain.get_chain('tongue_end', 'center')[0]
		tongue_component = tek.SplineIKComponent.create(tek_rig,
																   tongue_start,
																   tongue_end,
																   end_helper_joint,
																   mid_helper_joint,
																   start_helper_joint=start_helper_joint,
																   side='center',
																   region='tongue',
																   mid_flag=True,
																   can_retract=True)
		tongue_component.attach_component(neck_component, [pm.PyNode('head')])
		tongue_flags = tongue_component.get_flags()


		coat_l = chain.get_chain('coat', 'left')
		coat_l_component = tek.FKComponent.create(tek_rig,
														 coat_l[0],
														 coat_l[1],
														 side='left',
														 region='coat',
														 scale=0.1,
														 lock_root_translate_axes=[],
														 lock_child_translate_axes=[])
		coat_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_l_flag = coat_l_component.get_flags()[0]

		coat_r = chain.get_chain('coat', 'right')
		coat_r_component = tek.FKComponent.create(tek_rig,
														 coat_r[0],
														 coat_r[1],
														 side='right',
														 region='coat',
														 scale=0.1,
														 lock_root_translate_axes=[],
														 lock_child_translate_axes=[])
		coat_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_r_flag = coat_r_component.get_flags()[0]

		coat_back = chain.get_chain('coat', 'center')
		coat_back_component = tek.FKComponent.create(tek_rig,
															coat_back[0],
															coat_back[1],
															side='center',
															region='coat',
															scale=0.1,
															lock_root_translate_axes=[],
															lock_child_translate_axes=[])
		coat_back_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_back_flag = coat_back_component.get_flags()[0]

		coat_inner_r = chain.get_chain('coat_inner', 'right')
		coat_inner_r_component = tek.FKComponent.create(tek_rig,
															   coat_inner_r[0],
															   coat_inner_r[1],
															   side='right',
															   region='coat_inner',
															   scale=0.1,
															   lock_root_translate_axes=[],
															   lock_child_translate_axes=[])
		coat_inner_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_inner_r_flag = coat_inner_r_component.get_flags()[0]

		coat_inner_l = chain.get_chain('coat_inner', 'left')
		coat_inner_l_component = tek.FKComponent.create(tek_rig,
															   coat_inner_l[0],
															   coat_inner_l[1],
															   side='left',
															   region='coat_inner',
															   scale=0.1,
															   lock_root_translate_axes=[],
															   lock_child_translate_axes=[])
		coat_inner_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_inner_l_flag = coat_inner_l_component.get_flags()[0]


		tek_rig.rigTemplate.set(DemonicSummonerTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())
		return tek_rig


class ProtectingSummonerTemplate(BaseSummonerTemplate):
	VERSION = 1
	ASSET_ID = 'protectingsummoner'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(ProtectingSummonerTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self):
		pm.namespace(set=':')

		tek_rig = super(ProtectingSummonerTemplate, self).build(finalize=False)
		root_component = tek_rig.get_tek_parent()
		neck_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='neck')
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')
		r_clav_component = tek_rig.get_tek_children(of_type=tek.FKComponent, region='clav', side='right')
		l_clav_component = tek_rig.get_tek_children(of_type=tek.FKComponent, region='clav', side='left')

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)

		spine_04_prop_01_l = chain.get_start('spine_04_prop', 'left')
		spine_04_prop_01_l_component = tek.FKComponent.create(tek_rig,
		                                        spine_04_prop_01_l,
		                                        spine_04_prop_01_l,
		                                        side='left',
		                                        region='spine_04_prop',
		                                        lock_root_translate_axes=[])
		spine_04_prop_01_l_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		spine_04_prop_01_r = chain.get_start('spine_04_prop', 'right')
		spine_04_prop_01_r_component = tek.FKComponent.create(tek_rig,
		                                        spine_04_prop_01_r,
		                                        spine_04_prop_01_r,
		                                        side='right',
		                                        region='spine_04_prop',
		                                        lock_root_translate_axes=[])
		spine_04_prop_01_r_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		head_prop_01_l = chain.get_start('head_prop', 'left')
		head_prop_01_l_component = tek.FKComponent.create(tek_rig,
		                                        head_prop_01_l,
		                                        head_prop_01_l,
		                                        side='left',
		                                        region='head_prop',
		                                        lock_root_translate_axes=[])
		head_prop_01_l_component.attach_component(neck_component, [pm.PyNode('head')])

		head_prop_01_r = chain.get_start('head_prop', 'right')
		head_prop_01_r_component = tek.FKComponent.create(tek_rig,
		                                        head_prop_01_r,
		                                        head_prop_01_r,
		                                        side='right',
		                                        region='head_prop',
		                                        lock_root_translate_axes=[])
		head_prop_01_r_component.attach_component(neck_component, [pm.PyNode('head')])

		clavicle_deformer_r = chain.get_start('clavicle_deformer', 'right')
		clavicle_deformer_r_component = tek.FKComponent.create(tek_rig,
		                                                        clavicle_deformer_r,
		                                                        clavicle_deformer_r,
		                                                        side='right',
		                                                        region='clavicle_deformer',
		                                                        lock_root_translate_axes=[])
		clavicle_deformer_r_component.attach_component(r_clav_component, [pm.PyNode('clavicle_r')])

		clavicle_deformer_l = chain.get_start('clavicle_deformer', 'left')
		clavicle_deformer_l_component = tek.FKComponent.create(tek_rig,
		                                                        clavicle_deformer_l,
		                                                        clavicle_deformer_l,
		                                                        side='left',
		                                                        region='clavicle_deformer',
		                                                        lock_root_translate_axes=[])
		clavicle_deformer_l_component.attach_component(l_clav_component, [pm.PyNode('clavicle_l')])


		coat_l = chain.get_chain('coat', 'left')
		coat_l_component = tek.FKComponent.create(tek_rig,
														 coat_l[0],
														 coat_l[1],
														 side='left',
														 region='coat',
														 scale=0.1,
														 lock_root_translate_axes=[],
														 lock_child_translate_axes=[])
		coat_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_l_flag = coat_l_component.get_flags()[0]

		coat_r = chain.get_chain('coat', 'right')
		coat_r_component = tek.FKComponent.create(tek_rig,
														 coat_r[0],
														 coat_r[1],
														 side='right',
														 region='coat',
														 scale=0.1,
														 lock_root_translate_axes=[],
														 lock_child_translate_axes=[])
		coat_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_r_flag = coat_r_component.get_flags()[0]

		coat_back = chain.get_chain('coat', 'center')
		coat_back_component = tek.FKComponent.create(tek_rig,
															coat_back[0],
															coat_back[1],
															side='center',
															region='coat',
															scale=0.1,
															lock_root_translate_axes=[],
															lock_child_translate_axes=[])
		coat_back_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_back_flag = coat_back_component.get_flags()[0]

		coat_inner_r = chain.get_chain('coat_inner', 'right')
		coat_inner_r_component = tek.FKComponent.create(tek_rig,
															   coat_inner_r[0],
															   coat_inner_r[1],
															   side='right',
															   region='coat_inner',
															   scale=0.1,
															   lock_root_translate_axes=[],
															   lock_child_translate_axes=[])
		coat_inner_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_inner_r_flag = coat_inner_r_component.get_flags()[0]

		coat_inner_l = chain.get_chain('coat_inner', 'left')
		coat_inner_l_component = tek.FKComponent.create(tek_rig,
															   coat_inner_l[0],
															   coat_inner_l[1],
															   side='left',
															   region='coat_inner',
															   scale=0.1,
															   lock_root_translate_axes=[],
															   lock_child_translate_axes=[])
		coat_inner_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
		coat_inner_l_flag = coat_inner_l_component.get_flags()[0]


		tek_rig.rigTemplate.set(ProtectingSummonerTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())
		return tek_rig


class AngraStageTwoTemplate(BaseSummonerTemplate):
	VERSION = 1
	ASSET_ID = 'faxa-jjs9g-w9zls-dyzx'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(AngraStageTwoTemplate, self).__init__(asset_id, asset_type)

	def build(self):
		pm.namespace(set=':')

		tek_rig = super(AngraStageTwoTemplate, self).build(finalize=False)
		root_component = tek_rig.get_tek_parent()
		neck_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='neck')
		pelvis_component = tek_rig.get_tek_children(of_type=tek.CogComponent, region='pelvis')
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)

		tentacle_shoulder_r = chain.get_chain('tentacle_shoulder', 'right')
		tentacle_shoulder_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_shoulder_r[0],
		                                        tentacle_shoulder_r[1],
		                                        side='right',
		                                        region='tentacle_shoulder',
		                                        lock_root_translate_axes=[])
		tentacle_shoulder_r_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		tentacle_shoulder_l = chain.get_chain('tentacle_shoulder', 'left')
		tentacle_shoulder_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_shoulder_l[0],
		                                        tentacle_shoulder_l[1],
		                                        side='left',
		                                        region='tentacle_shoulder',
		                                        lock_root_translate_axes=[])
		tentacle_shoulder_l_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		tentacle_prime_r = chain.get_chain('tentacle_prime_center', 'right')
		tentacle_prime_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_r[0],
		                                        tentacle_prime_r[1],
		                                        side='right',
		                                        region='tentacle_prime_center',
		                                        lock_root_translate_axes=[])
		tentacle_prime_r_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		tentacle_prime_l = chain.get_chain('tentacle_prime_center', 'left')
		tentacle_prime_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_l[0],
		                                        tentacle_prime_l[1],
		                                        side='left',
		                                        region='tentacle_prime_center',
		                                        lock_root_translate_axes=[])
		tentacle_prime_l_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		head_prop_01 = chain.get_start('head_prop', 'center')
		head_prop_01_component = tek.FKComponent.create(tek_rig,
		                                        head_prop_01,
		                                        head_prop_01,
		                                        side='center',
		                                        region='head_prop',
		                                        lock_root_translate_axes=[])
		head_prop_01_component.attach_component(neck_component, [pm.PyNode('head')])
		head_prop_flag = head_prop_01_component.get_end_flag()

		tentacle_front = chain.get_chain('tentacle_front', 'center')
		tentacle_front_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_front[0],
		                                        tentacle_front[-1],
		                                        side='center',
		                                        region='tentacle_front')
		tentacle_front_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		tentacle_prime_lower_r = chain.get_chain('tentacle_prime_lower', 'right')
		tentacle_prime_lower_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_lower_r[0],
		                                        tentacle_prime_lower_r[0],
		                                        side='right',
		                                        region='tentacle_prime_lower',)
		tentacle_prime_lower_r_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		tentacle_prime_lower_l = chain.get_chain('tentacle_prime_lower', 'left')
		tentacle_prime_lower_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_lower_l[0],
		                                        tentacle_prime_lower_l[0],
		                                        side='left',
		                                        region='tentacle_prime_lower',)
		tentacle_prime_lower_l_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		tentacle_front_r = chain.get_chain('tentacle_front', 'right')
		tentacle_front_r_component = tek.FKComponent.create(tek_rig,
		                                                     tentacle_front_r[0],
		                                                     tentacle_front_r[-1],
		                                                     side='right',
		                                                     region='tentacle_front',
		                                                     lock_root_translate_axes=[])
		tentacle_front_r_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_outer_l = chain.get_chain('tentacle_back_outer', 'left')
		tentacle_back_outer_l_component = tek.FKComponent.create(tek_rig,
		                                                          tentacle_back_outer_l[0],
		                                                          tentacle_back_outer_l[-1],
		                                                          side='left',
		                                                          region='tentacle_back_outer',
		                                                          lock_root_translate_axes=[])
		tentacle_back_outer_l_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_l = chain.get_chain('tentacle_back', 'left')
		tentacle_back_l_component = tek.FKComponent.create(tek_rig,
		                                                    tentacle_back_l[0],
		                                                    tentacle_back_l[-1],
		                                                    side='left',
		                                                    region='tentacle_back',
		                                                    lock_root_translate_axes=[])
		tentacle_back_l_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_r = chain.get_chain('tentacle_back', 'right')
		tentacle_back_r_component = tek.FKComponent.create(tek_rig,
		                                                    tentacle_back_r[0],
		                                                    tentacle_back_r[-1],
		                                                    side='right',
		                                                    region='tentacle_back',
		                                                    lock_root_translate_axes=[])
		tentacle_back_r_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])


		tek.MultiConstraint.create(tek_rig,
										  side='center',
										  region='head_prop',
										  source_object=head_prop_flag,
										  target_list=[pm.PyNode('f_head'),
													   pm.PyNode('f_world'),
													   pm.PyNode('f_world_offset'),
													   pm.PyNode('spine_04')],
										  switch_obj=None,
										  default_name='default')
		tek_rig.rigTemplate.set(AngraStageTwoTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())
		return tek_rig



class AngraStageTwoV2Template(BaseSummonerTemplate):
	VERSION = 1
	ASSET_ID = 'angrastagetwov2'
	ASSET_TYPE = 'combatant'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(AngraStageTwoV2Template, self).__init__(asset_id, asset_type)

	def build(self):
		pm.namespace(set=':')

		tek_rig = super(AngraStageTwoV2Template, self).build(finalize=False)
		root_component = tek_rig.get_tek_parent()
		neck_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='neck')
		pelvis_component = tek_rig.get_tek_children(of_type=tek.CogComponent, region='pelvis')
		spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')

		root = root_component.root_joint
		chain = chain_markup.ChainMarkup(root)

		tentacle_prime_r = chain.get_chain('tentacle_prime_center', 'right')
		tentacle_prime_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_r[0],
		                                        tentacle_prime_r[1],
		                                        side='right',
		                                        region='tentacle_prime_center',
		                                        lock_root_translate_axes=[])
		tentacle_prime_r_component.attach_component(spine_component, [pm.PyNode('spine_03')])

		tentacle_prime_l = chain.get_chain('tentacle_prime_center', 'left')
		tentacle_prime_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_l[0],
		                                        tentacle_prime_l[1],
		                                        side='left',
		                                        region='tentacle_prime_center',
		                                        lock_root_translate_axes=[])
		tentacle_prime_l_component.attach_component(spine_component, [pm.PyNode('spine_03')])

		tentacle_shoulder_r = chain.get_chain('tentacle_shoulder', 'right')
		tentacle_shoulder_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_shoulder_r[0],
		                                        tentacle_shoulder_r[1],
		                                        side='right',
		                                        region='tentacle_shoulder',
		                                        lock_root_translate_axes=[])
		tentacle_shoulder_r_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		tentacle_shoulder_l = chain.get_chain('tentacle_shoulder', 'left')
		tentacle_shoulder_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_shoulder_l[0],
		                                        tentacle_shoulder_l[1],
		                                        side='left',
		                                        region='tentacle_shoulder',
		                                        lock_root_translate_axes=[])
		tentacle_shoulder_l_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		head_prop_01 = chain.get_start('head_prop', 'center')
		head_prop_01_component = tek.FKComponent.create(tek_rig,
		                                        head_prop_01,
		                                        head_prop_01,
		                                        side='center',
		                                        region='head_prop',
		                                        lock_root_translate_axes=[])
		head_prop_01_component.attach_component(neck_component, [pm.PyNode('head')])
		head_prop_flag = head_prop_01_component.get_end_flag()

		tentacle_front = chain.get_chain('tentacle_front', 'center')
		tentacle_front_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_front[0],
		                                        tentacle_front[-1],
		                                        side='center',
		                                        region='tentacle_front')
		tentacle_front_component.attach_component(pelvis_component, [pm.PyNode('pelvis')])

		tentacle_prime_lower_r = chain.get_chain('tentacle_prime_lower', 'right')
		tentacle_prime_lower_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_lower_r[0],
		                                        tentacle_prime_lower_r[0],
		                                        side='right',
		                                        region='tentacle_prime_lower')
		tentacle_prime_lower_r_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		tentacle_prime_lower_l = chain.get_chain('tentacle_prime_lower', 'left')
		tentacle_prime_lower_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_lower_l[0],
		                                        tentacle_prime_lower_l[0],
		                                        side='left',
		                                        region='tentacle_prime_lower')
		tentacle_prime_lower_l_component.attach_component(spine_component, [pm.PyNode('spine_04')])

		spine_03_prop = chain.get_chain('spine_03_prop', 'center')
		spine_03_prop_component = tek.FKComponent.create(tek_rig,
		                                        spine_03_prop[0],
		                                        spine_03_prop[-1],
		                                        side='center',
		                                        region='spine_03_prop',
		                                                  lock_root_translate_axes=[])
		spine_03_prop_component.attach_component(spine_component, [pm.PyNode('spine_04'), pm.PyNode('spine_03'), pm.PyNode('spine_02')])
		spine_03_prop_end_flag = spine_03_prop_component.get_end_flag()


		spine_03_prop_03_c = chain.get_chain('spine_03_prop_03', 'center')
		spine_03_prop_03_c_component = tek.FKComponent.create(tek_rig,
		                                        spine_03_prop_03_c[0],
		                                        spine_03_prop_03_c[-1],
		                                        side='center',
		                                        region='spine_03_prop_03',
		                                        lock_root_translate_axes=[])
		spine_03_prop_03_c_component.attach_component([spine_03_prop_component], [pm.PyNode('f_spine_03_prop_02')])


		tentacle_prime_upper_r = chain.get_chain('tentacle_prime_upper', 'right')
		tentacle_prime_upper_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_upper_r[0],
		                                        tentacle_prime_upper_r[-1],
		                                        side='right',
		                                        region='tentacle_prime_upper',
		                                        lock_root_translate_axes=[])
		tentacle_prime_upper_r_component.attach_component(spine_component,
		                                                  [pm.PyNode('spine_02'), pm.PyNode('spine_03')])


		tentacle_prime_upper_l = chain.get_chain('tentacle_prime_upper', 'left')
		tentacle_prime_upper_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_prime_upper_l[0],
		                                        tentacle_prime_upper_l[-1],
		                                        side='left',
		                                        region='tentacle_prime_upper',
		                                        lock_root_translate_axes=[])
		tentacle_prime_upper_l_component.attach_component(spine_component,
		                                                  [pm.PyNode('spine_01'), pm.PyNode('spine_02'), pm.PyNode('spine_03'), pm.PyNode('pelvis')])


		spine_02_prop_01 = chain.get_chain('spine_02_prop_01', 'right')
		spine_02_prop_01_component = tek.FKComponent.create(tek_rig,
		                                        spine_02_prop_01[0],
		                                        spine_02_prop_01[-1],
		                                        side='right',
		                                        region='spine_02_prop_01',
		                                        lock_root_translate_axes=[])
		spine_02_prop_01_component.attach_component(spine_component,
		                                                      [pm.PyNode('spine_01'), pm.PyNode('spine_02'), pm.PyNode('spine_03'), pm.PyNode('pelvis')])


		tentacle_front_outer_01_r = chain.get_chain('tentacle_front_outer', 'right')
		tentacle_front_outer_01_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_front_outer_01_r[0],
		                                        tentacle_front_outer_01_r[-1],
		                                        side='right',
		                                        region='tentacle_front_outer',
		                                        lock_root_translate_axes=[])
		tentacle_front_outer_01_r_component.attach_component([tentacle_front_component, pelvis_component[0], spine_component[0]],
		                                                     [pm.PyNode('f_tentacle_front_01_l'), pm.PyNode('pelvis'), pm.PyNode('spine_01')])


		tentacle_front_outer_01_l = chain.get_chain('tentacle_front_outer', 'left')
		tentacle_front_outer_01_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_front_outer_01_l[0],
		                                        tentacle_front_outer_01_l[-1],
		                                        side='left',
		                                        region='tentacle_front_outer',
		                                        lock_root_translate_axes=[])
		tentacle_front_outer_01_l_component.attach_component([pelvis_component[0], tentacle_front_component],
		                                                     [pm.PyNode('tentacle_front_01_l'), pm.PyNode('pelvis')])


		tentacle_front_r = chain.get_chain('tentacle_front', 'right')
		tentacle_front_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_front_r[0],
		                                        tentacle_front_r[-1],
		                                        side='right',
		                                        region='tentacle_front',)
		tentacle_front_r_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_outer_l = chain.get_chain('tentacle_back_outer', 'left')
		tentacle_back_outer_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_back_outer_l[0],
		                                        tentacle_back_outer_l[-1],
		                                        side='left',
		                                        region='tentacle_back_outer',)
		tentacle_back_outer_l_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_outer_r = chain.get_chain('tentacle_back_outer', 'right')
		tentacle_back_outer_r_component = tek.FKComponent.create(tek_rig,
		                                                          tentacle_back_outer_r[0],
		                                                          tentacle_back_outer_r[-1],
		                                                          side='right',
		                                                          region='tentacle_back_outer',
		                                                          lock_root_translate_axes=[])
		tentacle_back_outer_r_component.attach_component([tentacle_front_component, pelvis_component[0]],
		                                                 [pm.PyNode('tentacle_front_01_l'),
		                                                  pm.PyNode('tentacle_front_02_l'),
		                                                  pm.PyNode('pelvis')])

		tentacle_back_l = chain.get_chain('tentacle_back', 'left')
		tentacle_back_l_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_back_l[0],
		                                        tentacle_back_l[-1],
		                                        side='left',
		                                        region='tentacle_back',)
		tentacle_back_l_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])

		tentacle_back_r = chain.get_chain('tentacle_back', 'right')
		tentacle_back_r_component = tek.FKComponent.create(tek_rig,
		                                        tentacle_back_r[0],
		                                        tentacle_back_r[-1],
		                                        side='right',
		                                        region='tentacle_back',)
		tentacle_back_r_component.attach_component([tentacle_front_component], [pm.PyNode('tentacle_front_02_l')])


		tek.MultiConstraint.create(tek_rig,
										  side='center',
										  region='head_prop',
										  source_object=head_prop_flag,
										  target_list=[pm.PyNode('f_head'),
													   pm.PyNode('f_world'),
													   pm.PyNode('f_world_offset'),
													   pm.PyNode('spine_04')],
										  switch_obj=None,
										  default_name='default')


		tek_rig.rigTemplate.set(AngraStageTwoV2Template.__name__)
		tek_rig.finalize_rig(self.get_flags_path())
		return tek_rig




