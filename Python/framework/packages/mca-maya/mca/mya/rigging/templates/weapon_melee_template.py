#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Weapon Template
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates


class WeaponMelee(rig_templates.RigTemplates):
	VERSION = 1
	ASSET_ID = ''
	ASSET_TYPE = 'weapon'
	
	def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
		super(WeaponMelee, self).__init__(asset_id, asset_type)
	
	# We would not normally create the root and skel mesh here.
	def build(self):
		
		if self.asset_id == '':
			raise RuntimeError('Please enter an asset id.')
		
		pm.namespace(set=':')
		# import Skeletal Mesh using ASSET_ID into the namespace
		root_joint = pm.PyNode('root')
		
		frag_root = frag.FRAGRoot.create(root_joint, self.asset_type, self.asset_id)
		frag.SkeletalMesh.create(frag_root)
		frag_rig = frag.FRAGRig.create(frag_root)
		
		flags_all = frag_rig.flagsAll.get()
		
		# world
		start_joint = pm.PyNode('root')
		world_component = frag.WorldComponent.create(frag_rig,
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
		weapon_component = frag.FKComponent.create(frag_rig,
															start_joint,
															end_joint,
															side='center',
															region='handle',
															lock_root_translate_axes=['v'])
		weapon_component.attach_component(world_component, pm.PyNode('root'))
		weapon_flag = weapon_component.get_end_flag()
		
		frag.MultiConstraint.create(frag_rig,
											side='right',
											region='hand_prop',
											source_object=weapon_flag,
											target_list=[world_flag, root_flag, flags_all],
											switch_obj=None)
		
		frag_rig.rigTemplate.set(WeaponMelee.__name__)
		frag_rig.finalize_rig(self.get_flags_path())
		
		return frag_rig

