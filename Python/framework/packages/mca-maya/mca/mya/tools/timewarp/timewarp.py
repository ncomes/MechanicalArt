#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Test tool implementation.
"""

# System global imports
import os
# Software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.utils import list_utils
from mca.mya.animation import baking
from mca.mya.utils import attr_utils
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import flags


logger = log.MCA_LOGGER


class Timewarp(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'TimewarpUI.ui')
        super().__init__(title='Timewarp',
                         ui_path=ui_path,
                         version=Timewarp.VERSION)
        
        # ==============================
        # Signals
        # ==============================
        self.ui.add_pushButton.clicked.connect(add_objects_to_timewarp_cmd)
        self.ui.remove_pushButton.clicked.connect(remove_objects_from_timewarp_cmd)
        self.ui.get_all_pushButton.clicked.connect(get_all_timewarped_nodes_cmd)

        self.ui.bake_pushButton.clicked.connect(bake_timewarp)
        self.ui.delete_pushButton.clicked.connect(remove_timewarp)
    # ==============================
    # Slots
    # ==============================


def get_timewarp(create_new=True):
    """
    Return or build a new timewarp control.

    :param bool create_new: If unable to find a timewarp system create a new one.
    :return: The control that represents a new timewarp system in the scene.
    :rtype: Transform
    """

    time_control = list_utils.get_first_in_list(pm.ls('*.timewarp_node', o=True))

    if not time_control:
        if not create_new:
            return
        time_control = setup_timewarp_control()

    if not time_control.getAttr('timewarp_node'):
        setup_timewarp_node(time_control)

    if not time_control.getAttr('animation_layer'):
        setup_timewarp_layer(time_control)

    return time_control


def setup_timewarp_control():
    """
    Create a new control object for the timewarp system. This generates the flag and required attributes.

    :return: The control that represents a new timewarp system in the scene.
    :rtype: Transform
    """

    sca = 125
    # main face
    time_control = pm.curve(p=[(sca * .8528, 0, 0), (0, 0, sca * .8528), ((sca * -.8528), 0, 0), (0, 0, (sca * -.8528)),
                               (sca * .8528, 0, 0), (0, 0, sca * .8528), ((sca * -.8528), 0, 0),
                               (0, 0, (sca * -.8528))], per=1, k=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], d=4,
                            n="timewarp_flag")
    curve_list = []

    # hands
    curve_list.append(pm.curve(p=[(0, 0, 0), (0, 0, sca * -.1), (0, 0, sca * -.2), (0, 0, sca * -.35)]))
    curve_list.append(
        pm.curve(p=[(0, 0, 0), (sca * .05, 0, sca * -.05), (sca * .1, 0, sca * -.1), (sca * .15, 0, sca * -.15)]))

    # ticks
    curve_list.append(pm.curve(p=[(0, 0, sca * -.4), (0, 0, sca * -.42), (0, 0, sca * -.44), (0, 0, sca * -.45)]))
    curve_list.append(pm.curve(p=[(sca * .28, 0, sca * -.28), (sca * .29, 0, sca * -.29), (sca * .31, 0, sca * -.31),
                                  (sca * .32, 0, sca * -.32)]))
    curve_list.append(pm.curve(p=[(sca * .4, 0, 0), (sca * .42, 0, 0), (sca * .44, 0, 0), (sca * .45, 0, 0)]))
    curve_list.append(pm.curve(
        p=[(sca * .28, 0, sca * .28), (sca * .29, 0, sca * .29), (sca * .31, 0, sca * .31), (sca * .32, 0, sca * .32)]))
    curve_list.append(pm.curve(p=[(0, 0, sca * .4), (0, 0, sca * .42), (0, 0, sca * .44), (0, 0, sca * .45)]))
    curve_list.append(pm.curve(p=[(sca * -.28, 0, sca * .28), (sca * -.29, 0, sca * .29), (sca * -.31, 0, sca * .31),
                                  (sca * -.32, 0, sca * .32)]))
    curve_list.append(pm.curve(p=[(sca * -.4, 0, 0), (sca * -.42, 0, 0), (sca * -.44, 0, 0), (sca * -.45, 0, 0)]))
    curve_list.append(pm.curve(p=[(sca * -.28, 0, sca * -.28), (sca * -.29, 0, sca * -.29), (sca * -.31, 0, sca * -.31),
                                  (sca * -.32, 0, sca * -.32)]))

    for x in curve_list:
        pm.parent(x.getShape(), time_control, shape=1, r=1), pm.delete(x)

    time_control.addAttr('timewarp_node', h=False, k=False, at='message')
    time_control.addAttr('animation_layer', h=False, k=False, at='message')
    time_control.addAttr('timewarp_input', dv=0.0, k=True)

    attr_utils.set_attr_state(time_control, attr_utils.TRANSFORM_ATTRS+['v'])

    return time_control


def setup_timewarp_layer(time_control):
    """
    Creates a new animation layer for the timewarp system to work with.

    :param Transform time_control: The control that represents a timewarp system in the scene.
    """

    animation_layer = list_utils.get_first_in_list(pm.ls('Timewarp_Selection', type=pm.nt.AnimLayer))
    animation_layer = animation_layer or pm.animLayer('Timewarp_Selection')
    if not time_control.hasAttr('animation_layer'):
        time_control.addAttr('animation_layer', h=False, k=False, at='message')
    animation_layer.message >> time_control.animation_layer
    animation_layer.addMember(time_control)


def setup_timewarp_node(time_control):
    """
    Creates a new timewarp node to link animation curves to. Which allows us to retime them by offsetting keys.

    :param Transform time_control: The control that represents a timewarp system in the scene.
    """

    timewarp_node = pm.createNode(pm.nt.TimeWarp)
    timewarp_node.rename('animation_timewarp')
    if not time_control.hasAttr('timewarp_node'):
        time_control.addAttr('timewarp_node', h=False, k=False, at='message')
    timewarp_node.message >> time_control.timewarp_node
    if not time_control.hasAttr('timewarp_input'):
        time_control.addAttr('timewarp_input', dv=0.0, k=True)
    time_control.timewarp_input >> timewarp_node.input


def add_remove_objects_from_timewarp(node_list, add_to_warp=True):
    """
    Add or remove objects from their connection to the scene's timewarp node.

    :param list[PyNode] node_list: A list of objects with keys on them.
    :param bool add_to_warp: If objects should be added or removed to the timewarp.
    """

    time_control = get_timewarp()

    timewarp_node = time_control.getAttr('timewarp_node')

    current_anim_curve_list = timewarp_node.listConnections(type=pm.nt.AnimCurve)
    curves_to_append = pm.listConnections(node_list, type=pm.nt.AnimCurve)

    if not curves_to_append:
        # no keyframes on selected objects.
        logger.warning('The selected objects have no animation curves. Set keys to use timewarp.')
        return

    if not current_anim_curve_list:
        # setup first time keys based on incoming curves.
        keyframe_range = pm.keyframe(curves_to_append, q=True)
        start_frame = min(keyframe_range)
        end_frame = max(keyframe_range)

        pm.setKeyframe(time_control.timewarp_input, t=start_frame, v=start_frame)
        pm.setKeyframe(time_control.timewarp_input, t=end_frame, v=end_frame)
        pm.keyTangent(time_control.timewarp_input, itt="linear", ott="linear")
        logger.debug(f'Start and end keys added {start_frame}, {end_frame}')

    timewarp_output_attr = time_control.getAttr('timewarp_node').output
    if add_to_warp:
        if not set(curves_to_append).issubset(current_anim_curve_list):
            # incoming curves are not already connected.
            for anim_curve in curves_to_append:
                if anim_curve not in current_anim_curve_list:
                    if anim_curve.input.listConnections():
                        # break previous connection if there was one.
                        anim_curve.input.disconnect()
                    timewarp_output_attr >> anim_curve.input
    else:
        for anim_curve in curves_to_append:
            # break connections to the timewarp.
            if timewarp_node in anim_curve.input.listConnections():
                timewarp_output_attr // anim_curve.input


def get_all_timewarped_nodes():
    """
    From the timewarp return all PyNodes that are connected to the override.

    :return: A list of all objects under the timewarp.
    :rtype: list[PyNode]
    """

    time_control = get_timewarp(create_new=False)
    if not time_control:
        # no timewrap present in the scene.
        logger.warning('This scene does not have an active timewarp.')
        return
    timewarp_node = time_control.getAttr('timewarp_node')
    current_anim_curve_list = timewarp_node.listConnections(type=pm.nt.AnimCurve)
    source_node_list = []
    for anim_curve in current_anim_curve_list:
        source_node = list_utils.get_first_in_list(anim_curve.output.listConnections())
        if source_node not in source_node_list:
            source_node_list.append(source_node)
    return source_node_list


def add_objects_to_timewarp_cmd():
    """
    Add objects to the scene's timewarp.

    """

    selection = pm.selected()
    filtered_selection = [x for x in selection if flags.is_flag(x)]
    add_remove_objects_from_timewarp(filtered_selection, True)


def remove_objects_from_timewarp_cmd():
    """
    Remove objects from the scene's timewarp.

    """

    selection = pm.selected()
    filtered_selection = [x for x in selection if flags.is_flag(x)]
    add_remove_objects_from_timewarp(filtered_selection, False)


def get_all_timewarped_nodes_cmd():
    """
    Select all objects overriden by the timewarp

    """

    pm.select(get_all_timewarped_nodes())


def remove_timewarp():
    """
    Remove the scenes timewarp and all associated nodes and layers.

    """

    things_to_delete = []
    for time_control in pm.ls('*.timewarp_node', o=True):
        things_to_delete.append(time_control)
        things_to_delete.append(time_control.getAttr('timewarp_node'))
        things_to_delete.append(time_control.getAttr('animation_layer'))
    pm.delete(things_to_delete)



def bake_timewarp():
    """
    Bake the scene's timewarp down and remove it.

    """

    time_control = get_timewarp(create_new=False)
    if not time_control:
        # no timewarp present in the scene.
        logger.warning('This scene does not have an active timewarp.')
        return
    timewarp_node = time_control.getAttr('timewarp_node')
    current_anim_curve_list = timewarp_node.listConnections(type=pm.nt.AnimCurve)

    if not current_anim_curve_list:
        # no keys on the timewarp system.
        return

    bake_list = []
    for anim_curve in current_anim_curve_list:
        bake_list += [x for x in anim_curve.listConnections() if x != timewarp_node and x not in bake_list]

    keyframe_range = pm.keyframe(current_anim_curve_list, q=True)
    start_frame = min(keyframe_range)
    end_frame = max(keyframe_range)

    baking.bake_objects(bake_list, bake_range=[start_frame, end_frame])
    remove_timewarp()
