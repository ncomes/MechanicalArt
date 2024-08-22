#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to base FRAGNodes and their usage.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.mya.rigging.frag.components import frag_root

class FRAGMesh(frag_root.FRAGRootSingle):
    _version = 1.0

    def remove(self):
        mesh_group = self.mesh_group
        if mesh_group:
            pm.delete(mesh_group)
        try:
            pm.delete(self.pynode)
        except:
            pass

    # Handles all the managed mesh groups.
    @property
    def mesh_group(self):
        if self.pynode.hasAttr('mesh_group'):
            return self.pynode.getAttr('mesh_group')


    @mesh_group.setter
    def mesh_group(self, mesh_group):
        self.connect_node(mesh_group, 'mesh_group', 'frag_parent')
        
    def add_mesh_group(self):
        mesh_group = self.mesh_group
        if not self.mesh_group:
            mesh_group = self._create_managed_group('mesh_group')
            mesh_group.setParent(self.frag_parent.add_asset_group())

            self.mesh_group = mesh_group

        if mesh_group:
            frag_display_node = self.get_frag_root().frag_display
            if frag_display_node:
                asset_name = self.frag_parent.asset_name
                display_layer_name = f'{asset_name}_meshes_dl'
                frag_display_node.add_display_layer(display_layer_name)
                frag_display_node.add_objects_to_layer(display_layer_name, mesh_group)
        return mesh_group

    @property
    def skins_group(self):
        if self.pynode.hasAttr('skins_group'):
            return self.pynode.getAttr('skins_group')

    @skins_group.setter
    def skins_group(self, skins_group):
        self.connect_node(skins_group, 'skins_group', 'frag_parent')

    def add_skins_group(self):
        skins_group = self.skins_group
        if not self.skins_group:
            skins_group = self._create_managed_group('skins_group')
            skins_group.setParent(self.add_mesh_group())
            self.skins_group = skins_group
        return skins_group

    @property
    def blendshape_group(self):
        if self.pynode.hasAttr('blendshape_group'):
            return self.pynode.getAttr('blendshape_group')

    @blendshape_group.setter
    def blendshape_group(self, blendshape_group):
        self.connect_node(blendshape_group, 'blendshape_group', 'frag_parent')

    def add_blendshape_group(self):
        blendshape_group = self.blendshape_group
        if not self.blendshape_group:
            blendshape_group = self._create_managed_group('blendshape_group')
            blendshape_group.setParent(self.add_mesh_group())
            self.blendshape_group = blendshape_group
        return blendshape_group

