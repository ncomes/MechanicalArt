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


def get_material(material_name):
    """
    Returns a material object by searching for the given material name.

    :param str material_name: The name of the material to search for.
    :return: Returns a material object by searching for the given material name.
    :rtype: unreal.Material
    """

    asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_all_assets()
    master_material = None
    for asset in asset_list:
        asset_name = str(asset.asset_name)
        if asset_name == material_name:
            master_material = asset
            break
    if not master_material:
        logger.warning('Could not find material: {0}'.format(material_name))
        return
    return master_material.get_asset()


def get_master_character_duel_skin():
    """
    Returns the M_CharacterSkinDual_Master material.

    :return: Returns the M_CharacterSkinDual_Master material.
    :rtype: unreal.Material
    """

    return get_material('M_CharacterSkinDual_Master')


def get_character_master():
    """
    Returns the M_CharacterMaster material.

    :return: Returns the M_CharacterMaster material.
    :rtype: unreal.Material
    """

    return get_material('M_CharacterMaster')


def get_character_eyeball_master():
    """
    Returns the M_CharacterEyeBall_Master material.

    :return: Returns the M_CharacterEyeBall_Master material.
    :rtype: unreal.Material
    """

    return get_material('M_CharacterEyeBall_Master')


def get_character_eye_wet_master():
    """
    Returns the M_CharacterEyeWet_Master material.

    :return: Returns the M_CharacterEyeWet_Master material.
    :rtype: unreal.Material
    """

    return get_material('M_CharacterEyeWet_Master')


def get_character_hair_master():
    """
    Returns the M_CharacterHair_Master material.

    :return: Returns the M_CharacterHair_Master material.
    :rtype: unreal.Material
    """

    return get_material('M_CharacterHair_Master')


def get_material_instance_in_path(path):
    """
    Returns the material instances in the given path.

    :param str path: Game path to the folder containing the material instances.
    :return: Returns the material instances in the given path.
    :rtype: list(unreal.MaterialInstanceConstant))
    """

    mi_list = asset_utils.get_assets_in_path(path, 'MaterialInstanceConstant')
    if not mi_list:
        logger.warning(f'No Static Meshes Found at:\n{path}')
        return
    return mi_list


def get_materials_and_slot_names(static_mesh):
    """
    Returns the slot names for the materials on a static mesh

    :param unreal.StaticMeshComponent static_mesh: An unreal static mesh
    :return: Returns the slot names for the materials on a static mesh
    :rtype: list(str)
    """
    materials_dict = {}

    sm_component = unreal.StaticMeshComponent()
    sm_component.set_static_mesh(static_mesh)
    slot_names = unreal.StaticMeshComponent.get_material_slot_names(sm_component)
    if not slot_names:
        return
    for name in slot_names:
        idx = static_mesh.get_material_index(name)
        material_inst = static_mesh.get_material(idx)
        material_name = material_inst.get_name()
        materials_dict[str(name)] = {}
        materials_dict[str(name)].update({'name': material_name})
        materials_dict[str(name)].update({'index': idx})
        materials_dict[str(name)].update({'obj': material_inst})

    return materials_dict


def set_sk_materials(sk_asset, materials_to_change):
    """
    Sets the materials on a skeletal mesh.
    path_to_sk = "/Game/Meshes/Bob"

    :param unreal.SkeletalMesh sk_asset: The unreal skeletal mesh
    :param dict materials_to_change: List of materials - {"mat_head": unreal.load_asset("/Game/Materials/mi_head")}
    """

    # skeletal_mesh = unreal.load_asset(path_to_sk)
    skeletal_mesh = sk_asset
    skeletal_mesh_materials = skeletal_mesh.materials
    
    # material_array = unreal.Array(unreal.SkeletalMaterial)
    material_array = []
    for material in skeletal_mesh_materials:
        new_sk_material = unreal.SkeletalMaterial()
    
        slot_name = material.get_editor_property("material_slot_name")
        material_interface = material.get_editor_property("material_interface")
    
        if materials_to_change.get(str(slot_name)):
            material_interface = materials_to_change[str(slot_name)]
    
        new_sk_material.set_editor_property("material_slot_name", slot_name)
        new_sk_material.set_editor_property("material_interface", material_interface)
    
        material_array.append(new_sk_material)

    skeletal_mesh.set_editor_property("materials", material_array)


def assign_materials_to_sk_from_sm(sk_asset, sm_asset):
    """
    Assigns the materials to a skeletal mesh from a static mesh.

    :param unreal.SkeletalMesh sk_asset: The unreal skeletal mesh
    :param unreal.StaticMesh sm_asset: The unreal static mesh
    """

    materials_dict = get_materials_and_slot_names(sm_asset)
    sm_slots = {}
    for slot_name, mat in materials_dict.items():
        sm_slots.update({slot_name :mat['obj']})

    set_sk_materials(sk_asset, sm_slots)



