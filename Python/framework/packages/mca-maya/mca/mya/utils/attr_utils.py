#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""

# System global imports
import re
# software specific imports
import pymel.core as pm
import maya.cmds as cmds
import maya.api.OpenMaya as om

#  python imports
from mca.common.utils import lists
from mca.common import log
from mca.mya.utils import namespace
from mca.mya.modifiers import contexts
from mca.mya.utils.om import om_plug, attributetypes
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


def has_attribute(node, attr_name=''):
    """
    Efficient way of querying if an attribute exists on a PyNode or a DAG path. Runs slightly faster when given a DAG path,
    but isn't worth the cost of converting to a string path if you already have a PyNode instantiated.
    
    :param PyNode or str node: PyNode or string DAG path to object
    :param str attr_name: Name of the attribute to check for
    :return: Return True if the attribute exists, False if it doesn't, and None if the given node or path doesn't exist.
    :rtype: bool
    """
    
    sel_list = om.MSelectionList()
    sel_list.add(str(node))
    m_obj = sel_list.getDependNode(0)
    dep_node = om.MFnDependencyNode(m_obj)
    
    return dep_node.hasAttribute(attr_name)


def get_attribute(node, attr_name, attr_type='string'):
    """
    Efficient way of getting an attribute value that is slightly faster than using cmds getAttr.
    The trade-off is that the exact attribute type must be specified.
    
    :param PyNode or str node: PyNode or string DAG path to object
    :param attr_name: Name of attribute to get value of
    :param attr_type: Explicit type of attribute; supported types are 'string'
    :return: Returns the string name of the attribute value.
    :rtype: str
    """
    
    plug = None
    value = None
    
    if isinstance(node, pm.nt.DependNode):
        sel_list = om.MSelectionList()
        sel_list.add(str(node))
        m_obj = sel_list.getDependNode(0)
        dep_node = om.MFnDependencyNode(m_obj)
        plug = dep_node.findPlug(attr_name, True)
    
    if plug:
        if attr_type == 'string':
            value = plug.asString()
        else:
            raise Exception('get_attribute: Invalid attribute type of "{0}" specified!'.format(attr_type))
    
    return value


def get_indices(full_attribute):
    """
    Returns the index values of a multi attribute.
    
    :param str full_attribute: node.attribute name of a multi attribute (Exp: bShp1.inputTarget).
    :return: dictionary of integers that correspond to multi attribute indices.
    :rtype: dict
    """
    
    multi_attrs = pm.listAttr(full_attribute, multi=True)
    indices = dict()
    if not multi_attrs:
        return indices
    
    for multi_attr in multi_attrs:
        index = re.findall(r'\d+', multi_attr)
        if index:
            index = int(index[-1])
            indices[index] = None
    
    indices = list(indices.keys())
    indices.sort()
    
    return indices


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

    if attr_list is None:
        attr_list = TRANSFORM_ATTRS

    if not isinstance(node_list, list):
        node_list = [node_list]

    for node in node_list:
        # Unlock parent attrs so we can set the locks on a per attribute basis.
        node.unlock()
        node.t.unlock()
        node.r.unlock()
        node.s.unlock()

        for attr_name in attr_list:
            if locked:
                node.attr(attr_name).lock()
            else:
                node.attr(attr_name).unlock()
            if visibility:
                node.attr(attr_name).set(channelBox=not locked)
                node.attr(attr_name).set(keyable=not locked)

def lock_and_hide_attrs(node, attr_list):
    """
    Locks and hides attributes on a node.
    
    :param pm.nt.PyNode node: Any node that has the listed attributes
    :param list(str) attr_list: String list of attributes to lock.  EX: [tx, ty, tz] or [translateX,translateY,translateZ]
    """
    
    if not isinstance(attr_list, (tuple, list)):
        attr_list = [attr_list]
    
    for attr in attr_list:
        node.attr(attr).lock()
        node.attr(attr).set(keyable=False, channelBox=False)


