"""
Module that contains the mca decorators at a base python level
"""

# python imports
import os
# Qt imports
from mca.common.pyqt.pygui import qtcore, qtgui
# software specific imports
import pymel.all as pm
# mca python imports
from mca.common.assetlist import assetlist, archetype_assetlist
from mca.common.resources import resources
from mca.common.utils import list_utils

from mca.mya.modifiers import ma_decorators
from mca.mya.pyqt import maya_dialogs, mayawindows
from mca.mya.rigging import frag, rig_utils
from mca.mya.utils import namespace_utils
from mca.mya.tools.helios import helios_utils

from mca.common import log
logger = log.MCA_LOGGER

MISSING_ICON = resources.icon(r'color\question.png')

class Summoner(mayawindows.MCAMayaWindow):
    _version = 1.0
    tab_organization_dict = {}
    entry = None

    def __init__(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'summoner_ui.ui')
        super().__init__(title='Summoner',
                         ui_path=ui_path,
                         version=self._version)
        
        self.entry = qtgui.QStandardItemModel()
        self.ui.asset_list_listView.setModel(self.entry)
        self.ui.asset_list_listView.setSpacing(2)
        self.ui.asset_list_listView.setIconSize(qtcore.QSize(64, 64))

        self.setup_signals()
        self.initialize_lists()
    
    class AssetItem(qtgui.QStandardItem):
        ASSET_ENTRY = None
        def __init__(self, asset_entry):
            super().__init__()
            self.ASSET_ENTRY = asset_entry

            self.setEditable(False)

            self.setText(asset_entry.asset_name)
            asset_icon = None
            if asset_entry.mesh_path:
                asset_icon_path = f'{asset_entry.mesh_path[:-3]}jpg'
                if os.path.exists(asset_icon_path):
                    asset_icon = qtgui.QIcon(asset_icon_path)
            self.setIcon(asset_icon or MISSING_ICON)

    def setup_signals(self):
        self.ui.filter_lineEdit.textChanged.connect(self.filter_list)
        self.ui.asset_list_listView.clicked.connect(self.rig_entry_selected)
        self.ui.rigs_list_listWidget.itemDoubleClicked.connect(self.import_rig_clicked)
        self.ui.import_rig_pushButton.clicked.connect(self.import_rig_clicked)

    def initialize_lists(self):
        self.ui.category_select_comboBox.clear()

        asset_registry = assetlist.get_registry()
        archetype_registry = archetype_assetlist.get_archetype_registry()

        self.tab_organization_dict = {}
        for _, archetype_entry in archetype_registry.NAME_REGISTRY.items():            
            organization_dict = archetype_entry.organization
            if not organization_dict:
                continue
            
            # Should catch "rig" and "rigged_model" types.
            if not any(True if 'rig' in x else False for x in organization_dict.get('type', [])):
                continue

            if organization_dict:
                tab_name = organization_dict.get('tab_name')
                if tab_name not in self.tab_organization_dict:
                    self.tab_organization_dict[tab_name] = {'name': tab_name, 'type': [], 'asset_list': []}

                for tab_type_filter in organization_dict.get('type'):
                    if tab_type_filter not in self.tab_organization_dict[tab_name]['type']:
                        self.tab_organization_dict[tab_name]['type'].append(tab_type_filter)

                subtype_list = organization_dict.get('subtype')
                if subtype_list and len(subtype_list) == 1:
                    self.tab_organization_dict[tab_name]['subtype'] = subtype_list[0]

        for asset_entry in asset_registry.ASSET_ID_DICT.values():
            # Iterate through all known assets.
            for _, tab_dict in self.tab_organization_dict.items():
                # If they match our type filter, and subtype filter add them to the importable asset list.
                if asset_entry.asset_type not in tab_dict.get('type', []):
                    continue
                if not all(True if x in asset_entry.asset_subtype else False for x in tab_dict.get('subtype', [])):
                    continue
                tab_dict['asset_list'].append(asset_entry)
        self.ui.category_select_comboBox.addItems(sorted([x for x, y in self.tab_organization_dict.items() if y.get('asset_list')]))
        self.filter_list()
    
    def filter_list(self):
        filter_string = self.ui.filter_lineEdit.text()

        inclusive_list = []
        exclusive_list = []
        split_string = filter_string.split(' ')
        if split_string != ['']:
            for x in split_string:
                if x.startswith('-'):
                    exclusive_list.append(x[1:].lower())
                else:
                    inclusive_list.append(x.lower())

        current_rig_type = self.ui.category_select_comboBox.currentText()
        asset_entry_list =self.tab_organization_dict.get(current_rig_type, {}).get('asset_list', [])

        self.entry.clear()
        filtered_list = []
        if inclusive_list or exclusive_list:
            for asset_entry in asset_entry_list:
                if all(True if x in asset_entry.asset_name.lower() else False for x in inclusive_list) and all(True if x not in asset_entry.asset_name.lower() else False for x in exclusive_list):
                    filtered_list.append(self.AssetItem(asset_entry))

            if filtered_list:
                for item in filtered_list:
                    self.entry.appendRow(item)
        else:
            for asset_entry in asset_entry_list:
                self.entry.appendRow(self.AssetItem(asset_entry))

    def rig_entry_selected(self):
        asset_entry = None
        for index in self.ui.asset_list_listView.selectedIndexes():
            asset_entry = self.ui.asset_list_listView.model().itemFromIndex(index).ASSET_ENTRY
            break

        if asset_entry:
            rig_path = asset_entry.rig_path
            self.ui.rigs_list_listWidget.clear()
            if rig_path:
                self.ui.rigs_list_listWidget.addItems([x for x in os.listdir(rig_path) if x.lower().endswith('.rig')])

    @ma_decorators.keep_namespace_decorator
    def import_rig_clicked(self, *args, **kwargs):
        """
        From the displayname get our asset ID from our saved dict, then import an asset based on it.

        """
        selection = pm.selected()

        asset_entry = None
        for index in self.ui.asset_list_listView.selectedIndexes():
            asset_entry = self.ui.asset_list_listView.model().itemFromIndex(index).ASSET_ENTRY
            break
        selected_qwidget_item = self.ui.rigs_list_listWidget.currentItem()

        if not self.ui.with_namespace_checkBox.isChecked():
            namespace_utils.set_namespace('')
        else:
            namespace_str = asset_entry.asset_namespace or asset_entry.asset_name[:3]
            namespace_utils.set_namespace(namespace_str)

        # do import
        if self.ui.geo_only_checkBox.isChecked():
            logger.debug('geo only')
            helios_utils.import_asset(asset_entry, with_skinning=True)

        else:
            logger.debug('import rig')
            import_path = os.path.join(asset_entry.rig_path, selected_qwidget_item.text())
            cached_path = import_path.replace('.rig', '.ma')
            if self.ui.cached_checkBox.isChecked():
                logger.debug('using cached path')
                if not os.path.exists(cached_path):
                    result = maya_dialogs.question_prompt('Cached Rig is Missing', 'Would you like to regenerate the rig? \nRegenerating the rig will use the rig file and asset data to rebuild the rig.')
                    if result != 'Yes':
                        return
                else:
                    import_path = cached_path
                    
            logger.debug(import_path)
            frag_root = None
            if import_path.endswith('.ma'):
                imported_node_list = pm.importFile(import_path, returnNewNodes=True)
                for network_node in pm.ls(imported_node_list, type=pm.nt.Network):
                    frag_node = frag.FRAGNode(network_node)
                    if isinstance(frag_node, frag.FRAGRoot):
                        frag_root=frag_node
                        break
                if frag_root:
                    frag_rig = frag_root.frag_rig
                    if frag_rig:
                        rig_result = frag_rig.validate_rig()
                        if not rig_result:
                            result = maya_dialogs.question_prompt('Cached Rig is Out of Date', 'Would you like to regenerate the rig? \nRegenerating the rig will use the rig file and asset data to rebuild the rig.')
                            if result != 'Yes':
                                return
                            frag_root.remove()
                            import_path = import_path.replace('.ma', '.rig')
            if import_path.endswith('rig'):
                frag_root = rig_utils.import_rig(asset_entry, import_path, self.ui.with_namespace_checkBox.isChecked())

            if frag_root and self.ui.equip_weapons_checkBox.isChecked() and 'weapon' in asset_entry.asset_subtype:
                if selection:
                    logger.debug('equipping weapon')
                    frag_rig = frag.get_frag_rig(selection[0])
                    if frag_rig:
                        weapon_component = list_utils.get_first_in_list(frag_rig.get_frag_children(frag.FKComponent, 'right', 'weapon'))
                        if weapon_component:
                            imported_world_component = list_utils.get_first_in_list(frag_root.frag_rig.get_frag_children(frag.WorldComponent))
                            if imported_world_component:
                                world_flag = imported_world_component.pynode.getAttr('world_flag')
                                pm.parentConstraint(weapon_component.flags[0].pynode, world_flag)

