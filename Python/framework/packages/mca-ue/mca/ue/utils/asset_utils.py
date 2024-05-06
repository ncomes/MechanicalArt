#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.assettypes import asset_mapping, py_material_instance
from mca.ue.texturetypes import texture_2d

logger = log.MCA_LOGGER


def PyNode(u_asset):
    """
    Returns either a PyUnreal Asset or an Unreal Asset
    :param unreal.Object u_asset: an Unreal Asset
    :return:
    """

    if u_asset.__class__ == unreal.Texture2D:
        defined = texture_2d.TextureMapping.attr(u_asset)

    elif u_asset.__class__ == unreal.MaterialInstanceConstant:
        parent_material = u_asset.get_editor_property('parent')
        if parent_material:
            py_class = py_material_instance.ParentMaterialMapping.attr(parent_material)
            defined = py_class(u_asset)
        else:
            defined = u_asset

    else:
        defined = asset_mapping.AssetMapping.attr(u_asset)

    if defined == u_asset:
        logger.info(defined)

    return defined


def selected():
    """
    Returns a list of either Unreal Assets or PyUnreal Assets

    :return: Returns a list of either Unreal Assets or PyUnreal Assets
    :rtype: list[unreal.Object or PyUnreal.PyNode]
    """

    utility_base = unreal.GlobalEditorUtilityBase.get_default_object()
    selected_assets = list(utility_base.get_selected_assets())
    defined_list = []

    for selection in selected_assets:
        defined_list.append(PyNode(selection))
    return defined_list


def get_assets_in_path(path, asset_type=None):
    """
    Returns the asset objects in the given game path.

    :param str path: Directory where assets are located
    :param str asset_type: The asset type.  For example: 'StaticMesh' or 'SkeletalMesh'
    :return: Returns the asset objects in the given path
    :rtype: list[Asset Class]
    """

    eal = unreal.EditorAssetLibrary()
    asset_full_names = eal.list_assets(path)
    assets = []
    if not asset_full_names:
        return
    for asset in asset_full_names:
        asset_data = eal.find_asset_data(asset)
        if not asset_data.is_u_asset:
            continue
        if asset_type:
            class_type = asset_data.get_asset().__class__.__name__
            if class_type != asset_type:
                continue
        assets.append(asset_data.get_asset())
    return assets


def save_asset(asset_list, force_save=False):
    """
    Saves the given asset objects.

    :param list[object] asset_list: List of asset objects to save
    :param bool force_save: If True, will save regardless the asset is dirty or not.
    :return: True if all assets were saved correctly.  False if not. the false assets are returned.
    :rtype: bool, list[unreal.Object]
    """

    failed_assets = []
    only_if_is_dirty = not force_save
    asset_list = asset_list if isinstance(asset_list, (tuple, list)) else [asset_list]

    for asset in asset_list:
        try:
            asset_path = asset.get_full_name()
        except:
            asset_path = asset.path
        if unreal.EditorAssetLibrary.save_asset(asset_path, only_if_is_dirty):
            logger.info(f'Saved newly created asset: {asset_path}')
        else:
            logger.warning(f'Failed to save newly created asset: {asset_path}')
            failed_assets.append(asset)
    return len(failed_assets) == 0, failed_assets


def get_selected_assets():
    """
    Returns the Unreal Assets (only) that are selected in the editor.

    :return: Returns the Unreal Assets that are selected in the editor.
    :rtype: list[unreal.Object]
    """

    utility_base = unreal.GlobalEditorUtilityBase.get_default_object()
    return list(utility_base.get_selected_assets())


def set_meta_tags_on_asset(asset, tags):
    """
    Sets the metadata of a string attribute on the given asset.

    :param object asset: Asset object that has metadata.
    :param list(str) tags: Tag to set onto the asset.
    """

    for tag in tags:
        unreal.EditorAssetLibrary.set_metadata_tag(asset, tag, tags[tag])


def get_meta_tags_on_asset(asset, tag):
    """
    Returns the metadata from a string attribute on the given asset.

    :param object asset: Asset object that has metadata
    :param str tag: Tagged attributes to query from asset
    :return: Returns the metadata from a string attribute on the given asset.
    :rtype: str
    """

    return unreal.EditorAssetLibrary.get_metadata_tag(asset, tag)