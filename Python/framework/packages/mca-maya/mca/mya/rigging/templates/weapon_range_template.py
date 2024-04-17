#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Weapon Template
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import tek
from mca.mya.rigging.templates import rig_templates


class WeaponSR25(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = 'SR25'
	ASSET_TYPE = 'weapon'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(WeaponSR25, self).__init__(asset_id, asset_type)
	
	# We would not normally create the root and skel mesh here.
	def build(self):
		if self.asset_id == '':
			raise RuntimeError('Please enter an asset id.')
		
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')
		
		tek_root = tek.TEKRoot.create(root_joint, self.asset_type, self.asset_id)
		tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)
		
		flags_all = tek_rig.flagsAll.get()
		
		# world
		start_joint = pm.PyNode('root')
		world_component = tek.WorldComponent.create(tek_rig,
															start_joint,
															'center',
															'world',
															orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		
		start_joint = pm.PyNode('weapon')
		end_joint = pm.PyNode('weapon')
		weapon_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='center',
															region='weapon',
															lock_root_translate_axes=['v'])
		weapon_component.attach_component(world_component, pm.PyNode('root'))
		weapon_flag = weapon_component.get_end_flag()
		
		start_joint = pm.PyNode('bolt_01')
		end_joint = pm.PyNode('bolt_01')
		bolt_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='center',
															region='bolt',
															lock_root_translate_axes=['ty', 'tz', 'rx', 'ry', 'rz', 'v'])
		bolt_component.attach_component(weapon_component, pm.PyNode('weapon'))
		bolt_flag = bolt_component.get_end_flag()
		bolt_flag.set_as_sub()
		
		start_joint = pm.PyNode('breech_01')
		end_joint = pm.PyNode('breech_01')
		breech_component = tek.FKComponent.create(tek_rig,
														start_joint,
														end_joint,
														side='right',
														region='breech',
														lock_root_translate_axes=['ty', 'tz', 'rx', 'ry', 'rz', 'v'])
		breech_component.attach_component(weapon_component, pm.PyNode('weapon'))
		breech_flag = breech_component.get_end_flag()
		
		start_joint = pm.PyNode('breech_door_01')
		end_joint = pm.PyNode('breech_door_01')
		breech_door_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='right',
															region='breech_door',
															lock_root_translate_axes=['ty', 'tz', 'tx', 'ry', 'rz', 'v'])
		breech_door_component.attach_component(weapon_component, pm.PyNode('weapon'))
		breech_door_flag = breech_door_component.get_end_flag()
		
		start_joint = pm.PyNode('trigger_01')
		end_joint = pm.PyNode('trigger_01')
		trigger_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='center',
															region='trigger',
															lock_root_translate_axes=['ty', 'tz', 'tx', 'rx', 'rz', 'v'])
		trigger_component.attach_component(weapon_component, pm.PyNode('weapon'))
		trigger_flag = trigger_component.get_end_flag()
		
		start_joint = pm.PyNode('magazine_01')
		end_joint = pm.PyNode('magazine_01')
		magazine_component = tek.FKComponent.create(tek_rig,
															start_joint,
															end_joint,
															side='center',
															region='magazine',
															lock_root_translate_axes=['v'])
		magazine_component.attach_component(weapon_component, pm.PyNode('weapon'))
		magazine_flag = magazine_component.get_end_flag()


		tek.MultiConstraint.create(tek_rig,
											side='right',
											region='hand_prop',
											source_object=weapon_flag,
											target_list=[world_flag, root_flag, flags_all],
											switch_obj=None)
		
		tek.MultiConstraint.create(tek_rig,
											side='center',
											region='magazine',
											source_object=magazine_flag,
											target_list=[weapon_flag, world_flag, root_flag, flags_all],
											switch_obj=None)

		tek_rig.rigTemplate.set(WeaponSR25.__name__)
		tek_rig.finalize_rig(self.get_flags_path())
		
		return tek_rig


class WeaponRangeTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'weapon'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(WeaponRangeTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self):
		if self.asset_id == '':
			raise RuntimeError('Please enter an asset id.')

		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')

		tek_root = tek.TEKRoot.create(root_joint, self.asset_type, self.asset_id)
		tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)

		flags_all = tek_rig.flagsAll.get()

		# world
		start_joint = pm.PyNode('root')
		world_component = tek.WorldComponent.create(tek_rig,
														   start_joint,
														   'center',
														   'world',
														   orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()

		start_joint = pm.PyNode('weapon')
		end_joint = pm.PyNode('weapon')
		weapon_component = tek.FKComponent.create(tek_rig,
														 start_joint,
														 end_joint,
														 side='center',
														 region='weapon',
														 lock_root_translate_axes=['v'])
		weapon_component.attach_component(world_component, pm.PyNode('root'))
		weapon_flag = weapon_component.get_end_flag()

		# start_joint = pm.PyNode('breech_01')
		# end_joint = pm.PyNode('breech_01')
		# breech_component = tek.FKComponent.create(tek_rig,
		# 												 start_joint,
		# 												 end_joint,
		# 												 side='right',
		# 												 region='breech',
		# 												 lock_root_translate_axes=['ty', 'tz', 'rx', 'ry', 'rz', 'v'])
		# breech_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# breech_flag = breech_component.get_end_flag()

		# start_joint = pm.PyNode('forestock_01')
		# end_joint = pm.PyNode('forestock_01')
		# forestock_component = tek.FKComponent.create(tek_rig,
		# 												 start_joint,
		# 												 end_joint,
		# 												 side='center',
		# 												 region='forestock',
		# 												 lock_root_translate_axes=['ty', 'tz', 'rx', 'ry', 'rz', 'v'])
		# forestock_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# forestock_flag = forestock_component.get_end_flag()

		# start_joint = pm.PyNode('bolt_01')
		# end_joint = pm.PyNode('bolt_01')
		# bolt_component = tek.FKComponent.create(tek_rig,
		# 											   start_joint,
		# 											   end_joint,
		# 											   side='center',
		# 											   region='bolt',
		# 											   lock_root_translate_axes=['ty', 'tz', 'ry', 'rz', 'v'])
		# bolt_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# bolt_flag = bolt_component.get_end_flag()
		# bolt_flag.set_as_sub()

		# start_joint = pm.PyNode('trigger_01')
		# end_joint = pm.PyNode('trigger_01')
		# trigger_component = tek.FKComponent.create(tek_rig,
		# 												  start_joint,
		# 												  end_joint,
		# 												  side='center',
		# 												  region='trigger',
		# 												  lock_root_translate_axes=['ty', 'tz', 'tx', 'rx', 'rz', 'v'])
		# trigger_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# trigger_flag = trigger_component.get_end_flag()

		# start_joint = pm.PyNode('hammer_01')
		# end_joint = pm.PyNode('hammer_01')
		# hammer_component = tek.FKComponent.create(tek_rig,
		# 												start_joint,
		# 												end_joint,
		# 												side='center',
		# 												region='hammer',
		# 												lock_root_translate_axes=['ty', 'tz', 'tx', 'rx', 'rz', 'v'])
		# hammer_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# hammer_flag = hammer_component.get_end_flag()

		# start_joint = pm.PyNode('crane_01')
		# end_joint = pm.PyNode('crane_01')
		# crane_component = tek.FKComponent.create(tek_rig,
		# 												  start_joint,
		# 												  end_joint,
		# 												  side='right',
		# 												  region='crane',
		# 												  lock_root_translate_axes=['ty', 'tz', 'tx', 'ry', 'rz', 'v'])
		# crane_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# crane_flag = crane_component.get_end_flag()

		# start_joint = pm.PyNode('cylinder_01')
		# end_joint = pm.PyNode('cylinder_01')
		# cylinder_component = tek.FKComponent.create(tek_rig,
		# 												start_joint,
		# 												end_joint,
		# 												side='right',
		# 												region='cylinder',
		# 												lock_root_translate_axes=['ty', 'tz', 'tx', 'ry', 'rz', 'v'])
		# cylinder_component.attach_component(crane_component, pm.PyNode('crane_01'))
		# cylinder_flag = cylinder_component.get_end_flag()

		start_joint = pm.PyNode('magazine_01')
		end_joint = pm.PyNode('magazine_01')
		magazine_component = tek.FKComponent.create(tek_rig,
														start_joint,
														end_joint,
														side='center',
														region='magazine',
														lock_root_translate_axes=['v'])
		magazine_component.attach_component(weapon_component, pm.PyNode('weapon'))
		magazine_flag = magazine_component.get_end_flag()

		# start_joint = pm.PyNode('body_fuse')
		# end_joint = pm.PyNode('body_fuse')
		# bodyfuse_component = tek.FKComponent.create(tek_rig,
		# 												start_joint,
		# 												end_joint,
		# 												side='center',
		# 												region='body_fuse',
		# 												lock_root_translate_axes=['ty', 'tz', 'tx', 'rx', 'rz', 'v'])
		# bodyfuse_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# bodyfuse_flag = bodyfuse_component.get_end_flag()

		# start_joint = pm.PyNode('charging_handle_01')
		# end_joint = pm.PyNode('charging_handle_01')
		# charging_handle_component = tek.FKComponent.create(tek_rig,
		# 											   start_joint,
		# 											   end_joint,
		# 											   side='center',
		# 											   region='charging_handle',
		# 											   lock_root_translate_axes=['ty', 'tz', 'rx', 'ry', 'rz', 'v'])
		# charging_handle_component.attach_component(weapon_component, pm.PyNode('weapon'))
		# charging_handle_flag = charging_handle_component.get_end_flag()
		# charging_handle_flag.set_as_sub()

		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='hand_prop',
										  source_object=weapon_flag,
										  target_list=[world_flag, root_flag, flags_all],
										  switch_obj=None)

		tek.MultiConstraint.create(tek_rig,
										  side='center',
										  region='magazine',
										  source_object=magazine_flag,
										  target_list=[weapon_flag, world_flag, root_flag, flags_all],
										  switch_obj=None)

		tek_rig.rigTemplate.set(WeaponRangeTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig


class WeaponLeverActionTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = '0izd-squ37-ksv3j-388j'
	ASSET_TYPE = 'weapon'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(WeaponLeverActionTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self):
		if self.asset_id == '':
			raise RuntimeError('Please enter an asset id.')

		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')

		tek_root = tek.TEKRoot.create(root_joint, self.asset_type, self.asset_id)
		tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)

		flags_all = tek_rig.flagsAll.get()

		# world
		start_joint = pm.PyNode('root')
		world_component = tek.WorldComponent.create(tek_rig,
														   start_joint,
														   'center',
														   'world',
														   orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()

		start_joint = pm.PyNode('weapon')
		end_joint = pm.PyNode('weapon')
		weapon_component = tek.FKComponent.create(tek_rig,
														 start_joint,
														 end_joint,
														 side='center',
														 region='weapon',
														 lock_root_translate_axes=['v'])
		weapon_component.attach_component(world_component, pm.PyNode('root'))
		weapon_flag = weapon_component.get_end_flag()

		start_joint = pm.PyNode('bolt_carrier_01')
		end_joint = pm.PyNode('bolt_carrier_01')
		bolt_component = tek.FKComponent.create(tek_rig,
												   start_joint,
												   end_joint,
												   side='center',
												   region='bolt',
												   lock_root_translate_axes=['v'])
		bolt_component.attach_component(weapon_component, pm.PyNode('weapon'))
		bolt_flag = bolt_component.get_end_flag()

		start_joint = pm.PyNode('bolt_carrier_door_01')
		end_joint = pm.PyNode('bolt_carrier_door_01')
		bolt_door_component = tek.FKComponent.create(tek_rig,
												 start_joint,
												 end_joint,
												 side='center',
												 region='bolt_carrier',
												 lock_root_translate_axes=['v'])
		bolt_door_component.attach_component(weapon_component, pm.PyNode('weapon'))
		bolt_door_flag = bolt_door_component.get_end_flag()

		start_joint = pm.PyNode('loading_hinge_01')
		end_joint = pm.PyNode('loading_hinge_01')
		hinge_component = tek.FKComponent.create(tek_rig,
													  start_joint,
													  end_joint,
													  side='center',
													  region='hinge',
													  lock_root_translate_axes=['v'])
		hinge_component.attach_component(weapon_component, pm.PyNode('weapon'))
		hinge_flag = hinge_component.get_end_flag()

		start_joint = pm.PyNode('trigger_01')
		end_joint = pm.PyNode('trigger_01')
		trigger_component = tek.FKComponent.create(tek_rig,
												  start_joint,
												  end_joint,
												  side='center',
												  region='trigger',
												  lock_root_translate_axes=['v'])
		trigger_component.attach_component(weapon_component, pm.PyNode('weapon'))
		trigger_flag = trigger_component.get_end_flag()

		start_joint = pm.PyNode('hammer_01')
		end_joint = pm.PyNode('hammer_01')
		hammer_component = tek.FKComponent.create(tek_rig,
													start_joint,
													end_joint,
													side='center',
													region='trigger',
													lock_root_translate_axes=['v'])
		hammer_component.attach_component(weapon_component, pm.PyNode('weapon'))
		hammer_flag = hammer_component.get_end_flag()

		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='hand_prop',
										  source_object=weapon_flag,
										  target_list=[world_flag, root_flag, flags_all],
										  switch_obj=None)

		tek_rig.rigTemplate.set(WeaponRangeTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig


class WeaponArmatusTemplate(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = '7hww-o4nip-3n02l-mtkz'
	ASSET_TYPE = 'weapon'

	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(WeaponArmatusTemplate, self).__init__(asset_id, asset_type)

	# We would not normally create the root and skel mesh here.
	def build(self):
		if self.asset_id == '':
			raise RuntimeError('Please enter an asset id.')

		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')

		tek_root = tek.TEKRoot.create(root_joint, self.asset_type, self.asset_id)
		tek.SkeletalMesh.create(tek_root)
		tek_rig = tek.TEKRig.create(tek_root)

		flags_all = tek_rig.flagsAll.get()

		# world
		start_joint = pm.PyNode('root')
		world_component = tek.WorldComponent.create(tek_rig,
														   start_joint,
														   'center',
														   'world',
														   orientation=[-90, 0, 0])
		world_flag = world_component.world_flag
		root_flag = world_component.root_flag
		root_flag.set_as_sub()
		offset_flag = world_component.offset_flag
		offset_flag.set_as_detail()

		start_joint = pm.PyNode('weapon')
		end_joint = pm.PyNode('weapon')
		weapon_component = tek.FKComponent.create(tek_rig,
														 start_joint,
														 end_joint,
														 side='center',
														 region='weapon',
														 lock_root_translate_axes=['v'])
		weapon_component.attach_component(world_component, pm.PyNode('root'))
		weapon_flag = weapon_component.get_end_flag()

		start_joint = pm.PyNode('bolt_carrier_01')
		end_joint = pm.PyNode('bolt_carrier_01')
		bolt_component = tek.FKComponent.create(tek_rig,
												   start_joint,
												   end_joint,
												   side='center',
												   region='bolt',
												   lock_root_translate_axes=['v'])
		bolt_component.attach_component(weapon_component, pm.PyNode('weapon'))
		bolt_flag = bolt_component.get_end_flag()

		start_joint = pm.PyNode('trigger_01')
		end_joint = pm.PyNode('trigger_01')
		trigger_component = tek.FKComponent.create(tek_rig,
												  start_joint,
												  end_joint,
												  side='center',
												  region='trigger',
												  lock_root_translate_axes=['v'])
		trigger_component.attach_component(weapon_component, pm.PyNode('weapon'))
		trigger_flag = trigger_component.get_end_flag()

		tek.MultiConstraint.create(tek_rig,
										  side='right',
										  region='hand_prop',
										  source_object=weapon_flag,
										  target_list=[world_flag, root_flag, flags_all],
										  switch_obj=None)

		tek_rig.rigTemplate.set(WeaponRangeTemplate.__name__)
		tek_rig.finalize_rig(self.get_flags_path())

		return tek_rig