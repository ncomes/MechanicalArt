#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that centralizes May attribute types
"""
# System global imports
# software specific imports
import maya.api.OpenMaya as OpenMaya
# mca python imports


kMFnNumericBoolean = 0
kMFnNumericShort = 1
kMFnNumericInt = 2
kMFnNumericLong = 3
kMFnNumericByte = 4
kMFnNumericFloat = 5
kMFnNumericDouble = 6
kMFnNumericAddr = 7
kMFnNumericChar = 8
kMFnUnitAttributeDistance = 9
kMFnUnitAttributeAngle = 10
kMFnUnitAttributeTime = 11
kMFnkEnumAttribute = 12
kMFnDataString = 13
kMFnDataMatrix = 14
kMFnDataFloatArray = 15
kMFnDataDoubleArray = 16
kMFnDataIntArray = 17
kMFnDataPointArray = 18
kMFnDataVectorArray = 19
kMFnDataStringArray = 20
kMFnDataMatrixArray = 21
kMFnCompoundAttribute = 22
kMFnNumericInt64 = 23
kMFnNumericLast = 24
kMFnNumeric2Double = 25
kMFnNumeric2Float = 26
kMFnNumeric2Int = 27
kMFnNumeric2Long = 28
kMFnNumeric2Short = 29
kMFnNumeric3Double = 30
kMFnNumeric3Float = 31
kMFnNumeric3Int = 32
kMFnNumeric3Long = 33
kMFnNumeric3Short = 34
kMFnNumeric4Double = 35
kMFnMessageAttribute = 36

MAYA_NUMERIC_MULTI_TYPES = (OpenMaya.MFnNumericData.k2Double, OpenMaya.MFnNumericData.k2Float,
                            OpenMaya.MFnNumericData.k2Int, OpenMaya.MFnNumericData.k2Long,
                            OpenMaya.MFnNumericData.k2Short,  OpenMaya.MFnNumericData.k3Double,
                            OpenMaya.MFnNumericData.k3Float,  OpenMaya.MFnNumericData.k3Int,
                            OpenMaya.MFnNumericData.k3Long, OpenMaya.MFnNumericData.k3Short,
                            OpenMaya.MFnNumericData.k4Double)

_MAYA_TYPE_FROM_TYPE = dict(
    kMFnNumericBoolean=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kBoolean),
    kMFnNumericByte=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kByte),
    kMFnNumericShort=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kShort),
    kMFnNumericInt=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kInt),
    kMFnNumericLong=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kLong),
    kMFnNumericDouble=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kDouble),
    kMFnNumericFloat=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kFloat),
    kMFnNumericAddr=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kAddr),
    kMFnNumericChar=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.kChar),
    kMFnNumeric2Double=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k2Double),
    kMFnNumeric2Float=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k2Float),
    kMFnNumeric2Int=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k2Int),
    kMFnNumeric2Long=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k2Long),
    kMFnNumeric2Short=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k2Short),
    kMFnNumeric3Double=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k3Double),
    kMFnNumeric3Float=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k3Float),
    kMFnNumeric3Int=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k3Int),
    kMFnNumeric3Long=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k3Long),
    kMFnNumeric3Short=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k3Short),
    kMFnNumeric4Double=(OpenMaya.MFnNumericAttribute, OpenMaya.MFnNumericData.k4Double),
    kMFnUnitAttributeDistance=(OpenMaya.MFnUnitAttribute, OpenMaya.MFnUnitAttribute.kDistance),
    kMFnUnitAttributeAngle=(OpenMaya.MFnUnitAttribute, OpenMaya.MFnUnitAttribute.kAngle),
    kMFnUnitAttributeTime=(OpenMaya.MFnUnitAttribute, OpenMaya.MFnUnitAttribute.kTime),
    kMFnkEnumAttribute=(OpenMaya.MFnEnumAttribute, OpenMaya.MFn.kEnumAttribute),
    kMFnDataString=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kString),
    kMFnDataMatrix=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kMatrix),
    kMFnDataFloatArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kFloatArray),
    kMFnDataDoubleArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kDoubleArray),
    kMFnDataIntArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kIntArray),
    kMFnDataPointArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kPointArray),
    kMFnDataVectorArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kVectorArray),
    kMFnDataStringArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kStringArray),
    kMFnDataMatrixArray=(OpenMaya.MFnTypedAttribute, OpenMaya.MFnData.kMatrixArray),
    kMFnMessageAttribute=(OpenMaya.MFnMessageAttribute, OpenMaya.MFn.kMessageAttribute)
)

_TYPE_TO_STRING = {
    kMFnNumericBoolean: 'kMFnNumericBoolean',
    kMFnNumericByte: 'kMFnNumericByte',
    kMFnNumericShort: 'kMFnNumericShort',
    kMFnNumericInt: 'kMFnNumericInt',
    kMFnNumericLong: 'kMFnNumericLong',
    kMFnNumericDouble: 'kMFnNumericDouble',
    kMFnNumericFloat: 'kMFnNumericFloat',
    kMFnNumericAddr: 'kMFnNumericAddr',
    kMFnNumericChar: 'kMFnNumericChar',
    kMFnNumeric2Double: 'kMFnNumeric2Double',
    kMFnNumeric2Float: 'kMFnNumeric2Float',
    kMFnNumeric2Int: 'kMFnNumeric2Int',
    kMFnNumeric2Long: 'kMFnNumeric2Long',
    kMFnNumeric2Short: 'kMFnNumeric2Short',
    kMFnNumeric3Double: 'kMFnNumeric3Double',
    kMFnNumeric3Float: 'kMFnNumeric3Float',
    kMFnNumeric3Int: 'kMFnNumeric3Int',
    kMFnNumeric3Long: 'kMFnNumeric3Long',
    kMFnNumeric3Short: 'kMFnNumeric3Short',
    kMFnNumeric4Double: 'kMFnNumeric4Double',
    kMFnUnitAttributeDistance: 'kMFnUnitAttributeDistance',
    kMFnUnitAttributeAngle: 'kMFnUnitAttributeAngle',
    kMFnUnitAttributeTime: 'kMFnUnitAttributeTime',
    kMFnkEnumAttribute: 'kMFnkEnumAttribute',
    kMFnDataString: 'kMFnDataString',
    kMFnDataMatrix: 'kMFnDataMatrix',
    kMFnDataFloatArray: 'kMFnDataFloatArray',
    kMFnDataDoubleArray: 'kMFnDataDoubleArray',
    kMFnDataIntArray: 'kMFnDataIntArray',
    kMFnDataPointArray: 'kMFnDataPointArray',
    kMFnDataVectorArray: 'kMFnDataVectorArray',
    kMFnDataStringArray: 'kMFnDataStringArray',
    kMFnDataMatrixArray: 'kMFnDataMatrixArray',
    kMFnMessageAttribute: 'kMFnMessageAttribute',
    kMFnCompoundAttribute: 'kMFnCompoundAttribute'
}

_PM_TYPE_TO_TYPE = {
    'bool': kMFnNumericBoolean,
    'short': kMFnNumericShort,
    'long': kMFnNumericLong,
    'byte': kMFnNumericByte,
    'float': kMFnNumericFloat,
    'double': kMFnNumericDouble,
    'char': kMFnNumericChar,
    'angle': kMFnUnitAttributeAngle,
    'time': kMFnUnitAttributeTime,
    'enum': kMFnkEnumAttribute,
    'string': kMFnDataString,
    'matrix': kMFnDataMatrix,
    'fltMatrix': kMFnDataFloatArray,
    'compound': kMFnCompoundAttribute,
    'short2': kMFnNumeric2Short,
    'short3': kMFnNumeric3Short,
    'long2': kMFnNumeric2Long,
    'long3': kMFnNumeric3Long,
    'float2': kMFnNumeric2Float,
    'float3': kMFnNumeric3Float,
    'double2': kMFnNumeric2Double,
    'double3': kMFnNumeric3Double,
    'message': kMFnMessageAttribute,
}

_MAYA_NUMERIC_TYPE_TO_INTERNAL_TYPE = {
    OpenMaya.MFnNumericData.kBoolean: kMFnNumericBoolean,
    OpenMaya.MFnNumericData.kByte: kMFnNumericByte,
    OpenMaya.MFnNumericData.kShort: kMFnNumericShort,
    OpenMaya.MFnNumericData.kInt: kMFnNumericInt,
    OpenMaya.MFnNumericData.kLong: kMFnNumericLong,
    OpenMaya.MFnNumericData.kDouble: kMFnNumericDouble,
    OpenMaya.MFnNumericData.kFloat: kMFnNumericFloat,
    OpenMaya.MFnNumericData.kAddr: kMFnNumericAddr,
    OpenMaya.MFnNumericData.kChar: kMFnNumericChar,
    OpenMaya.MFnNumericData.k2Double: kMFnNumeric2Double,
    OpenMaya.MFnNumericData.k2Float: kMFnNumeric2Float,
    OpenMaya.MFnNumericData.k2Int: kMFnNumeric2Int,
    OpenMaya.MFnNumericData.k2Long: kMFnNumeric2Long,
    OpenMaya.MFnNumericData.k2Short: kMFnNumeric2Short,
    OpenMaya.MFnNumericData.k3Double: kMFnNumeric3Double,
    OpenMaya.MFnNumericData.k3Float: kMFnNumeric3Float,
    OpenMaya.MFnNumericData.k3Int: kMFnNumeric3Int,
    OpenMaya.MFnNumericData.k3Long: kMFnNumeric3Long,
    OpenMaya.MFnNumericData.k3Short: kMFnNumeric3Short,
    OpenMaya.MFnNumericData.k4Double: kMFnNumeric4Double,
}

_MAYA_UNIT_TYPE_TO_INTERNAL_TYPE = {
    OpenMaya.MFnUnitAttribute.kDistance: kMFnUnitAttributeDistance,
    OpenMaya.MFnUnitAttribute.kAngle: kMFnUnitAttributeAngle,
    OpenMaya.MFnUnitAttribute.kTime: kMFnUnitAttributeTime
}

_MAYA_MFNDATA_TYPE_TO_INTERNAL_TYPE = {
    OpenMaya.MFnData.kString: kMFnDataString,
    OpenMaya.MFnData.kMatrix: kMFnDataMatrix,
    OpenMaya.MFnData.kFloatArray: kMFnDataFloatArray,
    OpenMaya.MFnData.kDoubleArray: kMFnDataDoubleArray,
    OpenMaya.MFnData.kIntArray: kMFnDataIntArray,
    OpenMaya.MFnData.kPointArray: kMFnDataPointArray,
    OpenMaya.MFnData.kVectorArray: kMFnDataVectorArray,
    OpenMaya.MFnData.kStringArray: kMFnDataStringArray,
    OpenMaya.MFnData.kMatrixArray: kMFnDataMatrixArray
}

_OM_TYPE_TO_PM_TYPE = {
    kMFnNumericBoolean: 'bool',
    kMFnNumericShort: 'short',
    kMFnNumericLong: 'long',
    kMFnNumericByte: 'byte',
    kMFnNumericFloat: 'float',
    kMFnNumericDouble: 'double',
    kMFnNumericChar: 'char',
    kMFnUnitAttributeAngle: 'angle',
    kMFnUnitAttributeTime: 'time',
    kMFnkEnumAttribute: 'enum',
    kMFnDataString: 'string',
    kMFnDataMatrix: 'matrix',
    kMFnDataFloatArray: 'fltMatrix',
    kMFnCompoundAttribute: 'compound',
    kMFnNumeric2Short: 'short2',
    kMFnNumeric3Short: 'short3',
    kMFnNumeric2Long: 'long2',
    kMFnNumeric3Long: 'long3',
    kMFnNumeric2Float: 'float2',
    kMFnNumeric3Float: 'float3',
    kMFnNumeric2Double: 'double2',
    kMFnNumeric3Double: 'double3',
    kMFnMessageAttribute: 'message'
}


def api_type_to_string(api_attribute_type):
    """
    Coverts given integer Maya OpenMaya API attribute type as a string.

    :param int api_attribute_type: Maya OpenMaya API attribute type as an integer value.
    :return: Maya Openmaya API attribute type as a string.
    :rtype: str
    """

    return _TYPE_TO_STRING.get(api_attribute_type)


def maya_type_from_api_type(api_type):
    """
    Returns mya.cmds API type from the given Maya OpenMaya API type.
    :param int api_type: Maya OpenMaya API attribute type as an integer value.
    :return: mya.cmds API type.
    :rtype: str
    """

    type_conversion = _MAYA_TYPE_FROM_TYPE.get(api_type)
    if not type_conversion:
        return None, None

    return type_conversion


def api_type_from_pymel_type(pymel_type):
    """
    Returns OpenMaya API type from PyMEL type.

    :param str pymel_type: PyMEL attribute type.
    :return: OpenMaya type.
    :rtype: int
    """

    type_conversion = _PM_TYPE_TO_TYPE.get(pymel_type, None)

    return type_conversion


def maya_numeric_type_to_internal_type(numeric_type):
    """
    Returns the MCA internal attribute type for the given Maya numeric type.

    :param OpenMaya.MFnNumericData numeric_type: Maya numeric attribute type.
    :return: internal attribute type.
    :rtype: int
    """

    return _MAYA_NUMERIC_TYPE_TO_INTERNAL_TYPE.get(numeric_type)


def maya_unit_type_to_internal_type(typed_type):
    """
    Returns the MCA internal attribute type for the given Maya typed type.

    :param OpenMaya.MFnUnitAttribute typed_type: Maya typed attribute type.
    :return: internal attribute type.
    :rtype: int
    """

    return _MAYA_TYPE_FROM_TYPE.get(typed_type)


def maya_mfn_data_type_to_internal_type(data_type):
    """
    Returns the MCA internal attribute type for the given Maya data type.

    :param OpenMaya.MFnData data_type: Maya data attribute type.
    :return: internal attribute type.
    :rtype: int
    """

    return _MAYA_MFNDATA_TYPE_TO_INTERNAL_TYPE.get(data_type)


def maya_type_to_python_type(maya_type):
    """
    Returns the Python type for the given Maya type.

    :param object maya_type: Maya attribute type.
    :return: Python type.
    :rtype: int, float, string, list
    """

    if isinstance(maya_type, (OpenMaya.MDistance, OpenMaya.MTime, OpenMaya.MAngle)):
        return maya_type.value
    elif isinstance(maya_type, (OpenMaya.MMatrix, OpenMaya.MVector, OpenMaya.MPoint, OpenMaya.MQuaternion,
                                OpenMaya.MEulerRotation)):
        return list(maya_type)

    return maya_type


def om_type_to_pymel_type(om_type):
    """
    Returns PyMEL type from given OpenMaya type.

    :param int om_type: OpenMaya attribute type.
    :return: PyMEL type.
    :rtype: str
    """

    type_conversion = _OM_TYPE_TO_PM_TYPE.get(om_type, None)

    return type_conversion
