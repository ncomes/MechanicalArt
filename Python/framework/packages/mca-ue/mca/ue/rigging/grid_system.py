"""
Organizes nodes into the graph editor
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.rigging.controlrig import cr_pins, cr_comment

logger = log.MCA_LOGGER

GROUP_TYPES = ['input', 'main', 'output']

class GridNode:
    """
    Information about a node in the Control Rig grid
    """
    def __init__(self, node, grid_size=None):
        self.node = node
        self.grid_size = grid_size

    @property
    def size(self):
        """
       Returns the grid size of a node, based on 128x128 blocks.

        :return: Returns the grid size of a node, based on 128x128 blocks.
        :rtype: list(int)
        """

        grid_size = self.grid_size
        if not grid_size:
            grid_size = self.node.get_grid_size()
        if not grid_size[0] or not grid_size[1]:
            logger.warning(f'No Grid Size found for {self.get_fname}')
            return [1, 1]
        return grid_size

    def get_fname(self):
        """
        Returns the string node name.

        :return: Returns the string representation of the node name.
        :rtype: str
        """

        return str(self.node.get_fname())

    @property
    def unit_size(self):
        """
        Returns the actual size of the grid node, based on 128x128 blocks.

        :return: Returns the actual size of the grid node, based on 128x128 blocks.  ex: [1, 1] == [128, 128]
        :rtype: list[int]
        """

        if not self.size:
            return [128, 128]
        return [self.size[0] * 128,  self.size[1] * 128]


class CommentNodeSize:
    """
    Tracks the size of the comment node based on the size of the rows and columns.
    """

    def __init__(self, data=None):
        self.data = data
        if not self.data:
            self.data = {'rows': {}, 'columns': {}}  # Actual sizes of the rows and columns

    def add_row(self, row, size):
        """
        Adds a row and its size to the comment node size.
        It keeps track of each row size, so we can calculate the longest row.

        :param int row: the row number
        :param int size: The actual size of the row.
        """

        if not self.data['rows'].get(row, None):
            self.data['rows'].update({row: size})
        else:
            old_size = self.data['rows'].get(row, 0)
            self.data['rows'].update({row: old_size + size})

    def add_column(self, group_type, column, size):
        """
        Adds a column and its size to the comment node size.
        It keeps track of each column size, so we can calculate the longest row.

        :param str group_type: The type of the column. Either 'input' or 'output' or 'main'.
        :param int column: the column number
        :param int size: The actual size of the column.
        """

        if group_type not in self.data['columns'].keys():
            self.data['columns'].update({group_type: {}})

        if not self.data['columns'][group_type].get(column, None):
            self.data['columns'][group_type].update({column: size})
        else:
            old_size = self.data['columns'][group_type].get(column, 0)
            self.data['columns'][group_type].update({column: old_size + size})

    def longest_column(self):
        """
        Returns the longest column.

        :return: Returns the longest column.
        :rtype: int
        """

        longest_column = 0
        for group_type in GROUP_TYPES:
            if not group_type in self.data['columns'].keys():
                continue
            for column, size in self.data['columns'][group_type].items():
                if size > longest_column:
                    longest_column = size
        return longest_column

    def longest_row(self):
        """
        Returns the longest row.
        :return:  Returns the longest row.
        :rtype: int
        """

        longest_row = 0
        for row, size in self.data['rows'].items():
            if size > longest_row:
                longest_row = size
        return longest_row


class GridNodeCollection:
    """
    This organizes a collection of nodes that all relate together.
    Organizes nodes into a grid.  There are 3 "group types" of nodes: input, main, and output.
    The nodes are organized into columns and rows based on the group type.
    We use a Comment node to track the size of all the nodes.
    """

    def __init__(self, control_rig, main_node, controller=None):
        self.control_rig = control_rig
        self.comment_node_size = CommentNodeSize()
        self.node = GridNode(main_node)
        self.grid_buffer = 128
        self.grid_list = self.start_grid_list()
        self.controller = controller
        if not self.controller:
            self.controller = main_node.cr_controller
        self.comment_node = None

    def start_grid_list(self):
        """
        Adds the first main node to the grid list.

        :return: Returns the master list of all the nodes in the grid for this collection
        :rtype: list(dict)
        """

        grid_list = []
        item = self.node
        position = self.get_main_position(self.node.unit_size, [0, 0])
        item_dict = {}
        item_dict.update({item: {}})
        item_dict[item].update({'position': position})
        item_dict[item].update({'size': item.unit_size})
        item_dict[item].update({'row_column': [0, 0]})

        grid_list.append(item_dict)
        self.comment_node_size.add_row(row=0, size=item.unit_size[0])
        self.comment_node_size.add_column(group_type=GROUP_TYPES[1], column=0, size=item.unit_size[1])
        return grid_list

    def add_grid_node(self, node, group_type, row_column=(0, 0)):
        """
        adds a node to the grid list, which organizes it into a column and row based on the group type.

        :param FRAG Node node: A node that is part of the collection and is related to the main node.
        :param str group_type: The type of the node. Either 'input' or 'output' or 'main'.
        :param list(int) row_column: The row and column of the node in the grid.
        """

        item = GridNode(node)
        item_dict = {}
        item_dict.update({item: {}})

        if group_type == GROUP_TYPES[0]:
            position = self.get_input_position(item.unit_size, row_column)
            item_dict[item].update({'position': position})
            item_dict[item].update({'size': item.unit_size})
            item_dict[item].update({'row_column': row_column})
            self.grid_list.append(item_dict)

            self.comment_node_size.add_row(row=row_column[0], size=item.unit_size[0])
            self.comment_node_size.add_column(group_type=GROUP_TYPES[0], column=row_column[1], size=item.unit_size[1])

        elif group_type == GROUP_TYPES[-1]:
            position = self.get_output_position(item.unit_size, row_column)
            item_dict[item].update({'position': position})
            item_dict[item].update({'size': item.unit_size})
            item_dict[item].update({'row_column': row_column})

            self.grid_list.append(item_dict)
            self.comment_node_size.add_row(row=row_column[0], size=item.unit_size[0])
            self.comment_node_size.add_column(group_type=GROUP_TYPES[-1], column=row_column[1], size=item.unit_size[1])

        elif group_type == GROUP_TYPES[1]:
            position = self.get_main_position(item.unit_size, row_column)
            item_dict[item].update({'position': position})
            item_dict[item].update({'size': item.unit_size})
            item_dict[item].update({'row_column': row_column})

            self.grid_list.append(item_dict)
            self.comment_node_size.add_row(row=row_column[0], size=item.unit_size[0])
            self.comment_node_size.add_column(group_type=GROUP_TYPES[1], column=row_column[1], size=item.unit_size[1])
        else:
            logger.warning(f'Invalid Grid Position: {group_type}')
            return

    def get_input_position(self, unit_size, row_column):
        """
        Returns the position of an input node in the grid.

        :param list[int] unit_size: The size of the actual input node
        :param list[int] list(int) row_column: The row and column of the node in the grid.
        :return: Returns the position of the input node in the grid.
        :rtype: list(int)
        """

        row = row_column[0] + 1
        column = row_column[1]

        unit_x = (unit_size[0] * (row * -1)) + (self.grid_buffer * -1)
        if column == 0:
            unit_y = unit_size[1] * column
        else:
            unit_y = (unit_size[1] * column)
        return [unit_x, unit_y]

    def get_main_position(self, unit_size, row_column):
        """
        Returns the position of the main node in the grid.

        :param list[int] unit_size: The size of the actual main node
        :param list(int) row_column: The row and column of the node in the grid.
        :return: Returns the position of the main node in the grid.
        :rtype: list(int)
        """

        if row_column[0] == 0:
            unit_x = unit_size[0] * row_column[0]
        else:
            unit_x = (unit_size[0] * (row_column[0] * -1)) + self.grid_buffer
        if row_column[1] == 0:
            unit_y = unit_size[1] * row_column[1]
        else:
            unit_y = (unit_size[1] * row_column[1])
        return [unit_x, unit_y]

    def get_output_position(self, unit_size, row_column):
        """
        Returns the position of the output node in the grid.

        :param list[int] unit_size: The size of the actual main node
        :param list(int) row_column: The row and column of the node in the grid.
        :return: Returns the position of the output node in the grid.
        :rtype: list(int)
        """

        start_x = self.node.unit_size[0]

        row = row_column[0] + 1
        column = row_column[1]

        if row == 0:
            unit_x = unit_size[0] * row + (self.grid_buffer + start_x)
        else:
            unit_x = (unit_size[0] * row) + (self.grid_buffer + start_x)
        if column == 0:
            unit_y = unit_size[1] * column
        else:
            unit_y = (unit_size[1] * column)
        return [unit_x, unit_y]

    def get_a_position(self, node):
        """
        Returns the position of the node in the grid.

        :param FRAG Node node: The node to get the position
        :return: Returns the position of the node in the grid.
        :rtype: list(int)
        """

        if isinstance(node, cr_pins.PinsBase):
            logger.warning(f'Invalid node. {node}')
            return
        node_name = node.get_fname()
        for item in self.grid_list:
            grid_item = list(item.keys())[0]
            position = item[grid_item].get('position', None)
            if grid_item.get_fname() == node.get_fname():
                return position

    def set_all_positions(self):
        """
        Sets all the positions of the nodes in the collection, but not the comment node.
        """

        for item in self.grid_list:
            grid_item = list(item.keys())[0]
            position = item[grid_item].get('position', None)
            grid_item.node.set_position(position)

    def add_comment_node(self, comment_text,
                         color=(0.000000, 0.000000, 0.000000, 1.000000),
                         side='center',
                         region='comment'):
        """
        Creates a comment node in the graph connected to this node.

        :param str comment_text: Visible Text in the comment node
        :param list[float] color: four float num,bers representing RGBA
        :return: Returns the created comment node
        :rtype: RigVMCommentNode
        """

        position = self.comment_position()
        size = self.comment_size()

        nodes = []
        for item in self.grid_list:
            nodes.append(list(item.keys())[0].get_fname())

        comment_node = cr_comment.CommentNode.spawn(control_rig=self.control_rig,
                                                    controller=self.controller,
                                                    comment_text=comment_text,
                                                    node_list=nodes,
                                                    position=[position[0], position[1]],
                                                    size=[size[0], size[1]],
                                                    color=color,
                                                    side=side,
                                                    region=region)

        comment_node = GridNode(comment_node)
        comment_dict = {}
        comment_dict.update({comment_node: {}})
        comment_dict[comment_node].update({'position': position})
        comment_dict[comment_node].update({'size': comment_node.unit_size})

        self.comment_node = comment_dict

        return comment_node

    def get_box_positions(self):
        """
        Returns the actual position of the node.

        :return: Returns the actual position of the node.
        :rtype: list(float)
        """

        positions = []
        # [+x, +y, -x, -y]
        pos_x = 0
        pos_y = 0
        neg_x = 0
        neg_y = 0
        for item in self.grid_list:
            position = item[list(item.keys())[0]].get('position', None)
            positions.append(position)

        for pos in positions:
            if pos[0] > pos_x:
                pos_x = pos[0]
            if pos[0] < neg_x:
                neg_x = pos[0]
            if pos[1] > pos_y:
                pos_y = pos[1]
            if pos[1] < neg_y:
                neg_y = pos[1]

        return [pos_x, pos_y, neg_x, neg_y]

    def comment_size(self):
        """
        Returns the size of the comment node.

        :return: returns the size of the comment node.
        :rtype: list(int)
        """

        row = self.comment_node_size.longest_row()
        column = self.comment_node_size.longest_column()
        return [row, column]

    def comment_position(self):
        """
        Returns the position of the comment node.

        :return: Returns the position of the comment node
        :rtype: list(float)
        """

        box_positions = self.get_box_positions()
        return [box_positions[2] - 70, box_positions[3] - 70]

    def move_collection(self, position=(0, 0)):
        """
        Moves the collection to the specified position.  It is based on the comment node position.

        :param list(int) position: New position of the collection
        """

        comment_node = list(self.comment_node.keys())[0]
        comment_position = self.comment_node[list(self.comment_node.keys())[0]].get('position', None)
        comment_position_x = comment_position[0]
        comment_position_y = comment_position[1]
        if not position:
            logger.warning(f'Invalid position. {position}, There might not be a comment node.')
            return

        self.comment_node[comment_node].update({'position': position})

        comment_node.node.set_position(position=[position[0], position[1]])

        for item in self.grid_list:
            grid_item = list(item.keys())[0]
            item_pos_x = item[grid_item].get('position', None)[0]
            item_pos_y = item[grid_item].get('position', None)[1]

            if item_pos_x is None or item_pos_y is None:
                logger.warning('Not Moving!  A Value is missing')
                continue

            dif_x = abs(comment_position_x - item_pos_x)
            dif_y = abs(comment_position_y - item_pos_y)
            new_position_x = position[0] + dif_x
            new_position_y = position[1] + dif_y
            item[grid_item].update({'position': [new_position_x, new_position_y]})

            logger.warning(f'Moving {grid_item.get_fname()} to {new_position_x}, {new_position_y}')

        self.set_all_positions()

