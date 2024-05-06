#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Template for human players and npcs
"""

# System global imports
# Software specific imports
import pymel.core as pm

# mca python imports
from mca.common.utils import lists
from mca.mya.rigging import frag, rig_utils
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup
from mca.common import log


logger = log.MCA_LOGGER


class PlayerMaleTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'player_male'
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
        end_joint = pm.PyNode('spine_01')
        pelvis_component = frag.PelvisComponent.create(frag_rig,
                                                             start_joint,
                                                             end_joint,
                                                             'center',
                                                             'pelvis',
                                                             orientation=[-90, 0, 0])
        pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
        pelvis_flag = pelvis_component.get_flags()[0]

        # Spine
        spine_chain = chain.get_chain('spine', 'center')
        spine_component = frag.RFKComponent.create(frag_rig,
                                                         spine_chain[0],
                                                         spine_chain[1],
                                                         'center',
                                                         'spine')
        spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
        spine_flags = spine_component.get_flags()
        spine_sub_flags = spine_component.sub_flags

        # Neck
        neck_chain = chain.get_chain('neck', 'center')
        neck_component = frag.RFKComponent.create(frag_rig,
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
        l_clav_component = frag.FKComponent.create(frag_rig,
                                                         l_clav_chain[0],
                                                         l_clav_chain[1],
                                                         side='left',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        l_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        l_clav_flag = l_clav_component.get_flags()[0]

        # Right Clavicle
        r_clav_chain = chain.get_chain('clav', 'right')
        r_clav_component = frag.FKComponent.create(frag_rig,
                                                         r_clav_chain[0],
                                                         r_clav_chain[1],
                                                         side='right',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        r_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        r_clav_flag = r_clav_component.get_flags()[0]

        # IKFK Right arm
        r_arm_chain = chain.get_chain('arm', 'right')
        r_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          r_arm_chain[0],
                                                          r_arm_chain[1],
                                                          side='right',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
        r_arm_flags = r_arm_component.get_flags()
        r_arm_ik_flag = r_arm_component.ik_flag
        r_arm_switch_flag = r_arm_component.switch_flag
        r_arm_fk_flag = r_arm_component.fk_flags

        # IKFK Left arm
        l_arm_chain = chain.get_chain('arm', 'left')
        l_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          l_arm_chain[0],
                                                          l_arm_chain[1],
                                                          side='left',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        l_arm_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        l_arm_flags = l_arm_component.get_flags()
        l_arm_ik_flag = l_arm_component.ik_flag
        l_arm_switch_flag = l_arm_component.switch_flag
        l_arm_fk_flag = l_arm_component.fk_flags

        # Left Hand prop
        l_hand_contact = chain.get_start('hand_contact', 'left')
        l_prop_component = frag.FKComponent.create(frag_rig,
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
        r_prop_component = frag.FKComponent.create(frag_rig,
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
        l_weapon_component = frag.FKComponent.create(frag_rig,
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
        r_weapon_component = frag.FKComponent.create(frag_rig,
                                                           r_weapon,
                                                           r_weapon,
                                                           side='right',
                                                           region='hand_weapon',
                                                           scale=0.1,
                                                           lock_root_translate_axes=[])
        r_weapon_component.attach_component(r_arm_component, pm.PyNode('hand_r'))
        r_weapon_flag = r_weapon_component.get_flags()[0]
        r_weapon_flag.set_as_sub()

        # IKFK Left leg
        l_leg_chain = chain.get_chain('leg', 'left')
        l_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 l_leg_chain[0],
                                                                 l_leg_chain[1],
                                                                 side='left',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, 0])
        l_leg_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        l_leg_flags = l_leg_component.get_flags()
        l_leg_ik_flag = l_leg_component.ik_flag
        l_leg_switch_flag = l_leg_component.switch_flag

        # IKFK Right leg
        r_leg_chain = chain.get_chain('leg', 'right')
        r_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 r_leg_chain[0],
                                                                 r_leg_chain[1],
                                                                 side='right',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, 0])
        r_leg_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        r_leg_flags = r_leg_component.get_flags()
        r_leg_ik_flag = r_leg_component.ik_flag
        r_leg_switch_flag = r_leg_component.switch_flag

        ####  Left Fingers #######
        # left Index Finger
        l_index_chain = chain.get_chain('index_finger', 'left')
        l_index_component = frag.FKComponent.create(frag_rig,
                                                          l_index_chain[0],
                                                          l_index_chain[1],
                                                          side='left',
                                                          region='index_finger',
                                                          scale=0.1)
        l_index_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left middle Finger
        l_middle_chain = chain.get_chain('middle_finger', 'left')
        l_middle_component = frag.FKComponent.create(frag_rig,
                                                           l_middle_chain[0],
                                                           l_middle_chain[1],
                                                           side='left',
                                                           region='middle_finger',
                                                           scale=0.1)
        l_middle_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left ring Finger
        l_ring_chain = chain.get_chain('ring_finger', 'left')
        l_ring_component = frag.FKComponent.create(frag_rig,
                                                         l_ring_chain[0],
                                                         l_ring_chain[1],
                                                         side='left',
                                                         region='ring_finger',
                                                         scale=0.1)
        l_ring_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Pinky Finger
        l_pinky_chain = chain.get_chain('pinky_finger', 'left')
        l_pinky_component = frag.FKComponent.create(frag_rig,
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
        l_thumb_component = frag.FKComponent.create(frag_rig,
                                                          l_thumb_chain[0],
                                                          l_thumb_chain[1],
                                                          side='left',
                                                          region='thumb',
                                                          scale=0.1)
        l_thumb_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        ####  Right Fingers #######
        # left Index Finger
        r_index_chain = chain.get_chain('index_finger', 'right')
        r_index_component = frag.FKComponent.create(frag_rig,
                                                          r_index_chain[0],
                                                          r_index_chain[1],
                                                          side='right',
                                                          region='index_finger',
                                                          scale=0.1)
        r_index_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left middle Finger
        r_middle_chain = chain.get_chain('middle_finger', 'right')
        r_middle_component = frag.FKComponent.create(frag_rig,
                                                           r_middle_chain[0],
                                                           r_middle_chain[1],
                                                           side='right',
                                                           region='middle_finger',
                                                           scale=0.1)
        r_middle_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left ring Finger
        r_ring_chain = chain.get_chain('ring_finger', 'right')
        r_ring_component = frag.FKComponent.create(frag_rig,
                                                         r_ring_chain[0],
                                                         r_ring_chain[1],
                                                         side='right',
                                                         region='ring_finger',
                                                         scale=0.1)
        r_ring_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # left Pinky Finger
        r_pinky_chain = chain.get_chain('pinky_finger', 'right')
        r_pinky_component = frag.FKComponent.create(frag_rig,
                                                          r_pinky_chain[0],
                                                          r_pinky_chain[1],
                                                          side='right',
                                                          region='pinky_finger',
                                                          scale=0.1)
        r_pinky_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right Thumb Finger
        r_thumb_chain = chain.get_chain('thumb', 'right')
        r_thumb_component = frag.FKComponent.create(frag_rig,
                                                          r_thumb_chain[0],
                                                          r_thumb_chain[1],
                                                          side='right',
                                                          region='thumb',
                                                          scale=0.1)
        r_thumb_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Utilities
        # util
        util_joint = chain.get_start('utility', 'center')
        util_component = frag.FKComponent.create(frag_rig,
                                                       util_joint,
                                                       util_joint,
                                                       side='center',
                                                       region='utility',
                                                       lock_root_translate_axes=[])
        util_component.attach_component(world_component, root)
        util_flag = util_component.get_end_flag()
        util_flag.set_as_util()

        # util warp
        util_warp_joint = chain.get_start('utility_warp', 'center')
        util_warp_component = frag.FKComponent.create(frag_rig,
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
        pelvis_contact_component = frag.FKComponent.create(frag_rig,
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
        floor_component = frag.FKComponent.create(frag_rig,
                                                        floor_joint,
                                                        floor_joint,
                                                        side='center',
                                                        region='floor_contact',
                                                        lock_root_translate_axes=[])
        floor_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        floor_flag = floor_component.get_end_flag()
        floor_flag.set_as_contact()

        # Left
        l_foot_contact = chain.get_start('foot_contact', 'left')
        l_foot_contact_component = frag.FKComponent.create(frag_rig,
                                                                 l_foot_contact,
                                                                 l_foot_contact,
                                                                 side='left',
                                                                 region='foot_contact',
                                                                 lock_root_translate_axes=[])
        l_foot_contact_component.attach_component(floor_component, pm.PyNode('floor'))
        l_foot_contact_flag = l_foot_contact_component.get_end_flag()
        l_foot_contact_flag.set_as_contact()

        # Right
        r_foot_contact = chain.get_start('foot_contact', 'right')
        r_foot_contact_component = frag.FKComponent.create(frag_rig,
                                                                 r_foot_contact,
                                                                 r_foot_contact,
                                                                 side='right',
                                                                 region='foot_contact',
                                                                 lock_root_translate_axes=[])
        r_foot_contact_component.attach_component(floor_component, pm.PyNode('floor'))
        r_foot_contact_flag = r_foot_contact_component.get_end_flag()
        r_foot_contact_flag.set_as_contact()

        ### Multi Constraints ###############
        # floor
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='floor_contact',
                                          source_object=floor_flag,
                                          target_list=[root_flag,
                                                       offset_flag],
                                          switch_attr='follow')
        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])
        # Left floor
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot_contact',
                                          source_object=l_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       l_leg_switch_flag],
                                          switch_attr='follow')

        # Right floor
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot_contact',
                                          source_object=r_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       r_leg_switch_flag],
                                          switch_attr='follow')

        # Pelvis Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='pelvis_contact',
                                          source_object=pelvis_contact_flag,
                                          target_list=[floor_flag,
                                                       offset_flag],
                                          switch_attr='follow')

        # Left IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='arm_pv',
                                          source_object=l_arm_component.pv_flag,
                                          target_list=[offset_flag, l_clav_flag, spine_sub_flags[1], cog_flag],
                                          switch_obj=None)
        # PV Right Arm
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='arm_pv',
                                          source_object=r_arm_component.pv_flag,
                                          target_list=[offset_flag, r_clav_flag, spine_sub_flags[1], cog_flag],
                                          switch_obj=None)

        # IKFK Right Foot
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=r_leg_switch_flag)

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
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

        # Spine Top
        frag.MultiConstraint.create(frag_rig,
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

        frag.MultiConstraint.create(frag_rig,
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

        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_prop',
                                          source_object=l_prop_flag,
                                          target_list=[l_weapon_flag,
                                                       r_weapon_flag,
                                                       floor_flag,
                                                       cog_flag,
                                                       l_leg_chain[0],
                                                       r_leg_chain[0],
                                                       pm.PyNode('hand_l')],
                                          switch_obj=None,
                                          default_name='r_weapon')

        # Right Hand Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_prop',
                                          source_object=r_prop_flag,
                                          target_list=[r_weapon_flag,
                                                       l_weapon_flag,
                                                       floor_flag,
                                                       cog_flag,
                                                       l_leg_chain[0],
                                                       r_leg_chain[0],
                                                       pm.PyNode('hand_r')],
                                          switch_obj=None,
                                          default_name='r_weapon')

        # Right Weapon
        frag.MultiConstraint.create(frag_rig,
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
        frag.MultiConstraint.create(frag_rig,
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


        # pelvis_cloth = chain.get_chain('pelvis_cloth', 'left')
        # pelvis_cloth_component = frag.FKComponent.create(frag_rig,
        #                                                  pelvis_cloth[0],
        #                                                  pelvis_cloth[1],
        #                                                  side='left',
        #                                                  region='pelvis_cloth',
        #                                                  scale=0.1,
        #                                                  lock_root_translate_axes=[],
        #                                                  lock_child_translate_axes=[])
        # pelvis_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        # pelvis_cloth_flag = pelvis_cloth_component.get_flags()[0]

        if finalize:
            frag_rig.rigTemplate.set(PlayerMaleTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class CommanderTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'commander'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(CommanderTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(CommanderTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = [x for x in frag_rig.get_frag_children(of_type=frag.RFKComponent) if 'neck' in str(x)]

        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, side='center', region='spine')[0]
        pelvis_component = [x for x in frag_rig.get_frag_children(of_type=frag.PelvisComponent) if
                            'pelvis' in str(x)]
        l_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, side='left', region='clav')
        r_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, side='right', region='clav')
        leg_component = frag_rig.get_frag_children(of_type=frag.ReverseFootComponent, side='left', region='leg')
        arm_r_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='right')
        arm_l_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='left')
        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not neck_component:
            self.log.error('No Neck Component found!')
            return
        neck_component = neck_component[0]

        if not pelvis_component:
            self.log.error('No Pelvis Component found!')
            return
        pelvis_component = pelvis_component[0]

        if not l_clav_component:
            self.log.error('No Left Clav Component found!')
            return
        l_clav_component = l_clav_component[0]

        if not r_clav_component:
            self.log.error('No Right Clav Component found!')
            return
        r_clav_component = r_clav_component[0]

        if not leg_component:
            self.log.error('No Leg Component found!')
            return
        if not arm_l_component:
            self.log.error('No arm_l_component found!')
            return
        arm_l_component = arm_l_component[0]

        if not arm_r_component:
            self.log.error('No arm_r_component found!')
            return
        arm_r_component = arm_r_component[0]
        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)
        spine = spine_component.end_flag
        head_flag = neck_component.end_flag
        l_clav_flag = l_clav_component.get_flags()[0]
        r_clav_flag = r_clav_component.get_flags()[0]

        # Hair Component
        hair_chain = chain.get_full_chain('hair', 'center')
        hair_lower_component = frag.FKComponent.create(
            frag_rig,
            hair_chain[0],
            hair_chain[-1],
            'center',
            'hair',
            scale=0.1,
            lock_root_translate_axes = [],
            lock_child_translate_axes = [])
        hair_lower_component.attach_component(neck_component, head_flag)

        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_l[0],
                                                        back_cloth_l[1],
                                                        side='left',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_r[0],
                                                        back_cloth_r[1],
                                                        side='right',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_l[0],
                                                         coat_l[1],
                                                         side='left',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_r[0],
                                                         coat_r[1],
                                                         side='right',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_r_component.get_flags()[0]

        upperarm_deformer_r = chain.get_chain('upperarm_deformer', 'right')
        upperarm_deformer_r_component = frag.FKComponent.create(frag_rig,
                                                         upperarm_deformer_r[0],
                                                         upperarm_deformer_r[1],
                                                         side='right',
                                                         region='upperarm_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        upperarm_deformer_r_component.attach_component(arm_r_component, pm.PyNode('upperarm_r'))
        upperarm_deformer_r_flag = upperarm_deformer_r_component.get_flags()[0]

        upperarm_deformer_l = chain.get_chain('upperarm_deformer', 'left')
        upperarm_deformer_l_component = frag.FKComponent.create(frag_rig,
                                                         upperarm_deformer_l[0],
                                                         upperarm_deformer_l[1],
                                                         side='left',
                                                         region='upperarm_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        upperarm_deformer_l_component.attach_component(arm_l_component, pm.PyNode('upperarm_l'))
        upperarm_deformer_l_flag = upperarm_deformer_l_component.get_flags()[0]

        # Sword Component
        # leg_unequip_joint = chain.get_start('thigh_unequip', 'left')
        # sword_component = frag.FKComponent.create(
        #     frag_rig,
        #     leg_unequip_joint,
        #     leg_unequip_joint,
        #     'left',
        #     'thigh_unequip',
        #     scale=0.35,
        #     lock_root_translate_axes=(),
        #     lock_child_translate_axes=())
        # sword_component.attach_component(pelvis_component, pm.PyNode(pelvis_flag))
        # sword_flags = sword_component.get_flags()


        # frag.MultiConstraint.create(
        #     frag_rig,
        #     side='left',
        #     region='sword',
        #     source_object=sword_flags[-1],
        #     target_list=[pelvis_flag, leg_flag, offset_flag],
        #     translate=False,
        #     switch_obj=None)

        frag_rig.rigTemplate.set(CommanderTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class DemonTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'demon'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(DemonTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(DemonTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine')

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not neck_component:
            self.log.error('No Neck Component found!')
            return
        neck_component = neck_component[0]

        if not spine_component:
            self.log.error('No Spine Component found!')
            return
        spine_component = spine_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        r_breasts = chain.get_start('breasts', 'right')
        r_breasts_component = frag.FKComponent.create(frag_rig,
                                                            r_breasts,
                                                            r_breasts,
                                                            side='right',
                                                            region='breasts',
                                                            lock_root_translate_axes=[])
        r_breasts_component.attach_component(spine_component, pm.PyNode('spine_04'))
        r_breasts_flag = r_breasts_component.get_end_flag()

        l_breasts = chain.get_start('breasts', 'left')
        l_breasts_component = frag.FKComponent.create(frag_rig,
                                                            l_breasts,
                                                            l_breasts,
                                                            side='left',
                                                            region='breasts',
                                                            lock_root_translate_axes=[])
        l_breasts_component.attach_component(spine_component, pm.PyNode('spine_04'))
        l_breasts_flag = l_breasts_component.get_end_flag()

        r_hair_upper = chain.get_chain('hair_upper', 'right')
        r_hair_upper_component = frag.FKComponent.create(frag_rig,
                                                               r_hair_upper[0],
                                                               r_hair_upper[1],
                                                               side='right',
                                                               region='hair_upper')
        r_hair_upper_component.attach_component(neck_component, pm.PyNode('head'))
        r_hair_upper_flag = r_hair_upper_component.get_end_flag()

        l_hair_upper = chain.get_chain('hair_upper', 'left')
        l_hair_upper_component = frag.FKComponent.create(frag_rig,
                                                               l_hair_upper[0],
                                                               l_hair_upper[1],
                                                               side='left',
                                                               region='hair_upper')
        l_hair_upper_component.attach_component(neck_component, pm.PyNode('head'))
        l_hair_upper_flag = l_hair_upper_component.get_end_flag()

        l_hair_lower = chain.get_chain('hair_lower', 'left')
        l_hair_lower_component = frag.FKComponent.create(frag_rig,
                                                               l_hair_lower[0],
                                                               l_hair_lower[1],
                                                               side='left',
                                                               region='hair_lower')
        l_hair_lower_component.attach_component(neck_component, pm.PyNode('head'))
        l_hair_lower_flag = l_hair_lower_component.get_end_flag()

        r_hair_lower = chain.get_chain('hair_lower', 'right')
        r_hair_lower_component = frag.FKComponent.create(frag_rig,
                                                               r_hair_lower[0],
                                                               r_hair_lower[1],
                                                               side='right',
                                                               region='hair_lower')
        r_hair_lower_component.attach_component(neck_component, pm.PyNode('head'))
        r_hair_lower_flag = r_hair_lower_component.get_end_flag()

        hair_main = chain.get_chain('hair_main', 'center')
        hair_main_component = frag.FKComponent.create(frag_rig,
                                                            hair_main[0],
                                                            hair_main[1],
                                                            side='center',
                                                            region='hair_main')
        hair_main_component.attach_component(neck_component, pm.PyNode('head'))
        hair_main_flag = hair_main_component.get_end_flag()

        bracelet_01 = chain.get_chain('lowerarm_prop_01', 'left')
        bracelet_01_component = frag.FKComponent.create(frag_rig,
                                                              bracelet_01[0],
                                                              bracelet_01[1],
                                                              side='left',
                                                              region='lowerarm_prop_01',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        bracelet_01_component.attach_component(spine_component, pm.PyNode('lowerarm_twist_01_l'))
        bracelet_01_flag = bracelet_01_component.get_end_flag()
        bracelet_01_flag.set_as_detail()

        bracelet_02 = chain.get_chain('lowerarm_prop_02', 'left')
        bracelet_02_component = frag.FKComponent.create(frag_rig,
                                                              bracelet_02[0],
                                                              bracelet_02[1],
                                                              side='left',
                                                              region='lowerarm_prop_02',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        bracelet_02_component.attach_component(spine_component, pm.PyNode('lowerarm_twist_01_l'))
        bracelet_02_flag = bracelet_02_component.get_end_flag()
        bracelet_02_flag.set_as_detail()

        bracelet_03 = chain.get_chain('lowerarm_prop_03', 'left')
        bracelet_03_component = frag.FKComponent.create(frag_rig,
                                                              bracelet_03[0],
                                                              bracelet_03[1],
                                                              side='left',
                                                              region='lowerarm_prop_03',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        bracelet_03_component.attach_component(spine_component, pm.PyNode('lowerarm_twist_01_l'))
        bracelet_03_flag = bracelet_03_component.get_end_flag()
        bracelet_03_flag.set_as_detail()

        bracelet_04 = chain.get_chain('lowerarm_prop_04', 'left')
        bracelet_04_component = frag.FKComponent.create(frag_rig,
                                                              bracelet_04[0],
                                                              bracelet_04[1],
                                                              side='left',
                                                              region='lowerarm_prop_04',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        bracelet_04_component.attach_component(spine_component, pm.PyNode('lowerarm_twist_01_l'))
        bracelet_04_flag = bracelet_04_component.get_end_flag()
        bracelet_04_flag.set_as_detail()

        bracelet_05 = chain.get_chain('lowerarm_prop_05', 'left')
        bracelet_05_component = frag.FKComponent.create(frag_rig,
                                                              bracelet_05[0],
                                                              bracelet_05[1],
                                                              side='left',
                                                              region='lowerarm_prop_05',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        bracelet_05_component.attach_component(spine_component, pm.PyNode('lowerarm_twist_01_l'))
        bracelet_05_flag = bracelet_05_component.get_end_flag()
        bracelet_05_flag.set_as_detail()

        necklace_01 = chain.get_start('necklace_01', 'center')
        necklace_01_component = frag.FKComponent.create(frag_rig,
                                                              necklace_01,
                                                              necklace_01,
                                                              side='center',
                                                              region='necklace_01',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        necklace_01_component.attach_component(spine_component, pm.PyNode('spine_04'))
        necklace_01_flag = necklace_01_component.get_flags()

        necklace_02 = chain.get_start('necklace_02', 'center')
        necklace_02_component = frag.FKComponent.create(frag_rig,
                                                              necklace_02,
                                                              necklace_02,
                                                              side='center',
                                                              region='necklace_02',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        necklace_02_component.attach_component(spine_component, pm.PyNode('spine_04'))
        necklace_02_flag = necklace_02_component.get_flags()

        necklace_03 = chain.get_chain('necklace_03', 'center')
        necklace_03_component = frag.FKComponent.create(frag_rig,
                                                              necklace_03[0],
                                                              necklace_03[1],
                                                              side='center',
                                                              region='necklace_03',
                                                              lock_root_translate_axes=[],
                                                              lock_child_translate_axes=[])
        necklace_03_component.attach_component(spine_component, pm.PyNode('spine_04'))
        necklace_03_flag = necklace_03_component.get_flags()

        breast_l = chain.get_chain('breast', 'left')
        breast_l_component = frag.FKComponent.create(frag_rig,
                                                           breast_l[0],
                                                           breast_l[1],
                                                           side='left',
                                                           region='breast',
                                                           lock_root_translate_axes=[],
                                                           lock_child_translate_axes=[])
        breast_l_flag = breast_l_component.get_end_flag()
        breast_l_flag.set_as_sub()

        breast_r = chain.get_chain('breast', 'right')
        breast_r_component = frag.FKComponent.create(frag_rig,
                                                           breast_r[0],
                                                           breast_r[1],
                                                           side='right',
                                                           region='breast',
                                                           lock_root_translate_axes=[],
                                                           lock_child_translate_axes=[])
        breast_r_flag = breast_r_component.get_end_flag()
        breast_r_flag.set_as_sub()

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='breast',
                                          source_object=breast_l_flag,
                                          target_list=[l_breasts_flag,
                                                       r_breasts_flag],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='breast',
                                          source_object=breast_r_flag,
                                          target_list=[l_breasts_flag,
                                                       r_breasts_flag],
                                          switch_obj=None)

        frag_rig.rigTemplate.set(DemonTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class OperatorTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'p4om-yx7g7-4mjkq-3748'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(OperatorTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(OperatorTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine')
        arm_r_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='right')
        arm_l_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='left')
        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not neck_component:
            self.log.error('No Neck Component found!')
            return
        neck_component = neck_component[0]

        if not spine_component:
            self.log.error('No Spine Component found!')
            return
        spine_component = spine_component[0]

        if not pelvis_component:
            self.log.error('No Pelvis Component found!')
            return
        pelvis_component = pelvis_component[0]

        if not arm_l_component:
            self.log.error('No arm_l_component found!')
            return
        arm_l_component = arm_l_component[0]

        if not arm_r_component:
            self.log.error('No arm_r_component found!')
            return
        arm_r_component = arm_r_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        l_hair = chain.get_chain('hair', 'left')
        l_hair_component = frag.FKComponent.create(frag_rig,
                                                         l_hair[0],
                                                         l_hair[1],
                                                         side='left',
                                                         region='hair',
                                                         scale=0.1)
        l_hair_component.attach_component(neck_component, pm.PyNode('head'))
        l_hair_flag = l_hair_component.get_flags()[0]

        r_hair = chain.get_chain('hair', 'right')
        r_hair_component = frag.FKComponent.create(frag_rig,
                                                         r_hair[0],
                                                         r_hair[1],
                                                         side='right',
                                                         region='hair',
                                                         scale=0.1)
        r_hair_component.attach_component(neck_component, pm.PyNode('head'))
        r_hair_flag = r_hair_component.get_flags()[0]

        shirt = chain.get_chain('shirt_back', 'center')
        shirt_component = frag.FKComponent.create(frag_rig,
                                                        shirt[0],
                                                        shirt[1],
                                                        side='center',
                                                        region='shirt_back',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        shirt_component.attach_component(spine_component, pm.PyNode('spine_04'))
        shirt_flag = shirt_component.get_flags()[0]

        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_l[0],
                                                        back_cloth_l[1],
                                                        side='left',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_r[0],
                                                        back_cloth_r[1],
                                                        side='right',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        back_cloth_r_flag = back_cloth_r_component.get_flags()[0]

        coat_pd_l = chain.get_chain('coat_pd', 'left')
        coat_pd_l_component = frag.FKComponent.create(frag_rig,
                                                   coat_pd_l[0],
                                                   coat_pd_l[0],
                                                   side='left',
                                                   region='coat_pd',
                                                   scale=0.1,
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_pd_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_pd_l_flag = coat_pd_l_component.get_flags()[0]

        coat_pd_r = chain.get_chain('coat_pd', 'right')
        coat_pd_r_component = frag.FKComponent.create(frag_rig,
                                                   coat_pd_r[0],
                                                   coat_pd_r[0],
                                                   side='right',
                                                   region='coat_pd',
                                                   scale=0.1,
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_pd_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_l[0],
                                                         coat_l[1],
                                                         side='left',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_l_component.attach_component(coat_pd_l_component, coat_pd_l[0])
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_r[0],
                                                         coat_r[1],
                                                         side='right',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_r_component.attach_component(coat_pd_r_component, coat_pd_r[0])
        coat_r_flag = coat_r_component.get_flags()[0]

        # upperarm_deformer_r = chain.get_chain('upperarm_deformer', 'right')
        # upperarm_deformer_r_component = frag.FKComponent.create(frag_rig,
        #                                                  upperarm_deformer_r[0],
        #                                                  upperarm_deformer_r[1],
        #                                                  side='right',
        #                                                  region='upperarm_deformer',
        #                                                  scale=0.1,
        #                                                  lock_root_translate_axes=[],
        #                                                  lock_child_translate_axes=[])
        # upperarm_deformer_r_component.attach_component(arm_r_component, pm.PyNode('upperarm_r'))
        # upperarm_deformer_r_flag = upperarm_deformer_r_component.get_flags()[0]
        #
        # upperarm_deformer_l = chain.get_chain('upperarm_deformer', 'left')
        # upperarm_deformer_l_component = frag.FKComponent.create(frag_rig,
        #                                                  upperarm_deformer_l[0],
        #                                                  upperarm_deformer_l[1],
        #                                                  side='left',
        #                                                  region='upperarm_deformer',
        #                                                  scale=0.1,
        #                                                  lock_root_translate_axes=[],
        #                                                  lock_child_translate_axes=[])
        # upperarm_deformer_l_component.attach_component(arm_l_component, pm.PyNode('upperarm_l'))
        # upperarm_deformer_l_flag = upperarm_deformer_l_component.get_flags()[0]

        pelvis_cloth = chain.get_chain('pelvis_cloth', 'left')
        pelvis_cloth_component = frag.FKComponent.create(frag_rig,
                                                   pelvis_cloth[0],
                                                   pelvis_cloth[1],
                                                   side='left',
                                                   region='pelvis_cloth',
                                                   scale=0.1,
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        pelvis_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        pelvis_cloth_flag = pelvis_cloth_component.get_flags()[0]

        frag_rig.rigTemplate.set(OperatorTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        # Flag Rotation Changes
        XYZ = ('f_clavicle_l', 'f_clavicle_r', 'f_lowerarm_l', 'f_lowerarm_r', 'f_left_leg', 'f_right_leg', 'f_ball_l',
               'f_ball_r', 'f_calf_l', 'f_calf_r')
        XZY = ('f_upperarm_l', 'f_upperarm_r')
        YXZ = ('f_cog', 'f_pelvis')
        YZX = ('f_spine_01', 'f_spine_01_sub', 'f_spine_02', 'f_spine_03', 'f_spine_04', 'f_spine_04_sub')
        ZXY = ('f_hand_l', 'f_hand_r', 'f_hand_l_offset', 'f_hand_r_offset', 'f_thigh_l', 'f_thigh_r')
        ZYX = ('f_neck_01', 'f_neck_02', 'f_head', 'f_left_arm', 'f_right_arm', 'f_left_arm_offset',
               'f_right_arm_offset', 'f_foot_l', 'f_foot_r', 'f_foot_l_offset', 'f_foot_r_offset')

        rotateString = '.rotateOrder'

        for x in XYZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 0)

        for x in XZY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 3)

        for x in YXZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 4)

        for x in YZX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 1)

        for x in ZXY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 2)

        for x in ZYX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 5)

        return frag_rig

class AngelTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'angel'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(AngelTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(AngelTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine')
        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent, region='cog')
        arm_r_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='right')
        arm_l_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='left')

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not spine_component:
            self.log.error('No Spine Component found!')
            return
        if not arm_l_component:
            self.log.error('No arm_l_component found!')
            return
        arm_l_component = arm_l_component[0]

        if not arm_r_component:
            self.log.error('No arm_r_component found!')
            return
        arm_r_component = arm_r_component[0]

        spine_component = spine_component[0]
        pelvis_component = pelvis_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)
        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_l[0],
                                                        back_cloth_l[1],
                                                        side='left',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_r[0],
                                                        back_cloth_r[1],
                                                        side='right',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))


        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_l[0],
                                                         coat_l[1],
                                                         side='left',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_r[0],
                                                         coat_r[1],
                                                         side='right',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_r_component.get_flags()[0]

        upperarm_deformer_r = chain.get_chain('upperarm_deformer', 'right')
        upperarm_deformer_r_component = frag.FKComponent.create(frag_rig,
                                                         upperarm_deformer_r[0],
                                                         upperarm_deformer_r[1],
                                                         side='right',
                                                         region='upperarm_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        upperarm_deformer_r_component.attach_component(arm_r_component, pm.PyNode('upperarm_r'))
        upperarm_deformer_r_flag = upperarm_deformer_r_component.get_flags()[0]

        upperarm_deformer_l = chain.get_chain('upperarm_deformer', 'left')
        upperarm_deformer_l_component = frag.FKComponent.create(frag_rig,
                                                         upperarm_deformer_l[0],
                                                         upperarm_deformer_l[1],
                                                         side='left',
                                                         region='upperarm_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        upperarm_deformer_l_component.attach_component(arm_l_component, pm.PyNode('upperarm_l'))
        upperarm_deformer_l_flag = upperarm_deformer_l_component.get_flags()[0]

        frag_rig.rigTemplate.set(OperatorTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        coat_upper_l = chain.get_chain('coat_upper', 'left')
        coat_upper_l_component = frag.FKComponent.create(frag_rig,
                                                               coat_upper_l[0],
                                                               coat_upper_l[1],
                                                               side='left',
                                                               region='coat_upper',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        coat_upper_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
        coat_upper_l_flag = coat_upper_l_component.get_flags()[0]

        coat_upper_r = chain.get_chain('coat_upper', 'right')
        coat_upper_r_component = frag.FKComponent.create(frag_rig,
                                                               coat_upper_r[0],
                                                               coat_upper_r[1],
                                                               side='right',
                                                               region='coat_upper',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        coat_upper_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
        coat_upper_r_flag = coat_upper_r_component.get_flags()[0]

        shirt = chain.get_start('shirt_back', 'center')
        shirt_component = frag.FKComponent.create(frag_rig,
                                                        shirt,
                                                        shirt,
                                                        side='center',
                                                        region='shirt_back',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        shirt_component.attach_component(spine_component, pm.PyNode('spine_04'))
        shirt_flag = shirt_component.get_flags()[0]

        frag_rig.rigTemplate.set(AngelTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class ArchivistTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'archivist'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(ArchivistTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(ArchivistTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')

        if not root_component:
            logger.warning('No Root Component found!')
            return

        if not neck_component:
            logger.warning('No Neck Component found!')
            return
        neck_component = neck_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        nose_prop = chain.get_chain('nose_prop', 'center')
        nose_prop_component = frag.FKComponent.create(frag_rig,
                                                         nose_prop[0],
                                                         nose_prop[1],
                                                         side='center',
                                                         region='nose_prop',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        nose_prop_component.attach_component(neck_component, pm.PyNode('head'))
        nose_prop_flag = nose_prop_component.get_flags()[0]

        frag_rig.rigTemplate.set(ArchivistTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class ScientistTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'scientist'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(ScientistTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(ScientistTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine')
        cog_component = frag_rig.get_frag_children(of_type=frag.CogComponent, region='cog')
        head_component = frag_rig.get_frag_children(of_type=frag.CogComponent, region='neck')

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not spine_component:
            self.log.error('No Spine Component found!')
            return
        spine_component = spine_component[0]

        if not cog_component:
            self.log.error('No Cog Component found!')
            return
        cog_component = cog_component[0]
        if not head_component:
            self.log.error('No Head Component found!')
            return
        head_component = head_component[0]
        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_l[0],
                                                         coat_l[1],
                                                         side='left',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_l_component.attach_component(spine_component, pm.PyNode('spine_01'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_r[0],
                                                         coat_r[1],
                                                         side='right',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_r_component.attach_component(spine_component, pm.PyNode('spine_01'))
        coat_r_flag = coat_r_component.get_flags()[0]

        coat_back = chain.get_chain('coat', 'center')
        coat_back_component = frag.FKComponent.create(frag_rig,
                                                            coat_back[0],
                                                            coat_back[1],
                                                            side='center',
                                                            region='coat',
                                                            scale=0.1,
                                                            lock_root_translate_axes=[],
                                                            lock_child_translate_axes=[])
        coat_back_component.attach_component(spine_component, pm.PyNode('spine_01'))
        coat_back_flag = coat_back_component.get_flags()[0]

        coat_inner_r = chain.get_chain('coat_inner', 'right')
        coat_inner_r_component = frag.FKComponent.create(frag_rig,
                                                               coat_inner_r[0],
                                                               coat_inner_r[1],
                                                               side='right',
                                                               region='coat_inner',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        coat_inner_r_component.attach_component(spine_component, pm.PyNode('spine_01'))
        coat_inner_r_flag = coat_inner_r_component.get_flags()[0]

        coat_inner_l = chain.get_chain('coat_inner', 'left')
        coat_inner_l_component = frag.FKComponent.create(frag_rig,
                                                               coat_inner_l[0],
                                                               coat_inner_l[1],
                                                               side='left',
                                                               region='coat_inner',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        coat_inner_l_component.attach_component(spine_component, pm.PyNode('spine_01'))
        coat_inner_l_flag = coat_inner_l_component.get_flags()[0]

        earring_l = chain.get_chain('earring', 'left')
        earring_l_component = frag.FKComponent.create(frag_rig,
                                                               earring_l[0],
                                                               earring_l[1],
                                                               side='left',
                                                               region='earring',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        earring_l_component.attach_component(head_component, pm.PyNode('head'))
        earring_l_flag = earring_l_component.get_flags()[0]

        earring_r = chain.get_chain('earring', 'right')
        earring_r_component = frag.FKComponent.create(frag_rig,
                                                               earring_r[0],
                                                               earring_r[1],
                                                               side='right',
                                                               region='earring',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        earring_r_component.attach_component(head_component, pm.PyNode('head'))
        earring_r_flag = earring_r_component.get_flags()[0]

        monocle = chain.get_chain('monocle', 'right')
        monocle_component = frag.FKComponent.create(frag_rig,
                                                               monocle[0],
                                                               monocle[1],
                                                               side='right',
                                                               region='monocle',
                                                               scale=0.1,
                                                               lock_root_translate_axes=[],
                                                               lock_child_translate_axes=[])
        monocle_component.attach_component(head_component, pm.PyNode('head'))
        monocle_flag = monocle_component.get_flags()[0]


        frag_rig.rigTemplate.set(ScientistTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class TacticalSkirmisherTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'eliteskirmisher'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(TacticalSkirmisherTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(TacticalSkirmisherTemplate, self).build(finalize=False)
        print(frag_rig)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        r_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, region='clav', side='right')
        l_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, region='clav', side='left')

        if not root_component:
            logger.warning('No Root Component found!')
            return

        if not r_clav_component:
            logger.warning('No Right Clavicle Component found!')
            return
        r_clav_component = r_clav_component[0]

        if not l_clav_component:
            logger.warning('No Left Clavicle Component found!')
            return
        l_clav_component = l_clav_component[0]
        if not neck_component:
            logger.warning('No Neck Component found!')
            return
        neck_component = neck_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        neck_collar_l = chain.get_chain('neck_collar', 'left')
        neck_collar_l_component = frag.FKComponent.create(frag_rig,
                                                         neck_collar_l[0],
                                                         neck_collar_l[1],
                                                         side='left',
                                                         region='neck_collar',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        neck_collar_l_component.attach_component(neck_component, pm.PyNode('neck_01'))
        neck_collar_l_flag = neck_collar_l_component.get_flags()[0]

        neck_collar_r = chain.get_chain('neck_collar', 'right')
        neck_collar_r_component = frag.FKComponent.create(frag_rig,
                                                         neck_collar_r[0],
                                                         neck_collar_r[1],
                                                         side='right',
                                                         region='neck_collar',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        neck_collar_r_component.attach_component(neck_component, pm.PyNode('neck_01'))
        neck_collar_r_flag = neck_collar_r_component.get_flags()[0]

        clavicle_deformer_r = chain.get_chain('clavicle_deformer', 'right')
        clavicle_deformer_r_component = frag.FKComponent.create(frag_rig,
                                                         clavicle_deformer_r[0],
                                                         clavicle_deformer_r[1],
                                                         side='right',
                                                         region='clavicle_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        clavicle_deformer_r_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
        clavicle_deformer_r_flag = clavicle_deformer_r_component.get_flags()[0]


        clavicle_deformer_l = chain.get_chain('clavicle_deformer', 'left')
        clavicle_deformer_l_component = frag.FKComponent.create(frag_rig,
                                                         clavicle_deformer_l[0],
                                                         clavicle_deformer_l[1],
                                                         side='left',
                                                         region='clavicle_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        clavicle_deformer_l_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        clavicle_deformer_l_flag = clavicle_deformer_l_component.get_flags()[0]



        frag_rig.rigTemplate.set(TacticalSkirmisherTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())
        return frag_rig


class DemonicCrawlerTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'demonic_crawler'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(DemonicCrawlerTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        pm.namespace(set=':')
        frag_rig = super(DemonicCrawlerTemplate, self).build(finalize=False)

        frag_root = frag_rig.get_frag_parent()

        skel_root = frag_root.root_joint
        skel_hierarchy = chain_markup.ChainMarkup(skel_root)

        head_component = lists.get_first_in_list(frag_rig.get_frag_children(side='center', region='neck'))
        head_joint = skel_hierarchy.get_end('neck', 'center')

        jaw_joint = skel_hierarchy.get_start('jaw', 'center')
        jaw_component = frag.FKComponent.create(frag_rig,
                                                                      jaw_joint,
                                                                      jaw_joint,
                                                                      side='center',
                                                                      region='jaw',
                                                                      scale=0.1)
        jaw_component.attach_component(head_component, head_joint)

        for side in ['left', 'right']:
            for hair_region in ['front', 'back']:
                start_joint, end_joint = skel_hierarchy.get_chain(f'hair_{hair_region}', side)
                if not start_joint:
                    continue
                hair_component = frag.FKComponent.create(frag_rig,
                                                              start_joint,
                                                              end_joint,
                                                              side=side,
                                                              region=f'hair_{hair_region}',
                                                              scale=0.1)
                hair_component.attach_component(head_component, head_joint)

        start_joint, end_joint = skel_hierarchy.get_chain(f'hair', 'center')
        if start_joint:
            hair_component = frag.FKComponent.create(frag_rig,
                                                           start_joint,
                                                           end_joint,
                                                           side='center',
                                                           region=f'hair',
                                                           scale=0.1)
            hair_component.attach_component(head_component, head_joint)

        frag_rig.rigTemplate.set(DemonicCrawlerTemplate.__name__)
        if finalize:
            frag_rig.finalize_rig(self.get_flags_path())
        return frag_rig

class PossessedStrikerTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'possessed_striker'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(PossessedStrikerTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(PossessedStrikerTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        r_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, region='clav', side='right')
        l_clav_component = frag_rig.get_frag_children(of_type=frag.FKComponent, region='clav', side='left')

        if not root_component:
            logger.warning('No Root Component found!')
            return

        if not r_clav_component:
            logger.warning('No Right Clavicle Component found!')
            return
        r_clav_component = r_clav_component[0]

        if not l_clav_component:
            logger.warning('No Left Clavicle Component found!')
            return
        l_clav_component = l_clav_component[0]
        if not neck_component:
            logger.warning('No Neck Component found!')
            return
        neck_component = neck_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        jaw = chain.get_start('jaw', 'center')
        jaw_component = frag.FKComponent.create(frag_rig,
                                                      jaw,
                                                      jaw,
                                                      side='center',
                                                      region='jaw',
                                                      lock_root_translate_axes=[])
        jaw_component.attach_component(neck_component, pm.PyNode('head'))

        clavicle_deformer_r = chain.get_chain('clavicle_deformer', 'right')
        clavicle_deformer_r_component = frag.FKComponent.create(frag_rig,
                                                         clavicle_deformer_r[0],
                                                         clavicle_deformer_r[1],
                                                         side='right',
                                                         region='clavicle_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        clavicle_deformer_r_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
        clavicle_deformer_r_flag = clavicle_deformer_r_component.get_flags()[0]


        clavicle_deformer_l = chain.get_chain('clavicle_deformer', 'left')
        clavicle_deformer_l_component = frag.FKComponent.create(frag_rig,
                                                         clavicle_deformer_l[0],
                                                         clavicle_deformer_l[1],
                                                         side='left',
                                                         region='clavicle_deformer',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        clavicle_deformer_l_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        clavicle_deformer_l_flag = clavicle_deformer_l_component.get_flags()[0]



        frag_rig.rigTemplate.set(PossessedStrikerTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())
        return frag_rig


class PlayerTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'player_male'
    ASSET_TYPE = 'player'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(PlayerTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(PlayerTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not neck_component:
            self.log.error('No Neck Component found!')
            return
        neck_component = neck_component[0]

        if not pelvis_component:
            self.log.error('No Pelvis Component found!')
            return
        pelvis_component = pelvis_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        neck_collar_l = chain.get_chain('neck_collar', 'left')
        neck_collar_l_component = frag.FKComponent.create(frag_rig,
                                                         neck_collar_l[0],
                                                         neck_collar_l[1],
                                                         side='left',
                                                         region='neck_collar',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        neck_collar_l_component.attach_component(neck_component, pm.PyNode('neck_01'))
        neck_collar_l_flag = neck_collar_l_component.get_flags()[0]

        neck_collar_r = chain.get_chain('neck_collar', 'right')
        neck_collar_r_component = frag.FKComponent.create(frag_rig,
                                                         neck_collar_r[0],
                                                         neck_collar_r[1],
                                                         side='right',
                                                         region='neck_collar',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        neck_collar_r_component.attach_component(neck_component, pm.PyNode('neck_01'))
        neck_collar_r_flag = neck_collar_r_component.get_flags()[0]

        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_l[0],
                                                        back_cloth_l[1],
                                                        side='left',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                        back_cloth_r[0],
                                                        back_cloth_r[1],
                                                        side='right',
                                                        region='back_cloth',
                                                        scale=0.1,
                                                        lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_l[0],
                                                         coat_l[1],
                                                         side='left',
                                                         region='coat',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        frag_rig.rigTemplate.set(PlayerTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class ZaminaChildTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = '2vjc-hqinj-uc1zy-otxr'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(ZaminaChildTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(ZaminaChildTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck')
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine')
        arm_r_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='right')
        arm_l_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='left')
        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)

        if not root_component:
            self.log.error('No Root Component found!')
            return

        if not neck_component:
            self.log.error('No Neck Component found!')
            return
        neck_component = neck_component[0]

        if not spine_component:
            self.log.error('No Spine Component found!')
            return
        spine_component = spine_component[0]

        if not pelvis_component:
            self.log.error('No Pelvis Component found!')
            return
        pelvis_component = pelvis_component[0]

        if not arm_l_component:
            self.log.error('No arm_l_component found!')
            return
        arm_l_component = arm_l_component[0]

        if not arm_r_component:
            self.log.error('No arm_r_component found!')
            return
        arm_r_component = arm_r_component[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        pelvis_cloth = chain.get_chain('pelvis_cloth', 'left')
        pelvis_cloth_component = frag.FKComponent.create(frag_rig,
                                                         pelvis_cloth[0],
                                                         pelvis_cloth[1],
                                                         side='left',
                                                         region='pelvis_cloth',
                                                         scale=0.8,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        pelvis_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        pelvis_cloth_flag = pelvis_cloth_component.get_flags()[0]

        sleeve_l = chain.get_chain('sleeve', 'left')
        sleeve_l_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_l[0],
                                                     sleeve_l[1],
                                                     side='left',
                                                     region='sleeve',
                                                     lock_root_translate_axes=['tx', 'ty', 'tz'],
                                                     lock_child_translate_axes=[])
        sleeve_l_component.attach_component(arm_l_component, pm.PyNode('lowerarm_l'))

        sleeve_r = chain.get_chain('sleeve', 'right')
        sleeve_r_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_r[0],
                                                     sleeve_r[1],
                                                     side='right',
                                                     region='sleeve',
                                                     lock_root_translate_axes=['tx', 'ty', 'tz'],
                                                     lock_child_translate_axes=[])
        sleeve_r_component.attach_component(arm_r_component, pm.PyNode('lowerarm_r'))


        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                   coat_l[0],
                                                   coat_l[1],
                                                   side='left',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                   coat_r[0],
                                                   coat_r[1],
                                                   side='right',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_r_component.get_flags()[0]
        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_l[0],
                                                         back_cloth_l[1],
                                                         side='left',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_r[0],
                                                         back_cloth_r[1],
                                                         side='right',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        frag_rig.rigTemplate.set(ZaminaChildTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        # Flag Rotation Changes
        XYZ = ('f_clavicle_l', 'f_clavicle_r', 'f_lowerarm_l', 'f_lowerarm_r', 'f_left_leg', 'f_right_leg', 'f_ball_l',
               'f_ball_r', 'f_calf_l', 'f_calf_r')
        XZY = ('f_upperarm_l', 'f_upperarm_r')
        YXZ = ('f_cog', 'f_pelvis')
        YZX = ('f_spine_01', 'f_spine_01_sub', 'f_spine_02', 'f_spine_03', 'f_spine_04', 'f_spine_04_sub')
        ZXY = ('f_hand_l', 'f_hand_r', 'f_hand_l_offset', 'f_hand_r_offset', 'f_thigh_l', 'f_thigh_r')
        ZYX = ('f_neck_01', 'f_neck_02', 'f_head', 'f_left_arm', 'f_right_arm', 'f_left_arm_offset',
               'f_right_arm_offset', 'f_foot_l', 'f_foot_r', 'f_foot_l_offset', 'f_foot_r_offset')

        rotateString = '.rotateOrder'

        for x in XYZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 0)

        for x in XZY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 3)

        for x in YXZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 4)

        for x in YZX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 1)

        for x in ZXY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 2)

        for x in ZYX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 5)

        return frag_rig

class AngeloSacrificeTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'osc3-be91h-cvbnz-6bw9'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(AngeloSacrificeTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(AngeloSacrificeTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()

        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine', side='center')[0]
        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)[0]
        cog_component = frag_rig.get_frag_children(of_type=frag.CogComponent)[0]
        world_component = frag_rig.get_frag_children(of_type=frag.WorldComponent)[0]

        pelvis_flag = pelvis_component.get_flags()[0]
        cog_flag = cog_component.get_flags()[0]
        offset_flag = world_component.offset_flag
        spine_flag = spine_component.start_flag


        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_l[0],
                                                         back_cloth_l[1],
                                                         side='left',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_r[0],
                                                         back_cloth_r[1],
                                                         side='right',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        back_cloth_r_flag = back_cloth_r_component.get_flags()[0]
        coat_inner_r = chain.get_chain('coat_inner', 'right')
        coat_inner_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_inner_r[0],
                                                         coat_inner_r[1],
                                                         side='right',
                                                         region='coat_inner',
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_inner_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_inner_r_flag = coat_inner_r_component.get_flags()[0]

        coat_inner_l = chain.get_chain('coat_inner', 'left')
        coat_inner_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_inner_l[0],
                                                         coat_inner_l[1],
                                                         side='left',
                                                         region='coat_inner',
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_inner_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_inner_l_flag = coat_inner_l_component.get_flags()[0]

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                   coat_l[0],
                                                   coat_l[1],
                                                   side='left',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                   coat_r[0],
                                                   coat_r[1],
                                                   side='right',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_r_component.get_flags()[0]

        coat_middle = chain.get_chain('coat_middle', 'center')
        coat_middle_component = frag.FKComponent.create(frag_rig,
                                                   coat_middle[0],
                                                   coat_middle[1],
                                                   side='center',
                                                   region='coat_middle',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_middle_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_middle_flag = coat_middle_component.get_flags()[0]

        collar_01_l = chain.get_chain('collar_01', 'left')
        collar_01_l_component = frag.FKComponent.create(frag_rig,
                                                   collar_01_l[0],
                                                   collar_01_l[1],
                                                   side='left',
                                                   region='collar_01',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        collar_01_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_01_l_flag = collar_01_l_component.get_flags()[0]

        collar_01_r = chain.get_chain('collar_01', 'right')
        collar_01_r_component = frag.FKComponent.create(frag_rig,
                                                   collar_01_r[0],
                                                   collar_01_r[1],
                                                   side='right',
                                                   region='collar_01',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        collar_01_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_01_r_flag = collar_01_r_component.get_flags()[0]

        robe = chain.get_chain('robe', 'center')
        robe_component = frag.FKComponent.create(frag_rig,
                                                        robe[0],
                                                        robe[1],
                                                        side='center',
                                                        region='robe',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        robe_component.attach_component(cog_component, pm.PyNode(cog_flag))
        robe_flag = robe_component.get_flags()[0]


        ### Multi Constraints ###############

        # Coat Middle
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='coat_middle',
                                    source_object=coat_middle_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='coat',
                                    source_object=coat_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='coat',
                                    source_object=coat_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Inner Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='coat_inner',
                                    source_object=coat_inner_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Inner Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='coat_inner',
                                    source_object=coat_inner_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Back Cloth Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='back_cloth',
                                    source_object=back_cloth_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Back Cloth Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='back_cloth',
                                    source_object=back_cloth_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Collar 01 Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='collar_01',
                                    source_object=collar_01_l_flag,
                                    target_list=[offset_flag, cog_flag, spine_flag],
                                    switch_obj=None,
                                    translate=True)
        # Collar 01 Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='collar_01',
                                    source_object=collar_01_r_flag,
                                    target_list=[offset_flag, cog_flag, spine_flag],
                                    switch_obj=None,
                                    translate=True)

        # Robe
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='robe',
                                    source_object=robe_flag,
                                    target_list=[offset_flag, cog_flag],
                                    switch_obj=None,
                                    translate=True)


        frag_rig.rigTemplate.set(AngeloSacrificeTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        # Flag Rotation Changes
        XYZ = ('f_clavicle_l', 'f_clavicle_r', 'f_lowerarm_l', 'f_lowerarm_r', 'f_left_leg', 'f_right_leg', 'f_ball_l',
               'f_ball_r', 'f_calf_l', 'f_calf_r')
        XZY = ('f_upperarm_l', 'f_upperarm_r')
        YXZ = ('f_cog', 'f_pelvis')
        YZX = ('f_spine_01', 'f_spine_01_sub', 'f_spine_02', 'f_spine_03', 'f_spine_04', 'f_spine_04_sub')
        ZXY = ('f_hand_l', 'f_hand_r', 'f_hand_l_offset', 'f_hand_r_offset', 'f_thigh_l', 'f_thigh_r')
        ZYX = ('f_neck_01', 'f_neck_02', 'f_head', 'f_left_arm', 'f_right_arm', 'f_left_arm_offset',
               'f_right_arm_offset', 'f_foot_l', 'f_foot_r', 'f_foot_l_offset', 'f_foot_r_offset')

        rotateString = '.rotateOrder'

        for x in XYZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 0)

        for x in XZY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 3)

        for x in YXZ:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 4)

        for x in YZX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 1)

        for x in ZXY:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 2)

        for x in ZYX:
            flagName = f'{x}{rotateString}'
            pm.setAttr(flagName, 5)

        return frag_rig

class AngeloTemplate(AngeloSacrificeTemplate):
    VERSION = 1
    ASSET_ID = 'pih0-h0sal-kl1oj-ps4m'
    ASSET_TYPE = 'npc'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(AngeloTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')

        frag_rig = super(AngeloSacrificeTemplate, self).build(finalize=False)
        root_component = frag_rig.get_frag_parent()

        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)[0]
        spine_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='spine', side='center')[0]
        cog_component = frag_rig.get_frag_children(of_type=frag.CogComponent)[0]
        world_component = frag_rig.get_frag_children(of_type=frag.WorldComponent)[0]
        arm_r_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='right')[0]
        arm_l_component = frag_rig.get_frag_children(of_type=frag.IKFKComponent, region='arm', side='left')[0]
        neck_component = frag_rig.get_frag_children(of_type=frag.RFKComponent, region='neck', side='center')[0]

        pelvis_flag = pelvis_component.get_flags()[0]
        cog_flag = cog_component.get_flags()[0]
        offset_flag = world_component.offset_flag
        spine_flag = spine_component.end_flag
        neck_start_flag = neck_component.start_flag
        neck_end_flag = neck_component.end_flag

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        back_cloth_l = chain.get_chain('back_cloth', 'left')
        back_cloth_l_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_l[0],
                                                         back_cloth_l[1],
                                                         side='left',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        back_cloth_l_flag = back_cloth_l_component.get_flags()[0]

        back_cloth_r = chain.get_chain('back_cloth', 'right')
        back_cloth_r_component = frag.FKComponent.create(frag_rig,
                                                         back_cloth_r[0],
                                                         back_cloth_r[1],
                                                         side='right',
                                                         region='back_cloth',
                                                         lock_root_translate_axes=[])
        back_cloth_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        back_cloth_r_flag = back_cloth_r_component.get_flags()[0]
        coat_inner_r = chain.get_chain('coat_inner', 'right')
        coat_inner_r_component = frag.FKComponent.create(frag_rig,
                                                         coat_inner_r[0],
                                                         coat_inner_r[1],
                                                         side='right',
                                                         region='coat_inner',
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_inner_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_inner_r_flag = coat_inner_r_component.get_flags()[0]

        coat_inner_l = chain.get_chain('coat_inner', 'left')
        coat_inner_l_component = frag.FKComponent.create(frag_rig,
                                                         coat_inner_l[0],
                                                         coat_inner_l[1],
                                                         side='left',
                                                         region='coat_inner',
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        coat_inner_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_inner_l_flag = coat_inner_l_component.get_flags()[0]

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                   coat_l[0],
                                                   coat_l[1],
                                                   side='left',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                   coat_r[0],
                                                   coat_r[1],
                                                   side='right',
                                                   region='coat',
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_r_component.get_flags()[0]

        coat_middle = chain.get_chain('coat_middle', 'center')
        coat_middle_component = frag.FKComponent.create(frag_rig,
                                                        coat_middle[0],
                                                        coat_middle[1],
                                                        side='center',
                                                        region='coat_middle',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        coat_middle_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_middle_flag = coat_middle_component.get_flags()[0]

        # ------------------------------------------------------------------------------------

        pelvis_cloth = chain.get_chain('pelvis_cloth', 'left')
        pelvis_cloth_component = frag.FKComponent.create(frag_rig,
                                                         pelvis_cloth[0],
                                                         pelvis_cloth[1],
                                                         side='left',
                                                         region='pelvis_cloth',
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        pelvis_cloth_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        pelvis_cloth_flag = pelvis_cloth_component.get_flags()[0]

        sleeve_l = chain.get_chain('sleeve', 'left')
        sleeve_l_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_l[0],
                                                     sleeve_l[1],
                                                     side='left',
                                                     region='sleeve',
                                                     lock_root_translate_axes=[],
                                                     lock_child_translate_axes=[])
        sleeve_l_component.attach_component(arm_l_component, pm.PyNode('lowerarm_l'))
        sleeve_l_flag = sleeve_l_component.get_flags()[0]

        sleeve_r = chain.get_chain('sleeve', 'right')
        sleeve_r_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_r[0],
                                                     sleeve_r[1],
                                                     side='right',
                                                     region='sleeve',
                                                     lock_root_translate_axes=[],
                                                     lock_child_translate_axes=[])
        sleeve_r_component.attach_component(arm_r_component, pm.PyNode('lowerarm_r'))
        sleeve_r_flag = sleeve_r_component.get_flags()[0]

        sleeve_inner_l = chain.get_chain('sleeve_inner', 'left')
        sleeve_inner_l_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_inner_l[0],
                                                     sleeve_inner_l[1],
                                                     side='left',
                                                     region='sleeve_inner',
                                                     lock_root_translate_axes=[],
                                                     lock_child_translate_axes=[])
        sleeve_inner_l_component.attach_component(arm_l_component, pm.PyNode('lowerarm_l'))
        sleeve_inner_l_flag = sleeve_inner_l_component.get_flags()[0]

        sleeve_inner_r = chain.get_chain('sleeve_inner', 'right')
        sleeve_inner_r_component = frag.FKComponent.create(frag_rig,
                                                     sleeve_inner_r[0],
                                                     sleeve_inner_r[1],
                                                     side='right',
                                                     region='sleeve_inner',
                                                     lock_root_translate_axes=[],
                                                     lock_child_translate_axes=[])
        sleeve_inner_r_component.attach_component(arm_r_component, pm.PyNode('lowerarm_r'))
        sleeve_inner_r_flag = sleeve_inner_r_component.get_flags()[0]

        collar_01_l = chain.get_chain('collar_01', 'left')
        collar_01_l_component = frag.FKComponent.create(frag_rig,
                                                        collar_01_l[0],
                                                        collar_01_l[1],
                                                        side='left',
                                                        region='collar_01',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        collar_01_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_01_l_flag = collar_01_l_component.get_flags()[0]

        collar_01_r = chain.get_chain('collar_01', 'right')
        collar_01_r_component = frag.FKComponent.create(frag_rig,
                                                        collar_01_r[0],
                                                        collar_01_r[1],
                                                        side='right',
                                                        region='collar_01',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        collar_01_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_01_r_flag = collar_01_r_component.get_flags()[0]

        collar_02_l = chain.get_chain('collar_02', 'left')
        collar_02_l_component = frag.FKComponent.create(frag_rig,
                                                        collar_02_l[0],
                                                        collar_02_l[1],
                                                        side='left',
                                                        region='collar_02',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        collar_02_l_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_02_l_flag = collar_02_l_component.get_flags()[0]

        collar_02_r = chain.get_chain('collar_02', 'right')
        collar_02_r_component = frag.FKComponent.create(frag_rig,
                                                        collar_02_r[0],
                                                        collar_02_r[1],
                                                        side='right',
                                                        region='collar_02',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        collar_02_r_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_02_r_flag = collar_02_r_component.get_flags()[0]

        collar_back = chain.get_chain('collar_back', 'center')
        collar_back_component = frag.FKComponent.create(frag_rig,
                                                        collar_back[0],
                                                        collar_back[1],
                                                        side='center',
                                                        region='collar_back',
                                                        lock_root_translate_axes=[],
                                                        lock_child_translate_axes=[])
        collar_back_component.attach_component(spine_component, pm.PyNode('spine_04'))
        collar_back_flag = collar_back_component.get_flags()[0]

        ### Multi Constraints ###############

        # Coat Middle
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='coat_middle',
                                    source_object=coat_middle_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='coat',
                                    source_object=coat_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='coat',
                                    source_object=coat_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Inner Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='coat_inner',
                                    source_object=coat_inner_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Coat Inner Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='coat_inner',
                                    source_object=coat_inner_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Back Cloth Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='back_cloth',
                                    source_object=back_cloth_l_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Back Cloth Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='back_cloth',
                                    source_object=back_cloth_r_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # -----------------------------------------------------------------------------------

        # Coat Middle
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='pelvis_cloth',
                                    source_object=pelvis_cloth_flag,
                                    target_list=[pelvis_flag, cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Collar 01 Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='collar_01',
                                    source_object=collar_01_l_flag,
                                    target_list=[spine_flag, neck_start_flag, neck_end_flag,
                                                cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)
        # Collar 01 Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='collar_01',
                                    source_object=collar_01_r_flag,
                                    target_list=[spine_flag, neck_start_flag, neck_end_flag,
                                                 cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Collar 02 Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='collar_01',
                                    source_object=collar_02_l_flag,
                                    target_list=[spine_flag, neck_start_flag, neck_end_flag,
                                                 cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Collar 02 Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='collar_01',
                                    source_object=collar_02_r_flag,
                                    target_list=[spine_flag, neck_start_flag, neck_end_flag,
                                                 cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Collar Back
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='collar_back',
                                    source_object=collar_back_flag,
                                    target_list=[spine_flag, neck_start_flag, neck_end_flag,
                                                 cog_flag, offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Sleeve 01 Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='sleeve',
                                    source_object=sleeve_l_flag,
                                    target_list=[pm.PyNode('lowerarm_l'), pm.PyNode('hand_l'), offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Sleeve 01 Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='sleeve',
                                    source_object=sleeve_r_flag,
                                    target_list=[pm.PyNode('lowerarm_r'), pm.PyNode('hand_r'), offset_flag],
                                    switch_obj=None,
                                    translate=True)

        # Sleeve Inner Left
        frag.MultiConstraint.create(frag_rig,
                                    side='left',
                                    region='sleeve_inner',
                                    source_object=sleeve_inner_l_flag,
                                    target_list=[pm.PyNode('lowerarm_l'), pm.PyNode('hand_l'),
                                                 offset_flag, sleeve_l_flag],
                                    switch_obj=None,
                                    translate=True)

        # Sleeve Inner Right
        frag.MultiConstraint.create(frag_rig,
                                    side='right',
                                    region='sleeve_inner',
                                    source_object=sleeve_inner_r_flag,
                                    target_list=[pm.PyNode('lowerarm_r'), pm.PyNode('hand_r'),
                                                 offset_flag, sleeve_r_flag],
                                    switch_obj=None,
                                    translate=True)


        frag_rig.rigTemplate.set(AngeloTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())


class HagTemplate(PlayerMaleTemplate):
    VERSION = 1
    ASSET_ID = 'gigt-g93k5-08zwq-8nf2'

    def __init__(self, asset_id=ASSET_ID):
        super(HagTemplate, self).__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self):

        pm.namespace(set=':')
        frag_rig = super(HagTemplate, self).build(finalize=False)
        root = pm.PyNode('root')
        chain = chain_markup.ChainMarkup(root)

        pelvis_component = frag_rig.get_frag_children(of_type=frag.PelvisComponent)[0]

        frag_root = frag_rig.get_frag_parent()
        skel_root = frag_root.root_joint
        skel_hierarchy = chain_markup.ChainMarkup(skel_root)

        head_component = lists.get_first_in_list(frag_rig.get_frag_children(side='center', region='neck'))
        head_joint = skel_hierarchy.get_end('neck', 'center')

        jaw_joint = skel_hierarchy.get_start('jaw', 'center')
        jaw_component = frag.FKComponent.create(frag_rig,
                                                jaw_joint,
                                                jaw_joint,
                                                side='center',
                                                region='jaw',
                                                scale=0.1)
        jaw_component.attach_component(head_component, head_joint)

        coat_l = chain.get_chain('coat', 'left')
        coat_l_component = frag.FKComponent.create(frag_rig,
                                                   coat_l[0],
                                                   coat_l[1],
                                                   side='left',
                                                   region='coat',
                                                   scale=0.1,
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_l_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_l_flag = coat_l_component.get_flags()[0]

        coat_r = chain.get_chain('coat', 'right')
        coat_r_component = frag.FKComponent.create(frag_rig,
                                                   coat_r[0],
                                                   coat_r[1],
                                                   side='right',
                                                   region='coat',
                                                   scale=0.1,
                                                   lock_root_translate_axes=[],
                                                   lock_child_translate_axes=[])
        coat_r_component.attach_component(pelvis_component, pm.PyNode('pelvis'))
        coat_r_flag = coat_l_component.get_flags()[0]

        frag_rig.rigTemplate.set(HagTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())