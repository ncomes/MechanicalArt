"""
Interacts an Unreal Control Rig Sequence Node
"""

# mca python imports
# software specific imports
# mca python imports
from mca.ue.rigging.controlrig import cr_nodes, cr_config, cr_pins


SCRIPT_STRUCT_PATH = '/Script/RigVM.RigVMFunction_Sequence'
BASE_NODE_NAME = 'RigVMFunction_Sequence'


class SequenceNode(cr_pins.PinsBase):
    VERSION = '1.0.0'
    NODE_SIZE = [1, 5]
    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    @classmethod
    def spawn(cls, control_rig, side='center', region='seq', position=(192.0, -1296.0), number_of_pins=2):
        controller = control_rig.get_controller_by_name(cr_config.RIGVMMODEL)
        node_name = f'{BASE_NODE_NAME}_{side}_{region}'
        node = cr_nodes.create_control_rig_node(control_rig=control_rig,
                                       position=position,
                                       script_struct_path=SCRIPT_STRUCT_PATH,
                                       node_name=node_name)
        if number_of_pins > 2:
            for i in range(number_of_pins - 2):
                controller.add_aggregate_pin(BASE_NODE_NAME, '', '')
        return cls(control_rig, fnode=node_name)

    def get_pins(self):
        """
        Returns all the pins on the sequence node.

        :return: Returns all the pins on the sequence node.
        :rtype: list[RigVMPin]
        """

        return self.fnode.get_pins()

    def number_of_pins(self):
        """
        Returns the number of pins on the sequence node.

        :return: Returns the number of pins on the sequence node.
        :rtype: int
        """

        return len(self.fnode.get_aggregate_outputs())

    def get_empty_pins(self):
        """
        Returns a list of empty pins.

        :return: Returns a list of empty pins.
        :rtype: list[RigVMPin]
        """

        empty_list = []
        # Get all the pins in the sequence node.
        pins = self.get_pins()
        # We don't need the input pin, so lets remove it.
        pins.pop(0)
        # Get all the links in the sequence node.  This gets us all the connections as pins on the sequence node.
        links = [x.get_source_pin() for x in self.fnode.get_links()]
        # We don't need the input link, so lets remove it.
        links.pop(0)
        # Loop through and see if the pins match the links.  If they don't match, we'll add it to the list.
        for x in range(len(pins)):
            if pins[x] not in links:
                empty_list.append(pins[x])
        return empty_list

    def get_next_empty_pin(self):
        """
        Returns the next empty pin on the sequence node.

        :return: Returns the next empty pin on the sequence node.
        :rtype: RigVMPin
        """

        empty_pins = self.get_empty_pins()
        if not empty_pins:
            return []
        return empty_pins[0]

    def get_last_empty_pin(self):
        """
        Returns the last empty pin on the sequence node.

        :return: Returns the last empty pin on the sequence node.
        :rtype: RigVMPin
        """

        empty_pins = self.get_empty_pins()
        if not empty_pins:
            return []
        return empty_pins[-1]

    def add_pin(self):
        self.cr_controller.add_aggregate_pin(self.fnode.get_fname(), '')

    def add_pins(self, number_of_pins=1):
        for i in range(number_of_pins):
            self.cr_controller.add_aggregate_pin(self.fnode.get_fname(), '')

    def list_target_connections(self):
        return self.fnode.get_linked_target_nodes()

    def list_source_connections(self):
        return self.fnode.get_linked_source_nodes()

    def list_connections(self, source=True, target=True, **kwargs):
        t = kwargs.get('target', target)
        s = kwargs.get('source', source)

        connection_list = []
        if t:
            connection_list.extend(self.list_target_connections())
        if s:
            connection_list.extend(self.list_source_connections())

        return connection_list

    def link_to_next_empty_pin(self, target_node):
        pin = self.get_next_empty_pin()

        if pin:
            if not isinstance(target_node, str):
                target_node = target_node.get_fname()
            pin_letter = pin.get_fname()
            self.cr_controller.add_link(f'{self.get_fname()}.{pin_letter}', f'{target_node}.ExecuteContext')

        return pin

    def link_to_last_empty_pin(self, target_node):
        pin = self.get_last_empty_pin()

        if pin:
            if not isinstance(target_node, str):
                target_node = target_node.get_fname()
            pin_letter = pin.get_fname()
            self.cr_controller.add_link(f'{self.get_fname()}.{pin_letter}', f'{target_node}.ExecuteContext')

        return pin

