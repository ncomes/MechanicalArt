#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Categorized and edits rotation orders of flags.
"""

# System global imports
import os

# Software specific imports
import pymel.core as pm
import maya.cmds as cmds

# PySide2 imports
from PySide2.QtWidgets import QMenu, QAction
from PySide2.QtCore import Qt, QModelIndex

# mca python imports
from mca.common import log
from mca.common.paths import paths
from mca.common.textio import jsonio
from mca.common.utils import fileio
from mca.common.pyqt import messages
from mca.mya.utils import optionvars, namespace
from mca.mya.pyqt import dialogs, mayawindows
from mca.mya.rigging import frag

logger = log.MCA_LOGGER

FLAG_ROTATION_PRESETS = os.path.join(paths.get_common_tools_path(), 'Common\\Rigging\\Flag Rotation Presets\\')

class MCARigRotationsOptionVars(optionvars.MCAOptionVars):
    """
    Tracks the last used rig preset.
    """

    MCALastPreset = {'default_value': '', 'docstring': 'Last preset selected.'}

class FlagRotationOrderEditor(mayawindows.MCAMayaWindow):
    VERSION = '1.0.2'
    
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'flagrotationordereditor_ui.ui')
        super().__init__(title='Flag RotationOrder Editor',
                         ui_path=ui_path,
                         version=FlagRotationOrderEditor.VERSION)

        self.optionvars = MCARigRotationsOptionVars()
        self.setup_signals()
        self.setup_preset_comboBox()

        self.rig_namespace = ''

        # clears selections in any of the other widgets.
        self.ui.xyz_listWidget.itemPressed.connect(self.xyz_clear_selections)
        self.ui.yzx_listWidget.itemPressed.connect(self.yzx_clear_selections)
        self.ui.zxy_listWidget.itemPressed.connect(self.zxy_clear_selections)
        self.ui.xzy_listWidget.itemPressed.connect(self.xzy_clear_selections)
        self.ui.yxz_listWidget.itemPressed.connect(self.yxz_clear_selections)
        self.ui.zyx_listWidget.itemPressed.connect(self.zyx_clear_selections)

    def setup_signals(self):
        """
        Setting up signals.
        """

        self.ui.loadrig_pushButton.clicked.connect(self.loadrig_clicked)

        self.ui.preset_comboBox.currentIndexChanged.connect(self._preset_changed)

        self.ui.apply_preset_pushButton.clicked.connect(self.applypreset_clicked)
        self.ui.apply_rotations_pushButton.clicked.connect(self.apply_rotations)
        self.ui.save_preset_pushButton.clicked.connect(self.save_preset_clicked)
        self.ui.add_preset_pushButton.clicked.connect(self.add_preset_clicked)

        self.ui.edit_preset_frame.hide()
        self.ui.edit_preset_pushButton.clicked.connect(self.preset_edit_ui)
        self.ui.cancel_edit_pushButton.clicked.connect(self.default_ui)
        self.ui.add_flag_pushButton.clicked.connect(self.add_flag_clicked)
        self.ui.remove_flag_pushButton.clicked.connect(self.remove_flags_clicked)
        self.ui.save_full_preset_pushButton.clicked.connect(self.save_overwrite_preset)

        # left click menu pull up for each widget.
        self.ui.xyz_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.xyz_listWidget.customContextMenuRequested.connect(self.xyz_context_menu)
        self.ui.yzx_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.yzx_listWidget.customContextMenuRequested.connect(self.yzx_context_menu)
        self.ui.zxy_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.zxy_listWidget.customContextMenuRequested.connect(self.zxy_context_menu)
        self.ui.xzy_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.xzy_listWidget.customContextMenuRequested.connect(self.xzy_context_menu)
        self.ui.yxz_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.yxz_listWidget.customContextMenuRequested.connect(self.yxz_context_menu)
        self.ui.zyx_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.zyx_listWidget.customContextMenuRequested.connect(self.zyx_context_menu)

    def get_preset_names(self):
        """
        Grabs the names of the preset files from the Flag Rotation Presets folder.
        """

        if os.path.exists(FLAG_ROTATION_PRESETS):
            preset_names = [x for x in os.listdir(FLAG_ROTATION_PRESETS)]
            preset_names = [file.split('.', 1)[0] for file in preset_names]

            return preset_names

    def setup_preset_comboBox(self):
        """
        Takes names of the preset files and adds them to the combo box.
        """

        self.ui.preset_comboBox.blockSignals(True)

        preset_names = self.get_preset_names()
        if preset_names:
            self.ui.preset_comboBox.clear()
            self.ui.preset_comboBox.addItems(preset_names)

        self.ui.preset_comboBox.setCurrentText(self.optionvars.MCALastPreset)
        self.ui.preset_comboBox.blockSignals(False)

    def _preset_changed(self):
        """
        Logs current preset.
        """

        self.optionvars.MCALastPreset = self.ui.preset_comboBox.currentText()

    def default_ui(self):
        """
        Reload the default UI.
        """

        self.clear_list_widgets()

        self.ui.loadrig_frame.show()
        self.ui.preset_frame.show()
        self.ui.apply_rotations_frame.show()
        self.ui.edit_preset_frame.hide()

    def preset_edit_ui(self):
        """
        Loads the UI for editing preset files.
        """

        self.clear_list_widgets()

        self.ui.loadrig_frame.hide()
        self.ui.preset_frame.hide()
        self.ui.apply_rotations_frame.hide()
        self.ui.edit_preset_frame.show()

        preset_name = self.ui.preset_comboBox.currentText()
        self.ui.current_preset_label.setText(preset_name)

        self.setup_preset_edit()

    def clear_list_widgets(self):
        """
        Removes all items from the list widgets.
        """

        self.ui.xyz_listWidget.clear()
        self.ui.yzx_listWidget.clear()
        self.ui.zxy_listWidget.clear()
        self.ui.xzy_listWidget.clear()
        self.ui.yxz_listWidget.clear()
        self.ui.zyx_listWidget.clear()

    def xyz_clear_selections(self):
        """
        Clears selection in all list widgets but xyz.
        """

        self.ui.yzx_listWidget.clearSelection()
        self.ui.zxy_listWidget.clearSelection()
        self.ui.xzy_listWidget.clearSelection()
        self.ui.yxz_listWidget.clearSelection()
        self.ui.zyx_listWidget.clearSelection()

    def yzx_clear_selections(self):
        """
        Clears selection in all list widgets but yzx.
        """

        self.ui.xyz_listWidget.clearSelection()
        self.ui.zxy_listWidget.clearSelection()
        self.ui.xzy_listWidget.clearSelection()
        self.ui.yxz_listWidget.clearSelection()
        self.ui.zyx_listWidget.clearSelection()

    def zxy_clear_selections(self):
        """
        Clears selection in all list widgets but zxy.
        """

        self.ui.xyz_listWidget.clearSelection()
        self.ui.yzx_listWidget.clearSelection()
        self.ui.xzy_listWidget.clearSelection()
        self.ui.yxz_listWidget.clearSelection()
        self.ui.zyx_listWidget.clearSelection()

    def xzy_clear_selections(self):
        """
        Clears selection in all list widgets but xzy.
        """

        self.ui.xyz_listWidget.clearSelection()
        self.ui.yzx_listWidget.clearSelection()
        self.ui.zxy_listWidget.clearSelection()
        self.ui.yxz_listWidget.clearSelection()
        self.ui.zyx_listWidget.clearSelection()

    def yxz_clear_selections(self):
        """
        Clears selection in all list widgets but yxz.
        """

        self.ui.xyz_listWidget.clearSelection()
        self.ui.yzx_listWidget.clearSelection()
        self.ui.zxy_listWidget.clearSelection()
        self.ui.xzy_listWidget.clearSelection()
        self.ui.zyx_listWidget.clearSelection()

    def zyx_clear_selections(self):
        """
        Clears selection in all list widgets but zyx.
        """

        self.ui.xyz_listWidget.clearSelection()
        self.ui.yzx_listWidget.clearSelection()
        self.ui.zxy_listWidget.clearSelection()
        self.ui.xzy_listWidget.clearSelection()
        self.ui.yxz_listWidget.clearSelection()

    def loadrig_clicked(self):
        """
        Gets rig from selection and sorts flags into list widgets.
        """

        selection = pm.selected()
        if not selection:
            messages.info_message('Selection Error', 'Please select a flag on the rig')
            return

        self.clear_list_widgets()

        selection_str = cmds.ls(sl=True)
        self.rig_namespace = namespace.get_namespace(selection_str[0], False) + ':'

        for x in selection:
            frag_rig = frag.get_frag_rig(x)
        all_flags_raw = frag_rig.get_flags()
        all_flags_ns = [x.node.name() for x in all_flags_raw]

        xyz = []
        yzx = []
        zxy = []
        xzy = []
        yxz = []
        zyx = []

        for x in all_flags_ns:
            attr = cmds.getAttr(x + '.rotateOrder')
            if attr == 0:
                xyz.append(x)
            elif attr == 1:
                yzx.append(x)
            elif attr == 2:
                zxy.append(x)
            elif attr == 3:
                xzy.append(x)
            elif attr == 4:
                yxz.append(x)
            elif attr == 5:
                zyx.append(x)
            else:
                xyz.append(x)

        # strip namespace from flags.
        modify_groups = [xyz, yzx, zxy, xzy, yxz, zyx]
        for widget in modify_groups:
            for flag in range(len(widget)):
                widget[flag] = widget[flag].replace(self.rig_namespace, '')

        self.ui.xyz_listWidget.addItems(xyz)
        self.ui.yzx_listWidget.addItems(yzx)
        self.ui.zxy_listWidget.addItems(zxy)
        self.ui.xzy_listWidget.addItems(xzy)
        self.ui.yxz_listWidget.addItems(yxz)
        self.ui.zyx_listWidget.addItems(zyx)

    def excluded_flags(self, rig_flags, preset_flags, all_flags, all_preset_flags):
        """
        This function takes flags from the widget and sees if they are new or not. If new, they
        are left in the widget group. If not, they are removed so they can be placed in the
        correct widget according to the preset.

        :param str rig_flags: flags currently in the widget group.
        :param str preset_flags: flags meant to be in the widget group according to preset.
        :param str all_flags: all flags in the rig.
        :param str all_preset_flags: all flags in the preset.
        :return: list of flags that will be put into the widget group.
        """

        final_list = []

        # check if preset flags exist on the rig.
        # valid flags that will go into the widget.
        preset_flags = [item for item in preset_flags if item in all_flags]
        final_list += preset_flags

        # get flags that are new and add them to the final list.
        final_list += [item for item in rig_flags if item not in all_preset_flags]

        return final_list

    def unpack_preset_file(self, preset_folder, preset_name):
        """
        Takes dictionary from preset file and sorts it into lists according to rotation.

        :param str preset_folder: file path to preset folder.
        :param str preset_name: name of the preset from combobox.
        :return: lists of each rotation order.
        """

        file_path = os.path.join(preset_folder, f'{preset_name}.json')
        fileio.touch_path(file_path)

        preset_dic = jsonio.read_json_file(file_path)

        xyz = []
        yzx = []
        zxy = []
        xzy = []
        yxz = []
        zyx = []

        for key, value in preset_dic.items():
            if value == 0:
                xyz.append(key)
            elif value == 1:
                yzx.append(key)
            elif value == 2:
                zxy.append(key)
            elif value == 3:
                xzy.append(key)
            elif value == 4:
                yxz.append(key)
            elif value == 5:
                zyx.append(key)

        return xyz, yzx, zxy, xzy, yxz, zyx

    def applypreset_clicked(self):
        """
        Sorts the loaded flags according to a preset.
        """

        rig_xyz, rig_yzx, rig_zxy, rig_xzy, rig_yxz, rig_zyx = self.get_all_widget_flags()

        # grabs the flags from the preset file.
        current_preset_name = self.ui.preset_comboBox.currentText()
        xyz, yzx, zxy, xzy, yxz, zyx = self.unpack_preset_file(FLAG_ROTATION_PRESETS, current_preset_name)

        modify_widgets = [xyz, yzx, zxy, xzy, yxz, zyx,
                          rig_xyz, rig_yzx, rig_zxy, rig_xzy, rig_yxz, rig_zyx]

        # Adds namespaces to the flags in preset and widget.
        for widget in modify_widgets:
            for flag in range(len(widget)):
                widget[flag] = self.rig_namespace + widget[flag]

        all_rig_flags = rig_xyz + rig_yzx + rig_zxy + rig_xzy + rig_yxz + rig_zyx
        all_preset_flags = xyz + yzx + zxy + xzy + yxz + zyx

        # checks if rig has flags not in the preset and adds them.
        # TODO (maybe): Make a check to let user know there's flags not saved in the preset.
        xyz = self.excluded_flags(rig_xyz, xyz, all_rig_flags, all_preset_flags)
        yzx = self.excluded_flags(rig_yzx, yzx, all_rig_flags, all_preset_flags)
        zxy = self.excluded_flags(rig_zxy, zxy, all_rig_flags, all_preset_flags)
        xzy = self.excluded_flags(rig_xzy, xzy, all_rig_flags, all_preset_flags)
        yxz = self.excluded_flags(rig_yxz, yxz, all_rig_flags, all_preset_flags)
        zyx = self.excluded_flags(rig_zyx, zyx, all_rig_flags, all_preset_flags)

        # strip namespace from flags.
        modify_groups = [xyz, yzx, zxy, xzy, yxz, zyx]
        for widget in modify_groups:
            for flag in range(len(widget)):
                widget[flag] = widget[flag].replace(self.rig_namespace, '')

        self.clear_list_widgets()

        self.ui.xyz_listWidget.addItems(xyz)
        self.ui.yzx_listWidget.addItems(yzx)
        self.ui.zxy_listWidget.addItems(zxy)
        self.ui.xzy_listWidget.addItems(xzy)
        self.ui.yxz_listWidget.addItems(yxz)
        self.ui.zyx_listWidget.addItems(zyx)

    def get_all_widget_flags(self):
        """
        Goes through each list widget and grabs names of all flags.
        :return: list of all flags in a widget.
        """

        xyz = [self.ui.xyz_listWidget.item(i).text()
               for i in range(self.ui.xyz_listWidget.count())]
        yzx = [self.ui.yzx_listWidget.item(i).text()
               for i in range(self.ui.yzx_listWidget.count())]
        zxy = [self.ui.zxy_listWidget.item(i).text()
               for i in range(self.ui.zxy_listWidget.count())]
        xzy = [self.ui.xzy_listWidget.item(i).text()
               for i in range(self.ui.xzy_listWidget.count())]
        yxz = [self.ui.yxz_listWidget.item(i).text()
               for i in range(self.ui.yxz_listWidget.count())]
        zyx = [self.ui.zyx_listWidget.item(i).text()
               for i in range(self.ui.zyx_listWidget.count())]

        return xyz, yzx, zxy, xzy, yxz, zyx

    def apply_rotations(self):
        """
        Applies rotations according to the list widgets.
        """

        xyz, yzx, zxy, xzy, yxz, zyx = self.get_all_widget_flags()

        rotateString = '.rotateOrder'

        for flag in xyz:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 0)

        for flag in yzx:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 1)

        for flag in zxy:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 2)

        for flag in xzy:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 3)

        for flag in yxz:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 4)

        for flag in zyx:
            flagName = f'{self.rig_namespace}{flag}{rotateString}'
            pm.setAttr(flagName, 5)

        messages.info_message('Rotations applied!', 'Rotations have been applied to the flags.')

    def add_preset_clicked(self):
        """
        Adds a new preset name to the combo box.
        """

        preset_names = self.get_preset_names()

        new_preset_name = messages.text_prompt_message('New preset name:', 'Please enter a new name for the preset.')
        if new_preset_name and new_preset_name != '':
            new_preset_name = new_preset_name.lower()
            if ' ' in new_preset_name:
                new_preset_name = new_preset_name.replace(' ', '_')

            if new_preset_name not in preset_names:
                # TODO (maybe): Have the save_preset button clear asterisk when changed to a different preset.
                # TODO (maybe): If there's a new preset that isn't saved, alert the user when they click any buttons.

                file_path = os.path.join(FLAG_ROTATION_PRESETS, f'{new_preset_name}.json')
                preset_dic = {}
                jsonio.write_to_json_file(preset_dic, file_path)

                self.setup_preset_comboBox()
                # self.ui.save_preset_pushButton.setText('Save Preset Changes*')
                self.ui.preset_comboBox.setCurrentText(new_preset_name)

            else:
                messages.error_message('Error!', 'Entered name is already in use, please choose a different name.')

    def compile_flag_dic(self, namespace=False):
        """
        Saves the currently selected preset. New flags are added onto the file.
        """

        xyz, yzx, zxy, xzy, yxz, zyx = self.get_all_widget_flags()

        if namespace == True:
            namesp_len = len(self.rig_namespace)

            xyz = [item[namesp_len:] for item in xyz]
            yzx = [item[namesp_len:] for item in yzx]
            zxy = [item[namesp_len:] for item in zxy]
            xzy = [item[namesp_len:] for item in xzy]
            yxz = [item[namesp_len:] for item in yxz]
            zyx = [item[namesp_len:] for item in zyx]

        xyz_dic = {}
        yzx_dic = {}
        zxy_dic = {}
        xzy_dic = {}
        yxz_dic = {}
        zyx_dic = {}

        preset_dic = {}

        for flag in xyz:
            xyz_dic.update({flag: 0})
        for flag in yzx:
            yzx_dic.update({flag: 1})
        for flag in zxy:
            zxy_dic.update({flag: 2})
        for flag in xzy:
            xzy_dic.update({flag: 3})
        for flag in yxz:
            yxz_dic.update({flag: 4})
        for flag in zyx:
            zyx_dic.update({flag: 5})

        if xyz_dic:
            preset_dic.update(xyz_dic)
        if yzx_dic:
            preset_dic.update(yzx_dic)
        if zxy_dic:
            preset_dic.update(zxy_dic)
        if xzy_dic:
            preset_dic.update(xzy_dic)
        if yxz_dic:
            preset_dic.update(yxz_dic)
        if zyx_dic:
            preset_dic.update(zyx_dic)

        return preset_dic

    def save_preset_clicked(self):
        """
        Saves preset flags to respective json file.
        """

        # TODO (maybe): prevent new flags from being added to the json file.
        #               Will look into this later to see what we need from this tool.

        result = dialogs.question_prompt(title='Save Preset',
                                         text='Are you want to save these changes?')
        if result != 'Yes':
            return

        preset_dic = self.compile_flag_dic()

        # gets the json file path.
        filename = self.ui.preset_comboBox.currentText()
        file_path = os.path.join(FLAG_ROTATION_PRESETS, f'{filename}.json')
        fileio.touch_path(file_path)

        original_preset_dic = jsonio.read_json_file(file_path)
        original_preset_dic.update(preset_dic)

        jsonio.write_to_json_file(original_preset_dic, file_path)

    def setup_preset_edit(self):
        """
        Grabs the flags from the preset file
        """

        current_preset_name = self.ui.preset_comboBox.currentText()
        xyz, yzx, zxy, xzy, yxz, zyx = self.unpack_preset_file(FLAG_ROTATION_PRESETS, current_preset_name)

        self.ui.xyz_listWidget.addItems(xyz)
        self.ui.yzx_listWidget.addItems(yzx)
        self.ui.zxy_listWidget.addItems(zxy)
        self.ui.xzy_listWidget.addItems(xzy)
        self.ui.yxz_listWidget.addItems(yxz)
        self.ui.zyx_listWidget.addItems(zyx)

    def add_flag_clicked(self):
        """
        Function that adds a new flag.
        """

        # TODO: comes back to this later to allow user to dictate where the new flag will go.
        #       add option of adding multiple flags.
        xyz, yzx, zxy, xzy, yxz, zyx = self.get_all_widget_flags()
        current_flags = xyz + yzx + zxy + xzy + yxz + zyx

        # creating a list variable here might be redundant, clean up later.
        new_flag_grp = []
        new_flag = messages.text_prompt_message('New flag name:', 'Please enter a new flag for the preset.', 'f_')
        new_flag_grp.append(new_flag)

        if new_flag and new_flag != '':
            for flag in new_flag_grp:
                if flag in current_flags:
                    messages.error_message('Error!', 'This flag already exists! Please enter a new name.')
                else:
                    add_flag = [flag]
                    self.ui.xyz_listWidget.addItems(add_flag)

    def remove_flags_clicked(self):
        """
        Function that removes selected flag(s).
        """

        result = dialogs.question_prompt(title='Delete Flags',
                                         text='Are you sure you want to delete the selected flags?')
        if result != 'Yes':
            return

        xyz_selected = self.ui.xyz_listWidget.selectedIndexes()
        yzx_selected = self.ui.yzx_listWidget.selectedIndexes()
        zxy_selected = self.ui.zxy_listWidget.selectedIndexes()
        xzy_selected = self.ui.xzy_listWidget.selectedIndexes()
        yxz_selected = self.ui.yxz_listWidget.selectedIndexes()
        zyx_selected = self.ui.zyx_listWidget.selectedIndexes()

        if xyz_selected:
            for item in reversed(xyz_selected):
                selected_index = QModelIndex.row(item)
                self.ui.xyz_listWidget.takeItem(selected_index)

        if yzx_selected:
            for item in reversed(yzx_selected):
                selected_index = QModelIndex.row(item)
                self.ui.yzx_listWidget.takeItem(selected_index)

        if zxy_selected:
            for item in reversed(zxy_selected):
                selected_index = QModelIndex.row(item)
                self.ui.zxy_listWidget.takeItem(selected_index)

        if xzy_selected:
            for item in reversed(xzy_selected):
                selected_index = QModelIndex.row(item)
                self.ui.xzy_listWidget.takeItem(selected_index)

        if yxz_selected:
            for item in reversed(yxz_selected):
                selected_index = QModelIndex.row(item)
                self.ui.yxz_listWidget.takeItem(selected_index)

        if zyx_selected:
            for item in reversed(zyx_selected):
                selected_index = QModelIndex.row(item)
                self.ui.zyx_listWidget.takeItem(selected_index)

    def save_overwrite_preset(self):
        """
        Saves preset json file. This one overwrites the entire file.
        """

        result = dialogs.question_prompt(title='Save Preset',
                                         text='Are you want to save these changes? (the preset will be overwritten)')
        if result != 'Yes':
            return

        preset_dic = self.compile_flag_dic(namespace=False)

        # gets the json file path.
        filename = self.ui.preset_comboBox.currentText()
        file_path = os.path.join(FLAG_ROTATION_PRESETS, f'{filename}.json')
        fileio.touch_path(file_path)

        jsonio.write_to_json_file(preset_dic, file_path)

        self.default_ui()

    def xyz_context_menu(self, position):
        """
        Creates context menu for the xyz list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.xyz_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_yzx_action = QAction('move -> yzx', self)
            move_yzx_action.triggered.connect(lambda: self.move_xyz_flags(1))
            actions.append(move_yzx_action)

            move_zxy_action = QAction('move -> zxy', self)
            move_zxy_action.triggered.connect(lambda: self.move_xyz_flags(2))
            actions.append(move_zxy_action)

            move_xzy_action = QAction('move -> xzy', self)
            move_xzy_action.triggered.connect(lambda: self.move_xyz_flags(3))
            actions.append(move_xzy_action)

            move_yxz_action = QAction('move -> yxz', self)
            move_yxz_action.triggered.connect(lambda: self.move_xyz_flags(4))
            actions.append(move_yxz_action)

            move_zyx_action = QAction('move -> zyx', self)
            move_zyx_action.triggered.connect(lambda: self.move_xyz_flags(5))
            actions.append(move_zyx_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.xyz_listWidget.mapToGlobal(position))

    def move_xyz_flags(self, widget):
        """
        Moves selected flags from xyz widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.xyz_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.xyz_listWidget.takeItem(current_row)

            if widget == 1:
                self.ui.yzx_listWidget.addItem(taken_item)
            elif widget == 2:
                self.ui.zxy_listWidget.addItem(taken_item)
            elif widget == 3:
                self.ui.xzy_listWidget.addItem(taken_item)
            elif widget == 4:
                self.ui.yxz_listWidget.addItem(taken_item)
            elif widget == 5:
                self.ui.zyx_listWidget.addItem(taken_item)

        self.ui.xyz_listWidget.clearSelection()

    def yzx_context_menu(self, position):
        """
        Creates context menu for the yzx list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.yzx_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_xyz_action = QAction('move <- xyz', self)
            move_xyz_action.triggered.connect(lambda: self.move_yzx_flags(0))
            actions.append(move_xyz_action)

            move_zxy_action = QAction('move -> zxy', self)
            move_zxy_action.triggered.connect(lambda: self.move_yzx_flags(2))
            actions.append(move_zxy_action)

            move_xzy_action = QAction('move -> xzy', self)
            move_xzy_action.triggered.connect(lambda: self.move_yzx_flags(3))
            actions.append(move_xzy_action)

            move_yxz_action = QAction('move -> yxz', self)
            move_yxz_action.triggered.connect(lambda: self.move_yzx_flags(4))
            actions.append(move_yxz_action)

            move_zyx_action = QAction('move -> zyx', self)
            move_zyx_action.triggered.connect(lambda: self.move_yzx_flags(5))
            actions.append(move_zyx_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.xyz_listWidget.mapToGlobal(position))

    def move_yzx_flags(self, widget):
        """
        Moves selected flags from yzx widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.yzx_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.yzx_listWidget.takeItem(current_row)

            if widget == 0:
                self.ui.xyz_listWidget.addItem(taken_item)
            elif widget == 2:
                self.ui.zxy_listWidget.addItem(taken_item)
            elif widget == 3:
                self.ui.xzy_listWidget.addItem(taken_item)
            elif widget == 4:
                self.ui.yxz_listWidget.addItem(taken_item)
            elif widget == 5:
                self.ui.zyx_listWidget.addItem(taken_item)

        self.ui.yzx_listWidget.clearSelection()

    def zxy_context_menu(self, position):
        """
        Creates context menu for the zxy list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.zxy_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_xyz_action = QAction('move <- xyz', self)
            move_xyz_action.triggered.connect(lambda: self.move_zxy_flags(0))
            actions.append(move_xyz_action)

            move_yzx_action = QAction('move <- yzx', self)
            move_yzx_action.triggered.connect(lambda: self.move_zxy_flags(1))
            actions.append(move_yzx_action)

            move_xzy_action = QAction('move -> xzy', self)
            move_xzy_action.triggered.connect(lambda: self.move_zxy_flags(3))
            actions.append(move_xzy_action)

            move_yxz_action = QAction('move -> yxz', self)
            move_yxz_action.triggered.connect(lambda: self.move_zxy_flags(4))
            actions.append(move_yxz_action)

            move_zyx_action = QAction('move -> zyx', self)
            move_zyx_action.triggered.connect(lambda: self.move_zxy_flags(5))
            actions.append(move_zyx_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.zxy_listWidget.mapToGlobal(position))

    def move_zxy_flags(self, widget):
        """
        Moves selected flags from zxy widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.zxy_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.zxy_listWidget.takeItem(current_row)

            if widget == 0:
                self.ui.xyz_listWidget.addItem(taken_item)
            elif widget == 1:
                self.ui.yzx_listWidget.addItem(taken_item)
            elif widget == 3:
                self.ui.xzy_listWidget.addItem(taken_item)
            elif widget == 4:
                self.ui.yxz_listWidget.addItem(taken_item)
            elif widget == 5:
                self.ui.zyx_listWidget.addItem(taken_item)

        self.ui.zxy_listWidget.clearSelection()

    def xzy_context_menu(self, position):
        """
        Creates context menu for the xzy list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.xzy_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_xyz_action = QAction('move <- xyz', self)
            move_xyz_action.triggered.connect(lambda: self.move_xzy_flags(0))
            actions.append(move_xyz_action)

            move_yzx_action = QAction('move <- yzx', self)
            move_yzx_action.triggered.connect(lambda: self.move_xzy_flags(1))
            actions.append(move_yzx_action)

            move_zxy_action = QAction('move <- zxy', self)
            move_zxy_action.triggered.connect(lambda: self.move_xzy_flags(2))
            actions.append(move_zxy_action)

            move_yxz_action = QAction('move -> yxz', self)
            move_yxz_action.triggered.connect(lambda: self.move_xzy_flags(4))
            actions.append(move_yxz_action)

            move_zyx_action = QAction('move -> zyx', self)
            move_zyx_action.triggered.connect(lambda: self.move_xzy_flags(5))
            actions.append(move_zyx_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.xzy_listWidget.mapToGlobal(position))

    def move_xzy_flags(self, widget):
        """
        Moves selected flags from zxy widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.xzy_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.xzy_listWidget.takeItem(current_row)

            if widget == 0:
                self.ui.xyz_listWidget.addItem(taken_item)
            elif widget == 1:
                self.ui.yzx_listWidget.addItem(taken_item)
            elif widget == 2:
                self.ui.zxy_listWidget.addItem(taken_item)
            elif widget == 4:
                self.ui.yxz_listWidget.addItem(taken_item)
            elif widget == 5:
                self.ui.zyx_listWidget.addItem(taken_item)

        self.ui.xzy_listWidget.clearSelection()

    def yxz_context_menu(self, position):
        """
        Creates context menu for the yxz list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.yxz_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_xyz_action = QAction('move <- xyz', self)
            move_xyz_action.triggered.connect(lambda: self.move_yxz_flags(0))
            actions.append(move_xyz_action)

            move_yzx_action = QAction('move <- yzx', self)
            move_yzx_action.triggered.connect(lambda: self.move_yxz_flags(1))
            actions.append(move_yzx_action)

            move_zxy_action = QAction('move <- zxy', self)
            move_zxy_action.triggered.connect(lambda: self.move_yxz_flags(2))
            actions.append(move_zxy_action)

            move_xzy_action = QAction('move <- xzy', self)
            move_xzy_action.triggered.connect(lambda: self.move_yxz_flags(3))
            actions.append(move_xzy_action)

            move_zyx_action = QAction('move -> zyx', self)
            move_zyx_action.triggered.connect(lambda: self.move_yxz_flags(5))
            actions.append(move_zyx_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.yxz_listWidget.mapToGlobal(position))

    def move_yxz_flags(self, widget):
        """
        Moves selected flags from yxz widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.yxz_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.yxz_listWidget.takeItem(current_row)

            if widget == 0:
                self.ui.xyz_listWidget.addItem(taken_item)
            elif widget == 1:
                self.ui.yzx_listWidget.addItem(taken_item)
            elif widget == 2:
                self.ui.zxy_listWidget.addItem(taken_item)
            elif widget == 3:
                self.ui.xzy_listWidget.addItem(taken_item)
            elif widget == 5:
                self.ui.zyx_listWidget.addItem(taken_item)

        self.ui.yxz_listWidget.clearSelection()

    def zyx_context_menu(self, position):
        """
        Creates context menu for the zyx list widget.

        :param list(QPoint) position: Coordinates to show the context menu at.
        """

        current_item = self.ui.zyx_listWidget.itemAt(position)
        actions = []
        if current_item:
            move_xyz_action = QAction('move <- xyz', self)
            move_xyz_action.triggered.connect(lambda: self.move_zyx_flags(0))
            actions.append(move_xyz_action)

            move_yzx_action = QAction('move <- yzx', self)
            move_yzx_action.triggered.connect(lambda: self.move_zyx_flags(1))
            actions.append(move_yzx_action)

            move_zxy_action = QAction('move <- zxy', self)
            move_zxy_action.triggered.connect(lambda: self.move_zyx_flags(2))
            actions.append(move_zxy_action)

            move_xzy_action = QAction('move <- xzy', self)
            move_xzy_action.triggered.connect(lambda: self.move_zyx_flags(3))
            actions.append(move_xzy_action)

            move_yxz_action = QAction('move <- yxz', self)
            move_yxz_action.triggered.connect(lambda: self.move_zyx_flags(4))
            actions.append(move_yxz_action)

        else:
            pass

        menu = QMenu(self)
        list(map(lambda x: menu.addAction(x), actions))
        menu.exec_(self.ui.zyx_listWidget.mapToGlobal(position))

    def move_zyx_flags(self, widget):
        """
        Moves selected flags from zyx widget to selected widget.

        :param int widget: integer corresponding with target widget.
        """

        items_selected = self.ui.zyx_listWidget.selectedIndexes()
        for flag in reversed(items_selected):
            current_row = QModelIndex.row(flag)
            taken_item = self.ui.zyx_listWidget.takeItem(current_row)

            if widget == 0:
                self.ui.xyz_listWidget.addItem(taken_item)
            elif widget == 1:
                self.ui.yzx_listWidget.addItem(taken_item)
            elif widget == 2:
                self.ui.zxy_listWidget.addItem(taken_item)
            elif widget == 3:
                self.ui.xzy_listWidget.addItem(taken_item)
            elif widget == 4:
                self.ui.yxz_listWidget.addItem(taken_item)

        self.ui.zyx_listWidget.clearSelection()
