#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
import re
# software specific imports
import pymel.core as pm

#  python imports
from mca.mya.modifiers import contexts
from mca.mya.utils import naming

from mca.common import log
logger = log.MCA_LOGGER

TRANSLATION_ATTRS = ['tx', 'ty', 'tz']
ROTATION_ATTRS = ['rx', 'ry', 'rz']
SCALE_ATTRS = ['sx', 'sy', 'sz']
TRANSFORM_ATTRS = TRANSLATION_ATTRS + ROTATION_ATTRS + SCALE_ATTRS

# quick reference match for incoming data type to mya values for adding attrs
# reason ATTR_MAPPINGS doesn't quite work is it's all string values: add attr args.
MAYA_TYPE_DICT = {
                    bool: 'bool',
                    str: 'string',
                    float: 'float',
                    int: int,
                    pm.Attribute: 'message',
                    pm.PyNode: 'message'
                    }


def set_attr_state(node_list, locked=True, attr_list=None, visibility=False):
    """
    For a given object set a list of attrs to locked or unlocked, and optionally toggle their visibility to match.
    Defaults to not hiding visibility, and sets all TRANSFORM attrs to locked.

    :param list[Transform] node_list: A list of transform to set attr states on.
    :param bool locked: If the attrs should be locked or unlocked.
    :param list[str] attr_list: The string name of the attributes to be set.
    :param bool visibility: If the attribute's visibility should be toggled as well.
    """
    if not node_list:
        return

    if not isinstance(node_list, list):
        node_list = [node_list]

    add_extra_attrs = False
    if attr_list is None:
        attr_list = TRANSFORM_ATTRS
        if locked is False:
            add_extra_attrs = True

    for node in node_list:
        # Unlock parent attrs so we can set the locks on a per attribute basis.
        node.unlock()
        node.t.unlock()
        node.r.unlock()
        node.s.unlock()

        local_attr_list = attr_list[:]
        if add_extra_attrs:
            local_attr_list += [x.shortName() for x in node.listAttr(locked=True)]
            local_attr_list = list(set(local_attr_list))

        for attr_name in local_attr_list:
            if locked:
                node.attr(attr_name).lock()
            else:
                node.attr(attr_name).unlock()
            if visibility:
                node.attr(attr_name).set(channelBox=not locked)
                node.attr(attr_name).set(keyable=not locked)


def purge_user_defined_attrs(node_list, skip_list=(), skip_dialog=False):
    """
    Removes all user defined attributes from the given node.
    
    :param list(pm.PyNode) node_list: node we want to remove user defined attributes of.
    :param list(str) skip_list: Attributes to skip
    :param bool skip_dialog: If True, no warning will be printed.
    :return: Returns a list of attributes that get purged.
    :rtype: list(str)
    """
    
    with contexts.undo_chunk_context():
        user_attrs = []
        for node in node_list:
            user_attrs = node.listAttr(ud=True)
            if not user_attrs:
                if not skip_dialog:
                    logger.warning(f'{node.nodeName()} does not have any user attributes.')
                return
            
            set_attr_state(node, False)
            if skip_list:
                skip_attrs = [node.attr(x) for x in skip_list if node.hasAttr(x)]
                user_attrs = [attr for attr in user_attrs if attr not in skip_attrs]
            
            pm.deleteAttr(user_attrs)
        return user_attrs


def set_attribute(node, attribute_dict, merge_values=False):
    """
    Convert a dictionary of attr names and values into stamped attrs.

    :param PyNode node: The PyNode to stamp the new attributes on
    :param dict attribute_dict: A dictionary of attr names to their values
    :param bool merge_values: If a multi attr should keep original values and add the new ones.
    :return:
    """

    for attr_name, attr_value in attribute_dict.items():
        if not node.hasAttr(attr_name):
            if isinstance(attr_value, (list, tuple)):
                # We need a single value to test typing against.
                if attr_value:
                    test_value = attr_value[0]
                else:
                    test_value = None
                multi_attr = True
            else:
                test_value = attr_value
                multi_attr = False
            if test_value is not None:
                # for non None data values
                for property_type, string_property_type in MAYA_TYPE_DICT.items():
                    # bools register as ints. So if we have a bool test_value make sure we don't okay it as an int.
                    if isinstance(test_value, property_type) and not (
                            isinstance(test_value, bool) and property_type == int) and not (
                            isinstance(test_value, pm.Attribute) and property_type == pm.PyNode):
                        # if we find a match break and take the string_property_type of the active entry
                        break
                else:
                    string_property_type = 'string'
                    f'An incoming data type does not have a register in the MAYA_TYPE_DICT type: {attr_value} for property: {attr_name}'

            if string_property_type in ['string']:
                node.addAttr(attr_name,
                             dataType=string_property_type,
                             nn=attr_name, m=multi_attr)
            else:
                node.addAttr(attr_name,
                             attributeType=string_property_type,
                             nn=attr_name, m=multi_attr)

        if attr_value is not None:
            new_node_attr = node.attr(attr_name)
            if isinstance(attr_value, (list, tuple)):
                original_values = []
                start_index = 0
                if merge_values:
                    original_values = new_node_attr.get() or []
                    found_index = node.getAttr(attr_name, mi=True)
                    start_index = max(found_index) + 1 if found_index else 0
                for index, val in enumerate(attr_value):
                    if merge_values and val in original_values:
                        continue
                    try:
                        if isinstance(val, pm.Attribute):
                            # attribute first as it's a derivative of PyNode
                            val.node().message >> new_node_attr[index + start_index]
                            node.message >> val
                        elif isinstance(val, pm.PyNode):
                            val.message >> new_node_attr[index + start_index]
                        else:
                            new_node_attr[index + start_index].set(val)
                    except AttributeError as exc:
                        pass
            else:
                try:
                    if isinstance(attr_value, pm.Attribute):
                        # attribute first as it's a derivative of PyNode
                        attr_value.node().message >> new_node_attr
                        node.message >> attr_value
                    elif isinstance(attr_value, pm.PyNode):
                        attr_value.message >> new_node_attr
                    else:
                        new_node_attr.set(attr_value)
                except AttributeError as exc:
                    pass


def set_compound_attribute_groups(node, compound_attr_name, attribute_dict):
    """
    Adds a set of attributes that represents the data in a given dict of strings to values. Handles multi.
    
    This uses the mya type dictionary at the head of this file to determine the string name of the data type when
    applying the new attributes.
    :param PyNode node: The node to apply the new attributes to.
    :param str compound_attr_name: The name of the parent attribute.
    :param dict{str, value} attribute_dict: A dictionary of the names of each of the properties and their values.
    """
    
    number_of_children = len([x for x in attribute_dict if isinstance(x, str)])
    if node.hasAttr(compound_attr_name):
        # setting always overrides data, if you need to update values individually target those values.
        # this also ensures the number of children under the parent attr is correct.
        # setting and adding a new property requires reading the existing data creating a attribute_dict then rebuilding.
        node.deleteAttr(compound_attr_name)
    if not number_of_children:
        # non compound entry for a property group without properties.
        # typing really doesn't matter here so I choose bool the value doesn't either.
        node.addAttr(compound_attr_name, attributeType='bool')
    else:
        # $Hack FSchorsch Without adding a bool type attr the rollout behavior in the UI will not always work
        # this seems to happen when all children attributes are of a single type, and not bools.
        # we're adding an extra child attr here to get around it.
        # when we export since this doesn't have the block name appended it'll fail to find when setting it to schema.
        node.addAttr(compound_attr_name, numberOfChildren=(number_of_children + 1), attributeType='compound')
        node.addAttr(f'_{compound_attr_name}_hidden', attributeType='bool', parent=compound_attr_name, h=True)
    # END HACK
    # add child attrs to the compound, these still register as if added directly to the node.
    for property_name, property_value in attribute_dict.items():
        if not isinstance(property_name, str):
            'Dictionary key with value {property_value} is not a string, entry will be skipped.'
            continue
        # since the attr is added directly to the node, we need to make the name a little more unique
        if not node.hasAttr(f'{compound_attr_name}_{property_name}'):
            # block name and property name are combined to avoid property blocks with the same property name.
            # all attrs are registered on the base node and will conflict without this.
            if isinstance(property_value, (list, tuple)):
                # We need a single value to test typing against.
                if property_value:
                    test_value = property_value[0]
                else:
                    test_value = None
                multi_attr = True
            else:
                test_value = property_value
                multi_attr = False
            if test_value is not None:
                # for non None data values
                for property_type, string_property_type in MAYA_TYPE_DICT.items():
                    # bools register as ints. So if we have a bool test_value make sure we don't okay it as an int.
                    if isinstance(test_value, property_type) and not (
                            isinstance(test_value, bool) and property_type == int) and not (
                            isinstance(test_value, pm.Attribute) and property_type == pm.PyNode):
                        # if we find a match break and take the string_property_type of the active entry
                        break
                else:
                    string_property_type = 'string'
                    f'An incoming data type does not have a register in the MAYA_TYPE_DICT type: {type(property_value)} for property: {compound_attr_name}, {property_name}'
            else:
                # data value was None
                string_property_type = 'string'
            if string_property_type:
                # concatenate the class name and property name to create a unique attr name. Objects cannot have more than one property group of the same type.
                if string_property_type in ['string']:
                    node.addAttr(f'{compound_attr_name}_{property_name}',
                                 dataType=string_property_type,
                                 parent=compound_attr_name, nn=property_name, m=multi_attr)
                else:
                    node.addAttr(f'{compound_attr_name}_{property_name}',
                                 attributeType=string_property_type,
                                 parent=compound_attr_name, nn=property_name, m=multi_attr)
    for property_name, property_value in attribute_dict.items():
        if not isinstance(property_name, str):
            continue
        # set property values.  This needs to be done after all child attributes have been added to the compound attr.
        if isinstance(property_value, pm.Attribute):
            # check if the receiver is a message attr
            property_value.disconnect()
            property_value >> node.attr(f'{compound_attr_name}_{property_name}')
        # node.attr(f'{compound_attr_name}_{property_name}') >> property_value
        
        elif isinstance(property_value, pm.PyNode):
            # To handle message type connections
            if pm.attributeQuery('message', node=property_value, exists=True):
                property_value.message >> node.attr(f'{compound_attr_name}_{property_name}')
            else:
                f'{property_value} does not have a message attr and could not be connected.'
        elif isinstance(property_value, (list, tuple)):
            # to handle multi attrs
            for index, value in enumerate(property_value):
                if value is None:
                    # we can't set None
                    continue
                if isinstance(property_value, pm.Attribute):
                    # check if the receiver is a message attr
                    property_value.disconnect()
                    property_value >> node.attr(f'{compound_attr_name}_{property_name}')
                    # node.attr(f'{compound_attr_name}_{property_name}') >> property_value
                elif isinstance(value, pm.PyNode):
                    # to handle message type connections
                    if pm.attributeQuery('message', node=value, exists=True):
                        value >> node.attr(f'{compound_attr_name}_{property_name}')[index]
                    else:
                        '{value} does not have a message attr and could not be connected.'
                else:
                    node.attr(f'{compound_attr_name}_{property_name}')[index].set(value)
        else:
            # For standard single value settings.
            if property_value is not None:
                # We can't set None
                node.attr(f'{compound_attr_name}_{property_name}').set(property_value)


