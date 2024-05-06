# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports
# software specific imports
# mca python imports
from mca.ue.texturetypes import texture_2d


class PyTexture2D(texture_2d.PyTexture2D):
    def __init__(self, u_asset):
        super().__init__(u_asset)


class PyDiffuse(texture_2d.PyDiffuse):
    def __init__(self, u_asset):
        super().__init__(u_asset)


class PyNormalMap(texture_2d.PyDiffuse):
    def __init__(self, u_asset):
        super().__init__(u_asset)


class PyORME(texture_2d.PyDiffuse):
    def __init__(self, u_asset):
        super().__init__(u_asset)


class PySSTD(texture_2d.PyDiffuse):
    def __init__(self, u_asset):
        super().__init__(u_asset)


def get_list_of_textures_from_path(abs_path, game_path=None, convert_to_pynodes=True):
    """
    Returns a list of texture files in the given path.  Full Paths.

    :param str abs_path: The absolute path to the texture's folder.
    :param str game_path: The game path to the texture's folder.
    :param bool convert_to_pynodes: If True, the textures will be converted to pynodes.
    :return: Returns a list of texture files in the given path.
    :rtype: list[general.PyNode]
    """

    return texture_2d.get_list_of_textures_from_path(abs_path=abs_path,
                                                     game_path=game_path,
                                                     convert_to_pynodes=convert_to_pynodes)


def get_textures_paths_from_mca_inst_path(mat_inst_folder):
    """
    Returns a dictionary with the following keys:
    - 'game_paths': The path to the game's material instance constant texture's folder.
    - 'full_paths': The absolute path to the material instance constant texture's folder.

    :param str mat_inst_folder: path to the material instance constant.
    :return: Returns a dictionary with the game path and the full path to the texture's folder.
    :rtype: dict
    """

    return texture_2d.get_textures_paths_from_mca_inst_path(mat_inst_folder=mat_inst_folder)

