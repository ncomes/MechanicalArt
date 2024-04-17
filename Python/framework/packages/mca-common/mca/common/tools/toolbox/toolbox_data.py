#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import os

# software specific imports

# mca python imports
from mca.common import log

from mca.common.modifiers import singleton
from mca.common.paths import paths, path_utils
from mca.common.textio import yamlio
from mca.common.utils import fileio, strings

logger = log.MCA_LOGGER

LOCAL_TOOLBOX_DIR = os.path.join(paths.get_local_preferences_folder(), os.path.split(paths.get_dcc_tools_path())[-1], 'Toolbox')
DCC_TOOLBOX_DIR = os.path.join(paths.get_dcc_tools_path(), 'Toolbox')

class ToolboxLayout:
    _guid = ''
    _children = []

    def __init__(self, guid, data_dict):
        if not guid:
            guid = strings.generate_guid()
        self._guid = guid

        self._children = data_dict.get('children', [])

    @property
    def data(self):
        return_dict = {}
        return_dict['children'] = [x.id if not isinstance(x, str) else x for x in self.children]
        return self.id, return_dict

    @property
    def id(self):
        return self._guid

    @id.setter
    def id(self, value):
        self._guid = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value


class ToolboxCategory(ToolboxLayout):
    _guid = ''
    _children = []
    _display_name = ''
    _icon = ''
    _tooltip = ''

    def __init__(self, guid, data_dict):
        super().__init__(guid, data_dict)

        self._display_name = data_dict.get('display_name', '')
        self._icon = data_dict.get('icon')
        self._toolip = data_dict.get('tooltip')

    @property
    def data(self):
        return_dict = {}
        return_dict['display_name'] = self.display_name
        return_dict['children'] = [x.id if not isinstance(x, str) else x for x in self.children]
        return_dict['icon'] = self.icon
        return_dict['tooltip'] = self.tooltip
        return self.id, return_dict

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value


class ToolboxAction:
    _guid = ''
    _display_name = ''
    _tooltip = ''
    _icon = ''
    _command = ''
    _action_type = ''
    _color = None

    def __init__(self, guid, data_dict):
        if not guid:
            guid = strings.generate_guid()
        self._guid = guid

        self._display_name = data_dict.get('display_name', '')
        self._tooltip = data_dict.get('tooltip')
        self._icon = data_dict.get('icon')
        self._command = data_dict.get('command')
        self._action_type = data_dict.get('action_type')
        self._color = data_dict.get('color')

    @property
    def data(self):
        return_dict = {}
        return_dict['display_name'] = self.display_name
        return_dict['tooltip'] = self.tooltip
        return_dict['icon'] = self.icon
        return_dict['command'] = self.command
        return_dict['action_type'] = self.action_type
        return_dict['color'] = self.color
        return self.id, return_dict

    @property
    def id(self):
        return self._guid

    @id.setter
    def id(self, value):
        self._guid = value

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if (isinstance(value, list) and len(value) == 3) or value is None:
            self._color = value

    @property
    def action_type(self):
        return self._action_type

    @action_type.setter
    def action_type(self, value):
        self._action_type = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def tooltip(self):
        return self._tooltip

    @tooltip.setter
    def tooltip(self, value):
        self._tooltip = value


class ToolboxReference:
    _guid = ''
    _reference_id = ''
    _reference_toolbox = ''

    def __init__(self, guid, data_dict):
        if not guid:
            guid = strings.generate_guid()
        self._guid = guid

        self._reference_id = data_dict.get('reference_id')
        self._reference_toolbox = data_dict.get('reference_toolbox')

    @property
    def data(self):
        return_dict = {}
        return_dict['reference_id'] = self.reference_id
        return_dict['reference_toolbox'] = self.reference_toolbox
        return self.id, return_dict

    @property
    def id(self):
        return self._guid

    @id.setter
    def id(self, value):
        self._guid = value

    @property
    def reference_id(self):
        return self._reference_id

    @reference_id.setter
    def reference_id(self, value):
        self._reference_id = value

    @property
    def reference_toolbox(self):
        return self._reference_toolbox

    @reference_toolbox.setter
    def reference_toolbox(self, value):
        self._reference_toolbox = value


class Toolbox:
    EXT = "tbx"

    _toolbox_name = None
    _path = None
    _data_dict = {}

    ACTION_DICT = {}
    LAYOUT_DICT = {}
    CATEGORY_DICT = {}
    REFERENCE_DICT = {}

    DIRTY = False

    def __init__(self, file_path, force=True):
        if not os.path.exists(file_path) and not force:
            'File not found on disk.'
            return

        if not file_path.endswith(f'.{self.EXT}'):
            'File is not a valid toolbox file.'
            return

        self._toolbox_name = os.path.basename(file_path).split('.')[0]
        self._path = file_path

        self._data_dict = {}

        self.ACTION_DICT = {}
        self.LAYOUT_DICT = {}
        self.CATEGORY_DICT = {}
        self.REFERENCE_DICT = {}

        self.parse_toolbox(True)

    @property
    def GUID_DICT(self):
        # Assigning the entry data classes to two dictionaries causes an instancing error, this gets around it.
        return {**self.ACTION_DICT, **self.LAYOUT_DICT, **self.CATEGORY_DICT, **self.REFERENCE_DICT}

    @property
    def toolbox_name(self):
        return self._toolbox_name

    @toolbox_name.setter
    def toolbox_name(self, val):
        self._toolbox_name = val

    @property
    def path(self):
        return path_utils.to_full_path(self._path)

    @path.setter
    def path(self, val):
        self._path = val

    def parse_toolbox(self, force=False):
        if not self.path:
            'Path not set cannot parse data, a valid path is required to init a toolbox.'
            return
        elif os.path.exists(self.path) and (not self._data_dict or force):
            # file is on disk and we want to read it because we have no data or we want to reread it by force
            # file is on disk and we want to re-read it.
            self._data_dict = yamlio.read_yaml_file(self.path)
        elif os.path.exists(self.path) and not force:
            # file is on disk but we don't want to re read it.
            return
        elif not os.path.exists(self.path) and force:
            # file is not on disk, but we want it to parse whatever data we might have.
            pass
        elif not os.path.exists(self.path):
            # fie is not on disk and we want to fail the parse
            return

        self.ACTION_DICT = {}
        self.LAYOUT_DICT = {}
        self.CATEGORY_DICT = {}
        self.REFERENCE_DICT = {}

        for toolbox_category, entry_dict in self._data_dict.items():
            for entry_guid, entry_data_dict in entry_dict.items():
                if toolbox_category == 'actions':
                    data_class = ToolboxAction(entry_guid, entry_data_dict)
                    self.ACTION_DICT[entry_guid] = data_class
                elif toolbox_category == 'layouts':
                    data_class = ToolboxLayout(entry_guid, entry_data_dict)
                    self.LAYOUT_DICT[entry_guid] = data_class
                elif toolbox_category == 'categories':
                    data_class = ToolboxCategory(entry_guid, entry_data_dict)
                    self.CATEGORY_DICT[entry_guid] = data_class
                elif toolbox_category == 'references':
                    data_class = ToolboxReference(entry_guid, entry_data_dict)
                    self.REFERENCE_DICT[entry_guid] = data_class

    def commit(self):
        if self.DIRTY:
            fileio.touch_path(self.path)
            yamlio.write_to_yaml_file(self._data_dict, self.path)
            self.DIRTY = False

    def set_entry(self, toolbox_data_class, commit=False):
        """
        Of a Toolbox<DataClass> type register it to this toolbox.

        :param ToolboxAction|ToolboxLayout|ToolboxCategory|ToolboxReference toolbox_data_class: A toolbox data class to register.
        :param bool commit: If this toolbox should be saved to disk after this operation.
        """
        if isinstance(toolbox_data_class, ToolboxCategory):
            self.CATEGORY_DICT[toolbox_data_class.id] = toolbox_data_class
            if 'categories' not in self._data_dict:
                self._data_dict['categories'] = {}
            self._data_dict['categories'].update(dict([toolbox_data_class.data]))
            self.DIRTY = True
        elif isinstance(toolbox_data_class, ToolboxLayout):
            self.LAYOUT_DICT[toolbox_data_class.id] = toolbox_data_class
            if 'layouts' not in self._data_dict:
                self._data_dict['layouts'] = {}
            self._data_dict['layouts'].update(dict([toolbox_data_class.data]))
            self.DIRTY = True
        elif isinstance(toolbox_data_class, ToolboxAction):
            self.ACTION_DICT[toolbox_data_class.id] = toolbox_data_class
            if 'actions' not in self._data_dict:
                self._data_dict['actions'] = {}
            self._data_dict['actions'].update(dict([toolbox_data_class.data]))
            self.DIRTY = True
        elif isinstance(toolbox_data_class, ToolboxReference):
            self.REFERENCE_DICT[toolbox_data_class.id] = toolbox_data_class
            if 'references' not in self._data_dict:
                self._data_dict['references'] = {}
            self._data_dict['references'].update(dict([toolbox_data_class.data]))
            self.DIRTY = True

        if commit:
            self.commit()

    def remove_entry(self, guid, commit=False, clean_parent=False):
        """
        Remove an entry from this toolbox.

        :param str guid: The guid that represents a toolbox_data_class.
        :param bool commit: If this toolbox should be saved to disk after this operation.
        """
        for entry_dict, entry_name in zip([self.CATEGORY_DICT, self.LAYOUT_DICT, self.ACTION_DICT, self.REFERENCE_DICT], ['categories', 'layouts', 'actions', 'references']):
            found_key = entry_dict.pop(guid, None)
            if found_key:
                if not isinstance(found_key, (ToolboxAction, ToolboxReference)):
                    # If we found an entry and it's not an Action or Reference. Recursively remove its children.
                    for child_guid in found_key.children:
                        self.remove_entry(child_guid)

                if entry_name and entry_name in self._data_dict:
                    self._data_dict[entry_name].pop(guid, None)
                self.DIRTY = True
                break

        if clean_parent:
            # Only on first run check for the parent layout or category and remove the reference to this guid.
            for _, toolbox_data_class in {**self.CATEGORY_DICT, **self.LAYOUT_DICT}.items():
                children_guid_list = toolbox_data_class.children
                if guid in toolbox_data_class.children:
                    children_guid_list.remove(guid)
                try:
                    if isinstance(toolbox_data_class, ToolboxCategory):
                        self._data_dict['categories'][toolbox_data_class.id]['children'].remove(guid)
                    elif isinstance(toolbox_data_class, ToolboxLayout):
                        self._data_dict['layouts'][toolbox_data_class.id]['children'].remove(guid)
                except:
                    "Guid wasn't found so it's already removed."

        if commit:
            self.commit()

    def get_build_order(self):
        """
        Return a master build dict for this toolbox.
        The dictionary should be formatted as such.
        {'toolbox_class: Toolbox<DataClass>,
         'children: [{entry, entry, entry}]}

         Notably action data classes have no children so they are our leaves.

        :return: A master build dict for this toolbox.
        :rtype: dict
        """
        main_category = self.GUID_DICT.get('Main', {})
        return self._get_build_order_from_entry(main_category)

    def _get_build_order_from_entry(self, entry):
        """
        Recursive function designed to map a build structure for a toolbox from an entry.

        :param ToolboxCategory|ToolboxLayout|ToolboxAction|ToolboxReference entry: A Toolbox data class within this
            toolbox to map from.
        :return: The build dictionary for this entry down.
        :rtype: dict
        """
        return_dict = {}
        if isinstance(entry, ToolboxReference):
            toolbox_name = entry.reference_toolbox
            reference_id = entry.reference_id

            found_toolbox = get_toolbox_by_name(toolbox_name)
            if found_toolbox:
                return found_toolbox._get_build_order_from_entry(found_toolbox.GUID_DICT.get(reference_id))
        elif isinstance(entry, ToolboxAction):
            return_dict['toolbox_class'] = entry
        elif isinstance(entry, (ToolboxCategory, ToolboxLayout)):
            return_dict['toolbox_class'] = entry
            return_dict['children'] = []
            for x in entry.children:
                if x in self.GUID_DICT:
                    return_dict['children'].append(self._get_build_order_from_entry(self.GUID_DICT[x]))
        return return_dict


