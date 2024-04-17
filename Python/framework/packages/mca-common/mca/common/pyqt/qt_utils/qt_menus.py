#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A way to interact with QMenu

"""
# mca python imports
import logging
from PySide2.QtWidgets import QAction, QMenu, QMenuBar
from PySide2.QtGui import QIcon
from PySide2.QtCore import QSize, Qt

# software specific imports
# mca python imports

logger = logging.getLogger('mca-common')


class MainWindowsMenus:
	
	def __init__(self, menu_inst, main_window):
		self.main_window = main_window
		self.menu = menu_inst
	
	@classmethod
	def create(cls, menu_name, main_window, icon=None, skip_dialog=False):
		"""
		Returns an instance of the MainWindowMenu
		
		:param str menu_name: Object name of a specific QMenu
		:param QtMainWindow main_window: A QtMainWindow
		:param str icon: Full path to the icon
		:return: Returns an instance of the MainWindowMenu
		:rtype: MainWindowsMenus
		"""

		parent_menubar = main_window.findChild(QMenuBar)
		# Keeping this here for reference.  The code below crashes mobu
		#parent_menubar = main_window.menuBar() if hasattr(main_window, 'menuBar') else main_window.findChild(QMenuBar)
		
		menu_inst = None
		for child_widget in parent_menubar.children():
			if child_widget.objectName() == menu_name:
				menu_inst = child_widget
				if not skip_dialog:
					logger.info(f'QMenu {menu_name}: Found!')
				return cls(menu_inst, main_window)
		if not menu_inst:
			parent_menubar = get_main_menu_menubar(main_window)
			menu_inst = MainWindowsMenus(parent_menubar, main_window).add_menu(menu_name, icon=icon)
		
		return cls(menu_inst, main_window)
	
	def add_menu(self, menu_name, icon=None, tear_off=True, change_menu=True, skip_dialog=False):
		main_menu = QMenu(parent=self.menu)
		main_menu.setTitle(menu_name)
		main_menu.setAttribute(Qt.WA_TranslucentBackground, False)
		self.menu.addMenu(main_menu)
		main_menu.setObjectName(menu_name)
		main_menu.setTearOffEnabled(tear_off)
		
		if icon:
			if not isinstance(icon, QIcon):
				if not skip_dialog:
					logger.info('Not an instance of QIcon!')
				icon = self.convert_to_qicon(icon)
			main_menu.setIcon(icon)
		
		if change_menu:
			self.menu = main_menu
		
		return main_menu
	
	def add_action(self, action_name, fn, menu=None, icon=None, tooltip=None, skip_dialog=False):
		"""
		Adds a QAction to a QMenu
		
		:param str action_name: Name of the QAction
		:param function fn: The command the QAction will execute
		:param QMenu menu: an instance of QMenu
		:param str icon: Full path to the icon
		:param str tooltip: String Tool Tip
		"""
		
		if not menu:
			menu = self.menu
		
		action = QAction(action_name, menu)
		action.setText(action_name)
		action.setObjectName(action_name)
		action.triggered.connect(fn)
		
		if icon:
			if not isinstance(icon, QIcon):
				if not skip_dialog:
					logger.info('Not an instance of QIcon!')
				icon = self.convert_to_qicon(icon)
			action.setIcon(icon)
		
		if tooltip:
			action.setToolTip(tooltip)
		
		menu.addAction(action)
	
	def add_separator(self):
		self.menu.addSeparator()
	
	def convert_to_qicon(self, icon_path):
		"""
		Returns a QIcon from the given path
		
		:param str icon_path: Full path to the icon
		:return: Returns a QIcon from the given path
		:rtype: QIcon
		"""
		
		icon = QIcon()
		icon.addFile(icon_path, QSize(), QIcon.Normal, QIcon.Off)
		return icon
	
	def remove_action(self, action_name, menu=None):
		"""
		Returns if the action was removed or not.
		
		:param str action_name: Name of the QAction
		:param QMenu menu: Instance of a QMenu
		:return: Returns if the action was removed or not.
		:rtype: bool
		"""
		
		if not menu:
			menu = self.menu
		
		for act in menu.children():
			if not isinstance(act, QAction):
				continue
			if act.text() == action_name:
				act.deleteLater()
				return True
			return False
	
	def remove_menu(self, menu=None):
		"""
		Returns if the action was removed or not.

		:param QMenu menu: Instance of a QMenu
		:return: Returns if the action was removed or not.
		:rtype: bool
		"""
		
		if not menu:
			menu = self.menu
		menu.deleteLater()


def get_main_menu_menubar(main_window):
	"""
	Returns the main menu bar object.
	
	:return: found the menu bar Qt widget.
	:rtype: QMenuBar
	"""
	
	main_menu_bar = None
	for child in main_window.children():
		if isinstance(child, QMenuBar):
			main_menu_bar = child
	if not main_menu_bar:
		return main_window.findChild(QMenuBar)
	return main_menu_bar

