"""
Module that contains functions for interacting with the archetype assetlist


Using Archetypes to organize things. Some general recommendations.

I highly recommend sorting animation into the character organization, the biggest benefit is keeping
things which have dependencies on each other close together. Otherwise you'll need a scheme to mirror
the characters and animation directories which really is unfortunate for everyone involved.
Also when in doubt spell it out. Don't use abbreviations whenever possible. It makes it harder for
new folks who join a project mid development. Your organization structures should *reduce* the mental
overhead, not require a secret decoder ring.

Characters
    player
    # Sometimes your player and your npcs blend a little more, in that case don't make a distinction between
    # them if they're sharing vismodels and animation
    # this organization works well for a game with a primary player and enemy combatants.
        animation
            # I just recommend organizing some of the animations into sub dirs so you don't end up with
            # hundreds at the top level.
            _source
            movement
            attacks
            ? Maybe some more breakdowns in here.
        model
            _source
            meshes
            textures
        gear
            # If you're a live service game add a release directory here, if you go for a couple of "Seasons"
            # you'll find even the best organization structures break down without having a release folder.
            # If you're doing full armorsets switch "slot" and "piece descriptive name"
            slot: head, arms, legs, chest, hands, etc
                # Keep all variants close by, no one wants to rummage for them.
                # Normally one permutation is made first and modded to form the others, that one should
                # Contain the source and textures.
                piece_descriptive_name: wolf_shoulders
                    (optional - variation: orc, human, elf, dwarf, shared)
                        male
                            _source
                            meshes
                            textures
                        female
    npc
        (optional - faction, this should represent a group or faction within the game: soviets)
        # Note this can be used as a primary folder with an alternative organize style.
            name or skeleton archetype: sniper, human_male
                _source
                meshes
                textures
                (optional - variants: sniper_captain)
                # This should be used for alternative models that use the same base skeleton
                    _source
                    meshes
                    textures
    
    (alternative: biped)
    # Organize instead by skeletal archetype. For every character that will have the same core skeleton
    # You can organize them by a skeletal archetype.
    # this organization works well if the palyer model is shared with npcs, and there is a lot of gear
    # or shared equipment between npcs
        type: human, orc, elf
            animation
                _source
                movement
                attacks
            model
                ...
            variants
                ...
        gear (if gear will be shared place it at the top level, otherwise keep it with its type)
        # This can be elevated to the highest level if gear is the driving vis model for all characters.
            ...
    
    (alternative: major faction - Terran, Protoss, Zerg)
    # If there is a logical grouping due to major factions this is a good way to organize them
    # When organizing for major factions consider placing vehicles and weapons within the faction as well.
    # This works well when you have clear factions you're building a large amount of content for.

    weapons
    # Weapons are often shared so they can live in their own top level directory.
        archetype: bow, melee, revolver, pistol, shotgun_pump, rifle_automatic, rifle_lever
            animation
                _source
                # Probably safe to not sub divide weapon animations there tends to not be a lot, unless
                # It's a key weapon.
            model
                ...
            variants
                ...
    vehicles
    # Vehicles tend to be shared so keeping them here is a good plan, alternatively if you've got major
    # factions you can store them in there.
        name: tank_mammoth
            _source
            meshes
            textures

Cinematics
    # I have no strong suggestions here.
    # If running a live service game use releases to help organize this here.
    Shotname (or shot code)
        shot_number: 010, 020, 030, etc,
        #always use 10's so you can back fill shots if you need to.
            _source
            animation

EXAMPLE 1:
from assetlist import archetype_assetlist

new_archetype = archetype_assetlist.Archetype(data_dict={})
# This will be the name of the entry in the Wizard, and the register's entry key
new_archetype.name = 'NPC with Faction'
# This represents the base directory for this template, each of the $<<STR>> values will get replaced
new_archetype.base_dir = r'art_source\character\$faction_option\$sub_faction_option\$name\\'
hierarchy_dict = {}
asset_data_dict = {}
asset_data_dict['name'] = '$sub_faction_option_$name'
# Major type lets us sort these entries later. "model" will always have a "mesh_path",
# "rig" will always have a "skeleton_path" and "rig_path", "rigged_model" will expect both.
asset_data_dict['type'] = 'rigged_model'
# Subtypes are used to further organize our major types.
asset_data_dict['subtype'] = ['npc', '$archetype_name', '$faction_option']
asset_data_dict['rig_path'] = r"art_source\character\$faction_option\$sub_faction_option\$name\_source\\rigs\$name_rig.ma"
hierarchy_dict['asset_data'] = asset_data_dict
new_archetype.hierarchy = hierarchy_dict

# This ends the primary data section of the entry, everything below helps us setup the base dir and override values.
# Start of the options formatting each entry here will show up as a dynamic UI element.
# In this case we've got one extremely complicated entry that is a nested choice of sorted options.
# I'll have a few more examples below of how you can format this diffrently.
options_list = []
faction_choice_option = {}
faction_choice_option['name'] = 'faction_option'
faction_choice_option['type'] = 'nested_choice'
faction_choice_option['options'] = []
faction_choice_option['description'] = 'Select the universe faction:'
human_nested_choice = {}
human_nested_choice['name'] = 'human'
human_nested_choice['type'] = 'sorted_choice'
human_nested_choice['description'] = 'Choose a skeletal archetype.'
human_nested_choice['options'] = ['human_male', 'human_female']
faction_choice_option['options'].append(human_nested_choice)
orc_nested_choice = {}
orc_nested_choice['name'] = 'orc'
orc_nested_choice['type'] = 'sorted_choice'
orc_nested_choice['description'] = 'Choose a skeletal archetype.'
orc_nested_choice['options'] = ['orc_male', 'orc_female']
faction_choice_option['options'].append(orc_nested_choice)
elf_nested_choice = {}
elf_nested_choice['name'] = 'elf'
elf_nested_choice['type'] = 'sorted_choice'
elf_nested_choice['description'] = 'Choose a skeletal archetype.'
elf_nested_choice['options'] = ['elf_male', 'elf_female']
faction_choice_option['options'].append(elf_nested_choice)
options_list.append(faction_choice_option)
new_archetype.options = options_list

# Here we'll add an override to the template, this takes the default data on the new asset entry and replaces
# it based on some trigger conditions.
overrides_list = []
skel_override = {}
skel_override['type'] = 'data'
skel_override['trigger'] = {'option_var':'skeleton_option', 'inclusive':['human_male'], 'replace_prop':'asset_parent', 'replace_val':'rvls-9g1q9-qucd2-s5qk'}
overrides_list.append(skel_override)
new_archetype.overrides = overrides_list

# Lastly we register it to the archetype asset list.
new_archetype.register(True)

EXAMPLE 2:
from assetlist import archetype_assetlist

new_archetype = archetype_assetlist.Archetype(data_dict={})
new_archetype.name = 'Orc Armor'
new_archetype.base_dir = r'art_source\character\orc\gear\$armor_option\$faction_option\$slot_option\$sub_slot_option\$name\\'
hierarchy_dict = {}
asset_data_dict = {}
asset_data_dict['name'] = '$armor_option_$faction_option_$slot_option_$name'
asset_data_dict['type'] = 'model'
asset_data_dict['subtype'] = ['orc', '$armor_option', '$faction_option', '$slot_option']
# This value is hardcoded, but it'll allow entrys to inherit from a parent in the assetlist.
asset_data_dict['parent'] = 'rvls-9g1q9-qucd2-s5qk'
hierarchy_dict['asset_data'] = asset_data_dict
new_archetype.hierarchy = hierarchy_dict

options_list = []
armor_choice_option = {}
armor_choice_option['name'] = 'armor_option'
armor_choice_option['type'] = 'choice'
armor_choice_option['options'] = ['light', 'medium', 'heavy']
armor_choice_option['description'] = 'Select the armor type:'
options_list.append(armor_choice_option)

faction_choice_option = {}
faction_choice_option['name'] = 'faction_option'
faction_choice_option['type'] = 'sorted_choice'
faction_choice_option['options'] = ['hundrend_hands', 'red_birds', 'moon_moon_wolves']
faction_choice_option['description'] = 'Select the faction this armor belongs to:'
options_list.append(faction_choice_option)

slot_choice_option = {}
slot_choice_option['name'] = 'slot_option'
slot_choice_option['type'] = 'nested_choice'
slot_choice_option['options'] = ['head', 'shoulders', 'chest', 'arms', 'hand', 'legs', 'feet']
attachment_sub_option = {}
attachment_sub_option['name'] = 'attachments'
attachment_sub_option['type'] = 'sorted_choice'
attachment_sub_option['options'] = ['cloak', 'holster', 'belt_bits']
attachment_sub_option['description'] = 'Select the type of attachment:'
slot_choice_option['options'].append(attachment_sub_option)
slot_choice_option['description'] = 'Select the armor slot:'
options_list.append(slot_choice_option)
new_archetype.options = options_list

# "mirror" is a unique overide that pulls two asset entries into the organization structure and then nests
# them. This is valuable when you need different assets for the left/right of a character, but only want to
# represent them as a shared pair. (Easier on Character Art, easier on Technical Art for skinning.)
overrides_list = []
mirror_override = {}
mirror_override['type'] = 'mirror'
mirror_override['trigger'] = {'option_var':'slot_option', 'inclusive':['arms', 'shoulders', 'hand', 'feet']}
overrides_list.append(mirror_override)

attachment_override = {}
attachment_override['type'] = 'data'
attachment_override['trigger'] = {'option_var':'slot_option', 'inclusive':['attachment'], 'replace_prop':'skel_path', 'replace_val':r'$local\_source\$nicename.skl'}
overrides_list.append(attachment_override)
new_archetype.overrides = overrides_list
new_archetype.register(True)


"""