def unlock_transform_attributes(node, transform_list=None):
    """
    Unlocks all transform values on the given transform node.
    
    :param pm.PyNode node: node we want to unlock transform attributes of.
    :param list(str) transform_list: list of attribute names to unlock. By default, all transforms will be unlocked.
    :return: list of all unlocked attributes.
    :rtype: list(pm.Attribute)
    """
    
    transform_list = lists.force_list(transform_list or TRANSFORM_ATTRS)
    unlocked_attrs = list()
    for attr_name in transform_list:
        attr = node.attr(attr_name)
        if attr.isLocked():
            unlocked_attrs.append(attr)
        attr.unlock()
    
    return unlocked_attrs


def lock_all_keyable_attrs(node, hidden=False, allow_visibility=False):
    """
    locks all keyable attrs on the specified node.
    
    :param pm.nt.PyNode node: a node that will have it's attributes locked.
    :param hidden: optional variable to hide attr after locking.
    :param bool allow_visibility: Lock or not lock the visibility channel.
    :return:
    """
    
    if not len(pm.ls(node)):
        raise pm.MayaNodeError("lock_all_keyable_attrs: input node does not exist '{0}'".format(node))
    
    node = pm.PyNode(node)
    keyable_attrs = node.listAttr(keyable=True)
    
    if len(keyable_attrs):
        for keyable_attr in keyable_attrs:
            if (not keyable_attr == node.nodeName() + '.v') or (
                    keyable_attr == node.nodeName() + '.v' and not allow_visibility):
                keyable_attr.lock()
            if hidden:
                keyable_attr.setKeyable(0)


def unlock_all_attrs(obj, show=False):
    """
    Unlocks all attrs on a given object.
    
    :param pm.nt.PyNode obj: A pynode that has locked attributes.
    :param bool show: Sets the attribute as keyable.
    """
    
    if not pm.objExists(obj):
        raise pm.MayaNodeError('#unlock_all_attrs: ' + str(obj) + ' doesnt exist.')
    
    obj = pm.PyNode(obj)
    attrs = obj.listAttr(locked=True)
    
    for attr in attrs:
        attr.unlock()
        if show:
            attr.setKeyable(1)


def lock_and_hide_object_attrs(attr_list):
    """
    Locks and hides attributes on a node.
    
    :param pm.nt.PyNode node: Any node that has the listed attributes
    :param list(str) attr_list: String list of attributes to lock.  EX: [tx, ty, tz] or [translateX,translateY,translateZ]
    """
    
    if not isinstance(attr_list, list) and not isinstance(attr_list, set):
        attr_list = [attr_list]
    
    attr_list = map(lambda attr: pm.PyNode(attr), attr_list)
    
    # Lock and hide attributes
    for attr in attr_list:
        attr.lock()
        attr.set(keyable=False, channelBox=False)


def unlock_and_show_attrs(attr_list):
    """
    Unlocks and unhides attributes.
    :param list attr_list: List of attributes on an object.
    """
    
    if not isinstance(attr_list, list):
        attr_list = [attr_list]
    
    attr_list = map(lambda attr: pm.PyNode(attr), attr_list)
    for attr in attr_list:
        if pm.objExists(attr):
            attr.setKeyable(1)
            attr.unlock()


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
            
            unlock_all_attrs(node)
            if skip_list:
                skip_attrs = [node.attr(x) for x in skip_list if node.hasAttr(x)]
                user_attrs = [attr for attr in user_attrs if attr not in skip_attrs]
            
            pm.deleteAttr(user_attrs)
        return user_attrs


def unlock_node_attributes(node, attributes=None, only_keyable=False):
    """
    Unlock attributes on given node.

    :param pm.PyNode node: node to unlock attributes of.
    :param list(str) attributes: list of attributes name to unlock on node. If None, unlock any that are locked.
    :param bool only_keyable: whether to unlock only the keyable attributes.
    :return: list of unlocked attributes.
    :rtype: list(pm.Attribute)
    """

    unlocked_attributes = list()
    if not attributes:
        if only_keyable:
            attributes = pm.listAttr(node, locked=True, k=True)
        else:
            attributes = pm.listAttr(node, locked=True)

    if attributes:
        attributes = lists.force_list(attributes)
        for attr_name in attributes:
            attr = node.attr(attr_name)
            if not attr.isLocked():
                continue
            pm.setAttr('{}.{}'.format(node, attr_name), lock=False, keyable=True, channelBox=True)
            pm.setAttr('{}.{}'.format(node, attr_name), keyable=True)
            unlocked_attributes.append(attr)

    return unlocked_attributes


def serialize_attribute(attribute_to_serialize, optimize=True, force=False):
    """
    Function that converts given PyMEL attribute into a serialized dictionary.
    
    :param pm.Attribute attribute_to_serialize: attribute to serialize.
    :param bool optimize: If True, all the serialized data with default values will be ignored.
    :return: serialized plug as a dictionary.
    :rtype: dict
    """
    
    # this operation is a common operation we need to maximize its speed.
    # for this reason we use OpenMaya to retrieve the data.
    full_name = attribute_to_serialize.name(fullDagPath=True)
    plug = om_plug.as_mplug(full_name)
    
    serialized_data = om_plug.serialize_plug(plug, optimize=optimize, force=force)
    serialized_data.update({
                'min': attribute_to_serialize.getMin(),
                'max': attribute_to_serialize.getMax(),
                'softMin': attribute_to_serialize.getSoftMin(),
                'softMax': attribute_to_serialize.getSoftMax()
                })
    
    # make sure we save the attribute type using PyMEL format (string) not OpenMaya format (integer)
    if 'type' in serialized_data:
        serialized_data['type'] = attributetypes.om_type_to_pymel_type(serialized_data['type'])
    
    return serialized_data


def get_all_objects_with_attr(attr_name, of_type=None, as_pynode=True):
    """
    Search for objects with a given attribute name within all namespaces.
    
    :param str attr_name: Name of the attribute to search
    :param str of_type: Type of objects to look for
    :param bool as_pynode: return a list of pynodes or strings
    :return:
    :rtype: list[pm.nt.dagNode]
    """
    
    all_namespaces = namespace.get_all_namespaces()
    all_namespaces.append('')
    objects = []
    
    for ns in all_namespaces:
        search_string = f'{ns[1:]}:*.{attr_name}'
        if not of_type:
            objects += cmds.ls(search_string, o=1)
        else:
            objects += cmds.ls(search_string, o=1, type=of_type)
    
    if not as_pynode:
        return objects
    
    return [pm.PyNode(x) for x in objects]


def reset_attrs(obj):
    """
    puts all keyable attributes to default values,
    translates,
    rotates to 0,
    scales,
    visibility to 1,
    customs to defaultValues
    
    :param pm.nt.PyNode obj: The pynode object to reset
    :return: Returns a list of attributes which were set
    :rtype: list(str)
    """
    if not pm.objExists(obj):
        raise pm.MayaNodeError("object given, {0} , doesn't exist".format(obj))
    
    obj = pm.PyNode(obj)
    keyable_attrs = obj.listAttr(keyable=1)
    keyable_attrs = filter(lambda x: not x.isHidden(), keyable_attrs)
    keyable_attrs = filter(lambda x: not x.isLocked(), keyable_attrs)
    is_transform = isinstance(obj, pm.nodetypes.Transform)
    transformAttrs_values = {}
    
    if is_transform:
        transformAttrs_values = {obj.tx: 0,
                                 obj.ty: 0,
                                 obj.tz: 0,
                                 obj.rx: 0,
                                 obj.ry: 0,
                                 obj.rz: 0,
                                 obj.sx: 1,
                                 obj.sy: 1,
                                 obj.sz: 1,
                                 obj.v: 1}
    attrs_set = []
    
    for attr in keyable_attrs:
        if is_transform:
            if attr in transformAttrs_values.keys():
                attr.set(transformAttrs_values[attr])
                attrs_set.append(attr)
        
        default_value = None
        
        if attr.isDynamic():
            default_value = pm.addAttr(attr, q=1, dv=1)
        
        failed_attrs = list()
        if not default_value is None:
            try:
                attr.set(default_value)
                attrs_set.append(attr)
            except RuntimeError:
                logger.warning(f'Failed to reset {attr}')
                failed_attrs.append(attr)
        if failed_attrs:
            logger.warning(f'Failed to reset {len(failed_attrs)} attrs | {failed_attrs}')
    
    return list(set(attrs_set))


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
                    'An incoming data type does not have a register in the MAYA_TYPE_DICT type: {0} for property: {1}'.format(
                            type(attr_value), attr_name)
    
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
                    start_index = max(found_index)+1 if found_index else 0
                for index, val in enumerate(attr_value):
                    if merge_values and val in original_values:
                        continue
                    try:
                        if isinstance(val, pm.Attribute):
                            # attribute first as it's a derivative of PyNode
                            val.node().message >> new_node_attr[index + start_index]
                            node.message >> val
                        elif isinstance(val, pm.PyNode):
                            val.message >> new_node_attr[index+start_index]
                        else:
                            new_node_attr[index+start_index].set(val)
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
        node.addAttr('_{0}_hidden'.format(compound_attr_name), attributeType='bool', parent=compound_attr_name, h=True)
    # END HACK
    # add child attrs to the compound, these still register as if added directly to the node.
    for property_name, property_value in attribute_dict.items():
        if not isinstance(property_name, str):
            'Dictionary key with value {0} is not a string, entry will be skipped.'.format(property_value)
            continue
        # since the attr is added directly to the node, we need to make the name a little more unique
        if not node.hasAttr('{0}_{1}'.format(compound_attr_name, property_name)):
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
                    'An incoming data type does not have a register in the MAYA_TYPE_DICT type: {0} for property: {1}, {2}'.format(
                        type(property_value), compound_attr_name, property_name)
            else:
                # data value was None
                string_property_type = 'string'
            if string_property_type:
                # concatenate the class name and property name to create a unique attr name. Objects cannot have more than one property group of the same type.
                if string_property_type in ['string']:
                    node.addAttr('{0}_{1}'.format(compound_attr_name, property_name),
                                 dataType=string_property_type,
                                 parent=compound_attr_name, nn=property_name, m=multi_attr)
                else:
                    node.addAttr('{0}_{1}'.format(compound_attr_name, property_name),
                                 attributeType=string_property_type,
                                 parent=compound_attr_name, nn=property_name, m=multi_attr)
    for property_name, property_value in attribute_dict.items():
        if not isinstance(property_name, str):
            continue
        # set property values.  This needs to be done after all child attributes have been added to the compound attr.
        if isinstance(property_value, pm.Attribute):
            # check if the receiver is a message attr
            property_value.disconnect()
            property_value >> node.attr('{0}_{1}'.format(compound_attr_name, property_name))
        # node.attr('{0}_{1}'.format(compound_attr_name, property_name)) >> property_value
        
        elif isinstance(property_value, pm.PyNode):
            # To handle message type connections
            if pm.attributeQuery('message', node=property_value, exists=True):
                property_value.message >> node.attr('{0}_{1}'.format(compound_attr_name, property_name))
            else:
                'does not have a message attr and could not be connected.'.format(property_value)
        elif isinstance(property_value, (list, tuple)):
            # to handle multi attrs
            for index, value in enumerate(property_value):
                if value is None:
                    # we can't set None
                    continue
                if isinstance(property_value, pm.Attribute):
                    # check if the receiver is a message attr
                    property_value.disconnect()
                    property_value >> node.attr('{0}_{1}'.format(compound_attr_name, property_name))
                    # node.attr('{0}_{1}'.format(compound_attr_name, property_name)) >> property_value
                elif isinstance(value, pm.PyNode):
                    # to handle message type connections
                    if pm.attributeQuery('message', node=value, exists=True):
                        value >> node.attr('{0}_{1}'.format(compound_attr_name, property_name))[index]
                    else:
                        '{0} does not have a message attr and could not be connected.'.format(value)
                else:
                    node.attr('{0}_{1}'.format(compound_attr_name, property_name))[index].set(value)
        else:
            # For standard single value settings.
            if property_value is not None:
                # We can't set None
                node.attr('{0}_{1}'.format(compound_attr_name, property_name)).set(property_value)


