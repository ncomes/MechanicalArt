#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# System global imports
import os
# software specific imports
# PySide2 imports
from PySide2.QtCore import QSize
# mca python imports
from mca.common import log
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.resources import resources
from mca.mya.utils import optionvars
from mca.mya.rigging import rig_utils
from mca.mya.animation import time_utils, baking
from mca.mya.modifiers import ma_decorators
from mca.mya.tools.reanimator import reanimator
from mca.mya.pyqt import mayawindows, dialogs

logger = log.MCA_LOGGER

resources.register_resources()

BAKE_OPTION_VARS = baking.MCABakeOptionVars()


class MCAReanimatorOptionVars(optionvars.MCAOptionVars):
    MCAReanimBakeToRig = {'default_value': 0, 'docstring': 'Sets the Bake to Rig comboBox.'}
    MCAReanimSmallStartToZero = {'default_value': False, 'docstring': 'When baking the rig to a skeleton if the animation should be shifted to start at frame 0.'}
    MCAReanimUseFrameRange = {'default_value': False, 'docstring': 'Use Frame range when baking.'}


class ReanimatorSmall(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'Reanimator_tb.ui')
        super().__init__(title='Reanimator Compact',
                         ui_path=ui_path,
                         version=ReanimatorSmall.VERSION)
        
        self.optionvars = MCAReanimatorOptionVars()
        
        self.setMinimumHeight(250)
        self.setMaximumHeight(250)
        self.ui.to_rig_pushButton.setIcon(resources.icon(r'tools\player_run_pose_long.png'))
        self.ui.to_rig_pushButton.setIconSize(QSize(300, 40))
        self.ui.to_skel_pushButton.setIcon(resources.icon(r'tools\player_run_pose2_long.png'))
        self.ui.to_skel_pushButton.setIconSize(QSize(300, 40))
        
        # Optionvar Settings
        self.ui.to_rig_comboBox.setCurrentIndex(self.optionvars.MCAReanimBakeToRig)
        self.ui.start_frame_spinBox.setValue(BAKE_OPTION_VARS.MCAStartFrame)
        self.ui.end_frame_spinBox.setValue(BAKE_OPTION_VARS.MCAEndFrame)
        self.ui.start_at_zero_checkBox.setChecked(self.optionvars.MCAReanimSmallStartToZero)
        self.ui.use_frame_range_checkBox.setChecked(self.optionvars.MCAReanimUseFrameRange)

        
        #########################################
        # Signals
        #########################################
        self.ui.use_frame_range_checkBox.clicked.connect(self._update_option_vars)
        self.ui.start_frame_spinBox.valueChanged.connect(self._update_option_vars)
        self.ui.end_frame_spinBox.valueChanged.connect(self._update_option_vars)
        self.ui.start_at_zero_checkBox.clicked.connect(self._update_option_vars)
        self.ui.to_rig_comboBox.currentIndexChanged.connect(self._update_option_vars)
        self.ui.reload_rig_pushButton.clicked.connect(self.reload_rig)
        self.ui.to_rig_pushButton.clicked.connect(self._on_bake_to_rig_clicked)
        self.ui.to_skel_pushButton.clicked.connect(self._on_bake_to_skeleton_clicked)
        
        self.ui.pop_pushButton.clicked.connect(self.open_reanimator)
    
    ####################################
    # Slots
    ####################################
    
    def open_reanimator(self):
        reanimator.Reanimator()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self.open_reanimator, fn_name='popout reanimator', ui_type='toolbox')

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_bake_to_rig_clicked(self):
        motion_encode = False
        append_motion = False
        if self.ui.to_rig_comboBox.currentIndex() == 2 or self.ui.to_rig_comboBox.currentIndex() == 3:
            motion_encode = True
        
        if self.ui.to_rig_comboBox.currentIndex() == 1 or self.ui.to_rig_comboBox.currentIndex() == 3:
            append_motion = True
        
        logger.warning('Baking animation to rig.')
        asset_id = rig_utils.animate_rig_from_skeleton_cmd(append=append_motion,
                                                            motion_encode=motion_encode)
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_bake_to_rig_clicked, asset_id=asset_id, ui_type='toolbox')
    
        time_utils.reframe_visible_range()

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_bake_to_skeleton_clicked(self):
        logger.warning('Baking rig to skeleton')
        asset_id = rig_utils.bake_skeleton_from_rig_cmd(set_to_zero=self.ui.start_at_zero_checkBox.isChecked())
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_bake_to_skeleton_clicked, asset_id=asset_id, ui_type='toolbox')
    
    def _update_option_vars(self):
        self.optionvars.MCAReanimUseFrameRange = bool(self.ui.use_frame_range_checkBox.isChecked())
        BAKE_OPTION_VARS.MCAStartFrame = float(self.ui.start_frame_spinBox.text())
        BAKE_OPTION_VARS.MCAEndFrame = float(self.ui.end_frame_spinBox.text())
        self.optionvars.MCAReanimBakeToRig = int(self.ui.to_rig_comboBox.currentIndex())
        self.optionvars.MCAReanimSmallStartToZero = bool(self.ui.start_at_zero_checkBox.isChecked())
        
    def reload_rig(self):
        """
        Reloads the rig.  Imports a new rig and re-animates in in place.
        """
        result = dialogs.question_prompt(title='Reload Rig?', text='Reload selected rig/rigs?')
        if result != 'Yes':
            return
        asset_ids = rig_utils.reload_rig_cmd()
        if asset_ids:
            asset_ids = list(set(asset_ids))
            for asset_id in asset_ids:
                # dcc data
                dcc_tracking.ddc_tool_entry_thead(self.reload_rig, asset_id=asset_id, ui_type='toolbox')
    
    