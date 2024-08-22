"""
Module that contains fncs for dealing with mca's asset list.
"""

# System global imports
import copy
import os
import time
import inspect
# software specific imports
# mca python imports
from mca.common.modifiers import singleton
from mca.common.textio import yamlio
from mca.common.utils import fileio, path_utils

from mca.common import log
logger = log.MCA_LOGGER

NON_RIG_ASSETS = ['apparel', 'reference']

local_file_path = inspect.getabsfile(inspect.currentframe())
# Little bit hacky, but we're going to reconstruct the data path from this module's location.
REGISTRY_FILE_PATH = os.path.join(local_file_path.lower().split('python')[0], r'Common\Tools\Assetlist\asset_registry.yaml')


class AssetListRegistry(singleton.SimpleSingleton):
    REGISTRY_DICT = {}
    ASSET_ID_DICT = {}
    CATEGORY_DICT = {}
    CATEGORY_NAME_DICT = {}
    MESH_PATH_DICT = {}
    DIRTY = False

    LAST_EDIT = None

    def __init__(self, force=False):
        self.reload(force=force)

    def reload(self, force=False):
        """
        Regenerate the registry's lookups.

        :param bool force: If the lookups should be regenerated. Normally once this is initialized they are not reloaded unless requested.
        """
        self.REGISTRY_DICT = {}
        self.ASSET_ID_DICT = {}
        self.CATEGORY_DICT = {}
        self.CATEGORY_NAME_DICT = {}
        self.MESH_PATH_DICT = {}

        # Always sync before we load the registry, but do not force it in case there are local changes.
        #sourcecontrol.p4_sync(REGISTRY_FILE_PATH)
        if os.path.exists(REGISTRY_FILE_PATH):
            # Read the file or if the file is empty yield an empty dict.
            self.REGISTRY_DICT = yamlio.read_yaml(REGISTRY_FILE_PATH) or {}
        else:
            # could not find the registry file.
            if not force:
                raise IOError(f'{REGISTRY_FILE_PATH} The registry file was not found on disk, please verify you have latest.')
            self.REGISTRY_DICT = {}

        if os.path.exists(REGISTRY_FILE_PATH):
            self.LAST_EDIT = time.ctime(os.path.getmtime(REGISTRY_FILE_PATH))
        for asset_id, data_dict in self.REGISTRY_DICT.items():
            # Build our cached lookups.
            # The name registry is the asset_name to asset_entry
            # The asset_id_dict is unique identifier to asset_entry
            # the category_dict is the organization of type and subtype to asset_entry
            # the mesh_path_dict is the asset's full mesh_path to asset_entry
            asset_entry = Asset(asset_id, data_dict)
            self.ASSET_ID_DICT[asset_id] = asset_entry
            if asset_entry.asset_type not in self.CATEGORY_DICT:
                self.CATEGORY_DICT[asset_entry.asset_type] = {}
                self.CATEGORY_NAME_DICT[asset_entry.asset_type] = {}
            for subtype in asset_entry.asset_subtype:
                if subtype not in self.CATEGORY_DICT[asset_entry.asset_type]:
                    self.CATEGORY_DICT[asset_entry.asset_type][subtype] = {}
                    self.CATEGORY_NAME_DICT[asset_entry.asset_type][subtype] = {}
                self.CATEGORY_DICT[asset_entry.asset_type][subtype][asset_id] = asset_entry
                self.CATEGORY_NAME_DICT[asset_entry.asset_type][subtype][asset_entry.asset_name] = asset_entry
            self.MESH_PATH_DICT[asset_entry.mesh_path] = asset_entry

    def commit(self):
        """
        Save changes to the registry if there was a change made.

        """
        if self.DIRTY:
            fileio.touch_path(REGISTRY_FILE_PATH)
            yamlio.write_yaml(REGISTRY_FILE_PATH, self.REGISTRY_DICT)
            self.DIRTY = False

    def register_asset(self, asset_entry, commit=False):
        """
        This will serialize one of our data classes to the main register.

        :param Asset asset_entry: The asset to be registered.
        :param bool commit: If the registry should be saved after the addition. For perf reasons this can be held until
            multiple registers are completed.
        """

        existing_entry = self.ASSET_ID_DICT.get(asset_entry.asset_id)

        if not asset_entry.DIRTY:
            # If nothing has been changed.
            return

        if existing_entry and existing_entry is not asset_entry:
            if existing_entry.get_data_dict() == asset_entry.get_data_dict():
                # We're using a replica of the entry and nothing has been changed.
                return

        asset_entry.DIRTY = False
        registry_asset = copy.deepcopy(asset_entry)

        self.REGISTRY_DICT[registry_asset.asset_id] = registry_asset.get_data_dict()
        self.ASSET_ID_DICT[registry_asset.asset_id] = registry_asset
        if registry_asset.asset_type not in self.CATEGORY_DICT:
            self.CATEGORY_DICT[registry_asset.asset_type] = {}
        for subtype in registry_asset.asset_subtype:
            if subtype not in self.CATEGORY_DICT[registry_asset.asset_type]:
                self.CATEGORY_DICT[registry_asset.asset_type][subtype] = {}
            self.CATEGORY_DICT[registry_asset.asset_type][subtype][registry_asset.asset_id] = registry_asset
        if registry_asset.mesh_path:
            self.MESH_PATH_DICT[registry_asset.mesh_path] = registry_asset

        if commit:
            self.commit()

    def remove_entry(self, asset_id, commit=False):
        """
        Remove an asset entry by asset_id.

        :param str asset_id: The asset id associated with this Asset.
        :param bool commit: If the changes should be committed to the registry as part of the remove.
        """
        if asset_id in self.ASSET_ID_DICT:
            asset_entry = self.ASSET_ID_DICT[asset_id]
            del self.ASSET_ID_DICT[asset_id]
            del self.REGISTRY_DICT[asset_entry.asset_id]
            for asset_subtype in asset_entry.asset_subtype:
                del self.CATEGORY_DICT[asset_entry.asset_type][asset_subtype][asset_entry.asset_id]
            if asset_entry.mesh_path:
                del self.MESH_PATH_DICT[asset_entry.mesh_path]
            self.DIRTY = True

            if commit:
                self.commit()

    def get_entry(self, asset_id):
        """
        Return an Asset by asset_id.

        :param str asset_id: The asset_id to look up an entry by.
        :return: The found Asset or None
        :rtype: Asset
        """
        return self.ASSET_ID_DICT.get(asset_id)

    def get_entry_by_name(self, asset_name):
        """
        Return an Asset by asset_name.

        NOTE: This is generally not a safe way to look up an asset.

        :param str asset_name: The name of an asset to lookup.
        :return: The found Asset or None
        :rtype: Asset
        """
        return self.NAME_REGISTRY.get(asset_name)

    def get_entry_by_path(self, mesh_path):
        """
        Return an Asset by asset_path.

        :param str mesh_path: The path to an entry's SM file.
        :return: The found Asset or None
        :rtype: Asset
        """
        mesh_path = path_utils.to_full_path(mesh_path)
        return self.PATH_DICT.get(mesh_path)

