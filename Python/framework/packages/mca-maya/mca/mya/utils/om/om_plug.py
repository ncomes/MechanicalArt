#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that centralizes May attribute types
"""
# System global imports
# software specific imports
import maya.api.OpenMaya as OpenMaya
# mca python imports
from mca.mya.utils.om import attributetypes


def as_mplug(attribute_full_name):
    """
    Returns the MPlug instance of the given attribute full name (node.attribute_name).

    :param str attribute_full_name: full name of the Maya attribute to convert to MPlug
    :return: MPlug associated to given attribute name/
    :rtype: OpenMaya.MPlug
    """

    try:
        names = attribute_full_name.split(".")
        sel = OpenMaya.MSelectionList()
        sel.add(names[0])
        node = OpenMaya.MFnDependencyNode(sel.getDependNode(0))
        return node.findPlug('.'.join(names[1:]), False)
    except RuntimeError:
        sel = OpenMaya.MSelectionList()
        sel.add(str(attribute_full_name))
        return sel.getPlug(0)


def serialize_plug(plug, optimize=True, force=False):
    """
    Function that converts given OpenMaya.MPlug into a serialized dictionary.

    :param om.Plug plug: plug to serialize.
    :param bool optimize: If True, all the serialized data with default values will be ignored.
    :return: serialized plug as a dictionary.
    :rtype: dict
    """

    data = {'isDynamic': plug.isDynamic}
    attr_type = get_plug_type(plug)
    if not plug.isDynamic:

        # skip any default attribute that has not changed value.
        if plug.isDefaultValue() and not force:
            return dict()
        elif plug.isCompound:
            data['children'] = [serialize_plug(plug.child(i)) for i in range(plug.numChildren())]
        elif plug.isArray:
            return dict()

    elif attr_type != attributetypes.kMFnMessageAttribute:
        if plug.isDefaultValue() and not force:
            data['children'] = list()
        elif plug.isCompound:
            if plug.isArray:
                element = plug.elementByLogicalIndex(0)
                data['children'] = [serialize_plug(element.child(i)) for i in range(element.numChildren())]
            else:
                data['children'] = [serialize_plug(plug.child(i)) for i in range(plug.numChildren())]
        elif plug.isArray:
            data['children'] = list()

    data.update({
        'name': plug.partialName(includeNonMandatoryIndices=True, useLongNames=True, includeInstancedIndices=True),
        'channelBox': plug.isChannelBox,
        'keyable': plug.isKeyable,
        'locked': plug.isLocked,
        'isArray': plug.isArray,
        'default': attributetypes.maya_type_to_python_type(get_plug_default(plug)),
        'type': attr_type,
        'value': get_python_type_from_plug_value(plug),
        'isElement': plug.isElement,
        'isChild': plug.isChild
     })

    if get_plug_type(plug) == attributetypes.kMFnkEnumAttribute:
        data['enums'] = get_enum_names(plug)

    # optimize attribute serialized data
    if optimize:
        if data['channelBox'] is True:
            data.pop('channelBox')
        if data['keyable'] is False:
            data.pop('keyable')
        if data['locked'] is False:
            data.pop('locked')
        if data['isArray'] is False:
            data.pop('isArray')
        if data['isElement'] is False:
            data.pop('isElement')
        if data['isChild'] is False:
            data.pop('isChild')
        if not data.get('children', list()):
            data.pop('children', None)
        if data['isDynamic'] is True:
            data.pop('isDynamic')
        if data.get('min', None) is None:
            data.pop('min', None)
        if data.get('max', None) is None:
            data.pop('max', None)
        if data.get('softMin', None) is None:
            data.pop('softMin', None)
        if data.get('softMax', None) is None:
            data.pop('softMax', None)

    return data


def get_plug_type(plug):
    """
    Returns the type of the given OpenMaya MPlug.

    :param MPlug plug: plug we want to retrieve type and value of.
    :return: MPlug type.
    :rtype: str

    ..note:: If possible Python default type will be returned.
    """

    obj = plug.attribute()

    if obj.hasFn(OpenMaya.MFn.kCompoundAttribute):
        return attributetypes.kMFnCompoundAttribute
    if obj.hasFn(OpenMaya.MFn.kNumericAttribute):
        n_attr = OpenMaya.MFnNumericAttribute(obj)
        data_type = n_attr.numericType()
        return attributetypes.maya_numeric_type_to_internal_type(data_type)
    elif obj.hasFn(OpenMaya.MFn.kUnitAttribute):
        u_attr = OpenMaya.MFnUnitAttribute(obj)
        ut = u_attr.unitType()
        return attributetypes.maya_unit_type_to_internal_type(ut)
    elif obj.hasFn(OpenMaya.MFn.kTypedAttribute):
        t_attr = OpenMaya.MFnTypedAttribute(obj)
        data_type = t_attr.attrType()
        return attributetypes.maya_mfn_data_type_to_internal_type(data_type)
    elif obj.hasFn(OpenMaya.MFn.kEnumAttribute):
        return attributetypes.kMFnkEnumAttribute
    elif obj.hasFn(OpenMaya.MFn.kMessageAttribute):
        return attributetypes.kMFnMessageAttribute
    elif obj.hasFn(OpenMaya.MFn.kMatrixAttribute):
        return attributetypes.kMFnDataMatrix

    return None


def get_plug_default(plug):
    """
    Returns the default value of the given plug.

    :param OpenMaya.MPlug plug: plug to retrieve default value of.
    :return: plug default value.
    :rtype: object or None
    """

    obj = plug.attribute()
    if obj.hasFn(OpenMaya.MFn.kNumericAttribute):
        attr = OpenMaya.MFnNumericAttribute(obj)
        if attr.numericType() == OpenMaya.MFnNumericData.kInvalid:
            return None
        return attr.default
    elif obj.hasFn(OpenMaya.MFn.kTypedAttribute):
        attr = OpenMaya.MFnTypedAttribute(obj)
        default = attr.default
        if default.apiType() == OpenMaya.MFn.kInvalid:
            return None
        elif default.apiType() == OpenMaya.MFn.kStringData:
            return OpenMaya.MFnStringData(default).string()
        return default
    elif obj.hasFn(OpenMaya.MFn.kUnitAttribute):
        attr = OpenMaya.MFnUnitAttribute(obj)
        return attr.default
    elif obj.hasFn(OpenMaya.MFn.kMatrixAttribute):
        attr = OpenMaya.MFnMatrixAttribute(obj)
        return attr.default
    elif obj.hasFn(OpenMaya.MFn.kEnumAttribute):
        attr = OpenMaya.MFnEnumAttribute(obj)
        return attr.default

    return None


def get_python_type_from_plug_value(plug):
    """
    Returns Python type of the given MPlug.

    :param OpenMaya.MPlug plug: plug whose python type we want to retrieve.
    :return: Python type.
    :rtype: int, float, str, list or None
    """

    data_type, value = get_plug_type_and_value(plug)
    types = (attributetypes.kMFnDataMatrix, attributetypes.kMFnDataFloatArray,
             attributetypes.kMFnDataFloatArray, attributetypes.kMFnDataDoubleArray,
             attributetypes.kMFnDataIntArray, attributetypes.kMFnDataPointArray, attributetypes.kMFnDataStringArray,
             attributetypes.kMFnNumeric2Double, attributetypes.kMFnNumeric2Float, attributetypes.kMFnNumeric2Int,
             attributetypes.kMFnNumeric2Long, attributetypes.kMFnNumeric2Short, attributetypes.kMFnNumeric3Double,
             attributetypes.kMFnNumeric3Float, attributetypes.kMFnNumeric3Int, attributetypes.kMFnNumeric3Long,
             attributetypes.kMFnNumeric3Short, attributetypes.kMFnNumeric4Double)
    if data_type is None or data_type == attributetypes.kMFnMessageAttribute:
        return None
    elif isinstance(data_type, (list, tuple)):
        res = list()
        for idx, dt in enumerate(data_type):
            if dt == attributetypes.kMFnDataMatrix:
                res.append(tuple(value[idx]))
            elif dt in (
                    attributetypes.kMFnUnitAttributeDistance, attributetypes.kMFnUnitAttributeAngle,
                    attributetypes.kMFnUnitAttributeTime):
                res.append(value[idx].value)
        return res
    elif data_type in (attributetypes.kMFnDataMatrixArray, attributetypes.kMFnDataVectorArray):
        return list(map(tuple, value))
    elif data_type in (
            attributetypes.kMFnUnitAttributeDistance, attributetypes.kMFnUnitAttributeAngle,
            attributetypes.kMFnUnitAttributeTime):
        return value.value
    elif data_type in types:
        return tuple(value)

    return value


def get_enum_names(plug):
    """
    Returns the plug enumeration field names.

    :param OpenMaya.MPlug plug: MPlug to query enumeration field names from.
    :return: sequence of enum names.
    :rtype: list(str)
    """

    obj = plug.attribute()
    enum_fields = []
    if obj.hasFn(OpenMaya.MFn.kEnumAttribute):
        attr = OpenMaya.MFnEnumAttribute(obj)
        min_value = attr.getMin()
        max_value = attr.getMax()
        for i in range(min_value, max_value + 1):
            try:
                enum_fields.append(attr.fieldName(i))
            except Exception:
                pass

    return enum_fields


def get_plug_type_and_value(plug):
    """
    Returns the value and the type of the given OpenMaya MPlug.

    :param MPlug plug: plug we want to retrieve type and value of.
    :return: tuple containing the MPlug type and value.
    :rtype: tuple(int, object)

    ..note:: If possible Python default type will be returned.
    """

    mobj = plug.attribute()
    if plug.isArray:
        count = plug.evaluateNumElements()
        result = [None] * count, [None] * count
        data = [get_plug_type_and_value(plug.elementByPhysicalIndex(i)) for i in range(count)]
        for i in range(len(data)):
            result[0][i] = data[i][0]
            result[1][i] = data[i][1]
        return result

    if mobj.hasFn(OpenMaya.MFn.kNumericAttribute):
        return get_numeric_type_and_value(plug)
    elif mobj.hasFn(OpenMaya.MFn.kTypedAttribute):
        return get_typed_type_and_value(plug)
    elif mobj.hasFn(OpenMaya.MFn.kUnitAttribute):
        unit_attr = OpenMaya.MFnUnitAttribute(mobj)
        unit_type = unit_attr.unitType()
        if unit_type == OpenMaya.MFnUnitAttribute.kDistance:
            return attributetypes.kMFnUnitAttributeDistance, plug.asMDistance()
        elif unit_type == OpenMaya.MFnUnitAttribute.kAngle:
            return attributetypes.kMFnUnitAttributeAngle, plug.asMAngle()
        elif unit_type == OpenMaya.MFnUnitAttribute.kTime:
            return attributetypes.kMFnUnitAttributeTime, plug.asMTime()
    elif mobj.hasFn(OpenMaya.MFn.kEnumAttribute):
        return attributetypes.kMFnkEnumAttribute, plug.asInt()
    elif mobj.hasFn(OpenMaya.MFn.kMessageAttribute):
        source = plug.source()
        if source is not None:
            return attributetypes.kMFnMessageAttribute, source.node()
        return attributetypes.kMFnMessageAttribute, None
    elif mobj.hasFn(OpenMaya.MFn.kMatrixAttribute):
        return attributetypes.kMFnDataMatrix, OpenMaya.MFnMatrixData(plug.asMObject()).matrix()

    if plug.isCompound:
        count = plug.numChildren()
        result = [None] * count, [None] * count
        data = [get_plug_type_and_value(plug.child(i)) for i in range(count)]
        for i in range(len(data)):
            result[0][i] = data[i][0]
            result[1][i] = data[i][1]
        return result

    return None, None


def get_numeric_type_and_value(plug):
    """
    Returns the numeric type and value of the given OpenMaya MPlug.

    :param MPlug plug: plug we want to retrieve numeric type and value of.
    :return: tuple containing the numeric attribute type and value.
    :rtype: tuple(int, int or float)
    """

    obj = plug.attribute()
    n_attr = OpenMaya.MFnNumericAttribute(obj)
    data_type = n_attr.numericType()
    if data_type == OpenMaya.MFnNumericData.kBoolean:
        return attributetypes.kMFnNumericBoolean, plug.asBool()
    elif data_type == OpenMaya.MFnNumericData.kByte:
        return attributetypes.kMFnNumericByte, plug.asBool()
    elif data_type == OpenMaya.MFnNumericData.kShort:
        return attributetypes.kMFnNumericShort, plug.asShort()
    elif data_type == OpenMaya.MFnNumericData.kInt:
        return attributetypes.kMFnNumericInt, plug.asInt()
    elif data_type == OpenMaya.MFnNumericData.kLong:
        return attributetypes.kMFnNumericLong, plug.asInt()
    elif data_type == OpenMaya.MFnNumericData.kDouble:
        return attributetypes.kMFnNumericDouble, plug.asDouble()
    elif data_type == OpenMaya.MFnNumericData.kFloat:
        return attributetypes.kMFnNumericFloat, plug.asFloat()
    elif data_type == OpenMaya.MFnNumericData.kAddr:
        return attributetypes.kMFnNumericAddr, plug.asAddr()
    elif data_type == OpenMaya.MFnNumericData.kChar:
        return attributetypes.kMFnNumericChar, plug.asChar()
    elif data_type == OpenMaya.MFnNumericData.k2Double:
        return attributetypes.kMFnNumeric2Double, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k2Float:
        return attributetypes.kMFnNumeric2Float, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k2Int:
        return attributetypes.kMFnNumeric2Int, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k2Long:
        return attributetypes.kMFnNumeric2Long, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k2Short:
        return attributetypes.kMFnNumeric2Short, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k3Double:
        return attributetypes.kMFnNumeric3Double, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k3Float:
        return attributetypes.kMFnNumeric3Float, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k3Int:
        return attributetypes.kMFnNumeric3Int, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k3Long:
        return attributetypes.kMFnNumeric3Long, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k3Short:
        return attributetypes.kMFnNumeric3Short, OpenMaya.MFnNumericData(plug.asMObject()).getData()
    elif data_type == OpenMaya.MFnNumericData.k4Double:
        return attributetypes.kMFnNumeric4Double, OpenMaya.MFnNumericData(plug.asMObject()).getData()

    return None, None


def get_typed_type_and_value(plug):
    """
    Returns the typed type and value of the given OpenMaya MPlug.

    :param MPlug plug: plug we want to retrieve typed type and value of.
    :return: tuple containing the typed attribute type and value.
    :rtype: tuple(int, object)
    """
    
    typed_attr = OpenMaya.MFnTypedAttribute(plug.attribute())
    data_type = typed_attr.attrType()
    if data_type == OpenMaya.MFnData.kInvalid:
        return None, None
    elif data_type == OpenMaya.MFnData.kString:
        return attributetypes.kMFnDataString, plug.asString()
    elif data_type == OpenMaya.MFnData.kNumeric:
        return get_numeric_type_and_value(plug)
    elif data_type == OpenMaya.MFnData.kMatrix:
        return attributetypes.kMFnDataMatrix, OpenMaya.MFnMatrixData(plug.asMObject()).matrix()
    elif data_type == OpenMaya.MFnData.kFloatArray:
        # TODO: MFnFloatArrayData is missing from OpenMaya 2.0
        # return attributetypes.kMFnDataFloatArray, OpenMaya.MFnFloatArrayData(plug.asMObject()).array()
        return attributetypes.kMFnDataDoubleArray, OpenMaya.MFnDoubleArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kDoubleArray:
        return attributetypes.kMFnDataDoubleArray, OpenMaya.MFnDoubleArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kIntArray:
        return attributetypes.kMFnDataIntArray, OpenMaya.MFnIntArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kPointArray:
        return attributetypes.kMFnDataPointArray, OpenMaya.MFnPointArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kVectorArray:
        return attributetypes.kMFnDataVectorArray, OpenMaya.MFnVectorArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kStringArray:
        return attributetypes.kMFnDataStringArray, OpenMaya.MFnStringArrayData(plug.asMObject()).array()
    elif data_type == OpenMaya.MFnData.kMatrixArray:
        return attributetypes.kMFnDataMatrixArray, OpenMaya.MFnMatrixArrayData(plug.asMObject()).array()
    
    return None, None