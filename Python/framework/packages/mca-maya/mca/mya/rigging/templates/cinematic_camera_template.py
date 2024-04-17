#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Camera rig for use in cinematic scenes.
"""
# mca python imports
import os

# software specific imports

# mca python imports
from mca.mya.rigging import tek, chain_markup, skel_utils
from mca.mya.rigging.templates import rig_templates
from mca.mya.rigging.flags import tek_flag
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import namespace
from mca.common.paths import paths
from mca.common import log

logger = log.MCA_LOGGER


class CinematicCameraTemplate(rig_templates.RigTemplates):
    VERSION = 1
    ASSET_ID = ''
    ASSET_TYPE = ''

    def __init__(self, asset_id=ASSET_ID, asset_type=ASSET_TYPE):
        super(CinematicCameraTemplate, self).__init__(asset_id, asset_type)

    @ma_decorators.keep_namespace_decorator
    def build(self, **kwargs):
        camera_rig_path = os.path.join(os.path.dirname(paths.get_cine_seq_path()), 'Assets', 'camera', 'Rig')
        cam = kwargs.get('cam')
        if ':' in cam.name():
            camera_ns = cam.name().split(':')[0]
        else:
            camera_ns = ''
        namespace.set_namespace(camera_ns, check_existing=False)

        camera_skel_path = os.path.join(camera_rig_path, 'camera_skel.skl')
        root = skel_utils.import_skeleton(camera_skel_path)
        chain = chain_markup.ChainMarkup(root)
        cam_joint = chain.get_start('cam', 'center')

        tek_root = tek.TEKRoot.create(root, self.asset_type, self.asset_id)
        tek_rig = tek.TEKRig.create(tek_root)

        world_component = tek.WorldComponent.create(tek_rig,
                                                     root,
                                                     'center',
                                                     'world',
                                                     orientation=[-90, 0, 0])
        root_flag = world_component.root_flag
        root_flag.set_as_sub()
        offset_flag = world_component.offset_flag
        offset_flag.set_as_detail()

        cam_component = tek.CameraComponent.create(tek_rig,
                                                    cam_joint,
                                                    'center',
                                                    'cam',
                                                    cam)
        cam_component.attach_component([world_component], [offset_flag])

        # Since the camera is not a mca asset, and we do not want to add all meshes to skins grp, finalizing rig here.
        flag_path = os.path.join(camera_rig_path, 'Flags')
        flags = tek_rig.get_flags()
        tek_flag.swap_flags(flags, flag_path)
        tek_rig.color_flags()
        tek_rig.create_display_layers_for_cam(cam)
        tek_rig.all_grp.rename(f'{camera_ns}_all')

        return tek_rig

