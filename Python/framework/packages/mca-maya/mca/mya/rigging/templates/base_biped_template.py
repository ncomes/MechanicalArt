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


class BipedBaseRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'BaseBiped'

    def __init__(self, asset_id=ASSET_ID):
        self.ASSET_ID = asset_id
        super().__init__(self.ASSET_ID)

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
            component_dict = {}
            side_component_dict[side] = component_dict
            # Clav
            clav_start, clav_end = skel_hierarchy.get_chain('clav', side)
            if clav_start:
                clav_component = tek.FKComponent.create(tek_rig,
                                                         clav_start,
                                                         clav_end,
                                                         side=side,
                                                         region='clav',
                                                         lock_root_translate_axes=['v'])
                clav_component.attach_component(spine_component, spine_end)
                clav_flag = clav_component.get_flags()[0]
                component_dict['clav'] = clav_component

                # IKFK arm
                arm_start, arm_end = skel_hierarchy.get_chain('arm', side)
                arm_component = tek.IKFKComponent.create(tek_rig,
                                                          arm_start,
                                                          arm_end,
                                                          side=side,
                                                          region='arm',
                                                          ik_flag_pv_orient=[-90, 0, 0])
                arm_component.attach_component(clav_component, clav_start)
                component_dict['arm'] = arm_component

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='arm_pv',
                                            source_object=arm_component.pv_flag,
                                            target_list=[offset_flag, clav_flag, spine_sub_flags[1], cog_flag])

                for finger in ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinky_finger']:
                    # Finger
                    finger_start, finger_end = skel_hierarchy.get_chain(finger, side)
                    finger_component = tek.FKComponent.create(tek_rig,
                                                               finger_start,
                                                               finger_end,
                                                               side=side,
                                                               region=finger,
                                                               lock_child_rotate_axes=['rx', 'ry'],
                                                               scale=0.1)
                    finger_component.attach_component(arm_component, arm_end)
                    first_knuckle_flag = finger_component.get_flags()[1]
                    attr_utils.set_attr_state(first_knuckle_flag.node, locked=False, attr_list=attr_utils.ROTATION_ATTRS, visibility=True)


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
                component_dict['prop'] = prop_component
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
                component_dict['weapon'] = weapon_component
                weapon_flag = weapon_component.get_flags()[0]
                weapon_flag.set_as_sub()

            ###
            # Leg build
            ###
            # Leg
            leg_start, *mid_joints, leg_end = skel_hierarchy.get_full_chain('leg', side)
            if leg_start:
                if len(mid_joints) == 2:
                    # Standard 4 joint chain
                    leg_component = tek.ReverseFootComponent.create(tek_rig,
                                                                     leg_start,
                                                                     leg_end,
                                                                     side=side,
                                                                     region='leg',
                                                                     ik_flag_pv_orient=[-90, 0, 0])
                else:
                    leg_component = tek.ZLegComponent.create(tek_rig,
                                                              leg_start,
                                                              leg_end,
                                                              side=side,
                                                              region='leg',
                                                              ik_flag_pv_orient=[-90, 0, 0])
                leg_component.attach_component(pelvis_component, pelvis_start)
                component_dict['leg'] = leg_component
                leg_ik_flag = leg_component.ik_flag
                leg_switch_flag = leg_component.switch_flag

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='ik_leg',
                                            source_object=leg_ik_flag,
                                            target_list=[offset_flag, pelvis_flag, cog_flag],
                                            switch_obj=leg_switch_flag)

                tek.MultiConstraint.create(tek_rig,
                                            side='left',
                                            region='leg_pv',
                                            source_object=leg_component.pv_flag,
                                            target_list=[offset_flag, leg_ik_flag, pelvis_flag, cog_flag])

                # Contact
                foot_contact = skel_hierarchy.get_start('foot_contact', side)
                foot_contact_component = tek.FKComponent.create(tek_rig,
                                                                 foot_contact,
                                                                 foot_contact,
                                                                 side=side,
                                                                 region='foot_contact',
                                                                 lock_root_translate_axes=[])
                foot_contact_component.attach_component(floor_component, floor_joint)
                foot_contact_flag = foot_contact_component.get_end_flag()
                foot_contact_flag.set_as_contact()

                # Contact Multiconstraint
                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='foot_contact',
                                            source_object=foot_contact_flag,
                                            target_list=[floor_flag,
                                                         mid_joints[-1]])

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
        pelvis_contact_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        pelvis_contact_flag = pelvis_contact_component.get_end_flag()
        pelvis_contact_flag.set_as_contact()

        tek.MultiConstraint.create(tek_rig,
                                    side='center',
                                    region='pelvis_contact',
                                    source_object=pelvis_contact_flag,
                                    target_list=[floor_flag,
                                                 offset_flag])

        # Multi Constraints
        for side in ['left', 'right']:
            # Arm Multi constraint
            inv_side = 'left' if side == 'right' else 'right'

            clav_component = side_component_dict[side].get('clav')
            arm_component = side_component_dict[side].get('arm')
            weapon_component = side_component_dict[side].get('weapon')
            prop_component = side_component_dict[side].get('prop')
            leg_component = side_component_dict[side].get('leg')

            if arm_component:
                arm_ik_flag = arm_component.ik_flag
                arm_switch_flag = arm_component.switch_flag
                arm_fk_flag = arm_component.fk_flags[0]

                ik_arm_target_list = [offset_flag]
                fk_arm_target_list = []
                prop_target_list = []
                weapon_target_list = [arm_component.bindJoints.get()[-1]]

                if clav_component:
                    clav_flag = clav_component.get_flags()[0]
                    ik_arm_target_list.append(clav_flag)
                    fk_arm_target_list.append(clav_flag)

                inv_arm_component = side_component_dict[inv_side].get('arm')
                if inv_arm_component:
                    ik_arm_target_list.append(inv_arm_component.ik_flag)

                prop_flag = None
                if prop_component:
                    weapon_target_list.append(prop_component.get_flags()[0])
                    inv_prop_flag = side_component_dict[inv_side].get('prop')
                    if inv_prop_flag:
                        weapon_target_list.append(inv_prop_flag.get_flags()[0])

                weapon_flag = None
                if weapon_component:
                    weapon_flag = weapon_component.get_flags()[0]
                    prop_target_list.append(weapon_flag)
                    inv_weapon_component = side_component_dict[inv_side].get('weapon')
                    if inv_weapon_component:
                        inv_weapon_flag = inv_weapon_component.get_flags()[0]
                        prop_target_list.append(inv_weapon_flag)
                        weapon_target_list.append(inv_weapon_flag)

                weapon_target_list.append(head_flag)

                ik_arm_target_list.append(spine_sub_flags[1])
                fk_arm_target_list.append(spine_sub_flags[1])

                ik_arm_target_list.append(floor_flag)
                prop_target_list.append(floor_flag)
                weapon_target_list.append(floor_flag)

                fk_arm_target_list.append(offset_flag)
                weapon_target_list.append(offset_flag)

                ik_arm_target_list.append(cog_flag)
                fk_arm_target_list.append(cog_flag)
                prop_target_list.append(cog_flag)
                weapon_target_list.append(cog_flag)

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='ik_arm',
                                            source_object=arm_ik_flag,
                                            target_list=ik_arm_target_list,
                                            switch_obj=arm_switch_flag, )

                tek.MultiConstraint.create(tek_rig,
                                            side=side,
                                            region='fk_arm',
                                            source_object=arm_fk_flag,
                                            target_list=fk_arm_target_list,
                                            t=False)



                # build target list with optional leg targets.
                if leg_component:
                    prop_target_list.append(leg_component.bindJoints.get()[0])
                    inv_leg_component = side_component_dict[inv_side].get('leg')
                    if inv_leg_component:
                        prop_target_list.append(inv_leg_component.bindJoints.get()[0])
                prop_target_list.append(arm_component.bindJoints.get()[-1])

                if prop_flag:
                    tek.MultiConstraint.create(tek_rig,
                                                side=side,
                                                region='hand_prop',
                                                source_object=prop_flag,
                                                target_list=prop_target_list,
                                                default_name=f'{side[0]}_hand')

                if weapon_flag:
                    tek.MultiConstraint.create(tek_rig,
                                                side=side,
                                                region='weapon',
                                                source_object=weapon_flag,
                                                target_list=weapon_target_list,
                                                default_name=f'{side[0]}_weapon')

        if finalize:
            tek_rig.rigTemplate.set(BipedBaseRig.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class TheWarriorTemplate(BipedBaseRig):
    VERSION = 1
    ASSET_ID = 'thewarrior'

    def __init__(self, asset_id=ASSET_ID):
        super(TheWarriorTemplate, self).__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')

        tek_rig = super(TheWarriorTemplate, self).build()
        root_component = tek_rig.get_tek_parent()
        spine_component = tek_rig.get_tek_children(of_type=tek.RFKComponent, region='spine')[0]

        root = root_component.root_joint
        chain = chain_markup.ChainMarkup(root)

        back_cloak_l = chain.get_chain('cloak', 'left')
        back_cloak_l_component = tek.FKComponent.create(tek_rig,
                                                         back_cloak_l[0],
                                                         back_cloak_l[-1],
                                                         side='left',
                                                         region='cloak',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        back_cloak_l_component.attach_component(spine_component, [pm.PyNode('spine_04')])

        back_cloak_r = chain.get_chain('cloak', 'right')
        back_cloak_r_component = tek.FKComponent.create(tek_rig,
                                                         back_cloak_r[0],
                                                         back_cloak_r[-1],
                                                         side='right',
                                                         region='cloak',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        back_cloak_r_component.attach_component(spine_component, [pm.PyNode('spine_04')])

        back_cloak_c = chain.get_chain('cloak', 'center')
        back_cloak_c_component = tek.FKComponent.create(tek_rig,
                                                         back_cloak_c[0],
                                                         back_cloak_c[-1],
                                                         side='right',
                                                         region='cloak',
                                                         scale=0.1,
                                                         lock_root_translate_axes=[],
                                                         lock_child_translate_axes=[])
        back_cloak_c_component.attach_component(spine_component, [pm.PyNode('spine_04')])

        if finalize:
            tek_rig.rigTemplate.set(TheWarriorTemplate.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig
