"""
Base class for all control rig functions
"""

# mca python imports
# software specific imports
import unreal
# mca python imports
from mca.common import log
from mca.ue.rigging.controlrig import cr_base

logger = log.MCA_LOGGER


class PinsBase(cr_base.ControlRigBase):
    def __init__(self, control_rig, fnode):
        super().__init__(control_rig=control_rig, fnode=fnode)

    def get_pins(self):
        """
        Returns all the pins on the sequence node.

        :return: Returns all the pins on the sequence node.
        :rtype: list[RigVMPin]
        """

        return self.fnode.get_pins()

    def get_empty_source_pins(self):
        """
        Returns a list of empty pins.

        :return: Returns a list of empty pins.
        :rtype: list[RigVMPin]
        """

        empty_list = []
        # Get all the pins in the sequence node.
        pins = self.get_pins()

        # Get all the links in the sequence node.  This gets us all the connections as pins on the sequence node.
        links = [x.get_source_node() for x in self.fnode.get_links()]
        # We don't need the input link, so lets remove it.
        # Loop through and see if the pins match the links.  If they don't match, we'll add it to the list.
        for x in range(len(pins)):
            if pins[x] not in links:
                empty_list.append(pins[x])
        return empty_list

    def get_pin_by_name(self, pin_name):
        """
        Returns a pin by name.

        :param str pin_name: Name of the pin.
        :return: Returns a pin by name.
        :rtype: RigVMPin
        """

        pins = self.get_pins()
        found = []
        if not pins:
            return
        for pin in pins:
            if str(pin_name) in str(pin.get_display_name()):
                found.append(pin)
        return found


    def list_target_connections(self):
        """
        Returns a list of all the nodes connected from the right side.

        :return: Returns a list of all the nodes connected from the right side.
        :rtype: list[unreal.RigVMNode]
        """

        return self.fnode.get_linked_target_nodes()

    def list_source_connections(self):
        """
        Returns a list of all the nodes connected from the left side.

        :return: Returns a list of all the nodes connected from the left side.
        :rtype: list[unreal.RigVMNode]
        """

        return self.fnode.get_linked_source_nodes()

    def list_connections(self, source=True, target=True, **kwargs):
        """
        Returns a list of all connected nodes.

        :return: Returns a list of all connected nodes.
        :rtype: list[unreal.RigVMNode]
        """

        t = kwargs.get('target', target)
        s = kwargs.get('source', source)

        connection_list = []
        if t:
            connection_list.extend(self.list_target_connections())
        if s:
            connection_list.extend(self.list_source_connections())

        return connection_list

    def set_expand_pin(self, node_name, pin_name, expand=True):
        self.cr_controller.set_pin_expansion(pin_path=f'{node_name}.{pin_name}', is_expanded=expand)

    def set_rig_element_pin(self, node_name, pin_name, in_type, other_name):
        self.cr_controller.set_pin_default_value(f'{node_name}.{pin_name}.Type', in_type, False)
        self.cr_controller.set_pin_default_value(f'{node_name}.{pin_name}.Name', other_name, False)

    def link_flag(self, source_pin, target_pin):
        """

        :param RigVMPin source_pin: The source pin.  The pin from the node.
        :param unreal.RigVMPin target_pin: The target pin.  The pin into the node.
        """

        source_path = source_pin.get_pin_path()
        target_path = target_pin.get_pin_path()
        self.cr_controller.add_link(source_path, target_path)

    def add_link(self, pin_name, target, target_pin):
        if isinstance(target, PinsBase) and isinstance(target_pin, str):
            target = f'{target.get_fname()}.{target_pin}'

        elif isinstance(target, str) and '.' in target:
            target = target

        elif isinstance(target, str) and isinstance(target_pin, str):
            target = f'{target}.{target}'

        else:
            logger.warning('Unable to link nodes, It looks like the source or target link does not exist.')
            return

        source = f'{self.get_fname()}.{pin_name}'
        self.cr_controller.add_link(source, target)


