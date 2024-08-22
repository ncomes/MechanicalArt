#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.mya.modifiers import ma_decorators
from mca.mya.utils import namespace_utils, naming

from mca.mya.rigging.frag.components import frag_root

class FRAGDisplay(frag_root.FRAGRootSingle):
    _version = 1.0

    def remove(self):
        for _, display_layer in self.display_layers.items():
            try:
                pm.delete(display_layer)
            except:
                pass
        try:
            pm.delete(self.pynode)
        except:
            pass

    @property
    def display_layers(self):
        return_dict = {}
        if self.pynode.hasAttr('display_layers'):
            for display_layer in self.pynode.getAttr('display_layers'):
                display_layer_name = naming.get_basename(display_layer)
                return_dict[display_layer_name] = display_layer
        return return_dict

    @ma_decorators.keep_namespace_decorator
    def add_display_layer(self, display_layer_name):
        """
        Create a new display layer and register it with the FRAGDisplay node.

        :param str display_layer_name: Name of the display layer.
        :return: The newly minted display layer.
        :rtype: DisplayLayer
        """
        display_layer = self.display_layers.get(display_layer_name)

        if not display_layer:
            namespace_utils.set_namespace(self.pynode.namespace())

            cmds.select(None)
            display_layer = pm.createDisplayLayer(empty=True, name=display_layer_name)
            self.connect_nodes([display_layer], 'display_layers', merge_values=True)
        return display_layer

    def remove_layer(self, display_layer_name):
        """
        Remove a display layer by name from the managed display layers.

        :param str display_layer_name: Name of the display layer.
        """
        display_layer = self.display_layers.get(display_layer_name)
        if display_layer:
            pm.delete(display_layer)

    def add_objects_to_layer(self, display_layer_name, node_list, force=False):
        """
        Add objects to a managed display layer.

        :param str display_layer_name: Name of the display layer.
        :param list(PyNode) node_list: A list of PyNodes to add to the display layer.
        :param bool force: If we should forcibly move the objects into the display layer.
        :return: The display layer used.
        :rtype: DisplayLayer
        """
        if node_list and not isinstance(node_list, list):
            node_list = [node_list]

        display_layer = self.display_layers.get(display_layer_name) or self.add_display_layer(display_layer_name)

        for node in node_list:
            if not force and node.drawOverride.connections():
                continue
            display_layer.addMembers(node)
        return display_layer

    def get_layer_members(self, display_layer_name):
        """
        Return all nodes registered to a display layer.

        :param str display_layer_name: Name of the display layer.
        :return: A list of all the objects in the display layer.
        :rtype: list(PyNode)
        """
        display_layer = self.display_layers.get(display_layer_name)
        return_list = []
        if display_layer:
            return_list = display_layer.listMembers()
        return return_list

    def remove_layer_members(self, display_layer_name, node_list):
        """
        From a managed display layer remove the given nodes.

        :param str display_layer_name: Name of the display layer.
        :param list(PyNode) node_list: The list of objects to remove from the display layer.
        """
        display_layer = self.display_layers.get(display_layer_name)

        if display_layer:
            pm.editDisplayLayerMembers('defaultLayer', node_list, noRecurse=True)

    def layer_visible(self, display_layer_name, visible=True):
        """
        Toggles the managed display layer's visibiltiy setting.

        :param str display_layer_name: Name of the display layer.
        :param bool visible: What the layer visibility should be set to.
        """
        display_layer = self.display_layers.get(display_layer_name)
        if display_layer:
            display_layer.v.set(visible)

    def layer_template(self, display_layer_name, template=True):
        """
        Changes the managed display layer's state setting.

        :param str display_layer_name: Name of the display layer.
        :param bool template: What the layer state should be set to.
        """
        display_layer = self.display_layers.get(display_layer_name)
        if display_layer:
            display_layer.displayType.set(template) # 0 is default 1 is template 2 is reference

    def layer_reference(self, display_layer_name, reference=True):
        """
        Changes the managed display layer's state setting.

        :param str display_layer_name: Name of the display layer.
        :param bool reference: What the layer state should be set to.
        """
        display_layer = self.display_layers.get(display_layer_name)
        if display_layer:
            display_layer.displayType.set(2 if reference else 0)



