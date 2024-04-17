"""
purpose: managing mya internal events. Allows to connect listeners to special events.
"""

# System global imports
import functools
# Software specific imports
import maya.OpenMaya as om
import maya.OpenMayaAnim as OpenMayaAnim

#  python imports
from mca.common import log
from mca.common.modifiers import decorators, singleton
from mca.mya.modifiers import ma_decorators


logger = log.MCA_LOGGER


@decorators.add_metaclass(singleton.Singleton)
class EventsRegister:
	"""
	This static class lets perform script callbacks during events that arent available in the scriptJob events.
	To use it, you register a command with a unique ID. This will keep the callback ID for the command so you can
	unregister it by that name later.
	"""
	
	def __init__(self):
		self.events = {}
		self.paused_events = {}
		self.m_anim_message = OpenMayaAnim.MAnimMessage()
		self.m_event_message = om.MEventMessage()
		self.m_scene_message = om.MSceneMessage()
		self.m_model_message = om.MModelMessage()
		self.m_dag_message = om.MDagMessage()
		self.m_dg_message = om.MDGMessage()
		self.m_node_message = om.MNodeMessage()
		self.m_user_event_message = om.MUserEventMessage
		self.dag_message_types = ['kParentAdded', 'kParentRemoved', 'kChildAdded', 'kChildRemoved', 'kChildReordered',
									'kInstanceAdded', 'kInstanceRemoved']
	
	
	@property
	def parent_id(self):
		return self._parent_id
	
	@parent_id.setter
	def parent_id(self, value):
		self._parent_id = value
	
	
	# user defined events
	def register_user_event(self, callback_id):
		if not self.m_user_event_message.isUserEvent(callback_id):
			self.m_user_event_message.registerUserEvent(callback_id)
	
	def add_user_event(self, callback_id, unique_id, function):
		if self.m_user_event_message.isUserEvent(callback_id):
			self.unregister_event(unique_id)
			self.events[unique_id] = self.m_user_event_message.addUserEventCallback(callback_id,
																					self._wrap_event_function(function))
		return
	
	@ma_decorators.undo_decorator
	def post_user_event(self, callback_id, *args):
		if self.m_user_event_message.isUserEvent(callback_id):
			self.m_user_event_message.postUserEvent(callback_id, *args)
		return
	
	# end user defined
	
	def register_before_save_event(self, unique_id, function):
		"""
		Registers an API scene save event which fires when the scene attempts to save.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kBeforeSave, function)
		return
	
	def register_before_save_check_event(self, unique_id, function):
		"""
		Registers an API scene save event which fires when the scene attempts to save. It allows you to cancel
		the save when the event is fired.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(do_save, extra_data)
		"""
		
		self.register_scene_check_event(unique_id, self.m_scene_message.kBeforeSaveCheck, function)
		return
	
	def register_before_new_event(self, unique_id, function):
		"""
		Registers an API scene new event which fires when a new scene attempts to be created.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kBeforeNew, function)
		return
	
	def register_before_new_check_event(self, unique_id, function):
		"""
		Registers an API scene new event which fires when a new scene attempts to be created. It allows you to
		cancel the new when the event is fired.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(do_new, extra_data)
		"""
		
		self.register_scene_check_event(unique_id, self.m_scene_message.kBeforeNewCheck, function)
		return
	
	def register_after_new_event(self, unique_id, function):
		"""
		Registers an API scene new event which fires after a new scene has been created.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kAfterNew, function)
		return
	
	def register_before_open_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires when a scene attempts to be opened.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kBeforeOpen, function)
		return
	
	def register_before_open_check_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires when a scene attempts to be opened. It allows you to cancel
		the open when the event is fired.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(do_open, extra_data)
		"""
		
		self.register_scene_check_event(unique_id, self.m_scene_message.kBeforeOpenCheck, function)
		return
	
	def register_after_open_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires after a scene is opened.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kAfterOpen, function)
		return
	
	def register_before_import_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires before a scene is imported.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kBeforeImport, function)
		return
	
	def register_after_import_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires after a scene is imported.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kAfterImport, function)
		return
	
	def register_maya_exiting_event(self, unique_id, function):
		"""
		Registers an API scene open event which fires when Maya is exiting.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.register_scene_event(unique_id, self.m_scene_message.kMayaExiting, function)
		return
	
	def register_scene_event(self, unique_id, message_type, function):
		"""
		Registers an API scene event of the given message type.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		message_type: The type of message that the event should be registered for (see below)
		function: 	  Callback when event fires. Form: function(do_action, extra_data)

		Message types (prefix with self.m_scene_message.)
			kSceneUpdate 	Called after any operation that changes which files are loaded.
			kBeforeNew 	Called before a File > New operation.
			kAfterNew 	Called after a File > New operation.
			kBeforeImport 	Called before a File > Import operation.
			kAfterImport 	Called after a File > Import operation.
			kBeforeOpen 	Called before a File > Open operation.
			kAfterOpen 	Called after a File > Open operation.
			kBeforeExport 	Called before a File > Export operation.
			kAfterExport 	Called after a File > Export operation.
			kBeforeSave 	Called before a File > Save (or SaveAs) operation.
			kAfterSave 	Called after a File > Save (or SaveAs) operation.
			kBeforeReference 	Called before a File > Reference operation.
			kAfterReference 	Called after a File > Reference operation.
			kBeforeRemoveReference 	Called before a File > RemoveReference operation.
			kAfterRemoveReference 	Called after a File > RemoveReference operation.
			kBeforeImportReference 	Called before a File > ImportReference operation.
			kAfterImportReference 	Called after a File > ImportReference operation.
			kBeforeExportReference 	Called before a File > ExportReference operation.
			kAfterExportReference 	Called after a File > ExportReference operation.
			kBeforeUnloadReference 	Called before a File > UnloadReference operation.
			kAfterUnloadReference 	Called after a File > UnloadReference operation.
			kBeforeSoftwareRender 	Called before a Software Render begins.
			kAfterSoftwareRender 	Called after a Software Render ends.
			kBeforeSoftwareFrameRender 	Called before each frame of a Software Render.
			kAfterSoftwareFrameRender 	Called after each frame of a Software Render.
			kSoftwareRenderInterrupted 	Called when an interactive render is interrupted by the user.
			kMayaInitialized 	Called on interactive or batch startup after initialization.
			kMayaExiting 	Called just before Maya exits.
			kBeforeLoadReference 	Called before a File > LoadReference operation.
			kAfterLoadReference 	Called after a File > LoadReference operation.
			kBeforePluginLoad 	Called prior to a plugin being loaded.
			kAfterPluginLoad 	Called after a plugin is loaded.
			kBeforePluginUnload 	Called prior to a plugin being unloaded.
			kAfterPluginUnload 	Called after a plugin is unloaded.
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = {
			'callback': self.m_scene_message.addCallback(message_type, self._wrap_event_function(function)),
			'args': (unique_id, message_type, function),
			'register_method': self.register_scene_event,
			'message_type': self.m_scene_message}
		return
	
	def register_scene_check_event(self, unique_id, message_type, function):
		"""
		Registers an API scene event which allows you to cancel the action when the event is fired.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		message_type: The type of message that the event should be registered for (see below)
		function:	  Callback when event fires. Form: def function(do_action, extra_data)

		Message types (prefix with self.m_scene_message.)
			kBeforeNewCheck 	Called prior to File > New operation, allows user to cancel action.
			kBeforeOpenCheck 	Called prior to File > Open operation, allows user to cancel action.
			kBeforeSaveCheck 	Called prior to File > Save operation, allows user to cancel action.
			kBeforeImportCheck 	Called prior to File > Import operation, allows user to cancel action.
			kBeforeExportCheck 	Called prior to File > Export operation, allows user to cancel action.
			kBeforeLoadReferenceCheck 	Called before a File > LoadReference operation, allows user to cancel action.
			kBeforeReferenceCheck 	Called prior to a File > CreateReference operation, allows user to cancel action.
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_scene_message.addCheckCallback(message_type, self._wrap_event_function(function))
		return
	
	def register_selection_changed_event(self, unique_id, function):
		"""
		Registers an API model event which fires when the scene selection changes.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = {'callback': self.m_model_message.addCallback(self.m_model_message.kActiveListModified,
																				self._wrap_event_function(function)),
									'args': (unique_id, function),
									'register_method': self.register_selection_changed_event,
									'message_type': self.m_model_message}
		return
	
	def register_dag_changes_event(self, unique_id, function):
		"""
		Registers an API dag event which fires when the dag heirarchy changes.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(message_type, child, parent, extra_data)

		message_type is an enum with the following values =
		['kParentAdded',
		'kParentRemoved',
		'kChildAdded',
		'kChildRemoved',
		'kChildReordered',
		'kInstanceAdded',
		'kInstanceRemoved']
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_dag_message.addAllDagChangesCallback(self._wrap_event_function(function))
		return
	
	def register_node_added_event(self, unique_id, function, node_type="dependNode"):
		"""
		Registers an API dg event which fires when a node is added to the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(new_node, extra_data)
		node_type:	  Node filter for events. Events will only be fired if the object added is of this node type (or is
					  inherited from this node type)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_dg_message.addNodeAddedCallback(self._wrap_event_function(function), node_type)
		return
	
	def register_time_changed_event(self, unique_id, function):
		"""
		This method registers a callback that is called whenever the time changes in the dependency graph.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(new_node, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info('Registering {unique_id}')
		self.events[unique_id] = self.m_dg_message.addTimeChangeCallback(self._wrap_event_function(function))
		return
	
	def register_node_removed_event(self, unique_id, function, node_type="dependNode"):
		"""
		Registers an API dg event which fires when a node is removed from the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(removed_node, extra_data)
		node_type:	  Node filter for events. Events will only be fired if the object removed is of this node type (or is
					  inherited from this node type)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f'Registering {0}'.format(unique_id))
		self.events[unique_id] = self.m_dg_message.addNodeRemovedCallback(self._wrap_event_function(function), node_type)
		return
	
	def register_node_name_changed_event(self, unique_id, function):
		"""
		Registers an API node event which fires when a node is renamed in the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(node, old_name, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info('Registering {unique_id}')
		self.events[unique_id] = self.m_node_message.addNameChangedCallback(om.MObject(), self._wrap_event_function(function))
		return
	
	def register_keyframe_changed_event(self, unique_id, function):
		"""
		Registers an API node event which fires when an animation curve is edited in the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(node, anim_curve, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_anim_message.addAnimCurveEditedCallback(self._wrap_event_function(function))
		return
	
	def register_keyframe_edited_event(self, unique_id, function):
		"""
		Registers an API node event which fires when a node is keyframed in the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(node, keyframe, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_anim_message.addAnimKeyframeEditedCallback(self._wrap_event_function(function))
		return
	
	def register_node_keyframe_edited_event(self, unique_id, function, node):
		"""
		Registers an API node event which fires when a node is keyframed in the scene.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(node, keyframe, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_anim_message.addNodeAnimKeyframeEditedCallback(node, self._wrap_event_function(
			function))
		return
	
	def register_attribute_changed_event(self, unique_id, function, node):
		"""
		Registers an API node event which fires when attributes of the node in the scene are changed.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(message, plug, other_plug, extra_data)
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_node_message.addAttributeChangedCallback(node.__apimobject__(), self._wrap_event_function(function))
		return
	
	def register_node_about_to_delete_event(self, unique_id, function, node):
		"""
		Registers an API node event which fires when the node is about to be deleted.

		:param unique_id: Unique name to register the event to. Use this name to unregister the event later.
		:param function: Callback when event fires. Form: def function(message, plug, other_plug, extra_data)
		:param node: Valid PyNode that inherits from pm.nt.DependNode
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = self.m_node_message.addNodeAboutToDeleteCallback(node.__apimobject__(), self._wrap_event_function(function))
	
	def register_tool_changed_event(self, unique_id, function):
		"""
		Registers an API event which fires when the user changes tools.

		:param unique_id: Unique name to register the event to. Use this name to unregister the event later.
		:param function: Callback when event fires. This event passes None to the callback.
		"""
		
		self.unregister_event(unique_id)
		self.events[unique_id] = self.m_event_message.addEventCallback('ToolChanged', function)
	
	def register_event_event(self, unique_id, function, event_name):
		"""
		Registers an API node event which fires when the named event occurs.

		unique_id: 	  Unique name to register the event to. Use this name to unregister the event later.
		function:	  Callback when event fires. Form: def function(node, keyframe, extra_data)
		event_name:	  Event to register the callback for
		"""
		
		self.unregister_event(unique_id)
		logger.info(f"Registering {unique_id}")
		self.events[unique_id] = om.MEventMessage.addEventCallback(event_name, self._wrap_event_function(function))
		return
	
	def unregister_event(self, unique_id):
		"""
		Unregisters the event with the given unique id

		unique_id: 	  Unique name to unregister the event from.
		"""
		
		if unique_id in self.events:
			logger.info(f"Unregistering {unique_id}")
			if isinstance(self.events[unique_id], dict):
				callback = self.events[unique_id]['callback']
			else:
				callback = self.events[unique_id]
			self.m_scene_message.removeCallback(callback)
			self.events.pop(unique_id)
		return
	
	def pause_event(self, unique_id):
		if unique_id in self.events:
			event_type = self.events[unique_id]['message_type']
			event_type.removeCallback(self.events[unique_id]['callback'])
			self.paused_events[unique_id] = self.events[unique_id]
			self.events.pop(unique_id)
		return
	
	def resume_event(self, unique_id):
		if unique_id in self.paused_events:
			event_data = self.paused_events[unique_id]
			event_data['register_method'](*event_data['args'])
			self.paused_events.pop(unique_id)
		return
	
	def _wrap_event_function(self, func):
		"""
		Wrap the passed function in self._logged_event
		intended for use with event functions

		:param func: event function to wrap
		:return: wrapped function
		"""
		
		return functools.partial(self._logged_event, func)
	
	@staticmethod
	def _logged_event(func, *args, **kwargs):
		"""
		Wrapper function. Log the event when it's being called and where it's coming from.
		Not intended for use outside of _wrap_event_function

		:param func: function attached to the event
		:param args: args for the function
		:param kwargs: kwargs for the function
		:return: func result signature
		"""
		
		logger.info(f'Event Starting: {repr(func)}')
		result = func(*args, **kwargs)
		logger.info(f'Event Complete: {repr(func)}')
		return result

