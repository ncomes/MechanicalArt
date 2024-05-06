# -*- coding: utf-8 -*-

"""
Initialization module for import and creating Textures and Material Instance Constants.
"""

# mca python imports
import os
# PySide2 imports
# software specific imports
# mca python imports
from mca.common import log
from mca.common.pyqt import common_windows
from mca.common.modifiers import decorators
from mca.ue.assetlist import ue_assetlist

logger = log.MCA_LOGGER


class MATUnrealAssetListUI(common_windows.MCAMainWindow):
    """
    UI for importing Textures and creating Material Instance Constants.
    """

    VERSION = '1.0.0'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'asset_list.ui')
        super().__init__(title='Asset List UI',
                         ui_path=ui_path,
                         version=MATUnrealAssetListUI.VERSION,
                         style='incrypt',
                         parent=parent)

        self.ue_asset_list = ue_assetlist.UnrealAssetListToolBox()

        self.set_ui_properties()

        ############################################
        # Signals
        ############################################
        self.ui.asset_type_comboBox.currentIndexChanged.connect(self.set_asset_names)
        self.ui.refresh_pushButton.clicked.connect(self.reset)
        self.ui.asset_name_comboBox.currentIndexChanged.connect(self.update_preferences)

    @decorators.track_fnc
    def reset(self):
        """
        Resets the UI
        """

        self.ue_asset_list.reload_asset_list()
        subtype_filter = self.ue_asset_list.get_sub_type_filter()

        self.blockSignals(True)
        self.ui.asset_type_comboBox.addItems(subtype_filter)
        type_name = self.ui.asset_type_comboBox.currentText()
        names = self.ue_asset_list.get_names_from_type(type_name)
        self.ui.asset_name_comboBox.addItems(names)
        self.blockSignals(False)

    def set_asset_types(self):
        """
        Sets the asset type combobox
        """

        self.blockSignals(True)
        asset_type = self.ue_asset_list.asset_type
        subtype_filter = self.ue_asset_list.get_sub_type_filter()
        self.ui.asset_type_comboBox.clear()
        self.ui.asset_type_comboBox.addItems(subtype_filter)
        if asset_type:
            self.ui.asset_type_comboBox.setCurrentText(asset_type)
        self.blockSignals(False)

    def set_asset_names(self):
        """
        Sets the asset name combo box
        """

        self.ui.asset_name_comboBox.clear()

        type_name = self.ui.asset_type_comboBox.currentText()
        names = self.ue_asset_list.get_names_from_type(type_name)
        self.ui.asset_name_comboBox.addItems(sorted(names))

        asset_name = self.ue_asset_list.asset_name
        if asset_name:
            self.ui.asset_name_comboBox.setCurrentText(asset_name)

    def update_preferences(self):
        """
        Updates the local preferences
        """

        self.ue_asset_list.asset_type = self.ui.asset_type_comboBox.currentText()
        self.ue_asset_list.asset_name = self.ui.asset_name_comboBox.currentText()
        self.ue_asset_list.write_file()

    def blockSignals(self, block=True):
        """
        Blocks signals
        :param bool block: True to block signals, False to unblock
        """

        self.ui.asset_type_comboBox.blockSignals(block)
        self.ui.asset_name_comboBox.blockSignals(block)

    def set_ui_properties(self, block=True):
        """
        Sets the UI properties
        :param bool block: True to block signals, False to unblock
        """

        self.blockSignals(block=block)
        self.set_asset_types()
        self.set_asset_names()
        self.blockSignals(block=not block)
