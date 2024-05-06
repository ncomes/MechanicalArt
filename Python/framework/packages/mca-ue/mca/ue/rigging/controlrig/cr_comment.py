"""
Interacts an Unreal Control Rig "Comment" Node
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.rigging.controlrig import cr_base

logger = log.MCA_LOGGER

SCRIPT_STRUCT_PATH = 'Comment'
BASE_NODE_NAME = 'EdGraphNode_Comment'


class CommentNode(cr_base.ControlRigBase):
    VERSION = '1.0.0'
    NODE_SIZE = [6, 6]

    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)


    @classmethod
    def spawn(cls, control_rig,
                    controller,
                    comment_text,
                    node_list=(),
                    position=(0.000000, 0.000000),
                    size=(400.000000, 300.000000),
                    color=(0.000000, 0.000000, 0.000000, 1.000000),
                    setup_undo_redo=True,
                    print_python_command=False,
                    side='center',
                    region='comment'):
        """
        Creates a comment node in the graph connected to this node.

        :param str comment_text: Visible Text in the comment node
        :param list[float] position: two floats representing the 2d position in the graph
        :param list[float] size: two floats representing the 2d size in the graph
        :param list[float] color: four float num,bers representing RGBA
        :param setup_undo_redo: sets up the undo/redo for the comment node
        :param print_python_command: TBD
        :return: Returns the created comment node
        :rtype: RigVMCommentNode
        """

        position = unreal.Vector2D(position[0], position[1])
        size = unreal.Vector2D(size[0], size[1])
        color = unreal.LinearColor(color[0], color[1], color[2], color[3])

        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        if node_list:
            controller.set_node_selection(node_list)
        comment_node = controller.add_comment_node(comment_text=comment_text,
                                                           position=position,
                                                           size=size,
                                                           color=color,
                                                           node_name=node_name,
                                                           setup_undo_redo=setup_undo_redo,
                                                           print_python_command=print_python_command)
        return cls(control_rig, fnode=node_name)

