#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Maya Animation Flag functions
"""

# mca python imports
import os

# software specific imports
import pymel.core as pm
# mca python imports
from mca.common import log
from mca.common.textio import yamlio
from mca.common.utils import fileio

from mca.mya.utils import naming, attr_utils, dag
from mca.mya.rigging import joint_utils, rig_utils

logger = log.MCA_LOGGER

SERIALIZER_VERSION = '1.0'
FLAG_TYPES = ['isDetail', 'isSub', 'isContact', 'isUtil']

def is_flag_node(obj_node):
    """
    If a given node is a rig flag node.

    :param obj_node:
    :return: True or False depending on the node's markup
    :rtype: Bool
    """
    if isinstance(obj_node, pm.nt.Transform):
        if obj_node.hasAttr('isFlag') and obj_node.isFlag.get():
            return True
    return False


def transform_scale(align_grp, flag, translate_scale=(1, 1, 1)):
    align_grp.scaleX.set(1.0 / translate_scale[0])
    align_grp.scaleY.set(1.0 / translate_scale[1])
    align_grp.scaleZ.set(1.0 / translate_scale[2])
    flag.scaleX.set(translate_scale[0])
    flag.scaleY.set(translate_scale[1])
    flag.scaleZ.set(translate_scale[2])

    flag.sx.lock()
    flag.sx.set(keyable=False, channelBox=False)
    flag.sy.lock()
    flag.sy.set(keyable=False, channelBox=False)
    flag.sz.lock()
    flag.sz.set(keyable=False, channelBox=False)


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
                dag.parent_shape_node(new_curve, found_flag, maintain_offset=True, freeze_transform=True)
        else:
            logger.warning(f'Flag with name "{flag_name}" does not exist in following paths:\n\t{this_flag_path}')


class Flag:
    def __init__(self, node):
        self.node = pm.PyNode(node)

    @classmethod
    def create(cls, object_to_match,
               shape=None,
               maintain_shape_offset=False,
               label=None,
               point=True,
               orient=True,
               scale=1.0,
               add_align_transform=True,
               orientation=None,
               is_detail=False,
               is_sub=False,
               is_contact=False,
               is_util=False,
               meta_connect=True):

        """
        Creates an animation control.

        :param nt.Transform object_to_match: object we align the flag to.
        :param nt.Transform shape: shape to parent to the flag transform if provided, else is a polyCube.
        :param bool maintain_shape_offset: maintain shape offset
        :param str label: object label, if label is not input, construct the flag label from the name of object_to_match
        :param bool point: align the translation to the object to match
        :param bool orient: orient the flag to the object to match
        :param float scale: scale of the flag.
        :param bool add_align_transform: True creates a zero transform node above the flag.
        :param bool meta_connect: True if we want to connect the flag to the driven transform.
        :return: Returns an isinstance of the Flag class
        :rtype: Flag
        """

        if not pm.objExists(object_to_match):
            raise pm.MayaNodeError("object given to match, {0}, doesn't exist".format(object_to_match))
        object_to_match = pm.PyNode(object_to_match)

        pm.select(cl=True)
        _flag = pm.joint()
        _flag.rotateOrder.set(object_to_match.rotateOrder.get())

        # create a meta connection between the flag and the driven transform
        if meta_connect:
            attr_utils.connect_nodes_with_message_attrs(_flag, 'driven_transform', object_to_match, 'driver_flag')

        # rename flag
        if not label:
            label = object_to_match.split(':')[-1]
        if label.split('_')[0] == 'b':
            label_list = label.split(':')[-1].split('_')[1:]
            label = '_'.join(label_list)

        _flag = pm.rename(_flag, 'f_{}'.format(label))
        if isinstance(object_to_match, pm.nt.Joint):
            joint_utils.inherit_joint_labelling(object_to_match, _flag)

        shape_name = 'f_{naming.get_basename(object_to_match)}Shape'
        shape_node = pm.curve(n=shape_name, d=1, p=(
            (7, 7, 7), (7, 7, -7), (7, -7, -7), (7, -7, 7), (7, 7, 7), (-7, 7, 7), (-7, 7, -7), (7, 7, -7),
            (7, -7, -7), (-7, -7, -7), (-7, -7, 7), (7, -7, 7), (7, 7, 7), (-7, 7, 7), (-7, -7, 7), (-7, -7, -7),
            (-7, 7, -7)), k=(0, 1, 2, 3, 4, 5, 6, 7, 7, 9, 10, 11, 12, 13, 14, 15, 16))

        shape_node.scale.set(scale, scale, scale)
        pm.makeIdentity(shape_node, apply=True, t=1, r=1, s=1, n=0)

        # parent new flag shapes into original transform flag node and make sure shape nodes are renamed properly
        dag.parent_shape_node(shape_node, _flag, maintain_offset=maintain_shape_offset)
        _flag.drawStyle.set(2)
        for i, flag_shape in enumerate(_flag.getShapes()):
            flag_shape.rename('{}Shape{}'.format(_flag.shortName(), str(i) if i > 0 else ''))

        # align and move rotation to joint orient
        if point:
            pm.delete(pm.pointConstraint(object_to_match, _flag, mo=False, w=1))

        if orient:
            pm.delete(pm.orientConstraint(object_to_match, _flag, mo=False, w=1))

        pm.makeIdentity(_flag, apply=True, t=0, r=1, s=0, n=0)

        if add_align_transform:
            align_transform = rig_utils.create_align_transform(_flag)
            if orientation:
                align_parent = align_transform.getParent()
                pm.parent(align_parent, w=True)
                align_transform.rotate.set(orientation)
                pm.parent(align_transform, align_parent)
                pm.parent(_flag, align_transform)
                _flag.jointOrient.set(0, 0, 0)

        # Add Attributes
        _flag.addAttr('isFlag', at='bool', dv=True)
        _flag.addAttr('flagLayer', at="message", )
        _flag.radius.set(keyable=False, channelBox=False)

        # check whether it should be a detail flag that is hidden separately in a display layer.
        _flag.addAttr('isDetail', at='bool', dv=True)
        _flag.addAttr('isSub', at='bool', dv=True)
        _flag.addAttr('isContact', at='bool', dv=True)
        _flag.addAttr('isUtil', at='bool', dv=True)
        if not is_detail:
            _flag.isDetail.set(False)

        if not is_sub:
            _flag.isSub.set(False)

        if not is_contact:
            _flag.isContact.set(False)

        if not is_util:
            _flag.isUtil.set(False)

        return cls(_flag)

    @property
    def name(self):
        """
        Returns the absolute flag name.

        :return: Returns the absolute joint name.
        :rtype: str
        """

        return naming.get_basename(self.node)

    @staticmethod
    def create_ratio(object_to_match,
                     ratio=0.5,
                     label='',
                     point=True,
                     orient=True,
                     scale=1,
                     shape=None,
                     add_align_transform=True,
                     is_detail=False,
                     is_sub=False):
        if not isinstance(object_to_match, pm.nt.Transform):
            raise pm.MayaNodeError("object given to match, {0}, is not a Transform".format(object_to_match))

        _flag = Flag.create(object_to_match=object_to_match,
                            shape=shape,
                            maintain_shape_offset=True,
                            label=label,
                            point=point,
                            orient=orient,
                            scale=scale,
                            add_align_transform=add_align_transform,
                            is_detail=is_detail,
                            is_sub=is_sub)
        return _flag

    def set_as_detail(self):
        """
        Sets the flag as a detail flag.

        """

        self.isDetail.set(True)

    def set_as_sub(self):
        """
        Sets the flag as a subset flag.

        """

        self.isSub.set(True)

    def set_as_contact(self):
        """
        Sets the flag as a contact flag.

        """

        self.isContact.set(True)

    def set_as_util(self):
        """
        Sets the flag as a util flag.

        """

        self.isUtil.set(True)

    def get_align_transform(self):
        '''
        Get the zero transform for the flag.

        :return: align_transform: the zero transform node.
        :rtype: nt.Transform
        '''

        align_transform = None
        if self.hasAttr('alignTransform'):
            align_transforms = self.alignTransform.listConnections()
            if align_transforms:
                align_transform = align_transforms[0]
        return align_transform

    def hide_align_transform(self):
        align = self.get_align_transform
        align.v.set(0)

    def lock_and_hide_attrs(self, attr_list):
        """
        Locks and hides attributes

        :param list(str) attr_list: List of attributes to lock.  EX: ['tx', 'ty', 'tz']
        """

        attr_utils.lock_and_hide_attrs(self, attr_list)

    def __getattr__(self, attrname):
        return getattr(self.node, attrname)

    def __str__(self):
        return self.node.__str__()

    def __melobject__(self):
        return self.node.__melobject__()

    def __apimfn__(self):
        return self.node.__apimfn__()

    def __repr__(self):
        return self.node.__repr__()

    def __radd__(self, other):
        return self.node.__radd__(other)

    def __reduce__(self):
        return self.node.__reduce__()

    def __eq__(self, other):
        return self.node.__eq__(other)

    def __ne__(self, other):
        return self.node.__ne__(other)

    def __nonzero__(self):
        return self.node.__nonzero__()

    def __lt__(self, other):
        return self.node.__lt__(other)

    def __gt__(self, other):
        return self.node.__gt__(other)

    def __le__(self, other):
        return self.node.__le__(other)

    def __ge__(self, other):
        return self.node.__ge__(other)

    def __hash__(self):
        return self.node.__hash__()


# $TODO FSchorsch consider a better place to put this function
def _get_curve_data(shape_node):
    """
    Internal function that retrieves the curve data from the given shape node.

    :param pm.Shape shape_node: flag curve shape node.
    :return: dictionary containing all the curve shape data.
    :rtype: dict
    """

    curve_data = {'knots': tuple(shape_node.getKnots()),
                  'cvs': tuple(map(tuple, shape_node.getCVs('world'))),
                  'degree': shape_node.degree(),
                  'form': int(shape_node.form())}

    return curve_data


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
        curve_data = _get_curve_data(found_shape)
        data[naming.get_basename(found_shape)] = curve_data

    return data


def export_flag(transform_node, flag_path):
    """
    Serializes given transform node and saves it to the given path.

    :param Transform transform_node: node that represents a transform node with shapes.
    :param str flag_path: path to save the serialized flag.
    """

    if not isinstance(transform_node.getShape(), pm.nt.NurbsCurve):
        return

    # Duplicate the flag we want to export
    flag_to_export = pm.duplicate(transform_node)[0]
    flag_to_export.setParent(None)
    flag_parent = flag_to_export.getParent()
    if flag_parent:
        flag_parent.r.set(0, 0, 0)
        flag_parent.t.set(0, 0, 0)
        flag_parent.s.set(1, 1, 1)
        flag_to_export.setParent(None)
        pm.delete(flag_parent)
    attr_utils.set_attr_state(flag_to_export, False)

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
    yamlio.write_to_yaml_file(data_dict, flag_path)


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
        cvs = curve_data['cvs']
        knots = curve_data['knots']
        degree = curve_data['degree']
        form = curve_data['form']
        periodic = True if form == 3 else False

        if not new_curve:
            new_curve = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic, append=False)

        child_curve = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic)
        dag.parent_shape_node(child_curve, new_curve, maintain_offset=True, replace=False)

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
    flag_data = yamlio.read_yaml_file(flag_path) or {}
    return deserialize_flag(flag_data.get('curve_data', {}))
