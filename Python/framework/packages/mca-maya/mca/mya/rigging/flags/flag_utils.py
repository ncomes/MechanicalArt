#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that interact with the rig flags
"""

# mca python imports
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
from mca.mya.utils import attr_utils, display_layers
from mca.mya.rigging import frag
from mca.mya.pyqt import dialogs

logger = log.MCA_LOGGER


def zero_flags_cmd():
    selection = pm.selected()
    if not selection:
        dialogs.info_prompt(title='Nothing Selected', text='Please select a FRAG rig.')
        return
    zero_flags(selection)
    

@decorators.track_fnc
def zero_flags(node_list):
    """
    Sets all the flag attributes that are keyable back to their default values.

    :param list(pm.nt.PyNode) node_list: List of nodes connected to a rig
    """
    
    if not node_list:
        logger.warning('Please select a flag.')
        return
    
    frag_rigs = []
    
    for node in node_list:
        frag_rig = frag.get_frag_rig(node)
        if frag_rig:
            frag_rigs.append(frag_rig)
    
    frag_rigs = list(set(frag_rigs))
    for frag_rig in frag_rigs:
        [attr_utils.reset_attrs(x) for x in frag_rig.get_flags()]


@decorators.track_fnc
def flags_visibility(node_list, toggle=False, on=False):
    """
    Toggles the visibility layer for the flags.

    :param list(pm.nt.PyNode) node_list: List of nodes connected to a rig
    :param bool toggle: uses the function as a toggle.  If toggle is true, the 'on' flag will not be used.
    :param bool on: If True, the flags layer will be visible.  If False, the flags layer will not be visible.
    """
    
    if not node_list:
        logger.warning('Please select a flag.')
        return
    
    frag_rigs = []
    
    for node in node_list:
        frag_rig = frag.get_frag_rig(node)
        if frag_rig:
            frag_rigs.append(frag_rig)
    
    frag_rigs = list(set(frag_rigs))
    for frag_rig in frag_rigs:
        flags = frag_rig.get_flags()
        display_lyrs = display_layers.get_display_layers(flags)
        if not display_lyrs:
            logger.warning(f'{frag_rig.pynode}: Rig is not not under a layer.')
            continue
        if toggle:
            value = display_lyrs[0].v.get()
            [x.v.set(not value) for x in display_lyrs]
            continue
        
        [x.v.set(on) for x in display_lyrs]


def select_all_flags_cmd():
    selection = pm.selected()
    if not selection:
        dialogs.info_prompt(title='Select All', text='Please make sure you select at least one FRAG rig!')
        logger.warning('Please make sure you select at least one FRAG rig!')
        return
    select_all_flags(selection)


@decorators.track_fnc
def select_all_flags(node_list):
    """
    Selects all the flag for the selected rigs.

    :param list(pm.nt.PyNode) node_list: List of nodes connected to a rig
    """
    
    if not node_list:
        logger.warning('Please select a flag.')
        return
    
    frag_rigs = []
    
    for node in node_list:
        frag_rig = frag.get_frag_rig(node)
        if frag_rig:
            frag_rigs.append(frag_rig)
    
    frag_rigs = list(set(frag_rigs))
    for frag_rig in frag_rigs:
        pm.select(frag_rig.get_flags())


def cut_all_flag_animations(rig_node):
    """
    Cut animation from all the flags on a rig.

    :param pm.nt.dagNode rig_node: a node on the rig.
    :return: Returns if True, the keys were cut successfully
    :rtype: bool
    """
    
    frag_rig = frag.get_frag_rig(rig_node)
    if not frag_rig:
        return False
    flags = frag_rig.get_flags()
    [pm.cutKey(x) for x in flags]
    zero_flags(flags)
    return True

