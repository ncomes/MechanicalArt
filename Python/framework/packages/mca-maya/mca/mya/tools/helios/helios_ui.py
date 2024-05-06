#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Helios main UI.
"""

# System global imports
import os
import random
# PySide2 imports
from PySide2.QtWidgets import QFileDialog
# software specific imports
import pymel.all as pm
# mca python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.paths import paths, path_utils
from mca.common.pyqt import messages
from mca.common.utils import lists, fileio
from mca.common.modifiers import decorators
from mca.common.tools.dcctracking import dcc_tracking

from mca.mya.tools.helios import helios_registry, helios_utils
from mca.mya.utils import dag as dag_utils
from mca.mya.rigging import skel_utils
from mca.mya.rigging.flags import frag_flag
from mca.mya.pyqt import mayawindows

logger = log.MCA_LOGGER


WIZARD_LIST = ['Albus', 'Bigby', 'Strange', 'Elminster', 'Gandalf', 'Glinda', 'Howl', 'Jareth', 'Merlin', 'Frank',
               'Mordenkainen', 'Puck', 'Raistlin', 'Rasputin', 'Ravenna', 'Sauron', 'Tim', 'Vecna', 'Vivi', 'Zatanna']

WIZARD = None


CURRENT_RELEASE_LIST = os.path.join(paths.get_asset_list_path(), 'release_list.yaml')
HELIOS_OPTION_VARS = helios_utils.HELIOS_OPTION_VARS


class Helios(mayawindows.MCAMayaWindow):
    VERSION = '1.0.4'
    
    APPAREL_SLOTS = ['head', 'top', 'legs', 'shoes', 'backpack']

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'heliosUI.ui')
        super().__init__(title='Helios',
                            ui_path=ui_path,
                            version=Helios.VERSION)

        hardware_globals_node = lists.get_first_in_list(pm.ls(type=pm.nt.HardwareRenderingGlobals))
        hardware_globals_node.transparencyAlgorithm.set(3)

        self.setup_signals()

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def setup_signals(self):
        """
        Connect all buttons and initialize all lists.

        """
        self._initialize_lists()

        # restore UI
        self.ui.performance_materials_checkBox.setChecked(HELIOS_OPTION_VARS.MCAPerfMaterials)

        self.ui.with_skinning_checkBox.setChecked(HELIOS_OPTION_VARS.MCAWithSkinning)
        self.ui.to_selected_checkBox.setChecked(HELIOS_OPTION_VARS.MCAToSelected)

        self.ui.save_source_ma_checkBox.setChecked(HELIOS_OPTION_VARS.MCAExportSourceMa)
        self.ui.update_skn_checkBox.setChecked(HELIOS_OPTION_VARS.MCAExportSkn)

        tab_order = HELIOS_OPTION_VARS.MCALastOpenTab
        try:
            # Don't do a blind "if" test, the value can be 0 which gets you got.
            if tab_order != []:
                self.ui.import_tabWidget.setCurrentIndex(int(tab_order[0]))
                if int(tab_order[0]) == 1:
                    self.ui.apparel_tabWidget.setCurrentIndex(int(tab_order[-1]))
        except:
            logger.warning('There was an error recovering the last open tab, resetting to default open.')
            HELIOS_OPTION_VARS.MCALastOpenTab = '0'
            self.ui.import_tabWidget.setCurrentIndex(0)

        self.ui.filter_lineEdit.textChanged.connect(self._filter_lists)
        self.ui.remove_entry_pushButton.clicked.connect(self.remove_entry_clicked)
        self.ui.import_pushButton.clicked.connect(self.import_selected_clicked)

        self.ui.open_source_pushButton.clicked.connect(self.open_source_clicked)
        self.ui.wizard_pushButton.clicked.connect(summon_the_wizard)

        self.ui.export_pushButton.clicked.connect(self.export_selected_clicked)
        
    # =================================================================================================================
    # Initialization
    # =================================================================================================================

    def _initialize_lists(self):
        """
        Refresh each of Helios' import lists.

        """
        # $TODO FSchorsch there might be a better way to register all of these lists automatically from the archetype registry
        self.APPAREL_PARTS_DICT = {}
        self.APPAREL_COLLECTIONS_DICT = {}

        self.CHARACTER_DICT = {}

        self.WEAPONS_DICT = {}

        self.PROPS_DICT = {}

        self.REFERENCE_DICT = {}

        asset_registry = assetlist.AssetListRegistry()
        asset_registry.reload()
        for asset_id, mca_asset in asset_registry.ASSET_ID_DICT.items():
            if mca_asset.asset_type == 'collection':
                self.APPAREL_COLLECTIONS_DICT[mca_asset.asset_name] = mca_asset
            elif any(x in mca_asset.asset_type.lower() for x in self.APPAREL_SLOTS):
                self.APPAREL_PARTS_DICT[mca_asset.asset_name] = mca_asset
            elif mca_asset.asset_subtype.lower() in ['enemies', 'npc', 'player', 'attachment']:
                self.CHARACTER_DICT[mca_asset.asset_name] = mca_asset
            elif mca_asset.asset_subtype.lower() == 'weapon':
                self.WEAPONS_DICT[mca_asset.asset_name] = mca_asset
            elif mca_asset.asset_subtype.lower() == 'props':
                self.PROPS_DICT[mca_asset.asset_name] = mca_asset
            elif mca_asset.asset_subtype.lower() == 'reference':
                self.REFERENCE_DICT[mca_asset.asset_name] = mca_asset

        self._filter_lists()

    def _filter_lists(self):
        """
        For each import list filter them based on whatever is put in the filter line edit.
        This includes multiple lookups based on white space and negative lookups preceded by a hyphen.

        :return:
        """

        filter_string_raw = self.ui.filter_lineEdit.text()
        required_str_list = []
        excluded_str_list = []
        for filter_string in filter_string_raw.split(' '):
            if filter_string.startswith('-'):
                if filter_string != '-':
                    excluded_str_list.append(filter_string[1:].lower())
            else:
                required_str_list.append(filter_string.lower())

        logger.debug(f'required: {required_str_list} \nexcluded: {excluded_str_list}')

        ui_dict_pairs = [(self.APPAREL_PARTS_DICT, self.ui.apparel_parts_listWidget),
                         (self.APPAREL_COLLECTIONS_DICT, self.ui.apparel_collections_listWidget),
                         (self.CHARACTER_DICT, self.ui.characters_listWidget),
                         (self.WEAPONS_DICT, self.ui.weapons_listWidget),
                         (self.PROPS_DICT, self.ui.props_listWidget),
                         (self.REFERENCE_DICT, self.ui.reference_listWidget)]

        for asset_dict, ui_element in ui_dict_pairs:
            ui_element.clear()
            for index, asset_name in enumerate(sorted(asset_dict)):
                if required_str_list and not all(x in asset_name.lower() for x in required_str_list):
                    # if we don't find all our expected filters in the name
                    continue

                if excluded_str_list and any(x in asset_name.lower() for x in excluded_str_list):
                    # if we find any of our exclusions in the name
                    continue

                ui_element.addItem(asset_name)

    def _find_active_list(self):
        """
        This looks up which tab is active and saves it allowing the user to quickly return when reopening Helios.

        """

        active_list = None
        asset_dict = {}
        active_tab = ''
        if self.ui.import_tabWidget.currentIndex() == 0:
            # Characters
            active_list = self.ui.characters_listWidget
            asset_dict = self.CHARACTER_DICT
            active_tab += '0'
        elif self.ui.import_tabWidget.currentIndex() == 1:
            # Apparel
            active_tab += '1'
            if self.ui.apparel_tabWidget.currentIndex() == 0:
                active_list = self.ui.apparel_collections_listWidget
                asset_dict = self.APPAREL_COLLECTIONS_DICT
                active_tab += '0'
            elif self.ui.apparel_tabWidget.currentIndex() == 1:
                active_list = self.ui.apparel_parts_listWidget
                asset_dict = self.APPAREL_PARTS_DICT
                active_tab += '1'
        elif self.ui.import_tabWidget.currentIndex() == 2:
            # Weapons
            active_tab += '2'
            active_list = self.ui.weapons_listWidget
            asset_dict = self.WEAPONS_DICT
        elif self.ui.import_tabWidget.currentIndex() == 3:
            # Props
            active_tab += '3'
            active_list = self.ui.props_listWidget
            asset_dict = self.PROPS_DICT
        elif self.ui.import_tabWidget.currentIndex() == 4:
            # References
            active_tab += '4'
            active_list = self.ui.reference_listWidget
            asset_dict = self.REFERENCE_DICT

        HELIOS_OPTION_VARS.MCALastOpenTab = active_tab
        return active_list, asset_dict

    @decorators.track_fnc
    def remove_entry_clicked(self):
        """
        Remove the selected entry from an import list.

        """

        active_list, asset_dict = self._find_active_list()
        if not active_list:
            return

        selected_items = active_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            asset_name = item.text()
            mca_asset = asset_dict[asset_name]

            assetlist.AssetListRegistry().remove_entry(mca_asset.asset_id)

        assetlist.AssetListRegistry().commit()
        assetlist.AssetListRegistry().reload()

        self._initialize_lists()

    def import_selected_clicked(self):
        """
        From the selected assets import them into the current scene.

        """

        active_list, asset_dict = self._find_active_list()
        if not active_list:
            return

        # Save UI settings
        HELIOS_OPTION_VARS.MCAPerfMaterials = self.ui.performance_materials_checkBox.isChecked()

        HELIOS_OPTION_VARS.MCAWithSkinning = self.ui.update_skn_checkBox.isChecked()
        HELIOS_OPTION_VARS.MCAToSelected = self.ui.to_selected_checkBox.isChecked()
        HELIOS_OPTION_VARS.MCAWithFullSkeleton = self.ui.with_full_skeleton_checkBox.isChecked()

        import_list = []
        for item in active_list.selectedItems():
            asset_name = item.text()
            import_list.append(asset_dict[asset_name])

        bind_dict = {}
        if self.ui.to_selected_checkBox.isChecked():
            selection = pm.selected()
            selected_joints = [x for x in pm.ls(selection, type=pm.nt.Joint) if not frag_flag.is_flag_node(x)]
            bind_root_list = []
            for joint_node in selected_joints:
                bind_root = dag_utils.get_absolute_parent(joint_node, node_type=pm.nt.Joint)
                if bind_root not in bind_root_list:
                    bind_root_list.append(bind_root)
                # need markup on root joint for where skel came from
                continue

            if not selection:
                bind_root_list = pm.ls('|*', type=pm.nt.Joint)
                # need markup on root joint for where skel came from

            if len(selection) == 1:
                bind_dict['default'] = selection[0]
            elif len(bind_root_list) == 1:
                bind_dict['default'] = bind_root_list[0]
            else:
                for bind_root in bind_root_list:
                    # make a bind dict for asset_id lookups.
                    if bind_root.hasAttr('asset_id'):
                        bind_dict[bind_root.getAttr('asset_id')] = bind_root

        for mca_asset in import_list:
            _, skel_root_dict = helios_utils.import_helios_asset(mca_asset,
                                                                 with_skinning=self.ui.with_skinning_checkBox.isChecked(),
                                                                 skel_root_dict=bind_dict)
            if self.ui.with_full_skeleton_checkBox.isChecked():
                bind_root = skel_root_dict.get(mca_asset.skel_path)
                if not bind_root:
                    bind_root = skel_root_dict.get('default')
                if bind_root:
                    skel_path = mca_asset.skel_path
                    skel_utils.import_merge_skeleton(skel_path, bind_root)
            # dcc data
            dcc_tracking.ddc_tool_entry_thead(fn=self.import_selected_clicked,
                                              asset_id=mca_asset.asset_id,
                                              asset_name=mca_asset.asset_name,
                                              checkboxes=[self.ui.update_skn_checkBox,
                                                          self.ui.to_selected_checkBox,
                                                          self.ui.with_full_skeleton_checkBox,
                                                          self.ui.performance_materials_checkBox])

    def open_source_clicked(self):
        """
        Open the meshes folder for a selected asset.

        """

        selection = pm.selected()
        if not selection:
            messages.info_message('Selection Error', 'Please select an organization group.', icon='error')
            return

        organization_grp = selection[0]
        if organization_grp.hasAttr('helios_path'):
            fileio.explore_to_path(path_utils.to_full_path(organization_grp.getAttr('helios_path')))

    def export_selected_clicked(self):
        """
        For each selected asset export their SK/SM and optionally save their source file.

        """

        selection = pm.selected()

        if not selection:
            messages.info_message('Failed to find.', 'Please select an organization group.')
            return

        # Save UI settings
        HELIOS_OPTION_VARS.MCAExportSourceMa = self.ui.save_source_ma_checkBox.isChecked()
        HELIOS_OPTION_VARS.MCAExportSkn = self.ui.update_skn_checkBox.isChecked()

        helios_export_group_list = [x for x in selection if x.hasAttr('helios')]

        helios_export_list = []
        for export_group in helios_export_group_list:
            # don't allow any children of a selected export group, use the parent only.
            if not any(export_group in x.listRelatives(ad=True, type=pm.nt.Transform) for x in helios_export_group_list):
                helios_export_list.append(export_group)

        for export_group in helios_export_list:
            helios_utils.export_helios_asset(export_group,
                                             update_skn=self.ui.update_skn_checkBox.isChecked(),
                                             save_source=self.ui.save_source_ma_checkBox.isChecked())
            
            # dcc data
            checkboxes = [self.ui.update_skn_checkBox, self.ui.save_source_ma_checkBox]
            dcc_tracking.ddc_tool_entry_thead(fn=self.export_selected_clicked,
                                              asset_id=export_group.helios_asset_id.get(),
                                              asset_name=export_group.helios_name.get(),
                                              checkboxes=checkboxes)

        self._initialize_lists()



@decorators.track_fnc
def summon_the_wizard():
    global WIZARD
    try:
        WIZARD.close()
    except:
        pass
    WIZARD = Wizard()
    WIZARD.ui.show()


class Wizard(mayawindows.MCAMayaWindow):
    
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'WizardUI.ui')
        super().__init__(title='HeliosWizard',
                            ui_path=ui_path,
                            version=Helios.VERSION)

        self.setWindowTitle(random.choice(WIZARD_LIST))

        self.setup_signals()
        self._initialize_lists()
        self.preview_export_path()
        self.ui.create_now_checkBox.setChecked(HELIOS_OPTION_VARS.MCACreateFolders)
    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def setup_signals(self):
        """
        Connect all buttons to their fncs.

        """

        self.ui.asset_select_comboBox.currentIndexChanged.connect(self.preview_export_path)
        self.ui.name_lineEdit.textChanged.connect(self.preview_export_path)

        self.ui.organize_pushButton.clicked.connect(self.organize_scene)

        self.ui.export_dir_browse_pushButton.clicked.connect(self.browse_export_directory)

    def _initialize_lists(self):
        """
        Update the drop downs in the Wizard from the archetype registry.

        """
        helios_archetype_registry = helios_registry.HeliosArchetypeRegistry(force=True)
        archetype_list = list(sorted(helios_archetype_registry.NAME_REGISTRY.keys()))
        self.ui.asset_select_comboBox.insertItems(0, archetype_list)
        previous_asset = HELIOS_OPTION_VARS.MCALastAssetType
        if previous_asset in archetype_list:
            self.ui.asset_select_comboBox.setCurrentIndex(archetype_list.index(previous_asset))
    
    def _format_name(self, string_name):
        """
        Conform our name to our naming conventions.
        
        :param str string_name: The original string name.
        :return: The formatted string name.
        :rtype: str
        """

        string_name = string_name.replace(' ', '_')
        split_name = string_name.split('_')
        return '_'.join([x[0].upper() + x[1:] if x else x for x in split_name])

    def browse_export_directory(self):
        """
        Find an override directory and use that instead of the automatically generated field.

        """

        helios_archetype_registry = helios_registry.HeliosArchetypeRegistry()
        selected_archetype = self.ui.asset_select_comboBox.currentText()
        helios_archetype = helios_archetype_registry.NAME_REGISTRY.get(selected_archetype, None)

        start_path = path_utils.to_full_path(helios_archetype.base_dir)

        found_path = QFileDialog.getExistingDirectory(None, 'Select Directory', start_path)
        if not found_path:
            return

        self.ui.export_dir_lineEdit.setText(path_utils.to_relative_path(found_path))
    
    def preview_export_path(self):
        """
        This updates the export preview path whenever one of the re-requisites is updated.

        """

        # $HACK FSchorsch should really come up with a better way to identify this
        #print(self.ui.asset_select_comboBox.currentText())
        #print(self.ui.release_comboBox.currentText())
        #print(self.ui.name_lineEdit.text())

        helios_archetype_registry = helios_registry.HeliosArchetypeRegistry()
        selected_archetype = self.ui.asset_select_comboBox.currentText()
        helios_archetype = helios_archetype_registry.NAME_REGISTRY.get(selected_archetype, None)

        if not helios_archetype:
            return

        export_path = ''
        if helios_archetype:
            export_path += helios_archetype.base_dir

        asset_name = self._format_name(self.ui.name_lineEdit.text())
        if asset_name:
            export_path = os.path.join(export_path, asset_name)
        else:
            self.ui.export_dir_lineEdit.setText('')
            self.ui.export_dir_lineEdit.setPlaceholderText('A name must be picked for this asset.')
            logger.warning('A name must be picked for this asset.')
            return
        self.ui.export_dir_lineEdit.setText(export_path)
    
    @decorators.track_fnc
    def organize_scene(self):
        """
        From the selected archetype and name generate the new Helios Asset build structure for the scene
        and optionally build out the working folder structure.

        """

        asset_name = self._format_name(self.ui.name_lineEdit.text())
        if not asset_name:
            logger.warning(f'{asset_name} is not a valid asset name')
            return

        original_path = self.ui.export_dir_lineEdit.text()
        if not original_path:
            logger.warning(f'{original_path} is not a valid export directory')
            return

        # Save UI settings
        HELIOS_OPTION_VARS.MCALastAssetType = self.ui.asset_select_comboBox.currentText()
        HELIOS_OPTION_VARS.MCACreateFolders = self.ui.create_now_checkBox.isChecked()

        helios_archetype_registry = helios_registry.HeliosArchetypeRegistry()
        selected_archetype = self.ui.asset_select_comboBox.currentText()
        helios_archetype = helios_archetype_registry.NAME_REGISTRY.get(selected_archetype, None)

        base_dir, dir_name = os.path.split(original_path)

        if dir_name == asset_name:
            modified_base_dir = False
        else:
            modified_base_dir = True
            base_dir = original_path
        helios_utils.organize_scene_from_archetype(helios_archetype, asset_name, base_dir, modified_base_dir, self.ui.create_now_checkBox.isChecked())

