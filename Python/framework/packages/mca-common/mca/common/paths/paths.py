#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import ctypes.wintypes
import os

# software specific imports

# mca python imports
from mca import common
from mca.common.paths import project_paths, path_utils
from mca.common.startup.configs import consts
from mca.common.assetlist import assetlist
from mca.common.utils import dcc_util, lists


def get_common_tools_path():
    """
    Returns the path to the Tools folder in the ART Plastic directory
    
    :return: Returns the path to the Tools folder in the ART Plastic directory
    :rtype: str
    """
    
    path = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Common', 'Tools')
    return os.path.normpath(path)


def get_art_characters_path():
    """
    Returns the path to the Tools folder in the ART Plastic directory

    :return: Returns the path to the Tools folder in the ART Plastic directory
    :rtype: str
    """

    path = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Characters')
    return os.path.normpath(path)


def get_common_path():
    """
    Returns the path to the Tools/Common folder in the ART Plastic directory

    :return: Returns the path to the Tools/Common folder in the ART Plastic directory
    :rtype: path
    """
    
    path = os.path.join(project_paths.MCA_PROJECT_ROOT, 'Common')
    return os.path.normpath(path)


def get_dcc_tools_path():
    """
    Returns the path to the MCA\Tools\<dcc>

    :return: Returns the path to the MCA\Tools\<dcc> in the project directory
    :rtype: path
    """
    dcc_app = dcc_util.application()
    return os.path.normpath(os.path.join(get_common_tools_path(), dcc_app))


def get_documents_folder(absolute=True):
    """
    Returns the path to the user folder.

    :return: path to the user folder.
    :rtype: path
    """

    return project_paths.get_documents_folder(absolute=absolute)


def get_local_preferences_folder():
    """
    Returns the path to the user's mca preferences folder.

    :return: path to the user's mca preferences folder.
    :rtype: str
    """

    return project_paths.get_local_preferences_folder()


def get_dcc_prefs_folder(dcc):
    """
    Returns the path to the user's mca preferences folder to a specific dcc software.

    :param str dcc: Name of dcc software or folder to the preferences.
    :return: path to the user's mca preferences folder to a specific dcc software.
    :rtype: str
    """

    docs_folder = get_local_preferences_folder()
    prefs_folder = os.path.join(docs_folder, 'prefs', dcc)  # 'mca_preferences'
    return os.path.normpath(prefs_folder)


def get_local_tools_prefs_folder(dcc, tool_name):
    """
    Creates the folder where the local prefs lives.

    :param str dcc: the dcc software
    :param str tool_name: Name of the folder where the local prefs lives.
    :return: Returns the folder where the local prefs lives.
    :rtype: str
    """

    toolbox_folder = os.path.join(get_dcc_prefs_folder(dcc=dcc), tool_name)
    if not os.path.exists(toolbox_folder):
        os.makedirs(toolbox_folder)
    return toolbox_folder


def get_asset_list_path():
    """
    Returns the path to the asset list.

    :return: path to the asset list.
    :rtype: path
    """
    
    return os.path.normpath(os.path.join(get_common_path(), 'Asset List'))


def get_asset_list_file_path():
    """
    Returns the path to the asset list.

    :return: path to the asset list.
    :rtype: path
    """
    
    return os.path.join(get_common_tools_path(), r'Asset List\asset_list.yaml')


def get_common_face():
    """
    Returns the path to Tools/Common/Face.

    :return: path to Tools/Common/Face.
    :rtype: path
    """

    face_path = os.path.join(get_common_path(), 'Face')
    return os.path.normpath(face_path)


def get_common_skinning():
    """
    Returns the path to the common skinning folder.

    :return: Returns the path to the common skinning folder.
    :rtype: str
    """
    _path = os.path.join(get_common_path(), r'Skinning')
    return os.path.normpath(_path)


# CGP ASSET Path helpers.
def get_asset_path(asset_id, full_path=False):
    """
    Returns the asset path of the given asset ID.
    
    :param str asset_id: ID of the asset we want to retrieve path of.
    :param bool full_path: whether to return relative asset path or full asset path.
    :return: asset path of the asset with given ID.
    :rtype: str
    """
    mca_asset = assetlist.get_asset_by_id(asset_id)
    if mca_asset:
        if full_path:
            return mca_asset.general_path
        else:
            return path_utils.to_relative_path(mca_asset.general_path)
    return ''


def get_asset_source_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """
    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.source_path


def get_asset_rig_path(asset_id):
    """
    Returns the Project Asset Rig path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """
    
    mca_asset = assetlist.get_asset_by_id(asset_id)
    if mca_asset:
        return mca_asset.rigs_path


def get_asset_name(asset_id):
    """
    Returns the Asset name.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the the Asset name.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    if mca_asset:
        return mca_asset.asset_name
    return ''


