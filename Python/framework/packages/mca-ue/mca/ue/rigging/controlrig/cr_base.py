"""
Base class for all control rig functions
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.ue.rigging.controlrig import cr_config


class ControlRigBase:
    VERSION = '1.0.0'
    NODE_SIZE = [None, None]

    def __init__(self, control_rig, fnode):
        self.control_rig = control_rig
        self._fnode = fnode
        self.cr_controller = control_rig.get_controller_by_name(cr_config.RIGVMMODEL)

    @property
    def fnode(self):
        node = self._fnode
        if isinstance(node, str):
            top_level_graph = self.cr_controller.get_top_level_graph()
            return top_level_graph.find_node(node)
        return

    def get_grid_size(self):
        return self.NODE_SIZE

    def get_library_controller(self):
        library = self.control_rig.get_local_function_library()
        library_controller = self.control_rig.get_controller(library)
        return library_controller

    def get_hierarchy_controller(self):
        hierarchy = self.control_rig.hierarchy
        hierarchy_controller = hierarchy.get_controller()
        return hierarchy_controller

    def connect_from_sequence(self, source_node, target_node, letter='A'):
        self.cr_controller.add_link(f'{source_node}.{letter}', f'{target_node}.ExecuteContext')

    def add_comment_node(self, comment_text,
                         position=(0.000000, 0.000000),
                         size=(400.000000, 300.000000),
                         color=(0.000000, 0.000000, 0.000000, 1.000000),
                         node_name='',
                         setup_undo_redo=True,
                         print_python_command=False):
        """
        Creates a comment node in the graph connected to this node.

        :param str comment_text: Visible Text in the comment node
        :param list[float] position: two floats representing the 2d position in the graph
        :param list[float] size: two floats representing the 2d size in the graph
        :param list[float] color: four float num,bers representing RGBA
        :param str node_name: name of the comment node
        :param setup_undo_redo: sets up the undo/redo for the comment node
        :param print_python_command: TBD
        :return: Returns the created comment node
        :rtype: RigVMCommentNode
        """

        position = unreal.Vector2D(position[0], position[1])
        size = unreal.Vector2D(size[0], size[1])
        color = unreal.LinearColor(color[0], color[1], color[2], color[3])

        if node_name == '':
            node_name = f'{self.get_fname()}_Comment'

        self.cr_controller.set_node_selection([self.get_fname()])
        comment_node = self.cr_controller.add_comment_node(comment_text=comment_text,
                                                           position=position,
                                                           size=size,
                                                           color=color,
                                                           node_name=node_name,
                                                           setup_undo_redo=setup_undo_redo,
                                                           print_python_command=print_python_command)
        return comment_node

    def get_input_pins(self):
        return []

    def get_output_pins(self):
        return []

    def get_class(self):
        """
        Returns the Unreal class of this instance

        :return: Returns the Unreal class of this instance
        :rtype: self
        """

        return self.fnode.get_class()

    def get_default_object(self):
        """
        Returns the Unreal class default object

        :return: Returns the Unreal class default object
        :rtype: (CDO) of this type
        """

        return self.fnode.get_default_object()

    def get_editor_property(self, property_name):
        """
        Returns the value of any property visible to the editor

        :param str property_name: name of the property in the editor
        :return: Returns the value of any property visible to the editor
        :rtype: str
        """

        return self.fnode.get_default_object()

    def get_fname(self):
        """
        Returns the name of this instance

        :return: Returns the name of this instance
        :rtype: str
        """

        return self.fnode.get_fname()

    def get_full_name(self):
        """
        Returns the full name (class name + full path) of this instance

        :return: Returns the full name (class name + full path) of this instance
        :rtype: str
        """

        return self.fnode.get_full_name()

    def get_name(self):
        """
        Returns the name of this instance

        :return: Returns the name of this instance
        :rtype: str
        """

        return self.fnode.get_name()

    def get_outer(self):
        """
        Returns the outer object from this instance (if any)

        :return: Returns the outer object from this instance (if any)
        :rtype: unreal.Object
        """

        return self.fnode.get_outer()

    def get_outermost(self):
        """
        Returns the outermost object (the package) from this instance

        :return: Returns the outermost object (the package) from this instance
        :rtype: unreal.Object
        """

        return self.fnode.get_outermost()

    def get_package(self):
        """
        Returns the package directly associated with this instance

        :return: Returns the package directly associated with this instance
        :rtype: unreal.Object
        """

        return self.fnode.get_package()

    def get_path_name(self):
        """
        Returns the path name of this instance

        :return: Returns the path name of this instance
        :rtype: str
        """

        return self.fnode.get_path_name()

    def get_typed_outer(self, outer_type):
        """
        Returns the first outer object of the given type from this instance (if any)

        :param list(Class, type) outer_type: The class and the type of the outer object to be returned
        :return: Returns the first outer object of the given type from this instance (if any)
        :rtype: str
        """

        return self.fnode.get_typed_outer(outer_type)

    def get_world(self):
        """
        Returns the world associated with this instance (if any)

        :return: Returns the world associated with this instance (if any)
        :rtype: unreal.Object
        """

        return self.fnode.get_world()

    def is_package_external(self):
        """
        Returns true if this instance has a different package than its outer's package

        :return: Returns true if this instance has a different package than its outer's package
        :rtype: bool
        """

        return self.fnode.is_package_external()

    def modify(self, always_mark_dirty):
        """
        Returns inform that this instance is about to be modified (tracks changes for undo/redo if transactional)

        :param bool always_mark_dirty: If true, then this instance is always marked as dirty
        :return: Returns inform that this instance is about to be modified
        :rtype: bool
        """

        return self.fnode.modify(always_mark_dirty)

    def rename(self, name, outer=None):
        """
        rename this instance and/or change its outer

        :param str name: If true, then this instance is always marked as dirty
        :param ureal.Object outer: the outer object from this instance
        :return: Returns True if the rename was successful, False otherwise
        :rtype: bool
        """

        return self.fnode.rename(name=name, outer=outer)

    def set_editor_properties(self, properties):
        """
        set the value of any properties visible to the editor (from a name->value dict),
        ensuring that the pre/post change notifications are called

        :param map[str, object] properties: If true, then this instance is always marked as dirty
        """

        return self.fnode.set_editor_properties(properties)

    def set_editor_property(self, name, value):
        """
        set the value of any property visible to the editor,
        ensuring that the pre/post change notifications are called

        :param str name: editor property name
        :param property value value: the property to be set
        """

        return self.fnode.set_editor_property(name, value)

    def static_class(self):
        """
        Returns the Unreal class of this type

        :return: Returns the Unreal class of this type
        :rtype: cls
        """

        return self.fnode.static_class()

    def get_position(self):
        """
        Gets the position of this node in the control rig graph.

        :return: Returns the position of this node in the control rig graph.
        :rtype: Unreal.Vector2
        """

        return self.fnode.get_position()

    def get_size(self):
        """
        Gets the size of this node in the control rig graph.

        :return: Returns the size of this node in the control rig graph.
        :rtype: Unreal.Vector2
        """

        return self.fnode.get_size()

    def get_node_path(self):
        """
        Returns the node name of the node.

        :return: Returns the node name of the node.
        :rtype: str
        """

        return self.fnode.get_node_path()

    def connect_execute_content_nodes(self, source_node, target_node):
        """
        Connects the given source node to the given target node through the ExecuteContext pin.

        :param unreal.Object source_node: The source node.
        :param unreal.Object target_node: The target node.
        """

        source_str = f'{source_node.get_fname()}.ExecuteContext'
        target_str = f'{target_node.get_fname()}.ExecuteContext'
        self.cr_controller.add_link(source_str, target_str)

    def set_position(self, position):
        self.cr_controller.set_node_position(node=self.fnode,
                                      position=unreal.Vector2D(position[0], position[1]),
                                      setup_undo_redo=True,
                                      merge_undo_action=False,
                                      print_python_command=False)


