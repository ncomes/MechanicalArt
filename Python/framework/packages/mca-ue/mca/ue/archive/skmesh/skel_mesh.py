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

SK_FBX_PATH = r'D:\wkspaces\DarkWinterArt\DarkWinter\Characters\Enemies\HornedCharger\Meshes\SK_HornedCharger.fbx'
SK_PATH = r'\Game\DarkWinter\Characters\Enemies\ChaosCaster\Meshes'


def test_import_asset():
    asset_path = r'D:\wkspaces\DarkWinterArt\DarkWinter\Characters\Enemies\HornedCharger\Meshes\SK_HornedCharger.fbx'
    fbx_task = build_import_task(asset_path, r'\Game\DarkWinter\Characters\Enemies\ChaosCaster\Meshes')
    execute_import_tasks([fbx_task])


def import_sk_assets():
    skeletal_mesh_task = build_import_task(SK_FBX_PATH, SK_PATH)
    execute_import_tasks([skeletal_mesh_task])


def build_import_task(file_name, destination_path, options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', False)
    task.set_editor_property('destination_name', 'SK_HornedCharger_TEST')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', file_name)
    task.set_editor_property('replace_existing', False)
    task.set_editor_property('save', False)
    task.set_editor_property('options', options)
    return task


def build_static_mesh_options():
    options = unreal.FbxImportsUI()
    # unreal.FbxImportsUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', False)

    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

    # unreal.FbxStaticMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('combine_meshes', True)
    options.skeletal_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
    options.skeletal_mesh_import_data.set_editor_property('auto_generate_collision', False)


def build_sk_options():
    options = unreal.FbxImportsUI()
    # unreal.FbxImportsUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', True)
    options.set_editor_property('replace_existing', False)
    options.set_editor_property('save', False)

    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    options.skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose ', False)
    return options


# https://docs.unrealengine.com/5.1/en-US/PythonAPI/class/AssetTools.html
def execute_import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            unreal.log(f'imported: {path}')


##################################
# Below Works!
##################################
class ImportTask():
    def __int__(self, replace_existing=False, save=False):
        self.import_task = unreal.AssetImportTask()


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
    options = unreal.FbxImportUI()
    options.import_textures = True
    return options


def import_skeletal_mesh(fbx_path, game_path, asset_name, skeletal_mesh=None, physics_asset=None, replace=False):
    """
    Import a single skeletalMesh into the engine provided an FBX

    :param str fbx_path: path to fbx
    :param str game_path: Game path asset
    :param str asset_name: Name of asset
    :param unreal.SkeletalMesh skeletal_mesh: SkeletalMesh that will be assigned.  If None, it will create one.
    :param unreal.PhysicsAsset physics_asset: PhysicsAsset that will be assigned.  If None, it will create one.
    :param bool replace: Sets whether it is replacing an SK or importing as new.
    :return:
    """

    # Create an import task
    import_task = unreal.AssetImportTask()

    # Set base properties on the import task
    import_task.filename = fbx_path
    import_task.destination_path = game_path
    import_task.destination_name = asset_name
    import_task.automated = True  # Suppress UI
    import_task.set_editor_property('replace_existing', replace)
    import_task.set_editor_property('save', False)

    # Set the skeletal mesh options on the import task
    import_task.options = _get_skeletal_mesh_import_options(skeletal_mesh=skeletal_mesh, physics_asset=physics_asset)

    # Import the skeletalMesh
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(
        [import_task])  # Expects a list for multiple import tasks

    imported_assets = import_task.get_editor_property('imported_object_paths')

    if not imported_assets:
        unreal.log_warning('No assets were imported!')
        return

    # Return the instance of the imported skeletalMesh
    return unreal.load_asset(imported_assets[0])


def _get_skeletal_mesh_import_options(skeletal_mesh=None, physics_asset=None):
    """
    Returns hard coded SkeletalMesh import options

    :param unreal.SkeletalMesh skeletal_mesh: SkeletalMesh that will be assigned.  If None, it will create one.
    :param unreal.PhysicsAsset physics_asset: PhysicsAsset that will be assigned.  If None, it will create one.
    :return: Returns the unreal.FbxImportUI options.  The options for the FBX Import UI
    :rtype: unreal.FbxImportUI
    """

    options = unreal.FbxImportUI()
    options.import_as_skeletal = True
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH

    # Default to compute normals
    import_method = unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS
    options.skeletal_mesh_import_data.normal_import_method = import_method

    # Don't import materials or textures - unreal.FbxImportsUI
    options.import_mesh = True
    options.import_materials = False
    options.import_textures = False
    options.import_as_skeletal = True
    options.lod_number = 4
    options.reset_to_fbx_on_material_conflict = True
    options.import_animations = False
    if skeletal_mesh and isinstance(skeletal_mesh, unreal.Skeleton):
        unreal.log_warning('Setting the Skeleton')
        options.skeleton = skeletal_mesh
    if physics_asset and isinstance(physics_asset, unreal.PhysicsAsset):
        unreal.log_warning('Setting the Physics Asset')
        options.create_physics_asset = False
        options.physics_asset = physics_asset

    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)

    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
    options.skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose', True)
    options.skeletal_mesh_import_data.set_editor_property('convert_scene', True)

    return options


def regenerate_skeletal_mesh_lods(skeletal_mesh, number_of_lods=4):
    """
    Regenerate the LODs to a specific LOD level

    .. Note EditorScriptUtilities plugin needs to be enabled

    :param SkeletalMesh skeletal_mesh: SkeletalMesh Object
    :param int number_of_lods: Number of LODs to generate
    :return:
    """

    did_update_lods = skeletal_mesh.regenerate_lod(number_of_lods)
    if not did_update_lods:
        unreal.log_warning(f'Unable to generate LODs for {skeletal_mesh.get_full_name()}')