# python imports
import copy
import os
import time
# software specific imports
# Project python imports
from mca.common.assetlist import assetlist
from mca.common.modifiers import singleton
from mca.common.textio import yamlio
from mca.common.utils import dict_utils, fileio, string_utils, path_utils


from mca.common import log
logger = log.MCA_LOGGER


REGISTRY_FILE_PATH = assetlist.REGISTRY_FILE_PATH
ARCHETYPE_REGISTRY_PATH = os.path.join(os.path.dirname(REGISTRY_FILE_PATH), 'archetype_registry.yaml')


class ArchetypeRegistry(singleton.SimpleSingleton):
    REGISTRY_DICT = {}
    NAME_REGISTRY = {}
    DIR_REGISTRY = {}
    DIRTY = False

    LAST_EDIT = None

    def __init__(self, force=False):
        self.reload(force=force)

    def reload(self, force=False):
        self.REGISTRY_DICT = {}
        self.NAME_REGISTRY = {}
        self.DIR_REGISTRY = {}

        # Always sync before we load the registry, but do not force it in case there are local changes.
        #sourcecontrol.p4_sync(ARCHETYPE_REGISTRY_PATH)
        if os.path.exists(ARCHETYPE_REGISTRY_PATH):
            self.REGISTRY_DICT = yamlio.read_yaml(ARCHETYPE_REGISTRY_PATH) or {}
        else:
            # could not find the registry file.
            if not force:
                raise IOError(f'{ARCHETYPE_REGISTRY_PATH} The registry file was not found on disk, please verify you have latest.')
            self.REGISTRY_DICT = {}

        if os.path.exists(ARCHETYPE_REGISTRY_PATH):
            self.LAST_EDIT = time.ctime(os.path.getmtime(ARCHETYPE_REGISTRY_PATH))
        for name, data_dict in self.REGISTRY_DICT.items():
            archetype = Archetype(data_dict)
            self.NAME_REGISTRY[name] = archetype
            base_dir = data_dict.get('base_dir', None)
            if base_dir:
                self.DIR_REGISTRY[base_dir] = archetype

    def commit(self):
        if self.DIRTY:
            fileio.touch_path(ARCHETYPE_REGISTRY_PATH)
            yamlio.write_yaml(ARCHETYPE_REGISTRY_PATH, self.REGISTRY_DICT)
            self.DIRTY = False

    def register_asset(self, archetype_entry, commit=False):
        """
        This will serialize one of our data classes to the main register.

        :param Archetype archetype_entry: The  archetype to be registered.
        :param bool commit: If the registry should be saved after the addition. For perf reasons this can be held until
            multiple registers are completed.
        """

        registry_asset = copy.deepcopy(archetype_entry)
        self.NAME_REGISTRY[archetype_entry.name] = registry_asset
        self.REGISTRY_DICT[archetype_entry.name] = archetype_entry.get_data_dict()

        self.DIRTY = True
        if commit:
            self.commit()

