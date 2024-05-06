#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm

from mca.mya.rigging import frag, chain_markup
from mca.mya.rigging.templates import rig_templates


class Lumpy(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'lumpy'

    def __init__(self, asset_id=ASSET_ID):
        super(Lumpy, self).__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self, asset_type='combatant'):

        pm.namespace(set=':')
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        flags_all = frag_rig.flagsAll.get()

        # world
        start_joint = pm.PyNode('root')
        world_component = frag.WorldComponent.create(frag_rig,
                                                            start_joint,
                                                            'center',
                                                            'world',
                                                            orientation=[-90, 0, 0])
        root_flag = world_component.root_flag
        world_flag = world_component.world_flag
        offset_flag = world_component.offset_flag

        chain = chain_markup.ChainMarkup(start_joint)

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag],
                                          switch_attr='follow')

        # Cog
        start_joint = pm.PyNode('pelvis')
        end_joint = pm.PyNode('pelvis')
        cog_component = frag.CogComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        'center',
                                                        'cog',
                                                        orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode('root'))
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

        start_joint = pm.PyNode('loincloth')
        end_joint = pm.PyNode('loincloth')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='center',
                                                         region='loincloth',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        # Spine
        start_joint = pm.PyNode('spine_01')
        end_joint = pm.PyNode('spine_04')
        spine_component = frag.RFKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            'center',
                                                            'spine')
        spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
        spine_flags = spine_component.get_flags()
        spine_sub_flags = spine_component.sub_flags

        start_joint = pm.PyNode('belly_l')
        end_joint = pm.PyNode('belly_l')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='belly',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(spine_component, pm.PyNode('spine_01'))

        start_joint = pm.PyNode('belly_r')
        end_joint = pm.PyNode('belly_r')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='right',
                                                         region='belly',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(pelvis_component, pm.PyNode('spine_01'))

        # Neck
        start_joint = pm.PyNode('neck_01')
        end_joint = pm.PyNode('head')
        neck_component = frag.RFKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        'center',
                                                        'neck',
                                                        False)
        neck_component.attach_component(spine_component, pm.PyNode('spine_04'))
        neck_flags = neck_component.get_flags()
        head_flag = neck_component.end_flag
        neck_flag = neck_component.start_flag
        neck_flag.set_as_sub()
        for neck_mid_flag in neck_component.mid_flags:
            neck_mid_flag.set_as_detail()

        start_joint = pm.PyNode('jaw')
        end_joint = pm.PyNode('jaw')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='center',
                                                         region='jaw',
                                                         lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
        finger_component.attach_component(neck_component, pm.PyNode('head'))

        start_joint = pm.PyNode('hair_01_l')
        end_joint = pm.PyNode('hair_04_l')
        l_hair = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='hair')
        l_hair.attach_component(neck_component, pm.PyNode('head'))

        start_joint = pm.PyNode('hair_01_front_r')
        end_joint = pm.PyNode('hair_05_front_r')
        r_front_hair = frag.FKComponent.create(frag_rig,
                                               start_joint,
                                               end_joint,
                                               side='right',
                                               region='front_hair')
        r_front_hair.attach_component(neck_component, pm.PyNode('head'))

        start_joint = pm.PyNode('hair_01_back_r')
        end_joint = pm.PyNode('hair_06_back_r')
        r_back_hair = frag.FKComponent.create(frag_rig,
                                               start_joint,
                                               end_joint,
                                               side='right',
                                               region='back_hair')
        r_back_hair.attach_component(neck_component, pm.PyNode('head'))

        # Left Clavicle
        start_joint = pm.PyNode('clavicle_l')
        end_joint = pm.PyNode('clavicle_l')
        l_clav_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='clav',
                                                            lock_root_translate_axes=['v'])
        l_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        l_clav_flag = l_clav_component.get_flags()[0]

        # Right Clavicle
        start_joint = pm.PyNode('clavicle_r')
        end_joint = pm.PyNode('clavicle_r')
        r_clav_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='clav',
                                                            lock_root_translate_axes=['v'])
        r_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        r_clav_flag = r_clav_component.get_flags()[0]

        # IKFK Right arm
        start_joint = pm.PyNode('upperarm_r')
        end_joint = pm.PyNode('hand_r')
        r_arm_component = frag.IKFKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='arm',
                                                            ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
        r_arm_flags = r_arm_component.get_flags()
        r_arm_ik_flag = r_arm_component.ik_flag
        r_arm_switch_flag = r_arm_component.switch_flag
        r_arm_fk_flag = r_arm_component.fk_flags

        # IKFK Left arm
        start_joint = pm.PyNode('upperarm_l')
        end_joint = pm.PyNode('hand_l')
        l_arm_component = frag.IKFKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='arm',
                                                            ik_flag_pv_orient=[-90, 0, 0])
        l_arm_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        l_arm_flags = l_arm_component.get_flags()
        l_arm_ik_flag = l_arm_component.ik_flag
        l_arm_switch_flag = l_arm_component.switch_flag
        l_arm_fk_flag = l_arm_component.fk_flags

        # Left Hand weapon
        l_weapon = pm.PyNode('weapon_l')
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
        r_weapon = pm.PyNode('weapon_r')
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

        # Left Back Clavicle
        start_joint = pm.PyNode('back_clavicle_l')
        end_joint = pm.PyNode('back_clavicle_l')
        l_back_clav_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='back_clav',
                                                            lock_root_translate_axes=['v'])
        l_back_clav_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        l_back_clav_flag = l_back_clav_component.get_flags()[0]

        # IKFK Back Left arm
        start_joint = pm.PyNode('back_upperarm_l')
        end_joint = pm.PyNode('back_hand_l')
        l_back_arm_component = frag.IKFKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='back_arm',
                                                            ik_flag_pv_orient=[-90, 0, 0])
        l_back_arm_component.attach_component(l_back_clav_component, pm.PyNode('back_clavicle_l'))
        l_back_arm_flags = l_back_arm_component.get_flags()
        l_back_arm_ik_flag = l_back_arm_component.ik_flag
        l_back_arm_switch_flag = l_back_arm_component.switch_flag
        l_back_arm_fk_flag = l_back_arm_component.fk_flags

        # Fingers
        for joint_name in ['back_hand_thumb_l', 'back_hand_ring_l', 'back_hand_middle_l', 'back_hand_index_l']:
            start_joint = pm.PyNode(joint_name)
            end_joint = pm.PyNode(joint_name)
            region = joint_name.split('_')
            region = f'{region[0]}_{region[2]}'
            finger_component = frag.FKComponent.create(frag_rig,
                                                                  start_joint,
                                                                  end_joint,
                                                                  side='left',
                                                                  region=region,
                                                                  lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
            finger_component.attach_component(l_back_arm_component, pm.PyNode('back_hand_l'))

        # Center Back Clavicle
        start_joint = pm.PyNode('back_clavicle_c')
        end_joint = pm.PyNode('back_clavicle_c')
        c_back_clav_component = frag.FKComponent.create(frag_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='center',
                                                                region='back_clav',
                                                                lock_root_translate_axes=['v'])
        c_back_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        c_back_clav_flag = c_back_clav_component.get_flags()[0]

        # IKFK Center Left arm
        start_joint = pm.PyNode('back_upperarm_c')
        end_joint = pm.PyNode('back_hand_c')
        c_back_arm_component = frag.IKFKComponent.create(frag_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='center',
                                                                region='back_arm',
                                                                ik_flag_pv_orient=[-90, 0, 0])
        c_back_arm_component.attach_component(c_back_clav_component, pm.PyNode('back_clavicle_c'))
        c_back_arm_flags = c_back_arm_component.get_flags()
        c_back_arm_ik_flag = c_back_arm_component.ik_flag
        c_back_arm_switch_flag = c_back_arm_component.switch_flag
        c_back_arm_fk_flag = c_back_arm_component.fk_flags

        # Fingers
        for joint_name in ['back_hand_thumb_c', 'back_hand_ring_c', 'back_hand_middle_c', 'back_hand_index_c']:
            start_joint = pm.PyNode(joint_name)
            end_joint = pm.PyNode(joint_name)
            region = joint_name.split('_')
            region = f'{region[0]}_{region[2]}'
            finger_component = frag.FKComponent.create(frag_rig,
                                                             start_joint,
                                                             end_joint,
                                                             side='center',
                                                             region=region,
                                                             lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
            finger_component.attach_component(c_back_arm_component, pm.PyNode('back_hand_c'))

        # Right Back Clavicle
        start_joint = pm.PyNode('back_clavicle_r')
        end_joint = pm.PyNode('back_clavicle_r')
        r_back_clav_component = frag.FKComponent.create(frag_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='right',
                                                                region='back_clav',
                                                                lock_root_translate_axes=['v'])
        r_back_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        r_back_clav_flag = r_back_clav_component.get_flags()[0]

        # IKFK Right Left arm
        start_joint = pm.PyNode('back_upperarm_r')
        end_joint = pm.PyNode('back_hand_r')
        r_back_arm_component = frag.IKFKComponent.create(frag_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='right',
                                                                region='back_arm',
                                                                ik_flag_pv_orient=[-90, 0, 0])
        r_back_arm_component.attach_component(r_back_clav_component, pm.PyNode('back_clavicle_r'))
        r_back_arm_flags = r_back_arm_component.get_flags()
        r_back_arm_ik_flag = r_back_arm_component.ik_flag
        r_back_arm_switch_flag = r_back_arm_component.switch_flag
        r_back_arm_fk_flag = r_back_arm_component.fk_flags

        # Fingers
        for joint_name in ['back_hand_thumb_r', 'back_hand_ring_r', 'back_hand_middle_r', 'back_hand_index_r']:
            start_joint = pm.PyNode(joint_name)
            end_joint = pm.PyNode(joint_name)
            region = joint_name.split('_')
            region = f'{region[0]}_{region[2]}'
            finger_component = frag.FKComponent.create(frag_rig,
                                                             start_joint,
                                                             end_joint,
                                                             side='right',
                                                             region=region,
                                                             lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
            finger_component.attach_component(r_back_arm_component, pm.PyNode('back_hand_r'))

        # Left Hand prop
        start_joint = pm.PyNode('hand_contact_l')
        end_joint = pm.PyNode('hand_contact_l')
        l_prop_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='hand_prop',
                                                            scale=0.1,
                                                            lock_root_translate_axes=[])
        l_prop_component.attach_component(l_arm_component, pm.PyNode('hand_l'))
        l_prop_flag = l_prop_component.get_flags()[0]
        l_prop_flag.set_as_sub()

        # Right Hand prop
        start_joint = pm.PyNode('hand_contact_r')
        end_joint = pm.PyNode('hand_contact_r')
        r_prop_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='hand_prop',
                                                            scale=0.1,
                                                            lock_root_translate_axes=[])
        r_prop_component.attach_component(r_arm_component, pm.PyNode('hand_r'))
        r_prop_flag = r_prop_component.get_flags()[0]
        r_prop_flag.set_as_sub()

        # IKFK Left leg
        start_joint = pm.PyNode('thigh_l')
        end_joint = pm.PyNode('ball_l')
        l_leg_component = frag.ReverseFootComponent.create(frag_rig,
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
        start_joint = pm.PyNode('thigh_r')
        end_joint = pm.PyNode('ball_r')
        r_leg_component = frag.ReverseFootComponent.create(frag_rig,
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

        ####  Left Fingers #######
        # left Index Finger
        start_joint = pm.PyNode('index_metacarpal_l')
        end_joint = pm.PyNode('index_03_l')
        l_index_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='index_finger',
                                                            scale=0.1)
        l_index_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left middle Finger
        start_joint = pm.PyNode('middle_metacarpal_l')
        end_joint = pm.PyNode('middle_03_l')
        l_middle_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='middle_finger',
                                                            scale=0.1)
        l_middle_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left ring Finger
        start_joint = pm.PyNode('ring_metacarpal_l')
        end_joint = pm.PyNode('ring_03_l')
        l_ring_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='ring_finger',
                                                            scale=0.1)
        l_ring_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Pinky Finger
        start_joint = pm.PyNode('pinky_metacarpal_l')
        end_joint = pm.PyNode('pinky_03_l')
        l_pinky_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='pinky_finger',
                                                            scale=0.1)
        l_pinky_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Thumb Finger
        start_joint = pm.PyNode('thumb_01_l')
        end_joint = pm.PyNode('thumb_03_l')
        l_thumb_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='thumb_finger',
                                                            scale=0.1)
        l_thumb_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Extra Finger 01
        start_joint = pm.PyNode('hexadactyl_metacarpal_l')
        end_joint = pm.PyNode('hexadactyl_03_l')
        l_ext_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='ext_01_finger',
                                                            scale=0.1)
        l_ext_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Extra Finger 02
        start_joint = pm.PyNode('eptadactyl_metacarpal_l')
        end_joint = pm.PyNode('eptadactyl_03_l')
        l_ext_component = frag.FKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='left',
                                                        region='ext_02_finger',
                                                        scale=0.1)
        l_ext_component.attach_component(l_arm_component, pm.PyNode('hand_l'))


        ####  Right Fingers #######
        # Right Index Finger
        start_joint = pm.PyNode('index_metacarpal_r')
        end_joint = pm.PyNode('index_03_r')
        r_index_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='index_finger',
                                                            scale=0.1)
        r_index_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right ring Finger
        start_joint = pm.PyNode('ring_metacarpal_r')
        end_joint = pm.PyNode('ring_03_r')
        r_ring_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='ring_finger',
                                                            scale=0.1)
        r_ring_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right Pinky Finger
        start_joint = pm.PyNode('pinky_metacarpal_r')
        end_joint = pm.PyNode('pinky_03_r')
        r_pinky_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='pinky_finger',
                                                            scale=0.1)
        r_pinky_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right Thumb Finger
        start_joint = pm.PyNode('thumb_01_r')
        end_joint = pm.PyNode('thumb_03_r')
        r_thumb_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='thumb_finger',
                                                            scale=0.1)
        r_thumb_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

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
        # Left IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='arm',
                                            source_object=l_arm_ik_flag,
                                            target_list=[world_flag,
                                                        l_clav_flag,
                                                        r_arm_ik_flag,
                                                        cog_flag,
                                                        spine_sub_flags[1]],
                                            switch_obj=l_arm_switch_flag,
                                            switch_attr='follow')
        # Right IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                            side='right',
                                            region='arm',
                                            source_object=r_arm_ik_flag,
                                            target_list=[world_flag,
                                                            r_clav_flag,
                                                            l_arm_ik_flag,
                                                            cog_flag,
                                                            spine_sub_flags[1]],
                                            switch_obj=r_arm_switch_flag)

        # Left FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='fk_arm',
                                            source_object=l_arm_fk_flag[0],
                                            target_list=[l_clav_flag,
                                                        spine_sub_flags[1],
                                                        world_flag,
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
                                                            world_flag,
                                                            cog_flag],
                                            t=False,
                                            switch_attr='rotateFollow')

        # Center Cog Multi
        frag.MultiConstraint.create(frag_rig,
                                            side='center',
                                            region='cog',
                                            source_object=cog_flag,
                                            target_list=[world_flag, flags_all],
                                            switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                            side='center',
                                            region='head',
                                            source_object=head_flag,
                                            target_list=[world_flag,
                                                            neck_flag,
                                                            neck_mid_flag,
                                                            cog_flag,
                                                            flags_all],
                                            switch_obj=None,
                                            translate=False,
                                            switch_attr='rotateFollow')
        # PV Left Arm
        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='arm_pv',
                                            source_object=l_arm_component.pv_flag,
                                            target_list=[world_flag,
                                                            l_clav_flag,
                                                            spine_sub_flags[1],
                                                            cog_flag,
                                                            flags_all],
                                            switch_obj=None)
        # PV Right Arm
        frag.MultiConstraint.create(frag_rig,
                                            side='right',
                                            region='arm_pv',
                                            source_object=r_arm_component.pv_flag,
                                            target_list=[world_flag,
                                                        r_clav_flag,
                                                        spine_sub_flags[1],
                                                        cog_flag,
                                                        flags_all],
                                            switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                            side='right',
                                            region='foot',
                                            source_object=r_leg_ik_flag,
                                            target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
                                            switch_obj=r_leg_switch_flag)

        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='foot',
                                            source_object=l_leg_ik_flag,
                                            target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
                                            switch_obj=l_leg_switch_flag)

        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='leg_pv',
                                            source_object=l_leg_component.pv_flag,
                                            target_list=[world_flag, l_leg_ik_flag, cog_flag, flags_all],
                                            switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                            side='right',
                                            region='leg_pv',
                                            source_object=r_leg_component.pv_flag,
                                            target_list=[world_flag, r_leg_ik_flag, cog_flag, flags_all],
                                            switch_obj=None)

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

        frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='hand_prop',
                                            source_object=l_prop_flag,
                                            target_list=[pm.PyNode('hand_l'), r_prop_flag, world_flag, flags_all],
                                            switch_obj=None,
                                            default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                            side='right',
                                            region='hand_prop',
                                            source_object=r_prop_flag,
                                            target_list=[pm.PyNode('hand_r'), l_prop_flag, world_flag, flags_all],
                                            switch_obj=None,
                                            default_name='default')
        frag_rig.rigTemplate.set(Lumpy.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class AcidLumpy(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'acidlumpy'

    def __init__(self, asset_id=ASSET_ID):
        super(AcidLumpy, self).__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self, asset_type='combatant'):

        pm.namespace(set=':')
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        flags_all = frag_rig.flagsAll.get()

        # world
        start_joint = pm.PyNode('root')
        world_component = frag.WorldComponent.create(frag_rig,
                                                           start_joint,
                                                           'center',
                                                           'world',
                                                           orientation=[-90, 0, 0])
        root_flag = world_component.root_flag
        world_flag = world_component.world_flag
        offset_flag = world_component.offset_flag

        chain = chain_markup.ChainMarkup(start_joint)

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag],
                                          switch_attr='follow')

        # Cog
        start_joint = pm.PyNode('pelvis')
        end_joint = pm.PyNode('pelvis')
        cog_component = frag.CogComponent.create(frag_rig,
                                                       start_joint,
                                                       end_joint,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode('root'))
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

        start_joint = pm.PyNode('loincloth')
        end_joint = pm.PyNode('loincloth')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='center',
                                                         region='loincloth',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(pelvis_component, pm.PyNode('pelvis'))

        # Spine
        start_joint = pm.PyNode('spine_01')
        end_joint = pm.PyNode('spine_04')
        spine_component = frag.RFKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         'center',
                                                         'spine')
        spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
        spine_flags = spine_component.get_flags()
        spine_sub_flags = spine_component.sub_flags

        start_joint = pm.PyNode('belly_l')
        end_joint = pm.PyNode('belly_l')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='belly',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(spine_component, pm.PyNode('spine_01'))

        start_joint = pm.PyNode('belly_r')
        end_joint = pm.PyNode('belly_r')
        finger_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='right',
                                                         region='belly',
                                                         lock_root_translate_axes=['v'])
        finger_component.attach_component(pelvis_component, pm.PyNode('spine_01'))

        # Neck
        start_joint = pm.PyNode('neck_01')
        end_joint = pm.PyNode('head')
        neck_component = frag.RFKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        'center',
                                                        'neck',
                                                        False)
        neck_component.attach_component(spine_component, pm.PyNode('spine_04'))
        neck_flags = neck_component.get_flags()
        head_flag = neck_component.end_flag
        neck_flag = neck_component.start_flag
        neck_flag.set_as_sub()
        for neck_mid_flag in neck_component.mid_flags:
            neck_mid_flag.set_as_detail()

        for side, tag in [('left', 'l'), ('right', 'r')]:
            jaw_joint = pm.PyNode(f'jaw_{tag}')
            jaw_component = frag.FKComponent.create(frag_rig,
                                                             jaw_joint,
                                                             jaw_joint,
                                                             side=side,
                                                             region='jaw',
                                                             lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
            jaw_component.attach_component(neck_component, pm.PyNode('head'))
            for pos in ['top', 'mid', 'bot']:
                sub_jaw_joint = pm.PyNode(f'jaw_stretch_{pos}_{tag}')
                sub_jaw = frag.FKComponent.create(frag_rig,
                                                        sub_jaw_joint,
                                                        sub_jaw_joint,
                                                        side=side,
                                                        region=f'jaw_stretch_{pos}',
                                                        lock_root_translate_axes=['v'])
                sub_jaw.attach_component(sub_jaw, jaw_joint)

            for pos in ['', 'inner']:
                joint_name = f'mouth_{pos}_{tag}' if pos else f'mouth_{tag}'
                mouth_joint = pm.PyNode(joint_name)
                mouth_component = frag.FKComponent.create(frag_rig,
                                                                mouth_joint,
                                                                mouth_joint,
                                                                side=side,
                                                                region=joint_name[:-2],
                                                                lock_root_translate_axes=['v'])
                mouth_component.attach_component(neck_component, pm.PyNode('head'))


        start_joint = pm.PyNode('jaw_c')
        end_joint = pm.PyNode('jaw_c')
        jaw_component = frag.FKComponent.create(frag_rig,
                                                      start_joint,
                                                      end_joint,
                                                      side='center',
                                                      region='jaw',
                                                      lock_root_translate_axes=['v', 'tx', 'ty', 'tz'])
        jaw_component.attach_component(neck_component, pm.PyNode('head'))

        # Left Clavicle
        start_joint = pm.PyNode('clavicle_l')
        end_joint = pm.PyNode('clavicle_l')
        l_clav_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        l_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        l_clav_flag = l_clav_component.get_flags()[0]

        # Right Clavicle
        start_joint = pm.PyNode('clavicle_r')
        end_joint = pm.PyNode('clavicle_r')
        r_clav_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='right',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        r_clav_component.attach_component(spine_component, pm.PyNode('spine_04'))
        r_clav_flag = r_clav_component.get_flags()[0]

        # IKFK Right arm
        start_joint = pm.PyNode('upperarm_r')
        end_joint = pm.PyNode('hand_r')
        r_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='right',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, pm.PyNode('clavicle_r'))
        r_arm_flags = r_arm_component.get_flags()
        r_arm_ik_flag = r_arm_component.ik_flag
        r_arm_switch_flag = r_arm_component.switch_flag
        r_arm_fk_flag = r_arm_component.fk_flags

        # IKFK Left arm
        start_joint = pm.PyNode('upperarm_l')
        end_joint = pm.PyNode('hand_l')
        l_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='left',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        l_arm_component.attach_component(l_clav_component, pm.PyNode('clavicle_l'))
        l_arm_flags = l_arm_component.get_flags()
        l_arm_ik_flag = l_arm_component.ik_flag
        l_arm_switch_flag = l_arm_component.switch_flag
        l_arm_fk_flag = l_arm_component.fk_flags

        # Left Hand weapon
        l_weapon = pm.PyNode('weapon_l')
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
        r_weapon = pm.PyNode('weapon_r')
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

        # Left Hand prop
        start_joint = pm.PyNode('hand_contact_l')
        end_joint = pm.PyNode('hand_contact_l')
        l_prop_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='hand_prop',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        l_prop_component.attach_component(l_arm_component, pm.PyNode('hand_l'))
        l_prop_flag = l_prop_component.get_flags()[0]
        l_prop_flag.set_as_sub()

        # Right Hand prop
        start_joint = pm.PyNode('hand_contact_r')
        end_joint = pm.PyNode('hand_contact_r')
        r_prop_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='right',
                                                         region='hand_prop',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        r_prop_component.attach_component(r_arm_component, pm.PyNode('hand_r'))
        r_prop_flag = r_prop_component.get_flags()[0]
        r_prop_flag.set_as_sub()

        # IKFK Left leg
        start_joint = pm.PyNode('thigh_l')
        end_joint = pm.PyNode('ball_l')
        l_leg_component = frag.ReverseFootComponent.create(frag_rig,
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
        start_joint = pm.PyNode('thigh_r')
        end_joint = pm.PyNode('ball_r')
        r_leg_component = frag.ReverseFootComponent.create(frag_rig,
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

        ####  Left Fingers #######
        # left Index Finger
        start_joint = pm.PyNode('index_metacarpal_l')
        end_joint = pm.PyNode('index_03_l')
        l_index_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='left',
                                                          region='index_finger',
                                                          scale=0.1)
        l_index_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left middle Finger
        start_joint = pm.PyNode('middle_metacarpal_l')
        end_joint = pm.PyNode('middle_03_l')
        l_middle_component = frag.FKComponent.create(frag_rig,
                                                           start_joint,
                                                           end_joint,
                                                           side='left',
                                                           region='middle_finger',
                                                           scale=0.1)
        l_middle_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left ring Finger
        start_joint = pm.PyNode('ring_metacarpal_l')
        end_joint = pm.PyNode('ring_03_l')
        l_ring_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='left',
                                                         region='ring_finger',
                                                         scale=0.1)
        l_ring_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Pinky Finger
        start_joint = pm.PyNode('pinky_metacarpal_l')
        end_joint = pm.PyNode('pinky_03_l')
        l_pinky_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='left',
                                                          region='pinky_finger',
                                                          scale=0.1)
        l_pinky_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Thumb Finger
        start_joint = pm.PyNode('thumb_01_l')
        end_joint = pm.PyNode('thumb_03_l')
        l_thumb_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='left',
                                                          region='thumb_finger',
                                                          scale=0.1)
        l_thumb_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Extra Finger 01
        start_joint = pm.PyNode('hexadactyl_metacarpal_l')
        end_joint = pm.PyNode('hexadactyl_03_l')
        l_ext_component = frag.FKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='left',
                                                        region='ext_01_finger',
                                                        scale=0.1)
        l_ext_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        # left Extra Finger 02
        start_joint = pm.PyNode('eptadactyl_metacarpal_l')
        end_joint = pm.PyNode('eptadactyl_03_l')
        l_ext_component = frag.FKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='left',
                                                        region='ext_02_finger',
                                                        scale=0.1)
        l_ext_component.attach_component(l_arm_component, pm.PyNode('hand_l'))

        ####  Right Fingers #######
        # Right Index Finger
        start_joint = pm.PyNode('index_metacarpal_r')
        end_joint = pm.PyNode('index_03_r')
        r_index_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='right',
                                                          region='index_finger',
                                                          scale=0.1)
        r_index_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right ring Finger
        start_joint = pm.PyNode('ring_metacarpal_r')
        end_joint = pm.PyNode('ring_03_r')
        r_ring_component = frag.FKComponent.create(frag_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='right',
                                                         region='ring_finger',
                                                         scale=0.1)
        r_ring_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right Pinky Finger
        start_joint = pm.PyNode('pinky_metacarpal_r')
        end_joint = pm.PyNode('pinky_03_r')
        r_pinky_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='right',
                                                          region='pinky_finger',
                                                          scale=0.1)
        r_pinky_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

        # Right Thumb Finger
        start_joint = pm.PyNode('thumb_01_r')
        end_joint = pm.PyNode('thumb_03_r')
        r_thumb_component = frag.FKComponent.create(frag_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='right',
                                                          region='thumb_finger',
                                                          scale=0.1)
        r_thumb_component.attach_component(r_arm_component, pm.PyNode('hand_r'))

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
        # Left IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='arm',
                                          source_object=l_arm_ik_flag,
                                          target_list=[world_flag,
                                                       l_clav_flag,
                                                       r_arm_ik_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=l_arm_switch_flag,
                                          switch_attr='follow')
        # Right IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='arm',
                                          source_object=r_arm_ik_flag,
                                          target_list=[world_flag,
                                                       r_clav_flag,
                                                       l_arm_ik_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=r_arm_switch_flag)

        # Left FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='fk_arm',
                                          source_object=l_arm_fk_flag[0],
                                          target_list=[l_clav_flag,
                                                       spine_sub_flags[1],
                                                       world_flag,
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
                                                       world_flag,
                                                       cog_flag],
                                          t=False,
                                          switch_attr='rotateFollow')

        # Center Cog Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='cog',
                                          source_object=cog_flag,
                                          target_list=[world_flag, flags_all],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='head',
                                          source_object=head_flag,
                                          target_list=[world_flag,
                                                       neck_flag,
                                                       neck_mid_flag,
                                                       cog_flag,
                                                       flags_all],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow')
        # PV Left Arm
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='arm_pv',
                                          source_object=l_arm_component.pv_flag,
                                          target_list=[world_flag,
                                                       l_clav_flag,
                                                       spine_sub_flags[1],
                                                       cog_flag,
                                                       flags_all],
                                          switch_obj=None)
        # PV Right Arm
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='arm_pv',
                                          source_object=r_arm_component.pv_flag,
                                          target_list=[world_flag,
                                                       r_clav_flag,
                                                       spine_sub_flags[1],
                                                       cog_flag,
                                                       flags_all],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_ik_flag,
                                          target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
                                          switch_obj=r_leg_switch_flag)

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
                                          source_object=l_leg_ik_flag,
                                          target_list=[world_flag, pelvis_flag, cog_flag, flags_all],
                                          switch_obj=l_leg_switch_flag)

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='leg_pv',
                                          source_object=l_leg_component.pv_flag,
                                          target_list=[world_flag, l_leg_ik_flag, cog_flag, flags_all],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='leg_pv',
                                          source_object=r_leg_component.pv_flag,
                                          target_list=[world_flag, r_leg_ik_flag, cog_flag, flags_all],
                                          switch_obj=None)

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

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_prop',
                                          source_object=l_prop_flag,
                                          target_list=[pm.PyNode('hand_l'), r_prop_flag, world_flag, flags_all],
                                          switch_obj=None,
                                          default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_prop',
                                          source_object=r_prop_flag,
                                          target_list=[pm.PyNode('hand_r'), l_prop_flag, world_flag, flags_all],
                                          switch_obj=None,
                                          default_name='default')
        frag_rig.rigTemplate.set(Lumpy.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig
