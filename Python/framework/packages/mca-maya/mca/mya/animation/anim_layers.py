#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
purpose: Animation Layers
"""

# System global imports
# Software specific imports
import pymel.core as pm
import maya.cmds as cmds
# mca python imports
from mca.common import log
from mca.common.utils import list_utils
from mca.mya.utils import attr_utils, naming
from mca.mya.animation import anim_curves, baking

# Internal module imports
logger = log.MCA_LOGGER


def check_obj_for_anim_layer(obj):
    """
    Checks to see if there is an animation layers connected to the object.

    :param pm.nt.transform obj: The object that animation curves will be transferred to.
    :return: If True, The object has an animation layer.
    :rtype: bool
    """

    anim_layer = obj.listConnections(type=pm.nt.AnimBlendNodeBase, scn=True)
    if anim_layer:
        return True
    return False


def get_objects_in_anim_layer(anim_layer):
    """
    Returns all the animated objects connected to a specific layer.

    :param pm.nt.AnimLayer anim_layer: Animation Layer
    :return: Returns all the animated objects connected to a specific layer.
    :rtype: list[pm.nt.DagNode]
    """

    return list(set(anim_layer.dagSetMembers.listConnections()))


def connect_layer_dagSetMembers(obj_attr, anim_layer):
    """
    Connects an animation layer to the dagSetMember of an object attribute.

    :param pm.nt.Attribute obj_attr:  The attribute on an object that you are attaching animation.
    :param pm.nt.AnimLayer anim_layer: Animation Layer
    """

    loop = True
    x = 0
    while loop:
        if not anim_layer.dagSetMembers[x].listConnections():
            pm.connectAttr(obj_attr, anim_layer.dagSetMembers[x], f=True)
            loop = False
        x += 1


def get_all_anim_layers_in_network(anim_blend):
    """
    Returns all the animation layers in an animation layer network.  This is per object attribute.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :return: Returns all the animation layers in an animation layer network.
    :rtype: list[pm.nt.AnimLayer]
    """

    mapped_network = map_anim_layers(anim_blend)
    layers = []
    for blend, layer in mapped_network:
        layers.append(layer)
    return layers


def get_all_anim_blends_in_network(anim_blend):
    """
    Returns all the animation blend nodes in an animation layer network.  This is per object attribute.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :return: Returns all the animation blend nodes in an animation layer network.
    :rtype: list[pm.nt.AnimBlendNodeBase]
    """

    mapped_network = map_anim_layers(anim_blend)
    blends = []
    for blend, layer in mapped_network:
        blends.append(blend)
    return blends


def delete_anim_blends_and_curves(anim_blend):
    """
    Deletes the animation layer network.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    """

    blend_nodes = get_all_anim_blends_in_network(anim_blend)
    curves = get_all_curves_in_layer_network(anim_blend)
    pm.delete(blend_nodes, curves)


def get_all_curves_in_layer_network(anim_blend):
    """
    Returns all of the pm.nt.AnimCurve s in a animation layer network.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :return: Returns all of the AnimCurves in a animation layer network.
    :rtype: list[pm.nt.AnimCurve]
    """

    mapping = map_anim_layers(anim_blend)
    curves = []
    for blend, layer in mapping:
        connected_curves = blend.listConnections(type=pm.nt.AnimCurve)
        if connected_curves:
            curves += connected_curves
    return curves


def get_base_anim_curves(anim_blend):
    """
    Returns the base pm.nt.AnimCurve.  This would be the animation in the base animation layer.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :return list[pm.nt.AnimCurve]: Returns the base pm.nt.AnimCurve.
    :rtype: list[pm.nt.AnimCurve]
    """

    blends = get_all_anim_blends_in_network(anim_blend)
    if blends[-1].inputA.isCompound():
        base_curve = attr_utils.get_compound_attr_connections(blends[-1], 'inputA')
    else:
        base_curve = blends[-1].inputA.listConnections(type=pm.nt.AnimCurve)
    if not base_curve:
        logger.warning('No Base Animation Curve was connected to the Animation Layer Network.')
    return base_curve


def map_anim_layers(anim_blend_layer):
    """
    Returns a list of animation blend nodes and it's corresponding animation layer.
    It will work backwards using inputs.
    [[BLEND NODE, ANIMATION LAYER]]

    :param pm.nt.AnimBlendNodeBase anim_blend_layer: Animation blend node
    :return: Returns a list of animation blend nodes and it's corresponding animation layer.
    :rtype: list[pm.nt.AnimBlendNodeBase, pm.nt.AnimLayer]
    """

    if not isinstance(anim_blend_layer, pm.nt.AnimBlendNodeBase):
        logger.warning('Mapping must start with the Animation Blend node.')
        return
    mapping = []
    nested_layers = True
    # Get the Animation Layer
    while nested_layers:
        anim_layer = list(set(anim_blend_layer.listConnections(type=pm.nt.AnimLayer)))
        anim_layer = list_utils.get_first_in_list(anim_layer)
        mapping.append([anim_blend_layer, anim_layer])

        if anim_blend_layer.inputA.isCompound():
            input_a = attr_utils.get_compound_attr_connections(anim_blend_layer, 'inputA')
        else:
            input_a = anim_blend_layer.inputA.listConnections()

        next_anim_layer = [x for x in input_a if isinstance(x, pm.nt.AnimBlendNodeBase)]

        if next_anim_layer:
            anim_blend_layer = next_anim_layer[0]
        else:
            nested_layers = False

    return mapping


def get_node_connections(node):
    """
    Returns a dictionary with input and output connections.

    :param pm.nt.transform node: An object with connections.
    :return: Returns a dictionary with input and output connections.
    :rtype: dictionary{pm.nt.attribute:pm.nt.attribute}
    """

    _dict = {}
    # Get all the animation blend node's connections.
    input_connections = node.listConnections(plugs=True, c=True, s=True, d=False)
    output_connections = node.listConnections(plugs=True, c=True, d=True, s=False)

    input_connections = map(lambda x: [str(x[0]), str(x[1])], input_connections)
    output_connections = map(lambda x: [str(x[0]), str(x[1])], output_connections)

    _dict['input'] = {}
    _dict['output'] = {}
    for x in input_connections:
        _dict['input'][x[1]] = x[0]
    for x in output_connections:
        _dict['output'][x[0]] = x[1]

    return _dict


def update_connections_dict(blend_connections, new_name, node_type):
    """
    Updates the node connections with a different node.  Used for switching connections to a duplicated node.
    Use this to after duplicating the node.  This will switch the original node name to the duplicated name.

    :param dictionary blend_connections: A dictionary with input and output connections.
    :param string new_name: Name of an animation blend node for animation layers.
    :param type() node_type: checks for the type of node.
    :return:  Returns an updated dictionary.
    :rtype: dictionary{pm.nt.attribute:pm.nt.attribute}
    """

    new_blend_connections = {}
    new_blend_connections['input'] = {}
    new_blend_connections['output'] = {}
    if not isinstance(new_name, str):
        new_name = str(new_name)
    for output_node_attr, input_node_attr in blend_connections['input'].iteritems():
        if cmds.objExists(output_node_attr) and isinstance(pm.PyNode(output_node_attr).node(), node_type):
            output_node_attr = output_node_attr.replace(output_node_attr.split('.')[0], new_name)
        if cmds.objExists(input_node_attr) and isinstance(pm.PyNode(input_node_attr).node(), node_type):
            input_node_attr = input_node_attr.replace(input_node_attr.split('.')[0], new_name)
        new_blend_connections['input'][output_node_attr] = input_node_attr

    for output_node_attr, input_node_attr in blend_connections['output'].iteritems():
        if cmds.objExists(output_node_attr) and isinstance(pm.PyNode(output_node_attr).node(), node_type):
            output_node_attr = output_node_attr.replace(output_node_attr.split('.')[0], new_name)
        if cmds.objExists(input_node_attr) and isinstance(pm.PyNode(input_node_attr).node(), node_type):
            input_node_attr = input_node_attr.replace(input_node_attr.split('.')[0], new_name)
        new_blend_connections['output'][output_node_attr] = input_node_attr
    return new_blend_connections


def update_anim_blend_in_dict(blend_connections, new_anim_blend):
    """
    Swapping out the animation blend node in the "get_node_connection" dictionary for a new animation blend node.

    :param dict blend_connections: input and output connections from an animation blend node.
    :param string new_anim_blend: Name of an animation blend node for animation layers.
    :return : Returns input and output connections from an animation blend node.
    :rtype: dictionary{pm.nt.attribute:pm.nt.attribute}
    """

    return update_connections_dict(blend_connections, new_anim_blend, pm.nt.AnimBlendNodeBase)


def update_anim_layer_in_dict(blend_connections, new_anim_layer):
    """
    Swapping out the animation layer node in the "get_node_connection" dictionary for a new animation layer node.

    :param dict blend_connections: input and output connections from an animation layer node.
    :param string new_anim_layer: Name of an animation layer node for animation layers.
    :return: Returns input and output connections from an animation layer node.
    :rtype: dictionary{pm.nt.attribute:pm.nt.attribute}
    """

    return update_connections_dict(blend_connections, new_anim_layer, pm.nt.AnimLayer)


def duplicate_anim_layer(anim_layer, new_name=None):
    """
    Duplicates the animation layer and adds an attribute to track the original anim layer.

    :param pm.nt.AnimLayer anim_layer: Animation Layer.
    :param string new_name: Name of the duplicated animation Library.
    :return:  Returns a duplicate animation layer.
    :rtype: pm.nt.AnimLayer
    """

    if not isinstance(anim_layer, pm.nt.AnimLayer):
        logger.warning('Node must be an animation layer node: {0}'.format(pm.nt.AnimLayer.__name__))
    if new_name:
        dup_anim_layer = pm.duplicate(anim_layer, n=new_name)[0]
    else:
        dup_anim_layer = pm.duplicate(anim_layer, n=new_name)[0]
    # Add an attribute that holds the original animation layer name.
    dup_anim_layer.addAttr('original_anim_layer', dt='string')
    dup_anim_layer.original_anim_layer.set(str(anim_layer))
    return dup_anim_layer


def check_layer_original(anim_layer, anim_layer_list):
    """
    Check a list of animation laters to see if it is a duplicated layer and if it matches the original node.

    :param pm.nt.AnimLayer anim_layer:  Animation Layer.
    :param list anim_layer_list: list of duplicated animation layers.
    :return: If True, it will return a duplicated animation layer that matches the anim_layer.
    :rtype: pm.nt.AnimLayer
    """

    for x in anim_layer_list:
        if x.hasAttr('original_anim_layer') and x.original_anim_layer.get() == str(anim_layer):
            return x
    return


def duplicate_anim_layer_network(anim_layers_map, anim_layer_list=None):
    """
    Duplicates the animation layer network.

    :param list anim_layers_map: Map of existing animation blend nodes and the animation layers they are connected to.
    :param list anim_layer_list: List of animations layers that already exist.  Use these animation layers to
    connect the duplicated blend nodes.
    :return: Returns an updated anim_layers_map with the duplicated nodes.
    :rtype: list[pm.nt.AnimBlendNodeBase, pm.nt.AnimLayer]
    """

    new_mapping = []
    for anim_blend, anim_layer in anim_layers_map:
        # Get the connections from the anim blend node and then duplicate the node.
        blend_connections = get_node_connections(anim_blend)
        dup_blend = pm.duplicate(anim_blend)[0]
        # Update the connections dictionary with the duplicated node.
        blend_connections = update_anim_blend_in_dict(blend_connections, dup_blend)

        # Check to see what animation layer will be connected to the anim blend.
        # The attempt here is to check to see if the animation has already been duplicated.  If already duplicated,
        # we want to connect to that animation layer.  If not, then duplicate the animation layer.
        anim_layer_list = pm.ls(type=pm.nt.AnimLayer)
        original_layer = check_layer_original(anim_layer, anim_layer_list)
        if not original_layer:
            duped_anim_layer = duplicate_anim_layer(anim_layer)
            anim_layer_list.append(duped_anim_layer)
        else:
            duped_anim_layer = original_layer
            anim_layer_list.append(duped_anim_layer)

        blend_connections = update_anim_layer_in_dict(blend_connections, duped_anim_layer)

        # Connect new input nodes just like the old nodes.
        for output_node_attr, input_node_attr in blend_connections['input'].iteritems():
            output_node = pm.PyNode(output_node_attr).node()
            output_attr = output_node_attr.split('.')[-1]
            # Connect the duplicated blend node and animation layer.
            if isinstance(output_node, pm.nt.AnimLayer):
                pm.connectAttr(output_node_attr, input_node_attr, f=True)
            # Duplicate the animation curve and connect.
            elif isinstance(output_node, pm.nt.AnimCurve):
                curve = pm.duplicate(output_node)[0]
                pm.connectAttr(curve.attr(output_attr), input_node_attr, f=True)

        # Connect new output nodes just like the old nodes.
        for output_node_attr, input_node_attr in blend_connections['output'].iteritems():
            input_node = pm.PyNode(input_node_attr).node()
            if isinstance(input_node, pm.nt.AnimLayer):
                pm.connectAttr(output_node_attr, input_node_attr, f=True)
        new_mapping.append([dup_blend, duped_anim_layer])

    if len(new_mapping) > 1:
        for x in range(len(new_mapping) - 1):
            blend_node = new_mapping[x][0]
            next_blend_node = new_mapping[x + 1][0]
            if isinstance(blend_node, pm.nt.AnimBlendNodeBase) and isinstance(next_blend_node, pm.nt.AnimBlendNodeBase):
                next_blend_node.output >> blend_node.inputA

    return [new_mapping, anim_layer_list]


def merge_anim_layer_network(anim_blend, new_anim_blend, delete_curve=True):
    """
    Merges 2 base animation curves from two different animation layer networks.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :param pm.nt.AnimBlendNodeBase new_anim_blend: The animation blend node that ties the curves and layers together.
    :param bool delete_curve: If true, deletes the unused animation curve.
    """

    # map the two networks and get the base animation curves
    anim_map = get_all_anim_blends_in_network(new_anim_blend)
    original_base_curves = get_base_anim_curves(anim_blend)
    new_base_curves = get_base_anim_curves(new_anim_blend)
    # merge the anim curves and connect the blends together.
    if len(new_base_curves) == len(original_base_curves):
        for x in range(len(new_base_curves)):
            anim_curves.replace_into_curve(new_base_curves[x], original_base_curves[x], delete_curve=delete_curve)

    # connect the networks together
    last_anim_blend = anim_map[-1]
    if last_anim_blend.inputA.isCompound():
        input_attrs = last_anim_blend.inputA.getChildren()
        output_attrs = anim_blend.output.getChildren()
        for x in range(len(input_attrs)):
            pm.disconnectAttr(output_attrs[x])
            pm.connectAttr(output_attrs[x], input_attrs[x], f=True)
    else:
        pm.connectAttr(anim_blend.output, last_anim_blend.inputA, f=True)


def connect_layer_to_base_layer(anim_layer):
    """
    Connects an animation layer to the base animation layer.

    :param pm.nt.AnimLayer anim_layer: Animation layer node.
    """

    root_layer = pm.animLayer(q=True, r=True)
    if not root_layer:
        pm.delete(pm.animLayer())
        root_layer = pm.animLayer(q=True, r=True)
        logger.warning('There is not Base Layer in the scene.  Creating {0}.'.format(root_layer))

    parent_layer = pm.animLayer(anim_layer, query=True, parent=True)

    if parent_layer == root_layer:
        logger.warning('{0} is already connected to the base layer {1}.'.format(anim_layer, root_layer))
        return

    if not anim_layer in root_layer.childrenSolo.listConnections():
        c_solo = pm.getAttr(root_layer.childrenSolo, size=True)
        pm.connectAttr(anim_layer.solo, root_layer.childrenSolo[c_solo], f=True)
    if not anim_layer in root_layer.childrenLayers.listConnections():
        c_layers = pm.getAttr(root_layer.childrenLayers, size=True)
        pm.connectAttr(anim_layer.parentLayer, root_layer.childrenLayers[c_layers], f=True)

    pm.connectAttr(root_layer.childsoloed, anim_layer.siblingSolo, f=True)
    pm.connectAttr(root_layer.outMute, anim_layer.parentMute, f=True)
    pm.connectAttr(root_layer.foregroundWeight, anim_layer.parentWeight, f=True)


def store_object_animation(obj,
                           keep_animation=True,
                           min_time_range=None,
                           max_time_range=None,
                           merge_layers=False,
                           start_time=None):
    """
    Creates compound attributes associated with the objects and animation curves.
    This will disconnect the animation curve and connect them to the associated compound attribute.

    :param pm.nt.transform obj: An object that has animation curves.
    :param bool keep_animation: If True, the animation curves are duplicated before adding to the node.
    :param int min_time_range: Any key before this number will be deleted.
    :param int max_time_range: Any key after this number will be deleted.
    :return obj: The object that animation curves were transferred to.
    :rtype: pm.nt.transform
    """

    attr_curves = {}

    # check for animation layer.  If there is one, merge layers.
    if merge_layers and check_obj_for_anim_layer(obj=obj):
        baking.merge_all_animation_layers()

    # get all the animation curves and the plugs.  This will disconnect the animation curves
    # and connect them to the associated compound attribute.
    curves = obj.listConnections(type=(pm.nt.AnimCurve, pm.nt.AnimBlendNodeBase), scn=True, d=False)
    if not curves:
        return

    curves = list(set(curves))
    for curve in curves:
        if isinstance(curve, pm.nt.AnimCurve):
            plug, curve = create_dict_curve_connections(curve, keep_animation)
            if min_time_range or max_time_range:
                anim_curves.crop_time_range(node_list=curve, min_time=min_time_range, max_time=max_time_range)
            if isinstance(start_time, int):
                key_time = pm.keyframe(curve, q=True)
                start_diff = start_time - key_time[0]
                anim_curves.change_curve_start_time(node_list=curve, shift_length=start_diff)
            attr_curves[plug] = curve.output
        elif isinstance(curve, pm.nt.AnimBlendNodeBase):
            attr_curves.update(create_anim_layer_network(curve, keep_animation, min_time_range, max_time_range))

    return attr_curves


def create_anim_layer_network(anim_blend, keep_animation=True, min_time_range=None, max_time_range=None):
    """
    Duplicates the animation layer network.

    :param pm.nt.AnimBlendNodeBase anim_blend: Animation blend node.
    :return: Returns a list of the animation blend nodes and animation layers.
    :rtype: list[pm.nt.AnimBlendNodeBase, pm.nt.AnimLayer]
    """

    attr_curves = {}
    if not anim_blend:
        logger.warning('There is no connected animation blend node.')
        return
    if anim_blend.output.isCompound():
        obj_attrs = attr_utils.get_compound_attr_connections(anim_blend, 'output', as_plugs=True)
    else:
        obj_attrs = pm.PyNode(anim_blend + '.output').listConnections(plugs=True)[0]

    # Duplicate the whole animation layer network and connect new layers to this node.
    mapped_layers = map_anim_layers(anim_blend)
    new_mapping, animation_layers = duplicate_anim_layer_network(mapped_layers)
    new_anim_blend = pm.PyNode(new_mapping[0][0])

    # Remove existing animation blend nodes.  Delete Animation.
    if not keep_animation:
        delete_anim_blends_and_curves(anim_blend)

    curves = get_all_curves_in_layer_network(new_anim_blend)
    if min_time_range or max_time_range and curves:
        anim_curves.crop_time_range(node_list=curves, min_time=min_time_range, max_time=max_time_range)

    if isinstance(obj_attrs, list):
        new_anim_blend_attrs = new_anim_blend.output.getChildren()
        plug = naming.get_basename(obj_attrs[0].node())
        attr_name = str(obj_attrs[0].parent().split('.')[-1])
        plug = plug + '_' + attr_name
        attr_curves[plug] = new_anim_blend_attrs
    else:
        plug = naming.get_basename(obj_attrs)
        attr_curves[plug] = new_anim_blend.output
    return attr_curves


def create_dict_curve_connections(curve, keep_animation=True):
    """
    Creates a dictionary of the how the animation curve was connected.

    :param object curve: an object that is connected.
    :param bool keep_animation: if connected the object curve will be duplicated.
    :return: Returns a dictionary of the how the animation curve was connected.
    :rtype: dictionary{pm.nt.attribute:pm.nt.attribute}
    """

    curves_dict = {}
    # Get the object the plug is connected to.
    plug = curve.listConnections(plugs=True)[0]

    if keep_animation:
        curve = pm.duplicate(curve)[0]

    # remove name spaces and create the connection dictionary.
    plug = naming.get_basename(plug)
    curve_name = naming.get_basename(curve)
    curve = pm.PyNode(curve.rename(curve_name))
    # curves_dict[plug] = curve.output
    return [plug, curve]


###############################
# Restore Layers
###############################
def restore_for_anim_layers(anim_blend,
                            object_attribute,
                            keep_curves=False,
                            delete_old_curves=False,
                            start_time=None):
    """
    The main command to restore animation curves onto an object.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :param pm.nt.general.Attribute object_attribute: The object attribute that connects to an animation.
    :param bool keep_curves: If True, will duplicate the animation curves or anim layer network before re-connecting.
    :param bool delete_old_curves: deletes the curves that are already connected to the new object.
    :param int start_time: The start frame if the animation needs to change in the timeline.
    :return: returns the last frame if the start time changes.
    :rtype: int
    """

    end_time = None
    if keep_curves:
        # Duplicates the animation layer network and connects the new animation layers.
        keep_anim_layer_curves(anim_blend)
    else:
        # Disconnect all the animation layers and connect them to the BaseAnimation layer.
        swap_anim_layer_curves(anim_blend=anim_blend, object_attribute=object_attribute)

    # adjust time range to match the selected timeline.
    if start_time:
        end_time = adjust_layers_timeline(anim_blend=anim_blend, start_time=start_time)

    # get the connections of the flag/object
    if object_attribute.isCompound():
        obj_curves = list(set(attr_utils.get_compound_attr_connections(node=object_attribute,
                                                                    destination=False,
                                                                    source=True)))
    else:
        obj_curves = object_attribute.listConnections(d=False, s=True)

    if not obj_curves:
        # Swap the animation curve from the node to the object.
        connect_anim_layer_curves(anim_blend, object_attribute)
    # Connect Animation Layers

    elif obj_curves and delete_old_curves:
        # Delete the old curves 1st, then swap the animation curve from the node to the object.
        [delete_all_old_curves(obj_curve) for obj_curve in obj_curves]
        connect_anim_layer_curves(anim_blend, object_attribute)

    elif obj_curves and not delete_old_curves:
        if isinstance(obj_curves[0], pm.nt.AnimCurve):
            base_curves = get_base_anim_curves(anim_blend)
            if base_curves:
                for x in range(len(base_curves)):
                    anim_curves.replace_into_curve(obj_curves[x], base_curves[x])
                pm.delete(obj_curves)
                connect_anim_layer_curves(anim_blend, object_attribute)
        elif isinstance(obj_curves[0], pm.nt.AnimBlendNodeBase):
            merge_anim_layer_network(obj_curves[0], anim_blend)
            connect_anim_layer_curves(anim_blend, object_attribute)
    return end_time


def connect_anim_layer_curves(anim_blend, object_attribute):
    """
    # Swap the animation curve from the node to the object.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :param pm.nt.general.Attribute object_attribute: The object attribute that connects to an animation.
    """

    if not anim_blend.output.isCompound() and not object_attribute.isCompound():
        anim_blend.output >> object_attribute
    elif anim_blend.output.isCompound() and object_attribute.isCompound():
        anim_blend_attrs = attr_utils.get_all_attributes_from_compound_attr(anim_blend.output)
        object_attrs = attr_utils.get_all_attributes_from_compound_attr(object_attribute)
        for x in range(len(anim_blend_attrs)):
            pm.connectAttr(anim_blend_attrs[x], object_attrs[x], f=True)
        # connect rotate orders
        blends = get_all_anim_blends_in_network(anim_blend)
        for blend in blends:  # Todo ncomes make RotateOrder not a unique condition.
            if blend.hasAttr('rotateOrder'):
                object_attribute.node().rotateOrder >> blend.rotateOrder
    else:
        logger.warning('There is a mismatch between object attributes and animation blend. '
                       'Both objects need to be either a multi attr or a single attr: '
                       '{0}, {1}'.format(anim_blend.output, object_attribute))


def keep_anim_layer_curves(anim_blend):
    """
    On restoring animations, duplicates the animation layer network and connects the new animation layers.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :return: The animation blend node that ties the curves and layers together.
    :rtype: pm.nt.AnimBlendNodeBase
    """

    # Return a list of all anim_blend nodes and animation_layer_nodes
    # [[anim_blend, anim_layers], [anim_blend, anim_layers]]
    mapped_layers = map_anim_layers(anim_blend)
    # Get a list of all animation layers connected to the base layer.
    root_layer = pm.animLayer(q=True, r=True)
    anim_layer_list = root_layer.childrenLayers.listConnections()
    new_mapping = duplicate_anim_layer_network(mapped_layers, anim_layer_list)

    # Connect the animation layer to the base animation layer if it was just created/duplicated.
    for blend_node, anim_layer in new_mapping:
        if anim_layer not in anim_layer_list:
            connect_layer_to_base_layer(anim_layer)
    anim_blend = new_mapping[0][0]
    return anim_blend


def swap_anim_layer_curves(anim_blend, object_attribute):
    """
    Connects the animation layer to the base layer and the object.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :param pm.nt.general.Attribute object_attribute: The object attribute that connects to an animation.
    """

    # Disconnect all the animation layers and connect them to the BaseAnimation layer.
    root_layer = pm.animLayer(q=True, r=True)
    layers = get_all_anim_layers_in_network(anim_blend)
    # Attempt to connect all Layers to the base layer
    for anim_layer in layers:
        if not anim_layer in root_layer.listConnections():
            connect_layer_to_base_layer(anim_layer)
    # Connect layers to the flag/object attribute
    for layer in layers:
        connect_layer_dagSetMembers(object_attribute, layer)


def adjust_layers_timeline(anim_blend, start_time):
    """
    Adjusts all the animation curves in an animation layer network.

    :param pm.nt.AnimBlendNodeBase anim_blend: The animation blend node that ties the curves and layers together.
    :param int start_time: The start frame if the animation needs to change in the timeline.
    :return int: returns the last frame if the start time changes.
    :rtype: int
    """

    # adjust time range to match the selected timeline.
    end_frame = None
    if start_time:
        curves = get_all_curves_in_layer_network(anim_blend)
        for curve in curves:
            anim_curves.change_curve_start_time(node_list=curve, shift_length=start_time)
            end_frame = pm.keyframe(curve, q=True)[-1]
    return end_frame


def delete_all_old_curves(anim_obj):
    """
    Deletes an animation curve or an animation layer network.

    :param pm.nt.transform anim_obj: An animation object.
    """

    if isinstance(anim_obj, pm.nt.AnimCurve):
        pm.delete(anim_obj)
    elif isinstance(anim_obj, pm.nt.AnimBlendNodeBase):
        delete_anim_blends_and_curves(anim_obj)