def get_all_attributes_from_compound_attr(node, compound_attr_name=None):
    """
    Returns all the attributes in a given compound attr
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :param string compound_attr_name: the name of the compound attribute
    :return: Returns all the attributes in a given compound attribute.
    :rtype: list(pm.nt.General.Attribute)
    """
    
    if isinstance(node, pm.nt.general.Attribute):
        compound_attr = node
    elif not compound_attr_name or not node.hasAttr(compound_attr_name):
        logger.error(f'"{compound_attr_name}": Compound attribute does not exist.')
        return
    else:
        compound_attr = get_compound_attr_name_as_attribute(node, compound_attr_name)
    
    attribute_list = [node.attr(x) for x in pm.listAttr(compound_attr) if not str(x) in compound_attr.split('.')[-1]]
    return attribute_list


def get_compound_attr_name_as_attribute(node, compound_attr_name):
    """
    Retrieves the names in a compound attribute.
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :param string compound_attr_name: name of the compound attribute.
    :return: Returns all the message attributes names.
    :rtype: pm.nt.General.Attribute
    """
    
    if node.hasAttr(compound_attr_name):
        result = node.attr(compound_attr_name)
        return result
    logger.warning(f'"{compound_attr_name}": Compound attribute does not exist.')
    return pm.nt.General.Attribute


def get_compound_attr_connections(node, compound_attr_name=None, as_plugs=False, destination=True, source=True):
    """
    Retrieves the objects in a compound attribute.
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :param string compound_attr_name: name of the compound attribute.
    :param bool as_plugs: if True, returns the plugs rather than the objects.
    :param bool destination: if True, returns the "destination" side of connections.
    :param bool source: if True, returns the  "source" side of connections.
    :return: Returns all the connected objects in a particular compound attribute.
    :rtype: list(pm.nt.PyNode)
    """
    
    if isinstance(node, pm.nt.general.Attribute):
        compound_attr = node
    elif not compound_attr_name or not node.hasAttr(compound_attr_name):
        logger.error(f'"{compound_attr_name}": Compound attribute does not exist.')
        return
    else:
        compound_attr = node.attr(compound_attr_name)
    # get a list of all the message attributes
    compound_attrs = list(map(lambda x: node.attr(x), pm.listAttr(compound_attr, c=True)))
    compound_attr_data = [x.listConnections(d=destination, s=source) for x in compound_attrs if x.listConnections()]
    if as_plugs:
        compound_attr_data = [x.listConnections(plugs=True, d=destination, s=source) for x in compound_attrs if
                              x.listConnections()]
    flatten_compound_attr_data = [x for compound_attr_data_item in compound_attr_data for x in compound_attr_data_item]
    compound_attr_data = list(map(lambda x: pm.PyNode(x), flatten_compound_attr_data))
    return compound_attr_data


def get_compound_attr_names(node):
    """
    Returns all the compound attribute names.
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :return: string list of all the compound attribute names.
    :rtype: list(str)
    """
    
    compound = []
    all_attrs = node.listAttr()
    for attrs in all_attrs:
        if pm.objExists(attrs):
            if attrs.type() == 'TdataCompound':
                compound.append(str(attrs).split('.')[-1])
    return compound


def disconnect_all_compound_attr_connections(node, compound_attr_name):
    """
    Disconnects objects from the compound attribute.
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :param string compound_attr_name:
    """
    
    compound_attributes = get_all_attributes_from_compound_attr(node, compound_attr_name)
    for x in range(len(compound_attributes)):
        compound_connections = compound_attributes[x].listConnections()
        if compound_connections and len(compound_connections) > 1:
            for i in range(len(compound_connections)):
                objs_plug = compound_attributes[x][i].listConnections(p=True)[0]
                pm.disconnectAttr(objs_plug, compound_attributes[x][i])
        elif compound_connections and len(compound_connections) == 1:
            objs_plug = compound_attributes[x].listConnections(p=True)[0]
            pm.disconnectAttr(objs_plug, compound_attributes[x])


