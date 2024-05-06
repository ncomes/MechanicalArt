"""
Modules that contains important fncs for serializing and loading serialized rigs.
"""
# System global imports
import os
# software specific imports
import pymel.core as pm

# PySide2 imports
from PySide2.QtWidgets import QLabel, QPushButton, QFrame, QVBoxLayout

# mca python imports
from mca.common import log
from mca.common.resources import resources
from mca.common.assetlist import assetlist
from mca.common.textio import yamlio
from mca.mya.pyqt import mayawindows
from mca.mya.rigging import frag, rig_serialzation
from mca.mya.utils import events


logger = log.MCA_LOGGER


class RigUpdaterWindow(mayawindows.MCAMayaWindow):
    """
    A window that shows a list of outdated rigs in the scene.
    """

    VERSION = '1.0.0'

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'rig_updater.ui')
        super().__init__(title='Rig Updater', ui_path=ui_path, version=self.VERSION)

        self.setMinimumSize(215, 230)

        self.register_import_event(unique_id='import_rig_event', fnc=self.check_rig_versions)
        self.frag_roots = []
        self._resources = resources.register_resources()
        self.events_register = events.EventsRegister()
        self.spotter_window = SpotterWindow(parent=self.ui.image_frame)
        self.check_rig_versions()

    def register_import_event(self, unique_id, fnc):
        """
        Registers after something is imported into the scene.
        :param unique_id: Unique name to register the event to.
        :param fnc: Function to call after opening a scene.

        """

        if not self.events_register:
            self.events_register = events.EventsRegister()

        self.events_register.register_after_import_event(unique_id, fnc)
        self._callbacks.append(unique_id)

    def check_rig_versions(self, *args, **kwargs):
        self.frag_roots = []
        self.asset_names = []
        frag_roots = frag.get_all_frag_roots()
        if not frag_roots:
            logger.info('No frag roots found.')
            return

        for frag_root in frag_roots:
            frag_rig = frag_root.get_rig()
            if not frag_rig:
                logger.info(f'No frag rig connected to {frag_root.nodeName()}')
                continue

            asset_id = frag_root.asset_id
            rig_version = frag_rig.version.get()
            asset_list = assetlist.get_asset_by_id(asset_id)

            asset_name = asset_list.asset_name.lower()
            rig_path = os.path.join(asset_list.rigs_path, f'{asset_name}.rig')
            if not os.path.exists(rig_path):
                logger.warning(f'No .rig file found at {rig_path}.  Please save a rig or check the name is correct')
                continue

            data_dict = yamlio.read_yaml_file(rig_path)
            serialized_rig = rig_serialzation.SerializeRig(frag_rig=frag_rig, build_list=data_dict)
            version = serialized_rig.version
            if version > rig_version:
                rig_dict = {}
                rig_dict[asset_name] = {}
                rig_dict[asset_name].update({'frag_rig': frag_rig})
                rig_dict[asset_name].update({'current_version': rig_version})
                rig_dict[asset_name].update({'new_version': version})
                self.frag_roots.append(rig_dict)
                self.asset_names.append(asset_name)

        if not self.frag_roots:
            self.set_spotter_icon_good()
            return

        self.ui.rig_list_comboBox.addItems(self.asset_names)
        self.set_spotter_icon_bad()
        logger.info(f'Found {len(self.frag_roots)} outdated rigs.')

    def set_spotter_icon_good(self):
        self.spotter_window.set_icon_yes_updates()

    def set_spotter_icon_bad(self):
        self.spotter_window.set_icon_no_updates()

class SpotterWindow(QFrame):
    def __init__(self, parent=None, icon_setting=True):
        super().__init__(parent=parent)
        self.icon_setting = icon_setting
        self.setMinimumSize(110, 110)
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.label = QLabel()
        self.label.setMinimumSize(100,100)
        self.main_layout.addWidget(self.label)

        no_updates = resources.pixmap(r'color\high_priority.png')
        yes_updates = resources.pixmap(r'color\checked.png')
        if icon_setting:
            self.label.setPixmap(yes_updates)
        else:
            self.label.setPixmap(no_updates)

        self.show()

    def set_icon_no_updates(self):
        self.label.setPixmap(resources.pixmap(r'color\high_priority.png'))

    def set_icon_yes_updates(self):
        self.label.setPixmap(resources.pixmap(r'color\checked.png'))
