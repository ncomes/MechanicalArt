#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to rig Flags
"""

# python imports
import os

# software specific imports
import maya.cmds as cmds
import pymel.all as pm

# Project python imports
from mca.common.project import paths
from mca.common.utils import fileio
from mca.common.textio import yamlio

from mca.mya.utils import naming, attr_utils, dag_utils
from mca.mya.rigging import frag

from mca.common import log
logger = log.MCA_LOGGER

SERIALIZER_VERSION = 1.0

DEFAULT_SHAPE_PATH = 'cube'
DEFAULT_FLAGS_PATH = os.path.join(paths.get_common_tools_path(), 'Flag Shapes')

class Flag(object):
    def __new__(cls, node=None):
        if isinstance(node, Flag):
            logger.debug('already have a flag.')
            return node
        elif isinstance(node, pm.nt.Joint):
            return object.__new__(cls)
        else:
            pass

    def __init__(self, node):
        if isinstance(node, Flag):
            return
        self.pynode = node
        if not self.pynode.hasAttr('is_flag'):
            self.pynode.addAttr('is_flag', at='bool', dv=True)

    # These two class overrides are important as it lets us look up the wrapper in lists or dicts.
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pynode == other.pynode
        return False
    
    def __hash__(self):
        return hash(self.pynode)

    @classmethod
    def create(cls, name=None, alignment_node=None, scale=None, align_transform=True, flag_path=None):
        scale = scale or 1.0
        cmds.select(None)

        flag_name = name or f'f_{naming.get_basename(alignment_node)}' if alignment_node else 'f_new_flag'
        if not flag_name.startswith('f_'):
            flag_name = f'f_{flag_name}'

        new_flag_joint = pm.joint(n=flag_name)
        new_flag_joint.v.set(keyable=False, channelBox=False)
        new_flag_joint.radius.set(keyable=False, channelBox=False)
        flag_node = cls(new_flag_joint)

        flag_path = flag_path or DEFAULT_SHAPE_PATH
        if flag_path:
            flag_node.swap_shape(flag_path, scale)
        else:
            shape_name = f'{flag_name}Shape'
            shape_node = pm.curve(n=shape_name, d=1, p=(
                (7, 7, 7), (7, 7, -7), (7, -7, -7), (7, -7, 7), (7, 7, 7), (-7, 7, 7), (-7, 7, -7), (7, 7, -7),
                (7, -7, -7), (-7, -7, -7), (-7, -7, 7), (7, -7, 7), (7, 7, 7), (-7, 7, 7), (-7, -7, 7), (-7, -7, -7),
                (-7, 7, -7)), k=(0, 1, 2, 3, 4, 5, 6, 7, 7, 9, 10, 11, 12, 13, 14, 15, 16))
            shape_node.scale.set(scale, scale, scale)
            pm.makeIdentity(shape_node, apply=True, t=1, r=1, s=1, n=0)
            dag_utils.parent_shape_node(shape_node, new_flag_joint)
        new_flag_joint.drawStyle.set(2)

        if alignment_node and isinstance(alignment_node, pm.nt.Transform):
            pm.delete(pm.parentConstraint(alignment_node, new_flag_joint))

        pm.makeIdentity(new_flag_joint, apply=True, t=0, r=1, s=0, n=0)

        if align_transform:
            flag_node.add_align_group()
        return flag_node

    @property
    def name(self):
        """
        Returns the absolute flag name.

        :return: Returns the absolute joint name.
        :rtype: str
        """

        return naming.get_basename(self.node)

    @property
    def side(self):
        if self.pynode.hasAttr('flag_side'):
            return self.pynode.getAttr('flag_side')

    @side.setter
    def side(self, val):
        if not self.pynode.hasAttr('flag_side'):
            self.pynode.addAttr('flag_side', dt='string')
        self.pynode.setAttr('flag_side', val)

    @property
    def region(self):
        if self.pynode.hasAttr('flag_region'):
            return self.pynode.getAttr('flag_region')

    @region.setter
    def region(self, val):
        if not self.pynode.hasAttr('flag_region'):
            self.pynode.addAttr('flag_region', dt='string')
        self.pynode.setAttr('flag_region', val)

    @property
    def detail(self):
        if self.pynode.hasAttr('detail'):
            return self.pynode.getAttr('detail')

    @detail.setter
    def detail(self, val):
        if not self.pynode.hasAttr('detail'):
            self.pynode.addAttr('detail', at='bool', dv=val)
        else:
            self.pynode.setAttr('detail', val)

    @property
    def sub(self):
        if self.pynode.hasAttr('sub'):
            return self.pynode.getAttr('sub')

    @sub.setter
    def sub(self, val):
        if not self.pynode.hasAttr('sub'):
            self.pynode.addAttr('sub', at='bool', dv=val)
        else:
            self.pynode.setAttr('sub', val)

    @property
    def contact(self):
        if self.pynode.hasAttr('contact'):
            return self.pynode.getAttr('contact')

    @contact.setter
    def contact(self, val):
        if not self.pynode.hasAttr('contact'):
            self.pynode.addAttr('contact', at='bool', dv=val)
        else:
            self.pynode.setAttr('contact', val)

    @property
    def utility(self):
        if self.pynode.hasAttr('utility'):
            return self.pynode.getAttr('utility')

    @utility.setter
    def utility(self, val):
        if not self.pynode.hasAttr('utility'):
            self.pynode.addAttr('utility', at='bool', dv=val)
        else:
            self.pynode.setAttr('utility', val)

    @property
    def align_group(self):
        if self.pynode.hasAttr('align_group'):
            return self.pynode.getAttr('align_group')

    def add_align_group(self):
        align_group = self.align_group
        if not self.align_group:
            align_group = dag_utils.create_aligned_parent_group(self.pynode, 'align')

        if self.pynode.getParent() != align_group:
            pm.delete(pm.parentConstraint(self.pynode, align_group))
            self.pynode.setParent(align_group)
        return align_group
    
    @property
    def frag_parent(self):
        if self.pynode.hasAttr('fragParent'):
            return frag.FRAGNode(self.pynode.getAttr('fragParent'))

    def swap_shape(self, flag_path, scale=None, rot_offset=None):
        """
        Swaps the default flags for rig specific flags.

        :param str flag_path: Path to where the flags live.
        :param float scale: If the flag shape should be scaled on import.
        :parm list[float, float, float] rot_offset: If the new shape should be rotated relatively before being attached.
        """
        flag_node = self.pynode
        new_curve = import_flag(flag_path)
        if new_curve:
            pm.delete(pm.parentConstraint(flag_node, new_curve, w=True, mo=False))
            if scale:
                new_curve.s.set(3*[scale])
                pm.makeIdentity(new_curve, apply=True, s=True)
            if rot_offset:
                pm.rotate(new_curve, rot_offset, r=True, os=True, fo=True)
            dag_utils.parent_shape_node(new_curve, flag_node, maintain_offset=True)

    def set_attr_state(self, locked=True, attr_list=None, visibility=True):
        attr_utils.set_attr_state(self.pynode, locked, attr_list, visibility)


def is_flag(node):
    if isinstance(node, Flag):
        return node

    if isinstance(node, pm.nt.Transform) and node.hasAttr('is_flag') and node.getAttr('is_flag'):
        return Flag(node)
    return None


def serialize_flag(transform_node):
    """
    Serializes given transform node and returns a dictionary with all the data necessary to recreate that flag.

    :param pm.Transform transform_node: node that represents a transform node with shapes.
    :return: serialized transform curves.
    :rtype: dict
    """

    data = {}
    shapes = transform_node.getShapes()
    for found_shape in shapes:
        if found_shape.isIntermediateObject():
            continue
        if not isinstance(found_shape, pm.nt.NurbsCurve):
            logger.error('{found_shape} is not a NurbsCurve.')
            continue
        curve_data = dag_utils.get_curve_data(found_shape)
        data[naming.get_basename(found_shape)] = curve_data

    return data


def export_flag(flag_path, transform_node):
    """
    Serializes given transform node and saves it to the given path.

    :param Transform transform_node: node that represents a transform node with shapes.
    :param str flag_path: path to save the serialized flag.
    """
    if isinstance(transform_node, Flag):
        transform_node = transform_node.pynode

    if not isinstance(transform_node.getShape(), pm.nt.NurbsCurve):
        return

    # Duplicate the flag we want to export
    flag_to_export = pm.duplicate(transform_node)[0]
    attr_utils.set_attr_state(flag_to_export, False)
    flag_to_export.setParent(None)

    # Zero all flag values.
    flag_to_export.r.set(0, 0, 0)
    flag_to_export.t.set(0, 0, 0)
    flag_to_export.s.set(1, 1, 1)
    if flag_to_export.hasAttr('jointOrient'):
        flag_to_export.jointOrient.set(0, 0, 0)

    # Serialize the flag
    flag_data = serialize_flag(flag_to_export)
    pm.delete(flag_to_export)
    if not flag_data:
        return

    data_dict = {'version': SERIALIZER_VERSION,
                 'curve_data': flag_data}

    # Save the flag data
    fileio.touch_path(flag_path)
    yamlio.write_yaml(flag_path, data_dict)


def deserialize_flag(flag_data):
    """
    Deserializes given flag data and creates a new shaped transform for it.

    :param dict flag_data: flag data serialized using serialize_flag function.
    :return: newly created transform.
    :rtype: Transform or None
    """

    current_shape = 0
    new_curve = None
    for shape_name, curve_data in iter(flag_data.items()):
        cvs = [x[:3] for x in curve_data['cvs']] # $HACK Sometimes this saves with 4 length distance lists?
        knots = curve_data['knots']
        degree = curve_data['degree']
        form = curve_data['form']
        periodic = True if form == 3 else False
        #logger.debug([shape_name, cvs, knots, degree, form, periodic])

        if not new_curve:
            new_curve = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic, append=False)

        child_curve = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic)
        dag_utils.parent_shape_node(child_curve, new_curve, maintain_offset=True, replace=False)

        current_shape += 1

    if not new_curve:
        logger.warning('Was not possible to deserialize flag')
        return

    return new_curve

def import_flag(flag_path):
    """
    Given a flag path, read and build a new transform with a shape from the data.

    :param str flag_path: Path to the serialized flag.
    :rtype: Transform or None
    :return: The newly built flag shape.
    """

    if not os.path.exists(flag_path):
        basic_flag_path = os.path.join(DEFAULT_FLAGS_PATH, f'{flag_path}.flag')
        if os.path.exists(basic_flag_path):
            flag_path = basic_flag_path
        else:
            return
    flag_data = yamlio.read_yaml(flag_path) or {}
    return deserialize_flag(flag_data.get('curve_data', {}))


def swap_flags(flags, flag_path):
    """
    Swaps the default flags for rig specific flags.

    :param list(flag.FLAG) flags: Animation controls.
    :param str flag_path: Path to where the flags live.
    """

    for found_flag in flags:
        flag_name = found_flag.nodeName(stripNamespace=True)
        this_flag_path = os.path.join(flag_path, f'{flag_name}.flag')
        if os.path.exists(this_flag_path):
            new_curve = import_flag(this_flag_path)
            if new_curve:
                pm.delete(pm.parentConstraint(found_flag, new_curve, w=True, mo=False))
                dag_utils.parent_shape_node(new_curve, found_flag, maintain_offset=True, freeze_transform=True)
        else:
            logger.warning(f'Flag with name "{flag_name}" does not exist in following paths:\n\t{this_flag_path}')





