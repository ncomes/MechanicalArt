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
from mca.ue.utils import asset_utils

logger = log.MCA_LOGGER


def import_asset(filename, game_path, asset_name, import_options=None, replace_existing=True, save=False):
    """
    Imports an asset into Unreal

    :param str filename: full file name path to the FBX.
    :param str game_path: Folder path to the asset.  This does not include the asset name.
    :param str asset_name: Name of the asset.
    :param unreal.FbxImportUI import_options: This sets the options on the import window.
    :param bool replace_existing: If True, the asset will be overwritten.
    :param bool save: If True, the asset will be saved.
    :return:  Returns the unreal.Object instance
    :rtype: unreal.Object
    """

    # Create an import task
    import_task = unreal.AssetImportTask()

    # Set base properties on the import task
    import_task.filename = filename
    import_task.destination_path = game_path
    import_task.destination_name = asset_name
    import_task.automated = True  # Suppress UI
    import_task.set_editor_property('replace_existing', replace_existing)
    import_task.set_editor_property('save', save)

    if import_options:
        import_task.options = import_options

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])

    imported_assets = import_task.get_editor_property('imported_object_paths')

    if not imported_assets:
        logger.warning(f'{asset_name}: was not imported!')
        return

    # Return the instance of the imported asset
    asset = imported_assets[0]
    asset = unreal.EditorAssetLibrary.find_asset_data(asset).get_asset()
    asset_utils.save_asset(asset)
    return unreal.load_asset(imported_assets[0])


def texture_2d_import_options():
    """
    Returns the import options for the texture 2d import window.

    :return: Returns the import options for the texture 2d import window.
    :rtype: unreal.FbxImportUI
    """

    options = unreal.FbxImportUI()
    options.import_textures = True
    return options






