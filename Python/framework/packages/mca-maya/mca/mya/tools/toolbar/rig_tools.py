#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.common.assetlist import assetlist
from mca.common.utils import list_utils, string_utils

from mca.mya.animation import baking, time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import maya_dialogs
from mca.mya.utils import constraint_utils, dag_utils, naming, namespace_utils

from mca.mya.rigging import frag, flags

from mca.common import log
logger = log.MCA_LOGGER


@ma_decorators.keep_selection_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_autokey_decorator
@ma_decorators.keep_current_frame_decorator
def attach_rigs_cmd():
    """
    Given a selection or two rigs, match up their components by side and region then constrain their flags.

    """

    selection = pm.selected()

    if not selection or len(selection) < 2:
        maya_dialogs.info_prompt(title='No Selections', text='Please select exactly two separate FRAG rigs')
        return

    rig_list = []
    for selected_node in selection:
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            rig_list.append(frag_rig)

    if not rig_list or rig_list[0] == rig_list[-1]:
        maya_dialogs.info_prompt(title='No Selections', text='Please select exactly two separate FRAG rigs')
        return
    for frag_rig in rig_list:
        asset_id = frag_rig.asset_id
        asset_entry = assetlist.get_asset_by_id(asset_id)
        if asset_entry:
            if 'head' in asset_entry.asset_subtype:
                attached_rig = frag_rig
                driver_rig = [x for x in rig_list if x != attached_rig][0]
                break
    else:
        driver_rig, attached_rig = rig_list
    frag.attach_rigs(driver_rig, attached_rig)


@ma_decorators.keep_selection_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_autokey_decorator
@ma_decorators.keep_current_frame_decorator
def detach_rig_cmd(bake_animation=False, start_frame=None, end_frame=None):
    """
    Wrapped fnc for the detach_rig fnc.

    :param bake_animation: If the animation should be baked down to the attached rig.
    :param int start_frame: The first frame in the bake range.
    :param int end_frame: The last frame in the bake range.
    """
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt(title='Select a rig', text='Please select a FRAG rig')
        return

    selected_node = list_utils.get_first_in_list(selection)
    frag_rig = frag.get_frag_rig(selected_node)

    if not frag_rig:
        maya_dialogs.info_prompt(title='Select a rig', text='Please select a FRAG rig')
        return

    frag.detach_rig(frag_rig, bake_animation, start_frame, end_frame)
    asset_id = frag_rig.get_asset_id(frag_rig)
    return asset_id


@ma_decorators.keep_selection_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_autokey_decorator
@ma_decorators.keep_current_frame_decorator
def create_overdriver_cmd(skip_rotate_attrs=None, skip_translate_attrs=None, rotate_order=None):
    """
    Constrain a flag to a given driver object, or create and align a temporary driver object.

    :param int skip_rotate_attrs: If some axis should not be constrained by rotation
    :param int skip_translate_attrs: If some axis should not be constrained by translation
    :param int rotate_order: What rotation order should be used for the overdriver.
    """

    selection = pm.selected()

    if not selection:
        return

    skip_rotate_attrs = skip_rotate_attrs or []
    skip_translate_attrs = skip_translate_attrs or []

    driver_object = selection[0]
    driven_object = selection[-1]
    
    
    flag = None
    wrapped_flag = flags.is_flag(driven_object)
    if driver_object == driven_object and wrapped_flag:
        # If we only have one selection we're going to create a new override object
        driver_object = pm.spaceLocator(n=f'{naming.get_basename(driven_object)}_overdriver')
        pm.delete(pm.parentConstraint(driven_object, driver_object))
        flag = driven_object

    driven_keyframes = pm.keyframe(driven_object, q=True)
    driver_keyframes = pm.keyframe(driver_object, q=True)
    if driven_keyframes and not driver_keyframes:
        temp_constraint = constraint_utils.parent_constraint_safe(driven_object, driver_object, mo=True)
        baking.bake_objects(driver_object, bake_range=[min(driven_keyframes), max(driven_keyframes)])
        pm.delete(temp_constraint)
    constraint_utils.parent_constraint_safe(driver_object, driven_object,
                                      skip_rotate_attrs=skip_rotate_attrs, skip_translate_attrs=skip_translate_attrs,  mo=True)
    if not driven_object.hasAttr('overdriven_by'):
        driven_object.addAttr('overdriven_by', at='message')
    driver_object.message >> driven_object.overdriven_by
    
    asset_id = ''
    if flag:
        frag_root = frag.get_frag_root(flag)
        asset_id = frag_root.asset_id
        return asset_id
    return asset_id


