#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base custom implementation for Neil3D Stay On Floor Tool
"""

# mca python imports
import os

# software specific imports
from pyfbsdk import FBSystem, FBTime, FBModelList, FBGetSelectedModels

# mca python imports
from mca.common.modifiers import decorators
from mca.common.utils import process
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.resources import resources
from mca.common import log
from mca.mobu.animation import timeline
from mca.mobu.pyqt import mobuwindows

from mca.mobu.tools.stayonfloor import lib


logger = log.MCA_LOGGER


class StayOnFloorTool(mobuwindows.MATMobuWindow):
    INITIAL_WIDTH = 280
    INITIAL_HEIGHT = 220
    
    VERSION = '1.0.0'
    
    def __init__(self, title='Stay On Floor'):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'stayonfloor_ui.ui')
        super().__init__(title=title, ui_path=ui_path, version=StayOnFloorTool.VERSION)

        self.setMinimumHeight(StayOnFloorTool.INITIAL_HEIGHT)
        self.setMinimumWidth(StayOnFloorTool.INITIAL_WIDTH)
        
        self.ui.run_comboBox.addItems(['T', 'R', 'TR', 'S', 'TRS'])
        max_frame = 100000000
        min_frame = -max_frame

        self.ui.start_spinBox.setMinimum(min_frame)
        self.ui.start_spinBox.setMaximum(max_frame)
        self.ui.end_spinBox.setMinimum(min_frame)
        self.ui.end_spinBox.setMaximum(max_frame)
        self.ui.blendtime_spinBox.setMinimum(min_frame)
        self.ui.blendtime_spinBox.setMaximum(max_frame)
        
        # Setup icons
        self.ui.start_pushButton.setIcon(resources.icon(r'default\cursor.png'))
        self.ui.end_pushButton.setIcon(resources.icon(r'default\cursor.png'))
        self.ui.run_pushButton.setIcon(resources.icon(r'default\play.png'))

        # Tracking
        process.cpu_threading(dcc_tracking.ddc_tool_entry(StayOnFloorTool))
        
        ############################
        # Signals
        ############################
        self.ui.start_pushButton.clicked.connect(self._on_assign_start_frame_button_clicked)
        self.ui.end_pushButton.clicked.connect(self._on_assign_end_frame_button_clicked)
        self.ui.blendtime_pushButton.clicked.connect(self._on_timeline_range_button_clicked)
        self.ui.run_pushButton.clicked.connect(self._on_run_button_clicked)

    ############################
    # Slots
    ############################
    def _on_assign_start_frame_button_clicked(self):
        logger.warning('start frame updated...')
        print(timeline.get_current_frame())
        self.ui.start_spinBox.setValue(timeline.get_current_frame())

    def _on_assign_end_frame_button_clicked(self):
        self.ui.end_spinBox.setValue(timeline.get_current_frame())

    def _on_timeline_range_button_clicked(self):
        start_frame, end_frame = timeline.get_active_frame_range()
        self.ui.start_spinBox.setValue(start_frame)
        self.ui.end_spinBox.setValue(end_frame)
    
    @decorators.track_fnc
    def _on_run_button_clicked(self):
        curren_time = FBSystem().LocalTime
        start_time = FBTime(0, 0, 0, int(self.ui.start_spinBox.value()))
        stop_time = FBTime(0, 0, 0, int(self.ui.end_spinBox.value()))
        blend_time = FBTime(0, 0, 0, int(self.ui.blendtime_spinBox.value()))

        models = FBModelList()
        FBGetSelectedModels(models)

        mode = self.ui.run_comboBox.currentIndex()
        for model in models:
            if mode in [0, 2, 4]:
                anim_node = model.Translation.GetAnimationNode()
                if anim_node:
                    lib.process_animation_node(anim_node, curren_time, start_time, stop_time, blend_time)
            if mode in [1, 2, 4]:
                anim_node = model.Rotation.GetAnimationNode()
                if anim_node:
                    lib.process_animation_node(anim_node, curren_time, start_time, stop_time, blend_time)
            if mode in [3, 4]:
                anim_node = model.Scaling.GetAnimationNode()
                if anim_node:
                    lib.process_animation_node(anim_node, curren_time, start_time, stop_time, blend_time)
