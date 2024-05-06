# -*- coding: utf-8 -*-

"""
Initialization module for import and creating Textures and Material Instance Constants.
"""

# mca python imports
# PySide2 imports
# from PySide2.QtWidgets import QAbstractItemView
# software specific imports
import unreal
# mca python imports
from mca.ue.paths import ue_path_utils
from mca.ue.utils import u_assets
from mca.ue.assettypes import py_skeletalmesh, py_staticmesh


def get_materials_info():
    level_actors = unreal.EditorActorSubsystem().get_all_level_actors()

    for level_actor in level_actors:
        if level_actor.get_class().get_name() == 'StaticMeshActor':
            static_mesh_component = level_actor.static_mesh_component

            print(level_actor.get_name())
            materials = static_mesh_component.get_materials()

            for material in materials:
                print(material.get_name())


def get_sm_materials():
    pass


def get_material_slot_names(static_mesh):
    """
    Returns the slot names for the materials on a static mesh

    :param unreal.StaticMeshComponent static_mesh: An unreal static mesh
    :return: Returns the slot names for the materials on a static mesh
    :rtype: list(str)
    """

    sm_component = unreal.StaticMeshComponent()
    sm_component.set_static_mesh(static_mesh)
    slot_names =  unreal.StaticMeshComponent.get_material_slot_names(sm_component)
    unreal.log(f'{static_mesh.get_name()}: Slot Names: {slot_names}')
    return slot_names


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

def set_test_sk_materials():
    # SLot names need to match!

    path = ue_path_utils.get_current_content_browser_path()
    sk_list = py_skeletalmesh.get_sks_in_asset_path(path)
    sk = sk_list[0]
    sm_list = py_skeletalmesh.get_sms_in_asset_path(path)
    sm = sm_list[0]

    materials_dict = get_materials_and_slot_names(sm)
    sm_slots = {}
    for slot_name, mat in materials_dict.items():
        sm_slots.update({slot_name: mat['obj']})

    skeletal_mesh_materials = sk.materials

    material_array = unreal.Array(unreal.SkeletalMaterial)

    for material in skeletal_mesh_materials:
        new_sk_material = unreal.SkeletalMaterial()

        slot_name = material.get_editor_property("material_slot_name")
        material_interface = material.get_editor_property("material_interface")

        if sm_slots.get(str(slot_name)):
            material_interface = sm_slots[str(slot_name)]

        new_sk_material.set_editor_property("material_slot_name", slot_name)
        new_sk_material.set_editor_property("material_interface", material_interface)

        material_array.append(new_sk_material)

    sk.set_editor_property("materials", material_array)

    # for sk_mat in sk_asset.materials:
    #     sk_slot_name = sk_mat.get_editor_property('material_slot_name')
    #     for sm_slot_name, sm_material_obj in sm_slots.items():
    #         if sm_slot_name == sk_slot_name:
    #             unreal.SkeletalMaterial
    #             # Set material!
