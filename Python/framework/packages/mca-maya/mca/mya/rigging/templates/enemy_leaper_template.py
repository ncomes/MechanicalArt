
#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports
from __future__ import print_function, division, absolute_import
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists

from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup

from mca.mya.utils import attr_utils


class LeaperTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'leaper'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(LeaperTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):
        # pm.newFile(f=True)

        pm.namespace(set=':')
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, self.asset_type, self.asset_id)
        frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        root = frag_root.root_joint
        flags_all = frag_rig.flagsAll.get()
        do_not_touch = frag_rig.do_not_touch
        chain = chain_markup.ChainMarkup(root)

        # world
        world_component = frag.WorldComponent.create(frag_rig,
                                                           root,
                                                           'center',
                                                           'world',
                                                           orientation=[-90, 0, 0])
        world_flag = world_component.get_flags()[0]
        offset_flag = world_component.offset_flag
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()
        pm.group(pm.PyNode('f_root_align_transform'), n='flags_center_root')
        pm.parent(pm.PyNode('flags_center_root'), pm.PyNode('flags_all'))

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
        spine_start = chain.get_start('spine', 'center')
        pelvis_component = frag.PelvisComponent.create(frag_rig,
                                                             pelvis_joint,
                                                             spine_start,
                                                             'center',
                                                             'pelvis',
                                                             orientation=[-90, 0, 0])
        pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
        pelvis_flag = pelvis_component.get_flags()[0]

        # Spine
        spine_chain = chain.get_chain('spine', 'center')
        spine_end = chain.get_end('spine', 'center')
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
        neck_component = frag.FKComponent.create(frag_rig,
                                                       neck_chain[0],
                                                       neck_chain[1],
                                                       side='left',
                                                       region='neck',
                                                       lock_root_translate_axes=['v'],
                                                       lock_child_translate_axes=('v'))
        neck_component.attach_component(spine_component, spine_end)
        neck_flags = neck_component.get_flags()
        neck_flags[1].set_as_sub()
        head_flag = neck_component.get_flags()[-1]

        # Left Clavicle
        l_clav_chain = chain.get_start('clav', 'left')
        l_clav_component = frag.FKComponent.create(frag_rig,
                                                         l_clav_chain,
                                                         l_clav_chain,
                                                         side='left',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        l_clav_component.attach_component(spine_component, spine_end)
        l_clav_flag = l_clav_component.get_flags()[0]

        # Right Clavicle
        r_clav_chain = chain.get_start('clav', 'right')
        r_clav_component = frag.FKComponent.create(frag_rig,
                                                         r_clav_chain,
                                                         r_clav_chain,
                                                         side='right',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        r_clav_component.attach_component(spine_component, spine_end)
        r_clav_flag = r_clav_component.get_flags()[0]

        # Left Clavicle Spike
        l_spike_clav_chain = chain.get_start('spike_clav', 'left')
        l_clav_spike_component = frag.FKComponent.create(frag_rig,
                                                               l_spike_clav_chain,
                                                               l_spike_clav_chain,
                                                               side='left',
                                                               region='clav_spike',
                                                               lock_root_translate_axes=['v'])
        l_clav_spike_component.attach_component(spine_component, spine_end)
        l_clav_spike_flag = l_clav_spike_component.get_flags()[0]

        # Right Clavicle Spike
        r_spike_clav_chain = chain.get_start('spike_clav', 'right')
        r_clav_spike_component = frag.FKComponent.create(frag_rig,
                                                               r_spike_clav_chain,
                                                               r_spike_clav_chain,
                                                               side='right',
                                                               region='clav_spike',
                                                               lock_root_translate_axes=['v'])
        r_clav_spike_component.attach_component(spine_component, spine_end)
        r_clav_spike_flag = r_clav_spike_component.get_flags()[0]

        # IKFK Right arm
        r_arm_chain = chain.get_chain('arm', 'right')
        r_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          r_arm_chain[0],
                                                          r_arm_chain[1],
                                                          side='right',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, r_clav_chain)
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
        l_arm_component.attach_component(l_clav_component, l_clav_chain)
        l_arm_flags = l_arm_component.get_flags()
        l_arm_ik_flag = l_arm_component.ik_flag
        l_arm_switch_flag = l_arm_component.switch_flag
        l_arm_fk_flag = l_arm_component.fk_flags

        # Spike IKFK Right arm
        r_spike_arm_chain = chain.get_chain('spike_arm', 'right')
        r_arm_spike_component = frag.IKFKComponent.create(frag_rig,
                                                                r_spike_arm_chain[0],
                                                                r_spike_arm_chain[1],
                                                                side='right',
                                                                region='arm_spike',
                                                                ik_flag_pv_orient=[-90, 0, 0])
        r_arm_spike_component.attach_component(r_clav_spike_component, r_spike_clav_chain)
        r_arm_spike_ik_flag = r_arm_spike_component.ik_flag
        r_arm_spike_switch_flag = r_arm_spike_component.switch_flag

        # Spike IKFK Left arm
        l_spike_arm_chain = chain.get_chain('spike_arm', 'left')
        l_arm_spike_component = frag.IKFKComponent.create(frag_rig,
                                                                l_spike_arm_chain[0],
                                                                l_spike_arm_chain[1],
                                                                side='left',
                                                                region='arm_spike',
                                                                ik_flag_pv_orient=[-90, 0, 0])
        l_arm_spike_component.attach_component(l_clav_spike_component, l_spike_clav_chain)
        l_arm_spike_ik_flag = l_arm_spike_component.ik_flag
        l_arm_spike_switch_flag = l_arm_spike_component.switch_flag

        # Right Spike
        r_spike_chain = chain.get_start('spike', 'right')
        r_spike_component = frag.FKComponent.create(frag_rig,
                                                          r_spike_chain,
                                                          r_spike_chain,
                                                          side='right',
                                                          region='spike',
                                                          lock_root_translate_axes=[])
        r_spike_component.attach_component(r_arm_spike_component, r_spike_arm_chain[1])
        r_spike_flag = r_spike_component.get_flags()[0]

        # Left Spike
        l_spike_chain = chain.get_start('spike', 'left')
        l_spike_component = frag.FKComponent.create(frag_rig,
                                                          l_spike_chain,
                                                          l_spike_chain,
                                                          side='left',
                                                          region='spike',
                                                          lock_root_translate_axes=[])
        l_spike_component.attach_component(l_arm_spike_component, l_spike_arm_chain[1])
        l_spike_flag = l_spike_component.get_flags()[0]

        # Left Hand Contact
        l_hand_contact_chain = chain.get_start('hand_contact', 'left')
        l_prop_component = frag.FKComponent.create(frag_rig,
                                                         l_hand_contact_chain,
                                                         l_hand_contact_chain,
                                                         side='left',
                                                         region='hand_contact',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        l_prop_component.attach_component(l_arm_component, l_arm_chain[1])
        l_hand_contact_flag = l_prop_component.get_flags()[0]
        l_hand_contact_flag.set_as_contact()

        # Right Hand Contact
        r_hand_contact_chain = chain.get_start('hand_contact', 'right')
        r_prop_component = frag.FKComponent.create(frag_rig,
                                                         r_hand_contact_chain,
                                                         r_hand_contact_chain,
                                                         side='right',
                                                         region='hand_contact',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        r_prop_component.attach_component(r_arm_component, r_arm_chain[1])
        r_hand_contact_flag = r_prop_component.get_flags()[0]
        r_hand_contact_flag.set_as_contact()


        # Left Hand Weapon
        l_hand_weapon_chain = chain.get_start('hand_prop', 'left')
        l_weapon_component = frag.FKComponent.create(frag_rig,
                                                           l_hand_weapon_chain,
                                                           l_hand_weapon_chain,
                                                           side='left',
                                                           region='hand_weapon',
                                                           scale=0.1,
                                                           lock_root_translate_axes=[])
        l_weapon_component.attach_component(l_arm_component, l_arm_chain[1])
        l_hand_weapon_flag = l_weapon_component.get_flags()[0]

        # Right Hand Weapon
        r_hand_weapon_chain = chain.get_start('hand_prop', 'right')
        r_weapon_component = frag.FKComponent.create(frag_rig,
                                                           r_hand_weapon_chain,
                                                           r_hand_weapon_chain,
                                                           side='right',
                                                           region='hand_weapon',
                                                           scale=0.1,
                                                           lock_root_translate_axes=[])
        r_weapon_component.attach_component(r_arm_component, r_arm_chain[1])
        r_hand_weapon_flag = r_weapon_component.get_flags()[0]

        # IKFK Left leg
        l_leg_chain_start, l_leg_chain_end = chain.get_chain('leg', 'left')
        l_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 l_leg_chain_start,
                                                                 l_leg_chain_end,
                                                                 side='left',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, -25])
        l_leg_component.attach_component(pelvis_component, pelvis_joint)
        l_leg_flags = l_leg_component.get_flags()
        l_leg_ik_flag = l_leg_component.ik_flag
        l_leg_switch_flag = l_leg_component.switch_flag

        # IKFK Right leg
        r_leg_chain_start, r_leg_chain_end = chain.get_chain('leg', 'right')
        r_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 r_leg_chain_start,
                                                                 r_leg_chain_end,
                                                                 side='right',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, 25])
        r_leg_component.attach_component(pelvis_component, pelvis_joint)
        r_leg_flags = r_leg_component.get_flags()
        r_leg_ik_flag = r_leg_component.ik_flag
        r_leg_switch_flag = r_leg_component.switch_flag

        # IKFK Left Inner leg
        l_leg_inner_chain_start, l_leg_inner_chain_end = chain.get_chain('inner_leg', 'left')
        l_leg_inner_component = frag.ReverseFootComponent.create(frag_rig,
                                                                       l_leg_inner_chain_start,
                                                                       l_leg_inner_chain_end,
                                                                       side='left',
                                                                       region='leg_inner',
                                                                       ik_flag_pv_orient=[-90, 0, 0],
                                                                       ik_flag_orient=[-90, 0, -80])
        l_leg_inner_component.attach_component(pelvis_component, pelvis_joint)
        l_leg_inner_flags = l_leg_inner_component.get_flags()
        l_leg_inner_ik_flag = l_leg_inner_component.ik_flag
        l_leg_inner_switch_flag = l_leg_inner_component.switch_flag

        # IKFK Right Inner leg
        r_leg_inner_chain_start, r_leg_inner_chain_end = chain.get_chain('inner_leg', 'right')
        r_leg_inner_component = frag.ReverseFootComponent.create(frag_rig,
                                                                       r_leg_inner_chain_start,
                                                                       r_leg_inner_chain_end,
                                                                       side='right',
                                                                       region='leg_inner',
                                                                       ik_flag_pv_orient=[-90, 0, 0],
                                                                       ik_flag_orient=[-90, 0, 80])
        r_leg_inner_component.attach_component(pelvis_component, pelvis_joint)
        r_leg_inner_flags = r_leg_inner_component.get_flags()
        r_leg_inner_ik_flag = r_leg_inner_component.ik_flag
        r_leg_inner_switch_flag = r_leg_inner_component.switch_flag

        # # Twist Upper Right leg
        # start_joint = pm.PyNode('thigh_r')
        # end_joint = pm.PyNode('calf_r')
        # r_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        #
        # # Twist Upper Left leg
        # start_joint = pm.PyNode('thigh_l')
        # end_joint = pm.PyNode('calf_l')
        # l_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)

        # Twist Lower Right leg
        start_joint = pm.PyNode('calf_r')
        end_joint = pm.PyNode('foot_r')
        r_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='right',
                                                                        region='twist_lower_leg')

        # Twist Lower Left leg
        start_joint = pm.PyNode('calf_l')
        end_joint = pm.PyNode('foot_l')
        l_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='left',
                                                                        region='twist_lower_leg')
        # # Twist Upper Inner Right leg
        # start_joint = pm.PyNode('thigh_inner_r')
        # end_joint = pm.PyNode('calf_inner_r')
        # inner_r_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        #
        # # Twist Upper Inner Left leg
        # start_joint = pm.PyNode('thigh_inner_l')
        # end_joint = pm.PyNode('calf_inner_l')
        # inner_l_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        # Twist Lower Inner Right leg
        start_joint = pm.PyNode('calf_inner_r')
        end_joint = pm.PyNode('foot_inner_r')
        inner_r_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                              start_joint,
                                                                              end_joint,
                                                                              side='right',
                                                                              region='twist_lower_leg')

        # Twist Lower Inner Left leg
        start_joint = pm.PyNode('calf_inner_l')
        end_joint = pm.PyNode('foot_inner_l')
        inner_l_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                              start_joint,
                                                                              end_joint,
                                                                              side='left',
                                                                              region='twist_lower_leg')

        # Twist Lower Right arm
        start_joint = pm.PyNode('lowerarm_r')
        end_joint = pm.PyNode('hand_r')
        r_twi_low_arm_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='right',
                                                                        region='twist_lower_arm')

        # # Twist Upper Right arm
        # start_joint = pm.PyNode('upperarm_r')
        # end_joint = pm.PyNode('lowerarm_r')
        # r_twi_up_arm_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_arm',
        #                                                                reverse=True)

        # Twist Lower Left arm
        start_joint = pm.PyNode('lowerarm_l')
        end_joint = pm.PyNode('hand_l')
        l_twi_low_arm_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='left',
                                                                        region='twist_lower_arm')

        # # Twist Upper Left arm
        # start_joint = pm.PyNode('upperarm_l')
        # end_joint = pm.PyNode('lowerarm_l')
        # l_twi_up_arm_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_arm',
        #                                                                reverse=True)

        #### Inner Right Toes #######

        # inner right Pinky Toe
        r_pinky_toe_inner_start, r_pinky_toe_inner_end = chain.get_chain('pinky_inner_toe', 'right')
        pinky_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                    r_pinky_toe_inner_start,
                                                                    r_pinky_toe_inner_end,
                                                                    side='right',
                                                                    region='pinky_toe',
                                                                    scale=0.1)
        pinky_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('ball_inner_r'))

        # inner right Middle Toes
        r_middle_toe_inner = chain.get_start('middle_inner_toe', 'right')
        middle_toes_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                      r_middle_toe_inner,
                                                                      r_middle_toe_inner,
                                                                      side='right',
                                                                      region='middle_toes',
                                                                      scale=0.1)
        middle_toes_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('ball_inner_r'))

        # inner right Second Toe
        r_sec_toe_inner_start, r_sec_toe_inner_end = chain.get_chain('second_inner_toe', 'right')
        second_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                     r_sec_toe_inner_start,
                                                                     r_sec_toe_inner_end,
                                                                     side='right',
                                                                     region='second_toe')
        second_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('ball_inner_r'))

        # inner right Big Toe
        r_big_toe_inner_start, r_big_toe_inner_end = chain.get_chain('big_inner_toe', 'right')
        big_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                  r_big_toe_inner_start,
                                                                  r_big_toe_inner_end,
                                                                  side='right',
                                                                  region='big_toe')
        big_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('foot_inner_r'))

        #### Right Toes #######
        # right Pinky Toe
        r_pinky_toe_start, r_pinky_toe_end = chain.get_chain('pinky_toe', 'right')
        r_pinky_toe_component = frag.FKComponent.create(frag_rig,
                                                              r_pinky_toe_start,
                                                              r_pinky_toe_end,
                                                              side='right',
                                                              region='pinky_toe',
                                                              scale=0.1)
        r_pinky_toe_component.attach_component(r_leg_component, pm.PyNode('ball_r'))

        # right Middle Toes
        r_middle_toe_start, r_middle_toe_end = chain.get_chain('middle_toe', 'right')
        r_middle_toes_component = frag.FKComponent.create(frag_rig,
                                                                r_middle_toe_start,
                                                                r_middle_toe_end,
                                                                side='right',
                                                                region='middle_toes')
        r_middle_toes_component.attach_component(r_leg_component, pm.PyNode('ball_r'))

        # right Second Toe
        r_sec_toe_start, r_sec_toe_end = chain.get_chain('second_toe', 'right')
        second_toe_r_component = frag.FKComponent.create(frag_rig,
                                                               r_sec_toe_start,
                                                               r_sec_toe_end,
                                                               side='right',
                                                               region='second_toe')
        second_toe_r_component.attach_component(r_leg_component, pm.PyNode('ball_r'))

        # right Big Toe
        r_big_toe_start, r_big_toe_end = chain.get_chain('big_toe', 'right')
        big_toe_r_component = frag.FKComponent.create(frag_rig,
                                                            r_big_toe_start,
                                                            r_big_toe_end,
                                                            side='right',
                                                            region='big_toe')
        big_toe_r_component.attach_component(r_leg_component, pm.PyNode('foot_r'))

        ####  Inner Left Toes  #######
        # inner left Pinky Toe
        l_pinky_toe_inner_start, l_pinky_toe_inner_end = chain.get_chain('pinky_inner_toe', 'left')
        l_pinky_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                    l_pinky_toe_inner_start,
                                                                    l_pinky_toe_inner_end,
                                                                    side='left',
                                                                    region='pinky_toe')
        l_pinky_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('ball_inner_l'))

        # inner left Middle Toes
        l_middle_toe_inner_start, l_middle_toe_inner_end = chain.get_chain('middle_inner_toe', 'left')
        l_middle_toes_inner_component = frag.FKComponent.create(frag_rig,
                                                                      l_middle_toe_inner_start,
                                                                      l_middle_toe_inner_end,
                                                                      side='left',
                                                                      region='middle_toes')
        l_middle_toes_inner_component.attach_component(l_leg_inner_component, pm.PyNode('ball_inner_l'))

        # inner left Second Toe
        l_second_toe_inner_start, l_second_toe_inner_end = chain.get_chain('second_inner_toe', 'left')
        l_second_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                     l_second_toe_inner_start,
                                                                     l_second_toe_inner_end,
                                                                     side='left',
                                                                     region='second_toe',
                                                                     scale=0.1)
        l_second_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('ball_inner_l'))

        # inner left Big Toe
        l_big_toe_inner_start, l_big_toe_inner_end = chain.get_chain('big_inner_toe', 'left')
        l_big_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                  l_big_toe_inner_start,
                                                                  l_big_toe_inner_end,
                                                                  side='left',
                                                                  region='big_toe',
                                                                  scale=0.1)
        l_big_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('foot_inner_l'))

        ####  Left Toes  #######
        # left Pinky Toe
        l_pinky_toe_start, l_pinky_toe_end = chain.get_chain('pinky_toe', 'left')
        l_pinky_toe_component = frag.FKComponent.create(frag_rig,
                                                              l_pinky_toe_start,
                                                              l_pinky_toe_end,
                                                              side='left',
                                                              region='pinky_toe',
                                                              scale=0.1)
        l_pinky_toe_component.attach_component(l_leg_component, pm.PyNode('ball_l'))

        # left Middle Toes
        l_middle_toe_start, l_middle_toe_end = chain.get_chain('middle_toe', 'left')
        l_middle_toes_component = frag.FKComponent.create(frag_rig,
                                                                l_middle_toe_start,
                                                                l_middle_toe_end,
                                                                side='left',
                                                                region='middle_toes')
        l_middle_toes_component.attach_component(l_leg_component, pm.PyNode('ball_l'))

        # left Second Toe
        l_second_toe_start, l_second_toe_end = chain.get_chain('second_toe', 'left')
        l_second_toe_component = frag.FKComponent.create(frag_rig,
                                                               l_second_toe_start,
                                                               l_second_toe_end,
                                                               side='left',
                                                               region='second_toe')
        l_second_toe_component.attach_component(l_leg_component, pm.PyNode('ball_l'))

        # left Big Toe
        l_big_toe_start, l_big_toe_end = chain.get_chain('big_toe', 'left')
        l_big_toe_component = frag.FKComponent.create(frag_rig,
                                                            l_big_toe_start,
                                                            l_big_toe_end,
                                                            side='left',
                                                            region='big_toe',
                                                            scale=0.1)
        l_big_toe_component.attach_component(l_leg_component, pm.PyNode('foot_l'))

        ####  Left Fingers #######
        # left Index Finger
        l_index_start, l_index_end = chain.get_chain('index_finger', 'left')
        l_index_component = frag.FKComponent.create(frag_rig,
                                                          l_index_start,
                                                          l_index_end,
                                                          side='left',
                                                          region='index_finger')
        l_index_component.attach_component(l_arm_component, l_arm_chain[1])

        # left middle Finger
        l_middle_start, l_middle_end = chain.get_chain('middle_finger', 'left')
        l_middle_component = frag.FKComponent.create(frag_rig,
                                                           l_middle_start,
                                                           l_middle_end,
                                                           side='left',
                                                           region='middle_finger')
        l_middle_component.attach_component(l_arm_component, l_arm_chain[1])

        # left ring Finger
        l_ring_start, l_ring_end = chain.get_chain('ring_finger', 'left')
        l_ring_component = frag.FKComponent.create(frag_rig,
                                                         l_ring_start,
                                                         l_ring_end,
                                                         side='left',
                                                         region='ring_finger')
        l_ring_component.attach_component(l_arm_component, l_arm_chain[1])

        # left Pinky Finger
        l_pinky_start, l_pinky_end = chain.get_chain('pinky_finger', 'left')
        l_pinky_component = frag.FKComponent.create(frag_rig,
                                                          l_pinky_start,
                                                          l_pinky_end,
                                                          side='left',
                                                          region='pinky_finger')
        l_pinky_component.attach_component(l_arm_component, l_arm_chain[1])

        # left Thumb Finger
        l_thumb_start, l_thumb_end = chain.get_chain('thumb', 'left')
        l_thumb_component = frag.FKComponent.create(frag_rig,
                                                          l_thumb_start,
                                                          l_thumb_end,
                                                          side='left',
                                                          region='thumb_finger')
        l_thumb_component.attach_component(l_arm_component, l_arm_chain[1])

        # left Hexadactyly Finger
        l_hexa_start, l_hexa_end = chain.get_chain('hexadactyly_finger', 'left')
        l_hexadactyly_component = frag.FKComponent.create(frag_rig,
                                                                l_hexa_start,
                                                                l_hexa_end,
                                                                side='left',
                                                                region='hexadactyly_finger')
        l_hexadactyly_component.attach_component(l_arm_component, l_arm_chain[1])

        ####  Right Fingers #######
        # left Index Finger
        r_index_start, r_index_end = chain.get_chain('index_finger', 'right')
        r_index_component = frag.FKComponent.create(frag_rig,
                                                          r_index_start,
                                                          r_index_end,
                                                          side='right',
                                                          region='index_finger')
        r_index_component.attach_component(r_arm_component, r_arm_chain[1])

        # left middle Finger
        r_middle_start, r_middle_end = chain.get_chain('middle_finger', 'right')
        r_middle_component = frag.FKComponent.create(frag_rig,
                                                           r_middle_start,
                                                           r_middle_end,
                                                           side='right',
                                                           region='middle_finger')
        r_middle_component.attach_component(r_arm_component, r_arm_chain[1])

        # left ring Finger
        r_ring_start, r_ring_end = chain.get_chain('ring_finger', 'right')
        r_ring_component = frag.FKComponent.create(frag_rig,
                                                         r_ring_start,
                                                         r_ring_end,
                                                         side='right',
                                                         region='ring_finger')
        r_ring_component.attach_component(r_arm_component, r_arm_chain[1])

        # left Pinky Finger
        r_pinky_start, r_pinky_end = chain.get_chain('pinky_finger', 'right')
        r_pinky_component = frag.FKComponent.create(frag_rig,
                                                          r_pinky_start,
                                                          r_pinky_end,
                                                          side='right',
                                                          region='pinky_finger')
        r_pinky_component.attach_component(r_arm_component, r_arm_chain[1])

        # left Thumb Finger
        r_thumb_start, r_thumb_end = chain.get_chain('thumb', 'right')
        r_thumb_component = frag.FKComponent.create(frag_rig,
                                                          r_thumb_start,
                                                          r_thumb_end,
                                                          side='right',
                                                          region='thumb_finger')
        r_thumb_component.attach_component(r_arm_component, r_arm_chain[1])

        # Right Hexadactyly Finger
        r_hexa_start, r_hexa_end = chain.get_chain('hexadactyly_finger', 'right')
        r_hexadactyly_component = frag.FKComponent.create(frag_rig,
                                                                r_hexa_start,
                                                                r_hexa_end,
                                                                side='right',
                                                                region='hexadactyly_finger')
        r_hexadactyly_component.attach_component(r_arm_component, r_arm_chain[1])

        # Head flaps
        # Right Top
        r_head_flap_start, r_head_flap_end = chain.get_chain('head_flap', 'left')
        r_head_flap_component = frag.FKComponent.create(frag_rig,
                                                              r_head_flap_start,
                                                              r_head_flap_end,
                                                              side='right',
                                                              region='head_flap')
        r_head_flap_component.attach_component(neck_component, neck_chain[1])

        # Left Top
        l_head_flap_start, l_head_flap_end = chain.get_chain('head_flap', 'right')
        l_head_flap_component = frag.FKComponent.create(frag_rig,
                                                              l_head_flap_start,
                                                              l_head_flap_end,
                                                              side='left',
                                                              region='head_flap')
        l_head_flap_component.attach_component(neck_component, neck_chain[1])

        # Right Top
        r_jaw_flap_start, r_jaw_flap_end = chain.get_chain('jaw_flap', 'right')
        r_jaw_flap_component = frag.FKComponent.create(frag_rig,
                                                             r_jaw_flap_start,
                                                             r_jaw_flap_end,
                                                             side='right',
                                                             region='jaw_flap')
        r_jaw_flap_component.attach_component(neck_component, neck_chain[1])

        # Left Top
        r_jaw_flap_start, l_jaw_flap_end = chain.get_chain('jaw_flap', 'left')
        l_jaw_flap_component = frag.FKComponent.create(frag_rig,
                                                             r_jaw_flap_start,
                                                             l_jaw_flap_end,
                                                             side='left',
                                                             region='jaw_flap')
        l_jaw_flap_component.attach_component(neck_component, neck_chain[1])

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
        pelvis_contact_component.attach_component(world_component, root)
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
        floor_component.attach_component(world_component, root)
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
        l_foot_contact_component.attach_component(floor_component, floor_joint)
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
        r_foot_contact_component.attach_component(floor_component, floor_joint)
        r_foot_contact_flag = r_foot_contact_component.get_end_flag()
        r_foot_contact_flag.set_as_contact()

        # Left inner foot contact
        l_foot_contact = chain.get_start('foot_inner_contact', 'left')
        l_foot_inner_contact_comp = frag.FKComponent.create(frag_rig,
                                                                  l_foot_contact,
                                                                  l_foot_contact,
                                                                  side='left',
                                                                  region='foot_inner_contact',
                                                                  lock_root_translate_axes=[])
        l_foot_inner_contact_comp.attach_component(floor_component, floor_joint)
        l_foot_inner_contact_flag = l_foot_inner_contact_comp.get_end_flag()
        l_foot_inner_contact_flag.set_as_contact()

        # Right inner foot contact
        r_foot_contact = chain.get_start('foot_inner_contact', 'right')
        r_foot_inner_contact_component = frag.FKComponent.create(frag_rig,
                                                                       r_foot_contact,
                                                                       r_foot_contact,
                                                                       side='right',
                                                                       region='foot_inner_contact',
                                                                       lock_root_translate_axes=[])
        r_foot_inner_contact_component.attach_component(floor_component, floor_joint)
        r_foot_inner_contact_flag = r_foot_inner_contact_component.get_end_flag()
        r_foot_inner_contact_flag.set_as_contact()

        # Left spike contact
        l_spike_contact = chain.get_start('spike_contact', 'left')
        l_spike_contact_comp = frag.FKComponent.create(frag_rig,
                                                             l_spike_contact,
                                                             l_spike_contact,
                                                             side='left',
                                                             region='spike_contact',
                                                             lock_root_translate_axes=[])
        l_spike_contact_comp.attach_component(l_spike_component, l_spike_chain)
        l_spike_contact_flag = l_spike_contact_comp.get_end_flag()
        l_spike_contact_flag.set_as_contact()

        # Right spike contact
        r_spike_contact = chain.get_start('spike_contact', 'right')
        r_spike_contact_component = frag.FKComponent.create(frag_rig,
                                                                  r_spike_contact,
                                                                  r_spike_contact,
                                                                  side='right',
                                                                  region='spike_contact',
                                                                  lock_root_translate_axes=[])
        r_spike_contact_component.attach_component(r_spike_component, r_spike_chain)
        r_spike_contact_flag = r_spike_contact_component.get_end_flag()
        r_spike_contact_flag.set_as_contact()

        # Right aim reference
        aim_ref = chain.get_start('aim', 'center')
        aim_ref_component = frag.FKComponent.create(frag_rig,
                                                          aim_ref,
                                                          aim_ref,
                                                          side='center',
                                                          region='aim_ref',
                                                          lock_root_translate_axes=[])
        aim_ref_component.attach_component(world_component, root, point=False)
        aim_ref_component.attach_component(spine_component, spine_sub_flags[-1], orient=False)
        aim_ref_flag = aim_ref_component.get_end_flag()
        aim_ref_flag.set_as_detail()

        # Mouth
        mouth_chain = chain.get_start('mouth', 'center')
        mouth_component = frag.FKComponent.create(frag_rig,
                                                        mouth_chain,
                                                        mouth_chain,
                                                        side='center',
                                                        region='mouth',
                                                        scale=0.1,
                                                        constrain_scale=True,
                                                        lock_root_translate_axes=[],
                                                        lock_root_scale_axes=[])
        mouth_component.attach_component(neck_component, 'head')
        mouth_flag = mouth_component.get_flags()[0]

        # Tentacles
        tentacle_joints = []

        tentacle_right_upper_start, tentacle_right_upper_end = chain.get_chain('tentacle_upper', 'right')
        tentacle_right_upper_comp = frag.FKComponent.create(frag_rig,
                                                                 tentacle_right_upper_start,
                                                                 tentacle_right_upper_end,
                                                                 side='right',
                                                                 region='tentacle',
                                                                 lock_root_translate_axes=[],
                                                                 constrain_translate=False)
        tentacle_joints.append(tentacle_right_upper_start)

        tentacle_left_upper_start, tentacle_left_upper_end = chain.get_chain('tentacle_upper', 'left')
        tentacle_left_upper_comp = frag.FKComponent.create(frag_rig,
                                                                tentacle_left_upper_start,
                                                                tentacle_left_upper_end,
                                                                side='left',
                                                                region='tentacle',
                                                                lock_root_translate_axes=[],
                                                                constrain_translate=False)
        tentacle_joints.append(tentacle_left_upper_start)

        tentacle_right_lower_start, tentacle_right_lower_end = chain.get_chain('tentacle_lower', 'right')
        tentacle_right_lower_comp = frag.FKComponent.create(frag_rig,
                                                                 tentacle_right_lower_start,
                                                                 tentacle_right_lower_end,
                                                                 side='right',
                                                                 region='tentacle',
                                                                 lock_root_translate_axes=[],
                                                                 constrain_translate=False)
        tentacle_joints.append(tentacle_right_lower_start)

        tentacle_left_lower_start, tentacle_left_lower_end = chain.get_chain('tentacle_lower', 'left')
        tentacle_left_lower_comp = frag.FKComponent.create(frag_rig,
                                                                tentacle_left_lower_start,
                                                                tentacle_left_lower_end,
                                                                side='left',
                                                                region='tentacle',
                                                                lock_root_translate_axes=[],
                                                                constrain_translate=False)
        tentacle_joints.append(tentacle_left_lower_start)

        tentacle_middle_start, tentacle_middle_end = chain.get_chain('tentacle', 'center')
        tentacle_middle_comp = frag.FKComponent.create(frag_rig,
                                                            tentacle_middle_start,
                                                            tentacle_middle_end,
                                                            side='center',
                                                            region='tentacle',
                                                            lock_root_translate_axes=[],
                                                            constrain_translate=False)
        tentacle_joints.append(tentacle_middle_start)

        # Tongue Spline
        tongue_start, tongue_end = chain.get_chain('tongue', 'center')
        start_helper_joint = chain.get_chain('tongue_start', 'center')[0]
        mid_helper_joint = chain.get_chain('tongue_helper', 'center')[0]
        end_helper_joint = chain.get_chain('tongue_end', 'center')[0]
        tongue_component = frag.LeaperTongueComponent.create(frag_rig,
                                                                   tongue_start,
                                                                   tongue_end,
                                                                   end_helper_joint,
                                                                   mid_helper_joint,
                                                                   start_helper_joint=start_helper_joint,
                                                                   side='center',
                                                                   region='tongue',
                                                                   mid_flag=True,
                                                                   can_retract=True)
        tongue_component.attach_component(neck_component, 'head')
        tongue_flags = tongue_component.get_flags()

        # Attach tentacles to tongue
        tentacle_right_upper_comp.attach_component(tongue_component, 'tongue_08_exp')
        tentacle_right_lower_comp.attach_component(tongue_component, 'tongue_08_exp')
        tentacle_left_upper_comp.attach_component(tongue_component, 'tongue_08_exp')
        tentacle_left_lower_comp.attach_component(tongue_component, 'tongue_08_exp')
        tentacle_middle_comp.attach_component(tongue_component, 'tongue_08_exp')

        ## Multi Constraints ###############

        # Left IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='arm',
                                          source_object=l_arm_ik_flag,
                                          target_list=[offset_flag,
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
                                          target_list=[offset_flag,
                                                       r_clav_flag,
                                                       l_arm_ik_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=r_arm_switch_flag)

        # Floor
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='floor_contact',
                                          source_object=floor_flag,
                                          target_list=[root_flag,
                                                       offset_flag],
                                          switch_attr='follow')
        # Root
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag],
                                          switch_attr='follow')

        # Left Spike Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='spike_contact',
                                          source_object=l_spike_contact_flag,
                                          target_list=[floor_flag,
                                                       cog_flag,
                                                       l_spike_flag],
                                          switch_attr='follow')

        # Right Spike Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='spike_contact',
                                          source_object=r_spike_contact_flag,
                                          target_list=[floor_flag,
                                                       cog_flag,
                                                       r_spike_flag],
                                          switch_attr='follow')

        # Left Foot Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot_contact',
                                          source_object=l_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       l_leg_switch_flag],
                                          switch_attr='follow')

        # Right Foot Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot_contact',
                                          source_object=r_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       r_leg_switch_flag],
                                          switch_attr='follow')

        # Left Foot Inner Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot_inner_contact',
                                          source_object=l_foot_inner_contact_flag,
                                          target_list=[floor_flag,
                                                       l_leg_inner_switch_flag],
                                          switch_attr='follow')

        # Right Foot Inner Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot_inner_contact',
                                          source_object=r_foot_inner_contact_flag,
                                          target_list=[floor_flag,
                                                       r_leg_inner_switch_flag],
                                          switch_attr='follow')

        # Pelvis Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='pelvis_contact',
                                          source_object=pelvis_contact_flag,
                                          target_list=[floor_flag,
                                                       pelvis_flag],
                                          switch_attr='follow')

        # Left FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='fk_arm',
                                          source_object=l_arm_fk_flag[0],
                                          target_list=[l_clav_flag,
                                                       spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')
        # Right FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='fk_arm',
                                          source_object=r_arm_fk_flag[0],
                                          target_list=[r_clav_flag,
                                                       spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
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

        # Right IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=r_leg_switch_flag)

        # Left IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
                                          source_object=l_leg_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=l_leg_switch_flag)

        # Inner Right IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_inner_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=r_leg_inner_switch_flag)

        # Inner Left IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
                                          source_object=l_leg_inner_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=l_leg_inner_switch_flag)

        # PV Left Leg
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='leg_pv',
                                          source_object=l_leg_component.pv_flag,
                                          target_list=[offset_flag, l_leg_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Right Leg

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='leg_pv',
                                          source_object=r_leg_component.pv_flag,
                                          target_list=[offset_flag, r_leg_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Inner Left Leg
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='leg_pv',
                                          source_object=l_leg_inner_component.pv_flag,
                                          target_list=[offset_flag, l_leg_inner_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Inner Right Leg

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='leg_pv',
                                          source_object=r_leg_inner_component.pv_flag,
                                          target_list=[offset_flag, r_leg_inner_ik_flag, cog_flag],
                                          switch_obj=None)

        # Left Spike IK Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='spike',
                                          source_object=l_arm_spike_ik_flag,
                                          target_list=[offset_flag,
                                                       l_clav_spike_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=l_arm_spike_switch_flag)

        # Right Spike IK Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='spike',
                                          source_object=r_arm_spike_ik_flag,
                                          target_list=[offset_flag,
                                                       r_clav_spike_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=r_arm_spike_switch_flag)

        # Spine
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_top',
                                          source_object=spine_sub_flags[1],
                                          target_list=[spine_component.end_flag,
                                                       spine_component.mid_flags[1]],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_mid_top',
                                          source_object=spine_component.mid_flags[1],
                                          target_list=[spine_component.mid_offset_groups[1],
                                                       spine_component.mid_flags[0]],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_mid_bottom',
                                          source_object=spine_component.mid_flags[0],
                                          target_list=[spine_component.mid_offset_groups[0],
                                                       spine_component.start_flag],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        # Hand Contacts
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_contact',
                                          source_object=l_hand_contact_flag,
                                          target_list=[floor_flag,
                                                       r_hand_weapon_flag,
                                                       l_hand_weapon_flag,
                                                       pm.PyNode('hand_l')],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_contact',
                                          source_object=r_hand_contact_flag,
                                          target_list=[floor_flag,
                                                       r_hand_weapon_flag,
                                                       l_hand_weapon_flag,
                                                       pm.PyNode('hand_r')],
                                          switch_obj=None)

        # Weapon Props
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_weapon',
                                          source_object=l_hand_weapon_flag,
                                          target_list=[floor_flag,
                                                       r_hand_contact_flag,
                                                       l_hand_contact_flag,
                                                       cog_flag,
                                                       head_flag,
                                                       pm.PyNode('hand_r'),
                                                       offset_flag,
                                                       r_hand_weapon_flag],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_weapon',
                                          source_object=r_hand_weapon_flag,
                                          target_list=[floor_flag,
                                                       r_hand_contact_flag,
                                                       l_hand_contact_flag,
                                                       cog_flag,
                                                       head_flag,
                                                       pm.PyNode('hand_r'),
                                                       offset_flag,
                                                       l_hand_weapon_flag],
                                          switch_obj=None)

        # Head Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_flags[0],
                                          target_list=[spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_flags[2],
                                          target_list=[spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='tongue',
                                          source_object=tongue_flags[2],
                                          target_list=[tongue_flags[0],
                                                       offset_flag])

        frag_rig.rigTemplate.set(LeaperTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class LeaperLotusTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'lotusflowerleaper'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(LeaperLotusTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self):
        # pm.newFile(f=True)

        pm.namespace(set=':')
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')


        frag_root = frag.FRAGRoot.create(root_joint, self.asset_type, self.asset_id)
        frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        root = frag_root.root_joint
        flags_all = frag_rig.flagsAll.get()
        do_not_touch = frag_rig.do_not_touch
        chain = chain_markup.ChainMarkup(root)

        # world
        world_component = frag.WorldComponent.create(frag_rig,
                                                           root,
                                                           'center',
                                                           'world',
                                                           orientation=[-90, 0, 0])
        world_flag = world_component.get_flags()[0]
        offset_flag = world_component.offset_flag
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()
        pm.group(pm.PyNode('f_root_align_transform'), n='flags_center_root')
        pm.parent(pm.PyNode('flags_center_root'), pm.PyNode('flags_all'))

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
        spine_start = chain.get_start('spine', 'center')
        pelvis_component = frag.PelvisComponent.create(frag_rig,
                                                             pelvis_joint,
                                                             spine_start,
                                                             'center',
                                                             'pelvis',
                                                             orientation=[-90, 0, 0])
        pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
        pelvis_flag = pelvis_component.get_flags()[0]

        # Spine
        spine_chain = chain.get_chain('spine', 'center')
        spine_end = chain.get_end('spine', 'center')
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
        neck_component = frag.FKComponent.create(frag_rig,
                                                       neck_chain[0],
                                                       neck_chain[1],
                                                       side='left',
                                                       region='neck',
                                                       lock_root_translate_axes=['v'],
                                                       lock_child_translate_axes=('v'))
        neck_component.attach_component(spine_component, spine_end)
        neck_flags = neck_component.get_flags()
        neck_flags[1].set_as_sub()
        head_flag = neck_component.get_flags()[-1]

        # Left Clavicle
        l_clav_chain = chain.get_start('clav', 'left')
        l_clav_component = frag.FKComponent.create(frag_rig,
                                                         l_clav_chain,
                                                         l_clav_chain,
                                                         side='left',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        l_clav_component.attach_component(spine_component, spine_end)
        l_clav_flag = l_clav_component.get_flags()[0]

        # Right Clavicle
        r_clav_chain = chain.get_start('clav', 'right')
        r_clav_component = frag.FKComponent.create(frag_rig,
                                                         r_clav_chain,
                                                         r_clav_chain,
                                                         side='right',
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
        r_clav_component.attach_component(spine_component, spine_end)
        r_clav_flag = r_clav_component.get_flags()[0]

        # IKFK Right arm
        r_arm_chain = chain.get_chain('arm', 'right')
        r_arm_component = frag.IKFKComponent.create(frag_rig,
                                                          r_arm_chain[0],
                                                          r_arm_chain[1],
                                                          side='right',
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
        r_arm_component.attach_component(r_clav_component, r_clav_chain)
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
        l_arm_component.attach_component(l_clav_component, l_clav_chain)
        l_arm_flags = l_arm_component.get_flags()
        l_arm_ik_flag = l_arm_component.ik_flag
        l_arm_switch_flag = l_arm_component.switch_flag
        l_arm_fk_flag = l_arm_component.fk_flags

        # Left Hand Contact
        l_hand_contact_chain = chain.get_start('hand_contact', 'left')
        l_prop_component = frag.FKComponent.create(frag_rig,
                                                         l_hand_contact_chain,
                                                         l_hand_contact_chain,
                                                         side='left',
                                                         region='hand_contact',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        l_prop_component.attach_component(l_arm_component, l_arm_chain[1])
        l_hand_contact_flag = l_prop_component.get_flags()[0]
        l_hand_contact_flag.set_as_contact()

        # Right Hand Contact
        r_hand_contact_chain = chain.get_start('hand_contact', 'right')
        r_prop_component = frag.FKComponent.create(frag_rig,
                                                         r_hand_contact_chain,
                                                         r_hand_contact_chain,
                                                         side='right',
                                                         region='hand_contact',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[])
        r_prop_component.attach_component(r_arm_component, r_arm_chain[1])
        r_hand_contact_flag = r_prop_component.get_flags()[0]
        r_hand_contact_flag.set_as_contact()


        # Left Hand Weapon
        l_hand_weapon_chain = chain.get_start('hand_prop', 'left')
        l_weapon_component = frag.FKComponent.create(frag_rig,
                                                           l_hand_weapon_chain,
                                                           l_hand_weapon_chain,
                                                           side='left',
                                                           region='hand_weapon',
                                                           scale=0.1,
                                                           lock_root_translate_axes=[])
        l_weapon_component.attach_component(l_arm_component, l_arm_chain[1])
        l_hand_weapon_flag = l_weapon_component.get_flags()[0]

        # Right Hand Weapon
        r_hand_weapon_chain = chain.get_start('hand_prop', 'right')
        r_weapon_component = frag.FKComponent.create(frag_rig,
                                                           r_hand_weapon_chain,
                                                           r_hand_weapon_chain,
                                                           side='right',
                                                           region='hand_weapon',
                                                           scale=0.1,
                                                           lock_root_translate_axes=[])
        r_weapon_component.attach_component(r_arm_component, r_arm_chain[1])
        r_hand_weapon_flag = r_weapon_component.get_flags()[0]

        # IKFK Left leg
        l_leg_chain_start, l_leg_chain_end = chain.get_chain('leg', 'left')
        l_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 l_leg_chain_start,
                                                                 l_leg_chain_end,
                                                                 side='left',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, -25])
        l_leg_component.attach_component(pelvis_component, pelvis_joint)
        l_leg_flags = l_leg_component.get_flags()
        l_leg_ik_flag = l_leg_component.ik_flag
        l_leg_switch_flag = l_leg_component.switch_flag

        # IKFK Right leg
        r_leg_chain_start, r_leg_chain_end = chain.get_chain('leg', 'right')
        r_leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                                 r_leg_chain_start,
                                                                 r_leg_chain_end,
                                                                 side='right',
                                                                 region='leg',
                                                                 ik_flag_pv_orient=[-90, 0, 0],
                                                                 ik_flag_orient=[-90, 0, 25])
        r_leg_component.attach_component(pelvis_component, pelvis_joint)
        r_leg_flags = r_leg_component.get_flags()
        r_leg_ik_flag = r_leg_component.ik_flag
        r_leg_switch_flag = r_leg_component.switch_flag

        # IKFK Left Inner leg
        l_leg_inner_chain_start, l_leg_inner_chain_end = chain.get_chain('inner_leg', 'left')
        l_leg_inner_component = frag.ReverseFootComponent.create(frag_rig,
                                                                       l_leg_inner_chain_start,
                                                                       l_leg_inner_chain_end,
                                                                       side='left',
                                                                       region='leg_inner',
                                                                       ik_flag_pv_orient=[-90, 0, 0],
                                                                       ik_flag_orient=[-90, 0, -80])
        l_leg_inner_component.attach_component(pelvis_component, pelvis_joint)
        l_leg_inner_flags = l_leg_inner_component.get_flags()
        l_leg_inner_ik_flag = l_leg_inner_component.ik_flag
        l_leg_inner_switch_flag = l_leg_inner_component.switch_flag

        # IKFK Right Inner leg
        r_leg_inner_chain_start, r_leg_inner_chain_end = chain.get_chain('inner_leg', 'right')
        r_leg_inner_component = frag.ReverseFootComponent.create(frag_rig,
                                                                       r_leg_inner_chain_start,
                                                                       r_leg_inner_chain_end,
                                                                       side='right',
                                                                       region='leg_inner',
                                                                       ik_flag_pv_orient=[-90, 0, 0],
                                                                       ik_flag_orient=[-90, 0, 80])
        r_leg_inner_component.attach_component(pelvis_component, pelvis_joint)
        r_leg_inner_flags = r_leg_inner_component.get_flags()
        r_leg_inner_ik_flag = r_leg_inner_component.ik_flag
        r_leg_inner_switch_flag = r_leg_inner_component.switch_flag

        # # Twist Upper Right leg
        # start_joint = pm.PyNode('thigh_r')
        # end_joint = pm.PyNode('calf_r')
        # r_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        #
        # # Twist Upper Left leg
        # start_joint = pm.PyNode('thigh_l')
        # end_joint = pm.PyNode('calf_l')
        # l_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)

        # Twist Lower Right leg
        start_joint = pm.PyNode('calf_r')
        end_joint = pm.PyNode('foot_r')
        r_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='right',
                                                                        region='twist_lower_leg')

        # Twist Lower Left leg
        start_joint = pm.PyNode('calf_l')
        end_joint = pm.PyNode('foot_l')
        l_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='left',
                                                                        region='twist_lower_leg')
        # # Twist Upper Inner Right leg
        # start_joint = pm.PyNode('thigh_inner_r')
        # end_joint = pm.PyNode('calf_inner_r')
        # inner_r_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        #
        # # Twist Upper Inner Left leg
        # start_joint = pm.PyNode('thigh_inner_l')
        # end_joint = pm.PyNode('calf_inner_l')
        # inner_l_twi_up_leg_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_leg',
        #                                                                reverse=True)
        # Twist Lower Inner Right leg
        start_joint = pm.PyNode('calf_inner_r')
        end_joint = pm.PyNode('foot_inner_r')
        inner_r_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                              start_joint,
                                                                              end_joint,
                                                                              side='right',
                                                                              region='twist_lower_leg')

        # Twist Lower Inner Left leg
        start_joint = pm.PyNode('calf_inner_l')
        end_joint = pm.PyNode('foot_inner_l')
        inner_l_twi_low_leg_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                              start_joint,
                                                                              end_joint,
                                                                              side='left',
                                                                              region='twist_lower_leg')

        # Twist Lower Right arm
        start_joint = pm.PyNode('lowerarm_r')
        end_joint = pm.PyNode('hand_r')
        r_twi_low_arm_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='right',
                                                                        region='twist_lower_arm')

        # # Twist Upper Right arm
        # start_joint = pm.PyNode('upperarm_r')
        # end_joint = pm.PyNode('lowerarm_r')
        # r_twi_up_arm_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='right',
        #                                                                region='twist_upper_arm',
        #                                                                reverse=True)

        # Twist Lower Left arm
        start_joint = pm.PyNode('lowerarm_l')
        end_joint = pm.PyNode('hand_l')
        l_twi_low_arm_component = frag.TwistFixUpComponent.create(frag_rig,
                                                                        start_joint,
                                                                        end_joint,
                                                                        side='left',
                                                                        region='twist_lower_arm')

        # # Twist Upper Left arm
        # start_joint = pm.PyNode('upperarm_l')
        # end_joint = pm.PyNode('lowerarm_l')
        # l_twi_up_arm_component = frag.TwistFixUpComponent.create(frag_rig,
        #                                                                start_joint,
        #                                                                end_joint,
        #                                                                side='left',
        #                                                                region='twist_upper_arm',
        #                                                                reverse=True)

        #### Inner Right Toes #######

        # inner right Pinky Toe
        r_pinky_toe_inner_start, r_pinky_toe_inner_end = chain.get_chain('pinky_inner_toe', 'right')
        pinky_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                    r_pinky_toe_inner_start,
                                                                    r_pinky_toe_inner_end,
                                                                    side='right',
                                                                    region='pinky_toe',
                                                                    scale=0.1)
        pinky_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('ball_inner_r'))

        # inner right Second Toe
        r_sec_toe_inner_start, r_sec_toe_inner_end = chain.get_chain('second_inner_toe', 'right')
        second_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                     r_sec_toe_inner_start,
                                                                     r_sec_toe_inner_end,
                                                                     side='right',
                                                                     region='second_toe')
        second_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('ball_inner_r'))

        # inner right Big Toe
        r_big_toe_inner_start, r_big_toe_inner_end = chain.get_chain('big_inner_toe', 'right')
        big_toe_inner_r_component = frag.FKComponent.create(frag_rig,
                                                                  r_big_toe_inner_start,
                                                                  r_big_toe_inner_end,
                                                                  side='right',
                                                                  region='big_toe')
        big_toe_inner_r_component.attach_component(r_leg_inner_component, pm.PyNode('foot_inner_r'))

        #### Right Toes #######
        # right Pinky Toe
        r_pinky_toe_start, r_pinky_toe_end = chain.get_chain('pinky_toe', 'right')
        r_pinky_toe_component = frag.FKComponent.create(frag_rig,
                                                              r_pinky_toe_start,
                                                              r_pinky_toe_end,
                                                              side='right',
                                                              region='pinky_toe',
                                                              scale=0.1)
        r_pinky_toe_component.attach_component(r_leg_component, pm.PyNode('ball_r'))

        # right Second Toe
        r_sec_toe_start, r_sec_toe_end = chain.get_chain('second_toe', 'right')
        second_toe_r_component = frag.FKComponent.create(frag_rig,
                                                               r_sec_toe_start,
                                                               r_sec_toe_end,
                                                               side='right',
                                                               region='second_toe')
        second_toe_r_component.attach_component(r_leg_component, pm.PyNode('ball_r'))

        # right Big Toe
        r_big_toe_start, r_big_toe_end = chain.get_chain('big_toe', 'right')
        big_toe_r_component = frag.FKComponent.create(frag_rig,
                                                            r_big_toe_start,
                                                            r_big_toe_end,
                                                            side='right',
                                                            region='big_toe')
        big_toe_r_component.attach_component(r_leg_component, pm.PyNode('foot_r'))

        ####  Inner Left Toes  #######
        # inner left Pinky Toe
        l_pinky_toe_inner_start, l_pinky_toe_inner_end = chain.get_chain('pinky_inner_toe', 'left')
        l_pinky_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                    l_pinky_toe_inner_start,
                                                                    l_pinky_toe_inner_end,
                                                                    side='left',
                                                                    region='pinky_toe')
        l_pinky_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('ball_inner_l'))

        # inner left Second Toe
        l_second_toe_inner_start, l_second_toe_inner_end = chain.get_chain('second_inner_toe', 'left')
        l_second_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                     l_second_toe_inner_start,
                                                                     l_second_toe_inner_end,
                                                                     side='left',
                                                                     region='second_toe',
                                                                     scale=0.1)
        l_second_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('ball_inner_l'))

        # inner left Big Toe
        l_big_toe_inner_start, l_big_toe_inner_end = chain.get_chain('big_inner_toe', 'left')
        l_big_toe_inner_component = frag.FKComponent.create(frag_rig,
                                                                  l_big_toe_inner_start,
                                                                  l_big_toe_inner_end,
                                                                  side='left',
                                                                  region='big_toe',
                                                                  scale=0.1)
        l_big_toe_inner_component.attach_component(l_leg_inner_component, pm.PyNode('foot_inner_l'))

        ####  Left Toes  #######
        # left Pinky Toe
        l_pinky_toe_start, l_pinky_toe_end = chain.get_chain('pinky_toe', 'left')
        l_pinky_toe_component = frag.FKComponent.create(frag_rig,
                                                              l_pinky_toe_start,
                                                              l_pinky_toe_end,
                                                              side='left',
                                                              region='pinky_toe',
                                                              scale=0.1)
        l_pinky_toe_component.attach_component(l_leg_component, pm.PyNode('ball_l'))

        # left Second Toe
        l_second_toe_start, l_second_toe_end = chain.get_chain('second_toe', 'left')
        l_second_toe_component = frag.FKComponent.create(frag_rig,
                                                               l_second_toe_start,
                                                               l_second_toe_end,
                                                               side='left',
                                                               region='second_toe')
        l_second_toe_component.attach_component(l_leg_component, pm.PyNode('ball_l'))

        # left Big Toe
        l_big_toe_start, l_big_toe_end = chain.get_chain('big_toe', 'left')
        l_big_toe_component = frag.FKComponent.create(frag_rig,
                                                            l_big_toe_start,
                                                            l_big_toe_end,
                                                            side='left',
                                                            region='big_toe',
                                                            scale=0.1)
        l_big_toe_component.attach_component(l_leg_component, pm.PyNode('foot_l'))

        ####  Left Fingers #######
        # left Index Finger
        l_index_start, l_index_end = chain.get_chain('index_finger', 'left')
        l_index_component = frag.FKComponent.create(frag_rig,
                                                          l_index_start,
                                                          l_index_end,
                                                          side='left',
                                                          region='index_finger')
        l_index_component.attach_component(l_arm_component, l_arm_chain[1])

        # left middle Finger
        l_middle_start, l_middle_end = chain.get_chain('middle_finger', 'left')
        l_middle_component = frag.FKComponent.create(frag_rig,
                                                           l_middle_start,
                                                           l_middle_end,
                                                           side='left',
                                                           region='middle_finger')
        l_middle_component.attach_component(l_arm_component, l_arm_chain[1])


        # left Pinky Finger
        l_pinky_start, l_pinky_end = chain.get_chain('pinky_finger', 'left')
        l_pinky_component = frag.FKComponent.create(frag_rig,
                                                          l_pinky_start,
                                                          l_pinky_end,
                                                          side='left',
                                                          region='pinky_finger')
        l_pinky_component.attach_component(l_arm_component, l_arm_chain[1])

        # left Thumb Finger
        l_thumb_start, l_thumb_end = chain.get_chain('thumb', 'left')
        l_thumb_component = frag.FKComponent.create(frag_rig,
                                                          l_thumb_start,
                                                          l_thumb_end,
                                                          side='left',
                                                          region='thumb_finger')
        l_thumb_component.attach_component(l_arm_component, l_arm_chain[1])

        # left Hexadactyly Finger
        l_hexa_start, l_hexa_end = chain.get_chain('hexadactyly_finger', 'left')
        l_hexadactyly_component = frag.FKComponent.create(frag_rig,
                                                                l_hexa_start,
                                                                l_hexa_end,
                                                                side='left',
                                                                region='hexadactyly_finger')
        l_hexadactyly_component.attach_component(l_arm_component, l_arm_chain[1])

        ####  Right Fingers #######
        # left Index Finger
        r_index_start, r_index_end = chain.get_chain('index_finger', 'right')
        r_index_component = frag.FKComponent.create(frag_rig,
                                                          r_index_start,
                                                          r_index_end,
                                                          side='right',
                                                          region='index_finger')
        r_index_component.attach_component(r_arm_component, r_arm_chain[1])

        # left middle Finger
        r_middle_start, r_middle_end = chain.get_chain('middle_finger', 'right')
        r_middle_component = frag.FKComponent.create(frag_rig,
                                                           r_middle_start,
                                                           r_middle_end,
                                                           side='right',
                                                           region='middle_finger')
        r_middle_component.attach_component(r_arm_component, r_arm_chain[1])

        # left Pinky Finger
        r_pinky_start, r_pinky_end = chain.get_chain('pinky_finger', 'right')
        r_pinky_component = frag.FKComponent.create(frag_rig,
                                                          r_pinky_start,
                                                          r_pinky_end,
                                                          side='right',
                                                          region='pinky_finger')
        r_pinky_component.attach_component(r_arm_component, r_arm_chain[1])

        # left Thumb Finger
        r_thumb_start, r_thumb_end = chain.get_chain('thumb', 'right')
        r_thumb_component = frag.FKComponent.create(frag_rig,
                                                          r_thumb_start,
                                                          r_thumb_end,
                                                          side='right',
                                                          region='thumb_finger')
        r_thumb_component.attach_component(r_arm_component, r_arm_chain[1])

        # Right Hexadactyly Finger
        r_hexa_start, r_hexa_end = chain.get_chain('hexadactyly_finger', 'right')
        r_hexadactyly_component = frag.FKComponent.create(frag_rig,
                                                                r_hexa_start,
                                                                r_hexa_end,
                                                                side='right',
                                                                region='hexadactyly_finger')
        r_hexadactyly_component.attach_component(r_arm_component, r_arm_chain[1])

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
        pelvis_contact_component.attach_component(world_component, root)
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
        floor_component.attach_component(world_component, root)
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
        l_foot_contact_component.attach_component(floor_component, floor_joint)
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
        r_foot_contact_component.attach_component(floor_component, floor_joint)
        r_foot_contact_flag = r_foot_contact_component.get_end_flag()
        r_foot_contact_flag.set_as_contact()

        # Left inner foot contact
        l_foot_contact = chain.get_start('foot_inner_contact', 'left')
        l_foot_inner_contact_comp = frag.FKComponent.create(frag_rig,
                                                                  l_foot_contact,
                                                                  l_foot_contact,
                                                                  side='left',
                                                                  region='foot_inner_contact',
                                                                  lock_root_translate_axes=[])
        l_foot_inner_contact_comp.attach_component(floor_component, floor_joint)
        l_foot_inner_contact_flag = l_foot_inner_contact_comp.get_end_flag()
        l_foot_inner_contact_flag.set_as_contact()

        # Right inner foot contact
        r_foot_contact = chain.get_start('foot_inner_contact', 'right')
        r_foot_inner_contact_component = frag.FKComponent.create(frag_rig,
                                                                       r_foot_contact,
                                                                       r_foot_contact,
                                                                       side='right',
                                                                       region='foot_inner_contact',
                                                                       lock_root_translate_axes=[])
        r_foot_inner_contact_component.attach_component(floor_component, floor_joint)
        r_foot_inner_contact_flag = r_foot_inner_contact_component.get_end_flag()
        r_foot_inner_contact_flag.set_as_contact()

        # Right aim reference
        aim_ref = chain.get_start('aim', 'center')
        aim_ref_component = frag.FKComponent.create(frag_rig,
                                                          aim_ref,
                                                          aim_ref,
                                                          side='center',
                                                          region='aim_ref',
                                                          lock_root_translate_axes=[])
        aim_ref_component.attach_component(world_component, root, point=False)
        aim_ref_component.attach_component(spine_component, spine_sub_flags[-1], orient=False)
        aim_ref_flag = aim_ref_component.get_end_flag()
        aim_ref_flag.set_as_detail()

        ## Multi Constraints ###############

        # Left IK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='arm',
                                          source_object=l_arm_ik_flag,
                                          target_list=[offset_flag,
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
                                          target_list=[offset_flag,
                                                       r_clav_flag,
                                                       l_arm_ik_flag,
                                                       cog_flag,
                                                       spine_sub_flags[1]],
                                          switch_obj=r_arm_switch_flag)

        # Floor
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='floor_contact',
                                          source_object=floor_flag,
                                          target_list=[root_flag,
                                                       offset_flag],
                                          switch_attr='follow')
        # Root
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag],
                                          switch_attr='follow')

        # Left Foot Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot_contact',
                                          source_object=l_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       l_leg_switch_flag],
                                          switch_attr='follow')

        # Right Foot Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot_contact',
                                          source_object=r_foot_contact_flag,
                                          target_list=[floor_flag,
                                                       r_leg_switch_flag],
                                          switch_attr='follow')

        # Left Foot Inner Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot_inner_contact',
                                          source_object=l_foot_inner_contact_flag,
                                          target_list=[floor_flag,
                                                       l_leg_inner_switch_flag],
                                          switch_attr='follow')

        # Right Foot Inner Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot_inner_contact',
                                          source_object=r_foot_inner_contact_flag,
                                          target_list=[floor_flag,
                                                       r_leg_inner_switch_flag],
                                          switch_attr='follow')

        # Pelvis Contact
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='pelvis_contact',
                                          source_object=pelvis_contact_flag,
                                          target_list=[floor_flag,
                                                       pelvis_flag],
                                          switch_attr='follow')

        # Left FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='fk_arm',
                                          source_object=l_arm_fk_flag[0],
                                          target_list=[l_clav_flag,
                                                       spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')
        # Right FK Arm Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='fk_arm',
                                          source_object=r_arm_fk_flag[0],
                                          target_list=[r_clav_flag,
                                                       spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
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

        # Right IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=r_leg_switch_flag)

        # Left IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
                                          source_object=l_leg_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=l_leg_switch_flag)

        # Inner Right IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='foot',
                                          source_object=r_leg_inner_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=r_leg_inner_switch_flag)

        # Inner Left IK Leg Multi

        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='foot',
                                          source_object=l_leg_inner_ik_flag,
                                          target_list=[offset_flag, pelvis_flag, cog_flag],
                                          switch_obj=l_leg_inner_switch_flag)

        # PV Left Leg
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='leg_pv',
                                          source_object=l_leg_component.pv_flag,
                                          target_list=[offset_flag, l_leg_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Right Leg

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='leg_pv',
                                          source_object=r_leg_component.pv_flag,
                                          target_list=[offset_flag, r_leg_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Inner Left Leg
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='leg_pv',
                                          source_object=l_leg_inner_component.pv_flag,
                                          target_list=[offset_flag, l_leg_inner_ik_flag, cog_flag],
                                          switch_obj=None)

        # PV Inner Right Leg

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='leg_pv',
                                          source_object=r_leg_inner_component.pv_flag,
                                          target_list=[offset_flag, r_leg_inner_ik_flag, cog_flag],
                                          switch_obj=None)

        # Spine
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_top',
                                          source_object=spine_sub_flags[1],
                                          target_list=[spine_component.end_flag,
                                                       spine_component.mid_flags[1]],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_mid_top',
                                          source_object=spine_component.mid_flags[1],
                                          target_list=[spine_component.mid_offset_groups[1],
                                                       spine_component.mid_flags[0]],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='spine_mid_bottom',
                                          source_object=spine_component.mid_flags[0],
                                          target_list=[spine_component.mid_offset_groups[0],
                                                       spine_component.start_flag],
                                          switch_obj=None,
                                          translate=False,
                                          switch_attr='rotateFollow',
                                          default_name='default')

        # Hand Contacts
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_contact',
                                          source_object=l_hand_contact_flag,
                                          target_list=[floor_flag,
                                                       r_hand_weapon_flag,
                                                       l_hand_weapon_flag,
                                                       pm.PyNode('hand_l')],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_contact',
                                          source_object=r_hand_contact_flag,
                                          target_list=[floor_flag,
                                                       r_hand_weapon_flag,
                                                       l_hand_weapon_flag,
                                                       pm.PyNode('hand_r')],
                                          switch_obj=None)

        # Weapon Props
        frag.MultiConstraint.create(frag_rig,
                                          side='left',
                                          region='hand_weapon',
                                          source_object=l_hand_weapon_flag,
                                          target_list=[floor_flag,
                                                       r_hand_contact_flag,
                                                       l_hand_contact_flag,
                                                       cog_flag,
                                                       head_flag,
                                                       pm.PyNode('hand_r'),
                                                       offset_flag,
                                                       r_hand_weapon_flag],
                                          switch_obj=None)

        frag.MultiConstraint.create(frag_rig,
                                          side='right',
                                          region='hand_weapon',
                                          source_object=r_hand_weapon_flag,
                                          target_list=[floor_flag,
                                                       r_hand_contact_flag,
                                                       l_hand_contact_flag,
                                                       cog_flag,
                                                       head_flag,
                                                       pm.PyNode('hand_r'),
                                                       offset_flag,
                                                       l_hand_weapon_flag],
                                          switch_obj=None)

        # Head Multi
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_flags[0],
                                          target_list=[spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')

        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_flags[2],
                                          target_list=[spine_sub_flags[1],
                                                       offset_flag],
                                          t=False,
                                          switch_attr='rotateFollow')

        frag_rig.rigTemplate.set(LeaperTemplate.__name__)
        frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig
    
class LeaperLotusTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'lotusflowerleaper'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(LeaperLotusTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True, lock_toes=True):
        # pm.newFile(f=True)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, 'combatant', self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        # Core Components
        # world
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = frag.WorldComponent.create(frag_rig,
                                                     root_joint,
                                                     'center',
                                                     'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])

        # Cog
        pelvis_start, pelvis_end = skel_hierarchy.get_chain('pelvis', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                 pelvis_start,
                                                 pelvis_start,
                                                 'center',
                                                 'cog',
                                                 orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode(offset_flag))
        cog_flag = cog_component.get_flags()[0]

        # floor
        floor_joint = skel_hierarchy.get_start('floor', 'center')
        floor_component = frag.FKComponent.create(frag_rig,
                                                  floor_joint,
                                                  floor_joint,
                                                  side='center',
                                                  region='floor_contact',
                                                  lock_root_translate_axes=[])
        floor_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        floor_flag = floor_component.get_end_flag()
        floor_flag.set_as_contact()

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='floor_contact',
                                    source_object=floor_flag,
                                    target_list=[root_flag,
                                                 offset_flag])

        ###
        # Center Components
        ###
        # Pelvis
        pelvis_component = frag.PelvisComponent.create(frag_rig,
                                                       pelvis_start,
                                                       pelvis_end,
                                                       'center',
                                                       'pelvis',
                                                       orientation=[-90, 0, 0])
        pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
        pelvis_flag = pelvis_component.get_flags()[0]

        # pelvis contact
        contact_joint = skel_hierarchy.get_start('pelvis_contact', 'center')
        pelvis_contact_component = frag.FKComponent.create(frag_rig,
                                                           contact_joint,
                                                           contact_joint,
                                                           side='center',
                                                           region='pelvis_contact',
                                                           lock_root_translate_axes=[])
        pelvis_contact_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        pelvis_contact_flag = pelvis_contact_component.get_end_flag()
        pelvis_contact_flag.set_as_contact()

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='pelvis_contact',
                                    source_object=pelvis_contact_flag,
                                    target_list=[floor_flag,
                                                 offset_flag])

        # Spine
        spine_start, spine_end = skel_hierarchy.get_chain('spine', 'center')
        spine_component = frag.RFKComponent.create(frag_rig,
                                                   spine_start,
                                                   spine_end,
                                                   'center',
                                                   'spine')
        spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
        spine_sub_flags = spine_component.sub_flags

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='spine_top',
                                    source_object=spine_sub_flags[1],
                                    target_list=[spine_component.end_flag,
                                                 spine_component.mid_flags[1]],
                                    translate=False,
                                    default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='spine_mid_top',
                                    source_object=spine_component.mid_flags[1],
                                    target_list=[spine_component.mid_offset_groups[1],
                                                 spine_component.mid_flags[0]],
                                    translate=False,
                                    default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='spine_mid_bottom',
                                    source_object=spine_component.mid_flags[0],
                                    target_list=[spine_component.mid_offset_groups[0],
                                                 spine_component.start_flag],
                                    translate=False,
                                    default_name='default')

        # Neck
        neck_start, neck_end = skel_hierarchy.get_chain('neck', 'center')
        neck_component = frag.FKComponent.create(frag_rig,
                                                 neck_start,
                                                 neck_end,
                                                 side='center',
                                                 region='neck',
                                                 lock_root_translate_axes=['v'],
                                                 lock_child_translate_axes=['v'])
        neck_component.attach_component(spine_component, spine_end)
        neck_flags = neck_component.get_flags()
        neck_flags[1].set_as_sub()
        head_flag = neck_component.get_flags()[-1]

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='neck',
                                    source_object=neck_flags[0],
                                    target_list=[spine_sub_flags[1],
                                                 offset_flag],
                                    t=False)

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='neck',
                                    source_object=neck_flags[2],
                                    target_list=[spine_sub_flags[1],
                                                 offset_flag],
                                    t=False)

        ###
        # Utility Joints
        ###

        # util
        util_joint = skel_hierarchy.get_start('utility', 'center')
        util_component = frag.FKComponent.create(frag_rig,
                                                 util_joint,
                                                 util_joint,
                                                 side='center',
                                                 region='utility',
                                                 lock_root_translate_axes=[])
        util_component.attach_component(world_component, root_joint)
        util_flag = util_component.get_end_flag()
        util_flag.set_as_util()

        # util warp
        util_warp_joint = skel_hierarchy.get_start('utility_warp', 'center')
        util_warp_component = frag.FKComponent.create(frag_rig,
                                                      util_warp_joint,
                                                      util_warp_joint,
                                                      side='center',
                                                      region='util_warp',
                                                      lock_root_translate_axes=[])
        util_warp_component.attach_component(world_component, root_joint)
        util_warp_flag = util_warp_component.get_end_flag()
        util_warp_flag.set_as_util()

        # aim ref
        aim_ref = skel_hierarchy.get_start('aim', 'center')
        aim_ref_component = frag.FKComponent.create(frag_rig,
                                                    aim_ref,
                                                    aim_ref,
                                                    side='center',
                                                    region='aim_ref',
                                                    lock_root_translate_axes=[])
        aim_ref_component.attach_component(world_component, root_joint, point=False)
        aim_ref_component.attach_component(spine_component, spine_sub_flags[-1], orient=False)
        aim_ref_flag = aim_ref_component.get_end_flag()
        aim_ref_flag.set_as_detail()

        side_component_dict = {}
        for side in ['left', 'right']:
            clav_start = skel_hierarchy.get_start('clav', side)
            clav_component = frag.FKComponent.create(frag_rig,
                                                     clav_start,
                                                     clav_start,
                                                     side=side,
                                                     region='clav',
                                                     lock_root_translate_axes=['v'])
            clav_component.attach_component(spine_component, spine_end)
            clav_flag = clav_component.get_flags()[0]

            # IKFK main arm
            arm_start, arm_end = skel_hierarchy.get_chain('arm', side)
            arm_component = frag.IKFKComponent.create(frag_rig,
                                                      arm_start,
                                                      arm_end,
                                                      side=side,
                                                      region='arm',
                                                      ik_flag_pv_orient=[-90, 0, 0])
            arm_component.attach_component(clav_component, clav_start)

            frag.MultiConstraint.create(frag_rig,
                                        side='left',
                                        region='arm_pv',
                                        source_object=arm_component.pv_flag,
                                        target_list=[offset_flag, clav_flag, spine_sub_flags[1], cog_flag])

            for finger in ['index_finger', 'middle_finger', 'ring_finger', 'pinky_finger', 'hexadactyly_finger', 'thumb']:
                finger_start, finger_end = skel_hierarchy.get_chain(finger, side)
                if finger_start:
                    index_component = frag.FKComponent.create(frag_rig,
                                                              finger_start,
                                                              finger_end,
                                                              side=side,
                                                              region=finger)
                    index_component.attach_component(arm_component, arm_end)

            # Hand contact
            hand_contact_joint = skel_hierarchy.get_start('hand_contact', side)
            prop_component = frag.FKComponent.create(frag_rig,
                                                     hand_contact_joint,
                                                     hand_contact_joint,
                                                     side=side,
                                                     region='hand_contact',
                                                     scale=4.0,
                                                     lock_root_translate_axes=[])
            prop_component.attach_component(arm_component, arm_end)
            hand_contact_flag = prop_component.get_flags()[0]
            hand_contact_flag.set_as_contact()

            # Left Hand Weapon
            hand_weapon_joint = skel_hierarchy.get_start('hand_prop', side)
            weapon_component = frag.FKComponent.create(frag_rig,
                                                       hand_weapon_joint,
                                                       hand_weapon_joint,
                                                       side=side,
                                                       region='hand_weapon',
                                                       scale=0.1,
                                                       lock_root_translate_axes=[])
            weapon_component.attach_component(arm_component, arm_end)

            side_component_dict[side] = [clav_component, arm_component, prop_component, weapon_component]

            # IKFK spike arm
            # Clavicle Spike
            spike_clav_start = skel_hierarchy.get_start('spike_clav', side)
            if spike_clav_start:
                clav_spike_component = frag.FKComponent.create(frag_rig,
                                                               spike_clav_start,
                                                               spike_clav_start,
                                                               side=side,
                                                               region='clav_spike',
                                                               lock_root_translate_axes=['v'])
                clav_spike_component.attach_component(spine_component, spine_end)

                side_component_dict[side].append(clav_spike_component)
            else:
                side_component_dict[side].append(None)

            # Spike IKFK arm
            spike_arm_start, spike_arm_end = skel_hierarchy.get_chain('spike_arm', side)
            if spike_arm_start:
                arm_spike_component = frag.IKFKComponent.create(frag_rig,
                                                                spike_arm_start,
                                                                spike_arm_end,
                                                                side=side,
                                                                region='arm_spike',
                                                                ik_flag_pv_orient=[-90, 0, 0])
                arm_spike_component.attach_component(clav_spike_component, spike_clav_start)
                arm_spike_ik_flag = arm_spike_component.ik_flag
                arm_spike_switch_flag = arm_spike_component.switch_flag

                # Right Spike
                spike_start = skel_hierarchy.get_start('spike', side)
                spike_component = frag.FKComponent.create(frag_rig,
                                                          spike_start,
                                                          spike_start,
                                                          side=side,
                                                          region='spike',
                                                          lock_root_translate_axes=[])
                spike_component.attach_component(arm_spike_component, spike_arm_end)
                spike_flag = spike_component.get_flags()[0]

                # spike contact
                spike_contact_joint = skel_hierarchy.get_start('spike_contact', 'left')
                spike_contact_comp = frag.FKComponent.create(frag_rig,
                                                             spike_contact_joint,
                                                             spike_contact_joint,
                                                             side='left',
                                                             region='spike_contact',
                                                             lock_root_translate_axes=[])
                spike_contact_comp.attach_component(spike_component, spike_start)
                spike_contact_flag = spike_contact_comp.get_end_flag()
                spike_contact_flag.set_as_contact()

                side_component_dict[side].append(arm_spike_component)
            else:
                side_component_dict[side].append(None)

            # IKFK leg
            leg_start, leg_end = skel_hierarchy.get_chain('leg', side)
            leg_component = frag.ReverseFootComponent.create(frag_rig,
                                                             leg_start,
                                                             leg_end,
                                                             side=side,
                                                             region='leg',
                                                             ik_flag_pv_orient=[-90, 0, 0],
                                                             ik_flag_orient=[-90, 0, -25] if side == 'left' else [-90, 0, 25])
            leg_component.attach_component(pelvis_component, pelvis_start)
            leg_flags = leg_component.get_flags()
            leg_ik_flag = leg_component.ik_flag
            leg_switch_flag = leg_component.switch_flag

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='foot',
                                        source_object=leg_ik_flag,
                                        target_list=[offset_flag, pelvis_flag, cog_flag],
                                        switch_obj=leg_switch_flag)

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='leg_pv',
                                        source_object=leg_component.pv_flag,
                                        target_list=[offset_flag, leg_ik_flag, cog_flag])

            for toe in ['pinky_toe', 'middle_toe', 'second_toe', 'big_toe']:
                r_pinky_toe_start, r_pinky_toe_end = skel_hierarchy.get_chain(toe, side)
                r_pinky_toe_component = frag.FKComponent.create(frag_rig,
                                                                r_pinky_toe_start,
                                                                r_pinky_toe_end,
                                                                side=side,
                                                                region=toe,
                                                                lock_root_translate_axes=attr_utils.TRANSLATION_ATTRS if lock_toes else [],
                                                                scale=0.1)
                r_pinky_toe_component.attach_component(leg_component, leg_end if toe != 'big_toe' else leg_end.getParent())

            # foot contact
            foot_contact_joint = skel_hierarchy.get_start('foot_contact', side)
            foot_contact_component = frag.FKComponent.create(frag_rig,
                                                             foot_contact_joint,
                                                             foot_contact_joint,
                                                             side=side,
                                                             region='foot_contact',
                                                             lock_root_translate_axes=[])
            foot_contact_component.attach_component(floor_component, floor_joint)
            foot_contact_flag = foot_contact_component.get_end_flag()
            foot_contact_flag.set_as_contact()

            # Left Foot Contact
            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='foot_contact',
                                        source_object=foot_contact_flag,
                                        target_list=[floor_flag,
                                                     leg_switch_flag])

            # IKFK Inner leg
            leg_inner_start, leg_inner_end = skel_hierarchy.get_chain('inner_leg', side)
            leg_inner_component = frag.ReverseFootComponent.create(frag_rig,
                                                                   leg_inner_start,
                                                                   leg_inner_end,
                                                                   side=side,
                                                                   region='leg_inner',
                                                                   ik_flag_pv_orient=[-90, 0, 0],
                                                                   ik_flag_orient=[-90, 0, -80] if side == 'left' else [-90, 0, 80])
            leg_inner_component.attach_component(pelvis_component, pelvis_start)
            leg_inner_ik_flag = leg_inner_component.ik_flag
            leg_inner_switch_flag = leg_inner_component.switch_flag

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='foot',
                                        source_object=leg_inner_ik_flag,
                                        target_list=[offset_flag, pelvis_flag, cog_flag],
                                        switch_obj=leg_inner_switch_flag)

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='leg_pv',
                                        source_object=leg_inner_component.pv_flag,
                                        target_list=[offset_flag, leg_inner_ik_flag, cog_flag])

            for toe in ['pinky_inner_toe', 'middle_inner_toe', 'second_inner_toe', 'big_inner_toe']:
                toe_start, toe_end = skel_hierarchy.get_chain(toe, side)
                toe_component = frag.FKComponent.create(frag_rig,
                                                        toe_start,
                                                        toe_end,
                                                        side=side,
                                                        region=toe,
                                                        lock_root_translate_axes=attr_utils.TRANSLATION_ATTRS if lock_toes else [],
                                                        scale=0.1)
                toe_component.attach_component(leg_inner_component, leg_inner_end if toe != 'big_inner_toe' else leg_inner_end.getParent())

            # inner foot contact
            foot_contact_joint = skel_hierarchy.get_start('foot_inner_contact', side)
            foot_inner_contact_comp = frag.FKComponent.create(frag_rig,
                                                              foot_contact_joint,
                                                              foot_contact_joint,
                                                              side=side,
                                                              region='foot_inner_contact',
                                                              lock_root_translate_axes=[])
            foot_inner_contact_comp.attach_component(floor_component, floor_joint)
            foot_inner_contact_flag = foot_inner_contact_comp.get_end_flag()
            foot_inner_contact_flag.set_as_contact()

            # Left Foot Inner Contact
            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='foot_inner_contact',
                                        source_object=foot_inner_contact_flag,
                                        target_list=[floor_flag,
                                                     leg_inner_switch_flag])

            side_component_dict[side] += [leg_component, leg_inner_component]

        # Multi Constraints
        for side in ['left', 'right']:
            # Arm Multi constraint
            inv_side = 'left' if side == 'right' else 'right'

            clav_component, arm_component, weapon_component, prop_component, spike_clav_component, spike_arm_component, leg_component, leg_inner_component = side_component_dict[side]
            clav_flag = clav_component.get_flags()[0]

            arm_ik_flag = arm_component.ik_flag
            arm_switch_flag = arm_component.switch_flag
            arm_fk_flag = arm_component.fk_flags[0]
            inv_arm_ik_flag = side_component_dict[inv_side][1].ik_flag

            weapon_flag = weapon_component.get_flags()[0]
            inv_weapon_flag = side_component_dict[inv_side][2].get_flags()[0]

            prop_flag = prop_component.get_flags()[0]
            inv_prop_flag = side_component_dict[inv_side][3].get_flags()[0]

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='ik_arm',
                                        source_object=arm_ik_flag,
                                        target_list=[offset_flag,
                                                     clav_flag,
                                                     inv_arm_ik_flag,
                                                     cog_flag,
                                                     spine_sub_flags[1],
                                                     floor_flag],
                                        switch_obj=arm_switch_flag, )

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='fk_arm',
                                        source_object=arm_fk_flag,
                                        target_list=[clav_flag,
                                                     spine_sub_flags[1],
                                                     offset_flag,
                                                     cog_flag],
                                        t=False)

            # build target list with optional leg targets.
            target_list = [weapon_flag,
                           inv_weapon_flag,
                           floor_flag,
                           cog_flag,
                           leg_component.bindJoints.get()[0],
                           side_component_dict[inv_side][6].bindJoints.get()[0],
                           arm_component.bindJoints.get()[-1]]

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='hand_prop',
                                        source_object=prop_flag,
                                        target_list=target_list,
                                        default_name=f'{side[0]}_weapon')

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='weapon',
                                        source_object=weapon_flag,
                                        target_list=[arm_component.bindJoints.get()[-1],
                                                     prop_flag,
                                                     inv_prop_flag,
                                                     inv_weapon_flag,
                                                     cog_flag,
                                                     head_flag,
                                                     offset_flag,
                                                     floor_flag],
                                        default_name=f'{side[0]}_hand')


        if finalize:
            frag_rig.rigTemplate.set(LeaperTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class ShieldProtectorTemplate(LeaperLotusTemplate):
    VERSION = 1
    ASSET_ID = 'shieldprotector'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(ShieldProtectorTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        frag_rig = super().build(finalize=False, lock_toes=False)
        frag_root = frag_rig.get_root()
        frag_root.asset_id = self.ASSET_ID
        frag_root.assetName.set(self.ASSET_ID)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        world_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.WorldComponent, side='center', region='world'))
        if not world_component:
            return frag_rig
        world_flag = world_component.world_flag

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)
        _, spine_end = skel_hierarchy.get_chain('spine', 'center')

        spine_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.RFKComponent, side='center', region='spine'))
        if not spine_component:
            return frag_rig
        spine_end_flag = spine_component.end_flag

        _, neck_end = skel_hierarchy.get_chain('neck', 'center')

        neck_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.FKComponent, side='center', region='neck'))
        if not neck_component:
            return frag_rig

        eye_start, eye_end = skel_hierarchy.get_chain('eye', 'center')
        eye_component = frag.FKComponent.create(frag_rig,
                                                eye_start,
                                                eye_end,
                                                side='center',
                                                region='eye',
                                                lock_root_translate_axes=[])
        eye_component.attach_component(spine_component, spine_end)
        eye_flag = eye_component.get_flags()[0]

        eyeball_start, eyeball_end = skel_hierarchy.get_chain('eyeball', 'center')
        eyeball_component = frag.FKComponent.create(frag_rig,
                                                eyeball_start,
                                                eyeball_end,
                                                side='center',
                                                region='eyeball')
        eyeball_component.attach_component(eye_component, eye_end)

        # jaw
        jaw_start, jaw_end = skel_hierarchy.get_chain('jaw', 'center')
        jaw_component = frag.FKComponent.create(frag_rig,
                                                jaw_start,
                                                jaw_end,
                                                side='center',
                                                region='jaw')
        jaw_component.attach_component(neck_component, neck_end)

        for side in ['left', 'right']:
            lid_start, lid_end = skel_hierarchy.get_chain('lid', side)
            lid_component = frag.FKComponent.create(frag_rig,
                                                    lid_start,
                                                    lid_end,
                                                    side=side,
                                                    region='lid',
                                                    lock_root_rotate_axes=['rx', 'rz'])
            lid_component.attach_component(eye_component, eye_end)

            slab_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.FKComponent, side=side, region='clav_spike'))
            if slab_component:
                slab_flag = slab_component.get_flags()[0]
                frag.MultiConstraint.create(frag_rig,
                                            side=side,
                                            region='clav_spike',
                                            source_object=slab_flag,
                                            target_list=[eye_flag, spine_end_flag])

        if finalize:
            frag_rig.rigTemplate.set(ShieldProtectorTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig