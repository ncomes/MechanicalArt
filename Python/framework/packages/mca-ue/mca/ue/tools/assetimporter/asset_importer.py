# -*- coding: utf-8 -*-

"""
UI to import Textures, Material Instance Constants and Static Meshes
"""

# mca python imports
import os
# PySide2 imports
import unreal
# software specific imports
# mca python imports
from mca.common import log
from mca.common.pyqt import common_windows, messages, file_dialogs
from mca.common.pyqt.qt_utils import listwidget_utils
from mca.common.textio import yamlio
from mca.common.modifiers import decorators

from mca.ue.tools.assetimporter import local_prefs
from mca.ue.assetlist import ue_assetlist
from mca.ue.utils import asset_import, asset_utils, materials
from mca.ue.texturetypes import texture_2d
from mca.ue.paths import ue_path_utils, ue_paths
from mca.ue.startup.configs import ue_consts
from mca.ue.assettypes import py_material_instance, parent_materials, py_staticmesh

logger = log.MCA_LOGGER


class MATUnrealAssetImporter(common_windows.MCAMainWindow):
    """
    UI for importing Textures and creating Material Instance Constants.
    """

    VERSION = '1.0.0'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'asset_importer.ui')
        super().__init__(title='Asset Importer',
                         ui_path=ui_path,
                         version=MATUnrealAssetImporter.VERSION,
                         style='incrypt',
                         parent=parent)
        # Material Dict
        self.mat_dict = {}

        # Get the local preferences
        self.prefs = local_prefs.AssetImportPreferences()
        self.ue_asset_list = ue_assetlist.UnrealAssetListToolBox()
        # Sets the UI properties - These are the user's settings
        self.set_ui_properties()

        ############################################
        # Signals
        ############################################
        self.ui.master_mca_comboBox.currentIndexChanged.connect(self.hide_show_checkboxes)
        self.ui.import_texture_pushButton.clicked.connect(self.import_from_list)
        self.ui.text_reimp_pushButton.clicked.connect(self.import_selected)
        self.ui.text_dir_pushButton.clicked.connect(self.import_textures_from_dir)
        self.ui.mat_cb_pushButton.clicked.connect(self.load_materials_from_content_browser_clicked)
        self.ui.mat_al_pushButton.clicked.connect(self.load_materials_from_asset_list_clicked)
        self.ui.mat_listWidget.itemSelectionChanged.connect(self.change_master_material)
        self.ui.create_mca_pushButton.clicked.connect(self.create_mca_inst_sel_clicked)
        self.ui.create_mca_all_pushButton.clicked.connect(self.create_mca_inst_all_clicked)
        self.ui.static_mesh_al_pushButton.clicked.connect(self.import_sm_asset_list_clicked)
        self.ui.static_mesh_dir_pushButton.clicked.connect(self.import_sm_asset_dir_clicked)
        self.ui.set_materials_pushButton.clicked.connect(self.sm_set_materials_clicked)

    ############################################
    # Slots
    ############################################
    def get_asset_from_asset_list(self):
        """
        Returns the asset entry from the asset list.  This is using the name in the of the asset from
        the combobox and looking up the asset from the asset list using the name.

        :return: Returns the asset entry from the asset list.
        :rtype: assetlist.MATAsset
        """

        asset_data = self.ue_asset_list.asset_data
        if not asset_data:
            return
        return asset_data

    #### Textures ############
    @decorators.track_fnc
    def refresh_asset_list(self):
        """
        Refreshes the asset list and updates the UI
        This will refresh the 'type' and 'asset name' for the QComboboxes
        Then it will repopulate the QComboboxes with all the asset information.
        """

        self.ue_asset_list.reload_asset_list()
        self.set_ui_properties()

    @decorators.track_fnc
    def import_from_list(self):
        """
        Imports all the Textures from the art depot in to the game directory using the asset list comboboxes.
        """

        # Dialog prompt
        result = messages.question_message('Asset Importer', 'Import selected asset?')
        if result != 'Yes':
            return
        # Gets the asset data from the asset name combobox
        asset_data = self.get_asset_from_asset_list()
        if not asset_data:
            return

        # Gets the Art side textures path
        art_textures_path = asset_data.textures_path
        # Look for vaild textures
        texture_list = [os.path.join(art_textures_path, x) for x in os.listdir(art_textures_path)
                if x.endswith('.tga') or x.endswith('.jpg') or x.endswith('.png')]

        # Get the game side textures path
        game_textures_path = asset_data.game_textures_path
        imported_textures = []
        # import each Texture and set its default properties.
        for texture in texture_list:
            self.import_texture(texture, game_textures_path, asset_data.asset_name)
            imported_textures.append(texture)
        if imported_textures:
            self.load_materials_from_asset_list_clicked()

    @decorators.track_fnc
    def import_selected(self):
        """
        Re-imports all selected textures in the Content Browser.
        """

        # Dialog prompt
        result = messages.question_message('Asset Importer', 'Re-Import selected asset?')
        if result != 'Yes':
            return

        selection = asset_utils.selected()
        if not selection:
            messages.info_message('Asset Importer', 'Please select either an Albedo, Normal Map, ORME, or SSTD')
            return

        for texture in selection:
            if not isinstance(texture, texture_2d.PyTexture2D):
                logger.warning(f'{texture.get_name()} asset is not a supported texture by the asset importer')
                continue

            art_textures_path = texture.original_import_path
            game_textures_path = texture.original_import_path
            self.import_texture(art_textures_path, game_textures_path, texture.name, replace_existing=True)

    @decorators.track_fnc
    def import_textures_from_dir(self):
        """
        Imports selected textures from the art depot in to the game directory using a Dialog prompt.
        """

        # Open Dialog prompt
        results = file_dialogs.open_file_dialog(filters="Images (*.tga *.png *.jpg);;All Files *.*", parent=self)
        if not results:
            return
        # get the current Browser path
        game_textures_path = ue_path_utils.get_current_content_browser_path()

        # Go through the selected textures and make sure they are supported textures.
        for texture in results:
            texture_type = texture.split('_')[-1].split('.')[0]
            if texture_type.lower() not in ue_consts.TEXTURE_TYPES:
                texture_name = os.path.basename(texture)
                logger.warning(f'{texture_name} asset is not a supported texture by the asset importer')
                continue
            # If the texture is valid, import it.
            self.import_texture(texture, game_textures_path, os.path.basename(texture)[0].split('.')[0])

    def import_texture(self, texture, game_textures_path, asset_name, replace_existing=False):
        """
        Imports a single texture and sets its default properties.

        :param str texture: Full path to the texture.
        :param str game_textures_path: Path to the game texture's directory.  This is where it will be imported.
        :param str asset_name: final name of the game texture.
        :param bool replace_existing: If true, it will force replace the existing texture.
        :return: Returns the imported game texture.
        :rtype: txture_2d.PyTexture2D
        """

        # Update the ui preferences
        self.update_preferences()
        # import the textures
        options = asset_import.texture_2d_import_options()
        uasset = asset_import.import_asset(filename=texture,
                                          game_path=game_textures_path,
                                          asset_name=asset_name,
                                          import_options=options,
                                          replace_existing=replace_existing,
                                          save=True)
        uasset = asset_utils.PyNode(uasset)
        # Only set the properties and save if the asset is valid.
        if isinstance(uasset, texture_2d.PyTexture2D):
            uasset.set_editor_attributes()
            asset_utils.save_asset(uasset)
        return uasset

    ############## Materials ##############
    def populate_materials(self):
        """
        Populates the parent materials in the combobox.
        """

        masterial_list = py_material_instance.ParentMaterialMapping().get_parent_material_names()

        self.ui.master_mca_comboBox.clear()
        self.ui.master_mca_comboBox.addItems(masterial_list)
        if self.prefs.master_material:
            self.ui.master_mca_comboBox.setCurrentText(self.prefs.master_material)

    @decorators.track_fnc
    def load_materials_from_content_browser_clicked(self):
        """
        When button is clicked, load the materials from the content browser and add them to the list widget.
        """

        self.ui.mat_listWidget.clear()
        self.update_preferences()
        material_names = self.get_material_names_from_content_browser()
        if not material_names:
            return
        self.populate_materials_qlistwidget(material_names)

    @decorators.track_fnc
    def load_materials_from_asset_list_clicked(self):
        """
        When button is clicked, load the materials from the asset list and add them to the list widget.
        """

        self.ui.mat_listWidget.clear()
        self.update_preferences()
        material_names = self.get_material_names_from_asset_list()
        if not material_names:
            return
        self.populate_materials_qlistwidget(material_names)

    @decorators.track_fnc
    def create_mca_inst_sel_clicked(self):
        """
        Creates a material instance from the selected entry in the QListWidget.
        Also sets the default properties and any extra properties from the selected checkboxes in the UI.
        """

        self.update_preferences()
        # Dialog prompt
        result = messages.question_message('Create Material', 'Create the selected materials from the list?')
        if result != 'Yes':
            return
        # get the selected material from the QListWidget
        selection = listwidget_utils.get_qlist_widget_selected_items(self.ui.mat_listWidget)
        if not selection:
            return
        material_name = str(selection[0])
        # Get the parent Material to set on the martial instance
        parent_material_name = self.ui.master_mca_comboBox.currentText()
        parent_material = materials.get_material(parent_material_name)
        # get the material instance class that specifically is used for the material instance with that parent material.
        material_inst = py_material_instance.ParentMaterialMapping.attr(parent_material_name)

        # Get the textures associated with the material
        texture_list = self.mat_dict.get(material_name, None)
        if not texture_list:
            logger.warning('No textures found for the material instance.  '
                           'There must be textures to create the material instance.')
            return
        # get the Material Folder to set on the material instance
        texture_path = os.path.dirname(texture_list[0].path)
        material_path = ue_path_utils.convert_texture_to_material_path(texture_path)

        # Create the material instance
        material_instance = material_inst.create(name=material_name,
                                                 folder=material_path,
                                                 parent_material=parent_material,
                                                 texture_list=texture_list)
        material_instance.set_editor_properties()
        extra_properties = self.get_material_checkbox_properties()
        [material_instance.set_attr(str(x), True) for x in extra_properties]
        asset_utils.save_asset(material_instance)

    @decorators.track_fnc
    def create_mca_inst_all_clicked(self):
        """
        Creates a material instances from all the entries in the QListWidget.
        Also sets the default properties and any extra properties from the selected checkboxes in the UI.
        """

        self.update_preferences()
        # Dialog prompt
        result = messages.question_message('Create Materials', 'Create all materials from the list?')
        if result != 'Yes':
            return
        # get the selected material from the QListWidget
        items = listwidget_utils.get_qlist_widget_items(self.ui.mat_listWidget)
        if not items:
            return
        for item in items:
            material_name = str(item)
            # Get the parent Material to set on the martial instance
            # Get the textures associated with the material
            texture_list = self.mat_dict.get(material_name, None)
            if not texture_list:
                logger.warning('No textures found for the material instance.  '
                               'There must be textures to create the material instance.')
                return
            parent_material = parent_materials.get_parent_materials(texture_list)
            # get the material instance class that specifically is used for the
            # material instance with that parent material.
            material_inst = py_material_instance.ParentMaterialMapping.attr(parent_material.get_name())

            # get the Material Folder to set on the material instance
            texture_path = os.path.dirname(texture_list[0].path)
            material_path = ue_path_utils.convert_texture_to_material_path(texture_path)

            # Create the material instance
            material_instance = material_inst.create(name=material_name,
                                                     folder=material_path,
                                                     parent_material=parent_material,
                                                     texture_list=texture_list)
            material_instance.set_editor_properties()
            extra_properties = self.get_material_checkbox_properties()
            [material_instance.set_attr(str(x), True) for x in extra_properties]
            asset_utils.save_asset(material_instance)

    def get_material_checkbox_properties(self):
        """
        Returns a list of all the properties that are checked in the UI.

        :return: Returns a list of all the properties that are checked in the UI.
        :rtype: list(str)
        """

        # Get the mapping dictionary that maps the checkboxes to the checkbox properties.
        mapping = self.map_checkboxes()
        checkboxes = list(mapping.values())
        properties = list(mapping.keys())
        properties_list = []
        # Go through each checkbox and check if it is visible and checked.
        for x, checkbox in enumerate(checkboxes):
            if checkbox.isVisible() and checkbox.isChecked():
                properties_list.append(properties[x])
        return properties_list

    def change_master_material(self):
        """
        When a material is selected in the list widget, change the master material in the combobox.
        """

        selection = listwidget_utils.get_qlist_widget_selected_items(self.ui.mat_listWidget)
        if not selection:
            return
        material_name = str(selection[0])
        texture_list = self.mat_dict.get(material_name, None)
        if not texture_list:
            return
        master_material = parent_materials.get_parent_materials(texture_list)
        self.ui.master_mca_comboBox.setCurrentText(master_material.get_name())

    def verify_materials_browser_path(self):
        """
        Returns the texture path using the material path.

        :return: Returns the texture path using the material path.
        :rtype: str
        """

        content_browser_path = ue_path_utils.get_current_content_browser_path()
        path = None
        if ue_path_utils.is_game_material_path(content_browser_path):
            path = content_browser_path
        elif ue_path_utils.is_game_texture_path(content_browser_path):
            path = ue_path_utils.convert_texture_to_material_path(content_browser_path)
        return path

    def get_material_names_from_content_browser(self):
        """
        Returns the material names using the texture path

        :return: Returns the material names using the texture path
        :rtype: list(str)
        """

        path = self.verify_materials_browser_path()
        if not path:
            # Dialog prompt
            msg = 'Please make sure you are in the "Textures" or "Materials" folder in the content browser.'
            messages.info_message('Get Material Names', msg)
            logger.warning(msg)
            return
        material_names = self.get_material_names(path)
        return material_names

    def get_material_names_from_asset_list(self):
        """
        Return the material names using the textures directory and the asset comboboxes.

        :return: Return the material names using the textures directory and the asset comboboxes.
        :rtype: list(str)
        """

        asset_data = self.get_asset_from_asset_list()
        materials_path = asset_data.game_material_path
        materials_path = ue_path_utils.convert_to_game_path(materials_path)
        material_names = self.get_material_names(materials_path)
        return material_names

    def get_material_names(self, material_folder_path):
        """
        Return the material names using the textures directory.

        :param str material_folder_path: Game Directory for the Material Instances.
        :return: Return the material names using the textures directory.
        :rtype: list(str)
        """

        material_dict = py_material_instance.create_mic_names(material_folder_path)
        if not material_dict:
            logger.warning('No Textures or Materials folder found in the content browser')
            return
        self.mat_dict = material_dict
        material_names = list(material_dict.keys())
        return material_names

    def populate_materials_qlistwidget(self, material_list):
        """
        Populates the Material List Widget.

        :param list(str) material_list: List of string names of materials.
        """

        self.ui.mat_listWidget.addItems(material_list)
        self.ui.mat_listWidget.setCurrentRow(0)

    ################################################################
    # Static Mesh
    ################################################################
    def import_sm_asset_list_clicked(self):
        """
         Imports an SM from the selected asset in the combobox.
        """

        # Dialog prompt
        result = messages.question_message('Asset Importer', 'Import selected SM asset from the asset list?')
        if result != 'Yes':
            return
        # Gets the asset data from the asset name combobox
        asset_data = self.get_asset_from_asset_list()
        if not asset_data:
            return

        # Get the SM Art and Game paths
        art_sm = asset_data.sm_path
        path_manager = ue_path_utils.UEPathManager(art_sm)
        game_sm = path_manager.convert_art_path_to_game_path(remove_filename=True)
        asset_name = os.path.basename(art_sm).split('.')[0]

        self.import_sm(art_sm, game_sm, asset_name, replace_existing=True)

    def import_sm_asset_dir_clicked(self):
        """
        Imports an SM from the selected asset in the directory dialog.
        """

        # Open Dialog prompt
        results = file_dialogs.open_file_dialog(filters="All Files *.*", parent=self)
        if not results:
            return
        # get the current Browser path
        game_path = ue_path_utils.get_current_content_browser_path()
        sm = results[0]
        # Go through the selected textures and make sure they are supported textures.
        # If the texture is valid, import it.
        self.import_sm(sm_full_name=sm,
                       game_path=game_path,
                       asset_name=os.path.basename(sm).split('.')[0],
                       replace_existing=True)

    def import_sm(self, sm_full_name, game_path, asset_name, replace_existing=False):
        """
        Imports a single SM and sets its default properties.

        :param str sm_full_name: Full path to the asset.
        :param str game_path: Path to the game asset directory.  This is where it will be imported.
        :param str asset_name: final name of the game asset.
        :param bool replace_existing: If true, it will force replace the existing asset.
        :return: Returns the imported game SM.
        :rtype: py_staticmesh.PyStaticMesh
        """

        # Update the ui preferences
        self.update_preferences()
        # import the textures
        options = py_staticmesh.static_mesh_import_options()
        uasset = asset_import.import_asset(filename=sm_full_name,
                                          game_path=game_path,
                                          asset_name=asset_name,
                                          import_options=options,
                                          replace_existing=replace_existing,
                                          save=True)
        uasset = asset_utils.PyNode(uasset)
        # Only set the properties and save if the asset is valid.
        if isinstance(uasset, py_staticmesh.PyStaticMesh):
            uasset.set_materials()
            asset_utils.save_asset(uasset)
        return uasset

    def sm_set_materials_clicked(self):
        """
        Using the materials in the material folder to set on the static mesh.
        """

        self.update_preferences()
        # Dialog prompt
        result = messages.question_message('Set Materials', 'Set materials on selected Static Mesh?')
        if result != 'Yes':
            return
        assets = asset_utils.get_selected_assets()
        if not assets:
            return
        asset = assets[0]
        if not isinstance(asset, unreal.StaticMesh):
            return
        asset = asset_utils.PyNode(asset)
        asset.set_materials()
        asset_utils.save_asset(asset)


    ################################################################
    def map_checkboxes(self):
        """
        Returns a mapping connecting the checkboxes to their corresponding properties.

        :return: Returns a mapping connecting the checkboxes to their corresponding properties.
        :rtype: dict
        """

        mapping = {}
        mapping.update({'Use Subsurface Profile': self.ui.sub_sur_1_checkBox})
        mapping.update({'Use Subsurface Distance Fading': self.ui.sub_sur_2_checkBox})
        mapping.update({'Use Emissive': self.ui.emissive_checkBox})
        mapping.update({'Use Bent Normals': self.ui.bn_checkBox})
        mapping.update({'Use Filigree': self.ui.fillgri_checkBox})
        mapping.update({'Use Detail Texture': self.ui.detail_texture_checkBox})
        mapping.update({'Use Iridescent': self.ui.iridescent_checkBox})
        mapping.update({'Fuzzy Clothing': self.ui.fuzzy_cloth_checkBox})
        mapping.update({'Use Carbon Fiber': self.ui.cf_checkBox})
        mapping.update({'Use Simple Decals': self.ui.decal_checkBox})
        return mapping

    def property_mapping(self):
        """
        Maps the property names and exported properties in the asset imported yaml file.

        :return: Returns a dictionary of property names and exported properties in the asset imported yaml file.
        :rtype: dict
        """

        mapping = {}
        mapping.update({'Use Subsurface Profile': 'subsurface_profile'})
        mapping.update({'Use Subsurface Distance Fading': 'use_subsurface_distance_fading'})
        mapping.update({'Use Emissive': 'use_emissive'})
        mapping.update({'Use Bent Normals':'use_bent_normals'})
        mapping.update({'Use Filigree': 'use_filigree'})
        mapping.update({'Use Detail Texture': 'use_detail_texture'})
        mapping.update({'Use Iridescent': 'use_iridescent'})
        mapping.update({'Fuzzy Clothing': 'use_fuzzy_clothing'})
        mapping.update({'Use Carbon Fiber': 'use_carbon_fiber'})
        mapping.update({'Use Simple Decals': 'use_simple_decals'})
        return mapping

    def get_material_properties(self):
        """
        Returns the material properties' dictionary.

        :return: Returns the material properties' dictionary.
        :rtype: dict
        """

        # Get the parent material name
        parent_material = self.ui.master_mca_comboBox.currentText()
        # Get the local properties path for the material instance with the above parent material,
        # in the local document's folder.
        local_path = ue_paths.get_local_tool_prefs_folder(py_material_instance.PROPERTIES_FOLDER)
        full_path = os.path.join(local_path, parent_material + py_material_instance.MATERIAL_PROPERTIES_EXT)
        # If the local properties path does not exist, attempt to copy the file from Common\Tools\Unreal.
        if not os.path.exists(full_path):
            common_path = ue_paths.get_tool_prefs_folder(py_material_instance.PROPERTIES_FOLDER)
            common_full_path = os.path.join(common_path, parent_material + py_material_instance.MATERIAL_PROPERTIES_EXT)
            logger.warning(f'Could not find {full_path}, Attempting to use the common default properties')
            if os.path.exists(common_full_path):
                common_dict = yamlio.read_yaml_file(common_full_path)
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
                yamlio.write_to_yaml_file(common_dict, full_path)
                return common_dict

        if not os.path.exists(full_path):
            logger.warning(f'Could not find {full_path}')
            return

        return yamlio.read_yaml_file(full_path)

    def hide_show_checkboxes(self):
        """
        Either hides or shows the checkboxes depending on parent material.
        """

        self.update_preferences()
        settings = self.get_material_properties()
        properties = self.property_mapping()

        mapping = self.map_checkboxes()
        checkboxes = list(mapping.values())
        [x.setVisible(False) for x in checkboxes]

        for property_name, setting in settings['options'].items():
            checkbox = mapping.get(property_name, None)
            if not checkbox:
                continue
            prop_name = properties.get(property_name, None)
            value = self.prefs.data.get(prop_name, None)
            checkbox.setVisible(True)
            if value:
                checkbox.setChecked(value)

    def blockSignals(self, block=True):
        """
        Blocks signals
        :param bool block: True to block signals, False to unblock
        """

        self.ui.master_mca_comboBox.blockSignals(block)

    def set_ui_properties(self, block=True):
        """
        Sets the UI properties
        :param bool block: True to block signals, False to unblock
        """

        self.blockSignals(block=block)
        self.set_checkboxes()
        self.populate_materials()
        self.hide_show_checkboxes()
        self.set_checkboxes()
        self.blockSignals(block=not block)

    def update_preferences(self):
        """
        Updates the local preferences
        """

        self.prefs.subsurface_profile = self.ui.sub_sur_1_checkBox.isChecked()
        self.prefs.use_subsurface_distance_fading = self.ui.sub_sur_2_checkBox.isChecked()
        self.prefs.use_emissive = self.ui.emissive_checkBox.isChecked()
        self.prefs.use_bent_normals = self.ui.bn_checkBox.isChecked()
        self.prefs.use_filigree = self.ui.fillgri_checkBox.isChecked()
        self.prefs.use_detail_texture = self.ui.detail_texture_checkBox.isChecked()
        self.prefs.use_iridescent = self.ui.iridescent_checkBox.isChecked()
        self.prefs.use_fuzzy_clothing = self.ui.fuzzy_cloth_checkBox.isChecked()
        self.prefs.use_carbon_fiber = self.ui.cf_checkBox.isChecked()
        self.prefs.use_simple_decals = self.ui.decal_checkBox.isChecked()
        try:
            self.prefs.write_file()
        except Exception as e:
            logger.exception('Failed to write preferences file')
            logger.error(e)

    def set_checkboxes(self):
        """
        Sets the checkboxes from the preferences file.
        """

        subsurface = self.prefs.subsurface_profile or False
        subsurface_fading = self.prefs.use_subsurface_distance_fading or False
        emissive = self.prefs.use_emissive or False
        bn = self.prefs.use_bent_normals or False
        fil = self.prefs.use_filigree or False
        dt = self.prefs.use_detail_texture or False
        ir = self.prefs.use_iridescent or False
        fuzzy = self.prefs.use_fuzzy_clothing or False
        carbon = self.prefs.use_carbon_fiber or False
        decals = self.prefs.use_simple_decals or False

        self.ui.sub_sur_1_checkBox.setChecked(subsurface)
        self.ui.sub_sur_2_checkBox.setChecked(subsurface_fading)
        self.ui.emissive_checkBox.setChecked(emissive)
        self.ui.bn_checkBox.setChecked(bn)
        self.ui.fillgri_checkBox.setChecked(fil)
        self.ui.detail_texture_checkBox.setChecked(dt)
        self.ui.iridescent_checkBox.setChecked(ir)
        self.ui.fuzzy_cloth_checkBox.setChecked(fuzzy)
        self.ui.cf_checkBox.setChecked(carbon)
        self.ui.decal_checkBox.setChecked(decals)
