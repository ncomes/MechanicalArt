#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool for organizing a Maya scene.

"""

# python imports
import os
# Qt imports
from mca.common.pyqt.pygui import qtwidgets, qtcore, qtgui
try:
	QAction = qtwidgets.QAction
except:
	QAction = qtgui.QAction

# software specific imports
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# mca python imports
from mca.common import log
from mca.common.pyqt import messages
from mca.common.utils import fileio
from mca.mya.utils import namespace_utils, scene_utils
from mca.mya.rigging import frag
from mca.mya.pyqt.utils import ma_main_window
from mca.mya.pyqt import mayawindows

logger = log.MCA_LOGGER
MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()

def MCASceneManagerStartup():
	"""
	Starts up the Scene Manager. If there is already an instance of MCASceneManager, it will be restored. Otherwise,
	a new instance will be created.

	"""

	found_manager_widget = None
	for widget in MAYA_MAIN_WINDOW.findChildren(qtwidgets.QWidget):
		if isinstance(widget, MayaQWidgetDockableMixin) and 'MCA_SceneManager' in widget.objectName():
			found_manager_widget = widget
			break
	if found_manager_widget:
		found_manager_widget.initialize_layer_tree()
		pm.workspaceControl('MCA SceneManagerWorkspaceControl', edit=True, restore=True)

	else:
		if pm.workspaceControl('MCA SceneManagerWorkspaceControl', q=True, exists=True):
			pm.workspaceControl('MCA SceneManagerWorkspaceControl', e=True, close=True)
			pm.deleteUI('MCA SceneManagerWorkspaceControl', control=True)

		scene_manager_instance = MCASceneManager()
		scene_manager_instance.setObjectName('MCA SceneManager')

		scene_manager_instance.show(dockable=True,
									area='right',
									floating=False)

		pm.workspaceControl('MCA SceneManagerWorkspaceControl',
							e=True,
							ttc=['ChannelBoxLayerEditor', -1])


class MCASceneManager(MayaQWidgetDockableMixin, mayawindows.MCAMayaWindow):
	VERSION = '1.0.0'

	def __init__(self, parent=None):
		root_path = os.path.dirname(os.path.realpath(__file__))
		ui_path = os.path.join(root_path, 'ui', 'scene_manager_ui.ui')
		super(MCASceneManager, self).__init__(parent,
											  show_window=False,
											  title='Scene Manager',
											  ui_path=ui_path,
											  version=MCASceneManager.VERSION,
											  events_register=True)
		self.layer_data_dict = {}
		self.layer_tree_build_dict = {}

		self.initialize_layer_tree()
		self.setup_signals()
		self.register_after_new_event('NewMayaScene', self.initialize_layer_tree)
		self.register_after_open_event('OpenedMayaScene', self.initialize_layer_tree)

	def initialize_layer_tree(self, *args):
		"""
		Initializes the layer tree and layer data dict

		"""

		self.initialize_layer_tree_build_dict()
		self.ui.rigs_treeWidget.clear()
		self.layer_data_dict = {}
		for layer_group, layer_data in self.layer_tree_build_dict.items():
			rig_tree_widget_item = qtwidgets.QTreeWidgetItem(self.ui.rigs_treeWidget)
			rig_tree_widget_item.setSizeHint(1, qtcore.QSize(0, 30))
			rig_tree_widget_item.setText(0, layer_group)
			top_vis_button, top_p_button = self.setup_buttons(rig_tree_widget_item,
															  add_dt_button=False,
															  button_size=[20, 20])
			top_vis_button.setText('V')
			top_p_button.setText('P')
			top_vis_button.clicked.connect(self._on_top_vis_button_clicked)
			top_p_button.clicked.connect(self._on_top_p_button_clicked)
			display_layer_strings = layer_data.get('display_layers')
			display_layers = [pm.PyNode(x) for x in display_layer_strings]
			child_p_buttons = []
			child_dt_buttons = []
			child_vis_buttons = []

			if display_layers:
				for layer in display_layers:
					layer_tree_widget_item = qtwidgets.QTreeWidgetItem(rig_tree_widget_item)
					layer_tree_widget_item.setSizeHint(1, qtcore.QSize(0, 20))
					layer_tree_widget_item.setText(0, layer.name().split(':')[-1])


					dt_button, vis_button, p_button = self.setup_buttons(layer_tree_widget_item)

					child_vis_buttons.append(vis_button)
					child_dt_buttons.append(dt_button)
					child_p_buttons.append(p_button)

					vis_status = layer.v.get()
					display_status = layer.displayType.get()
					hide_on_pb = layer.hideOnPlayback.get()

					if not hide_on_pb:
						self.set_vis_button_state(p_button, 'P')
					if vis_status:
						self.set_vis_button_state(vis_button, 'V')
					self.set_dt_button_state(dt_button, display_status)

					self.layer_data_dict[layer.name()] = {'vis_button': vis_button,
														  'dt_button': dt_button,
														  'p_button': p_button,
														  'tree_widget_item': layer_tree_widget_item,
														  'parent_item': rig_tree_widget_item,
														  'vis_status': vis_status,
														  'display_status': display_status,
														  'hide_on_pb': hide_on_pb,
														  'top_vis_button': top_vis_button,
														  'top_p_button': top_p_button}


					vis_button.clicked.connect(self._on_vis_button_clicked)
					dt_button.clicked.connect(self._on_dt_button_clicked)
					p_button.clicked.connect(self._on_p_button_clicked)

			self.ui.rigs_treeWidget.setColumnWidth(0, 130)
			self.ui.rigs_treeWidget.setColumnWidth(1, 30)
			self.ui.rigs_treeWidget.setContextMenuPolicy(qtcore.Qt.CustomContextMenu)

			self.ui.rigs_treeWidget.customContextMenuRequested.connect(self.show_context_menu)
			self.ui.rigs_treeWidget.resizeColumnToContents(1)

	def setup_buttons(self, tree_widget_item, add_dt_button=True, button_size=[18, 18]):
		"""
		Sets up buttons for the rig tree widget item

		:param qtwidgets.QTreeWidgetItem tree_widget_item: Item to add buttons to.
		:param bool add_dt_button: Whether or not to add the dt button (top level buttons do not have a dt button).
		:param list(int) button_size: Width and height of the buttons.
		:return: Returrns list of created buttons.
		:rtype: list(qtwidgets.QPushButton)

		"""

		return_buttons = []
		button_widget = qtwidgets.QWidget()
		button_layout = qtwidgets.QHBoxLayout(button_widget)
		button_layout.setContentsMargins(0, 0, 0, 0)
		vis_button = qtwidgets.QPushButton()
		p_button = qtwidgets.QPushButton()

		if add_dt_button:
			dt_button = qtwidgets.QPushButton()
			dt_button.setSizePolicy(qtwidgets.QSizePolicy.Fixed, qtwidgets.QSizePolicy.Fixed)
			dt_button.setFixedSize(button_size[0], button_size[1])
			return_buttons.append(dt_button)

		return_buttons.append(vis_button)
		return_buttons.append(p_button)

		vis_button.setSizePolicy(qtwidgets.QSizePolicy.Fixed, qtwidgets.QSizePolicy.Fixed)
		p_button.setSizePolicy(qtwidgets.QSizePolicy.Fixed, qtwidgets.QSizePolicy.Fixed)

		vis_button.setFixedSize(button_size[0], button_size[1])
		p_button.setFixedSize(button_size[0], button_size[1])

		button_layout.addWidget(vis_button)
		button_layout.addWidget(p_button)
		if add_dt_button:
			button_layout.addWidget(dt_button)

		button_widget.setWindowFlags(qtcore.Qt.FramelessWindowHint)
		button_widget.setAttribute(qtcore.Qt.WA_TranslucentBackground)

		self.ui.rigs_treeWidget.setItemWidget(tree_widget_item, 1, button_widget)
		button_widget.setFixedSize(button_size[0]*3+20, button_size[1]+2)
		button_widget.setSizePolicy(qtwidgets.QSizePolicy.Fixed, qtwidgets.QSizePolicy.Fixed)

		for button in return_buttons:
			button.setContentsMargins(0, 0, 0, 0)
			button.setStyleSheet(f"font-size: {button_size[1]-9}px;")
			button.setStyleSheet("QPushbutton { margin: 0px; padding: 0px; }")

		return return_buttons

	def initialize_layer_tree_build_dict(self):
		"""
		Initializes build dict for the layer tree.

		"""

		self.layer_tree_build_dict = {}
		all_rig_layers = []
		rigs = frag.get_frag_rigs()
		for rig in rigs:
			camera_rig = False
			frag_node = frag.FRAGNode(rig)
			for frag_child in frag_node.get_frag_children():
				if isinstance(frag_child, frag.CameraComponent):
					camera_rig = True
					break

			frag_root = frag_node.get_frag_root(rig)
			if camera_rig:
				rig_name = rig.name().split(':')[0]
			else:
				rig_name = frag_root.assetName.get()

			display_layer_node = rig.get_frag_children(of_type=frag.DisplayLayers)
			display_layers = display_layer_node[0].get_layers()

			if not display_layers:
				continue

			all_rig_layers += display_layers
			self.layer_tree_build_dict[rig_name] = {'display_layers': [x.name() for x in display_layers]}

		scene_layers = pm.ls(type=pm.nt.DisplayLayer)
		non_rig_layers = [x for x in scene_layers if x not in all_rig_layers and 'defaultLayer' not in x.name()]

		self.layer_tree_build_dict = dict(sorted(self.layer_tree_build_dict.items()))
		self.layer_tree_build_dict['Other'] = {'display_layers': [x.name() for x in non_rig_layers]}

	def setup_signals(self):
		"""
		Sets up slot signals for the UI.

		"""

		self.ui.actionRemove_Dead_FRAG_Nodes.triggered.connect(self._on_action_remove_dead_frag_nodes_triggered)
		self.ui.actionClean_Scene.triggered.connect(self._on_action_clean_scene_triggered)
		# self.ui.actionNamespace_Check.triggered.connect(self._on_namespace_check_triggered)
		self.ui.actionCheck_Out_in_Plastic.triggered.connect(self._on_action_check_out_in_plastic_triggered)
		self.ui.refresh_pushButton.clicked.connect(self._on_refresh_button_clicked)

	def update_out_of_date_ui(self):
		"""
		Checks if all layers are up-to-date in UI and  if not refreshes UI.

		:return: Whether or not the UI was updated.
		:rtype: bool

		"""

		if any(pm.objExists(x) is False for x in self.layer_data_dict.keys()):
			logger.warning('Display out of date. Refreshing UI.')
			messages.info_message('Please Try Again', 'Display was out of date. Please try again.')
			self._on_refresh_button_clicked()
			return True

		return False

	def get_layer_from_button(self, button):
		"""
		Returns the layer(s) associated with the button.

		:param qtwidgets.QPushButton button: Button to get the layer from.
		:return: List of layer(s) associated with the button.
		:rtype: list(str)

		"""

		return_layers = []
		for layer, layer_data in self.layer_data_dict.items():
			for key, val in layer_data.items():
				if val == button:
					return_layers.append(layer)
		return return_layers

	
	def _on_top_vis_button_clicked(self):
		"""
		Sets the visibility of all layers in a layer group to off or their original value.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return

		button = self.sender()
		set_vis = False if button.text() != '' else True

		associated_layers = self.get_layer_from_button(button)

		for layer in associated_layers:
			layer_data = self.layer_data_dict.get(layer)
			sub_v_button = layer_data.get('vis_button')
			layer_node = pm.PyNode(layer)

			if not set_vis:
				layer_node.v.set(0)
				sub_v_button.setEnabled(False)

			else:
				layer_v = layer_data.get('vis_status')
				layer_node.v.set(layer_v)
				sub_v_button.setEnabled(True)

		self.set_vis_button_state(button, 'V')

	
	def _on_top_p_button_clicked(self):
		"""
		Sets the hideOnPlayback of all layers in a layer group to off or their original value.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		button = self.sender()
		set_p = False if button.text() != '' else True
		associated_layers = self.get_layer_from_button(button)

		for layer in associated_layers:
			layer_data = self.layer_data_dict.get(layer)
			sub_p_button = layer_data.get('p_button')
			layer_node = pm.PyNode(layer)

			if not set_p:
				layer_node.hideOnPlayback.set(1)
				sub_p_button.setEnabled(False)

			else:
				layer_p = layer_data.get('hide_on_pb')
				layer_node.hideOnPlayback.set(layer_p)
				sub_p_button.setEnabled(True)

		self.set_vis_button_state(button, 'P')

	def show_context_menu(self, position):
		"""
		Shows context menu at the given position.

		:param list(QPoint) position: Coordinates to show the context menu at.

		"""

		item = self.ui.rigs_treeWidget.itemAt(position)

		actions = []
		if item:
			if not item.parent():
				if item.text(0) == 'Other':
					return
				delete_action = QAction('Delete', self)
				actions.append(delete_action)
				delete_action.triggered.connect(lambda: self._on_delete_group_action_triggered(item))

			else:
				rename_action = QAction('Rename', self)
				actions.append(rename_action)
				rename_action.triggered.connect(lambda: self._on_rename_layer_action_triggered(item))

				delete_action = QAction('Delete', self)
				delete_action.triggered.connect(lambda: self._on_delete_layer_action_triggered(item))
				actions.append(delete_action)

				add_selected_action = QAction('Add Selected', self)
				add_selected_action.triggered.connect(lambda: self._on_add_selected_action_triggered(item))
				actions.append(add_selected_action)

				remove_selected_action = QAction('Remove Selected', self)
				remove_selected_action.triggered.connect(lambda: self._on_remove_selected_action_triggered(item))
				actions.append(remove_selected_action)

				empty_layer_action = QAction('Empty Layer', self)
				empty_layer_action.triggered.connect(lambda: self._on_empty_layer_action_triggered(item))
				actions.append(empty_layer_action)

				select_objects_action = QAction('Select Objects', self)
				select_objects_action.triggered.connect(lambda: self._on_select_objects_action_triggered(item))
				actions.append(select_objects_action)

		else:
			create_new_lyr_action = QAction('Create New Layer', self)
			actions.append(create_new_lyr_action)
			create_new_lyr_action.triggered.connect(self._on_create_new_layer_action_triggered)
		menu = qtwidgets.QMenu(self)

		list(map(lambda x: menu.addAction(x), actions))

		# Show the context menu at the specified position
		menu.exec_(self.ui.rigs_treeWidget.mapToGlobal(position))

	
	def _on_create_new_layer_action_triggered(self):
		"""
		Creates new layer.

		"""

		layer_name = messages.text_prompt_message('New Layer', 'Name for this layer:')
		if layer_name:
			pm.createNode(pm.nt.DisplayLayer, name=layer_name)
			self.initialize_layer_tree()

	
	def _on_empty_layer_action_triggered(self, item):
		"""
		Empties the layer.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return

		layer = self.get_layer_from_button(item)[0]
		layer_node = pm.PyNode(layer)
		layer_members = pm.editDisplayLayerMembers(layer_node, q=True)
		layer_node.removeMembers(layer_members)

	
	def _on_delete_group_action_triggered(self, item):
		"""
		Deletes layer group and all associated layers.

		:param qtwidgets.QTreeWidgetItem item: Item to delete.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		associated_layers = self.get_layer_from_button(item)

		message_result = messages.question_message('Delete Layer Group', f'Are you sure you want to delete layers:'
																		 f' {associated_layers}?')
		if not message_result == 'Yes':
			return

		layer_list = [x for x in associated_layers if pm.objExists(x)]
		for layer in layer_list:
			del self.layer_data_dict[layer]

		pm.delete(layer_list)

		index = self.ui.rigs_treeWidget.indexOfTopLevelItem(item)
		if index != -1:
			top_level_item = self.ui.rigs_treeWidget.takeTopLevelItem(index)
			for i in reversed(range(top_level_item.childCount())):
				child_item = top_level_item.takeChild(i)
				del child_item
			del top_level_item

	
	def _on_add_selected_action_triggered(self, item):
		"""
		Adds selected objects to layer.

		:param qtwidgets.QTreeWidgetItem item: Item whose associated layer we want to add selected objects to.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		selected_objects = pm.selected()
		if not selected_objects:
			logger.warning('No objects selected')
			return

		layer = self.get_layer_from_button(item)[0]
		layer_node = pm.PyNode(layer)
		layer_node.addMembers(selected_objects)

	
	def _on_remove_selected_action_triggered(self, item):
		"""
		Removes selected objects from layer.

		:param qtwidgets.QTreeWidgetItem item: Item whose associated layer we want to remove selected objects from.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		selected_objects = pm.selected()
		if not selected_objects:
			logger.warning('No objects selected')
			return

		layer = self.get_layer_from_button(item)[0]
		layer_node = pm.PyNode(layer)
		layer_node.removeMembers(selected_objects)

	
	def _on_delete_layer_action_triggered(self, item):
		"""
		Deletes selected layer.

		:param qtwidgets.QTreeWidgetItem item: Item whose associated layer we want to delete.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return

		layer = self.get_layer_from_button(item)[0]
		layer_node = pm.PyNode(layer)
		message_result = messages.question_message('Delete Layer', f'Are you sure you want to delete layer: {layer}?')
		if not message_result == 'Yes':
			return

		pm.delete(layer_node)
		parent_item = item.parent()
		index = parent_item.indexOfChild(item)
		parent_item.takeChild(index)

		if parent_item.childCount() == 0 and parent_item.text(0) != 'Other':
			parent_index = self.ui.rigs_treeWidget.indexOfTopLevelItem(parent_item)
			if index != -1:
				self.ui.rigs_treeWidget.takeTopLevelItem(parent_index)
			del parent_item

		del self.layer_data_dict[layer]

	
	def _on_rename_layer_action_triggered(self, item):
		"""
		Renames layer.

		:param qtwidgets.QTreeWidgetItem item: Tree item whose associated layer we want to rename.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return

		layer = self.get_layer_from_button(item)[0]
		layer_node = pm.PyNode(layer)
		layer_data = self.layer_data_dict.get(layer)

		new_name = messages.text_prompt_message('Rename Layer', 'New name for this layer:', layer.split(':')[-1])

		if new_name:
			layer_namespace = namespace_utils.get_namespace(layer, check_node=False)
			layer_node.rename(f'{layer_namespace}:{new_name}')
			item.setText(0, new_name.split(':')[-1])
			self.layer_data_dict[layer_node.name()] = layer_data
			del self.layer_data_dict[layer]

	
	def _on_dt_button_clicked(self):
		"""
		Sets the display type of the layer.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		button = self.sender()
		layer = self.get_layer_from_button(button)[0]
		layer_node = pm.PyNode(layer)
		if button.text() == '':
			val = 1
		elif button.text() == 'T':
			val = 2
		else:
			val = 0

		layer_node.displayType.set(val)
		self.set_dt_button_state(button, val)
		layer_data = self.layer_data_dict.get(layer)
		layer_data['display_status'] = val

	def set_dt_button_state(self, button, value):
		"""
		Sets the state of the display type button.
		:param qtwidgets.QPushButton button: Button to set the state of.
		:param int value: Value to set the button to.

		"""

		if value == 2:
			button.setText('R')
		elif value == 1:
			button.setText('T')
		else:
			button.setText('')

	
	def _on_vis_button_clicked(self):
		"""
		Sets the visibility of the layer.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		button = self.sender()
		layer = self.get_layer_from_button(button)[0]
		layer_node = pm.PyNode(layer)

		set_layer = not layer_node.v.get()
		layer_node.v.set(set_layer)
		self.set_vis_button_state(button, 'V')
		layer_data = self.layer_data_dict.get(layer)
		layer_data['vis_status'] = set_layer

	
	def _on_p_button_clicked(self):
		"""
		Sets the playback status of the layer.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return
		button = self.sender()
		layer = self.get_layer_from_button(button)[0]
		layer_node = pm.PyNode(layer)
		set_layer = not layer_node.hideOnPlayback.get()
		layer_node.hideOnPlayback.set(set_layer)
		self.set_vis_button_state(button, 'P')
		layer_data = self.layer_data_dict.get(layer)
		layer_data['hide_on_pb'] = set_layer

	def set_vis_button_state(self, button, letter):
		"""
		Sets the state of the visibility button.

		:param qtwidgets.QPushButton button: Button to set the state of.
		:param str letter: Letter to set the button to.

		"""

		if button.text() == '':
			button.setText(letter)
		else:
			button.setText('')

	
	def _on_action_clean_scene_triggered(self):
		"""
		Cleans the scene.

		"""

		deleted_nodes = scene_utils.clean_scene()
		logger.warning(f'Full removal list: {deleted_nodes}')

		info_messages = messages.info_message('Clean Scene', f'Removed {len(deleted_nodes)} garbage nodes.'
															 f'\nPlease see script editor for more details.')
		self.initialize_layer_tree()

	
	def _on_action_remove_dead_frag_nodes_triggered(self):
		"""
		Removes dead frag nodes.

		"""

		dead_nodes_list = frag.remove_dead_frag_nodes()
		info_message = messages.info_message('Remove Dead Frag Nodes', f'Removed {len(dead_nodes_list)} abandoned FRAG nodes.'
																	   f'\nPlease see script editor for more details.')
		self.initialize_layer_tree()

	
	def _on_action_check_out_in_plastic_triggered(self):
		"""
		Checks out the current scene in plastic.

		"""

		file_path = pm.sceneName()
		fileio.touch_and_checkout(file_path)

	
	def _on_refresh_button_clicked(self):
		"""
		Refreshes the layer tree.

		"""

		self.initialize_layer_tree()

	
	def _on_select_objects_action_triggered(self, item):
		"""
		Selects the layer members.
		:param qtwidgets.QTreeWidgetItem item: Tree item whose associated objects will be selected.

		"""

		updated_ui = self.update_out_of_date_ui()
		if updated_ui:
			return

		layer = self.get_layer_from_button(item)[0]
		layer_members = pm.editDisplayLayerMembers(layer, query=True)
		pm.select(layer_members, r=True)

	# def _on_namespace_check_triggered(self):
	# #Not safe for all Dark Winter assets due to incomplete connections.
	# 	frag_rig_nodes = frag_rig.get_frag_rigs()
	# 	rig_namespaces = []
	#
	# 	for f_rig_node in frag_rig_nodes:
	# 		rig_nodes = []
	# 		if not ':' in f_rig_node.name():
	# 			rig_namespace = None
	# 		else:
	# 			rig_namespace = namespace.get_namespace(f_rig_node.name(), check_node=False)
	# 		frag_rt = frag.get_frag_root(f_rig_node)
	# 		asset_id = frag_rt.assetID.get()
	# 		asset_name = frag_rt.assetName.get()
	#
	# 		if rig_namespace in rig_namespaces or not rig_namespace:
	# 			correct_namespace = assetlist.get_asset_by_id(asset_id).asset_namespace
	# 			if not correct_namespace or correct_namespace in namespace.get_all_namespaces():
	# 				correct_namespace = namespace.find_unique_namespace(asset_name[:3])
	# 			if not pm.namespace(exists=correct_namespace):
	# 				pm.namespace(add=correct_namespace)
	# 		else:
	# 			correct_namespace = rig_namespace
	#
	# 		rig_children = f_rig_node.listConnections()
	# 		for rig_node in rig_children:
	# 			rig_nodes.append(rig_node)
	# 			node_connections = cmds.listConnections(rig_node.name())
	# 			for node in node_connections:
	# 				rig_nodes.append(node)
	#
	# 		frag_root_connections = frag_rt.listConnections()
	# 		for frag_root_connection in frag_root_connections:
	# 			rig_nodes.append(frag_root_connection.name())
	#
	# 			if isinstance(frag_root_connection, pm.nt.Network):
	# 				if isinstance(frag.FRAGNode(frag_root_connection), frag.SkeletalMesh):
	# 					skins_grp = frag_root_connection.grpSkins.get()
	# 					rig_nodes.append(skins_grp)
	#
	# 					meshes = skins_grp.listRelatives(ad=True)
	# 					materials = []
	#
	# 					bshape_grp = frag_root_connection.grpBlendshapes.get()
	# 					if bshape_grp:
	# 						rig_nodes.append(bshape_grp)
	# 						meshes = meshes + bshape_grp.listRelatives(ad=True)
	#
	# 					meshes = [x for x in meshes if isinstance(x, pm.nt.Transform)]
	# 					for mesh in meshes:
	# 						rig_nodes.append(mesh)
	# 						if mesh.listRelatives(s=True):
	# 							mesh_connections = cmds.listConnections(mesh.name()) or []
	# 							rig_nodes = rig_nodes + mesh_connections
	#
	# 							skin_clus = skin_utils.get_skin_cluster_from_geometry(mesh)
	# 							if skin_clus:
	# 								rig_nodes.append(skin_clus)
	# 								bind_pose = pm.PyNode(skin_clus).bindPose.get()
	# 								rig_nodes.append(bind_pose)
	#
	# 							mesh_shape = mesh.getShape()
	# 							shading_engine = mesh_shape.listConnections(type=pm.nt.ShadingEngine)[0]
	# 							rig_nodes.append(shading_engine)
	# 							material = shading_engine.surfaceShader.listConnections()[0]
	# 							if not material in materials:
	# 								materials.append(material)
	#
	# 					for material in materials:
	# 						material_nodes = pm.listHistory(material)
	# 						rig_nodes = rig_nodes + material_nodes
	#
	# 		rig_nodes.append(frag_rt)
	# 		all_group_contents = f_rig_node.all.get().listRelatives(ad=True)
	# 		rig_nodes_filtered = list(set(rig_nodes + all_group_contents))
	# 		all_rig_nodes = [pm.PyNode(x) for x in rig_nodes_filtered]
	# 		list(map(lambda x: namespace.move_node_to_namespace(x, correct_namespace), all_rig_nodes))
	# 		rig_namespaces.append(rig_namespace)
	# 	self.initialize_layer_tree()