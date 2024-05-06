#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configurations for rig FK/IK and space switching options.
"""

# python imports
import os
from PySide2.QtWidgets import QLabel, QHBoxLayout, QComboBox, QPushButton, QScrollArea, QSizePolicy, QWidget
from PySide2.QtWidgets import QFrame, QVBoxLayout
from PySide2.QtCore import Qt

# software specific imports
import pymel.core as pm

# mca python imports
from mca.common import log
from mca.common.pyqt import messages
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import frag

logger = log.MCA_LOGGER

class RigSettings(mayawindows.MCAMayaWindow):
    VERSION = '1.1.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'rig_settings_ui.ui')
        super().__init__(title='RigSettings',
                         ui_path=ui_path,
                         version=RigSettings.VERSION)

        self.rig_namespace = ''
        self.container_layout = None
        self.flag_dict = {}

        self.setup_signals()
        self.initialize_scroll_widgets()

    def initialize_scroll_widgets(self):
        """
        Setting up scroll widget to place flags in later.
        """

        scroll_area = QScrollArea()
        scroll_area.setObjectName('MainScrollFrame')
        scroll_area.setFrameStyle(QFrame.Box | QFrame.Sunken)
        scroll_area.setContentsMargins(0, 0, 4, 0)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        self.ui.main_verticalLayout.addWidget(scroll_area)
        scroll_area_widget_contents = QWidget()
        scroll_area.setWidget(scroll_area_widget_contents)

        self.container_layout = QVBoxLayout(scroll_area_widget_contents)
        scroll_area_widget_contents.setLayout(self.container_layout)

    def setup_signals(self):
        """
        Setting up signals
        """

        self.ui.apply_pushButton.clicked.connect(self._apply_clicked)
        self.ui.loadRig_pushButton.clicked.connect(self.loadrig_clicked)

    def loadrig_clicked(self):
        """
        Goes through rig to find flags then add them to the scroll widget.
        """

        # This dictionary stores flag information to be used for the apply button later.
        self.flag_dict = {}

        # Checks if a flag is selected. Tool needs index specified but if not selected doesn't like that.
        selection_check = pm.selected()
        if not selection_check:
            messages.info_message('Selection Error', 'Please select a flag on the rig')
            return

        selection = pm.selected()[0]

        # Clears layout to load new rig flags
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

        # Rig information
        self.rig_namespace = selection.namespace()
        frag_rig = frag.get_frag_rig(selection)
        frag_rig_flags = frag_rig.get_flags()
        self.attr_flags = []

        # Goes through and gets flags with ik/fk and space switching
        for flag in frag_rig_flags:
            found_flag = pm.listAttr(flag, userDefined=True, keyable=True)
            if found_flag:
                if 'follow' in found_flag or 'rotateFollow' in found_flag or 'ikfk_switch' in found_flag:
                    self.attr_flags.append(flag)

        # Gets all components in the rig
        fragrig = frag.get_frag_rig(selection)
        components = frag.get_frag_node_descendants(fragrig)
        sorted_components_all = []

        # Gets components that have flags with ik/fk and space switching
        for component in components:
            flags = component.get_flags()
            for flag in flags:
                if flag in self.attr_flags:
                    sorted_components_all.append(component)

        # Removes duplicate components from list
        sorted_components = []
        [sorted_components.append(x) for x in sorted_components_all if x not in sorted_components]

        # Creates dictionary based on group names
        group_names_dict = {}
        for component in sorted_components:
            group = component.split('_')[-1]
            if group in group_names_dict:
                group_names_dict[group].append(component)
            else:
                group_names_dict[group] = [component]

        # Goes through each component and adds widget for flag, grouping it based on dict key.
        for key, value in group_names_dict.items():
            self._add_group_label(key)
            value_flags = self.check_flag_exists(value)
            self.create_flag_widgets(value_flags)
            self._add_horizontal_line()

    def check_flag_exists(self, components):
        """
        Sorts through flags in a group of components and checks if they exist on the rig.

        :param list components: List of components in a group.
        :return: valid flags that exist on the rig.
        """

        flag_box = []

        for component in components:
            all_flags = component.get_flags()
            for flag in all_flags:
                if flag in self.attr_flags:
                    flag_box.append(flag)

        return flag_box

    def _add_horizontal_line(self):
        """
        Adds a horizontal line divider to layout.
        """

        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        self.container_layout.addWidget(hline)

    def _add_group_label(self, name):
        """
        Adds a name label for a flag group.

        :param str name: Name of the label.
        """

        label = QLabel(name.capitalize())
        label_font = label.font()
        label_font.setBold(True)
        label.setFont(label_font)
        self.container_layout.addWidget(label)

    def create_flag_widgets(self, component_flags):
        """
        Creates widgets for each flag in a component group.

        :param list component_flags: List of flags in a component.
        """

        # Takes found flags, finds information, and sends it to be used to create a widget.
        for flag in component_flags:
            flag_attrs = pm.listAttr(flag, userDefined=True, keyable=True)
            ikfk_switch = False

            if 'follow' in flag_attrs:
                follow_enums = pm.attributeQuery('follow', n=flag, le=True)
                follow_enums = follow_enums[0].split(':')
                self.flag_dict[flag] = [follow_enums[0]]

            if 'rotateFollow' in flag_attrs:
                follow_enums = pm.attributeQuery('rotateFollow', n=flag, le=True)
                follow_enums = follow_enums[0].split(':')
                self.flag_dict[flag] = [follow_enums[0]]

            if 'ikfk_switch' in flag_attrs:
                ikfk_switch = True
                self.flag_dict[flag].append(0)

            # Takes info from if statements, creates a widget based on it, then adds it to the scroll layout
            flagoption = FlagOptionWidget(flag=flag, follow_enums=follow_enums, ikfk_switch=ikfk_switch,
                                          namespace=self.rig_namespace, parent=self.ui, parent_class=self)

            self.container_layout.addWidget(flagoption)

    def _apply_clicked(self):
        """
        Applies all space switching and IK FK options to the rig.
        """

        for key, value in self.flag_dict.items():
            flag_attr = pm.listAttr(key, userDefined=True, keyable=True)

            if 'ikfk_switch' in flag_attr:
                pm.setAttr(f'{key}.ikfk_switch', value[-1])

            if 'follow' in flag_attr:
                pm.setAttr(f'{key}.follow', value[0])

            if 'rotateFollow' in flag_attr:
                pm.setAttr(f'{key}.rotateFollow', value[0])


class FlagOptionWidget(QWidget):
    def __init__(self, flag=None, follow_enums=None, ikfk_switch=False, namespace=None, parent=None, parent_class=None):
        super().__init__(parent=parent)

        # Creates layout.
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 3, 3, 0)
        self.setLayout(self.main_layout)

        # Creates flag label.
        self.flag_label = QLabel()
        self.main_layout.addWidget(self.flag_label)

        # Creates combo box for ikfk_switch.
        self.ikfk_comboBox = QComboBox()
        self.ikfk_comboBox.setMaximumWidth(40)
        self.main_layout.addWidget(self.ikfk_comboBox)

        # Creates combo box for space switching.
        self.followenum_comboBox = QComboBox()
        self.followenum_comboBox.setMaximumWidth(100)
        self.main_layout.addWidget(self.followenum_comboBox)

        # Creates button to apply specific flag only.
        self.button = QPushButton('+')
        self.button.setMaximumHeight(20)
        self.button.setMaximumWidth(20)
        self.main_layout.addWidget(self.button)

        # Information about the flag
        self.flag = flag
        self.flag_short = flag.split(':')[-1]
        self.follow_enums = follow_enums
        self.ikfk_switch = ikfk_switch
        self.namespace = namespace
        self.parent_class = parent_class

        self.setup_ui(self.flag_short, self.ikfk_switch, self.follow_enums)
        self.setup_signals()
        self.show()

    def setup_ui(self, flag_short, ikfk_switch, follow_enums):
        """
        Sets up the UI for the widget.

        :param str flag_short: Flag name without namespace.
        :param bool ikfk_switch: If the flag has an IK FK switch.
        :param str follow_enums: List of space switching enums.
        """

        self.flag_label.setText(f'{flag_short} :')

        if ikfk_switch == True:
            self.ikfk_comboBox.addItems(['FK', 'IK'])
        elif ikfk_switch == False:
            self.ikfk_comboBox.hide()

        if follow_enums:
            self.followenum_comboBox.addItems(follow_enums)

    def setup_signals(self):
        """
        Connects buttons to functions.
        """

        self.button.clicked.connect(self.apply_single_option)

        # Changing values in the dictionary
        self.followenum_comboBox.currentIndexChanged.connect(self.followenum_combobox_changed)
        # TODO: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        self.ikfk_comboBox.currentIndexChanged.connect(self.ikfk_combobox_changed)

    def followenum_combobox_changed(self):
        """
        Changes dictionary value when space switching option is changed.
        """

        flag_list = self.parent_class.flag_dict[self.flag]
        flag_list[0] = self.followenum_comboBox.currentText()
        self.parent_class.flag_dict[self.flag] = flag_list

    def ikfk_combobox_changed(self):
        """
        Changes dictionary value when IK FK option is changed.
        """

        flag_list = self.parent_class.flag_dict[self.flag]
        flag_list[-1] = self.ikfk_comboBox.currentIndex()
        self.parent_class.flag_dict[self.flag] = flag_list

    def apply_single_option(self):
        """
        Applies settings to the single flag in this widget.
        """

        if self.ikfk_comboBox.isVisible():
            pm.setAttr(f'{self.flag}.ikfk_switch', self.ikfk_comboBox.currentIndex())

        # Checks if follow enum is follow or rotate follow.
        flag_attr = pm.listAttr(self.flag, userDefined=True, keyable=True)

        if 'follow' in flag_attr:
            pm.setAttr(f'{self.flag}.follow', self.followenum_comboBox.currentText())

        if 'rotateFollow' in flag_attr:
            pm.setAttr(f'{self.flag}.rotateFollow', self.followenum_comboBox.currentText())

