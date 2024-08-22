"""
Tool for adding and removing assets from asset list
"""

# python imports
import os
# software specific imports
# Qt imports
from mca.common.pyqt.pygui import qtwidgets
# mca python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.project import project_paths
from mca.common.pyqt import common_windows, messages
from mca.common.utils import list_utils, path_utils, string_utils

logger = log.MCA_LOGGER


class AssetRegister(common_windows.MCAMainWindow):
    VERSION = '2.1'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'asset_register_ui.ui')
        super().__init__(title='Asset Register',
                         ui_path=ui_path,
                         version=AssetRegister.VERSION,
                         parent=parent)

        self.active_entry = None
        self.setup_signals()

    def setup_signals(self):
        self.ui.category_comboBox.currentTextChanged.connect(self._filter_lists)
        self.ui.filter_lineEdit.textChanged.connect(self._filter_lists)
        self.ui.asset_listWidget.itemSelectionChanged.connect(self._on_asset_selected)
        self.ui.remove_pushButton.clicked.connect(self._on_remove_asset_button_clicked)

        self.ui.new_asset_pushButton.clicked.connect(self._clear_fields())
        self.ui.asset_name_lineEdit.editingFinished.connect(self._on_asset_name_changed)
        self.ui.file_browser_pushButton.clicked.connect(self._on_file_browser_button_clicked)
        self.ui.asset_path_lineEdit.editingFinished.connect(self._validate_path)
        self.ui.save_pushButton.clicked.connect(self._on_save_button_clicked)

        self._initialize_lists()

    def _initialize_lists(self):
        self.FILTERABLE_ASSETS_DICT = {}
        active_category = self.ui.category_comboBox.currentText()
        self.ui.category_comboBox.clear()
        self.ui.asset_subtype_comboBox.clear()

        asset_registry = assetlist.AssetListRegistry()
        asset_registry.reload()
        for subtype_name, subtype_data_dict in sorted(asset_registry.CATEGORY_DICT.get('model', {}).items()):
            if subtype_name.lower() in assetlist.NON_RIG_ASSETS:
                continue
            if subtype_name not in self.FILTERABLE_ASSETS_DICT:
                self.FILTERABLE_ASSETS_DICT[subtype_name] = {}
            for _, asset_entry in subtype_data_dict.items():
                self.FILTERABLE_ASSETS_DICT[subtype_name][asset_entry.asset_name] = asset_entry
            self.ui.category_comboBox.addItem(subtype_name)
            self.ui.asset_subtype_comboBox.addItem(subtype_name)

        if active_category:
            self.ui.category_comboBox.setCurrentText(active_category)

        self._filter_lists()

    def _filter_lists(self):
        self._clear_fields()

        filter_string_raw = self.ui.filter_lineEdit.text()
        required_str_list = []
        excluded_str_list = []
        for filter_string in filter_string_raw.split(' '):
            if filter_string.startswith('-'):
                if filter_string != '-':
                    excluded_str_list.append(filter_string[1:].lower())
            else:
                required_str_list.append(filter_string.lower())

        self.ui.asset_listWidget.clear()

        #logger.debug(f'required: {required_str_list} \nexcluded: {excluded_str_list}')

        active_category = self.ui.category_comboBox.currentText()
        self.ui.asset_subtype_comboBox.setCurrentText(active_category)
        for asset_name in sorted(self.FILTERABLE_ASSETS_DICT.get(active_category, {})):
            if required_str_list and not all(x in asset_name.lower() for x in required_str_list):
                # if we don't find all our expected filters in the name
                continue

            if excluded_str_list and any(x in asset_name.lower() for x in excluded_str_list):
                # if we find any of our exclusions in the name
                continue

            self.ui.asset_listWidget.addItem(asset_name)

    def _on_file_browser_button_clicked(self):
        """
        Opens Maya file dialog and sets chosen path in path line
        """

        current_path = self.ui.asset_path_lineEdit.text()
        start_path = path_utils.to_full_path(os.path.split(current_path)[0]) if current_path else os.path.join(project_paths.MCA_PROJECT_ROOT, 'Characters')

        found_path = list_utils.get_first_in_list(common_windows.getOpenFilesAndDirs(None,
                                                                                'Select a SM fbx file or folder:',
                                                                                start_path,
                                                                                'SM fbx (*.fbx)',
                                                                                options=qtwidgets.QFileDialog.DontConfirmOverwrite))
        if not found_path:
            return

        found_path = path_utils.to_relative_path(found_path)
        self.ui.asset_path_lineEdit.setText(found_path)

    def _clear_fields(self):
        self.ui.asset_listWidget.selectionModel().clearSelection()
        self.ui.asset_name_lineEdit.clear()
        self.ui.asset_namespace_lineEdit.clear()
        self.ui.asset_path_lineEdit.clear()
        self.ui.archetype_lineEdit.clear()

    def _on_asset_selected(self):
        """
        Sets information in data lines for the selected asset
        """

        active_subtype = self.ui.category_comboBox.currentText()
        active_selection = self.ui.asset_listWidget.currentItem()

        if not active_selection:
            self.clear_data_lines()
            return

        self.active_entry = self.FILTERABLE_ASSETS_DICT.get(active_subtype, {}).get(active_selection.text())

        if self.active_entry:
            self.ui.asset_path_lineEdit.setText(self.active_entry.sm_path)
            self.ui.asset_name_lineEdit.setText(self.active_entry.asset_name)
            self.ui.asset_namespace_lineEdit.setText(self.active_entry.asset_namespace)
            self.ui.asset_subtype_comboBox.setCurrentText(self.active_entry.asset_subtype)
            self.ui.archetype_lineEdit.setText(self.active_entry.asset_archetype)

    def _on_remove_asset_button_clicked(self):
        """
        Removes selected asset from asset list.
        """

        active_subtype = self.ui.category_comboBox.currentText()
        active_selection = self.ui.asset_listWidget.currentItem()

        if not active_selection:
            return

        asset_name = active_selection.text()

        result = messages.question_message('Remove Asset', f'Remove {asset_name} from asset list?')
        if result != 'Yes':
            return

        asset_entry = self.FILTERABLE_ASSETS_DICT[active_subtype][asset_name]

        assetlist.AssetListRegistry().remove_entry(asset_entry.asset_id, commit=True)
        self._initialize_lists()
        self._clear_fields()
        logger.info('Asset removed successfully.')

    def _on_save_button_clicked(self):
        """
        Updates asset list with user data input
        """
        asset_name = self.ui.asset_name_lineEdit.text()
        if not asset_name:
            logger.error('Add a asset name to continue.')
            return
        asset_namespace = self.ui.asset_namespace_lineEdit.text().lower()

        asset_subtype = self.ui.asset_subtype_comboBox.currentText()

        asset_path = path_utils.to_relative_path(self.ui.asset_path_lineEdit.text())
        if not asset_path:
            logger.error('Validate the asset path to continue')
            return

        if self.active_entry:
            # We're replacing an existing asset
            asset_entry = self.active_entry
        else:
            # We're adding a new asset.
            asset_id = string_utils.generate_guid()
            asset_entry = assetlist.MATAsset(asset_id, {})

        # Only allow registering of model type assets
        data_dict = {}
        data_dict['name'] = asset_name
        data_dict['namespace'] = asset_namespace
        data_dict['path'] = asset_path
        data_dict['type'] = 'model'
        data_dict['subtype'] = asset_subtype
        data_dict['archetype'] = self.ui.archetype_lineEdit.text()

        asset_entry._set_data(data_dict)
        asset_entry.DIRTY = True

        asset_entry.register()

        self._initialize_lists()
        self._clear_fields()
        self.active_entry = None
        logger.info('Asset saved successfully.')

    def _on_asset_name_changed(self):
        current_path = self.ui.asset_path_lineEdit.text()
        if current_path:
            # If we already have a path when we change the name don't adjust it.
            return

        current_name = self.ui.asset_path_lineEdit.text()
        asset_entry = assetlist.get_asset_by_name(current_name)
        if asset_entry:
            self.ui.asset_path_lineEdit.setText(path_utils.to_relative_path(asset_entry.sm_path))
        else:
            self._validate_path()

    def _validate_path(self):
        """
        Make sure we have a valid SM path here.
        """
        if not self.ui.asset_name_lineEdit.text():
            return

        self.ui.asset_path_lineEdit.blockSignals(True)

        current_path = self.ui.asset_path_lineEdit.text()
        if not current_path.endswith('.fbx'):
            current_name = self.ui.asset_path_lineEdit.text()
            asset_name = current_name.replace(' ', '_')
            file_name = f"SM_{asset_name}.fbx"
            sm_path = os.path.join('Characters', self.ui.asset_subtype_comboBox.currentText(), asset_name, 'Meshes', file_name)
            self.ui.asset_path_lineEdit.setText(sm_path)

        current_path = self.ui.asset_path_lineEdit.text()
        if 'SM_' not in current_path:
            if current_path.endswith('.fbx'):
                # If we have a fbx but the file name does not start with SM rebuild the path.
                self.ui.asset_path_lineEdit.setText(os.path.split(current_path)[0])
                self._validate_path()

        self.ui.asset_path_lineEdit.blockSignals(False)
