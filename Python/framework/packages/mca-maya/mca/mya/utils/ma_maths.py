#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with PyMEL API math
"""

# System global imports
import math
# software specific imports
import pymel.core as pm
#  python imports
from mca.common.utils import pymaths


X_AXIS_VECTOR = pm.dt.Vector(1, 0, 0)
Y_AXIS_VECTOR = pm.dt.Vector(0, 1, 0)
Z_AXIS_VECTOR = pm.dt.Vector(0, 0, 1)


def magnitude(vector=(0, 0, 0)):
    """
    Returns the magnitude (length) or a given vector.

    :param tuple(float, float, float) vector: vector to return the length of.
    :return: vector magnitude.
    :rtype: float
    """

    return pm.dt.Vector(vector[0], vector[1], vector[2]).length()


def offset_vector(point1, point2):
    """
    Returns the offset vector between point1 and point2.

    :param tuple(float, float, float) point1: start point of the offset calculation.
    :param tuple(float, float, float) point2: end point of the offset calculation.
    :return: offset vector as a tuple.
    :rtype: tuple(float, float, float)
    """

    pnt1 = pm.dt.Vector(point1[0], point1[1], point1[2])
    pnt2 = pm.dt.Vector(point2[0], point2[1], point2[2])
    vec = pnt2 - pnt1

    return vec.x, vec.y, vec.z


def distance_between_nodes(source_node=None, target_node=None):
    """
    Returns the distance between 2 given nodes.

    :param str source_node: first node to start measuring distance from. If not given, first selected node will be used.
    :param str target_node: second node to end measuring distance to. If not given, second selected node will be used.
    :return: distance between 2 nodes.
    :rtype: float
    """

    if source_node is None or target_node is None:
        sel = pm.ls(sl=True, type='transform')
        if len(sel) != 2:
            return 0
        source_node, target_node = sel

    source_pos = pm.dt.Point(*pm.xform(source_node, query=True, worldSpace=True, translation=True))
    target_pos = pm.dt.Point(*pm.xform(target_node, query=True, worldSpace=True, translation=True))

    return source_pos.distanceTo(target_pos)


def direction_vector_between_nodes(source_node=None, target_node=None):
    """
    Returns the direction vector between 2 given nodes
    :param str source_node: first node to start getting direction. If not given, first selected node will be used.
    :param str target_node: second node to end getting direction. If not given, second selected node will be used.
    :return: direction vector between 2 nodes.
    :rtype: pm.datatypes.Vector
    """

    if source_node is None or target_node is None:
        sel = pm.ls(sl=True, type='transform')
        if len(sel) != 2:
            return 0
        source_node, target_node = sel

    source_pos = pm.dt.Point(*pm.xform(source_node, query=True, worldSpace=True, translation=True))
    target_pos = pm.dt.Point(*pm.xform(target_node, query=True, worldSpace=True, translation=True))

    return target_pos - source_pos


def get_identity_matrix():
    """
    Returns identity matrix.

    :return: pm.datatypes.Matrix
    """

    return pm.dt.Matrix()


def multiply_matrix(matrix4x4_list1, matrix4x4_list2):
    """
    Multiplies the two given matrices.

    matrix1 and matrix2 are just the list of numbers of a 4x4 matrix
    (like the ones returned by cmds.getAttr('transform.worldMatrix) for example.

    :param matrix4x4_list1:
    :param matrix4x4_list2:
    :return: pm.datatypes.Matrix
    """

    mat1 = pm.dt.Matrix(matrix4x4_list1)
    mat2 = pm.dt.Matrix(matrix4x4_list2)

    return mat1 * mat2


def to_euler_xyz(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with XYZ rotation order.

    :param OpenMaya.MMatrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_z = rotation_matrix[2]
    if pymaths.is_equal(rotation_z, 1.0, 2):
        z = math.pi
        y = -math.pi * 0.5
        x = -z + math.atan2(-rotation_matrix[4], -rotation_matrix[7])
    elif pymaths.is_equal(rotation_z, -1.0, 2):
        z = math.pi
        y = math.pi * 0.5
        x = z + math.atan2(rotation_matrix[4], rotation_matrix[7])
    else:
        y = -math.asin(rotation_z)
        cos_y = math.cos(y)
        x = math.atan2(rotation_matrix[6] * cos_y, rotation_matrix[10] * cos_y)
        z = math.atan2(rotation_matrix[1] * cos_y, rotation_matrix[0] * cos_y)
    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler_xzy(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with XZY rotation order.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_yy = rotation_matrix[1]
    z = math.asin(rotation_yy)
    cos_z = math.cos(z)

    x = math.atan2(-rotation_matrix[9] * cos_z, rotation_matrix[5] * cos_z)
    y = math.atan2(-rotation_matrix[2] * cos_z, rotation_matrix[0] * cos_z)

    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler_yxz(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with YXZ rotation order.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_z = rotation_matrix[6]
    x = math.asin(rotation_z)
    cos_x = math.cos(x)

    y = math.atan2(-rotation_matrix[2] * cos_x, rotation_matrix[10] * cos_x)
    z = math.atan2(-rotation_matrix[4] * cos_x, rotation_matrix[5] * cos_x)

    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler_yzx(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with YZX rotation order.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_yx = rotation_matrix[4]
    z = -math.asin(rotation_yx)
    cos_z = math.cos(z)

    x = math.atan2(rotation_matrix[6] * cos_z, rotation_matrix[5] * cos_z)
    y = math.atan2(rotation_matrix[8] * cos_z, rotation_matrix[0] * cos_z)

    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler_zxy(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with ZXY rotation order.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_zy = rotation_matrix[9]
    x = -math.asin(rotation_zy)
    cos_x = math.cos(x)

    z = math.atan2(rotation_matrix[1] * cos_x, rotation_matrix[5] * cos_x)
    y = math.atan2(rotation_matrix[8] * cos_x, rotation_matrix[10] * cos_x)

    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler_zyx(rotation_matrix, degrees=False):
    """
    Converts given rotation matrix to a rotation with ZYX rotation order.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    rotation_zx = rotation_matrix[8]
    y = math.asin(rotation_zx)
    cos_y = math.cos(y)

    x = math.atan2(-rotation_matrix[9] * cos_y, rotation_matrix[10] * cos_y)
    z = math.atan2(-rotation_matrix[4] * cos_y, rotation_matrix[0] * cos_y)

    angles = x, y, z

    if degrees:
        return list(map(math.degrees, angles))

    return pm.dt.EulerRotation(angles)


def to_euler(rotation_matrix, rotate_order, degrees=False):
    """
    Converts given rotation matrix to an euler rotation.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to convert.
    :param str rotate_order: rotation order.
    :param bool degrees: whether to convert result in degrees or radians.
    :return: euler rotation.
    :rtype: pm.datatypes.EulerRotation
    """

    if rotate_order == pm.dt.TransformationMatrix.kXYZ:
        return to_euler_xyz(rotation_matrix, degrees)
    elif rotate_order == pm.dt.TransformationMatrix.kXZY:
        return to_euler_xzy(rotation_matrix, degrees)
    elif rotate_order == pm.dt.TransformationMatrix.kYXZ:
        return to_euler_yxz(rotation_matrix, degrees)
    elif rotate_order == pm.dt.TransformationMatrix.kYZX:
        return to_euler_yzx(rotation_matrix, degrees)
    elif rotate_order == pm.dt.TransformationMatrix.kZXY:
        return to_euler_zxy(rotation_matrix, degrees)

    return to_euler_zyx(rotation_matrix, degrees)


def mirror_xy(rotation_matrix):
    """
    Mirrors given rotation matrix along XY plane.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to mirror.
    :return: mirrored rotation matrix.
    :rtype: pm.datatypes.Matrix
    """

    rotation_matrix = pm.dt.Matrix(rotation_matrix)
    rotation_matrix[0] *= -1
    rotation_matrix[1] *= -1
    rotation_matrix[4] *= -1
    rotation_matrix[5] *= -1
    rotation_matrix[8] *= -1
    rotation_matrix[9] *= -1

    return rotation_matrix


def mirror_yz(rotation_matrix):
    """
    Mirrors given rotation matrix along YZ plane.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to mirror.
    :return: mirrored rotation matrix.
    :rtype: pm.datatypes.MMatrix
    """

    rotation_matrix = pm.dt.Matrix(rotation_matrix)
    rotation_matrix[1] *= -1
    rotation_matrix[2] *= -1
    rotation_matrix[5] *= -1
    rotation_matrix[6] *= -1
    rotation_matrix[9] *= -1
    rotation_matrix[10] *= -1

    return rotation_matrix


def mirror_xz(rotation_matrix):
    """
    Mirrors given rotation matrix along XZ plane.

    :param pm.datatypes.Matrix rotation_matrix: rotation matrix to mirror.
    :return: mirrored rotation matrix.
    :rtype: pm.datatypes.Matrix
    """

    rotation_matrix = pm.dt.Matrix(rotation_matrix)
    rotation_matrix[0] *= -1
    rotation_matrix[2] *= -1
    rotation_matrix[4] *= -1
    rotation_matrix[6] *= -1
    rotation_matrix[8] *= -1
    rotation_matrix[10] *= -1

    return rotation_matrix


def quaternion_dot(qa, qb):
    """
    Calculates the dot product based on given quaternions.

    :param pm.datatypes.Quaternion qa: quaternion to calculate dot product with.
    :param pm.datatypes.Quaternion qb: quaternion to calculate dot product with.
    :return: quaternion dot product.
    :rtype: float
    """

    return qa.w * qb.w + qa.x * qb.x + qa.y * qb.y + qa.z * qb.z


def slerp(qa, qb, weight):
    """
    Calculates the spherical interpolation  between two given quaternions.

    :param pm.datatypes.Quaternion qa: quaternion to calculate spherical interpolation with.
    :param pm.datatypes.Quaternion qb: quaternion to calculate spherical interpolation with.
    :param float weight: how far we want to interpolate.
    :return: result of the spherical interpolation.
    :rtype: pm.datatypes.MQuaternion
    """

    qc = pm.dt.Quaternion()
    dot = quaternion_dot(qa, qb)
    if abs(dot >= 1.0):
        qc.w = qa.w
        qc.x = qa.x
        qc.y = qa.y
        qc.z = qa.z
        return qc

    half_theta = math.acos(dot)
    sin_half_theta = math.sqrt(1.0 - dot * dot)
    if pymaths.is_equal(math.fabs(sin_half_theta), 0.0, 2):
        qc.w = (qa.w * 0.5 + qb.w * 0.5)
        qc.x = (qa.x * 0.5 + qb.x * 0.5)
        qc.y = (qa.y * 0.5 + qb.y * 0.5)
        qc.z = (qa.z * 0.5 + qb.z * 0.5)
        return qc

    ratio_a = math.sin((1.0 - weight) * half_theta) / sin_half_theta
    ratio_b = math.sin(weight * half_theta) / sin_half_theta

    qc.w = (qa.w * ratio_a + qb.w * ratio_b)
    qc.x = (qa.x * ratio_a + qb.x * ratio_b)
    qc.y = (qa.y * ratio_a + qb.y * ratio_b)
    qc.z = (qa.z * ratio_a + qb.z * ratio_b)

    return qc


def look_at(source_position, aim_position, aim_vector=None, up_vector=None, world_up_vector=None, constrain_axis=None):
    """
    Aims one node to another node using quaternions.

    :param pm.dt.Vector source_position: source position which acts as the eye.
    :param pm.dt.Vector aim_position: target position to aim at.
    :param pm.dt.Vector aim_vector: aim vector.
    :param pm.dt.Vector up_vector: up vector.
    :param pm.dt.Vector world_up_vector: optional world up vector.
    :param pm.dt.Vector constrain_axis: axis vector to constraint the aim on. For example (0, 1, 1) will set X
        rotation to 0.0.
    :return: quaternion that encapsulates the aim orientation.
    :rtype: pm.dt.Quaternion
    """

    constrain_axis = constrain_axis or pm.dt.Vector(1, 1, 1)

    if aim_vector is not None and isinstance(aim_vector, (list, tuple)):
        aim_vector = pm.dt.Vector(*aim_vector)
    if up_vector is not None and isinstance(up_vector, (list, tuple)):
        up_vector = pm.dt.Vector(*up_vector)
    if world_up_vector is not None and isinstance(world_up_vector, (list, tuple)):
        world_up_vector = pm.dt.Vector(*world_up_vector)
    if constrain_axis is not None and isinstance(constrain_axis, (list, tuple)):
        constrain_axis = pm.dt.Vector(*constrain_axis)

    eye_aim = aim_vector or X_AXIS_VECTOR
    eye_up = up_vector or Y_AXIS_VECTOR
    up_axis_str = pm.upAxis(query=True, axis=True).lower()
    world_up = world_up_vector or pm.dt.Vector(0, 1, 0) if up_axis_str == 'y' else pm.dt.Vector(0, 0, 1)
    eye_pivot_pos = source_position
    target_pivot_pos = aim_position

    aim_vector = target_pivot_pos - eye_pivot_pos
    eye_u = aim_vector.normal()
    eye_w = (eye_u ^ pm.dt.Vector(world_up.x, world_up.y, world_up.z)).normal()
    eye_v = eye_w ^ eye_u
    quat_u = pm.dt.Quaternion(eye_aim, eye_u)
    up_rotated = eye_up.rotateBy(quat_u)
    try:
        angle = math.acos(up_rotated * eye_v)
    except (ZeroDivisionError, ValueError):
        angle = 0.0 if sum(eye_up) > 0 else -math.pi

    quat_v = pm.dt.Quaternion(angle, eye_u)
    if not eye_v.isEquivalent(up_rotated.rotateBy(quat_v), 1.0e-5):
        angle = (2 * math.pi) - angle
        quat_v = pm.dt.Quaternion(angle, eye_u)

    quat_u *= quat_v
    rot = quat_u.asEulerRotation()
    if not constrain_axis.x:
        rot.x = 0.0
    if not constrain_axis.y:
        rot.y = 0.0
    if not constrain_axis.z:
        rot.z = 0.0

    return rot.asQuaternion()


def even_linear_point_distribution(start, end, count):
    """
    Generator function which evenly distributes points along a straight line.

    :param pm.dt.Vector start: start vector.
    :param pm.dt.Vector end: end vector.
    :param int count: number of points to distribute.
    :return: distributed vector with the position and their distribution value.
    :rtype: tuple(pm.dt.Vector, int)
    """

    direction_vector = end - start
    fraction = direction_vector.normal().length() / (count + 1)
    for n in range(1, count + 1):
        multiplier = fraction * n
        pos = start + (direction_vector * multiplier)
        yield pos, multiplier


def first_last_offset_linear_point_distribution(start, end, count, offset):
    """
    Generator function which evenly distributes points along a straight line but taking into account the given offset.

    :param pm.dt.Vector start: start vector.
    :param pm.dt.Vector end: end vector.
    :param int count: number of points to distribute.
    :param int offset: the value to offset the first and last points, which is calculated from
        the fraction(direction*(fraction*offset).
    :return: distributed vector with the position and their distribution value.
    :rtype: tuple(pm.dt.Vector, int)
    """

    direction_vector = end - start
    length = direction_vector.normal().length()
    first_last_fraction = length / (count + 1)
    primary_fraction = length / (count - 1)
    multiplier = first_last_fraction * offset
    yield start + (direction_vector * multiplier), multiplier

    for n in range(count - 2):
        multiplier = primary_fraction * (n + 1)
        pos = start + (direction_vector * multiplier)
        yield pos, multiplier

    multiplier = 1.0 - first_last_fraction * offset
    yield start + (direction_vector * multiplier), multiplier