@ma_decorators.keep_selection_decorator
@ma_decorators.undo_decorator
@ma_decorators.keep_autokey_decorator
@ma_decorators.keep_current_frame_decorator
def bake_overdriver_cmd(bake_animation=True, start_frame=None, end_frame=None):
    """
    For any constrained flags, find their parent and bake the keyframe range found.

    :param bool bake_animation: If when removed animation should be baked back onto the driven object. (The Flag)
    :param int start_frame: The first frame in the bake range.
    :param int end_frame: The last frame in the bake range.
    """

    selection = pm.selected()

    constraint_list = []
    bakeable_node_list = []
    driver_list = []
    for node in selection:
        if not flags.is_flag(node):
            continue
        if node.hasAttr('overdriven_by') and node.getAttr('overdriven_by'):
            overdriver_constraint = list_utils.get_first_in_list(node.listRelatives(type=pm.nt.Constraint))
            if not overdriver_constraint:
                node.disconnectAttr('overdriven_by')
                logger.debug(f'{naming.get_basename(node)}, was not constrained.')
                continue
            constraint_list.append(overdriver_constraint)
            driver_object = node.getAttr('overdriven_by')
            driver_list.append(driver_object)
            bakeable_node_list.append(node)

    if bake_animation:
        if not start_frame or not end_frame:
            time_range = time_utils.get_times(driver_list)
            start_frame = start_frame or time_range[0]
            end_frame = end_frame or time_range[1]
        baking.bake_objects(bakeable_node_list, bake_range=[start_frame, end_frame])
    pm.delete(constraint_list)

def bake_skeleton_to_rig_cmd(start_frame=None, end_frame=None, append=None, motion_encode=None):
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt(title='Bake Skeleton to Rig', text='Please make sure you select at least one FRAG rig, and one skeleton.')
        return

    frag_rig = None
    skel_root = None
    for selected_node in selection:
        # search through our selection to find a valid frag root and a valid skeleton, grab the first of each.
        frag_rig = frag.get_frag_rig(selected_node)
        wrapped_flag = flags.is_flag(selected_node)
        if not skel_root and not wrapped_flag and isinstance(selected_node, pm.nt.Joint):
            skel_root = dag_utils.get_absolute_parent(selected_node, node_type=pm.nt.Joint, inclusive=True)

        if frag_rig and skel_root:
            break
    
    if not frag_rig:
        return
    
    if append:
        start_frame, end_frame = [None, None]
    frag_rig.bake_skeleton_to_rig(skel_root, start_frame, end_frame, append, motion_encode)

    return frag_rig

def bake_rig_to_skeleton_cmd(start_frame=None, end_frame=None, set_to_zero=True):
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt(title='Bake Rig to Skeleton', text='Please make sure you select at least one FRAG rig!')
        return
    
    frag_rig = None
    for selected_node in selection:
        # search through our selection to find a valid frag root, grab the first.
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            break
    
    if not frag_rig:
        return
    
    frag_rig.bake_rig_to_skeleton(start_frame, end_frame, set_to_zero)

    return frag_rig

def mirror_rig_cmd(start_frame=None, end_frame=None):
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt(title='Mirror Rig', text='Please make sure you select at least one FRAG rig!')
        return
    
    frag_rig = None
    for selected_node in selection:
        # search through our selection to find a valid frag root, grab the first.
        frag_rig = frag.get_frag_rig(selected_node)
        if frag_rig:
            break
    
    if not frag_rig:
        return
    
    if not start_frame or end_frame:
        start_frame, end_frame = time_utils.get_times()

    frag_rig.mirror_rig(start_frame, end_frame)

    return frag_rig

def reload_rig_cmd():
    """
    Wrapped fnc for the reload_rig fnc.

    """
    selection = pm.selected()
    asset_id_list = []
    if not selection:
        maya_dialogs.info_prompt(title='Reload Rig', text='Please make sure you select at least one FRAG rig!')
        logger.warning('Please make sure you select at least one FRAG rig!')
        return
    
    for x in selection:
        if not pm.objExists(x):
            continue
        frag_rig = frag.get_frag_rig(x)
        if frag_rig:
            asset_id_list.append(frag_rig.asset_id)
            frag_rig.reload()
    return asset_id_list

