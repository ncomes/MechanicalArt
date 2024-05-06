#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains installer related functions for Autodesk Maya
"""

# System global imports
# software specific imports
import unreal
# mca python imports
from mca.common.utils import fileio


def rename_asset(new_name=None):
    """
    Renames a selected asset
    
    :param str new_name: new string name.
    """
    
    if not new_name:
        new_name = 'SK_HealingSkull'
    system_lib = unreal.SystemLibrary()
    editor_util = unreal.EditorUtilityLibrary()
    string_lib = unreal.StringLibrary()
    asset_lib = unreal.EditorAssetLibrary()
    
    # get the selected assets
    
    selected_assets = editor_util.get_selected_assets()
    if not selected_assets:
        unreal.log(f"Selected Please Select an Asset!")
        return
    asset = selected_assets[0]
    asset_name = system_lib.get_object_name(asset)
    unreal.log(f'Asset Name: {asset}\nAsset Path: {asset_lib.get_path_name_for_loaded_asset(asset)}')
    editor_util.rename_asset(asset, new_name)

