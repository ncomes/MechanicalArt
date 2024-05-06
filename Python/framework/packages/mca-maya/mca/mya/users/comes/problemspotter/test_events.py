"""
Modules that contains important fncs for serializing and loading serialized rigs.
"""
# System global imports
import os
# software specific imports
import pymel.core as pm

# PySide2 imports
from PySide2.QtWidgets import QFileDialog, QPushButton

# mca python imports
from mca.common import log
from mca.common.assetlist import assetlist
from mca.common.textio import yamlio
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import frag, rig_serialzation
from mca.mya.utils import events


logger = log.MCA_LOGGER


class TestEventUI(mayawindows.MCAMayaWindow):
    def __init__(self):
        super().__init__()

        #new_event = self.register_after_new_event(unique_id='test_event', fnc=self.check_rig_versions)
        self.events_register = events.EventsRegister()
        self.register_import_event(unique_id='import_rig_event', fnc=self.check_rig_versions)

        self.btn = QPushButton('Unregister')
        self.main_layout.addWidget(self.btn)

        self.btn.clicked.connect(self.unregister)
        #self.check_rig_versions()

    def check_rig_versions(self, *args, **kwargs):
        frag_rig = frag.get_frag_rigs()[0]
        frag_root = frag.get_frag_root(frag_rig)
        asset_id = frag_root.asset_id
        frag_version = frag_rig.version.get()
        asset_list = assetlist.get_asset_by_id(asset_id)

        aset_name = asset_list.asset_name.lower()
        rig_path = os.path.join(asset_list.rigs_path, f'{aset_name}.rig')

        data_dict = yamlio.read_yaml_file(rig_path)
        serialized_rig = rig_serialzation.SerializeRig(frag_rig=frag_rig, build_list=data_dict)
        version = serialized_rig.version
        if version > frag_version:
            print('Out of date!')

    def test_dialog(self, *args, **kwargs):
        self.main_layout.addWidget(QFileDialog())

    def unregister(self, *args, **kwargs):
        self.unregister_event(unique_id='test_event')

    def register_import_event(self, unique_id, fnc):
        """
        Registers after a scene opened event.
        :param unique_id: Unique name to register the event to.
        :param fnc: Function to call after opening a scene.

        """

        if not self.events_register:
            self.events_register = events.EventsRegister()

        self.events_register.register_after_import_event(unique_id, fnc)
        self._callbacks.append(unique_id)


def test_print():
    print('test_print')