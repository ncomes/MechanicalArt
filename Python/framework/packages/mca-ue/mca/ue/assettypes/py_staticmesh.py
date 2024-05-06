# -*- coding: utf-8 -*-

"""
Wrapper for unreal asset StaticMesh.
"""

# mca python imports
import random
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.assettypes import py_base_mesh, py_material_instance
from mca.ue.utils import asset_utils
from mca.ue.startup.configs import ue_consts


logger = log.MCA_LOGGER


class PyStaticMesh(py_base_mesh.PyBaseObjectMesh):
    """
    Class that is base for all MAT Static Meshes.
    """

    def __init__(self, u_asset):
        super().__init__(u_asset)
        if not isinstance(u_asset, unreal.StaticMesh):
            msg = f'{u_asset}: Must be an instance of StaticMesh'
            logger.error(msg)
            raise TypeError(msg)

    @property
    def materials(self):
        """
        Returns the list of materials on the SM.

        :return: Returns the list of materials on the SM.
        :rtype: list(unreal.MaterialInstanceConstant)
        """

        return self._u_asset.static_materials

    @property
    def material_instances(self):
        """
        Returns the list of material instances on the SM.

        :return: Returns the list of material instances on the SM.
        :rtype: list(unreal.MaterialInstanceConstant)
        """

        interfaces = []
        for material in self._u_asset.static_materials:
            interfaces.append(material.get_editor_property("material_interface"))
        return interfaces

    @property
    def slots(self):
        """
        Returns the list of material slot names on the SM.

        :return: Returns the list of material slot names on the SM.
        :rtype: list(str)
        """

        slot_names = []
        for material in self._u_asset.static_materials:
            slot_names.append(material.get_editor_property("material_slot_name"))
        return slot_names

    @slots.setter
    def slots(self, list_of_slots):
        """
        Returns the list of material slot names on the SM.

        :param list(str/unreal.Name()) list_of_slots: List of string names to name the material slots.
        """

        if not isinstance(list_of_slots, (list, tuple)):
            list_of_slots = [list_of_slots]

        material_slots = self.material_instances
        if not len(material_slots) == len(list_of_slots):
            logger.warning(f'Number of slots does not match the number of  materials.  Unable to rename slots.')
            return

        new_material_list = []
        for x, slot in enumerate(list_of_slots):
            sm_material = unreal.StaticMaterial()
            sm_material.set_editor_property("material_slot_name", slot)
            sm_material.set_editor_property("material_interface", material_slots[x])
            new_material_list.append(sm_material)
            logger.info(f'Renaming  Slot_name {slot} and re-adding material{material_slots[x].get_name()}')

        self.u_asset.set_editor_property("static_materials", new_material_list)

    def get_slot_index(self, slot_name):
        """
        Returns the index of the given material slot name on the SM.

        :param str slot_name: Name of a slot on the SM
        :return: Returns the index of the given material slot name on the SM.
        :rtype: int
        """

        return self.u_asset.get_material_index(slot_name)

    def replace_slot_name(self, slot_name, new_slot_name):
        slots = self.slots
        if slot_name not in slots:
            logger.warning(f'Slot name {slot_name} does not exist.  Unable to replace slot name.')
            return

        for x, slot in enumerate(slots):
            if str(slot) == str(slot_name):
                slots[x] = unreal.Name(new_slot_name)
                break

        self.slots = slots

    def create_material_interface_dict(self):
        """
        Returns a dictionary of the material instances and slot names indexed.
        Ex: {0:{slot_name: material_instance}}

        :return: Returns a dictionary of the material instances and slot names indexed.
        :rtype: dict
        """

        slot_names = self.slots
        materials_folder = self.materials_path
        mi_list = asset_utils.get_assets_in_path(materials_folder, 'MaterialInstanceConstant')
        if not mi_list:
            logger.warning(f'No materials found for the {self.name}')
            return
        pymi_list = []
        for mi in mi_list:
            result = py_material_instance.ParentMaterialMapping.attr(mi)
            if result != mi:
                pymi_list.append(result(mi))

        material_dict = {}
        for mi in pymi_list:
            slot_name, mi = py_base_mesh.pair_material_instance_and_slot_name(mi, slot_names)
            if not mi:
                return
            idx = self.get_slot_index(slot_name)
            material_dict.update({idx: {}})
            material_dict[idx].update({slot_name: mi})
        return material_dict

    def set_materials(self, material_list=None, set_default_materials=True):
        """
        Sets materials on the SM.  This looks at the materials folder to set.
        It will match the material names to the slot names.

        :param list(unreal.MaterialInterface) material_list: List of Material Interfaces.
        :param bool set_default_materials: If True, default materials will be set on empty slots.
        """

        if not material_list:
            material_dict = self.create_material_interface_dict()

            if not material_dict:
                logger.warning('No materials were found.  Please check the material and slot names '
                               'follow the naming conventions.')
                return
            for idx, slot_dict in material_dict.items():
                material_instance = list(slot_dict.values())[0]
                self.u_asset.set_material(idx, material_instance.u_asset)
        else:
            if not isinstance(material_list, list):
                material_list = [material_list]
            for idx, material_instance in enumerate(material_list):
                self.u_asset.set_material(idx, material_instance)

        if set_default_materials:
            self._set_default_materials()

    def _set_default_materials(self):
        """
        Sets default materials on the SM.
        """

        default_materials_class = py_material_instance.PlainMaterialInstances()
        default_materials = default_materials_class.default_materials
        print(default_materials)
        random.shuffle(default_materials)
        len_materials = len(default_materials)
        x = 0
        for idx, material in enumerate(self.materials):
            material_interface = material.get_editor_property('material_interface')
            material_name = ''
            if material_interface:
                material_name = material_interface.get_name()
            if not material_interface or material_name == ue_consts.DEFAULT_MATERIAL:
                if x > len_materials-1:
                    x = 0
                self.u_asset.set_material(idx, default_materials[x])
                x += 1

    @property
    def static_class(self):
        return self.u_asset.static_class()


