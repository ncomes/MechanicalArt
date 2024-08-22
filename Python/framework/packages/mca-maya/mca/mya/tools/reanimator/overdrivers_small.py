"""
Module that contains the mca decorators at a base python level
"""

# System global imports
import os
# software specific imports
# mca python imports
from mca.mya.animation import time_utils
from mca.mya.pyqt import mayawindows
from mca.mya.tools.toolbar import rig_tools
from mca.mya.utils import optionvars


class MCAOverDriverOptionVars(optionvars.MCAOptionVars):
    # Helios Misc
    MCAReanimTX = {'default_value': True, 'docstring': 'Overdiver should constrain translate X.'}
    MCAReanimTY = {'default_value': True, 'docstring': 'Overdiver should constrain translate Y.'}
    MCAReanimTZ = {'default_value': True, 'docstring': 'Overdiver should constrain translate Z.'}
    MCAReanimRX = {'default_value': True, 'docstring': 'Overdiver should constrain rotate X.'}
    MCAReanimRY = {'default_value': True, 'docstring': 'Overdiver should constrain rotate Y.'}
    MCAReanimRZ = {'default_value': True, 'docstring': 'Overdiver should constrain rotate Z.'}


class OverDriverSmall(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'
    
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'overdriver_tb.ui')
        super().__init__(title='OverDriver Compact',
                         ui_path=ui_path,
                         version=OverDriverSmall.VERSION)

        
        self.optionvars = MCAOverDriverOptionVars()
        
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        
        # Opening UI settings
        self.ui.translate_x_checkBox.setChecked(self.optionvars.MCAReanimTX)
        self.ui.translate_y_checkBox.setChecked(self.optionvars.MCAReanimTY)
        self.ui.translate_z_checkBox.setChecked(self.optionvars.MCAReanimTZ)
        self.ui.rotate_x_checkBox.setChecked(self.optionvars.MCAReanimRX)
        self.ui.rotate_y_checkBox.setChecked(self.optionvars.MCAReanimRY)
        self.ui.rotate_z_checkBox.setChecked(self.optionvars.MCAReanimRZ)
        
        #########################################
        # Signals
        #########################################
        self.ui.add_overdriver_pushButton.clicked.connect(self._on_add_overdriver_clicked)
        self.ui.remove_overdriver_pushButton.clicked.connect(self._on_remove_overdriver_clicked)
        self.ui.bake_and_remover_overdriver_pushButton.clicked.connect(self._on_remove_and_bake_overdriver_clicked)
        self.ui.translate_x_checkBox.clicked.connect(self._update_option_vars)
        self.ui.translate_y_checkBox.clicked.connect(self._update_option_vars)
        self.ui.translate_z_checkBox.clicked.connect(self._update_option_vars)
        self.ui.rotate_x_checkBox.clicked.connect(self._update_option_vars)
        self.ui.rotate_y_checkBox.clicked.connect(self._update_option_vars)
        self.ui.rotate_z_checkBox.clicked.connect(self._update_option_vars)
        
    ####################################
    # Slots
    ####################################
    def _update_option_vars(self):
        self.optionvars.MCAReanimTX = bool(self.ui.translate_x_checkBox.isChecked())
        self.optionvars.MCAReanimTY = bool(self.ui.translate_y_checkBox.isChecked())
        self.optionvars.MCAReanimTZ = bool(self.ui.translate_z_checkBox.isChecked())
        self.optionvars.MCAReanimRX = bool(self.ui.rotate_x_checkBox.isChecked())
        self.optionvars.MCAReanimRY = bool(self.ui.rotate_y_checkBox.isChecked())
        self.optionvars.MCAReanimRZ = bool(self.ui.rotate_z_checkBox.isChecked())

    def _on_add_overdriver_clicked(self):
    
        skip_rotate_attrs = []
        if not self.ui.rotate_x_checkBox.isChecked(): skip_rotate_attrs.append('x')
        if not self.ui.rotate_y_checkBox.isChecked(): skip_rotate_attrs.append('y')
        if not self.ui.rotate_z_checkBox.isChecked(): skip_rotate_attrs.append('z')
    
        skip_translate_attrs = []
        if not self.ui.translate_x_checkBox.isChecked(): skip_translate_attrs.append('x')
        if not self.ui.translate_y_checkBox.isChecked(): skip_translate_attrs.append('y')
        if not self.ui.translate_z_checkBox.isChecked(): skip_translate_attrs.append('z')
    
        rig_tools.create_overdriver_cmd(skip_rotate_attrs, skip_translate_attrs)


    
    def _on_remove_overdriver_clicked(self):
        rig_tools.bake_overdriver_cmd(False)

    
    def _on_remove_and_bake_overdriver_clicked(self):
        start_frame, end_frame = time_utils.get_scene_range()
        rig_tools.bake_overdriver_cmd(True, start_frame, end_frame)