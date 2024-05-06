# -*- coding: utf-8 -*-

"""
Wrapper for unreal asset SkeletalMesh.
"""

# mca python imports
import random
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.assettypes import py_base_mesh, py_material_instance
from mca.ue.utils import asset_utils, asset_import


logger = log.MCA_LOGGER


class PySkelMesh(py_base_mesh.PyBaseObjectMesh):
    """
    Abstract class that is base for all pymel nodes classes.

    The names of nodes and attributes can be passed to this class, and the appropriate subclass will be determined.
    If the passed node or attribute does not exist an error will be raised.
    """

    def __init__(self, u_asset):
        """

        :param unreal.SkeletalMesh u_asset:
        """
        super().__init__(u_asset)
        if not isinstance(u_asset, unreal.SkeletalMesh):
            msg = f'{u_asset}: Must be an instance of SkeletalMesh'
            logger.error(msg)
            raise TypeError(msg)

    @property
    def materials(self):
        return self._u_asset.materials

    @property
    def material_instances(self):
        interfaces = []
        for material in self._u_asset.materials:
            interfaces.append(material.get_editor_property("material_interface"))
        return interfaces

    @property
    def skeleton(self):
        return self.u_asset.skeleton

    @property
    def physics_asset(self):
        return self.u_asset.physics_asset

    @physics_asset.setter
    def physics_asset(self, physics_asset):
        self.u_asset.set_editor_property('physics_asset', physics_asset)

    @property
    def lod_settings(self):
        return self.u_asset.lod_settings

    @lod_settings.setter
    def lod_settings(self, lod_settings):
        self.u_asset.set_editor_property('lod_settings', lod_settings)

    @property
    def slots(self):
        """
        Returns the list of material slot names on the Skeletal Mesh.

        :return: Returns the list of material slot names on the Skeletal Mesh.
        :rtype: list(str)
        """

        return [x.get_editor_property('material_slot_name') for x in self.materials]

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
            new_sk_material = unreal.SkeletalMaterial()
            new_sk_material.set_editor_property("material_slot_name", slot)
            new_sk_material.set_editor_property("material_interface", material_slots[x])
            new_material_list.append(new_sk_material)
            logger.info(f'Renaming  Slot_name {slot} and re-adding material{material_slots[x].get_name()}')

        self.u_asset.set_editor_property("materials", new_material_list)
        # self.save()

    def get_slot_index(self, slot_name):
        slots = self.slots
        for x, slot in enumerate(slots):
            if slot == slot_name:
                return x
        return

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

    def set_materials(self):
        """
        Sets materials on the SM.  This looks at the materials folder to set.
        It will match the material names to the slot names.
        """

        # Checks the materials folder to see if there are materials that match the slot names.
        material_dict = self.create_material_interface_dict()

        if not material_dict:
            logger.warning('No materials were found.  Please check the material and slot names '
                           'follow the naming conventions.')
            return

        # Gets the default materials.  These are the MI_PlainColor materials
        default_materials_class = py_material_instance.PlainMaterialInstances()
        default_materials = default_materials_class.default_materials

        new_material_list = []
        for x, slot_name in enumerate(self.slots):
            found_material = False
            # randomly shuffle the list, so we can grab a random material each time
            random.shuffle(default_materials)
            for idx, slot_dict in material_dict.items():
                material_slot = list(slot_dict.keys())[0]
                # if our material name matches the slot name convention, set the material.
                if str(material_slot) == str(slot_name):
                    new_sk_material = unreal.SkeletalMaterial()
                    new_sk_material.set_editor_property("material_slot_name", slot_name)
                    material_instance = list(slot_dict.values())[0]
                    new_sk_material.set_editor_property("material_interface", material_instance.u_asset)
                    new_material_list.append(new_sk_material)
                    logger.info(f'Found a matching material.  '
                                f'Setting Material! {material_slot} : {material_instance.get_name()}')
                    found_material = True
            # If not material is found, then set a default material.
            if not found_material:
                new_sk_material = unreal.SkeletalMaterial()
                new_sk_material.set_editor_property("material_slot_name", slot_name)
                new_sk_material.set_editor_property("material_interface", default_materials[0])
                new_material_list.append(new_sk_material)
                logger.info(f'No matching material.  '
                            f'Setting a Default Material! {slot_name} : {default_materials.get_name()}')

        self.u_asset.set_editor_property("materials", new_material_list)
        self.save()

    def set_physics_asset(self, physics_asset=None):
        """
        Sets the physics asset on the Skeletal Mesh.
        If a physics asset is not specified, the physics asset in the Meshes folder will be used.

        :param unreal.PhysicsAsset physics_asset:
        """

        if not physics_asset:
            physics_asset = self.get_physics_asset_in_path()
        if not physics_asset:
            return
        self.u_asset.set_editor_property('physics_asset', physics_asset)

    def get_physics_asset_in_path(self):
        """
        Returns the physics asset in the Meshes folder.

        :return: Returns the physics asset in the Meshes folder.
        :rtype: unreal.PhysicsAsset
        """

        path = self.meshes_path
        physics_assets = asset_utils.get_assets_in_path(path, 'PhysicsAsset')
        if not physics_assets:
            logger.warning(f'No Physics Assets Found at:\n{path}')
            return
        return physics_assets[0]