def get_face_data_path(asset_id):
    """
    Returns the path to the face data folder.
    
    :return: Returns the path to the face data folder.
    :rtype: str
    """
    
    _path = os.path.join(get_asset_rig_path(asset_id), 'Face_Data')
    return os.path.normpath(_path)


def get_asset_animations_path(asset_id):
    """
    Returns the path to the Animations folder.

    :return: Returns the path to the Animations folder.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.animations_path


def get_asset_maya_rig_file_path(asset_id):
    """
    Returns the project asset rig file path.

    :return: Returns the project asset rig file path.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    rig_list = path_utils.all_file_types_in_directory(mca_asset.rigs_path, '.ma')
    rig_path = lists.get_first_in_list([x for x in rig_list if x.lower().endswith('_rig.ma')])
    return rig_path or ''


def get_asset_skin_data_path(asset_id):
    """
    Returns the Project Asset skinning data path.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Rig path.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.skin_data_path


def get_asset_flags_path(asset_id):
    """
    Returns the Project asset flags directory.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Project asset flags path.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.flags_path


def get_asset_skeletal_mesh_path(asset_id):
    """
    Returns the Project Asset Skeletal Mesh path.  This is the Maya file for the skinned mesh.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Skeletal Mesh path.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.sm_path


def get_meshes_folder(asset_id):
    """
    Returns the Project Asset Skeletal Mesh path.  This is the Maya file for the skinned mesh.

    :param str asset_id: ID of the asset to retrieve path for.
    :return: Returns the Project Asset Skeletal Mesh path.
    :rtype: str
    """

    mca_asset = assetlist.get_asset_by_id(asset_id)
    return mca_asset.meshes_path


def get_commond_sounds():
    """
    Returns the path to the common sounds folder.

    :return: Returns the path to the common sounds folder.
    :rtype: str
    """

    _path = os.path.join(get_common_path(), 'Sounds')
    return os.path.normpath(_path)


def get_common_skeletons():
    """
    Returns the path to the common face folder.

    :return: Returns the path to the common face folder.
    :rtype: str
    """
    _path = os.path.join(get_common_path(), r'Skeletons')
    return os.path.normpath(_path)


def get_common_face_skeletons():
    """
    Returns the path to the common face folder.
    
    :return: Returns the path to the common face folder.
    :rtype: str
    """
    _path = os.path.join(get_common_skeletons(), r'Face')
    return os.path.normpath(_path)


def get_face_blendshape_path(asset_id):
    """
    Returns the path to the face data folder.
    
    :return: Returns the path to the face data folder.
    :rtype: str
    """
    
    _path = os.path.join(get_asset_rig_path(asset_id), r'Blendshapes')
    return os.path.normpath(_path)


# Code helper paths.
def get_resources_path():
    """
    Returns the path to the face data folder.

    :return: Returns the path to the face data folder.
    :rtype: str
    """

    _path = os.path.join(common.TOP_ROOT, 'resources')
    return os.path.normpath(_path)


def get_icons_path():
    """
    Returns the path to the face data folder.

    :return: Returns the path to the face data folder.
    :rtype: str
    """

    _path = os.path.join(get_resources_path(), 'icons')
    return os.path.normpath(_path)


def get_images_path():
    """
    Returns the path to the face data folder.

    :return: Returns the path to the face data folder.
    :rtype: str
    """

    _path = os.path.join(get_resources_path(), 'images')
    return os.path.normpath(_path)


def get_movies_path():
    """
    Returns the path to the movies resource folder.

    :return: Returns the path to the movies resource folder.
    :rtype: str
    """

    _path = os.path.join(get_resources_path(), 'movies')
    return os.path.normpath(_path)

def get_stylesheet_path():
    """
    Returns the path to the face data folder.

    :return: Returns the path to the face data folder.
    :rtype: str
    """

    _path = os.path.join(get_resources_path(), 'styles')
    return os.path.normpath(_path)


def get_unreal_content_path():
    """
    Returns the path to Unreal's content path.

    :return: Returns the path to Unreal's content path.
    :rtype: str
    """

    _path = os.path.join(project_paths.MCA_UNREAL_ROOT, 'unreal', 'Game', 'Content', 'DarkWinter')
    return os.path.normpath(_path)

def get_cine_seq_path():
    """
    Returns the path to cinematic sequences folder.

    :return: Returns the path to cinematic sequences folder.
    :rtype: str
    """
    _path = os.path.join(project_paths.MCA_PROJECT_ROOT, r'Cinematics\Sequences')
    return os.path.normpath(_path)