def disconnect_and_delete_compound_attr(node, compound_attr_name):
    """
    Disconnects all objects from the compound_attr and then deletes it.
    
    :param pm.nt.Transform node: Maya transform with compound attribute.
    :param string compound_attr_name: Name of the compound attribute.
    """
    
    disconnect_all_compound_attr_connections(node, compound_attr_name)
    compound_attr = node.attr(compound_attr_name)
    pm.deleteAttr(compound_attr)


def invert_attribute(attr_to_invert):
    """
    Reverses the attribute.
    
    :param PyNode attr: Attribute name.
    :return: Returns the setRange node that reverses the value.
    :rtype: pm.nt.setRange
    """
    node_name = f'{naming.get_basename(attr_to_invert.node())}_inverseAttr'
    reverse_node = pm.createNode(pm.nt.SetRange, n=node_name)
    reverse_node.setAttr('min', [0, 1, 0], k=False, lock=True)
    reverse_node.setAttr('max', [1, 0, 100], k=False, lock=True)
    reverse_node.setAttr('oldMin', [0, 0, 0], k=False, lock=True)
    reverse_node.setAttr('oldMax', [1, 1, 1], k=False, lock=True)
    reverse_node.outValueX.setAlias('straight')
    reverse_node.outValueY.setAlias('inverse')
    reverse_node.outValueZ.setAlias('percent')

    attr_to_invert >> reverse_node.valueX
    attr_to_invert >> reverse_node.valueY
    attr_to_invert >> reverse_node.valueZ
    return reverse_node


def set_limits(rig_flag,
               rig_node=None,
               limit_point=((None, None), (None, None), (None, None)),
               limit_orient=((None, None), (None, None), (None, None))):
    """
    Sets limits on a flag and stamps the info onto a network node.
    
    :param flag.Flag rig_flag: A rig Flag
    :param FRAGNode rig_node: FRAG Node
    :param list(list(float)) limit_point: The limit points of a flag
    :param list(list(float)) limit_orient: The limit points of a flag
    """
    
    if not rig_node:
        rig_node = rig_flag
    # limits
    limits = []
    for limit_min, limit_max in limit_point + limit_orient:
        min_limited = not limit_min is None  # Set as True or False
        max_limited = not limit_max is None  # Set as True or False
        if limit_min is None:
            limit_min = 0
        if limit_max is None:
            limit_max = 0
        limits.append((limit_min, limit_max, min_limited, max_limited))
    pointX, pointY, pointZ, orientX, orientY, orientZ = limits
    
    # Set limits and create attributes that reflect those limits
    # Translate X
    pm.transformLimits(rig_flag, tx=(pointX[0], pointX[1]), etx=(pointX[2], pointX[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='translateLimitX',
                             limit_min=pointX[0],
                             limit_max=pointX[1],
                             limit_min_loc=pointX[2],
                             limit_max_loc=pointX[3])
    # Translate Y
    pm.transformLimits(rig_flag, ty=(pointY[0], pointY[1]), ety=(pointY[2], pointY[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='translateLimitY',
                             limit_min=pointY[0],
                             limit_max=pointY[1],
                             limit_min_loc=pointY[2],
                             limit_max_loc=pointY[3])
    # Translate Z
    pm.transformLimits(rig_flag, tz=(pointZ[0], pointZ[1]), etz=(pointZ[2], pointZ[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='translateLimitZ',
                             limit_min=pointZ[0],
                             limit_max=pointZ[1],
                             limit_min_loc=pointZ[2],
                             limit_max_loc=pointZ[3])
    # Orient X
    pm.transformLimits(rig_flag, rx=(orientX[0], orientX[1]), erx=(orientX[2], orientX[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='orientLimitX',
                             limit_min=orientX[0],
                             limit_max=orientX[1],
                             limit_min_loc=orientX[2],
                             limit_max_loc=orientX[3])
    # Orient Y
    pm.transformLimits(rig_flag, ry=(orientY[0], orientY[1]), ery=(orientY[2], orientY[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='orientLimitY',
                             limit_min=orientY[0],
                             limit_max=orientY[1],
                             limit_min_loc=orientY[2],
                             limit_max_loc=orientY[3])
    # Orient Z
    pm.transformLimits(rig_flag, rz=(orientZ[0], orientZ[1]), erz=(orientZ[2], orientZ[3]))
    add_limits_for_transform(node=rig_node,
                             limit_name='orientLimitZ',
                             limit_min=orientZ[0],
                             limit_max=orientZ[1],
                             limit_min_loc=orientZ[2],
                             limit_max_loc=orientZ[3])
    
    if not any(limit_point[0]):
        rig_flag.tx.lock()
        rig_flag.tx.set(keyable=False, channelBox=False)
    
    if not any(limit_point[1]):
        rig_flag.ty.lock()
        rig_flag.ty.set(keyable=False, channelBox=False)
    
    if not any(limit_point[2]):
        rig_flag.tz.lock()
        rig_flag.tz.set(keyable=False, channelBox=False)
    
    if not any(limit_orient[0]):
        rig_flag.rx.lock()
        rig_flag.rx.set(keyable=False, channelBox=False)
    
    if not any(limit_orient[1]):
        rig_flag.ry.lock()
        rig_flag.ry.set(keyable=False, channelBox=False)
    
    if not any(limit_orient[2]):
        rig_flag.rz.lock()
        rig_flag.rz.set(keyable=False, channelBox=False)


def add_limits_for_transform(node,
                             limit_name='translateLimitX',
                             limit_min=0,
                             limit_max=0,
                             limit_min_loc=True,
                             limit_max_loc=True):
    """
    Adds and sets the limit attributes.
    
    :param pm.nt.Transform node: Attribute to add the limit information.
    :param string limit_name: Attribute name
    :param float limit_min: Minimum attribute number.
    :param float limit_max: Maximum attribute number.
    :param bool limit_min_lock: If True, locks the min attribute.
    :param bool limit_max_lock: If True, locks the max attribute.
    """
    
    limit_min_name = limit_name + 'Min'
    limit_max_name = limit_name + 'Max'
    node.addAttr(limit_name, at='float2')
    node.addAttr(limit_min_name, at='float', parent=limit_name)
    node.addAttr(limit_max_name, at='float', parent=limit_name)
    node.attr(limit_min_name).set(limit_min)
    node.attr(limit_max_name).set(limit_max)
    if not limit_min_loc:
        node.attr(limit_min_name).lock(True)
    if not limit_max_loc:
        node.attr(limit_max_name).lock(True)


def remove_relationship_between_nodes(source_node, destination_node):
    """
    Disconnects all incoming connections from a source node to a destination node

    :param PyNode source_node: Source node to look for connections from
    :param PyNode destination_node: Destination node to look for incoming connections on
    """

    attributes = destination_node.listAttr()

    for attr in attributes:
        # Check if the attribute has incoming connections from the source node
        if attr.isDestination():
            sources = pm.listConnections(attr, source=True, plugs=True)
            for source in sources:
                if source.node() == source_node:
                    # Disconnect the attribute
                    pm.disconnectAttr(source, attr)


def get_enum_index(attr, enum_string):
    """
    Returns the index of a given string in a given enum attribute.

    :param str/pm.Attribute attr: Attribute to look in for a string.
    :param str enum_string: String to look for.
    :return: Returns the index of the given string in the attribute or None if not found.
    :rtype: int or None

    """

    attribute = pm.Attribute(attr)
    enum_strings = pm.attributeQuery(attribute.plugAttr(), node=attribute.node(), listEnum=True)[0].split(':')
    if enum_string in enum_strings:
        attr_index = enum_strings.index(enum_string.lower())
        return attr_index
    else:
        return None