class Archetype(object):
    _asset_name = ''
    _hierarchy = {}
    _base_dir = ''
    _options = []
    _organization = {}
    _overrides = []

    def __init__(self, data_dict):
        self._set_data(data_dict)

    def _set_data(self, data_dict):
        self._asset_name = data_dict.get('name', '')
        self._hierarchy = data_dict.get('hierarchy', {})
        self._base_dir = data_dict.get('base_dir', '')
        self._options = data_dict.get('options', [])
        self._organization = data_dict.get('organization', {})
        self._overrides = data_dict.get('overrides', [])

    @property
    def name(self):
        return self._asset_name

    @name.setter
    def name(self, val):
        self._asset_name = val

    @property
    def hierarchy(self):
        return self._hierarchy

    @hierarchy.setter
    def hierarchy(self, val):
        self._hierarchy = val

    @property
    def base_dir(self):
        return self._base_dir

    @base_dir.setter
    def base_dir(self, val):
        self._base_dir = path_utils.to_full_path(val)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, val):
        self._options = val

    def get_archetype_options(self):
        return_dict = {}
        for option_dict in self.options:
            option_name = option_dict.get('name', )
            if not option_name:
                continue
            return_dict[option_name] =[]
            for option_val in option_dict.get('options', []):
                if isinstance(option_val, list):
                    # A list from a paired choice
                    return_dict[option_name].append(option_val[0])
                elif isinstance(option_val, dict):
                    # A dict from a nested choice
                    return_dict[option_name].append(option_val.get('name'))
                else:
                    # Just a string
                    return_dict[option_name].append(option_val)
        return return_dict

    @property
    def organization(self):
        """
        tab_name = 'Rigs'
        type_list = []
        # If there are no subtypes all major types that match will be included on the tab
        subtype_list = [<<str>>, $<<option_name>>]
        # Each subtype will spawn a new tab(s) of the same name
        """
        return self._organization

    @organization.setter
    def organization(self, val):
        self._organization = val

    @property
    def overrides(self):
        return self._overrides

    @overrides.setter
    def overrides(self, val):
        self._overrides = val

    def get_data_dict(self):
        return_dict = {}
        return_dict['name'] = self.name
        return_dict['hierarchy'] = self.hierarchy
        return_dict['base_dir'] = path_utils.to_relative_path(self.base_dir)
        return_dict['options'] = self.options
        return_dict['organization'] = self.organization
        return_dict['overrides'] = self.overrides
        return return_dict

    def register(self, commit=True):
        registry = ArchetypeRegistry()
        registry.register_asset(self, commit=commit)


def get_archetype_registry():
    """
    Validate the asset list registry, reload it if it's out of date, before returning it.

    """
    registry = ArchetypeRegistry()
    if os.path.exists(ARCHETYPE_REGISTRY_PATH) and time.ctime(os.path.getmtime(ARCHETYPE_REGISTRY_PATH)) != registry.LAST_EDIT:
        registry.reload(True)
    return registry


def create_new_assets_from_archetype(archetype_entry, asset_name, remap_dict=None, base_dir=None):
    """
    From an Archetype return the Asset build structure.

    :param Archetype archetype_entry: A  Archetype class.
    :param str asset_name: Name of the new template.
    :param dict remap_dict: A dictionary of variables to replace in the template.
    :param str base_dir: The base directory this asset should be built.
    :param bool modified_base_dir: If the base directory has been modified from the templates expectations.
    :return: A freshly minted asset_entry based off this archetype.
    :rtype: Asset
    """
    remap_dict = {} if remap_dict is None else remap_dict
    remap_dict.update({'$local': base_dir, '$nicename': asset_name.replace(' ', '')})

    asset_entry = convert_template_to_asset(asset_name, base_dir or archetype_entry.base_dir, archetype_entry.hierarchy, remap_dict=remap_dict)

    # Maybe there is a better way to handle these? Maybe these are universally useful enough to keep them here?
    if archetype_entry.overrides:
        for override_data in archetype_entry.overrides:
            # Conditional check
            condition_val = override_data.get('trigger', {}).get('option_var')
            inclusive_val_list = override_data.get('trigger', {}).get('inclusive', [])
            exclusive_val_list = override_data.get('trigger', {}).get('exclusive', [])
            if f'${condition_val}' in remap_dict and (remap_dict[f'${condition_val}'] in inclusive_val_list and remap_dict[f'${condition_val}'] not in exclusive_val_list):
             # If the condition value is in the remap dict, and it's present in the inclusive list, and not in the exclusive list
                override_type = override_data.get('type')
                if override_type == 'mirror':
                    # We're duplicating this asset and appending side data. We'll always nest the left inside of the right.
                    asset_entry.mesh_path = asset_entry.mesh_path.replace('.', '_right.') # add the side indicator.

                    new_guid = string_utils.generate_guid()
                    nested_asset = copy.deepcopy(asset_entry)
                    asset_entry.asset_subtype += ['right']
                    nested_asset.asset_subtype += ['left', 'mirror']

                    nested_asset.asset_id = new_guid
                    nested_asset.mesh_path = nested_asset.mesh_path.replace('_right.', '_left.')

                    asset_entry.local_asset_list = [nested_asset]
                elif override_type == 'data':
                    # We have a value override, find it and its replacement value.
                    property_name = override_data.get('trigger', {}).get('replace_prop')
                    replace_val = override_data.get('trigger', {}).get('replace_val')
                    for search_str, replace_str in remap_dict.items():
                        replace_val = replace_val.replace(search_str, replace_str)
                    setattr(asset_entry, property_name, replace_val)
            else:
                logger.debug(f'{condition_val}\ninclusions: {inclusive_val_list}\nexclusions: {exclusive_val_list}\nConditions not met for override')

    return asset_entry