class ToolboxRegistry(singleton.SimpleSingleton):
    """
    Singleton class that handles distribution of all found toolboxes.

    """
    TOOLBOX_NAME_DICT = {}
    REFERENCED_GUID_LIST = []

    def __init__(self):
        self.reload()

    def reload(self):
        """
        Clear the cache and reload each toolbox.

        """

        self.TOOLBOX_NAME_DICT = {}
        self.REFERENCED_GUID_LIST = []

        toolbox_file_path_list = []
        for toolbox_directory in [LOCAL_TOOLBOX_DIR, DCC_TOOLBOX_DIR]:
            if os.path.exists(toolbox_directory):
                for file_name in os.listdir(toolbox_directory):
                    if file_name.endswith(Toolbox.EXT):
                        toolbox_file_path_list.append(os.path.join(toolbox_directory, file_name))

        for toolbox_file_path in toolbox_file_path_list:
            # Server side toolbox will overwrite local toolboxes.
            toolbox_name = os.path.basename(toolbox_file_path).split('.')[0]
            if toolbox_name in self.TOOLBOX_NAME_DICT:
                logger.warning(f'{toolbox_name} there is a local version of this toolbox and its reference will be overwritten')
                continue
            found_toolbox = Toolbox(toolbox_file_path)
            self.TOOLBOX_NAME_DICT[toolbox_name] = found_toolbox
            for _, toolbox_data_class in found_toolbox.REFERENCE_DICT.items():
                reference_id = toolbox_data_class.reference_id
                if reference_id not in self.REFERENCED_GUID_LIST:
                    self.REFERENCED_GUID_LIST.append(reference_id)


def get_toolbox_by_name(toolbox_name):
    """
    By name return a toolbox

    :param str toolbox_name: The name of the toolbox to be found.
    :return: The found Toolbox
    :rtype: Toolbox
    """
    return ToolboxRegistry().TOOLBOX_NAME_DICT.get(toolbox_name)


def get_entry_by_reference(toolbox_reference):
    """
    By ToolboxReference data return the real data it represents.

    :param ToolboxReference toolbox_reference: The ToolboxReference data class used to look up the real data.
    :return: The live data referred to by this reference.
    :rtype: ToolboxReference | ToolboxCategory | ToolboxActionLayout | ToolboxAction
    """
    toolbox_name = toolbox_reference.toolbox_name
    entry_guid = toolbox_reference.id

    found_toolbox = get_toolbox_by_name(toolbox_name)
    if found_toolbox:
        return found_toolbox.GUID_DICT.get(entry_guid)