@ma_decorators.undo_decorator
def single_frame_ikfk_Switch_cmd():
    """
    Wrapped fnc for switch_align on all components with that capability.

    """
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt('Single frame ik/fk switch.', 'Please make sure you select at least one switchable flag.')
        logger.warning('Please make sure you select at one switchable flag.')
        return

    current_frame = None

    component_list = []
    for x in selection:
        found_component = frag.get_component(x)
        if found_component not in component_list and isinstance(found_component, frag.IKFKComponent):
            if not current_frame:
                current_frame = cmds.currentTime(q=True)
            component_list.append(found_component)
            flag_pynode_list = [x.pynode for x in found_component.flags]
            pm.setKeyframe(flag_pynode_list, t=current_frame-1)
            things_to_delete = found_component.switch_align()
            pm.setKeyframe(flag_pynode_list)
            pm.delete(things_to_delete)

@ma_decorators.undo_decorator
def ikfk_switch_cmd():
    """
    Wrapped fnc for switch_align on all components with that capability.

    """
    selection = pm.selected()
    if not selection:
        maya_dialogs.info_prompt('Full ik/fk switch.', 'Please make sure you select at least one switchable flag.')
        logger.warning('Please make sure you select at one switchable flag.')
        return

    component_list = []
    all_flags = []
    things_to_delete = []
    for x in selection:
        found_component = frag.get_component(x)
        if found_component not in component_list and isinstance(found_component, frag.IKFKComponent):
            component_list.append(found_component)
            all_flags += [x.pynode for x in found_component.flags]
            things_to_delete += found_component.switch_align()
    
    if all_flags:
        time_range = time_utils.get_times(all_flags)
        baking.bake_objects(all_flags, bake_range=time_range)

@ma_decorators.keep_namespace_decorator
@ma_decorators.keep_autokey_decorator
@ma_decorators.keep_selection_decorator
@ma_decorators.keep_current_frame_decorator
@ma_decorators.undo_decorator
def switch_multiconstraint(rig_multi_dict, switch_target, start_frame=None, end_frame=None):
    """
    Switch a rig's multicconstraint target, and bake animation across.

    :param dict{FRAGRig list(FRAGAnimatedComponent)} rig_multi_dict: A dictionary containing FRAGRigs and a list of mulitconstraints to be switched.
    :param Transform switch_target: The object the multiconstraints will be switched to.
    :param int start_frame: The first frame in the bake range.
    :param int end_frame: The last frame in the bake range.
    """

    root_namespace = ''

    temp_namespace = string_utils.generate_random_string(5)
    namespace_utils.set_namespace(temp_namespace)
    flag_list = []
    pm.autoKeyframe(state=False)
    rig = None
    for frag_rig, multi_constraint_list in rig_multi_dict.items():
        frag_root = frag_rig.get_frag_root()
        all_grp = frag_root.asset_group
        driver_all_grp = pm.duplicate(all_grp, upstreamNodes=True, returnRootsOnly=True)[0]
        driver_rig = frag.FRAGNode(driver_all_grp.getAttr('frag_parent'))
        rig = frag_rig

        for multiconstraint_node in multi_constraint_list:
            root_namespace = multiconstraint_node.namespace()

            switch_node = multiconstraint_node.pynode.getAttr('switch_node')
            source_node = multiconstraint_node.pynode.getAttr('source_node')

            rig_component = frag.get_component(source_node)
            flag_index = rig_component.flags.index(source_node)

            driver_component = list_utils.get_first_in_list(driver_rig.get_frag_children(None, rig_component.side, rig_component.region))
            driver_source_node = driver_component.flags[flag_index]

            attr_target_dict = switch_node.follow.getEnums()
            target_name = naming.get_basename(switch_target)
            if target_name in attr_target_dict:
                pm.cutKey(switch_node.follow)
                switch_node.setAttr('follow', attr_target_dict[target_name])
            else:
                # failed to find switch target.
                continue

            # since we're aligning flag to flag from a duplicate rig we don't need to zero either first
            constraint_utils.parent_constraint_safe(driver_source_node, source_node)
            flag_list.append(source_node)
            # snap frame to catch up constraints.
            cmds.currentTime(-1337)

    start_frame, end_frame = (start_frame, end_frame) if None not in [start_frame, end_frame] else time_utils.get_times(flag_list)

    namespace_utils.set_namespace(root_namespace)
    baking.bake_objects(flag_list, bake_range=[start_frame, end_frame])
    namespace_utils.purge_namespace(temp_namespace)
    if rig:
        return rig.get_asset_id(rig)
    return
