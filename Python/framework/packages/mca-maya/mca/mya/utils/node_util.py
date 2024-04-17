#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that interact with transforms
"""

# System global imports
import json
import copy
# software specific imports
import pymel.core as pm

#  python imports
from mca.common.utils import lists, strings
from mca.mya.utils import material_utils, naming, namespace
from mca.mya.utils.om import attributetypes
from mca.mya.modifiers import ma_decorators
from mca.mya.plugins import loader
from mca.mya.utils import attr_utils
from mca.common import log

logger = log.MCA_LOGGER

ATTRIBUTES_TO_SKIP_SERIALIZE = ['message', 'center', 'hyperLayout', 'boundingBox', 'mcaConstraint']


class RotateOrder(object):
    XYZ = 'XYZ'
    YZX = 'YZX'
    ZXY = 'ZXY'
    XZY = 'XZY'
    YXZ = 'YXZ'
    ZYX = 'ZYX'

    @staticmethod
    def get_all():
        return [RotateOrder.XYZ, RotateOrder.YZX, RotateOrder.ZXY, RotateOrder.XZY, RotateOrder.YXZ, RotateOrder.ZYX]

    @staticmethod
    def from_index(index):
        if not isinstance(int, index):
            if index is not None and hasattr(index, 'index') and not callable(index.index):     # support for PyMEL enum
                index = index.index - 1
            else:
                return index

        return RotateOrder.get_all()[index]

    @staticmethod
    def to_index(rotate_order):
        return RotateOrder.get_all().index(str(rotate_order).upper())


def match_translation(transform_name_to_match, target_transform_name, space=None):
    """
    Matches the translation.

    :param nt.PyNode transform_name_to_match: name of the transform we want to match translation to target transform.
    :param nt.PyNode target_transform_name: name of the transform we want to match translation to.
    :param str space: whether to match translation in object space or world space. By default, in world space.
    """

    translate_vector = pm.xform(node=target_transform_name, space=space)
    scale_pivot_vector = pm.xform(node=target_transform_name, sp=True, ws=False)
    rotate_pivot_vector = pm.xform(node=target_transform_name, rp=True, world_space=False)
    pm.xform(node=transform_name_to_match, sp=scale_pivot_vector, world_space=False)
    pm.xform(node=transform_name_to_match, rp=rotate_pivot_vector, world_space=False)
    transform_name_to_match.setTranslatrion(position=translate_vector, space=space)


def match_rotation(transform_name_to_match, target_transform_name, space=None):
    """
    Matches the rotation in object or world space.

    :param nt.PyNode transform_name_to_match: name of the transform we want to match rotation to target transform.
    :param nt.PyNode target_transform_name: name of the transform we want to match rotation to.
    :param str space: whether to match rotation in object space or world space. By default, in world space.
    """

    rotation_vector = target_transform_name.getRotation(space=space)
    rotation_vector = rotation_vector.reorderIt(rotation_vector.getRotationOrder())
    pm.xform(node=transform_name_to_match, position=rotation_vector, space=space)


def reset_transform(transform_node, translate=True, rotate=True, scale=True):
    """
    Resets the transform of this node.

    :param :class:`pm.nt.Transform` transform_node: PyMEL node we want to set transform matrix of.
    :param bool translate: whether to reset translate components of this node transformation.
    :param bool rotate: whether to reset rotation components of this node transformation.
    :param bool scale: whether to reset scale components of this node transformation.
    """

    if translate:
        transform_node.setTranslation((0, 0, 0))
    if rotate:
        transform_node.setRotation(pm.dt.Quaternion(), space='transform')
    if scale:
        transform_node.setScale((1, 1, 1))


def is_empty(node, no_user_attributes=True, no_connections=True):
    """
    Returns whether a given node is an empty one (is not referenced, has no child transforms, has no custom attributes
    and has no connections).

    :param pm.PyNode node: name of a Maya node we want to check.
    :param bool no_user_attributes: whether a node is considered empty if it contains user attributes.
    :param bool no_connections: whether a node is considered empty if it contains connections.
    :return: True if the given node is an empty node; False otherwise.
    :rtype: bool
    """

    if pm.referenceQuery(node, isNodeReferenced=True):
        return False

    if isinstance(node, pm.nt.Transform):
        relatives = pm.listRelatives(node)
        if relatives:
            return False

    if no_user_attributes:
        attrs = pm.listAttr(node, userDefined=True, keyable=True)
        if attrs:
            return False

    default_nodes = ['defaultLightSet', 'defaultObjectSet', 'initialShadingGroup', 'uiConfigurationScriptNode',
                     'sceneConfigurationScriptNode']
    if node in default_nodes:
        return False

    if no_connections:
        connections = pm.listConnections(node)
        if connections != ['defaultRenderGlobals']:
            if connections:
                return False

    return True


def create_or_find(name, node_type):
    """
    Find by name or create a new node of the given type.

    :param str name: The desired name of the new node.
    :param PyNode node_type: The PyNode class of the node type.
    :return: The created or found PyNode.
    :rtype: PyNode
    """

    node = lists.get_first_in_list(pm.ls(name, r=True, type=node_type))
    if not node:
        node = pm.createNode(node_type, n=name)
    return node


@ma_decorators.keep_namespace_decorator
@ma_decorators.keep_selection_decorator
def rbf_retarget(source_node, target_node, nodes_to_process):
    """
    Using Hans Godard's RBF system reprocess a list of shaped transforms using two same topology source and target meshes.

    :param Transform source_node: The source shaped transform. This is what our processable meshes work with.
    :param Transform target_node: The target shaped transform. This is what we want our processable meshes to be morphed to.
    :param list[Transform] nodes_to_process: A list of shaped transforms we want to be run through the RBF retargeter.
    :return: A list of the reprocessed meshes.
    :rtype: list[Transform]
    """
    loader.load_rbf_retargeter_plugin()

    source_shape = source_node.getShape()
    if not source_shape:
        return []

    target_shape = target_node.getShape()
    if not target_shape:
        return []

    shape_node_list = []
    name_material_dict = {}
    count = 0
    for node in nodes_to_process:
        node_shape = node.getShape()
        if node_shape:
            shape_node_list.append(node_shape)
            node_name = naming.get_basename(node)
            material_dict = material_utils.get_object_material_face_dict(node)
            name_material_dict[count] = (node_name, material_dict)
            count += 1

    if not shape_node_list:
        return []

    temp_namespace = strings.generate_random_string(5)
    pm.namespace(set=temp_namespace)

    reshaped_nodes_list = pm.retargetShapes(source_shape, shape_node_list, target_shape, True, [])
    pm.namespace(set=':')

    return_list = []
    for index, str_name in enumerate(reshaped_nodes_list):
        node = pm.PyNode(str_name)
        return_list.append(node)
        node_name, material_dict = name_material_dict[index]
        for material_node, face_list in material_dict.items():
            material_utils.assign_material(material_node, node.f[face_list])
            node.rename(node_name)
            namespace.move_node_to_namespace(node, ':')

    namespace.purge_namespace(temp_namespace)

    return return_list


########################################################
# EVERYTHING BELOW THIS NEEDS TO DIE
########################################################
def add_attribute(node, **kwargs):
    """
    Adds a new attribute to the given PyNode. This function uses PyMEL addAttr function but give us a bit more
    flexibility:
        - Allow us to pass a dictionary with all arguments as keyword arguments. For example: {'name': 'test,
            'value': helloWorld, 'type': 'string', 'locked': True, 'storable': True, 'writable': True,
            'connectable': False}
        - Allow us to set a default value for string attributes (using value keyword argument).
        - Automatically handles the connectable, array and lock status of the attribute.

    :param pm.PyNode node: node to add attribute to.
    :param dict kwargs: keyword arguments.
    :return: newly create PyAttribute instance.
    :rtype: pm.Attribute
    :raises ValueError: if the attribute already exists.
    :raises TypeError: if the attribute type is not supported.
    """

    raise_exceptions = kwargs.pop('raise_exceptions', False)
    attr_name = kwargs.pop('name', None) or kwargs.pop('longName', None) or kwargs.pop('shortName', None)
    if node.hasAttr(attr_name):
        set_attribute_info_from_dict(node.attr(attr_name), **kwargs)
        if raise_exceptions:
            raise RuntimeError('Node "{}" already has attribute "{}"'.format(
                node.longName(), attr_name))
        return node.attr(attr_name)

    children = kwargs.pop('children', None)
    if children:
        attr = attr_utils.add_compound_attribute(node, name=attr_name, attr_map=children, **kwargs)
    else:
        attr_type = kwargs.pop('type', None) or kwargs.pop('attrType', None) or kwargs.pop('attr_type', None)
        if attr_type and isinstance(attr_type, int):
            attr_type = attributetypes.om_type_to_pymel_type(attr_type)

        if attr_type == 'complex':
            attr_type = 'string'
            value = kwargs.get('value', None)
            default = kwargs.get('default', None)
            if value and isinstance(value, dict):
                try:
                    kwargs['value'] = json.dumps(value)
                except Exception as exc:
                    logger.warning('Was not possible to convert dictionary to string!')
                    kwargs['value'] = ''
            if default and isinstance(default, dict):
                try:
                    kwargs['default'] = json.dumps(default)
                except Exception:
                    logger.warning('Was not possible to convert dictionary to string!')
                    kwargs['default'] = ''

        add_kwargs = kwargs.copy()
        add_kwargs['type'] = attr_type
        add_kwargs.pop('locked', False)
        add_kwargs.pop('isChild', False)
        add_kwargs.pop('isDynamic', True)
        add_kwargs.pop('isElement', False)
        add_kwargs.pop('softMin', None)
        add_kwargs.pop('softMax', None)
        add_kwargs.pop('min', None)
        add_kwargs.pop('max', None)
        value = add_kwargs.pop('value', None)
        connectable = add_kwargs.pop('connectable', True)
        channel_box = add_kwargs.pop('channelBox', False)
        is_array = add_kwargs.pop('isArray', False)
        default = add_kwargs.pop('default', None)
        default = default if default is not None else add_kwargs.pop('defaultValue', None)
        if 'multi' not in kwargs:
            add_kwargs['multi'] = is_array
        if 'writable' not in add_kwargs:
            add_kwargs['writable'] = connectable
        enums = add_kwargs.pop('enums', list())
        if enums:
            enum_names = add_kwargs.get('enumNames', list())
            enum_names.extend(enums)
            add_kwargs['enumName'] = list(set(enum_names))

        # if a value is given and the is a number we set defaultValue keyword argument
        if default is not None and isinstance(value, (int, float)):
            add_kwargs['defaultValue'] = value if value is not None else default

        node.addAttr(attr_name, **add_kwargs)
        attr = node.attr(attr_name)

        # if a value is given and the attribute type is a string, we set attribute value
        if value is not None and attr_type == 'string':
            attr.set(value)

        attr.showInChannelBox(channel_box)
        set_attribute_info_from_dict(attr, **kwargs)

    return attr


def set_attribute_info_from_dict(attr, **kwargs):
    """
    Sets the plug attributes from the given keyword arguments.

    :param pm.Attribute attr: plug to change.
    :param dict kwargs: keyword arguments.
    :raises RuntimeError: if an exception is raised while setting plug info.

    .. code-block:: python
        data = {
            "type": 5,
            "channelBox": true,
            "default": 1.0,
            "isDynamic": true,
            "keyable": true,
            "locked": false,
            "max": 99999,
            "min": 0.0,
            "name": "scale",
            "softMax": None,
            "softMin": None,
            "value": 1.0,
            "children": [{}] # in the same format as the parent info
          }
        new_plug = pm.Attribute(node)
        set_plug_info_from_dict(new_plug, **data)
    """

    children = kwargs.get('children', list())
    if attr.isCompound() and not attr.isArray():
        child_count = attr.numChildren()
        _children = attr.getChildren()
        if not children:
            children = [copy.deepcopy(kwargs) for i in range(child_count)]
            for i, child_info in enumerate(children):
                if not child_info:
                    continue
                if i in range(child_count):
                    value = child_info.get('value')
                    default_value = child_info.get('default')
                    if value is not None and i in range(len(value)):
                        child_info['value'] = value[i]
                    if default_value is not None and i in range(len(default_value)):
                        child_info['default'] = default_value[i]
                    set_attribute_info_from_dict(_children[i], **child_info)
        else:
            for i, child_info in enumerate(children):
                if not child_info:
                    continue
                if i in range(child_count):
                    child_plug = _children[i]
                    try:
                        set_attribute_info_from_dict(child_plug, **child_info)
                    except RuntimeError:
                        logger.error('Failed to set default values on plug: {}'.format(
                            child_plug.name()), extra={'attributeDict': child_info})
                        raise

    default = kwargs.get('default')
    min = kwargs.get('min')
    max = kwargs.get('max')
    soft_min = kwargs.get('softMin')
    soft_max = kwargs.get('softMax')
    value = kwargs.get('value')
    channel_box = kwargs.get('channelBox')
    keyable = kwargs.get('keyable')
    locked = kwargs.get('locked')

    if default is not None:
        pass
    # try:
    #     set_plug_default(plug, default)
    # except Exception:
    #     logger.error('Failed to set plug default values: {}'.format(plug.name()),
    #                  exc_info=True,
    #                  extra={'data': default})
    #     raise

    if value is not None and not attr.isCompound() and not attr.isArray():
        attr.set(value)
    if min is not None:
        attr.setMin(min)
    if max is not None:
        attr.setMax(max)
    if soft_min is not None:
        attr.setSoftMin(soft_min)
    if soft_max is not None:
        attr.setSoftMax(soft_max)
    if channel_box is not None:
        attr.showInChannelBox(channel_box)
    if keyable is not None:
        attr.setKeyable(keyable)
    if locked is not None:
        attr.setLocked(locked)