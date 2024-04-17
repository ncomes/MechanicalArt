#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox for streamlining pipeline.
"""
# python imports
import os
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QVBoxLayout, QSplitter, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QLabel
#from PySide2.QtGui import QSizePolicy
from PySide2.QtCore import Qt

# software specific imports
import maya.cmds as cmds
import pymel.core as pm

# mca python imports
from mca.common.resources import resources
from mca.common.pyqt import movies
from mca.mya.pyqt import dialogs, mayawindows
from mca.mya.utils import optionvars
from mca.mya.tools.helios import helios_ui
from mca.mya.tools.skeletonbuilder import skeletonbuilder_ui
# mca tool imports


class BuildAnAssetUi(mayawindows.MCAMayaWindow):
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'buildanasset.ui')
        super().__init__(title='Build An Asset', ui_path=None)

        self.setMinimumSize(800, 600)
        self.movies_path = resources.get_movies_path()

        # Header
        self.header_frame = QFrame()
        self.header_frame.setContentsMargins(0,0,0,0)
        self.header_frame.setMinimumHeight(60)
        self.header_frame.setMaximumHeight(60)
        self.main_layout.addWidget(self.header_frame)

        self.header_box = QHBoxLayout(self.header_frame)

        self.header_label = QLabel('Build An Asset')
        self.header_label.setMinimumWidth(150)
        self.header_box.addWidget(self.header_label)
        # Set header font styling
        self.header_label_font = self.header_label.font()
        self.header_label_font.setBold(True)
        self.header_label_font.setPointSize(16)
        self.header_label.setFont(self.header_label_font)

        wiz_gif = os.path.join(self.movies_path, 'ask_wizard_anim.gif')
        self.ask_wiz = movies.GifHoverToolButton(file_name=wiz_gif,
                                                    size=(50, 50),
                                                    parent=self)
        self.header_box.addWidget(self.ask_wiz)

        self.header_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.header_box.addItem(self.header_spacer)


        # Splitter
        self.tab_frame = QFrame()
        self.tab_frame.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.tab_frame)

        self.tab_main_layout = QHBoxLayout(self.tab_frame)

        self.splitter = QSplitter(self.tab_frame)
        self.splitter.setMinimumSize(800, 600)
        self.splitter.setStretchFactor(1,2)
        self.splitter.setOrientation(Qt.Horizontal)
        self.tab_main_layout.addWidget(self.splitter)

        self.tab_btn_frame = QFrame()
        self.tab_btn_frame.setMaximumSize(225, 600)
        self.tab_btn_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.tab_btn_frame.setContentsMargins(0, 0, 0, 0)
        self.tab_btn_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.tab_btn_layout = QVBoxLayout()
        self.tab_btn_frame.setLayout(self.tab_btn_layout)

        self.splitter_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.tab_main_layout.addItem(self.splitter_spacer)

        self.ui_body_frame = QFrame(self)
        self.ui_body_frame.setContentsMargins(3, 3, 3, 3)
        self.ui_body_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)

        self.splitter.addWidget(self.tab_btn_frame)
        self.splitter.addWidget(self.ui_body_frame)
        self.splitter.show()

        # Add Tab Buttons
        self.movies_path = resources.get_movies_path()
        model_button_gif = os.path.join(self.movies_path, 'counterplay_logo.gif')
        self.model_tab = movies.GifHoverToolButton(file_name=model_button_gif,
                                                   size=(200, 100),
                                                   parent=self)
        self.tab_btn_layout.addWidget(self.model_tab)

        skel_button_gif = os.path.join(self.movies_path, 'counterplay_logo.gif')
        self.skel_tab = movies.GifHoverToolButton(file_name=skel_button_gif,
                                                   size=(200, 100),
                                                   parent=self)
        self.tab_btn_layout.addWidget(self.skel_tab)

        rig_button_gif = os.path.join(self.movies_path, 'counterplay_logo.gif')
        self.rig_tab = movies.GifHoverToolButton(file_name=rig_button_gif,
                                                  size=(200, 100),
                                                  parent=self)
        self.tab_btn_layout.addWidget(self.rig_tab)

        anim_button_gif = os.path.join(self.movies_path, 'counterplay_logo.gif')
        self.anim_tab = movies.GifHoverToolButton(file_name=anim_button_gif,
                                                 size=(200, 100),
                                                 parent=self)
        self.tab_btn_layout.addWidget(self.anim_tab)

        self.btn_layout_spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab_btn_layout.addItem(self.btn_layout_spacer)

        # add Helios
        self.helios_frame = QFrame(self.ui_body_frame)
        self.helios_frame.setMinimumSize(400, 500)
        self.helios_layout = QVBoxLayout(self.helios_frame)
        #self.ui.helios_layout.setParent(self.ui_body_frame)

        helios_em = helios_ui.Helios()
        helios_em.setParent(self)
        self.helios_layout.addWidget(helios_em)

        self.skel_frame = QFrame(self.ui_body_frame)
        self.skel_frame.setMinimumSize(400, 500)
        self.skel_bldr_layout = QVBoxLayout(self.skel_frame)

        skel_bld = skeletonbuilder_ui.SkeletonBuilder()
        skel_bld.setParent(self)
        self.skel_bldr_layout.addWidget(skel_bld)
        self.skel_frame.setVisible(False)

        self.splitter.opaqueResize()

        #############################
        # Signals
        #############################
        self.model_tab.clicked.connect(self.show_tab_model)
        self.skel_tab.clicked.connect(self.show_tab_skel)


    #############################
    # Slots
    #############################
    def show_tab_model(self):
        self.helios_frame.setVisible(True)
        self.skel_frame.setVisible(False)

    def show_tab_skel(self):
        self.helios_frame.setVisible(False)
        self.skel_frame.setVisible(True)