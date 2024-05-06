# -*- coding: utf-8 -*-

"""
Wrapper for unreal asset SkeletalMesh.
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.assettypes import py_base, py_material_instance
from mca.ue.startup.configs import ue_consts
from mca.ue.utils import asset_utils

logger = log.MCA_LOGGER


class PyBaseObjectMesh(py_base.PyUnrealBaseAssetObject):
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

    @property
    def slots(self):
        """
        Returns the list of material slot names on the SM.

        :return: Returns the list of material slot names on the SM.
        :rtype: list(str)
        """

        return None

    @slots.setter
    def slots(self, list_of_slots):
        """
        Returns the list of material slot names on the SM.

        :param list(str/unreal.Name()) list_of_slots: List of string names to name the material slots.
        """

        pass

    def get_slot_index(self, slot_name):
        """
        Returns the index of the given material slot name on the SM.

        :param str slot_name: Name of a slot on the SM
        :return: Returns the index of the given material slot name on the SM.
        :rtype: int
        """

        pass

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
            slot_name, mi = pair_material_instance_and_slot_name(mi, slot_names)
            if not mi:
                return
            idx = self.get_slot_index(slot_name)
            material_dict.update({idx: {}})
            material_dict[idx].update({slot_name: mi})
        return material_dict


def pair_material_instance_and_slot_name(material_instance, slot_names):
    """
    Returns a dictionary of the slot name and the corresponding material instance.

    :param list(py_material_instance.PyMaterialInstanceConstant) material_instance: List of material instances.
    :param list(str) slot_names: List of material slot names.
    :return: Returns a dictionary of the slot name and the corresponding material instance.
    :rtype: dict
    """
    if not isinstance(material_instance, unreal.MaterialInstanceConstant) and\
            not isinstance(material_instance ,py_material_instance.PyMaterialInstanceConstant):
        return [None, None]
    mi_name = str(material_instance.get_name())
    if mi_name.startswith(ue_consts.MCA_INST_PREFIX):
        mi_name = mi_name.replace(ue_consts.# mca python importsINST_PREFIX, '')
    for slot_name in slot_names:
        if str(slot_name) == mi_name:
            return [slot_name, material_instance]
    return [None, None]
