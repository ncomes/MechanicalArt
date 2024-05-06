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


class SapperLeechRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'sapperleech'

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
        pelvis_start, pelvis_end = skel_hierarchy.get_chain('body', 'center')
        cog_component = frag.CogComponent.create(frag_rig,
                                                 pelvis_start,
                                                 pelvis_start,
                                                 'center',
                                                 'cog',
                                                 orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, pm.PyNode(offset_flag))
        cog_flag = cog_component.get_flags()[0]

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

        ###
        # Center Components
        ###
        # Pelvis
        pelvis_component = frag.PelvisComponent.create(frag_rig,
                                                       pelvis_start,
                                                       pelvis_end,
                                                       'center',
                                                       'body',
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

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='spine_mid_bottom',
                                    source_object=spine_component.mid_flags[0],
                                    target_list=[spine_component.mid_offset_groups[0],
                                                 spine_component.start_flag,
                                                 cog_flag],
                                    translate=False,
                                    default_name='default')

        # Tongue Spline
        tongue_start, tongue_end = skel_hierarchy.get_chain('tongue', 'center')
        start_helper_joint = skel_hierarchy.get_start('tongue_start', 'center')
        mid_helper_joint = skel_hierarchy.get_start('tongue_helper', 'center')
        end_helper_joint = skel_hierarchy.get_start('tongue_end', 'center')
        tongue_component = frag.SplineIKComponent.create(frag_rig,
                                                         tongue_start,
                                                         tongue_end,
                                                         end_helper_joint,
                                                         mid_helper_joint,
                                                         start_helper_joint=start_helper_joint,
                                                         side='center',
                                                         region='tongue')
        tongue_component.attach_component(spine_component, tongue_start.getParent())
        tongue_flags = tongue_component.get_flags()

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='tongue',
                                    source_object=tongue_flags[2],
                                    target_list=[tongue_flags[0], offset_flag])

        frag.MultiConstraint.create(frag_rig,
                                    side='center',
                                    region='tongue_mid',
                                    source_object=tongue_flags[-1],
                                    target_list=[tongue_flags[0], offset_flag])

        for side in ['left', 'right']:
            for tentacle_name in ['tentacle_upper', 'tentacle_lower']:
                start_joint, end_joint = skel_hierarchy.get_chain(tentacle_name, side)
                tentacle_component = frag.FKComponent.create(frag_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side=side,
                                                        region=tentacle_name)
                tentacle_component.attach_component(tongue_component, start_joint.getParent())

            arm_component_dict = {}
            for arm_name in ['arm', 'arm_back', 'arm_front', 'arm_back_mid', 'arm_body_front', 'arm_body', 'arm_head_front']:
                start_joint, end_joint = skel_hierarchy.get_chain(arm_name, side)
                if start_joint:
                    arm_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side=side,
                                                            region=arm_name,
                                                            lock_root_rotate_axes=['rx', 'ry'])
                    arm_component.attach_component(spine_component, start_joint.getParent())
                    arm_component_dict[end_joint] = arm_component

            for hand_name in ['hand_head_back', 'hand_head_front', 'hand_back', 'hand_front', 'hand_back_mid', 'hand_front_mid', 'hand_body_front', 'hand_body', 'hand']:
                start_joint = skel_hierarchy.get_start(hand_name, side)
                if start_joint:
                    hand_component = frag.FKComponent.create(frag_rig,
                                                             start_joint,
                                                             start_joint,
                                                             side=side,
                                                             region=hand_name)
                    hand_component.attach_component(arm_component_dict[start_joint] if start_joint in arm_component_dict else spine_component, start_joint.getParent())
                    arm_component_dict[start_joint] = hand_component
                
                for sub_name in ['index', 'thumb', 'mitten']:
                    search_name = hand_name.replace('hand', sub_name)
                    start_joint = skel_hierarchy.get_start(search_name, side)
                    if start_joint:
                        sub_component = frag.FKComponent.create(frag_rig,
                                                                start_joint,
                                                                start_joint,
                                                                side=side,
                                                                region=search_name)
                        sub_component.attach_component(arm_component_dict[start_joint] if start_joint in arm_component_dict else spine_component, start_joint.getParent())

            for foot_name in ['foot', 'foot_front']:
                start_joint, end_joint = skel_hierarchy.get_chain(foot_name, side)
                if start_joint:
                    sub_component = frag.FKComponent.create(frag_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side=side,
                                                            region=foot_name)
                    sub_component.attach_component(spine_component, start_joint.getParent())

        if finalize:
            frag_rig.rigTemplate.set(SapperLeechRig.__name__)
            frag_rig.finalize_rig(self.get_flags_path())

        return frag_rig
