#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates the Gargoyle Rig.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.common.utils import lists

from mca.mya.rigging import chain_markup, tek
from mca.mya.utils import attr_utils

from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging.templates import base_biped_template


class TriadTwinRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'triadtwin'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, 'combatant', self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        flags_all = tek_rig.flagsAll.get()

        # Core Components
        # world
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = tek.WorldComponent.create(tek_rig,
                                                     root_joint,
                                                     'center',
                                                     'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag

        # Root Multiconstraint
        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])

        # Cog
        pelvis_start, pelvis_end = skel_hierarchy.get_chain('pelvis', 'center')
        cog_component = tek.CogComponent.create(tek_rig,
                                                 pelvis_start,
                                                 pelvis_start,
                                                 'center',
                                                 'cog',
                                                 orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode(offset_flag))
        cog_flag = cog_component.get_flags()[0]

        ###
        # Center Components
        ###
        # Pelvis
        pelvis_component = tek.PelvisComponent.create(tek_rig,
                                                       pelvis_start,
                                                       pelvis_end,
                                                       'center',
                                                       'pelvis',
                                                       orientation=[-90, 0, 0])
        pelvis_component.attach_component(cog_component, pm.PyNode(cog_flag))
        pelvis_flag = pelvis_component.get_flags()[0]

        # Spine
        spine_start, spine_end = skel_hierarchy.get_chain('spine', 'center')
        spine_component = tek.RFKComponent.create(tek_rig,
                                                   spine_start,
                                                   spine_end,
                                                   'center',
                                                   'spine')
        spine_component.attach_component(cog_component, pm.PyNode(cog_flag))
        spine_sub_flags = spine_component.sub_flags

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='spine_top',
                                    source_object=spine_sub_flags[1],
                                    target_list=[spine_component.end_flag,
                                                 spine_component.mid_flags[1],
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='spine_mid_top',
                                    source_object=spine_component.mid_flags[1],
                                    target_list=[spine_component.mid_offset_groups[1],
                                                 spine_component.mid_flags[0],
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='spine_mid_bottom',
                                    source_object=spine_component.mid_flags[0],
                                    target_list=[spine_component.mid_offset_groups[0],
                                                 spine_component.start_flag,
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        # Neck
        neck_start, neck_end = skel_hierarchy.get_chain('neck', 'center')
        neck_component = tek.RFKComponent.create(tek_rig,
                                                  neck_start,
                                                  neck_end,
                                                  'center',
                                                  'neck',
                                                  False)
        neck_component.attach_component(spine_component, spine_end)
        head_flag = neck_component.end_flag
        neck_flag = neck_component.start_flag
        neck_flag.set_as_sub()
        mid_neck_flag = neck_component.mid_flags[0]
        mid_neck_flag.set_as_detail()

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='head',
                                    source_object=head_flag,
                                    target_list=[offset_flag,
                                                 neck_flag,
                                                 mid_neck_flag,
                                                 cog_flag],
                                    translate=False)

        # Jaw
        jaw_joint = skel_hierarchy.get_start('jaw', 'center')
        if jaw_joint:
            jaw_component = tek.FKComponent.create(tek_rig,
                                                    jaw_joint,
                                                    jaw_joint,
                                                    side='center',
                                                    region='jaw',
                                                    lock_root_translate_axes=[])
            jaw_component.attach_component(world_component, neck_end)

        # Center
        floor_joint = skel_hierarchy.get_start('floor', 'center')
        floor_component = tek.FKComponent.create(tek_rig,
                                                  floor_joint,
                                                  floor_joint,
                                                  side='center',
                                                  region='floor_contact',
                                                  lock_root_translate_axes=[])
        floor_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        floor_flag = floor_component.get_end_flag()
        floor_flag.set_as_contact()

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='floor_contact',
                                    source_object=floor_flag,
                                    target_list=[root_flag,
                                                 offset_flag])

        # Split Sides
        side_component_dict = {}
        for side in ['left', 'right']:
            ###
            # Arm Build
            ###

            # Clav
            clav_start, clav_end = skel_hierarchy.get_chain('clav', side)
            clav_component = tek.FKComponent.create(tek_rig,
                                                     clav_start,
                                                     clav_end,
                                                     side=side,
                                                     region='clav',
                                                     lock_root_translate_axes=['v'])
            clav_component.attach_component(spine_component, spine_end)
            clav_flag = clav_component.get_flags()[0]

            # IKFK arm
            arm_start, arm_end = skel_hierarchy.get_chain('arm', side)
            arm_component = tek.IKFKComponent.create(tek_rig,
                                                      arm_start,
                                                      arm_end,
                                                      side=side,
                                                      region='arm',
                                                      ik_flag_pv_orient=[-90, 0, 0])
            arm_component.attach_component(clav_component, clav_start)

            tek.MultiConstraint.create(tek_rig,
                                        side=side,
                                        region='arm_pv',
                                        source_object=arm_component.pv_flag,
                                        target_list=[offset_flag, clav_flag, spine_sub_flags[1], cog_flag])

            for finger in ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinky_finger']:
                # Finger
                finger_start, finger_end = skel_hierarchy.get_chain(finger, side)
                if not finger_start:
                    continue
                finger_component = tek.FKComponent.create(tek_rig,
                                                           finger_start,
                                                           finger_end,
                                                           side=side,
                                                           region=finger,
                                                           lock_child_rotate_axes=['rx', 'ry'],
                                                           scale=0.1)
                finger_component.attach_component(arm_component, arm_end)
                first_knuckle_flag = finger_component.get_flags()[1]
                attr_utils.set_attr_state(first_knuckle_flag.node, locked=False, attr_list=attr_utils.ROTATION_ATTRS,
                                          visibility=True)

            # Hand contact
            hand_contact = skel_hierarchy.get_start('hand_contact', side)
            prop_component = tek.FKComponent.create(tek_rig,
                                                     hand_contact,
                                                     hand_contact,
                                                     side=side,
                                                     region='hand_prop',
                                                     scale=0.1,
                                                     lock_root_translate_axes=[])
            prop_component.attach_component(arm_component, arm_end)
            prop_flag = prop_component.get_flags()[0]
            prop_flag.set_as_sub()

            # Hand weapon
            weapon_start = skel_hierarchy.get_start('hand_prop', side)
            weapon_component = tek.FKComponent.create(tek_rig,
                                                       weapon_start,
                                                       weapon_start,
                                                       side=side,
                                                       region='hand_weapon',
                                                       scale=0.1,
                                                       lock_root_translate_axes=[])
            weapon_component.attach_component(arm_component, arm_end)
            weapon_flag = weapon_component.get_flags()[0]
            weapon_flag.set_as_sub()

            side_component_dict[side] = [clav_component, arm_component, prop_component, weapon_component]

        ###
        # Utility Joints
        ###

        # util
        util_joint = skel_hierarchy.get_start('utility', 'center')
        util_component = tek.FKComponent.create(tek_rig,
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
        util_warp_component = tek.FKComponent.create(tek_rig,
                                                      util_warp_joint,
                                                      util_warp_joint,
                                                      side='center',
                                                      region='util_warp',
                                                      lock_root_translate_axes=[])
        util_warp_component.attach_component(world_component, root_joint)
        util_warp_flag = util_warp_component.get_end_flag()
        util_warp_flag.set_as_util()

        # Pelvis
        contact_joint = skel_hierarchy.get_start('pelvis_contact', 'center')
        pelvis_contact_component = tek.FKComponent.create(tek_rig,
                                                           contact_joint,
                                                           contact_joint,
                                                           side='center',
                                                           region='pelvis_contact',
                                                           lock_root_translate_axes=[])
        pelvis_contact_component.attach_component(world_component, pm.PyNode(offset_flag), point=False,
                                                  orient=False)
        pelvis_contact_flag = pelvis_contact_component.get_end_flag()
        pelvis_contact_flag.set_as_contact()

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='pelvis_contact',
                                    source_object=pelvis_contact_flag,
                                    target_list=[floor_flag,
                                                 offset_flag])

        start_tentacle, end_tentacle = skel_hierarchy.get_chain('tail', 'center')
        tentacle_component = tek.SplineIKRibbonComponent.create(tek_rig,
                                                                 start_tentacle,
                                                                 end_tentacle,
                                                                 side='center',
                                                                 region='tail')
        tentacle_component.attach_component(pelvis_component, pelvis_start)

        tek.MultiConstraint.create(tek_rig,
                                    side=side,
                                    region='tail_mid',
                                    source_object=tentacle_component.primary_flags[1],
                                    target_list=[root_flag,
                                                 pelvis_flag])

        tek.MultiConstraint.create(tek_rig,
                                    side=side,
                                    region='tail_end',
                                    source_object=tentacle_component.primary_flags[-1],
                                    target_list=[root_flag,
                                                 pelvis_flag])

        # Multi Constraints
        for side in ['left', 'right']:
            # Arm Multi constraint
            inv_side = 'left' if side == 'right' else 'right'

            clav_component, arm_component, weapon_component, prop_component = side_component_dict[side]
            clav_flag = clav_component.get_flags()[0]

            arm_ik_flag = arm_component.ik_flag
            arm_switch_flag = arm_component.switch_flag
            arm_fk_flag = arm_component.fk_flags[0]
            inv_arm_ik_flag = side_component_dict[inv_side][1].ik_flag

            weapon_flag = weapon_component.get_flags()[0]
            inv_weapon_flag = side_component_dict[inv_side][2].get_flags()[0]

            prop_flag = prop_component.get_flags()[0]
            inv_prop_flag = side_component_dict[inv_side][3].get_flags()[0]

            tek.MultiConstraint.create(tek_rig,
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

            tek.MultiConstraint.create(tek_rig,
                                        side=side,
                                        region='fk_arm',
                                        source_object=arm_fk_flag,
                                        target_list=[clav_flag,
                                                     spine_sub_flags[1],
                                                     offset_flag,
                                                     cog_flag],
                                        t=False)

            # build target list
            target_list = [weapon_flag,
                           inv_weapon_flag,
                           floor_flag,
                           cog_flag,
                           arm_component.bindJoints.get()[-1]]

            tek.MultiConstraint.create(tek_rig,
                                        side=side,
                                        region='hand_prop',
                                        source_object=prop_flag,
                                        target_list=target_list,
                                        default_name=f'{side[0]}_weapon')

            tek.MultiConstraint.create(tek_rig,
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
            tek_rig.rigTemplate.set(TriadTwinRig.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class MangledRusherRig(base_biped_template.BipedBaseRig):
    VERSION = 1
    ASSET_ID = 'mangledrusher'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        tek_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        neck_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.RFKComponent, side='center', region='neck'))
        neck_end = skel_hierarchy.get_end('neck', 'center')

        if not neck_component:
            return tek_rig

        pelvis_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.PelvisComponent, side='center', region='pelvis'))
        pelvis_start = skel_hierarchy.get_start('pelvis', 'center')

        jaw_start = skel_hierarchy.get_start('jaw', 'center')
        if jaw_start:
            jaw_component = tek.FKComponent.create(tek_rig,
                                                    jaw_start,
                                                    jaw_start,
                                                    side='center',
                                                    region='jaw')
            jaw_component.attach_component(neck_component, neck_end)

        tail_start, tail_end = skel_hierarchy.get_chain('tail', 'center')
        if tail_start:
            tail_component = tek.FKComponent.create(tek_rig,
                                                      tail_start,
                                                      tail_end,
                                                      side='center',
                                                      region=f'cloth')
            tail_component.attach_component(pelvis_component, pelvis_start)

