#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Maya Geometry
"""

# System global imports

# software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.utils import namespace_utils, naming


def make_pins(joint_list, size_multiplier, data_dict, delete_joint_list=True, merge_pins=False):
    """
    Creates reference pins

    :param list(pm.nt.Joint) joint_list: List of joints to create pins for
    :param float size_multiplier: Size to multiply base pin size from
    :param dict data_dict: Dictionary containing information of how to handle pins
    :param bool delete_joint_list: If true, delete the joints that pins were created on
    :param bool merge_pins: If true, merge the pins after building
    :return: Created pin(s)
    :rtype: pm.nt.Transform or list(pm.nt.Transform)
    """

    setup_info = data_dict.get('region_rotations')
    ignore_types = data_dict.get('ignore_types')
    created_pins = []
    if not merge_pins:
        namespace_utils.set_namespace('skel_ref')
    for each_joint in joint_list:
        joint_name = naming.get_basename(each_joint)
        found_joint = [x for x in setup_info.keys() if joint_name == x]
        if any(x in joint_name for x in ignore_types):
            continue

        if found_joint:
            rotate_axis, size, obj_shape = setup_info.get(joint_name)
        else:
            rotate_axis = 'rotateZ'
            size = 2
            obj_shape = 'Cylinder'

        dup_bone = pm.duplicate(each_joint, po=True, n=f'skel_ref_{each_joint}')[0]
        pm.setAttr(f'{dup_bone}.{rotate_axis}', 90)
        pin = create_reference_obj(size, size_multiplier, obj_shape, rotate_axis, each_joint)

        pm.delete(pm.parentConstraint(dup_bone, pin, w=True, mo=False))
        pm.delete(dup_bone)

        pin.translate.lock()

        created_pins.append(pin)

    if merge_pins:
        final_pins = pm.polyUnite(created_pins, n=f'skel_ref_pins')[0]
        pm.delete(final_pins, ch=True)
        final_pins.addAttr('ref_pins', at='bool')
    else:
        final_pins = created_pins
        pins_grp = pm.group(final_pins, n='ref_pins_grp')

    if delete_joint_list:
        pm.delete(joint_list)
    namespace_utils.set_namespace('')
    return final_pins


def create_reference_obj(size, size_multiplier, obj_shape, rotate_axis, matched_joint_name):
    """
    Creates a reference object

    :param float/int size: Base size of the object
    :param float/int size_multiplier: Value to increase size by
    :param str obj_shape: Shape of the object (currently only expecting Sphere or Cylinder)
    :param str rotate_axis: Rotate axis to be represented by the object
    :param str matched_joint_name: Name of the joint that object is to match
    """

    pin = eval(f'pm.poly{obj_shape}()[0]')
    pin.rename(f'{matched_joint_name}_ref_pin')

    secondary_scale = size * size_multiplier if obj_shape != 'Cylinder' else 0.15
    pin.scaleX.set(secondary_scale)
    pin.scaleY.set(size * size_multiplier)
    pin.scaleZ.set(secondary_scale)

    # Create and set attrs for pin setup data
    pin.addAttr('matchedJoint', dt='string')
    pin.matchedJoint.set(matched_joint_name)
    pin.addAttr('rotatedAxis', dt='string')
    pin.rotatedAxis.set(rotate_axis)
    pin.addAttr('objShape', dt='string')
    pin.objShape.set(obj_shape)
    pin.addAttr('ref_pin', at='bool')
    pin.addAttr('pinSize', at='double')
    pin.pinSize.set(size)

    return pin


def apply_cube_trick(node):
    """
    Merges then deletes a cube with a given object. This resets some mesh errors.

    :param Transform node: A shaped transform.
    :rtype: Transform
    :return: The resulting transform node of the cleaned mesh.
    """
    node_name = naming.get_basename(node)
    temp_cube = pm.polyCube()[0]
    node_parent = node.getParent()
    if node_parent:
        node.setParent(None)
    combined_node = pm.polyUnite(node, temp_cube, ch=False)[0]
    pm.delete(combined_node.faces[-6:])
    pm.bakePartialHistory(combined_node, all=True)
    if pm.objExists(node):
        pm.delete(node)
    combined_node.rename(node_name)
    if node_parent:
        combined_node.setParent(node_parent)
    return combined_node
