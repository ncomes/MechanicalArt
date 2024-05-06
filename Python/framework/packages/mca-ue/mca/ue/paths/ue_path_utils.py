#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains installer related functions for Autodesk Maya
"""

# System global imports
import os
# software specific imports
import unreal
# mca python imports
from mca.common.paths import project_paths
from mca.common import log

UE_ROOT = project_paths.MCA_UNREAL_ROOT.replace('\\', '/')
ART_ROOT = project_paths.# mca python importsPLASTIC_ROOT.replace('\\', '/')
logger = log.MCA_LOGGER


def get_asset_path(asset):
    """
    Returns the relative asset path
    :param str asset: String asset name
    :return: Returns the relative asset str
    :rtype: str
    """

    asset_lib = unreal.EditorAssetLibrary()
    unreal.log(f'Asset Name: {asset}\nAsset Path: {asset_lib.get_path_name_for_loaded_asset(asset)}')
    unreal.log(f'fname: {asset.get_fname()}')
    

def get_current_content_browser_path():
    """
    Returns the current path from the content browser
    
    :return: Returns the current path from the content browser
    :rtype: str
    """
    
    path = unreal.EditorUtilityLibrary.get_current_content_browser_path()
    unreal.log(f'Current Content Browser Path:\n{path}')
    return path


def is_game_path(file_path):
    if os.path.normpath('/Game/DarkWinter/') in os.path.normpath(file_path):
        return True
    return False


def is_game_texture_path(file_path):
    if not is_game_path(file_path) or 'Textures' != os.path.basename(file_path):
        return False
    return True


def is_game_material_path(file_path):
    if not is_game_path(file_path) or 'Materials' != os.path.basename(file_path):
        return False
    return True


def to_relative_path(file_path):
    """
    Convert a path to a project relative path by replacing the project path start.

    :param str file_path: A full path to a given file.
    :return: A path replacing the project path.
    :rtype: str
    """

    if not file_path:
        return None
    file_path = os.path.normpath(file_path)
    # strip the leading slashes here or we won't be able to join the paths later.
    if 'darkwinter' in file_path:
        seperator = os.path.split(UE_ROOT)[-1]
    else:
        seperator = 'DarkWinter'
    split_path = file_path.split(seperator)[-1]
    rel_path = split_path if not split_path.startswith('\\') else split_path[1:]
    if 'unreal' in rel_path:
        rel_path = rel_path.replace('unreal', '')
    return rel_path


def convert_to_game_path(file_path, add_slash=True):
    """
    Returns the game path for the given asset file.

    :param str file_path: A full path to a given file.
    :param bool add_slash: If True, it will add a '/' at the end of the path.
    :return: Returns the game path for the given asset file.
    :rtype: str
    """

    game_path = to_relative_path(file_path)
    if 'Content/' in game_path or 'Content\\' in game_path:
        game_path = game_path.replace('Content/', '')
        game_path = game_path.replace('Content\\', '')
    slash = '/'
    if not add_slash:
        slash = ''
    game_path = game_path.replace('\\', '/') + slash
    return game_path


def convert_to_art_path(file_path, add_slash=False, suffix='FBX'):
    """
    Returns the art path for the given game asset file.  This converts the game path
    to the art path.

    :param str file_path: A full path to a given file.
    :param bool add_slash: If True, it will add a '/' at the end of the path.
    :return: Returns the game path for the given asset file.
    :rtype: str
    """

    _path = file_path.replace('/Game', '')
    if 'DarkWinter' in _path:
        _path = _path.replace('/DarkWinter', '')
    art_full_path = f'{ART_ROOT}{_path}'
    if '.' in art_full_path:
        art_full_path = art_full_path.split('.')[0] + f'.{suffix}'
    slash = '/'
    if not add_slash:
        slash = ''
    art_path = art_full_path.replace('\\', '/') + slash
    return art_path


def convert_art_path_to_game_path(file_path):
    """
    Returns the game path for the given art asset file.

    :param str file_path: file path to an art asset.
    :return: Returns the game path for the given art asset file.
    :rtype: str
    """

    relative_path = to_relative_path(file_path)
    game_path = os.path.join('Game', 'DarkWinter', relative_path)
    game_path = f'/{game_path.split(".")[0]}'
    return game_path.replace('\\', '/')


def convert_to_material_void_path(file_path):
    """
    Returns the material void path from the given asset file.

    :param str file_path: A full path to a given file.
    :return: Returns the material void path from the given asset file.
    :rtype: str
    """

    file_path = convert_to_game_path(file_path)
    file_list = file_path.split('\\')[4:]
    return '\\'.join(file_list)


def convert_to_project_path(file_path):
    """
    Returns the project path from the game path.

    :param str file_path: Game Path.
    :return: Returns the project path for the given asset file.
    :rtype: str
    """

    file_path = file_path.replace('\\', '/')
    path = file_path.replace('/Game/DarkWinter/', '/unreal/Game/Content/DarkWinter/')
    ue_root = UE_ROOT.replace('\\', '/')
    project_path = ue_root + path
    return os.path.normpath(project_path)


def convert_material_to_texture_path(file_path):
    """
    Returns the texture path from the given Material Path.

    :param str file_path: Path to an asset's Materials folder.
    :return: Returns the texture path from the given Material Path.
    :rtype: str
    """

    if not 'Materials' in os.path.basename(file_path):
        logger.warning('The folder needs to be a "Materials folder"')
        return

    if not is_game_path(file_path):
        logger.warning('Please make sure the file is in the game folder')
        return

    path = os.path.join(os.path.dirname(file_path), 'Textures')
    path = path.replace('\\', '/')
    return path


def convert_texture_to_material_path(file_path):
    """
    Returns the texture path from the given Textures Path.

    :param str file_path: Path to an asset's Textures folder.
    :return: Returns the material path from the given Material Path.
    :rtype: str
    """

    if not 'Textures' in os.path.basename(file_path):
        logger.warning('The folder needs to be a "Textures folder"')
        return

    if not is_game_path(file_path):
        logger.warning('Please make sure the file is in the game folder')
        return
    path = os.path.join(os.path.dirname(file_path), 'Materials')
    path = path.replace('\\', '/')
    return path


class UEPathManager:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        """
        Returns the path with correct format

        :return: Returns the path with correct format
        :rtype: str
        """

        return self._path.replace('\\', '/')

    @property
    def art_root(self):
        """
        Returns the root directory of the art repository.

        :return: Returns the root directory of the art repository.
        :rtype: str
        """

        return ART_ROOT.replace('\\', '/')

    @property
    def ue_root(self):
        """
        Returns the root directory of the game repository.

        :return: Returns the root directory of the game repository.
        :rtype: str
        """

        return UE_ROOT.replace('\\', '/')

    def is_full_game_path(self, path=None):
        """
        Checks to see if the path is a full path in the game repository.

        :param str path: Path to check.
        :return: Returns True if the path is a full game path, False otherwise.
        :rtype: bool
        """

        if not path:
            path = self.path
        if self.ue_root in path:
            return True
        return False

    def is_art_path(self, path=None):
        """
        Checks to see if the path is a full path in the art repository.

        :param str path: Path to check.
        :return: Returns True if the path is a full art path, False otherwise.
        :rtype: bool
        """

        if not path:
            path = self.path
        if self.art_root in path:
            return True
        return False

    def is_game_path(self, path=None):
        """
        Checks to see if the path is a relative unreal path in the game repository.

        :param str path: Path to check.
        :return: Returns True if the path is a relative unreal path in the game repository, False otherwise.
        :rtype: bool
        """

        if not path:
            path = self.path
        if path.startswith('/Game'):
            return True
        return False

    def convert_full_game_path_to_game_path(self, path=None, remove_filename=False):
        """
        Converts a full game path to a relative unreal path in the game repository.

        :param str path: Full game path to convert.
        :param bool remove_filename: If True, it will remove the filename.
        :return: Returns a relative unreal path in the game repository.
        :rtype: str
        """

        if not path:
            path = self.path
        if not self.is_full_game_path(path):
            return
        game_path = convert_to_game_path(path, add_slash=False)
        if remove_filename:
            game_path = os.path.dirname(game_path)
        return game_path

    def convert_art_path_to_game_path(self, path=None, remove_filename=False):
        """
        Converts a full art path to a relative unreal path in the game repository.

        :param str path: Full art path to convert.
        :param bool remove_filename: If True, it will remove the filename.
        :return: Returns a relative unreal path in the game repository.
        :rtype: str
        """

        if not path:
            path = self.path
        if not self.is_art_path(path):
            return
        game_path = convert_art_path_to_game_path(path)
        if remove_filename:
            game_path = os.path.dirname(game_path)
        return game_path

    def convert_game_path_to_art_path(self, path=None, remove_filename=False):
        """
        Converts a relative unreal game path to an art path in the art repository.

        :param str path: relative unreal game path to convert.
        :param bool remove_filename: If True, it will remove the filename.
        :return: Returns an art path in the art repository.
        :rtype: str
        """

        if not path:
            path = self.path

        if not self.is_game_path(path):
            return
        art_path = convert_to_art_path(path)
        if remove_filename:
            art_path = os.path.dirname(art_path)
        return art_path

