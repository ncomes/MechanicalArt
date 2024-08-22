#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# System global imports
# software specific imports
# Qt imports
from mca.common.pyqt.pygui import qtcore
#  python imports
from mca.common.pyqt import common_windows
from mca.mya.pyqt.utils import ma_main_window
from mca.mya.utils import events


MAYA_MAIN_WINDOW = ma_main_window.get_maya_window()


class MayaWindowEvents:
	def __init__(self, events_register=False, parent=None, *args, **kwargs):
		self._callbacks = []
		# Start watching events
		self.events_register = events.EventsRegister() if events_register else None

	def register_event(self, unique_id, fnc):
		"""
		THIS IS A HACK FOR NOW.  THIS REGISTERS THE CHANGE SELECTED CALLBACK.
		:param unique_id: Unique name to register the event to.
		:param fnc: Function to call when the event is fired.

		"""

		if not self.events_register:
			self.events_register = events.EventsRegister()

		self.events_register.register_selection_changed_event(unique_id, fnc)
		self._callbacks.append(unique_id)

	def register_after_open_event(self, unique_id, fnc):
		"""
		Registers after a scene opened event.
		:param unique_id: Unique name to register the event to.
		:param fnc: Function to call after opening a scene.

		"""

		if not self.events_register:
			self.events_register = events.EventsRegister()

		self.events_register.register_after_open_event(unique_id, fnc)
		self._callbacks.append(unique_id)

	def register_after_new_event(self, unique_id, fnc):
		"""
		Registers after new scene created event.
		:param unique_id: Unique name to register the event to.
		:param fnc: Function to call after new scene is created.

		"""

		if not self.events_register:
			self.events_register = events.EventsRegister()

		self.events_register.register_after_new_event(unique_id, fnc)
		self._callbacks.append(unique_id)

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

	def unregister_event(self, unique_id):
		"""
		Unregisters the event with the given unique id
		:param unique_id: Unique name to register the event to.

		"""

		if not self.events_register:
			self.events_register = events.EventsRegister()

		self.events_register.unregister_event(unique_id)


class MCAMayaWindow(common_windows.MCAMainWindow, MayaWindowEvents):
	def __init__(self, title='Maya Tool',
						ui_path=None,
						version='1.0.0',
						parent=MAYA_MAIN_WINDOW,
						show_window=True,
						events_register=False):
		super().__init__(title=title, ui_path=ui_path, version=version, parent=parent, show_window=show_window)

		# Start watching events
		self.installEventFilter(self)
		if events_register:
			self._callbacks = []
			# Start watching events
			self.events_register = events.EventsRegister() if events_register else None

		if show_window:
			self.show()


class MCAMayaQWidget(common_windows.ParentableWidget, MayaWindowEvents):
	def __init__(self, ui_path=None, style=None, parent=MAYA_MAIN_WINDOW, events_register=False):
		super().__init__(ui_path=ui_path, style=style, parent=parent)

		self.installEventFilter(self)
		if events_register:
			self._callbacks = []
			# Start watching events
			self.events_register = events.EventsRegister() if events_register else None

		self.show()

	def eventFilter(self, obj, event):
		if obj is self:
			if event.type() == qtcore.QEvent.Close:

				for callback in self._callbacks:
					self.unregister_event(callback)
				self.closeEvent(event)
				return True
			else:
				return super().eventFilter(obj, event)


