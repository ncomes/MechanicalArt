
#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Templates for random props used in Dark Winter
"""

# System global imports
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging import frag
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup
from mca.common.utils import lists

# Internal module imports


class PropTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'fr4o-7ckam-7ob2m-3gyl'
    ASSET_TYPE = 'prop'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(PropTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
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
        hierarchy_markup = chain_markup.ChainMarkup(root)

        world_component = frag.WorldComponent.create(frag_rig,
                                                           root,
                                                           'center',
                                                           'world',
                                                           orientation=[-90, 0, 0])
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag = world_component.offset_flag
        offset_flag.set_as_detail()

        # Cog
        base_joint = hierarchy_markup.get_start('base', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                       base_joint,
                                                       base_joint,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode(offset_flag))

        # Center
        floor_joint = hierarchy_markup.get_start('floor', 'center')
        floor_component = frag.FKComponent.create(frag_rig,
                                                  floor_joint,
                                                  floor_joint,
                                                  side='center',
                                                  region='floor_contact',
                                                  lock_root_translate_axes=[])
        floor_component.attach_component(world_component, pm.PyNode(offset_flag), point=False, orient=False)
        floor_flag = floor_component.get_end_flag()
        floor_flag.set_as_contact()

        if finalize:
            frag_rig.rigTemplate.set(PropTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class TailorTweezersTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'tailor_tweezers'
    ASSET_TYPE = 'prop'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(TailorTweezersTemplate, self).__init__(asset_id, asset_type)

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
        hierarchy_markup = chain_markup.ChainMarkup(root)

        world_component = frag.WorldComponent.create(frag_rig,
                                                           root,
                                                           'center',
                                                           'world',
                                                           orientation=[-90, 0, 0])
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag = world_component.offset_flag
        offset_flag.set_as_detail()

        # Cog
        base_joint = hierarchy_markup.get_start('base', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                       base_joint,
                                                       base_joint,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode(offset_flag))

        for side in ['left', 'right']:
            arm_joint = hierarchy_markup.get_start('arm', side)
            arm_component = frag.FKComponent.create(frag_rig,
                                                          arm_joint,
                                                          arm_joint,
                                                          side,
                                                          'arm',
                                                          lock_root_rotate_axes=['rx', 'ry'])
            arm_component.attach_component(arm_component, base_joint)

class HealingTotemTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'healingtotem'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, 'prop', self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        # Core frag
        # world
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = frag.WorldComponent.create(frag_rig,
                                                           root_joint,
                                                           'center',
                                                           'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag])

        # Cog
        body_start, body_end = skel_hierarchy.get_chain('body', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Body
        body_component = frag.FKComponent.create(frag_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'body',
                                                       lock_root_translate_axes=[])
        body_component.attach_component(cog_component, cog_flag.node)

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

        for part in ['lower_ring', 'mid_ring', 'upper_ring', 'bob']:
            part_joint = skel_hierarchy.get_start(part, 'center')
            if part_joint:
                part_component = frag.FKComponent.create(frag_rig,
                                                               part_joint,
                                                               part_joint,
                                                               'center',
                                                               part,
                                                               lock_root_translate_axes=[])
                part_component.attach_component(body_component, body_start)

        if finalize:
            frag_rig.rigTemplate.set(HealingTotemTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class ProtectingTotemTemplate(HealingTotemTemplate):
    VERSION = 1
    ASSET_ID = 'protectingtotem'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        frag_rig = super().build(finalize=False)
        frag_root = frag_rig.get_root()
        frag_root.asset_id = self.ASSET_ID
        frag_root.assetName.set(self.ASSET_ID)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        lowerring_component = lists.get_first_in_list(frag_rig.get_frag_children(of_type=frag.FKComponent,
                                                         side='center',
                                                         region='lower_ring'))

        lowerring_flag = lowerring_component.get_flags()[0]

        for sc_part in ['shield_front', 'shield_back']:
            sc_start = skel_hierarchy.get_start(sc_part, 'center')
            if sc_start:
                sc_component = frag.FKComponent.create(frag_rig,
                                                               sc_start,
                                                               sc_start,
                                                               'center',
                                                               sc_part,
                                                               lock_root_translate_axes=[])

                sc_component.attach_component(lowerring_component, lowerring_flag.node)

        for side in ['left', 'right']:
            shield_start, shield_end = skel_hierarchy.get_chain('shield', side)
            if shield_start:
                shield_component = frag.FKComponent.create(frag_rig,
                                                           shield_start,
                                                           shield_end,
                                                           side=side,
                                                           region='shield',
                                                           lock_root_translate_axes=[])

                shield_component.attach_component(lowerring_component, lowerring_flag.node)

        if finalize:
            frag_rig.rigTemplate.set(ProtectingTotemTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class ArmatusStoreTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'armatusstore'
    ASSET_TYPE = 'prop'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(ArmatusStoreTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        pm.namespace(set=':')

        root_joint = pm.PyNode('root')
        frag_root = frag.FRAGRoot.create(root_joint, 'prop', self.ASSET_ID)
        frag_root.asset_id = self.ASSET_ID
        frag_root.assetName.set(self.ASSET_ID)
        frag_rig = frag.FRAGRig.create(frag_root)
        skel_mesh = frag.SkeletalMesh.create(frag_root)

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = frag.WorldComponent.create(frag_rig,
                                                     root_joint,
                                                     'center',
                                                     'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])

        # Cog
        body_start, body_end = skel_hierarchy.get_chain('base', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                 body_start,
                                                 body_start,
                                                 'center',
                                                 'cog',
                                                 orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Arm components
        for side in ['left', 'right']:
            arm_joint = skel_hierarchy.get_start('arm', side)
            arm_component = frag.FKComponent.create(frag_rig,
                                                    arm_joint,
                                                    arm_joint,
                                                    side,
                                                    'arm',
                                                    lock_root_translate_axes=[])
            arm_component.attach_component(arm_component, cog_flag.node)

        # Shield components
        for side in ['left', 'right']:
            shield_joint = skel_hierarchy.get_start('shield', side)
            shield_component = frag.FKComponent.create(frag_rig,
                                                    shield_joint,
                                                    shield_joint,
                                                    side,
                                                    'shield',
                                                    lock_root_translate_axes=[])
            shield_component.attach_component(shield_component, cog_flag.node)

        # Ring 01
        ring_01_joint = skel_hierarchy.get_start('ring_01', 'center')
        ring_01_component = frag.FKComponent.create(frag_rig,
                                                ring_01_joint,
                                                ring_01_joint,
                                                'center',
                                                'ring_01',
                                                lock_root_translate_axes=['tx', 'ty', 'tz'])
        ring_01_component.attach_component(ring_01_component, cog_flag.node)

        # Ring 02
        ring_02_joint = skel_hierarchy.get_start('ring_02', 'center')
        ring_02_component = frag.FKComponent.create(frag_rig,
                                                    ring_02_joint,
                                                    ring_02_joint,
                                                    'center',
                                                    'ring_02',
                                                    lock_root_translate_axes=['tx', 'ty', 'tz'])
        ring_02_component.attach_component(ring_02_component, cog_flag.node)

        # Ring 03
        ring_03_joint = skel_hierarchy.get_start('ring_03', 'center')
        ring_03_component = frag.FKComponent.create(frag_rig,
                                                    ring_03_joint,
                                                    ring_03_joint,
                                                    'center',
                                                    'ring_03',
                                                    lock_root_translate_axes=['tx', 'ty', 'tz'])
        ring_03_component.attach_component(ring_03_component, cog_flag.node)

        if finalize:
            frag_rig.rigTemplate.set(ArmatusStoreTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig

class CrawlerArmTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'crawler_arm_left'
    ASSET_TYPE = 'prop'

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(CrawlerArmTemplate, self).__init__(asset_id, asset_type)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        pm.namespace(set=':')

        root_joint = pm.PyNode('root')
        frag_root = frag.FRAGRoot.create(root_joint, 'prop', self.ASSET_ID)
        frag_root.asset_id = self.ASSET_ID
        frag_root.assetName.set(self.ASSET_ID)
        frag_rig = frag.FRAGRig.create(frag_root)
        skel_mesh = frag.SkeletalMesh.create(frag_root)

        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = frag.WorldComponent.create(frag_rig,
                                                     root_joint,
                                                     'center',
                                                     'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='root',
                                    source_object=root_flag,
                                    target_list=[world_flag,
                                                 offset_flag])

        # Cog
        cog_component = frag.CogComponent.create(frag_rig,
                                                 root_joint,
                                                 root_joint,
                                                 'center',
                                                 'cog',
                                                 orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Arm components
        leaf_joint_list = list(sorted(x for x in pm.ls(type='joint') if x.hasAttr('chainStart') and 'leaf' in x.chainStart.get()))

        arm_joint = skel_hierarchy.get_chain('arm', 'left')
        end_helper = skel_hierarchy.get_chain('arm_end', 'left')[0]
        mid_helper = skel_hierarchy.get_chain('arm_mid', 'left')[0]
        start_helper = skel_hierarchy.get_chain('arm_start', 'left')[0]
        arm_component = frag.SplineIKComponent.create(frag_rig,
                                                      arm_joint[0],
                                                      arm_joint[-1],
                                                      leaf_joint_list,
                                                      end_helper,
                                                      mid_helper,
                                                      'left',
                                                      'arm',
                                                      start_helper_joint=start_helper)
        arm_component.attach_component([cog_component], [cog_flag.node])
        aux_flag = arm_component.get_flags()[1]
        aux_flag.set_as_detail()



        for x in range(1,7):
            manual_twist_joint = pm.PyNode(f'arm_tentacle_leaf_0{x}_l')

            manual_twist_component = frag.FKComponent.create(frag_rig,
                                                             manual_twist_joint,
                                                             manual_twist_joint,
                                                             'left',
                                                             f'arm_leaf_0{x}',
                                                             lock_root_rotate_axes=['rz', 'ry'])

            manual_twist_component.attach_component([arm_component], [pm.PyNode(f'arm_tentacle_0{x}_l')])
            twist_flag = manual_twist_component.get_flags()[0]

            if x == 1:
                twist_flag.set_as_detail()
            elif x == 6:
                twist_flag.set_as_detail()
                hand_joint = skel_hierarchy.get_start('hand', 'left')
                hand_component = frag.FKComponent.create(frag_rig,
                                                         hand_joint,
                                                         hand_joint,
                                                         'left',
                                                         'hand')
                hand_component.attach_component([arm_component], [pm.PyNode('arm_tentacle_06_l')])

                # Shield components
                for finger in ['thumb', 'index_finger', 'pinky_finger', 'ring_finger', 'middle_finger']:
                    finger_joint = skel_hierarchy.get_chain(finger, 'left')
                    finger_component = frag.FKComponent.create(frag_rig,
                                                               finger_joint[0],
                                                               finger_joint[-1],
                                                               'left',
                                                               finger)
                    finger_component.attach_component([hand_component], [hand_joint])

        if finalize:
            frag_rig.rigTemplate.set(CrawlerArmTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig


class ShieldGoliathTotemTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'h715-2ue8l-441jf-hvjn'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')

        frag_root = frag.FRAGRoot.create(root_joint, 'prop', self.asset_id)
        skel_mesh = frag.SkeletalMesh.create(frag_root)
        frag_rig = frag.FRAGRig.create(frag_root)

        # Core frag
        # world
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)

        world_component = frag.WorldComponent.create(frag_rig,
                                                           root_joint,
                                                           'center',
                                                           'world')
        world_flag = world_component.get_flags()[0]
        root_flag = world_component.root_flag
        offset_flag = world_component.offset_flag
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Root Multiconstraint
        frag.MultiConstraint.create(frag_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag])

        # Cog
        body_start, body_end = skel_hierarchy.get_chain('body', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Body
        body_component = frag.FKComponent.create(frag_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'body',
                                                       lock_root_translate_axes=[])
        body_component.attach_component(cog_component, cog_flag.node)

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

        for part in ['base_ring', 'lower_ring', 'mid_ring', 'upper_ring', 'end_ring']:
            part_joint = skel_hierarchy.get_start(part, 'center')
            if part_joint:
                part_component = frag.FKComponent.create(frag_rig,
                                                               part_joint,
                                                               part_joint,
                                                               'center',
                                                               part,
                                                               lock_root_translate_axes=[])
                part_component.attach_component(body_component, body_start)

        if finalize:
            frag_rig.rigTemplate.set(HealingTotemTemplate.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig