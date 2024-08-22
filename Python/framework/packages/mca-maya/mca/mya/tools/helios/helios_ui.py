"""
Module that contains UI functions for Helios, and the wizard.
"""

# python imports
import inspect
import os
import random
import re
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui
# software specific imports
import pymel.all as pm
# Project python imports
from mca.mya.rigging import joint_utils
from mca.mya.pyqt import maya_dialogs, mayawindows
from mca.mya.tools.helios import helios_utils
from mca.mya.utils import dag_utils

from mca.common.assetlist import assetlist, archetype_assetlist
from mca.common.pyqt.qt_utils import general_utils
from mca.common.resources import resources
from mca.common.utils import fileio, list_utils, path_utils

from mca.common import log
logger = log.MCA_LOGGER

WIZARD_LIST = ['Albus', 'Bigby', 'Strange', 'Elminster', 'Gandalf', 'Glinda', 'Howl', 'Jareth', 'Merlin', 'Frank',
               'Mordenkainen', 'Puck', 'Raistlin', 'Rasputin', 'Ravenna', 'Sauron', 'Tim', 'Vecna', 'Vivi', 'Zatanna']

WIZARD = None

MISSING_ICON = resources.icon(r'color\question.png')

LOCAL_PATH = os.path.dirname(inspect.getabsfile(inspect.currentframe()))

def summon_the_wizard():
    global WIZARD
    try:
        WIZARD.close()
    except:
        pass
    WIZARD = Wizard()
    WIZARD.show()


class Wizard(mayawindows.MCAMayaWindow):
    """
    The wizard for setting up initial Assets and organizing your scene.

    """
    _version = 1.0

    DYNAMIC_UI_ELEMENTS = []

    def __init__(self):
        ui_path = os.path.join(LOCAL_PATH, 'uis', f'wizard_ui.ui')
        super().__init__(title='Wizard',
                         ui_path=ui_path,
                         version=str(self._version))
        self.setWindowTitle(f'MCA {random.choice(WIZARD_LIST)} {self._version}')

        self.setup_signals()
        self.initialize_lists()

    # Initialization/Core UI
    def setup_signals(self):
        """
        Connect all buttons to their fncs.

        """

        self.ui.asset_select_comboBox.currentIndexChanged.connect(self.setup_dynamic_ui)
        self.ui.name_lineEdit.textChanged.connect(self._title_name)

        self.ui.organize_pushButton.clicked.connect(self.organize_scene_pressed)

        self.ui.export_dir_browse_pushButton.clicked.connect(self.browse_export_directory_pressed)
        self.ui.explore_to_pushButton.clicked.connect(self.explore_to_directory_pressed)

    def initialize_lists(self):
        archetype_registry = archetype_assetlist.get_archetype_registry()
        self.ui.asset_select_comboBox.addItems(sorted(archetype_registry.NAME_REGISTRY.keys()))

    def setup_dynamic_ui(self):
        self.clear_layout(self.ui.modular_ui_verticalLayout)
        self.DYNAMIC_UI_ELEMENTS = []
        archetype_registry = archetype_assetlist.get_archetype_registry()
        current_archetype = self.ui.asset_select_comboBox.currentText()

        archetype_entry = archetype_registry.NAME_REGISTRY.get(current_archetype, None)
        for option_data in archetype_entry.options:
            option_type = option_data['type']

            new_choice = None
            if option_type in ['choice', 'sorted_choice']:
                new_choice = self.Choice(self, option_data, False if option_type == 'choice' else True)
            elif option_type in ['nested_choice']:
                new_choice = self.NestedChoice(self, option_data)
            elif option_type in ['paired_choice']:
                new_choice = self.PairedChoice(self, option_data)

            if new_choice:
                self.DYNAMIC_UI_ELEMENTS.append(new_choice)

        self.preview_export_path()
        ui_number = len(self.DYNAMIC_UI_ELEMENTS)
        self.resize(600, 180 + (ui_number*100))

    class Choice(object):
        option_data = None
        def __init__(self, parent, option_data, is_sorted=False):
            self.option_data = option_data

            self.parent_ui = parent
            self.parent_layout = parent.ui.modular_ui_verticalLayout

            vertical_layout = qtwidgets.QVBoxLayout()
            self.parent_layout.addLayout(vertical_layout)

            new_box = qtwidgets.QGroupBox()
            vertical_layout.addWidget(new_box)
            self.box_layout = qtwidgets.QVBoxLayout()
            new_box.setLayout(self.box_layout)

            horizontal_layout_choice = qtwidgets.QHBoxLayout()
            #horizontal_layout_edit = qtwidgets.QHBoxLayout()
            self.box_layout.addLayout(horizontal_layout_choice)
            #self.box_layout.addLayout(horizontal_layout_edit)

            self.option_name = self.option_data['name']
            option_description = self.option_data['description']

            option_list_values = []
            for x in self.option_data['options']:
                if isinstance(x, str):
                    # If it's a regular list just append the str option
                    option_list_values.append(x)
                elif isinstance(x, dict):
                    # If we have a dict it's a nested choice, get the new name value
                    option_list_values.append(x.get('name', ''))
                elif isinstance(x, list):
                    # If it's a list we have a nicename, and other values associated with that choice.
                    option_list_values.append(x[0])

            new_label = qtwidgets.QLabel()
            new_label.setText(option_description)
            horizontal_layout_choice.addWidget(new_label)

            choice_horizontal_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Expanding)
            horizontal_layout_choice.addItem(choice_horizontal_spacer)

            self.new_combobox = qtwidgets.QComboBox()
            self.new_combobox.addItems(sorted(option_list_values) if is_sorted else option_list_values)
            self.new_combobox.setEditable(True)
            self.new_combobox.currentTextChanged.connect(self.parent_ui.preview_export_path)
            self.new_combobox.setMinimumWidth(120)
            horizontal_layout_choice.addWidget(self.new_combobox)

            #edit_horizontal_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Expanding)
            #horizontal_layout_edit.addItem(edit_horizontal_spacer)

            #add_button = qtwidgets.QPushButton('Add Option')
            #add_button.clicked.connect(self.add_archetype_option)
            #horizontal_layout_edit.addWidget(add_button)

            #remove_button = qtwidgets.QPushButton('Remove Option')
            #remove_button.clicked.connect(self.remove_archetype_option)
            #horizontal_layout_edit.addWidget(remove_button)

        def add_archetype_option(self):
            new_option_val = self.new_combobox.currentText()
            current_archetype = self.parent_ui.ui.asset_select_comboBox.currentText()
            archetype_registry = archetype_assetlist.get_archetype_registry()
            archetype_entry = archetype_registry.NAME_REGISTRY.get(current_archetype, None)
            options_list = archetype_entry.options
            modified_list = []
            for option in options_list:
                if option['name'] == self.option_name and new_option_val not in option['options']:
                    modified_list.append({'name': option['name'],
                                          'type': option['type'],
                                          'description': option['description'],
                                          'options': option['options'] + [new_option_val]})

                    archetype_entry.DIRTY = True
                else :
                    modified_list.append(option)

            if archetype_entry.DIRTY:
                archetype_entry.options = modified_list
                archetype_entry.register(True)

        def remove_archetype_option(self):
            option_val_to_remove = self.new_combobox.currentText()
            current_archetype = self.parent_ui.ui.asset_select_comboBox.currentText()
            archetype_registry = archetype_assetlist.get_archetype_registry()
            archetype_entry = archetype_registry.NAME_REGISTRY.get(current_archetype, None)
            options_list = archetype_entry.options
            modified_list = []
            for option in options_list:
                if option['name'] == self.option_name and option_val_to_remove in option['options']:
                    local_options_list = option['options']
                    local_options_list.remove(option_val_to_remove)
                    modified_list.append({'name': option['name'],
                                          'type': option['type'],
                                          'description': option['description'],
                                          'options': local_options_list})
                    archetype_entry.DIRTY = True
                else:
                    modified_list.append(option)

            if archetype_entry.DIRTY:
                archetype_entry.options = modified_list
                archetype_entry.register(True)

        def get_option_val(self):
            return {f'${self.option_name}': self.new_combobox.currentText()}

    class PairedChoice(Choice):
        def get_option_val(self):
            current_option = self.new_combobox.currentText()
            return_dict = {f'${self.option_name}': current_option}
            for x in self.option_data['options']:
                if x[0] == current_option:
                    for i, pair_str in enumerate(x[1:]):
                        return_dict[f'${i+1}{self.option_name}'] = pair_str
            return return_dict

    class NestedChoice(Choice):
        sub_layout = None
        sub_combobox = None

        def __init__(self, parent, option_data, is_sorted=False):
            super().__init__(parent, option_data, is_sorted)
            # Grab the existing layout option.
            self.new_combobox.currentTextChanged.connect(self._check_for_sub)
            self._check_for_sub()

        def _check_for_sub(self):
            options_list = []
            sub_options_list = {}
            for option_val in self.option_data.get('options', []):
                if isinstance(option_val, dict):
                    sub_options_list[option_val.get('name')] = option_val
                else:
                    options_list.append(option_val)
            current_option = self.new_combobox.currentText()
            if current_option in options_list:
                self._remove_sub_option()
            elif current_option in sub_options_list:
                self._remove_sub_option()
                self._add_sub_option(sub_options_list.get(current_option, {}))

        def _add_sub_option(self, option_data):
            self.sub_layout = qtwidgets.QVBoxLayout()
            self.box_layout.addLayout(self.sub_layout)

            horizontal_layout_choice = qtwidgets.QHBoxLayout()
            self.sub_layout.addLayout(horizontal_layout_choice)

            option_description = option_data['description']

            option_list_values = [x if not isinstance(x, dict) else x['name'] for x in option_data['options']]

            new_label = qtwidgets.QLabel()
            new_label.setText(option_description)
            horizontal_layout_choice.addWidget(new_label)

            choice_horizontal_spacer = qtwidgets.QSpacerItem(40, 20, qtwidgets.QSizePolicy.Expanding)
            horizontal_layout_choice.addItem(choice_horizontal_spacer)

            self.sub_combobox = qtwidgets.QComboBox()
            self.sub_combobox.addItems(sorted(option_list_values) if 'sorted' in option_data.get('type', '') else option_list_values)
            self.sub_combobox.setEditable(True)
            self.sub_combobox.currentTextChanged.connect(self.parent_ui.preview_export_path)
            self.sub_combobox.setMinimumWidth(100)
            horizontal_layout_choice.addWidget(self.sub_combobox)

            self.parent_ui.preview_export_path()

        def _remove_sub_option(self):
            if self.sub_layout:
                general_utils.delete_layout_and_children(self.box_layout, self.sub_layout)
                self.sub_combobox = None
                self.parent_ui.preview_export_path()

        def get_option_val(self):
            return_dict = {f'${self.option_name}': self.new_combobox.currentText()}
            if self.sub_combobox:
                return_dict[f'$sub_{self.option_name}'] = self.sub_combobox.currentText()
            else:
                return_dict[f'$sub_{self.option_name}'] = ''
            return return_dict


    def clear_layout(self, layout):
        """
        Removes all QWidgets from a QLayout

        :param QLayout layout:
        """

        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().close()
                    child.widget().setParent(None)
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    # Ui Helpers
    def _title_name(self):
        """
        Forces the first letter of each word to be capitalized.

        """
        set_titles = False
        cursor_pos = self.ui.name_lineEdit.cursorPosition()
        start_len = len(self.ui.name_lineEdit.text())
        if set_titles:
            split_string = self.ui.name_lineEdit.text().split(' ')
            titled_string = ''
            if split_string != ['']:
                titled_string = ' '.join(x[0].upper() + x[1:] if x else x for x in split_string)
            
        else:
            titled_string = self.ui.name_lineEdit.text().lower()
        
        #cleanup invalid characters.
        pattern = re.compile('[^a-zA-Z0-9_ ]+')
        titled_string = pattern.sub('', titled_string)

        str_len = len(titled_string)
        if str_len < start_len:
            # If we remove characters adjust the cursor position.
            cursor_pos = cursor_pos-1 if cursor_pos-1 >= 0 else 0

        self.ui.name_lineEdit.setText(titled_string)
        self.ui.name_lineEdit.setCursorPosition(cursor_pos) if str_len >= cursor_pos else self.ui.name_lineEdit.setCursorPosition(str_len)
        self.preview_export_path()

    def _get_remap_dict(self):
        """
        Querries each of the dynamic UI elements to get the current option values.

        :return: The remap dictionary of option values.
        :rtype: dict
        """
        remap_dict = {}
        for option in self.DYNAMIC_UI_ELEMENTS:
            remap_dict.update(option.get_option_val())
        return remap_dict

    def _get_export_path(self):
        """
        Grab's the archetype selected and modifies the base path with the current option values.

        :return: Relative path to the export directory
        :rtype: str
        """
        archetype_registry = archetype_assetlist.get_archetype_registry()
        current_archetype = self.ui.asset_select_comboBox.currentText()

        archetype_entry = archetype_registry.NAME_REGISTRY.get(current_archetype, None)
        remap_dict = {'$name': self.ui.name_lineEdit.text().replace(' ', '_')}
        remap_dict.update(self._get_remap_dict())
        asset_path = archetype_entry.base_dir
        for search_str, replace_str in remap_dict.items():
            asset_path = asset_path.replace(search_str, replace_str)

        return os.path.normpath(asset_path)

    def preview_export_path(self):
        """
        Update the preview directory text box with the current option values.

        """
        self.ui.export_dir_lineEdit.setText(self._get_export_path())

    def browse_export_directory_pressed(self):
        """
        Override the current preview directory by browsing for a new directory.

        """
        start_path = path_utils.to_full_path(self._get_export_path())

        found_path = qtwidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', start_path)
        if not found_path:
            return

        self.ui.export_dir_lineEdit.setText(path_utils.to_relative_path(found_path))

    def explore_to_directory_pressed(self):
        """
        Open the current preview directory in a file explorer.

        """
        asset_path = f'{path_utils.to_full_path(self._get_export_path())}\\'

        fileio.touch_path(asset_path)

        fileio.explore_to_path(asset_path)

    def organize_scene_pressed(self):
        """
        Convert the UI into an organized scene for exporting a model asset.
        Optionally, create the folder structure for this asset.

        """

        asset_name = self.ui.name_lineEdit.text()
        if not asset_name:
            raise ValueError('Please enter a name for the new asset, every asset deserves a name.')
        remap_dict = self._get_remap_dict()

        archetype_registry = archetype_assetlist.get_archetype_registry()
        current_archetype = self.ui.asset_select_comboBox.currentText()

        archetype_entry = archetype_registry.NAME_REGISTRY.get(current_archetype, None)

        asset_entry = archetype_assetlist.create_new_assets_from_archetype(archetype_entry, asset_name, remap_dict, base_dir=self.ui.export_dir_lineEdit.text())
        if 'model' not in archetype_entry.hierarchy.get('asset_data', {}).get('type'):
            # If we don't have a model, punt on scene organization
            # But do register the new asset based off the archetype.
            asset_entry.register(True)

        if self.ui.create_now_checkBox.isChecked() and 'model' in archetype_entry.hierarchy.get('asset_data', {}).get('type'):
            # If we have a model asset and we want to organize the directory too
            starting_directory = self.ui.export_dir_lineEdit.text()
            for path_str in ['_source\\', 'meshes\\', 'textures\\']:
                fileio.touch_path(os.path.join(path_utils.to_full_path(starting_directory), path_str))

        # $TODO error checking for existing?
        # We have a model, model's are designed to have vis mesh associated with them, so we'll organize the scene
        helios_utils.import_asset(asset_entry)

class Helios(mayawindows.MCAMayaWindow):
    """
    Helios is the Import/Export nexus for the asset environment.

    """
    _version = 1.0

    DYNAMIC_UI_ELEMENTS = []

    def __init__(self):
        ui_path = os.path.join(LOCAL_PATH, 'uis', 'helios_ui.ui')
        super().__init__(title='Helios',
                         ui_path=ui_path,
                         version=str(self._version))

        self.setup_signals()

        # Grab latest before we inititalize lists.
        #sourcecontrol.sync_files(assetlist.REGISTRY_FILE_PATH)
        self.initialize_lists()

    class AssetItem(qtgui.QStandardItem):
        ASSET_ENTRY = None
        def __init__(self, asset_entry):
            super().__init__()
            self.ASSET_ENTRY = asset_entry

            self.setEditable(False)

            self.setText(asset_entry.asset_name)
            asset_icon = None
            if asset_entry.mesh_path:
                asset_icon_path = f'{asset_entry.mesh_path[:-3]}jpg'
                if os.path.exists(asset_icon_path):
                    asset_icon = qtgui.QIcon(asset_icon_path)
            self.setIcon(asset_icon or MISSING_ICON)


    class FilterableListWidget(qtwidgets.QListView):
        ITEM_LIST = None
        def __init__(self, parent_layout, item_list):
            super().__init__()
            parent_layout.addWidget(self)
            self.entry = qtgui.QStandardItemModel()
            self.setModel(self.entry)
            self.setSpacing(2)
            self.setIconSize(qtcore.QSize(64, 64))

            self.ITEM_LIST = item_list

            self.filterList('')

        def filterList(self, filter_string):
            inclusive_list = []
            exclusive_list = []
            split_string = filter_string.split(' ')
            if split_string != ['']:
                for x in split_string:
                    if x.startswith('-'):
                        exclusive_list.append(x[1:].lower())
                    else:
                        inclusive_list.append(x.lower())

            filtered_list = []
            if inclusive_list or exclusive_list:
                self.entry.clear()
                for item in self.ITEM_LIST:
                    if all(True if x in item.text().lower() else False for x in inclusive_list) and all(True if x not in item.text().lower() else False for x in exclusive_list):
                        filtered_list.append(item)

                if filtered_list:
                    for item in filtered_list:
                        self.entry.appendRow(item)
            else:
                self.entry.clear()
                for item in self.ITEM_LIST:
                    self.entry.appendRow(item)

    def setup_signals(self):
        self.ui.wizard_pushButton.clicked.connect(summon_the_wizard)

        self.ui.filter_lineEdit.textChanged.connect(self._filter_lists)

        self.ui.open_source_pushButton.clicked.connect(self.open_source_directory_pushed)
        self.ui.remove_entry_pushButton.clicked.connect(self.remove_entry_pushed)

        self.ui.import_pushButton.clicked.connect(self.import_button_pressed)
        self.ui.export_pushButton.clicked.connect(self.export_button_pressed)
        self.ui.export_all_pushButton.clicked.connect(lambda: self.export_button_pressed(True))

    def initialize_lists(self):
        self.DYNAMIC_UI_ELEMENTS = []

        main_tab_widget = self.ui.import_tabWidget
        for i in reversed(range(main_tab_widget.count())):
            main_tab_widget.removeTab(i)

        asset_registry = assetlist.get_registry()
        archetype_registry = archetype_assetlist.get_archetype_registry()
        tab_organization_dict = {}
        for _, archetype_entry in archetype_registry.NAME_REGISTRY.items():
            organization_dict = archetype_entry.organization
            if not organization_dict:
                continue
            
            tab_name = organization_dict.get('tab_name')
            if tab_name not in tab_organization_dict:
                tab_organization_dict[tab_name] = {'name': tab_name, 'type': [], 'sub_tabs': []}
            for tab_type_filter in organization_dict.get('type'):
                if tab_type_filter not in tab_organization_dict[tab_name]['type']:
                    tab_organization_dict[tab_name]['type'].append(tab_type_filter)

            organization_list = archetype_entry.get_archetype_options()
            subtype_list = organization_dict.get('subtype')
            if len(subtype_list) == 1:
                # If we have a single subtype we won't be making sub tabs, this could also be a list of subtypes to a filter a type list.
                # IE: [npc]
                tab_organization_dict[tab_name]['subtype'] = subtype_list[0]
            elif subtype_list:
                # Order is important here check it later.
                tab_organization_dict[tab_name]['sub_tabs'] = self._organize_subtype_tab(organization_list, subtype_list)
        
        main_set = list(asset_registry.ASSET_ID_DICT.values())
        for _, tab_dict in tab_organization_dict.items():
            type_filter = tab_dict.get('type')
            subtype_filter = tab_dict.get('subtype', [])

            current_set = []
            if type_filter:
                for asset_entry in main_set[:]:
                    if asset_entry.asset_type not in type_filter:
                        continue

                    if subtype_filter:
                        if not all(True if x in asset_entry.asset_subtype else False for x in subtype_filter):
                            continue
                    
                    current_set.append(asset_entry)

            if not current_set:
                continue

            self._fill_sub_tabs(current_set, [tab_dict], main_tab_widget, True)
                
    def _organize_subtype_tab(self, organization_list, subtype_list):
        tab_dict_list = []
        if subtype_list:
            lookup = subtype_list[0]
            if not isinstance(lookup, list):
                if lookup.startswith('$'):
                    lookup = organization_list.get(lookup[1:])
            for subtype_name in lookup:
                tab_dict = {'name': subtype_name, 'sub_tabs': []}
                tab_dict_list.append(tab_dict)
                if len(subtype_list) > 1:
                    tab_dict['sub_tabs'] += self._organize_subtype_tab(organization_list, subtype_list[1:])
        return tab_dict_list
    
    def _fill_sub_tabs(self, current_set, tab_list, current_tab_widget, ignore_filter=False):
        if not current_set:
            return
        
        for sub_tab in tab_list:
            # Add our new tab
            sub_tab_name = sub_tab.get('name')

            if not ignore_filter:
                # Filter by the subtype, and also pitch anything with 'mirror' in the subtype.
                filtered_set = [x for x in current_set[:] if sub_tab_name in x.asset_subtype and 'left' not in x.asset_subtype]
            else:
                filtered_set = current_set[:]

            if not filtered_set:
                continue

            new_widget = qtwidgets.QWidget()
            current_tab_widget.addTab(new_widget, sub_tab_name)
            # Filter the current set, and set it or pass it down.

            new_tab_layout = qtwidgets.QVBoxLayout()
            new_widget.setLayout(new_tab_layout)

            sub_tab_list = sub_tab.get('sub_tabs')
            if sub_tab_list:
                # if we have a sub_tab_list we're going deeper.
                new_tab_widget = qtwidgets.QTabWidget()
                new_tab_layout.addWidget(new_tab_widget)
                self._fill_sub_tabs(filtered_set, sub_tab_list, new_tab_widget)
            else:
                # If we don't have any sub_tabs we've hit our depth limit and we can add items straight away.
                # create new list widget
                item_list = []
                for asset_entry in sorted(filtered_set, key=lambda x: x.asset_name):
                    # Sort by name to create a new AssetItem list.
                    new_item = self.AssetItem(asset_entry)
                    item_list.append(new_item)

                if item_list:
                    new_list_widget = self.FilterableListWidget(new_tab_layout, item_list)
                    self.DYNAMIC_UI_ELEMENTS.append(new_list_widget)

    def _filter_lists(self):
        filter_string = self.ui.filter_lineEdit.text()
        for list_ui in self.DYNAMIC_UI_ELEMENTS:
            list_ui.filterList(filter_string)

    def _get_selected(self):
        selected = []
        for list_ui in self.DYNAMIC_UI_ELEMENTS:
            if list_ui.isVisible():
                for index in list_ui.selectedIndexes():
                    selected.append(list_ui.model().itemFromIndex(index).ASSET_ENTRY)
        return selected

    def open_source_directory_pushed(self):
        selected_assets = self._get_selected()
        selection = pm.selected()
        if not selected_assets and not selection:
            logger.error('Select an asset or an export group to preview the source directory')
            return

        asset_entry = list_utils.get_first_in_list(selected_assets)
        if not asset_entry and selection:
            asset_entry = helios_utils.get_asset_from_group(selection[0])

        if asset_entry:
            fileio.touch_path(asset_entry.model_path)
            fileio.explore_to_path(asset_entry.model_path)

    def remove_entry_pushed(self):
        selected_assets = self._get_selected()
        if not selected_assets:
            logger.error('Something needs to be selected to be removed.')
            return

        asset_names = []
        for asset_entry in selected_assets:
            asset_names.append(asset_entry.asset_name)

        msg_str = '\n'.join(['Are you sure you wish to remove:'] + asset_names)
        result = maya_dialogs.question_prompt('Confirm Delete', msg_str)
        if result != 'Yes':
            logger.debug('Op cancelled by user')
            return

        asset_registry = assetlist.get_registry()
        for asset_entry in selected_assets:
            if 'right' in asset_entry.asset_subtype:
                # mirrored assets are nested with their pair. And only one side will be shown in the import lists.
                for local_asset in asset_entry.local_asset_list:
                    asset_registry.remove_entry(local_asset.asset_id if isinstance(local_asset, assetlist.Asset) else local_asset)
            asset_registry.remove_entry(asset_entry.asset_id)

        if asset_registry.DIRTY:
            #cl_num = sourcecontrol.p4_create_cl('Maya - Helios: Delete entry')
            #sourcecontrol.checkout(cl_num, assetlist.REGISTRY_FILE_PATH)
            asset_registry.commit()

            self.initialize_lists()


    def import_button_pressed(self):
        selected_assets = self._get_selected()
        if not selected_assets:
            logger.error('Make a selection to continue')
            return

        simple_materials = self.ui.performance_materials_checkBox.isChecked()
        with_skinning = self.ui.with_skinning_checkBox.isChecked()
        to_selected = self.ui.to_selected_checkBox.isChecked()

        root_joint_dict = {}
        if with_skinning and to_selected:
            selection = pm.selected()
            found_roots = []
            for node in selection:
                if isinstance(node, pm.nt.Joint):
                    root_joint = dag_utils.get_absolute_parent(node)
                else:
                    root_joint = joint_utils.get_hierarchy_bind_roots(node)
                if root_joint and root_joint not in found_roots:
                    found_roots.append(root_joint)

            if not found_roots:
                found_roots = [x.node() for x in pm.ls('*.skel_path')]

            for root_joint in found_roots:
                skel_path = root_joint.getAttr('skel_path') if root_joint.hasAttr('skel_path') else None
                if skel_path:
                    root_joint_dict[skel_path] = root_joint

        for asset_entry in selected_assets:
            _, root_joint_dict = helios_utils.import_asset(asset_entry, simple_materials, with_skinning, root_joint_dict)

    def export_button_pressed(self, export_all=False):
        if export_all:
            exportable_group_list = helios_utils.get_all_exportable_groups()
        else:
            selection = pm.selected()
            if not selection:
                logger.error('Select export groups from the outliner, or use export all, we failed to find any export groups.')
                return
            exportable_group_list = []
            for node in selection:
                for export_group in helios_utils.get_all_exportable_groups(node):
                    if export_group not in exportable_group_list:
                        exportable_group_list.append(export_group)

        if not exportable_group_list:
            logger.error('Select export groups from the outliner, or use export all, we failed to find any export groups.')
            return

        # grab latest on the registry before we export.
        #sourcecontrol.sync_files(assetlist.REGISTRY_FILE_PATH)

        save_source = self.ui.save_source_ma_checkBox.isChecked()
        update_skn = self.ui.update_skn_checkBox.isChecked()
        update_thumbnail = self.ui.update_thumbnail_checkBox.isChecked()

        exported_file_list = helios_utils.export_asset(exportable_group_list, update_skn=update_skn, save_source=save_source, update_thumbnail=update_thumbnail)

        # Source control stuff.
        #cl_description = 'Maya - Helios Export'
        #cl_num = sourcecontrol.p4_create_cl(cl_description)
        #sourcecontrol.checkout(cl_num, exported_file_list, False)

        self.initialize_lists()
