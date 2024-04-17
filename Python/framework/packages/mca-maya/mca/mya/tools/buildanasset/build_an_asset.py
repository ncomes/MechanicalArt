#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox for streamlining pipeline.
"""
# python imports
import os
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QLabel

# software specific imports
import maya.cmds as cmds
import pymel.core as pm

# mca python imports
from mca.mya.pyqt import dialogs, mayawindows
from mca.mya.utils import optionvars
from mca.common.resources import resources

# mca tool imports
from mca.mya.tools.helios import helios_ui, helios_utils
from mca.mya.tools.buildarig import buildarig_ui
# from mca.mya.tools.flagrotationordereditor import flagrotationordereditor

class BuildAnAssetUi(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        print(root_path)
        ui_path = os.path.join(root_path, 'ui', 'buildanasset_ui.ui')
        print(ui_path)
        super().__init__(title='Build An Asset',
                         ui_path=ui_path,
                         version=BuildAnAssetUi.VERSION)

        self.setup_embeds()
        self.setup_signals()

    def setup_signals(self):
        """
        Setting up signals.

        """
        ### Model Signals ###

        self.ui.applymats_pushButton.pressed.connect(self.apply_mats_clicked)


        ### Skeleton Signals ###

        ### Rig Signals ###

        ### Animation Signals ###


    def setup_images(self):
        """
        Settting up images.

        """

        #Currently not working.
        # helios_image = resources.pixmap('maxwell_icon')
        # helios_image_display = self.ui.heliosimage_Label
        # helios_image_display.setPixmap(helios_image)

    def setup_embeds(self):
        """
        Setting up embedded UIs.

        """

        helios_embed = helios_ui.Helios()
        helios_embed.setParent(self)
        self.ui.helios_Layout.addWidget(helios_embed)

        buildarig_embed = buildarig_ui.BuildARig()
        buildarig_embed.setParent(self)
        self.ui.bar_Layout.addWidget(buildarig_embed)

        # Commenting out for now.
        # flagrotationorder_embed = flagrotationordereditor.FlagRotationOrderEditor()
        # flagrotationorder_embed.setParent(self)
        # self.ui.flagrotationorder_Layout.addWidget(flagrotationorder_embed)

    def apply_mats_clicked(self):
        """
        Using command from Helios Utils to apply materials.

        """
        helios_utils.apply_materials_to_selected_cmd()