class TriadRig(base_biped_template.BipedBaseRig):
    VERSION = 1
    ASSET_ID = 'triad'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        tek_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        spine_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.RFKComponent, side='center', region='spine'))
        if not spine_component:
            return tek_rig

        world_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.WorldComponent, side='center', region='world'))
        offset_flag = world_component.offset_flag

        floor_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.FKComponent, side='center', region='floor_contact'))
        floor_flag = floor_component.get_end_flag()

        spine_start, spine_end = skel_hierarchy.get_chain('spine', 'center')

        pelvis_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.PelvisComponent, side='center', region='pelvis'))
        pelvis_start = skel_hierarchy.get_start('pelvis', 'center')

        neck_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.RFKComponent, side='center', region='neck'))
        neck_end = skel_hierarchy.get_end('neck', 'center')

        # Triad Mid Joints
        cloth_start, cloth_end = skel_hierarchy.get_chain('cloth', 'center')
        if cloth_start:
            cloth_component = tek.FKComponent.create(tek_rig,
                                                      cloth_start,
                                                      cloth_end,
                                                      side='center',
                                                      region=f'cloth')
            cloth_component.attach_component(pelvis_component, pelvis_start)

        front_cloth_start = skel_hierarchy.get_start('front_cloth', 'center')
        if front_cloth_start:
            front_cloth_component = tek.FKComponent.create(tek_rig,
                                                            front_cloth_start,
                                                            front_cloth_start,
                                                            side='center',
                                                            region=f'front_cloth')
            front_cloth_component.attach_component(pelvis_component, pelvis_start)
            front_cloth_flag = front_cloth_component.get_flags()[0]

            loin_spine_start = skel_hierarchy.get_start('loin_spine', 'center')
            loin_spine_component = tek.FKComponent.create(tek_rig,
                                                           loin_spine_start,
                                                           loin_spine_start,
                                                           side='center',
                                                           region=f'loin_spine')
            loin_spine_component.attach_component(front_cloth_component, front_cloth_start)

            loin_skull_start = skel_hierarchy.get_start('loin_skull', 'center')
            loin_skull_component = tek.FKComponent.create(tek_rig,
                                                           loin_skull_start,
                                                           loin_skull_start,
                                                           side='center',
                                                           region=f'loin_skull')
            loin_skull_component.attach_component(front_cloth_component, front_cloth_start)

        for region in ['jaw', 'jaw_upper', 'jaw_inner']:
            jaw_start = skel_hierarchy.get_start(region, 'center')
            jaw_component = tek.FKComponent.create(tek_rig,
                                                    jaw_start,
                                                    jaw_start,
                                                    side='center',
                                                    region=region,
                                                    constrain_scale=False if region != 'jaw_upper' else True,
                                                    lock_root_translate_axes=attr_utils.TRANSLATION_ATTRS if region != 'jaw_inner' else (),
                                                    lock_root_scale_axes=attr_utils.SCALE_ATTRS if region != 'jaw_inner' else ())
            jaw_component.attach_component(neck_component, neck_end)

        for side in ['left', 'right']:
            # Anchors
            spine_attachment = skel_hierarchy.get_start('anchor', side)
            spine_attachment_component = tek.FKComponent.create(tek_rig,
                                                                 spine_attachment,
                                                                 spine_attachment,
                                                                 side=side,
                                                                 region=f'anchor_{side}')
            spine_attachment_component.attach_component(spine_component, spine_end)

            # Groin Goblin
            if front_cloth_start:
                loin_arm_start, loin_arm_end = skel_hierarchy.get_chain('loin_arm', side)
                loin_arm_component = tek.IKFKComponent.create(tek_rig,
                                                               loin_arm_start,
                                                               loin_arm_end,
                                                               side=side,
                                                               region='loin_arm',
                                                               ik_flag_pv_orient=[-90, 0, 0])
                loin_arm_component.attach_component(front_cloth_component, front_cloth_start)
                ik_flag = loin_arm_component.ik_flag
                ik_switch_flag = loin_arm_component.switch_flag
                pv_flag = loin_arm_component.pv_flag

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='loin_arm',
                                            source_object=ik_flag,
                                            switch_obj=ik_switch_flag,
                                            target_list=[front_cloth_flag, offset_flag])

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='loin_arm_pv',
                                            source_object=pv_flag,
                                            target_list=[front_cloth_flag, offset_flag])

                loin_arm_contact_start = skel_hierarchy.get_start('loin_arm_contact', side)
                loin_arm_contact_component = tek.FKComponent.create(tek_rig,
                                                                     loin_arm_contact_start,
                                                                     loin_arm_contact_start,
                                                                     side=side,
                                                                     region=f'loin_arm_contact')
                loin_arm_contact_component.attach_component(loin_arm_component, loin_arm_end)
                contact_flag = loin_arm_contact_component.get_flags()[0]

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='loin_arm_contact',
                                            source_object=contact_flag,
                                            target_list=[ik_flag, offset_flag, floor_flag])
