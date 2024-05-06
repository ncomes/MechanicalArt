# -*- coding: utf-8 -*-

"""
MAT version of Parent Materials.  These modules allow users to interact with Parent Materials.
"""

# mca python imports
import os
# software specific imports
# mca python imports
from mca.common import log
from mca.common.textio import yamlio
from mca.common.paths import paths
from mca.ue.paths import ue_paths
from mca.ue.utils import materials

logger = log.MCA_LOGGER


def get_parent_materials(texture_list):
    """
    Returns the parent material for the MaterialInstanceConstant object.
    This is a bit of a guess.  If there is the word Eye in the name it is probably the character_eyeball_master.
    If there is the word SSTD in the name it is probably the character_master.
    Else it is probably the master_character_duel_skin.

    :param list(str) texture_list: List of texture names associated with the MaterialInstanceConstant
    :return: Returns the parent material for the MaterialInstanceConstant object.
    :rtype: unreal.Material
    """

    if '_eyewet' in texture_list[0].name.lower():
        base_mtl = materials.get_character_eye_wet_master()
        return base_mtl

    elif '_eye' in texture_list[0].name.lower():
        base_mtl = materials.get_character_eyeball_master()
        return base_mtl

    sstd = False
    for texture in texture_list:
        if 'sstd' in texture.name.lower():
            sstd = True
            break

    if not sstd:
        base_mtl = materials.get_character_master()
    else:
        base_mtl = materials.get_master_character_duel_skin()

    return base_mtl


def get_local_asset_import_prefs(filename):
    """
    Returns the local parent default preferences.
    This file contains information about a specific parent material on the local machine.

    :param str filename: Name of the properties file.
    :return: Returns the local parent default preferences.
    :rtype: dict
    """

    local_prefs = paths.get_local_tools_prefs_folder('unreal', 'parent_materials')
    local_prefs = os.path.join(local_prefs, filename)
    if not '.properties' in local_prefs:
        local_prefs += '.properties'
    if not os.path.exists(local_prefs):
        common_file = get_asset_import_prefs(filename)
        common_data = yamlio.read_yaml_file(common_file)
        try:
            yamlio.write_to_yaml_file(common_data, local_prefs)
        except:
            yamlio.write_to_yaml_file({}, local_prefs)

    return local_prefs


def get_asset_import_prefs(filename):
    """
    Returns the shared parent default preferences.
    This file contains information about a specific parent material in the Tools/Common folder.

    :param str filename: Name of the properties file.
    :return: Returns the shared parent default preferences.
    :rtype: dict
    """

    common_prefs = ue_paths.get_tool_prefs_folder('parent_materials')
    local_prefs = os.path.join(common_prefs, filename)
    if not '.properties' in common_prefs:
        common_prefs += '.properties'
    if not os.path.exists(common_prefs):
        yamlio.write_to_yaml_file({}, common_prefs)

    return common_prefs
