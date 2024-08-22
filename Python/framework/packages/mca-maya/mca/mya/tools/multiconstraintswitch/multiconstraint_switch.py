"""
Tool that adds multi constraints.
"""

# System global imports
import os
# Software specific imports
import pymel.core as pm
import maya.cmds as cmds
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import flags, frag
from mca.mya.utils import naming
from mca.common import log
logger = log.MCA_LOGGER


class MulticonstraintSwitch(mayawindows.MCAMayaWindow):
    _version = 1.0
    
    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'multiconstraint_switchUI.ui')
        super().__init__(title='Multi Constraint Switch',
                         ui_path=ui_path,
                         version=MulticonstraintSwitch._version,
                         events_register=True)

        # we're going to establish these during the callback so they're ready to fire.
        self._target_dict = {}
        self._rig_multi_dict = {}

        # spin up callback to handle updating the dropdown options.
        #self.register_event('MultiSwitchSelection', self._sync_dropdown_options)
        self.sji = cmds.scriptJob( event= ["SelectionChanged", self._sync_dropdown_options])
        # ==============================
        # Signals
        # ==============================
        self.ui.switch_pushButton.clicked.connect(self.switch_multiconstraint_clicked)

    def closeEvent(self, event):
        if cmds.scriptJob(exists=self.sji):
            cmds.scriptJob(kill=self.sji)
        super().closeEvent(event)
    # ==============================
    # Slots
    # ==============================
    def _sync_dropdown_options(self, *args, **kwargs):
        selection = pm.selected()
        if not selection:
            return
        flag_filter_list = [x for x in selection if flags.is_flag(x) and x.hasAttr('source_multi_constraint')]

        self.ui.switch_comboBox.clear()
        self._target_dict = {}
        self._rig_multi_dict = {}
        if not flag_filter_list:
            # bail out asap since we're in a callback
            # no log here since this is used in a callback
            return

        target_count = len(flag_filter_list)
        target_count_dict = {}
        rig_multi_dict = {}
        first_target_list = []
        first_rig_multi_dict = {}
        for index, flag_node in enumerate(flag_filter_list):
            # filter flags to only those with a multiconstraint.
            multi_constraint = frag.FRAGNode(flag_node.getAttr('source_multi_constraint'))
            frag_root = frag.get_frag_root(multi_constraint)
            frag_rig = frag_root.frag_rig
            if frag_rig not in rig_multi_dict:
                rig_multi_dict[frag_rig] = []
            rig_multi_dict[frag_rig].append(multi_constraint)
            target_list = multi_constraint.targets
            if not index:
                # if we don't find any matches use this list for the valid switch list
                first_target_list = target_list
                first_rig_multi_dict = {frag_rig: [multi_constraint]}
                if target_count == 1:
                    # if we only have one multiconstraint source just bail here we'll use the first target list.
                    break
            for target_node in target_list:
                if target_node not in target_count_dict:
                    target_count_dict[target_node] = 0
                target_count_dict[target_node] += 1

        valid_target_list = []
        for target_node, count in target_count_dict.items():
            # do some manual counting of our targets if it matches the number of inputs it's valid.
            if count == target_count:
                valid_target_list.append(target_node)

        if not valid_target_list:
            # if we didn't find any shared valid targets, we'll operate on the first object.
            valid_target_list = first_target_list
            rig_multi_dict = first_rig_multi_dict

        self._rig_multi_dict = rig_multi_dict

        for target_node in valid_target_list:
            target_name = naming.get_basename(target_node)
            self.ui.switch_comboBox.addItem(target_name)
            self._target_dict[target_name] = target_node

    @ma_decorators.keep_selection_decorator
    @ma_decorators.undo_decorator
    @ma_decorators.keep_autokey_decorator
    @ma_decorators.keep_current_frame_decorator
    def switch_multiconstraint_clicked(self):
        switch_target = self._target_dict[self.ui.switch_comboBox.currentText()]


    