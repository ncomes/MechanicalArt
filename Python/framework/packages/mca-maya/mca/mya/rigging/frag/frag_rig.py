#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
# mca python imports
import pymel.core as pm
# mca python imports
from mca.mya.modifiers import ma_decorators
from mca.common.utils import lists
from mca.mya.rigging.flags import frag_flag
from mca.mya.utils import attr_utils, dag
# Internal module imports
from mca.mya.rigging.frag import frag_base, frag_root, skeletal_mesh, display_layers, keyable_component
from mca.mya.utils import namespace


def get_frag_rig(node):
    """
    From any node within the rig dag hierarchy find the all grp and return the fragParent connection. This should be the
    rig in all cases.

    :param Transform node:
    :return: The FRAGRig driving this hierarchy.
    :rtype: FRAGRig
    """

    # If we have the FRAGRoot
    if node.hasAttr('fragType') and node.getAttr('fragType') == 'FRAGRoot':
        return frag_base.FRAGNode(node)

    # If it is a frag child, get parent FRAGNode, root, then rig.
    if node.hasAttr('fragParent'):
        wrapped_frag_node = frag_base.FRAGNode(node.getAttr('fragParent'))
        wrapped_frag_root = frag_root.get_frag_root(wrapped_frag_node)
        return wrapped_frag_root.get_rig()

    # if it is in the hierarchy but not a frag node, search for the frag root.
    all_grp = dag.get_absolute_parent(node)
    if all_grp.hasAttr('fragParent'):
        return frag_base.FRAGNode(all_grp.getAttr('fragParent'))

def get_frag_rigs():
    """
    Returns a list of all the frag rigs in the scene.

    :return: Returns a list of all the frag rigs in the scene.
    :rtype: list(FRAGRig)
    """

    all_roots = frag_root.get_all_frag_roots()
    all_frag_rigs = list(map(lambda x: x.get_rig(), all_roots))
    all_frag_rigs = list(set(all_frag_rigs))
    return all_frag_rigs

