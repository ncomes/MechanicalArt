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

from mca.mya.rigging import chain_markup, frag
from mca.mya.utils import attr_utils

from mca.mya.rigging.templates import rig_templates


class GargoyleBaseRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'nightstalker'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, 'combatant', self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        flags_all = frag_rig.flagsAll.get()

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
                                                 spine_component.mid_flags[1],
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='spine_mid_top',
                                    source_object=spine_component.mid_flags[1],
                                    target_list=[spine_component.mid_offset_groups[1],
                                                 spine_component.mid_flags[0],
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        frag.MultiConstraint.create(frag_rig,
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
        neck_component = frag.RFKComponent.create(frag_rig,
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

        frag.MultiConstraint.create(frag_rig,
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
            jaw_component = frag.FKComponent.create(frag_rig,
                                                    jaw_joint,
                                                    jaw_joint,
                                                    side='center',
                                                    region='jaw',
                                                    lock_root_translate_axes=[])
            jaw_component.attach_component(world_component, neck_end)

        # Center
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

        # Split Sides
        side_component_dict = {}
        for side in ['left', 'right']:
            ###
            # Arm Build
            ###

            # Clav
            clav_start, clav_end = skel_hierarchy.get_chain('clav', side)
            clav_component = frag.FKComponent.create(frag_rig,
                                                     clav_start,
                                                     clav_end,
                                                     side=side,
                                                     region='clav',
                                                     lock_root_translate_axes=['v'])
            clav_component.attach_component(spine_component, spine_end)
            clav_flag = clav_component.get_flags()[0]

            # IKFK arm
            arm_start, arm_end = skel_hierarchy.get_chain('arm', side)
            arm_component = frag.IKFKComponent.create(frag_rig,
                                                      arm_start,
                                                      arm_end,
                                                      side=side,
                                                      region='arm',
                                                      ik_flag_pv_orient=[-90, 0, 0])
            arm_component.attach_component(clav_component, clav_start)

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='arm_pv',
                                        source_object=arm_component.pv_flag,
                                        target_list=[offset_flag, clav_flag, spine_sub_flags[1], cog_flag])

            for finger in ['thumb', 'index_finger', 'middle_finger', 'ring_finger', 'pinky_finger']:
                # Finger
                finger_start, finger_end = skel_hierarchy.get_chain(finger, side)
                finger_component = frag.FKComponent.create(frag_rig,
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
            prop_component = frag.FKComponent.create(frag_rig,
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
            weapon_component = frag.FKComponent.create(frag_rig,
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
            # Leg build
            ###
            # Leg
            leg_start, leg_end = skel_hierarchy.get_chain('leg', side)
            if leg_start:
                leg_component = frag.ZLegComponent.create(frag_rig,
                                                          leg_start,
                                                          leg_end,
                                                          side=side,
                                                          region='leg',
                                                          ik_flag_pv_orient=[-90, 0, 0])
                leg_component.attach_component(pelvis_component, pelvis_start)
                leg_ik_flag = leg_component.ik_flag
                leg_switch_flag = leg_component.switch_flag

                frag.MultiConstraint.create(frag_rig,
                                            side=side,
                                            region='ik_leg',
                                            source_object=leg_ik_flag,
                                            target_list=[offset_flag, pelvis_flag, cog_flag],
                                            switch_obj=leg_switch_flag)

                frag.MultiConstraint.create(frag_rig,
                                            side='left',
                                            region='leg_pv',
                                            source_object=leg_component.pv_flag,
                                            target_list=[offset_flag, leg_ik_flag, cog_flag])

                # Contact
                foot_contact = skel_hierarchy.get_start('foot_contact', side)
                foot_contact_component = frag.FKComponent.create(frag_rig,
                                                                 foot_contact,
                                                                 foot_contact,
                                                                 side=side,
                                                                 region='foot_contact',
                                                                 lock_root_translate_axes=[])
                foot_contact_component.attach_component(floor_component, floor_joint)
                foot_contact_flag = foot_contact_component.get_end_flag()
                foot_contact_flag.set_as_contact()

                # Contact Multiconstraint
                frag.MultiConstraint.create(frag_rig,
                                            side=side,
                                            region='foot_contact',
                                            source_object=foot_contact_flag,
                                            target_list=[floor_flag,
                                                         leg_switch_flag])

                side_component_dict[side].append(leg_component)
            else:
                'failed to find legs'
                side_component_dict[side].append(None)

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

        # Pelvis
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

        # Multi Constraints
        for side in ['left', 'right']:
            # Arm Multi constraint
            inv_side = 'left' if side == 'right' else 'right'

            clav_component, arm_component, weapon_component, prop_component, leg_component = side_component_dict[side]
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
                           cog_flag]
            if leg_component:
                target_list.append(leg_component.bindJoints.get()[0])
                target_list.append(side_component_dict[inv_side][4].bindJoints.get()[0])
            target_list.append(arm_component.bindJoints.get()[-1])

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
            frag_rig.rigTemplate.set(GargoyleBaseRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class GargoyleWingedRig(GargoyleBaseRig):
    VERSION = 1
    ASSET_ID = 'chaoscaster'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        spine_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.RFKComponent, side='center', region='spine'))
        if not spine_component:
            return frag_rig

        world_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.WorldComponent, side='center', region='world'))
        offset_flag = world_component.offset_flag

        cog_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.CogComponent, side='center', region='cog'))
        cog_flag = cog_component.get_flags()[0]

        floor_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.FKComponent, side='center', region='floor_contact'))
        floor_flag = floor_component.get_end_flag()

        spine_start, spine_end = skel_hierarchy.get_chain('spine', 'center')
        spine_sub_flags = spine_component.sub_flags

        for side in ['left', 'right']:
            # Clav
            clav_start, clav_end = skel_hierarchy.get_chain('clav_wing', side)
            clav_component = frag.FKComponent.create(frag_rig,
                                                     clav_start,
                                                     clav_end,
                                                     side=side,
                                                     region='clav_wing',
                                                     lock_root_translate_axes=['v'])
            clav_component.attach_component(spine_component, spine_end)
            clav_flag = clav_component.get_flags()[0]

            # IKFK wing
            wing_start, wing_end = skel_hierarchy.get_chain('wing', side)
            wing_component = frag.IKFKComponent.create(frag_rig,
                                                       wing_start,
                                                       wing_end,
                                                       side=side,
                                                       region='wing',
                                                       ik_flag_pv_orient=[-90, 0, 0])
            wing_component.attach_component(clav_component, clav_start)
            wing_ik_flag = wing_component.ik_flag
            wing_switch_flag = wing_component.switch_flag
            wing_fk_flag = wing_component.fk_flags[0]

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='wing_pv',
                                        source_object=wing_component.pv_flag,
                                        target_list=[offset_flag, clav_flag, spine_sub_flags[1], cog_flag])

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='ik_wing',
                                        source_object=wing_ik_flag,
                                        target_list=[offset_flag,
                                                     clav_flag,
                                                     cog_flag,
                                                     spine_sub_flags[1],
                                                     floor_flag],
                                        switch_obj=wing_switch_flag)

            frag.MultiConstraint.create(frag_rig,
                                        side=side,
                                        region='fk_wing',
                                        source_object=wing_fk_flag,
                                        target_list=[clav_flag,
                                                     spine_sub_flags[1],
                                                     offset_flag,
                                                     cog_flag],
                                        t=False)

            finger_list =['wing_index', 'wing_middle', 'wing_ring', 'wing_pinky', 'wing_thumb']
            for index, finger in enumerate(finger_list):
                # Finger
                finger_start, finger_end = skel_hierarchy.get_chain(finger, side)
                if not finger_start:
                    continue
                finger_mid = finger_end.getParent()
                finger_component = frag.FKComponent.create(frag_rig,
                                                           finger_start,
                                                           finger_end,
                                                           side=side,
                                                           region=finger,
                                                           lock_child_rotate_axes=[],
                                                           scale=0.1)
                finger_component.attach_component(wing_component, wing_end)

                float_joint = skel_hierarchy.get_start(f'{finger}_float', side)
                if not float_joint:
                    continue
                next_finger_end = skel_hierarchy.get_end(finger_list[index+1], side)
                next_finger_mid = next_finger_end.getParent()
                float_component = frag.FKComponent.create(frag_rig,
                                                          float_joint,
                                                          float_joint,
                                                          side=side,
                                                          region=f'{finger}_float',
                                                          lock_root_translate_axes=[],
                                                          scale=0.1)
                float_component.attach_component(wing_component, [finger_mid, next_finger_mid] if finger != 'wing_pinky' else [finger_mid, wing_end.getParent()])

        if finalize:
            frag_rig.rigTemplate.set(GargoyleWingedRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class HornedChargerRig(GargoyleWingedRig):
    VERSION = 1
    ASSET_ID = 'hornedcharger'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = lists.get_first_in_list(
            frag_rig.get_frag_children(of_type=frag.WorldComponent, side='center', region='world'))
        world_flag = world_component.world_flag

        pelvis_start = skel_hierarchy.get_start('pelvis', 'center')
        pelvis_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.PelvisComponent, side='center', region='pelvis'))

        tail_start, tail_end = skel_hierarchy.get_chain('tail', 'center')
        tail_component = frag.IKFKComponent.create(frag_rig,
                                                  tail_start,
                                                  tail_end,
                                                  side='center',
                                                  region='tail',
                                                  ik_flag_pv_orient=[-90, 0, 0])
        tail_component.attach_component(pelvis_component, pelvis_start)

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='arm_pv',
                                    source_object=tail_component.pv_flag,
                                    target_list=[pelvis_start, world_flag])

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='arm_ik',
                                    source_object=tail_component.ik_flag,
                                    target_list=[pelvis_start, world_flag])

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='arm_fk',
                                    source_object=tail_component.fk_flags[0],
                                    target_list=[pelvis_start, world_flag])

        if finalize:
            frag_rig.rigTemplate.set(HornedChargerRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class SpinyFiendRig(HornedChargerRig):
    VERSION = 1
    ASSET_ID = 'spinyfiend'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)
        for side in ['left', 'right']:
            _, arm_mid, _ = skel_hierarchy.get_full_chain('arm', side)
            arm_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.IKFKComponent, side=side, region='arm'))

            spike_start = skel_hierarchy.get_start('spike', side)
            spike_component = frag.FKComponent.create(frag_rig,
                                                      spike_start,
                                                      spike_start,
                                                      side=side,
                                                      region='spike',
                                                      lock_root_translate_axes=[],
                                                      lock_root_scale_axes=[],
                                                      constrain_scale=True,
                                                      scale=0.1)
            spike_component.attach_component(arm_component, arm_mid)

        if finalize:
            frag_rig.rigTemplate.set(SpinyFiendRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class GargoyleTailedRig(GargoyleWingedRig):
    VERSION = 1
    ASSET_ID = 'gargoyle'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = lists.get_first_in_list(
            frag_rig.get_frag_children(of_type=frag.WorldComponent, side='center', region='world'))
        world_flag = world_component.world_flag

        pelvis_start = skel_hierarchy.get_start('pelvis', 'center')
        pelvis_component = lists.get_first_in_list(
            frag_rig.get_frag_children(of_type=frag.PelvisComponent, side='center', region='pelvis'))
        pelvis_flag = pelvis_component.get_flags()[0]

        start_tail, end_tail = skel_hierarchy.get_chain('tail', 'center')
        tail_component = frag.IKFKRibbonComponent.create(frag_rig,
                                                         start_tail,
                                                         end_tail,
                                                         side='center',
                                                         region='tail')
        tail_component.attach_component(pelvis_component, pelvis_start)
        tail_fk_flag = tail_component.fk_flags[0]
        tail_ik_flag = tail_component.ik_flag
        tail_ik_pv_flag = tail_component.pv_flag

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='fk_tail',
                                    source_object=tail_fk_flag,
                                    target_list=[pelvis_flag,
                                                 world_flag],
                                    t=False)

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='ik_tail',
                                    source_object=tail_ik_flag,
                                    target_list=[pelvis_flag,
                                                 world_flag])

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='fk_pv_tail',
                                    source_object=tail_ik_pv_flag,
                                    target_list=[pelvis_flag,
                                                 world_flag])

        if finalize:
            frag_rig.rigTemplate.set(GargoyleTailedRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class AngraRig(GargoyleBaseRig):
    VERSION = 1
    ASSET_ID = 'angra'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        spine_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.RFKComponent, side='center', region='spine'))
        if not spine_component:
            return frag_rig
        spine_start, spine_end = skel_hierarchy.get_chain('spine', 'center')
        spine_end_flag = spine_component.end_flag

        pelvis_start = skel_hierarchy.get_start('pelvis', 'center')
        pelvis_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.PelvisComponent, side='center', region='pelvis'))

        world_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.WorldComponent, side='center', region='world'))
        world_flag = world_component.world_flag

        cog_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.CogComponent, side='center', region='cog'))
        cog_flag = cog_component.get_flags()[0]

        for side in ['left', 'right']:
            for pelvis_tentacle in ['tentacle_front', 'tentacle_front_outer', 'tentacle_back_outer', 'tentacle_back']:
                start_tentacle, end_tentacle = skel_hierarchy.get_chain(pelvis_tentacle, side)
                tentacle_component = frag.SplineIKRibbonComponent.create(frag_rig,
                                                                         start_tentacle,
                                                                         end_tentacle,
                                                                         side=side,
                                                                         region=pelvis_tentacle)
                tentacle_component.attach_component(pelvis_component, pelvis_start)

            start_tentacle, end_tentacle = skel_hierarchy.get_chain('tentacle_shoulder', side)
            tentacle_component = frag.SplineIKRibbonComponent.create(frag_rig,
                                                                     start_tentacle,
                                                                     end_tentacle,
                                                                     side=side,
                                                                     region='tentacle_shoulder')
            tentacle_component.attach_component(spine_component, spine_end)

            for spine_04_tentacle in ['tentacle_prime_upper', 'tentacle_prime_lower', 'tentacle_prime_center']:
                start_tentacle, end_tentacle = skel_hierarchy.get_chain(spine_04_tentacle, side)
                tentacle_component = frag.SplineIKRibbonComponent.create(frag_rig,
                                                                         start_tentacle,
                                                                         end_tentacle,
                                                                         side=side,
                                                                         region=spine_04_tentacle)
                tentacle_component.attach_component(spine_component, spine_end)
                for index, primary_flag in enumerate(tentacle_component.primary_flags[1:]):
                    frag.MultiConstraint.create(frag_rig,
                                                side=side,
                                                region=f'spine_04_tentacle_{index}',
                                                source_object=primary_flag,
                                                target_list=[world_flag,
                                                             cog_flag,
                                                             spine_end_flag])

        if finalize:
            frag_rig.rigTemplate.set(AngraRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class AngraTentacleBurrowRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'angratentacleburrow'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, 'combatant', self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        flags_all = frag_rig.flagsAll.get()

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

        tentacle_start, tentacle_end = skel_hierarchy.get_chain('tentacle', 'center')
        start_helper_joint = skel_hierarchy.get_chain('tentacle_start', 'center')[0]
        mid_helper_joint = skel_hierarchy.get_chain('tentacle_helper', 'center')[0]
        end_helper_joint = skel_hierarchy.get_chain('tentacle_end', 'center')[0]
        tentacle_component = frag.SplineIKComponent.create(frag_rig,
                                                           tentacle_start,
                                                           tentacle_end,
                                                           end_helper_joint,
                                                           mid_helper_joint,
                                                           start_helper_joint=start_helper_joint,
                                                           side='center',
                                                           region='tentacle')
        tentacle_component.attach_component(cog_component, cog_flag)