class Asset(object):
    _asset_name = ''
    _asset_namespace = ''
    _mesh_path = '' # This will always be to the skeletal mesh
    _rig_path = ''
    _skeleton_path = ''
    _asset_type = '' # Primary organization method. "Model" will always have a mesh path.
    _asset_subtype = [] # We'll overload the subtype with keywords.
    _asset_parent = '' # This is the inheritance path.
    _local_asset_list = [] # If there are any assets that should be subloaded.

    DIRTY = False

    def __init__(self, asset_id, data_dict):
        """
        This represents a single asset, and includes data about where it lives.

        :param asset_id:
        :param data_dict:
        """
        self._asset_id = asset_id
        self._set_data(data_dict)

    def _set_data(self, data_dict):
        self._asset_name = data_dict.get('name', '')
        self._asset_namespace = data_dict.get('namespace', '')
        self._mesh_path = data_dict.get('mesh_path', '')
        self._rig_path = data_dict.get('rig_path', '')
        self._skeleton_path = data_dict.get('skeleton_path', '')
        self._asset_type = data_dict.get('type', '')
        self._asset_subtype = data_dict.get('subtype', [])
        self._asset_parent = data_dict.get('parent', '')
        self._local_asset_list = data_dict.get('local_asset_list', [])
        # We don't want to dirty the class here because this is used to initialize it.
        # If it's a new asset the registry will add it because the asset id is unique.
        # Or if it's a replica of an entry with different data that will trigger the registry to save it as well.

    @property
    def asset_id(self):
        return self._asset_id

    @asset_id.setter
    def asset_id(self, val):
        if val != self._asset_id:
            self.DIRTY = True
        self._asset_id = str(val)

    @property
    def asset_name(self):
        return self._asset_name

    @asset_name.setter
    def asset_name(self, val):
        if val != self._asset_name:
            self.DIRTY = True
        self._asset_name = str(val)

    @property
    def asset_namespace(self):
        return self._asset_namespace

    @asset_namespace.setter
    def asset_namespace(self, val):
        if val != self._asset_namespace:
            self.DIRTY = True
        self._asset_namespace = str(val)
    
    # Note not all Assets will have a mesh path. Nor should we check for inheritance.
    @property
    def mesh_path(self):
        return path_utils.to_full_path(self._mesh_path)

    @mesh_path.setter
    def mesh_path(self, val):
        if val != self._mesh_path:
            self.DIRTY = True
        self._mesh_path = path_utils.to_relative_path(str(val))

    @property
    def asset_type(self):
        # This is the major category: model, collection
        # This should be used or organize the list by how the entry is to be used.
        return self._asset_type

    @asset_type.setter
    def asset_type(self, val):
        if val != self._asset_type:
            self.DIRTY = True
        self._asset_type = str(val)

    @property
    def asset_subtype(self):
        # This is a relative category which refines how the asset can be organized: apparel, npc, combatant, player, prop
        # This is used to organize the entry within user facing lists.
        return self._asset_subtype

    @asset_subtype.setter
    def asset_subtype(self, val):
        if val != self._asset_subtype:
            self.DIRTY = True
        self._asset_subtype = val

    @property
    def asset_parent(self):
        # This lets us know if the asset is a derivative of another. This is useful for loading rigs from a similar skel type.
        return self._asset_parent

    @asset_parent.setter
    def asset_parent(self, val):
        if val != self._asset_parent:
            self.DIRTY = True
        self._asset_parent = str(val)

    @property
    def local_asset_list(self):
        return_list = []
        for entry in self._local_asset_list:
            if isinstance(entry, Asset):
                return_list.append(entry)
            else:
                found_entry = get_asset_by_id(entry)
                if found_entry:
                    return_list.append(found_entry)
                else:
                    return_list.append(entry)
        return return_list

    @local_asset_list.setter
    def local_asset_list(self, val_list):
        self.DIRTY = True
        self._local_asset_list = val_list


    # Path Helpers
    # Model paths
    @property
    def model_path(self):
        # Returns the dir one above the mesh's local dir.
        mesh_path = self._mesh_path
        if mesh_path:
            return os.path.split(os.path.dirname(path_utils.to_full_path(mesh_path)))[0]

    @property
    def skin_path(self):
        mesh_path = self._mesh_path
        if mesh_path:
            skin_path = os.path.join(self.source_path, f'{self.asset_name}_skinning.fbx')
            return skin_path

    def parent_skins(self):
        skin_path = self.skin_path
        if not skin_path or not os.path.exists(skin_path):
            # Try snagging a local skeleton_path
            skeleton_path = path_utils.to_full_path(self._skeleton_path)
            if skeleton_path.lower().endswith('.fbx') or skeleton_path.lower().endswith('.ma'):
                # If the skel is a fbx or ma it might have geo.
                skin_path = skeleton_path
            if self.asset_parent:
                asset_entry = get_asset_by_id(self.asset_parent)
                if asset_entry:
                    skin_path = asset_entry.parent_skins()
        return skin_path

    @property
    def texture_path(self):
        return os.path.join(self.model_path, 'textures')

    @property
    def source_path(self):
        return os.path.join(self.model_path, '_source')

    # Animation Paths
    @property
    def skeleton_path(self):
        skel_path = path_utils.to_full_path(self._skeleton_path)
        if not os.path.exists(skel_path) and self.asset_parent:
            asset_entry = get_asset_by_id(self.asset_parent)
            if asset_entry:
                skel_path = asset_entry.skeleton_path

        return skel_path

    @skeleton_path.setter
    def skeleton_path(self, val):
        self._skeleton_path = path_utils.to_relative_path(val)

    def parent_skeletons(self):
        parent_skeleton_list = []
        if self.asset_parent:
            asset_entry = get_asset_by_id(self.asset_parent)
            if asset_entry:
                local_skel_path = asset_entry.skeleton_path
                if local_skel_path:
                    parent_skeleton_list.extend(local_skel_path)
                parent_skeleton_list += asset_entry.parent_skeletons()
        return parent_skeleton_list

    @property
    def rig_path(self):
        rig_path = path_utils.to_full_path(self._rig_path)
        if not os.path.exists(rig_path) and self.asset_parent:
            asset_entry = get_asset_by_id(self.asset_parent)
            if asset_entry:
                rig_path = asset_entry.rig_path

        return rig_path
    
    @rig_path.setter
    def rig_path(self, val):
        self._rig_path = path_utils.to_relative_path(val)

    @property
    def flags_path(self):
        if self.rig_path:
            return path_utils.to_full_path(os.path.join(os.path.dirname(self.rig_path), 'flags'))

    @property
    def animation_path(self):
        # Return the path one above the rig path.
        rig_path = self._rig_path
        if rig_path:
            return os.sep.join(rig_path.split(os.sep)[:-2])

    # Registry functions
    def get_data_dict(self):
        return_dict = {}
        return_dict['name'] = self.asset_name
        return_dict['namespace'] = self.asset_namespace
        return_dict['mesh_path'] = path_utils.to_relative_path(self.mesh_path)
        # Do NOT grab inheritance when saving.
        # Grabbing inheritance and saving it will defeat the purpose.
        return_dict['rig_path'] = path_utils.to_relative_path(self._rig_path)
        return_dict['skeleton_path'] = path_utils.to_relative_path(self._skeleton_path)
        return_dict['type'] = self.asset_type
        return_dict['subtype'] = self.asset_subtype
        return_dict['parent'] = self.asset_parent
        return_dict['local_asset_list'] = [entry.asset_id if isinstance(entry, Asset) else entry for entry in self.local_asset_list]
        return return_dict

    def register(self, commit=True):
        registry = AssetListRegistry()
        if self.asset_id not in registry.ASSET_ID_DICT:
            self.DIRTY = True

        if self.DIRTY:
            registry.DIRTY = True
            registry.register_asset(self, commit=commit)

