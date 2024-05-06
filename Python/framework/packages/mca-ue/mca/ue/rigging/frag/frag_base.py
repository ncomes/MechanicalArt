"""
Module that sets up the environment variables for MAT
"""

# mca python imports
import os

# software specific imports
import unreal

# mca python imports
from mca.ue.rigging.controlrig import cr_base


class UEFRAGNode(cr_base.ControlRigBase):
    def __init__(self, control_rig, fnode):
        super().__init__(control_rig, fnode)

    # @staticmethod
    # def create(control_rig, node_name=None):
    #     return UEFRAGNode(control_rig, node_name=node_name)

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