def get_static_mesh_in_path(path):
    """
    Returns static meshes in the given path.

    :param str path: Game path to the folder containing the static meshes.
    :return: Returns static meshes in the given path.
    :rtype: list(unreal.StaticMesh)
    """

    sm_list = asset_utils.get_assets_in_path(path, 'StaticMesh')
    if not sm_list:
        logger.warning(f'No Static Meshes Found at:\n{path}')
        return
    return sm_list


def static_mesh_import_options(import_textures=False,
                                import_materials=False,
                                import_animations=False,
                                override_full_name=True,
                                reset_to_fbx_on_material_conflict=True,
                                auto_generate_collision=True,
                                build_reversed_index_buffer=True,
                                translation=unreal.Vector(0.0, 0.0, 0.0),
                                rotation=unreal.Vector(0.0, 0.0, 0.0),
                                uniform_scale=1.0,
                                generate_lightmap_u_vs=True,
                                remove_degenerates=True,
                                one_convex_hull_per_ucx=True,
                                transform_vertex_to_absolute=True,
                                convert_scene=True,
                                reorder_material_to_fbx_order=True,
                                combine_meshes=True,
                                normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS,
                                normal_generation_method=unreal.FBXNormalGenerationMethod.MIKK_T_SPACE,
                                compute_weighted_normals=True,
                               ):
    """
    Returns StaticMesh import options

    :param bool import_textures: If True, Textures will be imported with the Static Mesh from the FBX.
    :param bool import_materials: If True, Materials will be created with the Static Mesh.
    :param bool import_animations: If True, animations will be imported from the FBX
    :param bool override_full_name: If True, the static mesh name will be overridden with the FBX name.
    :param bool reset_to_fbx_on_material_conflict: If True, The material slots will match the FBX material names.
    :param bool auto_generate_collision: If True, collision will be generated automatically.
    :param bool build_reversed_index_buffer:  If True,
    :param unreal.Vector translation: starting position of the StaticMesh.
    :param unreal.Vector rotation: starting rotation of the StaticMesh.
    :param float uniform_scale: starting uniform scale of the StaticMesh.
    :param bool generate_lightmap_u_vs:
    :param bool remove_degenerates:
    :param bool one_convex_hull_per_ucx:
    :param bool transform_vertex_to_absolute:
    :param bool convert_scene: If True, will convert the axis of to match Unreals default.  (Y-up to Z-up)
    :param bool reorder_material_to_fbx_order:
    :param bool combine_meshes:
    :param unreal.FBXNormalImportMethod normal_import_method:
    :param unreal.FBXNormalGenerationMethod normal_generation_method:
    :param bool compute_weighted_normals:
    :return: Returns the unreal.FbxImportUI options.  The options for the FBX Import UI
    :rtype: unreal.FbxImportUI
    """

    options = unreal.FbxImportUI()
    options.import_as_skeletal = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH

    # Don't import materials or textures - unreal.FbxImportsUI
    options.import_mesh = True
    options.import_materials = import_materials
    options.import_textures = import_textures
    options.reset_to_fbx_on_material_conflict = reset_to_fbx_on_material_conflict
    options.import_animations = import_animations
    options.override_full_name = override_full_name

    # unreal.FbxMeshImportData
    options.static_mesh_import_data .set_editor_property('import_translation', translation)
    options.static_mesh_import_data .set_editor_property('import_rotation', rotation)
    options.static_mesh_import_data .set_editor_property('import_uniform_scale', uniform_scale)

    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data .set_editor_property('auto_generate_collision', auto_generate_collision)
    options.static_mesh_import_data .set_editor_property('build_reversed_index_buffer', build_reversed_index_buffer)
    options.static_mesh_import_data .set_editor_property('generate_lightmap_u_vs', generate_lightmap_u_vs)
    options.static_mesh_import_data .set_editor_property('remove_degenerates', remove_degenerates)
    options.static_mesh_import_data .set_editor_property('one_convex_hull_per_ucx', one_convex_hull_per_ucx)
    options.static_mesh_import_data .set_editor_property('transform_vertex_to_absolute', transform_vertex_to_absolute)
    options.static_mesh_import_data .set_editor_property('convert_scene', convert_scene)
    options.static_mesh_import_data .set_editor_property('reorder_material_to_fbx_order', reorder_material_to_fbx_order)
    options.static_mesh_import_data .set_editor_property('combine_meshes', combine_meshes)
    options.static_mesh_import_data .set_editor_property('normal_import_method', normal_import_method)
    options.static_mesh_import_data .set_editor_property('normal_generation_method', normal_generation_method)
    options.static_mesh_import_data .set_editor_property('compute_weighted_normals', compute_weighted_normals)

    return options