class FRAGRig(frag_base.FRAGNode):
    VERSION = 1

    @staticmethod
    @ma_decorators.keep_namespace_decorator
    def create(frag_parent):

        # Set Namespace
        root_namespace = frag_parent.namespace().split(':')[0]
        namespace.set_namespace(root_namespace, check_existing=False)

        if not frag_parent.hasAttr('isFragRoot'):
            raise AttributeError('{0}: FRAG parent is not the Frag Root Component')

        # Create the FRAG Rig Network Node
        node = frag_base.FRAGNode.create(frag_parent, FRAGRig.__name__, FRAGRig.VERSION)

        # Get the asset name and root joint from the FRAG Root
        asset_name = frag_parent.assetName.get()
        root_joint = frag_parent.rootJoint.get()

        # Add Attributes
        node.addAttr('all', at='message')
        node.addAttr('doNotTouch', at='message')
        node.addAttr('flagsAll', at='message')
        node.addAttr('rigVersion', at='double', dv=0)
        node.addAttr('rigTemplate', dt='string')
        node.addAttr('rigScale', type='float', dv=1.0)

        # Create the rig hierarchy groups
        all_grp = pm.group(em=True, name=asset_name + '_all')
        all_grp.sx >> node.rigScale
        dnt_grp = pm.group(em=True, name='DO_NOT_TOUCH')
        flags_all_grp = pm.group(em=True, name='flags_all')

        # Connect the rig hierarchy groups to the FRAGRig
        node.connect_node(all_grp, 'all', 'fragParent')
        node.connect_node(dnt_grp, 'doNotTouch', 'fragParent')
        node.connect_node(flags_all_grp, 'flagsAll', 'fragParent')

        # Parent groups to finish the hierarchy
        pm.parent([dnt_grp, flags_all_grp, root_joint], all_grp)

        # Check for skin grp and parent
        sk_mesh = frag_parent.get_frag_children(of_type=skeletal_mesh.SkeletalMesh)
        if sk_mesh:
            skin_grp = sk_mesh[0].grpSkins.get()
            skin_grp.setParent(all_grp)

            blendshape_grp = sk_mesh[0].get_grp_blendshapes()
            if blendshape_grp:
                blendshape_grp.setParent(all_grp)
            if not blendshape_grp.listRelatives(c=True):
                pm.delete(blendshape_grp)

        return node

    def _scale_components(self):
        """
        Make sure all components are ready to be scaled and add scale attr if it's missing.

        """
        if not self.has_attribute('rigScale'):
            self.addAttr('rigScale', type='float', dv=1.0)
            all_grp = self.all.get()

            all_grp.sx >> self.pynode.rigScale

        for rig_component in self.get_frag_children(of_type=keyable_component.KeyableComponent):
            rig_component.set_scale()

    @property
    def rig_scale(self):
        if not self.has_attribute('rigScale'):
            self._scale_components()
        return self.pynode.rigScale.get()

    @rig_scale.setter
    def rig_scale(self, val):
        if isinstance(val, (int, float)):
            for axis in attr_utils.SCALE_ATTRS:
                self.all_grp.attr(axis).set(val)

    @property
    def flags_all(self):
        return self.flagsAll.get()

    @property
    def do_not_touch(self):
        return self.doNotTouch.get()

    @property
    def all_grp(self):
        return self.all.get()

    @property
    def rig_template(self):
        return self.rigTemplate.get()

    def get_root(self):
        return self.get_frag_parent()

    def create_display_layers(self):
        """
        Creates all the display layers for this rig.

        """

        display_node = display_layers.DisplayLayers.create(self)

        frag_root_node = frag_root.get_frag_root(self)

        # Get the joints, meshes, and flags.
        root_joint = frag_root_node.rootJoint.get()
        joints = pm.listRelatives(root_joint, ad=1, pa=1, type='joint')
        joints.append(root_joint)

        meshes = self.get_meshes()
        primary_flags = self.get_primary_flags()
        detail_flags = self.get_detail_flags()
        contact_flags = self.get_contact_flags()
        util_flags = self.get_util_flags()

        display_node.add_objects(joints, display_layers.SKEL_LYR)
        display_node.add_objects(meshes, display_layers.SKIN_LYR)
        display_node.add_objects(primary_flags, display_layers.FLAGS_LYR)

        display_node.set_layer_to_reference(display_layers.SKEL_LYR)
        display_node.hide_layer(display_layers.SKEL_LYR)
        display_node.set_layer_to_reference(display_layers.SKIN_LYR)

        if contact_flags:
            display_node.add_objects(contact_flags, display_layers.FLAGS_CONTACT_LYR)
            display_node.hide_layer(display_layers.FLAGS_CONTACT_LYR)

        if detail_flags:
            display_node.add_objects(detail_flags, display_layers.FLAGS_DETAIL_LYR)
            display_node.add_objects(util_flags, display_layers.FLAGS_DETAIL_LYR)
            display_node.hide_layer(display_layers.FLAGS_DETAIL_LYR)

        return display_node

    def create_display_layers_for_cam(self, cam):
        """
        Creates all the display layers for this rig.

        """

        display_node = display_layers.DisplayLayers.create(self)
        frag_root_node = frag_root.get_frag_root(self)

        # Get the joints, meshes, and flags.
        root_joint = frag_root_node.rootJoint.get()
        joints = pm.listRelatives(root_joint, ad=1, pa=1, type='joint')
        joints.append(root_joint)

        primary_flags = self.get_primary_flags()
        detail_flags = self.get_detail_flags()
        contact_flags = self.get_contact_flags()
        util_flags = self.get_util_flags()

        display_node.add_objects(joints, display_layers.SKEL_LYR)
        display_node.add_objects([cam], display_layers.SKIN_LYR)
        display_node.add_objects(primary_flags, display_layers.FLAGS_LYR)

        display_node.set_layer_to_reference(display_layers.SKEL_LYR)
        display_node.hide_layer(display_layers.SKEL_LYR)
        display_node.set_layer_to_reference(display_layers.SKIN_LYR)

        if contact_flags:
            display_node.add_objects(contact_flags, display_layers.FLAGS_CONTACT_LYR)
            display_node.hide_layer(display_layers.FLAGS_CONTACT_LYR)

        if detail_flags:
            display_node.add_objects(detail_flags, display_layers.FLAGS_DETAIL_LYR)
            display_node.add_objects(util_flags, display_layers.FLAGS_DETAIL_LYR)
            display_node.hide_layer(display_layers.FLAGS_DETAIL_LYR)

        return display_node

    def get_meshes(self):
        """
        Returns all the meshes from the rig, skinned meshes and meshes that are children of the skeleton.

        :return: Returns all the meshes from the rig, skinned meshes and meshes that are children of the skeleton.
        :rtype: list(pm.nt.Transform)
        """

        root_node = frag_root.get_frag_root(self.pynode)
        root_joint = root_node.rootJoint.get()

        grp_skins = skeletal_mesh.get_group_skins(self.pynode)

        meshes = pm.listRelatives(grp_skins, ad=True)
        meshes = meshes + pm.listRelatives(root_joint, ad=1, pa=1, type='mesh')

        blendshape_grp = skeletal_mesh.get_group_blendshapes(self.pynode)
        if not blendshape_grp:
            return meshes

        blendshape_meshes = pm.listRelatives(blendshape_grp, ad=True)
        meshes = meshes + blendshape_meshes

        return meshes

    def get_flags(self):
        all_flags = pm.ls(self.namespace()+'*.isFlag', objectsOnly=True)
        return [frag_flag.Flag(x) for x in all_flags]

    def get_primary_flags(self):
        all_flags = self.get_flags()
        return [x for x in all_flags if not x.isDetail.get() and not x.isContact.get() and not x.isUtil.get()]

    def get_detail_flags(self):
        all_flags = self.get_flags()
        return [x for x in all_flags if x.isDetail.get()]

    def get_sub_flags(self):
        all_flags = self.get_flags()
        return [x for x in all_flags if x.isSub.get()]

    def get_contact_flags(self):
        all_flags = self.get_flags()
        return [x for x in all_flags if x.isContact.get()]

    def get_util_flags(self):
        all_flags = self.get_flags()
        return [x for x in all_flags if x.isUtil.get()]

    def finalize_rig(self, path=None):
        """
        Finalizes the rig after creation.

        :param str path: Path to where the flags live.
        """
        # Create the display layers.
        self.create_display_layers()

        # Swap the flags for custom flags.
        flags = self.get_flags()
        if path:
            frag_flag.swap_flags(flags, path)

        # Color Flags
        self.color_flags()

    def color_flags(self):
        primary_flags = self.get_primary_flags()

        for flag_node in primary_flags:
            # don't trust the .side attr on the joint, use the component's side markup.
            if flag_node.hasAttr('fragParent'):
                wrapped_flag = frag_flag.Flag(flag_node)
                rig_component = wrapped_flag.getAttr('fragParent')
                if not rig_component:
                    continue
                wrapped_component_node = frag_base.FRAGNode(rig_component)
                flag_side = wrapped_component_node.side
                if flag_side:
                    for shape_node in flag_node.getShapes():
                        shape_node.overrideEnabled.set(1)
                        if flag_side == 'left':
                            shape_node.overrideColor.set(6)
                        elif flag_side == 'right':
                            shape_node.overrideColor.set(13)
                        elif flag_side == 'center':
                            shape_node.overrideColor.set(17)
                        elif flag_side == 'front':
                            shape_node.overrideColor.set(20)
                        elif flag_side == 'back':
                            shape_node.overrideColor.set(19)

        sub_flags = self.get_sub_flags()
        sub_flags = [x.getShapes() for x in sub_flags]
        sub_flags = lists.flatten_list(sub_flags)
        for sub in sub_flags:
            sub.overrideEnabled.set(1)
            sub.overrideColor.set(18)

        detail_flags = self.get_detail_flags()
        detail_flags = [x.getShapes() for x in detail_flags]
        detail_flags = lists.flatten_list(detail_flags)
        for found_flag in detail_flags:
            found_flag.overrideEnabled.set(1)
            found_flag.overrideColor.set(9)

        contact_flags = self.get_contact_flags()
        contact_flags = [x.getShapes() for x in contact_flags]
        contact_flags = lists.flatten_list(contact_flags)
        for found_flag in contact_flags:
            found_flag.overrideEnabled.set(1)
            found_flag.overrideColor.set(14)

        util_flags = self.get_util_flags()
        util_flags = [x.getShapes() for x in util_flags]
        util_flags = lists.flatten_list(util_flags)
        for found_flag in util_flags:
            found_flag.overrideEnabled.set(1)
            found_flag.overrideColor.set(19)

