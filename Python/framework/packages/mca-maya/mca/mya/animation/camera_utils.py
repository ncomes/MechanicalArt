#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that contains useful functions related to cameras and play blasting.
"""
# System global imports
import os
# software specific imports
import pymel.core as pm
# PySide2 imports

#  python imports
from mca.common.utils import fileio, video_utils
from mca.common.modifiers import decorators
from mca.mya.utils import attr_utils, namespace_utils
from mca.mya.animation import time_utils, baking
#from mca.mya.rigging.templates import cinematic_camera_template
# This should probably be moved to a tool and not in the general cam utils.
from mca.mya.rigging import frag
from mca.mya.rigging.frag import frag_rig
from mca.mya.utils import constraint_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import maya_dialogs

from mca.common import log
logger = log.MCA_LOGGER


def create_new_render_panel(camera_node=None, resolution=None, render_style=None, lighting_style=None, display_textures=True):
    """
    Create a new model panel and resize the window to account for our resolution settings.

    :param Transform camera_node: The transform of a given camera. Defaults to 'persp'
    :param list[int, int] resolution: Two ints representing the width and height of the final model panel.
    :param str, None render_style: The render style of the model panel. Defaults to "smoothShaded"
    :param str, None lighting_style: The render style for the lighting in the scene, default is 'default'
        'all'
        'active'
        'default'
        'none'
    :param bool display_textures: If textures should be rendered.
    :param bool display_hud: If the Maya HUD should be visible during the render.
    :return: The Window and ModelEditor renderer.
    :rtype: window, modelEditor
    """
    camera_node = camera_node if camera_node and isinstance(camera_node.getShape(), pm.nt.Camera) else pm.PyNode('persp')
    resolution = resolution if resolution and len(resolution) == 2 and all(isinstance(x, int) for x in resolution) else [1920, 1080]
    lighting_style = lighting_style or 'default'
    render_style = render_style or 'smoothShaded'

    new_window = pm.window()
    new_window.setWidth(resolution[0] + 2)
    new_window.setHeight(resolution[-1])
    form = pm.formLayout()
    new_model_editor = pm.modelEditor()
    column = pm.columnLayout('true')

    pm.formLayout(form,
                  edit=True,
                  attachForm=[(column, 'top', 0), (column, 'left', 0), (new_model_editor, 'top', 0), (new_model_editor, 'bottom', 0), (new_model_editor, 'right', 0)],
                  attachNone=[(column, 'bottom'), (column, 'right')],
                  attachControl=(new_model_editor, 'left', 0, column))

    pm.modelEditor(new_model_editor,
                   e=True,
                   displayAppearance=render_style,
                   displayTextures=display_textures,
                   displayLights=lighting_style,
                   th=True,
                   camera=camera_node,
                   activeView=True,
                   grid=False,
                   allObjects=True)

    pm.modelEditor(new_model_editor,
                   e=True,
                   nc=False,
                   j=False,
                   df=False,
                   ca=False,
                   lt=False,
                   ikh=False,
                   lc=False,
                   pv=False)

    pm.showWindow(new_window)
    return new_window, new_model_editor


def playblast_video(file_path, camera_node=None, node_list=None, time_range=None, resolution=None, bg_color=None, display_hud=False, lighting_style=None):
    """
    Capture a quick video using Maya's internal playblast feature.

    :param str file_path: File path to where the video should be saved. expected extension of ".avi"
    :param Transform camera_node: The transform of a given camera. Defaults to 'persp'
    :param list[int, int], None time_range: The inclusive time range that the video should be captured from. Current frame is the default for None.
    :param list[int, int], None resolution: Two ints representing the width and height of the capture. 1080 is the default for None
    :param list[float, float, float], None bg_color: RGB float values for the background of the captures.
    :param bool display_hud: If the Maya HUD should be visible during the render.
    :param str lighting_style: The render style for the lighting in the scene, default is 'default'
        'all'
        'active'
        'default'
        'none'
    :return: The resulting file path.
    :rtype: str
    """
    if not time_range or not all(isinstance(x, int) for x in time_range):
        time_range = time_utils.get_times()

    original_bg_color = None
    if bg_color:
        if isinstance(bg_color, list) and len(bg_color) == 3:
            original_bg_color = pm.displayRGBColor('background', q=True)
            pm.displayRGBColor('background', *bg_color)
        else:
            raise ValueError('Background color values are not a list of 3 floats: {0}'.format(bg_color))

    my_window, model_editor = create_new_render_panel(camera_node, resolution, display_hud=display_hud, lighting_style=lighting_style)
    
    if node_list:
        pm.select(node_list)
        pm.isolateSelect(model_editor, state=True)

    if not file_path.endswith('.avi'):
        file_path = f'{file_path}.avi'

    pm.select(None)
    pm.refresh()
    # Avi export doesn't work with arg "completeFilename", instead using "filename" which effectively works the same.
    fileio.touch_path(file_path, True)
    pm.playblast(percent=100,
                 startTime=time_range[0],
                 endTime=time_range[1],
                 filename=file_path,
                 format='avi',
                 viewer=False,
                 editorPanelName=model_editor,
                 forceOverwrite=True,
                 showOrnaments=True,
                 useTraxSounds=False,
                 sound=None)

    if original_bg_color:
        pm.displayRGBColor('background', *original_bg_color)

    my_window.delete()
    return file_path


def playblast_images(file_path, camera_node=None, node_list=None, frame_list=None, resolution=None, bg_color=None, lighting_style=None):
    """
    Capture images at frames using Maya's internal playblast feature.

    :param str file_path: A single path, or a directory to save multiple captures.
    :param Transform camera_node: The transform of a given camera.
    :param list[Transform] node_list: A list of objects to isolate view on if passed.
    :param list[int], None frame_list: A list of frames to capture at. Or none to capture just the current frame.
    :param list[int, int] resolution: Two ints representing the width and height of the capture.
    :param list[float, float, float], None bg_color: RGB float values for the background of the captures.
    :param bool hud: If the Maya HUD should be visible during the render.
    :param str lighting_style: The render style for the lighting in the scene, default is 'default'
        'all'
        'active'
        'default'
        'none'
    :return: A list of all captured files.
    :rtype: list[str]
    """
    if isinstance(frame_list, int):
        frame_list = [frame_list]

    if not frame_list or not all(isinstance(x, int) for x in frame_list):
        # If our frame range is bad just use the current frame.
        frame_list = [pm.currentTime()]

    new_window, model_editor = create_new_render_panel(camera_node, resolution, lighting_style=lighting_style)

    if node_list:
        pm.select(node_list)
        pm.isolateSelect(model_editor, state=True)

    original_bg_color = None
    if bg_color:
        if isinstance(bg_color, list) and len(bg_color) == 3:
            original_bg_color = pm.displayRGBColor('background', q=True)
            pm.displayRGBColor('background', *bg_color)
        else:
            raise ValueError('Background color values are not a list of 3 floats: {0}'.format(bg_color))

    pm.select(None)
    pm.refresh()
    if file_path.endswith('.jpg'):
        # Single frame playblast.
        fileio.touch_path(file_path, True)
        pm.playblast(percent=100,
                     frame=frame_list[0],
                     format="image",
                     compression='jpg',
                     viewer=False,
                     editorPanelName=model_editor,
                     forceOverwrite=True,
                     showOrnaments=False,
                     completeFilename=file_path)
    else:
        # Multi frame playblast.
        for x_file in os.listdir(file_path):
            if os.path.isfile(x_file) and 'still' in os.path.basename(x_file):
                fileio.touch_path(os.path.join(file_path, x_file), True)
        pm.playblast(percent=100,
                     filename=os.path.join(file_path, 'stills'),
                     frame=frame_list,
                     format="image",
                     compression='jpg',
                     viewer=False,
                     editorPanelName=model_editor,
                     forceOverwrite=True,
                     showOrnaments=False)

    if original_bg_color:
        pm.displayRGBColor('background', *original_bg_color)

    new_window.delete()
    return file_path if file_path.endswith('.jpg') else [os.path.join(file_path, x) for x in os.listdir(file_path) if 'stills.' in x]


def capture_and_compress_video(file_path, camera_node=None, time_range=None, resolution=None, delete_uncompressed=True, background=None, hud=False, lighting_style='default'):
    """
    Capture a quick video using Maya's internal playblast feature.

    :param str file_path: File path to where the video should be saved with an expected extension of .mp4.
    :param Transform camera_node: The transform of a given camera. Defaults to 'persp'
    :param list[int, int] time_range: The inclusive time range that the video should be captured from.
    :param list[int, int] resolution: Two ints representing the width and height of the capture.
    :param bool delete_uncompressed: If the original raw playblast avi should be deleted.
    :param list[float, float, float], None background: RGB float values for the background of the captures.
    :param bool hud: If the Maya HUD should be visible during the render.
    :param str lighting_style: The render style for the lighting in the scene, default is 'default'
        'all'
        'active'
        'default'
        'none'
    :return: The resulting file path.
    :rtype: str
    """
    if not file_path.endswith('.mp4'):
        logger.warning(f'{file_path}: File path must be to a valid .mp4')
        return

    fileio.touch_path(file_path)
    avi_path = file_path.replace('.mp4', '.avi')

    # Send the file path without extension we'll always get an .avi in return.
    temp_file_path = playblast_video(os.path.join(os.path.dirname(file_path), 'temp.avi'),
                                     camera_node=camera_node,
                                     time_range=time_range,
                                     resolution=resolution,
                                     bg_color=background,
                                     display_hud=hud,
                                     lighting_style=lighting_style)
    fileio.touch_path(avi_path, True)
    os.rename(temp_file_path, avi_path)

    # Run MP4 conversion.
    return_file_path = video_utils.ffmpeg_convert_to_mp4(avi_path)

    if return_file_path and os.path.exists(return_file_path) and delete_uncompressed:
        os.remove(avi_path)

    return return_file_path


def create_mca_ubercam(shot_node_list,
                       h_film_ap=1.249,
                       v_film_ap=0.531,
                       lens_squeeze_ratio=1.0,
                       shutter_angle=144.000,
                       near_clip=1.000,
                       far_clip=100000.000,
                       display_mask_opacity=1.0,
                       display_mask_color=(0.0, 0.0, 0.0),
                       center_of_interest=5.0):
    """
    Creates an Ubercam camera from a list of shots.

    :param list(pm.nt.Shot) shot_node_list: List of shots whose cameras to use for Ubercam.

    :param float h_film_ap: Horizontal film aperture.
    :param float v_film_ap: Vertical film aperture.
    :param float lens_squeeze_ratio: Lens squeeze ratio.
    :param float shutter_angle: Shutter angle.
    :param float near_clip: Near clip plane.
    :param float far_clip: Far clip plane.
    :param float display_mask_opacity: Display mask opacity.
    :param tuple(float, float, float) display_mask_color: Display mask color.
    :param float center_of_interest: Center of interest.
    :return: Returns the created Ubercam transform.
    :rtype: pm.nt.Transform

    """

    sorted_shots = sorted(shot_node_list, key=lambda s: s.startFrame.get())
    uc_transform, ubercam = pm.camera(name="UberCam",
                                      displayGateMask=True,
                                      horizontalFilmAperture=h_film_ap,
                                      verticalFilmAperture=v_film_ap,
                                      lensSqueezeRatio=lens_squeeze_ratio,
                                      shutterAngle=shutter_angle,
                                      nearClipPlane=near_clip,
                                      farClipPlane=far_clip)
    # other settings
    ubercam.displayGateMaskOpacity.set(display_mask_opacity)
    ubercam.displayGateMaskColor.set(display_mask_color)
    ubercam.centerOfInterest.set(center_of_interest)

    # locks
    # ubercam.horizontalFilmAperture.lock()
    # ubercam.verticalFilmAperture.lock()
    # ubercam.lensSqueezeRatio.lock()
    # ubercam.filmFitOffset.lock()
    # ubercam.horizontalFilmOffset.lock()
    # ubercam.verticalFilmOffset.lock()
    # ubercam.centerOfInterest.lock()
    # ubercam.overscan.lock()
    # ubercam.shutterAngle.lock()
    # uc_transform.rotateOrder.lock()

    uc_transform.rename("UberCam")
    if pm.animLayer("BaseAnimation", q=True, exists=True):
        pm.animLayer("BaseAnimation", edit=True, lock=False)
        pm.animLayer("BaseAnimation", edit=True, selected=True)
        pm.animLayer("BaseAnimation", edit=True, preferred=True)

    for i, shot in enumerate(sorted_shots):
        cam_xform = shot.currentCamera.get()
        pc = pm.parentConstraint(cam_xform, uc_transform, mo=False)
        pc_info = [pc.getTargetList(), pc.getWeightAliasList()]
        pc_info = dict(zip(*pc_info))

        maya_start_frame = int(round(shot.startFrame.get()))
        maya_end_frame = int(round(shot.endFrame.get()))

        choice_inputs = pm.choice(ubercam,
                                  n='ubercam_fl_choice',
                                  at='focalLength',
                                  t=[maya_start_frame, maya_end_frame],
                                  index=i)
        cam_xform.focalLength >> choice_inputs[0]

        if shot != sorted_shots[-1]:
            next_shot_start = sorted_shots[i + 1].startFrame.get()
            if next_shot_start - maya_start_frame > 1:
                maya_end_frame = next_shot_start - 1
        else:
            maya_end_frame = time_utils.get_scene_end_time()
        pc_info[cam_xform].setKey(time=maya_start_frame - 1, value=0.0)
        pc_info[cam_xform].setKey(time=maya_start_frame, value=1.0)
        pc_info[cam_xform].setKey(time=maya_end_frame, value=1.0)
        pc_info[cam_xform].setKey(time=maya_end_frame + 1, value=0.0)
        if len(sorted_shots) > 1 and shot == sorted_shots[-1]:
            pm.cutKey(pc_info[cam_xform], time=f':{maya_start_frame - 2}', cl=True)
            pc_info[cam_xform].setKey(time=0.0, value=0.0)

    uc_transform.v.set(0)
    uc_transform.addAttr('MCAUberCam', at='bool')
    pm.lookThru(uc_transform)
    uc_grp = pm.group(em=True, n='MCAUberCam_grp')
    uc_grp.addAttr('MCAAUberCamGrp', at='bool')
    uc_transform.setParent(uc_grp)
    cameras_grp = [x for x in pm.ls(type=pm.nt.Transform) if x.hasAttr('cameraGrp')]
    if cameras_grp:
        uc_grp.setParent(cameras_grp[0])
    return uc_transform



@ma_decorators.keep_namespace_decorator
def create_mca_ubercam_cmd():
    """
    Command to create ubercam.

    """

    if 'MCAUberCam' in namespace_utils.get_all_namespaces():
        namespace_utils.purge_namespace('MCAUberCam')
    namespace_utils.set_namespace('MCAUberCam')

    shot_node_list = pm.ls(type=pm.nt.Shot)
    if not shot_node_list:
        return
    uc_transform = create_mca_ubercam(shot_node_list)

    logger.info(f'Created ubercam: {uc_transform.name()}')



def rig_cinematic_camera_cmd():
    """
    Command to rig selected camera.

    """

    selection_list = pm.selected()
    for camera_xform in selection_list:
        if camera_xform.hasAttr('focalLength'):
            temp_loc = None
            cam_trans = 0.0
            cam_rot = 0.0
            start_time, end_time = time_utils.get_keyframe_range_from_nodes([camera_xform])
            if not end_time:
                cam_trans = camera_xform.getTranslation()
                cam_rot = camera_xform.getRotation()
            else:
                anim_curve_list = camera_xform.listConnections(type=pm.nt.AnimCurve)
                temp_loc = dag_utils.create_locator_at_object(camera_xform)
                temp_con = constraint_utils.parent_constraint_safe(camera_xform, temp_loc, mo=False)
                baking.bake_objects([temp_loc], bake_range=[start_time, end_time])
                pm.delete(temp_con)
                pm.delete(anim_curve_list)

            for attr in attr_utils.TRANSLATION_ATTRS + attr_utils.ROTATION_ATTRS:
                camera_xform.setAttr(attr, 0)

            #cam_rig = cinematic_camera_template.CinematicCameraTemplate().build(**{'cam': camera_xform})

            frag_children = [frag.FRAGNode(x) for x in cam_rig.fragChildren.listConnections()]
            cam_comp = [x for x in frag_children if isinstance(x, frag.CameraComponent)][0]
            cam_flag = cam_comp.get_flags()[0]

            if temp_loc:
                temp_con = constraint_utils.parent_constraint_safe(temp_loc, cam_flag, mo=False)
                baking.bake_objects([cam_flag], bake_range=[start_time, end_time])
                pm.delete(temp_con)
                pm.delete(temp_loc)
            else:
                cam_flag.setRotation(cam_rot)
                cam_flag.setTranslation(cam_trans)

            camera_grp = None
            for node in pm.ls(type=pm.nt.Transform):
                if node.hasAttr('cameraGrp'):
                    camera_grp = node
                    break
            if camera_grp:
                cam_rig.all_grp.setParent(camera_grp)



def remove_ubercam_cmd():
    """
    Purges ubercam namespace then looks to see if any of the ubercam objects exist in case they were not in NS.

    """

    ubercam_namespace = 'MCAUberCam'
    ubercam_objects = ['MCAUberCam', 'ubercam_fl_choice']

    if ubercam_namespace in namespace_utils.get_all_namespaces():
        namespace_utils.purge_namespace(ubercam_namespace)
    for uc_obj in ubercam_objects:
        if pm.objExists(uc_obj):
            pm.delete(uc_obj)


def camera_is_rigged(camera_xform):
    """
    Checks if a given camera is rigged.

    :param pm.nt.Transform camera_xform: Camera to check for rigged status of.
    :return: Returns True if the camera is rigged, False otherwise.
    :rtype: bool

    """

    found_rig = False
    if camera_xform.hasAttr('fragParent'):
        frag_parent = camera_xform.fragParent.listConnections()
        if frag_parent:
            found_rig = True
    return found_rig


def get_camera_flag_from_camera(camera_xform):
    """
    Finds the camera flag for a given camera.

    :param pm.nt.Transform camera_xform: Camera to find flag for
    :return: Returns the flag or None if no flag found.
    :rtype: pm.nt.Transform or None
    """
    cam_flag = None
    if camera_xform.hasAttr('fragParent'):
        frag_parent = camera_xform.fragParent.listConnections()
        if frag_parent:
            camera_component = frag.FRAGNode(frag_parent[0])
            cam_flag = camera_component.get_cam_flag()
    return cam_flag


def get_camera_from_flag(flag_node):
    """
    Finds the constrained camera from a flag node on a camera rig.

    :param pm.nt.Transform flag_node: Flag node on the camera rig.
    :return: Returns the camera or None if no camera is found.
    :rtype: pm.nt.Transform or None

    """
    frag_rig_node = frag_rig.get_frag_rig(flag_node)
    if not frag_rig_node:
        logger.warning(f'{flag_node} is not part of a FRAG rig.')
        return None
    camera_component = frag_rig_node.get_frag_children(of_type=frag.CameraComponent)

    if not camera_component:
        logger.warning(f'Could not find camera component for {flag_node}.')
        return None

    cam = camera_component[0].get_cam()
    return cam



def select_camera_from_flag_cmd():
    """
    Command to select the camera from a flag node on a camera rig.

    """

    selected_objs = pm.selected()
    if selected_objs:
        flag_node = selected_objs[0]
        cam = get_camera_from_flag(flag_node)
        if cam:
            pm.select(cam, r=True)
    else:
        logger.warning('Please select a camera rig.')



def copy_camera_cmd():
    """
    Command to copy settings between selected cameras

    """

    selection_list = pm.selected()
    camera_list = []
    for obj in selection_list:
        if isinstance(obj, pm.nt.Camera):
            camera_xform = obj.getTransform()
            camera_list.append(camera_xform)
        elif isinstance(obj, pm.nt.Transform):
            obj_shape = obj.getShape()
            if isinstance(obj_shape, pm.nt.Camera):
                camera_list.append(obj)
            else:
                cam_from_flag = get_camera_from_flag(obj)
                if cam_from_flag:
                    camera_list.append(cam_from_flag)
    if len(camera_list) > 1:
        copy_camera(camera_list)
    else:
        maya_dialogs.info_prompt('Copy Camera Error', 'Please select at least two cameras or camera rigs.', icon='error')


def copy_camera(camera_list):
    """
    Copies focal length settings and matches position of two cameras.

    """

    if not len(camera_list) > 1:
        return
    copy_from_cam = camera_list[0]
    copy_to_cams = camera_list[1:]
    for copy_to_cam in copy_to_cams:
        copy_to_cam.focalLength.setLocked(False)
        focal_length = copy_from_cam.focalLength.get()
        copy_to_cam.focalLength.set(focal_length)
        if copy_to_cam.listConnections(type=pm.nt.Constraint):
            if camera_is_rigged(copy_to_cam):
                camera_obj = get_camera_flag_from_camera(copy_to_cam)
            else:
                logger.warning(f'{copy_to_cam} is constrained but not to a rig.')
                continue
        else:
            camera_obj = copy_to_cam
        con = constraint_utils.parent_constraint_safe(copy_from_cam, camera_obj, mo=False)
        if con:
            if pm.keyframe(camera_obj, q=True, kc=True):
                pm.setKeyframe(camera_obj)
            pm.delete(con)
        logger.info(f'Camera settings copied from {copy_from_cam.name()} to {copy_to_cam.name()}.')

