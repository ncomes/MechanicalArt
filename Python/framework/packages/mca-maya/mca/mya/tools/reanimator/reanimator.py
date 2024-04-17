#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Test tool implementation.

"""

# System global imports
import os
# Software specific imports
import pymel.all as pm
# mca python imports
from mca.common import log
from mca.common.utils import process
from mca.common.modifiers import decorators
from mca.common.tools.dcctracking import dcc_tracking
from mca.mya.utils import optionvars
from mca.mya.animation import time_utils, baking
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows

from mca.mya.rigging import rig_utils

logger = log.MCA_LOGGER

BAKE_OPTION_VARS = baking.MCABakeOptionVars()


class MCAReanimatorOptionVars(optionvars.MCAOptionVars):
    # Helios Misc
    MCAReanimatorTX = {'default_value': True, 'docstring': 'Overdiver should constrain translate X.'}
    MCAReanimatorTY = {'default_value': True, 'docstring': 'Overdiver should constrain translate Y.'}
    MCAReanimatorTZ = {'default_value': True, 'docstring': 'Overdiver should constrain translate Z.'}
    MCAReanimatorRX = {'default_value': True, 'docstring': 'Overdiver should constrain rotate X.'}
    MCAReanimatorRY = {'default_value': True, 'docstring': 'Overdiver should constrain rotate Y.'}
    MCAReanimatorRZ = {'default_value': True, 'docstring': 'Overdiver should constrain rotate Z.'}
    MCAReanimatorAppend = {'default_value': False, 'docstring': 'When baking animation to the rig if the animation should be baked in place, or appended after the last animated frame.'}
    MCAReanimatorMotionEncode = {'default_value': False, 'docstring': 'When baking animation to the rig if the animation should try and match root motion before being applied.'}
    MCAReanimatorStartToZero = {'default_value': False, 'docstring': 'When baking the rig to a skeleton if the animation should be shifted to start at frame 0.'}


REANIMATOR_OPTION_VARS = MCAReanimatorOptionVars()


class Reanimator(mayawindows.MCAMayaWindow):
    VERSION = '1.0.1'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'ReanimatorUI.ui')
        super().__init__(title='Reanimator',
                         ui_path=ui_path,
                         version=Reanimator.VERSION)


        self.ui.use_frame_range_checkBox.setChecked(BAKE_OPTION_VARS.MCAFrameOverride)
        self.ui.start_frame_spinBox.setValue(BAKE_OPTION_VARS.MCAStartFrame)
        self.ui.end_frame_spinBox.setValue(BAKE_OPTION_VARS.MCAEndFrame)

        self.ui.translate_x_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorTX)
        self.ui.translate_y_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorTY)
        self.ui.translate_z_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorTZ)
        self.ui.rotate_x_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorRX)
        self.ui.rotate_y_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorRY)
        self.ui.rotate_z_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorRZ)

        self.ui.append_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorAppend)
        self.ui.motion_encode_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorMotionEncode)

        self.ui.start_at_zero_checkBox.setChecked(REANIMATOR_OPTION_VARS.MCAReanimatorStartToZero)

        # ==============================
        # Signals
        # ==============================
        self.ui.start_frame_spinBox.valueChanged.connect(self._update_option_vars)
        self.ui.end_frame_spinBox.valueChanged.connect(self._update_option_vars)
        self.ui.use_frame_range_checkBox.stateChanged.connect(self._update_option_vars)
        self.ui.bake_selected_pushButton.clicked.connect(self._on_bake_selected_clicked)

        self.ui.mirror_rig_pushButton.clicked.connect(self._on_mirror_rig_clicked)

        self.ui.attach_rigs_pushButton.clicked.connect(self._on_attach_selected_rigs_clicked)
        self.ui.detach_rig_pushButton.clicked.connect(self._on_detach_selected_rig_clicked)
        self.ui.bake_and_detach_pushButton.clicked.connect(self._on_bake_and_detach_selected_rig_clicked)

        self.ui.add_overdriver_pushButton.clicked.connect(self._on_add_overdriver_clicked)
        self.ui.remove_overdriver_pushButton.clicked.connect(self._on_remove_overdriver_clicked)
        self.ui.bake_and_remover_overdriver_pushButton.clicked.connect(self._on_remove_and_bake_overdriver_clicked)

        self.ui.bake_to_rig_pushButton.clicked.connect(self._on_bake_to_rig_clicked)
        self.ui.bake_to_skeleton_pushButton.clicked.connect(self._on_bake_to_skeleton_clicked)
    
    # ==============================
    # Slots
    # ==============================
    
    def _update_option_vars(self):
        BAKE_OPTION_VARS.MCAFrameOverride = bool(self.ui.use_frame_range_checkBox.isChecked())
        BAKE_OPTION_VARS.MCAStartFrame = int(self.ui.start_frame_spinBox.text())
        BAKE_OPTION_VARS.MCAEndFrame = int(self.ui.end_frame_spinBox.text())

        REANIMATOR_OPTION_VARS.MCAReanimatorTX = bool(self.ui.translate_x_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorTY = bool(self.ui.translate_y_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorTZ = bool(self.ui.translate_z_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorRX = bool(self.ui.rotate_x_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorRY = bool(self.ui.rotate_y_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorRZ = bool(self.ui.rotate_z_checkBox.isChecked())

        REANIMATOR_OPTION_VARS.MCAReanimatorAppend = bool(self.ui.append_checkBox.isChecked())
        REANIMATOR_OPTION_VARS.MCAReanimatorMotionEncode = bool(self.ui.motion_encode_checkBox.isChecked())

        REANIMATOR_OPTION_VARS.MCAReanimatorStartToZero = bool(self.ui.start_at_zero_checkBox.isChecked())

    def _get_ui_time_range(self):
        """
        If use frame range is selected lets peal the frame range from the UI

        :return:
        """

        self._update_option_vars()

        if BAKE_OPTION_VARS.MCAFrameOverride:
            start_frame = BAKE_OPTION_VARS.MCAStartFrame
            end_frame = BAKE_OPTION_VARS.MCAEndFrame
            if end_frame < start_frame:
                # trying to be clever here? reverse the orders.
                logger.warning("End frame is less than start frame, we'll reverse the order and continue.")
            return (end_frame, start_frame) if end_frame < start_frame else (start_frame, end_frame)
        return None, None

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    @decorators.track_fnc
    def _on_bake_selected_clicked(self):
        selection = pm.selected()
        if not selection:
            return

        custom_attrs = []
        for x in selection:
            custom_attrs += x.listAttr(ud=True, k=True)

        start_frame, end_frame = self._get_ui_time_range()
        bake_range = [start_frame, end_frame] if start_frame else None
        baking.bake_objects(selection, custom_attrs=custom_attrs, bake_range=bake_range)

    def _on_attach_selected_rigs_clicked(self):
        asset_id = rig_utils.attach_rigs_cmd()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_attach_selected_rigs_clicked, asset_id=asset_id)

    def _on_detach_selected_rig_clicked(self):
        asset_id = rig_utils.detach_rig_cmd()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_detach_selected_rig_clicked, asset_id=asset_id)

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_bake_and_detach_selected_rig_clicked(self):
        logger.warning('Baking animation to rig.')
        start_frame, end_frame = self._get_ui_time_range()

        asset_id = rig_utils.detach_rig_cmd(True, start_frame, end_frame)
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_bake_and_detach_selected_rig_clicked, asset_id=asset_id)

    def _on_add_overdriver_clicked(self):

        skip_rotate_attrs = []
        if not self.ui.rotate_x_checkBox.isChecked(): skip_rotate_attrs.append('x')
        if not self.ui.rotate_y_checkBox.isChecked(): skip_rotate_attrs.append('y')
        if not self.ui.rotate_z_checkBox.isChecked(): skip_rotate_attrs.append('z')

        skip_translate_attrs = []
        if not self.ui.translate_x_checkBox.isChecked(): skip_translate_attrs.append('x')
        if not self.ui.translate_y_checkBox.isChecked(): skip_translate_attrs.append('y')
        if not self.ui.translate_z_checkBox.isChecked(): skip_translate_attrs.append('z')

        asset_id = rig_utils.create_overdriver_cmd(skip_rotate_attrs, skip_translate_attrs)
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_add_overdriver_clicked, asset_id=asset_id)

    @decorators.track_fnc
    def _on_remove_overdriver_clicked(self):
        rig_utils.bake_overdriver_cmd(False)

    @decorators.track_fnc
    def _on_remove_and_bake_overdriver_clicked(self):
        start_frame, end_frame = self._get_ui_time_range()
        rig_utils.bake_overdriver_cmd(True, start_frame, end_frame)

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_bake_to_rig_clicked(self):
        logger.debug('Baking animation to rig.')
        start_frame, end_frame = self._get_ui_time_range()
        asset_id = rig_utils.animate_rig_from_skeleton_cmd(start_frame=start_frame, end_frame=end_frame,
                                                  append=self.ui.append_checkBox.isChecked(),
                                                  motion_encode=self.ui.motion_encode_checkBox.isChecked())

        time_utils.reframe_visible_range()
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_bake_to_rig_clicked, asset_id=asset_id)

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_bake_to_skeleton_clicked(self):
        logger.debug('Baking rig to skeleton')
        start_frame, end_frame = self._get_ui_time_range()
        asset_id = rig_utils.bake_skeleton_from_rig_cmd(start_frame=start_frame, end_frame=end_frame,
                                               set_to_zero=self.ui.start_at_zero_checkBox.isChecked())
        # dcc data
        dcc_tracking.ddc_tool_entry_thead(self._on_bake_to_skeleton_clicked, asset_id=asset_id)

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def _on_mirror_rig_clicked(self):
        logger.debug('Baking rig to skeleton')
        start_frame, end_frame = self._get_ui_time_range()
        asset_ids = rig_utils.mirror_rig_cmd(start_frame=start_frame, end_frame=end_frame)
        if asset_ids:
            asset_ids = list(set(asset_ids))
            for asset_id in asset_ids:
                # dcc data
                dcc_tracking.ddc_tool_entry_thead(self._on_mirror_rig_clicked, asset_id=asset_id)
