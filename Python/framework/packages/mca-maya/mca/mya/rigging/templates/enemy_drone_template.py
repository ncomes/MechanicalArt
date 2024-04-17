#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates the Drone Rig.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging import chain_markup
from mca.mya.rigging import tek
from mca.common.utils import lists


class DroneAngraRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'drone_angra'

    def __init__(self, asset_id=ASSET_ID):
        super(DroneAngraRig, self).__init__(asset_id)

    def build(self, asset_type='combatant'):

        pm.namespace(set=':')
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        flags_all = tek_rig.flagsAll.get()

        # world
        start_joint = pm.PyNode('root')
        world_component = tek.WorldComponent.create(tek_rig,
                                                          start_joint,
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
                                                       offset_flag],
                                          switch_attr='follow')

        # Body
        start_joint = pm.PyNode('body')
        end_joint = pm.PyNode('body')
        body_component = tek.FKComponent.create(tek_rig,
                                                      start_joint,
                                                      end_joint,
                                                      side='center',
                                                      region='body',
                                                      lock_root_translate_axes=['v'])
        body_component.attach_component(world_component, pm.PyNode('root'))
        body_flag = body_component.get_flags()[0]

        # Yaw Pivot
        start_joint = pm.PyNode('yaw_pivot')
        end_joint = pm.PyNode('yaw_pivot')
        yaw_component = tek.FKComponent.create(tek_rig,
                                                     start_joint,
                                                     end_joint,
                                                     side='center',
                                                     region='yaw',
                                                     lock_root_translate_axes=['tx', 'ty', 'tz', 'ry', 'rz', 'v'])
        yaw_component.attach_component(body_component, pm.PyNode('body'))
        yaw_flag = yaw_component.get_flags()[0]

        # pitch Pivot
        start_joint = pm.PyNode('pitch_pivot')
        end_joint = pm.PyNode('pitch_pivot')
        pitch_component = tek.FKComponent.create(tek_rig,
                                                       start_joint,
                                                       end_joint,
                                                       side='center',
                                                       region='pitch',
                                                       lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        pitch_component.attach_component(yaw_component, pm.PyNode('yaw_pivot'))
        pitch_flag = pitch_component.get_flags()[0]
        pitch_flag.set_as_sub()

        # shields
        start_joint = pm.PyNode('shield_c')
        end_joint = pm.PyNode('shield_c')
        shield_component = tek.FKComponent.create(tek_rig,
                                                        start_joint,
                                                        end_joint,
                                                        side='center',
                                                        region='shield',
                                                        lock_root_translate_axes=['v'])
        shield_component.attach_component(body_component, pm.PyNode('body'))
        shield_flag = shield_component.get_flags()[0]
        shield_flag.set_as_sub()

        # Left
        start_joint = pm.PyNode('shield_l')
        end_joint = pm.PyNode('shield_l')
        shield_l_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='left',
                                                          region='shield',
                                                          lock_root_translate_axes=['v'])
        shield_l_component.attach_component(shield_component, pm.PyNode('shield_c'))

        # Right
        start_joint = pm.PyNode('shield_r')
        end_joint = pm.PyNode('shield_r')
        shield_r_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='right',
                                                          region='shield',
                                                          lock_root_translate_axes=['v'])
        shield_r_component.attach_component(shield_component, pm.PyNode('shield_c'))

        # Left Exhaust 01
        start_joint = pm.PyNode('exhaust_01_l')
        end_joint = pm.PyNode('exhaust_01_l')
        exhaust_01_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='exhaust',
                                                            lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        exhaust_01_component.attach_component(body_component, pm.PyNode('body'))

        # Left Exhaust 02
        start_joint = pm.PyNode('exhaust_02_l')
        end_joint = pm.PyNode('exhaust_02_l')
        exhaust_02_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='exhaust_mid',
                                                            lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        exhaust_02_component.attach_component(body_component, pm.PyNode('body'))

        # Left Exhaust 03
        start_joint = pm.PyNode('exhaust_03_l')
        end_joint = pm.PyNode('exhaust_03_l')
        exhaust_03_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='exhaust_big',
                                                            lock_root_translate_axes=['v'])
        exhaust_03_component.attach_component(body_component, pm.PyNode('body'))

        # Left Exhaust 04
        start_joint = pm.PyNode('exhaust_04_l')
        end_joint = pm.PyNode('exhaust_04_l')
        exhaust_04_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='left',
                                                            region='exhaust_small',
                                                            lock_root_translate_axes=['v'])
        exhaust_04_component.attach_component(body_component, pm.PyNode('body'))

        # Right Exhaust 01
        start_joint = pm.PyNode('exhaust_01_r')
        end_joint = pm.PyNode('exhaust_01_r')
        exhaust_01_r_component = tek.FKComponent.create(tek_rig,
                                                              start_joint,
                                                              end_joint,
                                                              side='right',
                                                              region='exhaust',
                                                              lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        exhaust_01_r_component.attach_component(body_component, pm.PyNode('body'))

        # Right Exhaust 02
        start_joint = pm.PyNode('exhaust_02_r')
        end_joint = pm.PyNode('exhaust_02_r')
        exhaust_02_r_component = tek.FKComponent.create(tek_rig,
                                                              start_joint,
                                                              end_joint,
                                                              side='right',
                                                              region='exhaust_mid',
                                                              lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        exhaust_02_r_component.attach_component(body_component, pm.PyNode('body'))

        # Right Exhaust 03
        start_joint = pm.PyNode('exhaust_03_r')
        end_joint = pm.PyNode('exhaust_03_r')
        exhaust_03_r_component = tek.FKComponent.create(tek_rig,
                                                              start_joint,
                                                              end_joint,
                                                              side='right',
                                                              region='exhaust_big',
                                                              lock_root_translate_axes=['v'])
        exhaust_03_r_component.attach_component(body_component, pm.PyNode('body'))

        # Eye Shield
        start_joint = pm.PyNode('eye_shield')
        end_joint = pm.PyNode('eye_shield')
        eye_shield_component = tek.FKComponent.create(tek_rig,
                                                            start_joint,
                                                            end_joint,
                                                            side='right',
                                                            region='eye_shield',
                                                            lock_root_translate_axes=['tx', 'ty', 'tz', 'v'])
        eye_shield_component.attach_component(body_component, pm.PyNode('body'))
        eye_shield_flag = eye_shield_component.get_flags()[0]
        eye_shield_flag.set_as_sub()
        
        # Eye Shield
        start_joint = pm.PyNode('utility_warp')
        end_joint = pm.PyNode('utility_warp')
        warp_component = tek.FKComponent.create(tek_rig,
                                                                start_joint,
                                                                end_joint,
                                                                side='center',
                                                                region='utility_warp',
                                                                lock_root_translate_axes=['v'])
        warp_component.attach_component(world_component, pm.PyNode('root'))
        warp_flag = warp_component.get_flags()[0]
        warp_flag.set_as_detail()

        # Space Switching
        tek.MultiConstraint.create(tek_rig,
                                         side='center',
                                         region='body',
                                         source_object=body_flag,
                                         target_list=[world_flag, root_flag, flags_all],
                                         switch_obj=None)
        
        # utility warp
        tek.MultiConstraint.create(tek_rig,
                                            side='center',
                                            region='utility_warp',
                                            source_object=warp_flag,
                                            target_list=[world_flag, root_flag, flags_all],
                                            switch_obj=None)

        return tek_rig


class DroneChainsawRig(DroneAngraRig):
    VERSION = 1
    ASSET_ID = 'drone_angra_chainsaw'

    def __init__(self, asset_id=ASSET_ID):
        super(DroneChainsawRig, self).__init__(asset_id)

    def build(self, asset_type='combatant'):

        pm.namespace(set=':')

        DroneAngraRig(self.ASSET_ID).rig()
        tek_root = tek.get_tek_root_by_assetid(self.ASSET_ID)
        tek_rig = tek_root.get_rig()
        pitch_component = [x for x in tek_rig.get_tek_children(of_type=tek.FKComponent) if 'pitch' in str(x)]
        body_component = [x for x in tek_rig.get_tek_children(of_type=tek.FKComponent) if 'body' in str(x)]

        if not pitch_component:
            # Need a log here!
            return
        pitch_component = pitch_component[0]
        if not body_component:
            # Need a log here!
            return
        body_component = body_component[0]

        # curve_teeth_01
        start_joint = pm.PyNode('curve_teeth_01')
        end_joint = pm.PyNode('curve_teeth_01')
        tooth_01_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='center',
                                                          region='teeth_01',
                                                          lock_root_translate_axes=['v'])
        tooth_01_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        tooth_01_flag = tooth_01_component.get_flags()[0]
        tooth_01_flag.set_as_detail()

        # curve_teeth_02
        start_joint = pm.PyNode('curve_teeth_02')
        end_joint = pm.PyNode('curve_teeth_02')
        tooth_02_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='center',
                                                          region='teeth_02',
                                                          lock_root_translate_axes=['v'])
        tooth_02_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        tooth_02_flag = tooth_02_component.get_flags()[0]
        tooth_02_flag.set_as_detail()

        # curve_teeth_03
        start_joint = pm.PyNode('curve_teeth_03')
        end_joint = pm.PyNode('curve_teeth_03')
        tooth_03_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='center',
                                                          region='teeth_03',
                                                          lock_root_translate_axes=['v'])
        tooth_03_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        tooth_03_flag = tooth_03_component.get_flags()[0]
        tooth_03_flag.set_as_detail()

        # curve_teeth_04
        start_joint = pm.PyNode('curve_teeth_04')
        end_joint = pm.PyNode('curve_teeth_04')
        tooth_04_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='center',
                                                          region='teeth_04',
                                                          lock_root_translate_axes=['v'])
        tooth_04_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        tooth_04_flag = tooth_04_component.get_flags()[0]
        tooth_04_flag.set_as_detail()

        # curve_teeth_05
        start_joint = pm.PyNode('curve_teeth_05')
        end_joint = pm.PyNode('curve_teeth_05')
        tooth_05_component = tek.FKComponent.create(tek_rig,
                                                          start_joint,
                                                          end_joint,
                                                          side='center',
                                                          region='teeth_05',
                                                          lock_root_translate_axes=['v'])
        tooth_05_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        tooth_05_flag = tooth_05_component.get_flags()[0]
        tooth_05_flag.set_as_detail()

        # Bottom Teeth
        start_joint = pm.PyNode('bottom_teeth_c')
        end_joint = pm.PyNode('bottom_teeth_c')
        bottom_tooth_component = tek.FKComponent.create(tek_rig,
                                                              start_joint,
                                                              end_joint,
                                                              side='center',
                                                              region='bottom_tooth',
                                                              lock_root_translate_axes=['v'])
        bottom_tooth_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        bottom_tooth_flag = bottom_tooth_component.get_flags()[0]
        bottom_tooth_flag.set_as_detail()

        # Top Teeth
        start_joint = pm.PyNode('top_teeth_c')
        end_joint = pm.PyNode('top_teeth_c')
        top_tooth_component = tek.FKComponent.create(tek_rig,
                                                           start_joint,
                                                           end_joint,
                                                           side='center',
                                                           region='top_tooth',
                                                           lock_root_translate_axes=['v'])
        top_tooth_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        top_tooth_flag = top_tooth_component.get_flags()[0]
        top_tooth_flag.set_as_detail()
        
        tek_rig.rigTemplate.set(DroneChainsawRig.__name__)
        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class DroneGatlingRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'drone_angra_gatling'

    def __init__(self, asset_id=ASSET_ID):
        super(DroneGatlingRig, self).__init__(asset_id)

    def build(self, asset_type='combatant'):
        pm.namespace(set=':')

        DroneAngraRig(self.ASSET_ID).rig()
        tek_root = tek.get_tek_root_by_assetid(self.ASSET_ID)
        tek_rig = tek_root.get_rig()
        pitch_component = [x for x in tek_rig.get_tek_children(of_type=tek.FKComponent) if 'pitch' in str(x)]
    
        if not pitch_component:
            # Need a log here!
            return
        pitch_component = pitch_component[0]

        # Gatling Barrel
        start_joint = pm.PyNode('gatling_barrel_c')
        end_joint = pm.PyNode('gatling_barrel_c')
        gatling_component = tek.FKComponent.create(tek_rig,
                                                         start_joint,
                                                         end_joint,
                                                         side='center',
                                                         region='gatling_barrel',
                                                         lock_root_translate_axes=['tx', 'ty', 'tz', 'rx', 'ry', 'v'])
        gatling_component.attach_component(pitch_component, pm.PyNode('pitch_pivot'))
        gatling_flag = gatling_component.get_flags()[0]
        gatling_flag.set_as_sub()
        
        tek_rig.rigTemplate.set(DroneGatlingRig.__name__)
        tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class DronePhasingFlyerRig(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 'phasingflyerdrone'

    def __init__(self, asset_id=ASSET_ID):
        super(DronePhasingFlyerRig, self).__init__(asset_id)

    def build(self, asset_type='combatant', finalize=True):

        pm.namespace(set=':')
        
        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        skel_markup = chain_markup.ChainMarkup(root_joint)

        tek_root = tek.TEKRoot.create(root_joint, asset_type, self.asset_id)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

        flags_all = tek_rig.flagsAll.get()

        # World
        start_joint = skel_markup.get_start('root', 'center')
        world_component = tek.WorldComponent.create(tek_rig,
                                                           start_joint,
                                                           'center',
                                                           'world')
        offset_flag = world_component.offset_flag
        root_flag = world_component.root_flag
        world_flag = world_component.world_flag

        # Cog
        pelvis_joint = skel_markup.get_start('body', 'center')
        cog_component = tek.CogComponent.create(tek_rig,
                                                       pelvis_joint,
                                                       pelvis_joint,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Body
        body_start_joint, body_end_joint = skel_markup.get_chain('body', 'center')
        body_component = tek.FKComponent.create(tek_rig,
                                                       body_start_joint,
                                                       body_end_joint,
                                                       side='center',
                                                       region='body')
        body_component.attach_component(cog_component, cog_flag.node)
        body_flag = body_component.get_flags()[0]

        # Neck
        head_start_joint, head_end_joint = skel_markup.get_chain('head', 'center')
        neck_component = tek.FKComponent.create(tek_rig,
                                                       head_start_joint,
                                                       head_end_joint,
                                                       side='center',
                                                       region='head')
        neck_component.attach_component(body_component, body_start_joint)
        neck_flag = neck_component.get_start_flag()

        # Tail
        """
        start_joint, end_joint = skel_markup.get_chain('tail', 'center')
        tail_component = tek.FKComponent.create(tek_rig,
                                                       start_joint,
                                                       end_joint,
                                                       side='center',
                                                       region='tail')
        tail_component.attach_component(body_component, body_start_joint)
        """
        tail_chain = skel_markup.get_full_chain('tail', 'center')
        tail_component = tek.IKFKRibbonComponent.create(tek_rig,
                                                             tail_chain[0],
                                                             tail_chain[-1],
                                                             side='center',
                                                             region='tail')
        tail_component.attach_component(body_component, body_start_joint)
        tail_fk_flag = tail_component.fk_flags[0]
        tail_ik_flag = tail_component.ik_flag
        tail_ik_pv_flag = tail_component.pv_flag

        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='fk_tail',
                                          source_object=tail_fk_flag,
                                          target_list=[body_flag,
                                                       world_flag],
                                          t=False,
                                          switch_attr='follow')

        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='ik_tail',
                                          source_object=tail_ik_flag,
                                          target_list=[body_flag,
                                                       world_flag])

        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='fk_pv_tail',
                                          source_object=tail_ik_pv_flag,
                                          target_list=[body_flag,
                                                       world_flag])

        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_component.get_flags()[0],
                                          target_list=[body_flag,
                                                       world_flag])

        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='neck',
                                          source_object=neck_component.get_flags()[-1],
                                          target_list=[neck_component.get_flags()[-2],
                                                       world_flag])

        # Wings
        for side in ['left', 'right']:
            clav_joint = skel_markup.get_start('clavicle', side)
            clavicle_component = tek.FKComponent.create(tek_rig,
                                                          clav_joint,
                                                          clav_joint,
                                                          side=side,
                                                          region='clavicle')
            clavicle_component.attach_component(body_component, body_start_joint)
            clav_flag = clavicle_component.get_flags()[0]

            arm_start_joint, arm_end_joint = skel_markup.get_chain('arm', side)
            arm_component = tek.FKComponent.create(tek_rig,
                                                           arm_start_joint,
                                                           arm_end_joint,
                                                           side=side,
                                                           region='arm')
            arm_component.attach_component(clavicle_component, clav_joint)
            arm_component.get_flags()[1].lock_and_hide_attrs(['rx', 'ry'])

            thumb_start_joint, thumb_end_joint = skel_markup.get_chain('thumb', side)
            thumb_component = tek.FKComponent.create(tek_rig,
                                                            thumb_start_joint,
                                                            thumb_end_joint,
                                                            side=side,
                                                            region='thumb')
            thumb_component.attach_component(arm_component, arm_end_joint)

            index_start_joint, index_end_joint = skel_markup.get_chain('index', side)
            index_component = tek.FKComponent.create(tek_rig,
                                                          index_start_joint,
                                                          index_end_joint,
                                                          side=side,
                                                          region='index')
            index_component.attach_component(arm_component, arm_end_joint)

            middle_start_joint, middle_end_joint = skel_markup.get_chain('middle', side)
            middle_component = tek.FKComponent.create(tek_rig,
                                                            middle_start_joint,
                                                            middle_end_joint,
                                                            side=side,
                                                            region='middle')
            middle_component.attach_component(index_component, index_start_joint)

            ring_start_joint, ring_end_joint = skel_markup.get_chain('ring', side)
            ring_component = tek.FKComponent.create(tek_rig,
                                                             ring_start_joint,
                                                             ring_end_joint,
                                                             side=side,
                                                             region='ring')
            ring_component.attach_component(index_component, index_start_joint)

            ring_split_start_joint, ring_split_end_joint = skel_markup.get_chain('ring_split', side)
            ring_split_component = tek.FKComponent.create(tek_rig,
                                                           ring_split_start_joint,
                                                           ring_split_end_joint,
                                                           side=side,
                                                           region='ring_split')
            ring_split_component.attach_component(index_component, ring_end_joint.getParent())

            wing_float_start_joint, wing_float_end_joint = skel_markup.get_chain('wing_float', side)
            wing_float_component = tek.FKComponent.create(tek_rig,
                                                                 wing_float_start_joint,
                                                                 wing_float_end_joint,
                                                                 side=side,
                                                                 region='wing_float',
                                                                 lock_root_translate_axes=[])
            wing_float_component.attach_component(arm_component, arm_end_joint)

            pinky_start_joint, pinky_end_joint = skel_markup.get_chain('pinky', side)
            pinky_component = tek.FKComponent.create(tek_rig,
                                                                 pinky_start_joint,
                                                                 pinky_end_joint,
                                                                 side=side,
                                                                 region='pinky')
            pinky_component.attach_component(arm_component, arm_start_joint)

            hexadactyl_start_joint, hexadactyl_end_joint = skel_markup.get_chain('hexadactyl', side)
            hexadactyl_component = tek.FKComponent.create(tek_rig,
                                                            hexadactyl_start_joint,
                                                            hexadactyl_end_joint,
                                                            side=side,
                                                            region='hexadactyl')
            hexadactyl_component.attach_component(arm_component, arm_start_joint)

            septadactyl_start_joint, septadactyl_end_joint = skel_markup.get_chain('septadactyl', side)
            septadactyl_component = tek.FKComponent.create(tek_rig,
                                                            septadactyl_start_joint,
                                                            septadactyl_end_joint,
                                                            side=side,
                                                            region='septadactyl')
            septadactyl_component.attach_component(arm_component, arm_start_joint)

            septadactyl_split_start_joint, septadactyl_split_end_joint = skel_markup.get_chain('septadactyl_split', side)
            septadactyl_split_component = tek.FKComponent.create(tek_rig,
                                                                 septadactyl_split_start_joint,
                                                                 septadactyl_split_end_joint,
                                                                 side=side,
                                                                 region='septadactyl_split')
            septadactyl_split_component.attach_component(septadactyl_component, septadactyl_split_end_joint.getParent())

            tek.MultiConstraint.create(tek_rig,
                                              side=side,
                                              region='fk_arm',
                                              source_object=clav_flag,
                                              target_list=[body_flag,
                                                           root_flag],
                                              t=False,
                                              switch_attr='follow')

            # Tail Fingers
            index_top_tail_start_joint, index_top_tail_end_joint = skel_markup.get_chain('index_top_tail', side)
            index_top_tail_component = tek.FKComponent.create(tek_rig,
                                                                  index_top_tail_start_joint,
                                                                  index_top_tail_end_joint,
                                                                  side=side,
                                                                  region='index_top_tail')
            index_top_tail_component.attach_component(tail_component, tail_chain[0])

            middle_top_tail_start_joint, middle_top_tail_end_joint = skel_markup.get_chain('middle_top_tail', side)
            middle_top_tail_component = tek.FKComponent.create(tek_rig,
                                                                     middle_top_tail_start_joint,
                                                                     middle_top_tail_end_joint,
                                                                     side=side,
                                                                     region='middle_top_tail')
            middle_top_tail_component.attach_component(tail_component, tail_chain[1])

            index_bot_tail_start_joint, index_bot_tail_end_joint = skel_markup.get_chain('index_bot_tail', side)
            index_bot_tail_component = tek.FKComponent.create(tek_rig,
                                                                     index_bot_tail_start_joint,
                                                                     index_bot_tail_end_joint,
                                                                     side=side,
                                                                     region='index_bot_tail')
            index_bot_tail_component.attach_component(tail_component, tail_chain[-3])

            middle_bot_tail_start_joint, middle_bot_tail_end_joint = skel_markup.get_chain('middle_bot_tail', side)
            middle_bot_tail_component = tek.FKComponent.create(tek_rig,
                                                                     middle_bot_tail_start_joint,
                                                                     middle_bot_tail_end_joint,
                                                                     side=side,
                                                                     region='middle_bot_tail')
            middle_bot_tail_component.attach_component(tail_component, tail_chain[-2])

            ring_bot_tail_start_joint, ring_bot_tail_end_joint = skel_markup.get_chain('ring_bot_tail', side)
            ring_bot_tail_component = tek.FKComponent.create(tek_rig,
                                                                     ring_bot_tail_start_joint,
                                                                     ring_bot_tail_end_joint,
                                                                     side=side,
                                                                     region='ring_bot_tail')
            ring_bot_tail_component.attach_component(tail_component, tail_chain[-2])

            # Face Joints
            for region in ['sub_index_face', 'index_face', 'sub_middle_face', 'middle_face', 'ring_face', 'jaw']:
                start_joint, end_joint = skel_markup.get_chain(region, side)
                new_component = tek.FKComponent.create(tek_rig,
                                                                     start_joint,
                                                                     end_joint,
                                                                     side=side,
                                                                     region=region)
                new_component.attach_component(neck_component, head_end_joint)

        thumb_face_start_joint, thumb_face_end_joint = skel_markup.get_chain('thumb_face', 'center')
        thumb_face_component = tek.FKComponent.create(tek_rig,
                                                                thumb_face_start_joint,
                                                                thumb_face_end_joint,
                                                                side='center',
                                                                region='thumb_face')
        thumb_face_component.attach_component(neck_component, head_end_joint)

        if finalize:
            tek_rig.rigTemplate.set(ExplodingEyeTemplate.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig

class ExplodingEyeTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = 't8bz-r6nyl-ch1x8-4wlt'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    def build(self, finalize=True):
        pm.namespace(set=':')

        # import Skeletal Mesh using ASSET_ID into the namespace
        root_joint = pm.PyNode('root')

        tek_root = tek.TEKRoot.create(root_joint, 'combatant', self.ASSET_ID)
        skel_mesh = tek.SkeletalMesh.create(tek_root)
        tek_rig = tek.TEKRig.create(tek_root)

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
        root_flag.set_as_sub()
        offset_flag.set_as_detail()

        # Root Multiconstraint
        tek.MultiConstraint.create(tek_rig,
                                          side='center',
                                          region='root',
                                          source_object=root_flag,
                                          target_list=[world_flag,
                                                       offset_flag])

        # Cog
        body_start, body_end = skel_hierarchy.get_chain('body', 'center')
        cog_component = tek.CogComponent.create(tek_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'cog',
                                                       orientation=[-90, 0, 0])
        cog_component.attach_component(world_component, offset_flag.node)
        cog_flag = cog_component.get_flags()[0]

        # Body
        body_component = tek.FKComponent.create(tek_rig,
                                                       body_start,
                                                       body_start,
                                                       'center',
                                                       'body',
                                                       lock_root_translate_axes=[])
        body_component.attach_component(cog_component, cog_flag.node)

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

        for side in ['left', 'right']:
            shield_joint = skel_hierarchy.get_start('shield', side)
            if shield_joint:
                jaw_component = tek.FKComponent.create(tek_rig,
                                                              shield_joint,
                                                              shield_joint,
                                                              side=side,
                                                              region='shield',
                                                              lock_root_translate_axes=[])
                jaw_component.attach_component(body_component, body_start)

        if finalize:
            tek_rig.rigTemplate.set(ExplodingEyeTemplate.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig


class HealingSkullTemplate(ExplodingEyeTemplate):
    VERSION = 1
    ASSET_ID = 'healingskull'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        tek_rig = super().build(finalize=False)
        tek_root = tek_rig.get_root()
        tek_root.asset_id = self.ASSET_ID
        tek_root.assetName.set(self.ASSET_ID)

        pm.namespace(set=':')
        root_joint = pm.PyNode('root')
        skel_hierarchy = chain_markup.ChainMarkup(root_joint)
        body_component = lists.get_first_in_list(tek_rig.get_tek_children(of_type=tek.FKComponent,
                                                                            side='center',
                                                                            region='body'))
        body_flag = body_component.get_flags()[0]

        # veil cloths
        for side in ['left', 'right']:
            for veil in ['exhaust_01', 'exhaust_02', 'exhaust_03', 'exhaust_04', 'exhaust_05', 'exhaust_06',
                         'exhaust_07']:
                veil_start, veil_end = skel_hierarchy.get_chain(veil, side)
                if veil_start:
                    veil_component = tek.FKComponent.create(tek_rig,
                                                            veil_start,
                                                            veil_end,
                                                            side=side,
                                                            region=veil,
                                                            lock_root_translate_axes=[])

                    veil_component.attach_component(body_component, body_flag.node)

        if finalize:
            tek_rig.rigTemplate.set(HealingSkullTemplate.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig

class ShieldingSkullTemplate(ExplodingEyeTemplate):
    VERSION = 1
    ASSET_ID = 'shieldingskull'
    ASSET_TYPE = 'combatant'

    def __init__(self, asset_id=ASSET_ID):
        super().__init__(asset_id)

    # We would not normally create the root and skel mesh here.
    def build(self, finalize=True):
        tek_rig = super().build(finalize=False)
        tek_root = tek_rig.get_root()
        tek_root.asset_id = self.ASSET_ID
        tek_root.assetName.set(self.ASSET_ID)

        if finalize:
            tek_rig.rigTemplate.set(ShieldingSkullTemplate.__name__)
            tek_rig.finalize_rig(self.get_flags_path())

        return tek_rig