def create_message_compound_attr(node, attr_names, compound_attr_name):
    """
    Creates a compound attribute with a list of attribute names.
    The compound attr uses message attributes.
    
    :param pm.nt.Transform node: Maya transform to create compound attributes.
    :param list(str) attr_names: list of attribute names to use in the compound attribute.
    :param str compound_attr_name: the name of the compound attribute
    :return: returns the newly created compound attribute.
    :rtype: pm.nt.General.Attribute
    """
    
    if not isinstance(attr_names, list):
        logger.error('Attribute names must be a list.')
        return
    obj_number = len(attr_names)
    node.addAttr(compound_attr_name, numberOfChildren=obj_number, attributeType='compound')
    for x in range(obj_number):
        node.addAttr(str(attr_names[x]), attributeType='message', parent=compound_attr_name)
    compound_attr = node.attr(compound_attr_name)
    if not node.hasAttr(compound_attr_name):
        compound_attr.setAlias(compound_attr_name)
    return compound_attr


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


def invert_attribute(attr):
    """
    Reverses the attribute.
    
    :param str attr: Attribute name.
    :return: Returns the setRange node that reverses the value.
    :rtype: pm.nt.setRange
    """
    
    node_name = pm.PyNode(attr).nodeName().split(':')[-1]
    node_name = node_name.replace('.', '_')
    # Create setRange Node
    reverse_node = pm.createNode("setRange", n="{0}_inverseAttr".format(node_name))
    pm.setAttr(".min", [0, 1, 0], k=False, lock=True)
    pm.setAttr(".max", [1, 0, 100], k=False, lock=True)
    pm.setAttr(".oldMin", [0, 0, 0], k=False, lock=True)
    pm.setAttr(".oldMax", [1, 1, 1], k=False, lock=True)
    pm.aliasAttr("straight", "{0}.outValueX".format(reverse_node), "inverse", "{0}.outValueY".format(reverse_node),
                 "percentage", "{0}.outValueZ".format(reverse_node))
    pm.connectAttr(attr, "{0}.valueX".format(reverse_node), force=True)
    pm.connectAttr(attr, "{0}.valueY".format(reverse_node), force=True)
    pm.connectAttr(attr, "{0}.valueZ".format(reverse_node), force=True)
    return reverse_node


def set_limits(rig_flag,
               rig_node=None,
               limit_point=((None, None), (None, None), (None, None)),
               limit_orient=((None, None), (None, None), (None, None))):
    """
    Sets limits on a flag and stamps the info onto a network node.
    
    :param flag.Flag rig_flag: A rig Flag
    :param TEKNode rig_node: TEK Node
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


def connect_nodes_with_message_attrs(source_node, source_attr, target_node, target_attr):
    """
    connect two nodes with provided message attrs.
    :param      PyNode      source_node :source node connecting from
    :param      str         source_attr :attribute on object a we'd like to connect as out
    :param      PyNode      target_node :target node connecting to
    :param      str         target_attr :attribute on object a we'd like to connect as in
    :return:
    """

    source_attr_node = None
    target_attr_node = None

    # Source Attr
    if isinstance(source_attr, str):
        if source_node.hasAttr(source_attr):
            source_attr_node = source_node.attr(
                source_attr)  # this attr wrappiing may need to be optimized down the road.
            if not source_attr_node.type() == 'message':
                raise AttributeError(
                    '{node}:{attr} is not a message attribute and was not connected.'.format(node=source_node,
                                                                                             attr=source_attr))
        else:
            source_node.addAttr(source_attr, at='message')
            source_attr_node = source_node.attr(source_attr)

    elif isinstance(source_attr, pm.Attribute):
        if source_attr.type() == 'message':
            source_attr_node = source_attr

    # target attr
    if isinstance(target_attr, str):
        if target_node.hasAttr(target_attr):
            target_attr_node = target_node.attr(target_attr)
            if not target_attr_node.type() == 'message':
                raise AttributeError(
                    '{node}:{attr} is not a message attribute and was not connected.'.format(node=target_node,
                                                                                             attr=target_attr))
        else:
            target_node.addAttr(target_attr, at='message')
            target_attr_node = target_node.attr(target_attr)

    elif isinstance(target_attr, pm.Attribute):
        if target_attr.type() == 'message':
            target_attr_node = target_attr

    # connect
    try:
        source_attr_node >> target_attr_node
    except Exception:
        pass


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


