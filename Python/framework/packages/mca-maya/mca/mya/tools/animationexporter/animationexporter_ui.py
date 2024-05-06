#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains AnimationExporter UIs.

"""

# python imports
import os
import re

# software specific imports
import pymel.core as pm

from PySide2.QtWidgets import QVBoxLayout, QToolButton, QSizePolicy, QSpacerItem, QFrame

import PySide2.QtCore as QtCore
from PySide2.QtCore import Qt
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui


# mca python imports
from mca.common import log
from mca.common.modifiers import decorators
from mca.common.assetlist import assetlist
from mca.common.paths import path_utils, project_paths
from mca.common.pyqt import common_windows, messages
from mca.common.tools.dcctracking import dcc_tracking
from mca.common.utils import strings

from mca.mya.animation import time_utils
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import frag
from mca.mya.tools.animationexporter import animationexporter_utils as ae_utils
from mca.mya.utils import optionvars

logger = log.MCA_LOGGER


class MCAAnimationExporterOptionVars(optionvars.MCAOptionVars):
    """
    This stores the last path for animation browsing.

    """
    MCALastAnimationPath = {'default_value': project_paths.MCA_PROJECT_ROOT, 'docstring': 'Branch content path.'}


ANIMATIONEXPORTER_OPTION_VARS = MCAAnimationExporterOptionVars()
global SEQUENCE_PATH_DICT
SEQUENCE_PATH_DICT = {}


class AnimationExporter(mayawindows.MCAMayaWindow):
    VERSION = '1.0.3'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'animationexporter_mainUI.ui')
        super().__init__(title='AnimationExporter',
                         ui_path=ui_path,
                         version=AnimationExporter.VERSION)

        self._rig_dict = {}
        self._rig_list = []
        self.vertical_spacer = None
        self.initialize_tabs()
        self.setup_signals()

    def initialize_tabs(self):
        """
        This procedurally generates new tabs and fills them out from the found frag_rigs in the scene and all currently
        registered sequences on the FRAG Sequencer.

        """
        ae_utils.reconnect_orphaned_sequences()
        ae_utils.convert_legacy()

        # start fresh.
        self.ui.tabWidget.clear()

        self._rig_dict = {}
        self._rig_list = []

        global SEQUENCE_PATH_DICT
        for value in SEQUENCE_PATH_DICT.values():
            try:
                value.deleteLater()
            except:
                pass
        SEQUENCE_PATH_DICT = {}

        frag_root_list = frag.get_all_frag_roots()
        for frag_root in frag_root_list:
            # New tab for each rig in the scene.
            frag_rig = frag_root.get_rig()
            if not frag_rig:
                continue
            self._rig_dict[frag_rig] = {}
            self._rig_list.append(frag_rig)

            # Tab widget and layout
            rig_tab_widget = QtWidgets.QWidget()
            rig_vertical_layout = QtWidgets.QVBoxLayout()
            rig_horizontal_layout = QtWidgets.QHBoxLayout()
            rig_vertical_layout.addLayout(rig_horizontal_layout)
            rig_tab_widget.setLayout(rig_vertical_layout)

            toggle_export_checkbox = QtWidgets.QCheckBox('Toggle Rig Export')
            toggle_export_checkbox.setChecked(True)
            self._rig_dict[frag_rig]['toggle_rig_export_checkbox'] = toggle_export_checkbox
            rig_horizontal_layout.addWidget(toggle_export_checkbox)
            add_sequence_button = QtWidgets.QPushButton('Add Sequence')
            self._rig_dict[frag_rig]['add_sequence_button'] = add_sequence_button
            rig_horizontal_layout.addWidget(add_sequence_button)

            rig_tab_index = self.ui.tabWidget.addTab(rig_tab_widget, f'{frag_root.namespace().replace(":", "")}:{frag_root.assetName.get()}')

            # Sequence widget and v Layout
            rig_tab_sequence_widget = QtWidgets.QWidget()
            rig_sequence_vertical_layout = QtWidgets.QVBoxLayout()
            self._rig_dict[frag_rig]['rig_sequence_vertical_layout'] = rig_sequence_vertical_layout
            rig_tab_sequence_widget.setLayout(rig_sequence_vertical_layout)

            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(rig_tab_sequence_widget)
            rig_vertical_layout.addWidget(scroll_area)

            add_sequence_button.pressed.connect(self.add_sequence_cmd)
            toggle_export_checkbox.pressed.connect(self._toggle_local_export)

        for frag_rig, sequence_wrapper_dict in ae_utils.get_sequences().items():
            if not frag_rig:
                continue
            # If we have preexisting sequences registered on the FRAGSequencer load those into the GUI.
            # Order the entries based on the ui_index value for each entry.
            for index, (_, sequence_wrapper) in enumerate(sorted(sequence_wrapper_dict.items(), key=lambda sequence_tuple: sequence_tuple[1].ui_index)):
                sequence_widget = self.add_sequence(frag_rig)

                sequence_widget.ui.sequence_export_path_lineEdit.setText(sequence_wrapper.sequence_path)
                sequence_widget.ui.sequence_start_frame_lineEdit.setText(str(sequence_wrapper.frame_range[0]))
                sequence_widget.ui.sequence_end_frame_lineEdit.setText(str(sequence_wrapper.frame_range[1]))
                sequence_widget.ui.sequence_notes_lineEdit.setText(sequence_wrapper.sequence_notes)
                sequence_widget.ui.root_to_origin_checkBox.setChecked(sequence_wrapper.root_to_origin)
                sequence_widget.ui.start_to_zero_checkBox.setChecked(sequence_wrapper.start_at_zero)
                sequence_widget.ui.sequence_name_lineEdit.setText(os.path.basename(sequence_wrapper.sequence_path).replace('.fbx', ''))
                sequence_widget.set_sequence()
            self._add_vertical_spacer(frag_rig)

    def _add_vertical_spacer(self, frag_rig):
        """
                This removes and then adds the vertical spacer to the end of the main v_layout.

                """
        try:
            if self.vertical_spacer:
                self._rig_dict[frag_rig]['rig_sequence_vertical_layout'].removeWidget(self.vertical_spacer.widget())
        except:
            pass

        self.vertical_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._rig_dict[frag_rig]['rig_sequence_vertical_layout'].addItem(self.vertical_spacer)

    def setup_signals(self):
        """
        Non-dynamic UI signal hookup.

        """

        self.ui.export_all_checkBox.pressed.connect(self._toggle_global_export)
        self.ui.refresh_pushButton.pressed.connect(self.initialize_tabs)
        self.ui.all_rigs_export_selected_pushButton.pressed.connect(lambda: self.export_sequences())
        self.ui.all_rigs_export_all_pushButton.pressed.connect(lambda: self.export_sequences(True))

    def _toggle_global_export(self):
        """
        Toggle only all tab's sequence export checkbox.

        """
        self.toggle_export(self._rig_list, self.ui.export_all_checkBox)

    def _toggle_local_export(self):
        """
        Toggle only the current tab's sequence export checkbox.

        """
        index = self.ui.tabWidget.currentIndex()
        frag_rig = self._rig_list[index]

        self.toggle_export([frag_rig], self._rig_dict[frag_rig]['toggle_rig_export_checkbox'])

    def toggle_export(self, frag_rig_list, toggle_checkbox):
        """
        For each sequence entry belonging to the list of FRAG Rigs, toggle their export option to match the checkbox.

        :param list[FRAGRig] frag_rig_list:
        :param QtWidgets.QCheckbox toggle_checkbox: The checkbox that's currently being toggled.
        """
        global SEQUENCE_PATH_DICT
        check_val = toggle_checkbox.isChecked()

        for sequence_widget in SEQUENCE_PATH_DICT.values():
            if sequence_widget.frag_rig in frag_rig_list:
                sequence_widget.ui.export_sequence_checkBox.setChecked(not check_val)

    def add_sequence_cmd(self):
        """
        Finds the active UI tab and looks up the appropriate FRAGRig by its index.

        """
        index = self.ui.tabWidget.currentIndex()
        frag_rig = self._rig_list[index]

        self.add_sequence(frag_rig)
        asset_id = frag_rig.get_asset_id(frag_rig)
        dcc_tracking.ddc_tool_entry_thead(self.add_sequence_cmd, asset_id=asset_id)

    def add_sequence(self, frag_rig):
        """
        Add a new sequencer UI to the active tab.

        :param FRAGRig frag_rig:
        :return: The widget that represents the new sequence that was added.
        :rtype: AnimationExporterSequence
        """
        if not frag_rig.pynode.exists():
            self.initialize_tabs()

        parent_layout = self._rig_dict[frag_rig]['rig_sequence_vertical_layout']
        sequence_frame = SequenceFrameButton(frag_rig, parent=self, parent_layout=parent_layout)
        sequence_widget = sequence_frame.sequence_widget
        parent_layout.addWidget(sequence_frame)
        self._add_vertical_spacer(frag_rig)
        return sequence_widget

    def export_sequences(self, all_rigs=False):
        """
        For each registered sequence export them if their export toggles are true.

        :param bool all_rigs: If the current tab or all rig tabs should be exported.
        """
        global SEQUENCE_PATH_DICT

        sequences_to_skip = []
        active_frag_rig = self._rig_list[self.ui.tabWidget.currentIndex()]

        # Collect all sequence paths which should be skipped.
        for sequence_path, sequencer_widget in SEQUENCE_PATH_DICT.items():
            if not sequencer_widget.ui.export_sequence_checkBox.isChecked():
                if all_rigs:
                    sequences_to_skip.append(sequence_path)
                elif sequencer_widget.frag_rig == active_frag_rig:
                    sequences_to_skip.append(sequence_path)

        ae_utils.export_frag_sequences_cmd(frag_rig_list=self._rig_list, sequences_to_skip=sequences_to_skip)
        frag_list = list(set(self._rig_list))
        for frag_rig in frag_list:
            if not pm.objExists(frag_rig):
                messages.info_message('Export Failure', 'One or more frag rigs were unable to be located in the scene. Please ensure that the rig exists in the scene.', icon='error')
                return
            asset_id = frag_rig.get_asset_id(frag_rig)
            dcc_tracking.ddc_tool_entry_thead(self.export_sequences, asset_id=asset_id)


class SequenceFrameButton(QFrame):
    def __init__(self, frag_rig, parent=None, parent_layout=None):
        super().__init__(parent=parent)
        self.main_ui = parent
        self.parent_layout = parent_layout

        guid = strings.generate_guid()

        self.setContentsMargins(1, 0, 0, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(195)
        self.setMaximumHeight(195)

        self.tool_v_layout = QVBoxLayout(self)
        self.tool_v_layout.setContentsMargins(0, 0, 0, 0)

        self.tool_button = QToolButton(self)
        self.tool_button.setObjectName(f'{guid}_toolButton')
        self.tool_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tool_button.setArrowType(Qt.RightArrow)
        self.tool_button.setText('New Animation')
        self.tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tool_button.setContentsMargins(2, 0, 0, 1)
        self.tool_button.setMaximumHeight(25)
        self.tool_button.setMinimumHeight(25)
        self.tool_button.setParent(self)
        self.tool_v_layout.addWidget(self.tool_button)

        self.q_frame = QFrame(self)
        self.q_frame.setObjectName(f'{guid}_frame')
        self.q_frame.setContentsMargins(2, 0, 1, 0)
        self.q_frame.setMinimumHeight(25)
        self.tool_v_layout.addWidget(self.q_frame)
        self.q_frame.setVisible(0)
        self.q_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.sequence_layout = QVBoxLayout(self.q_frame)
        #self.sequence_layout.setContentsMargins(2, 0, 1, 0)
        self.sequence_layout.setObjectName(f'{guid}_layout')

        self.sequence_widget = AnimationExporterSequence(frag_rig, parent, self)
        self.sequence_layout.addWidget(self.sequence_widget.ui)

        #############
        # Signals
        #############
        self.tool_button.pressed.connect(self.button_pressed)
        self.open_button()

    def remove_frame(self):
        self.parent_layout.removeWidget(self)
        self.deleteLater()


    ##########
    # Slots
    ##########
    def button_pressed(self):
        """
        Opens or closes the QToolbarButton
        """

        if self.q_frame and not self.q_frame.isVisible():
            self.open_button()
        else:
            self.close_button()

    def open_button(self):
        """
        Opens the QToolbarButton
        """

        self.tool_button.setArrowType(Qt.DownArrow)
        self.q_frame.setVisible(1)
        self.setMinimumHeight(195)

    def close_button(self):
        """
        Closes the QToolbarButton
        """

        self.tool_button.setArrowType(Qt.RightArrow)
        self.q_frame.setVisible(0)
        self.setMinimumHeight(25)


class AnimationExporterSequence(common_windows.ParentableWidget):
    def __init__(self, frag_rig, parent=None, parent_frame=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'animationexporter_sequenceUI.ui')
        super().__init__(parent=parent,
                         ui_path=ui_path)

        self.frag_rig = frag_rig
        self.parent_frame = parent_frame
        self.sequence_path = None

        self.setup_signals()

    def setup_signals(self):
        """
        Connect most UI elements to the set_sequence function which handles updating the FRAGSequencer node.

        """
        self.ui.sequence_start_frame_lineEdit.editingFinished.connect(self.set_sequence)
        self.ui.min_frame_pushButton.clicked.connect(lambda: self.set_current_frame(self.ui.sequence_start_frame_lineEdit))
        self.ui.sequence_end_frame_lineEdit.editingFinished.connect(self.set_sequence)
        self.ui.max_frame_pushButton.clicked.connect(lambda: self.set_current_frame(self.ui.sequence_end_frame_lineEdit))

        self.ui.remove_sequence_pushButton.clicked.connect(self.remove_sequence)
        self.ui.browse_path_pushButton.clicked.connect(self._find_file)

        self.ui.move_up_pushButton.clicked.connect(lambda: self.move_sequence(positive_move=True))
        self.ui.move_down_pushButton.clicked.connect(lambda: self.move_sequence(positive_move=False))

        self.ui.root_to_origin_checkBox.clicked.connect(self.set_sequence)
        self.ui.start_to_zero_checkBox.clicked.connect(self.set_sequence)

        self.ui.sequence_export_path_lineEdit.editingFinished.connect(self.set_sequence)
        self.ui.sequence_name_lineEdit.editingFinished.connect(self._update_path)
        self.ui.sequence_notes_lineEdit.editingFinished.connect(self.set_sequence)

        self.ui.export_sequence_pushButton.clicked.connect(self.export_sequence)

        self.ui.set_timeline_pushButton.setIcon(QtGui.QIcon(":adjustTimeline.png"))
        self.ui.set_timeline_pushButton.clicked.connect(self.set_frame_range)
        self.ui.play_range_pushButton.setIcon(QtGui.QIcon(":playClip.png"))
        self.ui.play_range_pushButton.clicked.connect(self.play_frame_range)
        self.ui.playblast_sequence_pushButton.setIcon(QtGui.QIcon(":playblast.png"))
        self.ui.playblast_sequence_pushButton.clicked.connect(self.playblast_frame_range)


    def _update_path(self):
        """
        When the name field is updated if the path field is empty automatically propagate the expected path.

        """
        new_name = self.ui.sequence_name_lineEdit.text()
        if self.ui.sequence_export_path_lineEdit.text() or not new_name:
            return

        mca_asset = assetlist.get_asset_by_id(self.frag_rig.get_asset_id(self.frag_rig))
        animation_path = None
        if mca_asset:
            animation_path = path_utils.to_relative_path(mca_asset.animations_path)

        if animation_path:
            # Only update the UI and FRAG Sequencer if we had a valid path resolution.
            self.set_sequence(os.path.join(animation_path, f'{new_name}.fbx'))

    def _find_file(self):
        """
        Open the file browser to look for where this animation should be exported to.

        """
        # Use the current path or our option var path if the current path is empty.
        start_path = path_utils.to_full_path(self.ui.sequence_export_path_lineEdit.text())
        start_path = os.path.split(start_path)[0] if start_path else ANIMATIONEXPORTER_OPTION_VARS.MCALastAnimationPath

        found_path_list, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Select Animation', start_path, 'animation (*.fbx)')
        if not found_path_list:
            return

        found_sequence_path = path_utils.to_relative_path(found_path_list)
        self.set_sequence(found_sequence_path)

    def _get_frame_range(self):
        """
        Since the frame range line edits are string boxes fixup the values that are input and adjust them if necessary.
        Use the scene default time ranges if we're unsure.

        return: The start and end frame that is supplied by either the UI or best guess of the scene range.
        rtype: list[int, int]
        """
        frame_range = []
        for frame_element in [self.ui.sequence_start_frame_lineEdit, self.ui.sequence_end_frame_lineEdit]:
            frame_val = frame_element.text()
            frame_val = re.sub('[^-0-9]', '', frame_val)
            if frame_val == '':
                frame_val = None
            else:
                frame_val = int(frame_val)
            frame_range.append(frame_val)

        if None in frame_range:
            frame_range = time_utils.get_times()
            frame_range = [pm.currentTime(), frame_range[-1]]
        for frame_element, frame_val in zip([self.ui.sequence_start_frame_lineEdit, self.ui.sequence_end_frame_lineEdit], frame_range):
            # Don't run cycles of this as we reset the cleaned up value.
            frame_element.blockSignals(True)
            frame_element.setText(str(int(frame_val)))
            frame_element.blockSignals(False)
        return frame_range

    def remove_sequence(self):
        """
        Remove the sequence from the FRAG Sequencer, the UI and close this instance of a sequence.

        """
        self.ui.close()
        self.deleteLater()
        self.parent_frame.remove_frame()

        sequence_path = self.ui.sequence_export_path_lineEdit.text()
        ae_utils.remove_sequence(sequence_path, self.frag_rig)

        global SEQUENCE_PATH_DICT
        SEQUENCE_PATH_DICT.pop(self.sequence_path, None)

    @ma_decorators.keep_current_frame_decorator
    def set_sequence(self, found_sequence_path=None):
        """
        Register an update to this sequence UI to the FRAG Sequencer.

        :param str found_sequence_path: The relative path to a fbx file that this sequence represents.
        """
        if not self.frag_rig.pynode.exists():
            logger.warning('Refresh the main UI, The FRAG Rig associated with this sequence has been lost.')
            return

        found_sequence_path = found_sequence_path if isinstance(found_sequence_path, str) and found_sequence_path else path_utils.to_relative_path(self.ui.sequence_export_path_lineEdit.text())
        if not found_sequence_path:
            return
        global SEQUENCE_PATH_DICT

        if found_sequence_path in SEQUENCE_PATH_DICT and SEQUENCE_PATH_DICT[found_sequence_path] != self:
            logger.warning('This sequence is already registered. Select a unique animation path.')
            return

        # If we were passed a sequence path reset the UI textfield after verifying the path is valid for this sequence.
        self.ui.sequence_export_path_lineEdit.setText(found_sequence_path)
        if not found_sequence_path.lower().endswith('.fbx'):
            self.ui.sequence_export_path_lineEdit.setStyleSheet("""QLineEdit { background-color: darkred }""")
        else:
            self.ui.sequence_export_path_lineEdit.setStyleSheet("""QLineEdit { background-color: None }""")

        ANIMATIONEXPORTER_OPTION_VARS.MCALastAnimationPath = os.path.dirname(found_sequence_path)
        SEQUENCE_PATH_DICT[found_sequence_path] = self

        if self.sequence_path != found_sequence_path:
            ae_utils.remove_sequence(self.sequence_path, self.frag_rig)
            SEQUENCE_PATH_DICT.pop(self.sequence_path, None)

        frame_range = self._get_frame_range()
        ae_utils.set_sequence(found_sequence_path, self.frag_rig, frame_range=frame_range,
                              start_at_zero=self.ui.start_to_zero_checkBox.isChecked(),
                              root_to_origin=self.ui.root_to_origin_checkBox.isChecked(),
                              sequence_notes=self.ui.sequence_notes_lineEdit.text())

        self.sequence_path = path_utils.to_relative_path(self.ui.sequence_export_path_lineEdit.text())
        anim_name = os.path.basename(self.sequence_path.replace('.fbx', ''))
        self.ui.sequence_name_lineEdit.setText(anim_name)
        if self.parent_frame:
            self.parent_frame.tool_button.setText(anim_name)

    @decorators.track_fnc
    def set_current_frame(self, ui_element):
        """
        Sets the current frame to either the min or max frame fields.

        :param ui_element: The lineEdit to be updated with the current frame number.
        """
        current_frame = pm.currentTime()
        ui_element.setText(str(int(current_frame)))
        self.set_sequence()

    @decorators.track_fnc
    def export_sequence(self):
        """
        Export only this sequence.

        """
        # Create a filter list of other animations assigned to this rig and exclude them before running an export for
        # this sequence.
        rig_sequences = ae_utils.get_sequences()
        if not pm.objExists(self.frag_rig):
            logger.warning('Refresh the main UI, The FRAG Rig associated with this sequence has been lost.')
            messages.info_message('Export Failure', 'One or more frag rigs were unable to be located in the scene. Please ensure that the rig exists in the scene.', icon='error')
            return
        ae_utils.export_frag_sequences_cmd(frag_rig_list=[self.frag_rig], sequences_to_skip=[x for x in rig_sequences[self.frag_rig] if x != self.sequence_path])

    @decorators.track_fnc
    def move_sequence(self, positive_move=True):
        """
        Reorder the animation in the UI by adjusting the ui_index value.

        :param bool positive_move: If the animation should be moved up or down on the list.
        """
        if ae_utils.reorder_sequence(self.sequence_path, self.frag_rig, positive_move):
            self.parent_frame.main_ui.initialize_tabs()

    @decorators.track_fnc
    def set_frame_range(self):
        """
        Set the active frame range in mya to match this sequence.

        """
        frame_range = self._get_frame_range()
        time_utils.set_timeline_range(frame_range[0], frame_range[-1])
        pm.currentTime(frame_range[0])

    @decorators.track_fnc
    def play_frame_range(self):
        """
        Set the active frame range in mya to match this sequence. Then play that frame range.

        """

        current_state = pm.play(q=True, state=True)
        if pm.playbackOptions(query=True, animationStartTime=True) != float(self._get_frame_range()[0]):
            current_state = False

        self.set_frame_range()
        pm.play(state=not current_state)

    @decorators.track_fnc
    def playblast_frame_range(self):
        start_frame, end_frame = self._get_frame_range()

        #playblast.create_playblast(file_name=self.ui.sequence_name_lineEdit.text(), start_frame=start_frame, end_frame=end_frame)
