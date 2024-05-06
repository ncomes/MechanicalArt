#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains installer related functions for Autodesk Maya
"""

# System global imports
import os
# software specific imports
# mca python imports
from mca.common.paths import project_paths, paths

UE_ROOT = project_paths.MCA_UNREAL_ROOT


def ue_content_path():
    string_path = r'unreal\Game\Content\DarkWinter'
    full_path = os.path.join(UE_ROOT, string_path)
    return os.path.normpath(full_path)


def ue_characters_path():
    string_path = 'Characters'
    full_path = os.path.join(ue_content_path(), string_path)
    return os.path.normpath(full_path)


def get_local_tool_prefs_folder(tool_name):
    return paths.get_local_tools_prefs_folder(dcc='Unreal', tool_name=tool_name)


def get_tool_prefs_folder(tool_name):
    art_tools_path = paths.get_common_tools_path()
    tool_path = os.path.join(art_tools_path, 'Unreal', tool_name)
    return os.path.normpath(tool_path)


def get_asset_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    asset_path = os.path.join(ue_content_path(), paths.get_asset_path(asset_id=asset_id))
    return os.path.normpath(asset_path+'\\')


def asset_texture_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    asset_path = os.path.join(get_asset_path(asset_id), 'Textures')
    return os.path.normpath(asset_path)


def asset_meshes_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    asset_path = os.path.join(get_asset_path(asset_id), 'Meshes')
    return os.path.normpath(asset_path)


def asset_animations_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    asset_path = os.path.join(get_asset_path(asset_id), 'Animations')
    return os.path.normpath(asset_path)


def asset_materials_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    asset_path = os.path.join(get_asset_path(asset_id), 'Materials')
    asset_path = os.path.normpath(asset_path)
    return asset_path.replace('\\', '/') + '/'


def get_plugins_path():
    _path = os.path.dirname(os.path.dirname(ue_content_path()))
    plugin_path = os.path.join(_path, 'Plugins')
    return os.path.normpath(plugin_path)


def get_void_character_path():
    _path = get_plugins_path()
    void_path = os.path.join(_path, 'MAT', 'MATCharacterVoid')
    return os.path.normpath(void_path)


def material_void_shaders_path():
    _path = os.path.join(get_void_character_path(), 'Content', 'MasterMaterials', 'Characters',
                         'Shaders')
    return os.path.normpath(_path)


def get_default_ini():
    return os.path.join(ue_content_path(), 'unreal', 'Game', 'Config', 'DefaultEngine.ini')