def get_registry():
    """
    Validate the asset list registry, reload it if it's out of date, before returning it.
    
    """

    registry = AssetListRegistry()
    if  os.path.exists(REGISTRY_FILE_PATH) and time.ctime(os.path.getmtime(REGISTRY_FILE_PATH)) != registry.LAST_EDIT:
        registry.reload(True)
    return registry


def get_asset_by_id(asset_id):
    """
    Return an Asset by asset_id

    :param str asset_id: The asset_id to look up by.
    :return: The Asset that matches the asset_id or None
    :rtype: Asset
    """

    if not asset_id:
        return

    registry = get_registry()
    return registry.get_entry(asset_id)


def get_asset_by_path(mesh_path):
    """
    Return an Asset by asset_path

    :param str mesh_path: The asset_path to look up by.
    :return: The Asset that matches the asset_path or None
    :rtype: Asset
    """

    if not mesh_path:
        return

    registry = get_registry()
    return registry.get_entry_by_path(mesh_path)

def get_asset_skeleton(asset_id, local=False):
    """
    Return the skeleton path of a given asset by asset id.

    :param str asset_id: The asset_id to look up by.
    :param bool local: If the asset's local path should be forced.
    :return: The path to this asset's skeleton, or the inherited skeleton path.
    :rtype: str
    """

    registry = get_registry()
    asset_entry = registry.get_entry(asset_id)
    if asset_entry:
        if local:
            return asset_entry._skeleton_path
        else:
            return asset_entry.skeleton_path
            

def get_asset_category_dict(asset_subtype=None, asset_type='model', by_name=True):
    """
    Return the entry dictionary of the given category lookups.

    :param str, list asset_subtype: The subtype that should be gotten.
    :param str asset_type: The type that should be gotten.
    :param bool by_name: If a name to asset entry should be returned.
    :return: A dictionary of all entries that match the lookup criteria
    :rtype: dict
    """

    cpg_asset_list = AssetListRegistry()
    asset_type = asset_type or 'model'

    if asset_subtype and not isinstance(asset_subtype, list):
        asset_subtype = [asset_subtype]

    return_dict = {}
    if by_name:
        lookup_dict = cpg_asset_list.CATEGORY_NAME_DICT
    else:
        lookup_dict = cpg_asset_list.CATEGORY_DICT
    for subtype, entry_dict in lookup_dict.get(asset_type, {}).items():
        if asset_subtype and subtype not in asset_subtype:
            continue
        for lookup_identifier, asset_entry in entry_dict.items():
            return_dict[lookup_identifier] = asset_entry
    return return_dict