def convert_template_to_asset(asset_name, base_dir, hierarchy_dict, remap_dict=None):
    """
    This converts a template into valid Asset. This can be called recursively depending on the complexity
    of the template.

    :param str asset_name: Name of the new Asset build structure
    :param str base_dir: The base directory this asset should be built.
    :param dict hierarchy_dict: Dictionary containing the build structure for the Asset.
        Rough example template.
        {'asset_data':{property_name:property_value},
        'children':nested_dict, #This is optional
        'iterable_data':{'$childname':[str, ...],
                         '$alt_prop': [val, ...]} # This should only be used with children, and every entry should contain
                                                    a list of the same length. 3 children names, 3 alt_prop values.
        }
    :param dict remap_dict: A dictionary of strings to values that are remapped within each template entry.
    :return: Asset that are built from the template.
    :rtype: Asset
    """

    asset_id = string_utils.generate_guid()
    asset_entry = assetlist.Asset(asset_id, {})

    data_dict = hierarchy_dict.get('asset_data', {})
    if '$name' not in remap_dict:
        remap_dict.update({'$name': asset_name})
    local_remap_dict = data_dict
    local_remap_dict.update(remap_dict)

    # Set all properties using the remap_dict to adjust.
    for property_name, property_value in local_remap_dict.items():
        for search_str, replace_str in remap_dict.items():
            if isinstance(property_value, list):
                property_value = [item.replace(search_str, replace_str) for item in property_value]
            else:
                property_value = property_value.replace(search_str, replace_str)
        setattr(asset_entry, f'asset_{property_name}', property_value)

    if '$childname' in local_remap_dict:
        # Child entries spawn a sub dir.
        base_dir = os.path.join(base_dir, local_remap_dict['$childname'])

    if asset_entry.asset_type in ['model', 'rigged_model']:
        # EG: asset_name is The_Boulder, but the directory path is characters//NPC//Boulder we'll keep "Boulder"
        # model assets may have an override skeleton if they need to add joints for dynamics. They're kept separate the main skeleton.
        asset_entry.mesh_path = os.path.join(base_dir, 'meshes', f'sk_{asset_entry.asset_name}.fbx')
    if 'rig' in asset_entry.asset_type:
        # this will catch 'rig' and rigged_model'
        asset_entry.rig_path = os.path.join(base_dir, 'animation', 'rig', f'{asset_entry.asset_name}_rig.ma')
        asset_entry.skeleton_path = os.path.join(base_dir, 'animation', '_source', f'{asset_entry.asset_name}.skl')

    child_hierarchy_dict = hierarchy_dict.get('children')
    if child_hierarchy_dict:
        for index in range(len(child_hierarchy_dict['iterable_data']['$childname'])):
            # This takes a slice that lines up with which child is currently being iterated over.
            # EG: $childname = ['arms', 'legs', 'chest'] slices 0, 1, 2 respectively, all itertable data should have an entry for each slice that lines up.
            #    The entry name and the value at that slice get globbed with the remap_dict and passed recursviely down.
            child_remap_dict = dict_utils.get_dict_slice(child_hierarchy_dict.get('iterable_data', {}), index)
            child_remap_dict.update(data_dict)
            child_asset = convert_template_to_asset(asset_name, base_dir, child_hierarchy_dict, child_remap_dict)
            asset_entry.local_asset_list.append(child_asset)
    return asset_entry
