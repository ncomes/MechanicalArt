"""
Modules that contains important fncs for serializing and loading serialized rigs.
"""
# System global imports
import os
import time
import datetime
# software specific imports

# PySide2 imports
from PySide2.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

# mca python imports
from mca.common import log
from mca.common.resources import resources
from mca.common.assetlist import assetlist
from mca.common.textio import yamlio
from mca.mya.rigging import frag, rig_serialzation
from mca.mya.utils import events
from mca.mya.pyqt import mayawindows

logger = log.MCA_LOGGER


class SceneStatusWidget(mayawindows.MayaQWidget):
    VERSION = '1.0.0'

    def __init__(self, parent=None):
        if not parent:
            parent = mayawindows.MAYA_MAIN_WINDOW
        super().__init__(parent=parent)

        self.setMinimumSize(105, 105)

        self.events_register = events.EventsRegister()
        self._callbacks = []
        # Start watching events
        self.installEventFilter(self)

        self.register_import_event(unique_id='mca_import_rig_event', fnc=self.check_rig_versions)
        self.register_after_open_event(unique_id='mca_open_rig_event', fnc=self.check_rig_versions)
        self.register_after_new_event(unique_id='mca_new_scene_rig_event', fnc=self.check_rig_versions)
        self.frag_roots = []
        self._resources = resources.register_resources()

        self.spotter_button = SceneStatusButton(parent=self)
        self.main_layout.addWidget(self.spotter_button)

        self.check_rig_versions()

        self.show()

    def check_rig_versions(self, *args, **kwargs):
        """
        Checks the scene for the version of the rig to see if it is out of date.
        """

        self.frag_roots = []
        self.asset_names = []
        frag_roots = frag.get_all_frag_roots()
        if not frag_roots:
            logger.info('No frag roots found.')
            self.spotter_button.set_icon_status_good()
            return

        for frag_root in frag_roots:
            frag_rig = frag_root.get_rig()
            if not frag_rig:
                self.spotter_button.set_icon_status_good()
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
            self.spotter_button.set_icon_status_good()
            return
        self.spotter_button.set_icon_status_bad()


class SceneStatusButton(QPushButton):
    def __init__(self, icon_status=True, asset_data=None, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(100, 100)
        self.asset_data = asset_data
        self.bad_status_icon = resources.icon(r'color\high_priority.png')
        self.good_status_icon = resources.icon(r'color\checked.png')
        self.parent_widget = parent

        if icon_status:
            self.set_icon_status_good()
        else:
            self.set_icon_status_bad()

        self.clicked.connect(self.open_updater_clicked)

    def set_icon_status_bad(self):
        self.setIcon(self.bad_status_icon)

    def set_icon_status_good(self):
        self.setIcon(self.good_status_icon)

    def open_updater_clicked(self):
        UpdaterStatusWindow(parent_widget=self.parent_widget)


class UpdaterStatusWindow(mayawindows.MCAMayaWindow):
    VERSION = '1.0.0'

    def __init__(self, parent_widget):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'scene_status_updater.ui')
        super().__init__(title='Scene Status Updater', ui_path=ui_path, version=self.VERSION)
        self.parent_widget = parent_widget
        self.frag_roots = self.parent_widget.frag_roots
        self.asset_names = self.parent_widget.asset_names
        self.setMinimumSize(355, 335)

        self.rig_layout = QVBoxLayout(self)
        self.ui.rigs_scrollAreaWidgetContents.setLayout(self.rig_layout)
        self.ui.rigs_scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.create_outdated_rig()

    def create_outdated_rig(self):
        if not self.frag_roots:
            return
        for frag_root in self.frag_roots:
            asset_name = list(frag_root.keys())[0]
            frag_rig = frag_root[asset_name].get('frag_rig', None)
            current_version = frag_rig.version.get()
            old_version = frag_root[asset_name].get('new_version', None)
            outdated_widget = OutdatedRigsWidget(asset_name=asset_name,
                                                 frag_rig=frag_rig,
                                                 current_version=current_version,
                                                 old_version=old_version,
                                                 parent=self.ui.rigs_scrollAreaWidgetContents)
            self.rig_layout.addWidget(outdated_widget)


class OutdatedRigsWidget(mayawindows.MayaQWidget):
    VERSION = '1.0.0'

    def __init__(self, asset_name, frag_rig, current_version, old_version, parent=None):
        super().__init__(parent=parent)
        self.asset_name = asset_name
        self.frag_rig = frag_rig
        self.current_version = current_version
        self.old_version = old_version

        self.setFixedHeight(35)
        self.setMinimumWidth(340)

        self.h_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.h_layout)

        self.rig_name = QLabel()
        self.rig_name.setText(f'{self.asset_name}: update version {self.old_version} -> {self.current_version}')
        self.rig_name.setMinimumWidth(250)
        self.rig_name.setFixedHeight(30)
        self.h_layout.addWidget(self.rig_name)

        self.update_button = QPushButton(' Update Rig ')
        self.rig_name.setFixedHeight(30)
        self.h_layout.addWidget(self.update_button)

        self.update_button.clicked.connect(self.update_clicked)

    def update_clicked(self):
        print(f'Updating {self.asset_name}')
