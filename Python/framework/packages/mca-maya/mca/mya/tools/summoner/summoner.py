#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# python imports
import os
# software specific imports
# mca python imports
from mca.common.assetlist import assetlist
from mca.common.tools.dcctracking import dcc_tracking

from mca.mya.pyqt import dialogs, mayawindows
from mca.mya.rigging import rig_utils, skel_utils
from mca.mya.utils import optionvars
from mca.mya.tools.helios import helios_registry, helios_utils


class MCASummonerOptionVars(optionvars.MCAOptionVars):
    """
    This handles keeping track of Summoner's last UI values to be restored or used during various UI functions.
    """
    
    MCALastSummonerCategory = {'default_value': '', 'docstring': 'Last opened category in Summoner.'}
    MCALastRig = {'default_value': '', 'docstring': 'Last selected rig in Summoner.'}
    MCASMCheckBox = {'default_value': False, 'docstring': 'If SM was checked.'}
    MCASKCheckBox = {'default_value': False, 'docstring': 'If SK was checked.'}


class Summoner(mayawindows.MCAMayaWindow):
    VERSION = '1.0.3'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'summoner_small_ui.ui')
        super().__init__(title='Summoner',
                         ui_path=ui_path,
                         version=Summoner.VERSION)

        self.setMinimumHeight(110)
        self.setMinimumWidth(300)
        
        
        self.optionvars = MCASummonerOptionVars()
        
        self.DISPLAY_TO_ASSET_ID_DICT = {}

        mca_asset_list = assetlist.AssetListRegistry()
        mca_asset_list.reload()

        self.setup_category_combobox()
        self.setup_signals()

        # Sets up checkboxes
        self.ui.as_sk_checkBox.blockSignals(True)
        self.ui.as_sm_checkBox.blockSignals(True)
        self.ui.as_sk_checkBox.setChecked(self.optionvars.MCASKCheckBox)
        self.ui.as_sm_checkBox.setChecked(self.optionvars.MCASMCheckBox)
        self.ui.as_sk_checkBox.blockSignals(False)
        self.ui.as_sm_checkBox.blockSignals(False)
        
    def setup_signals(self):
        self.ui.type_comboBox.currentTextChanged.connect(self._category_changed)
        self.ui.rig_comboBox.currentTextChanged.connect(self._rig_changed)
        self.ui.as_sm_checkBox.stateChanged.connect(self._sm_checkbox)
        self.ui.as_sk_checkBox.stateChanged.connect(self._sk_checkbox)
        self.ui.import_pushButton.clicked.connect(self.import_asset)

    def setup_category_combobox(self):
        """
        Adds each category into the type combo box of the UI.

        """
        mca_asset_list = assetlist.AssetListRegistry()

        self.ui.type_comboBox.clear()
        self.DISPLAY_TO_ASSET_ID_DICT = {}
        category_list = []
        for sub_category, entry_dict in mca_asset_list.CATEGORY_DICT.get('model', {}).items():
            if sub_category in assetlist.NON_RIG_ASSETS:
                continue
            category_list.append(sub_category)
            for asset_id, mca_asset in entry_dict.items():
                self.DISPLAY_TO_ASSET_ID_DICT[mca_asset.asset_name] = mca_asset

        self.ui.type_comboBox.addItems(list(sorted(category_list)))

        if self.optionvars.MCALastSummonerCategory in category_list:
            self.ui.type_comboBox.setCurrentText(self.optionvars.MCALastSummonerCategory)

        self._category_changed()

    def _category_changed(self):
        """
        When the category is changed refresh the rig list combo box.

        """
        category = self.ui.type_comboBox.currentText()
        mca_asset_list = assetlist.AssetListRegistry()

        self.ui.rig_comboBox.clear()
        rig_list = []
        if category in mca_asset_list.CATEGORY_DICT.get('model', {}):
            for asset_id, mca_asset in mca_asset_list.CATEGORY_DICT.get('model', {}).get(category, {}).items():
                rig_list.append(mca_asset.asset_name)

        self.ui.rig_comboBox.blockSignals(True)
        self.ui.rig_comboBox.addItems(list(sorted(rig_list)))
        self.ui.rig_comboBox.blockSignals(False)

        if self.optionvars.MCALastRig in rig_list:
            self.ui.rig_comboBox.blockSignals(True)
            self.ui.rig_comboBox.setCurrentText(self.optionvars.MCALastRig)
            self.ui.rig_comboBox.blockSignals(False)

        self.optionvars.MCALastSummonerCategory = self.ui.type_comboBox.currentText()

    def _rig_changed(self):
        """
        Whenever a new rig is selected from the rig list combo box save the value in the user's option vars.

        """
        self.optionvars.MCALastRig = self.ui.rig_comboBox.currentText()

    def _sk_checkbox(self):
        """
        Checks if SM is checked or not and unchecks SK accordingly.

        """
        sm_status = self.ui.as_sm_checkBox.isChecked()
        if sm_status == True:
            self.ui.as_sm_checkBox.blockSignals(True)
            self.ui.as_sm_checkBox.setChecked(False)
            self.ui.as_sm_checkBox.blockSignals(False)
        else:
            pass

        self.optionvars.MCASKCheckBox = self.ui.as_sk_checkBox.isChecked()
        self.optionvars.MCASMCheckBox = self.ui.as_sm_checkBox.isChecked()

    def _sm_checkbox(self):
        """
        Checks if SK is checked or not and unchecks SM accordingly.

        """
        sk_status = self.ui.as_sk_checkBox.isChecked()
        if sk_status == True:
            self.ui.as_sk_checkBox.blockSignals(True)
            self.ui.as_sk_checkBox.setChecked(False)
            self.ui.as_sk_checkBox.blockSignals(False)
        else:
            pass

        self.optionvars.MCASKCheckBox = self.ui.as_sk_checkBox.isChecked()
        self.optionvars.MCASMCheckBox = self.ui.as_sm_checkBox.isChecked()

    def import_asset(self):
        """
        From the displayname get our asset ID from our saved dict, then import an asset based on it.

        """
        display_name = self.ui.rig_comboBox.currentText()
        mca_asset = self.DISPLAY_TO_ASSET_ID_DICT[display_name]
        result = dialogs.question_prompt(title='Import Asset', text=f'Import {display_name} in the scene?')
        if result != 'Yes':
            return

        if self.ui.as_sk_checkBox.isChecked():
            _, skel_dict = helios_utils.import_helios_asset(mca_asset)
            bind_root = skel_dict[mca_asset.skel_path]
            skel_utils.import_merge_skeleton(mca_asset.skel_path, bind_root)
        elif self.ui.as_sm_checkBox.isChecked():
            helios_utils.import_helios_asset(mca_asset, with_skinning=False)
        else:
            rig_utils.import_asset(mca_asset.asset_id)

        # dcc data
        dcc_tracking.ddc_tool_entry_thead(fn=self.import_asset, asset_name=mca_asset.asset_name, asset_id=mca_asset.asset_id)
