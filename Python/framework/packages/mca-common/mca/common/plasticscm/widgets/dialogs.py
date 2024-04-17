#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that functions to retrieve info from running processes
"""

# mca python imports

# software specific imports

# mca python imports
# from mca.common import log, utils
# from mca.common.paths import project_paths
# from mca.common.python import helpers, decorators, path
# from mca.common.qt import api as qt
# from mca.common.qt.widgets import dialog
# from mca.common.resources import resources
#
# from mca.common.plasticscm import api as plastic
#
# logger = log.MCA_LOGGER
#
#
# class BasePlasticSyncDialog(dialog.MainDialog):
#
# 	def __init__(self, files_to_sync, enable_templates=False, parent=None):
# 		super(BasePlasticSyncDialog, self).__init__(parent=parent)
#
# 		self._files_to_sync = helpers.force_list(files_to_sync)
# 		self._all_files_to_sync = list()
# 		self._enable_templates = enable_templates
# 		self._plastic_templates = dict()
# 		self._result = None
#
# 		self.setWindowTitle('Plastic Sync')
# 		self.setWindowIcon(resources.icon('plastic'))
# 		self.resize(400, 400)
# 		self.refresh()
#
# 	# =================================================================================================================
# 	# ABSTRACT
# 	# =================================================================================================================
#
# 	@decorators.abstractmethod
# 	def sync(self, item_to_sync):
# 		"""
# 		Function that should be called when sync starts.
#
# 		:param str item_to_sync: path to sync.
# 		"""
#
# 		raise NotImplementedError
#
# 	# =================================================================================================================
# 	# PROPERTIES
# 	# =================================================================================================================
#
# 	@property
# 	def result(self):
# 		return self._result
#
# 	# =================================================================================================================
# 	# OVERRIDES
# 	# =================================================================================================================
#
# 	def setup_ui(self):
# 		super(BasePlasticSyncDialog, self).setup_ui()
#
# 		self._templates_widget = qt.widget(layout=qt.horizontal_layout(), parent=self)
# 		templates_label = qt.label('Plastic Templates:', parent=self)
# 		self._templates_combo = qt.combobox(parent=self)
# 		self._templates_widget.main_layout.addWidget(templates_label)
# 		self._templates_widget.main_layout.addWidget(self._templates_combo)
#
# 		self._list_widget = qt.QListWidget(parent=self)
#
# 		self._progress_label = qt.label('Hello', parent=self)
# 		progress_label_layout = qt.horizontal_layout()
# 		progress_label_layout.addStretch()
# 		progress_label_layout.addWidget(self._progress_label)
# 		progress_label_layout.addStretch()
# 		self._progress = qt.BaseProgressBar(parent=self)
# 		self._progress_label.setVisible(False)
# 		self._progress.setVisible(False)
#
# 		self._sync_button = qt.base_push_button('Sync', icon=resources.icon('sync'), parent=self)
#
# 		self.main_layout.addWidget(self._templates_widget)
# 		self.main_layout.addWidget(self._list_widget)
# 		self.main_layout.addLayout(progress_label_layout)
# 		self.main_layout.addWidget(self._progress)
# 		self.main_layout.addWidget(qt.divider(parent=self))
# 		self.main_layout.addWidget(self._sync_button)
#
# 	def setup_signals(self):
# 		super(BasePlasticSyncDialog, self).setup_signals()
#
# 		self._templates_combo.currentTextChanged.connect(self._on_templates_combo_text_changed)
# 		self._sync_button.clicked.connect(self._on_sync_button_clicked)
#
# 	# =================================================================================================================
# 	# BASE
# 	# =================================================================================================================
#
# 	def refresh(self):
# 		"""
# 		Refreshes UI.
# 		"""
#
# 		current_project = utils.get_project()
# 		project_config = current_project.get_configuration() if current_project else None
#
# 		with qt.block_signals(self._templates_combo):
# 			self._templates_combo.clear()
# 			if project_config:
# 				self._plastic_templates = project_config.get('plastic', default=dict()).get('templates', list())
# 			self._templates_combo.addItem('all')
# 			for template_name in list(self._plastic_templates.keys()):
# 				self._templates_combo.addItem(template_name)
#
# 		self._templates_widget.setVisible(self._enable_templates)
# 		self._on_templates_combo_text_changed('all')
#
# 	# =================================================================================================================
# 	# CALLBACKS
# 	# =================================================================================================================
#
# 	def _on_templates_combo_text_changed(self, current_text):
# 		"""
# 		Internal callback function that is called each time templates combo text changes.
#
# 		:param str current_text: current template name.
# 		"""
#
# 		self._list_widget.clear()
#
# 		if current_text.lower() == 'all' or not self._plastic_templates:
# 			for item in self._files_to_sync:
# 				list_item = qt.QListWidgetItem(item)
# 				self._list_widget.addItem(list_item)
# 			self._all_files_to_sync = self._files_to_sync[:]
# 		else:
# 			template_paths = self._plastic_templates.get(current_text, list())
# 			if not template_paths:
# 				for item in self._files_to_sync:
# 					list_item = qt.QListWidgetItem(item)
# 					self._list_widget.addItem(list_item)
# 				self._all_files_to_sync = self._files_to_sync[:]
# 			else:
# 				for file_to_sync in self._files_to_sync:
# 					file_ext = path.get_extension(file_to_sync)
# 					if file_ext:
# 						self._all_files_to_sync.append(file_to_sync)
# 						list_item = qt.QListWidgetItem(file_to_sync)
# 						self._list_widget.addItem(list_item)
# 					else:
# 						print(file_to_sync)
# 						for template_path in template_paths:
# 							template_file_to_sync = path.join_path(file_to_sync, template_path)
# 							self._all_files_to_sync.append(template_file_to_sync)
# 							list_item = qt.QListWidgetItem(template_file_to_sync)
# 							self._list_widget.addItem(list_item)
#
# 	def _on_sync_button_clicked(self):
# 		"""
# 		Internal callback function that is called when Sync button is clicked by the user.
# 		"""
#
# 		def _sync_files():
# 			all_valid = True
# 			for i, item in enumerate(self._all_files_to_sync):
# 				result = self.sync(item)
# 				if not result:
# 					all_valid = False
# 				self._progress.setValue(i + 1)
# 				self._progress_label.setText('Syncing from Plastic ({}/{})'.format(i + 1, len(self._all_files_to_sync)))
# 				qt.QApplication.processEvents()
# 			self._result = all_valid
# 			self._progress_label.setVisible(False)
# 			self._progress.setVisible(False)
# 			self.close()
#
# 		if not self._all_files_to_sync:
# 			logger.warning('No files to sync')
# 			return
# 		self._progress.setVisible(True)
# 		self._progress_label.setVisible(True)
# 		self._progress_label.setText('Syncing from Plastic ({}/{})'.format(1, len(self._all_files_to_sync)))
# 		self._progress.setRange(0, len(self._all_files_to_sync) + 1)
# 		self._progress.setValue(1)
# 		qt.QApplication.processEvents()
# 		qt.QTimer.singleShot(1, _sync_files)
#
#
# class PlasticLoadItemsDialog(BasePlasticSyncDialog):
#
# 	def sync(self, item_to_sync):
# 		"""
# 		Function that should be called when sync starts.
#
# 		:param str item_to_sync: path to sync.
# 		"""
#
# 		return plastic.load_items(item_to_sync, ui=False)
#
#
# class PlasticUnloadItemsDialog(BasePlasticSyncDialog):
#
# 	def sync(self, item_to_sync):
# 		"""
# 		Function that should be called when sync starts.
#
# 		:param str item_to_sync: path to sync.
# 		"""
#
# 		return plastic.unload_items(item_to_sync, ui=False)