def get_skeletal_meshes_in_path(path):
    """
    Returns skeletal meshes in the given path.

    :param str path: Game path to the folder containing the skeletal meshes.
    :return: Returns skeletal meshes in the given path.
    :rtype: list(unreal.SkeletalMesh)
    """

    sk_list = asset_utils.get_assets_in_path(path, 'SkeletalMesh')
    if not sk_list:
        logger.warning(f'No Skeletal Meshes Found at:\n{path}')
        return
    return sk_list


def skeletal_mesh_import_options(skeleton=None,
                                 physics_asset=None,
                                 translation=unreal.Vector(0.0, 0.0, 0.0),
                                 rotation=unreal.Vector(0.0, 0.0, 0.0),
                                 uniform_scale=1.0,
                                 import_morph_targets=True,
                                 update_skeleton_reference_pose=False,
                                 use_t0_as_ref_pose=True,
                                 convert_scene=True,
                                 lod_number=5,
                                 import_materials=False,
                                 import_textures=False
                                 ):

    """
    Returns hard coded SkeletalMesh import options
    
    :param unreal.SkeletalMesh skeleton: SkeletalMesh that will be assigned.  If None, it will create one.
    :param unreal.PhysicsAsset physics_asset: PhysicsAsset that will be assigned.  If None, it will create one.
    :param unreal.Vector translation: starting position of the SkeletalMesh.
    :param unreal.Vector rotation: starting rotation of the SkeletalMesh.
    :param float uniform_scale: starting uniform scale of the SkeletalMesh.
    :param bool import_morph_targets: If True, will import blend shapes targets.
    :param bool update_skeleton_reference_pose: If True, will update the Skeleton's reference pose
    :param bool use_t0_as_ref_pose: If True, will use the Skeleton's Timeline 0 frame as the reference pose.
    :param bool convert_scene: If True, will convert the axis of to match Unreals default.  (Y-up to Z-up)
    :param int lod_number: Number of LODs.
    :param bool import_materials: If True, will create materials from the FBX file.
    :param bool import_textures: If True, will create textures from the FBX file.
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
    options.import_materials = import_materials
    options.import_textures = import_textures
    options.import_as_skeletal = True
    options.lod_number = lod_number
    options.reset_to_fbx_on_material_conflict = True
    options.import_animations = False
    if skeleton and isinstance(skeleton, unreal.Skeleton):
        unreal.log_warning('Setting the Skeleton')
        options.skeleton = skeleton
    if physics_asset and isinstance(physics_asset, unreal.PhysicsAsset):
        unreal.log_warning('Setting the Physics Asset')
        options.create_physics_asset = False
        options.physics_asset = physics_asset

    # unreal.FbxMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_translation', translation)
    options.skeletal_mesh_import_data.set_editor_property('import_rotation', rotation)
    options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', uniform_scale)

    # unreal.FbxSkeletalMeshImportData
    options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', import_morph_targets)
    options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose',
                                                            update_skeleton_reference_pose)
    options.skeletal_mesh_import_data.set_editor_property('use_t0_as_ref_pose', use_t0_as_ref_pose)
    options.skeletal_mesh_import_data.set_editor_property('convert_scene', convert_scene)

    return options


def import_skeletal_mesh(fbx_path, game_path, asset_name, skeleton=None, physics_asset=None, replace=False):
    """
    Import a single skeletalMesh into the engine provided an FBX

    :param str fbx_path: path to fbx
    :param str game_path: Game path asset
    :param str asset_name: Name of asset
    :param unreal.SkeletalMesh skeleton: SkeletalMesh that will be assigned.  If None, it will create one.
    :param unreal.PhysicsAsset physics_asset: PhysicsAsset that will be assigned.  If None, it will create one.
    :param bool replace: Sets whether it is replacing an SK or importing as new.
    :return:
    """

    # import the textures
    options = skeletal_mesh_import_options(skeleton=skeleton, physics_asset=physics_asset)

    uasset = asset_import.import_asset(filename=fbx_path,
                                       game_path=game_path,
                                       asset_name=asset_name,
                                       import_options=options,
                                       replace_existing=replace,
                                       save=True)
    uasset = asset_utils.PyNode(uasset)
    # Only set the properties and save if the asset is valid.
    if isinstance(uasset, PySkelMesh):
        uasset.set_materials()
        uasset.save()
    return uasset

