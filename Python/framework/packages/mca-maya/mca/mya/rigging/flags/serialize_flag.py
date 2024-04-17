#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Rig Control data part implementation
"""

# System global imports
import os
import re
# software specific imports
import pymel.core as pm
# mca python imports
from mca.common.assetlist import assetlist
from mca.common.resources import resources
from mca.common.utils import strings, lists, fileio
from mca.common.textio import jsonio
from mca.common.paths import project_paths
from mca.mya.utils import node_util, attr_utils, maya_utils, dag
from mca.common import log
from mca.mya.rigging import tek


logger = log.MCA_LOGGER


def serialize_flag(transform_node, space=None, serialize_color=True, normalize=False, serialize_transform_matrix=True):
    """
    Serializes given transform node and returns a dictionary with all the data necessary to recreate that flag.

    :param pm.Transform transform_node: node that represents a transform node with shapes.
    :param str space: space we want to serialize shape data with ('world', 'transform', 'object')
    :param bool serialize_color: whether to include color data of the curve shapes.
    :param bool normalize: whether to CVs should be normalized in 0 to 1 range.
    :param bool serialize_transform_matrix: whether to include curve transform matrices.
    :return: returns serialized transform curves.
    :return: serialized transform curves.
    :rtype: dict
    """

    def _get_curve_data(shape_node):
        """
        Internal function that retrieves the curve data from the given shape node.

        :param pm.Shape shape_node: flag curve shape node.
        :return: dictionary containing all the curve shape data.
        :rtype: dict
        """

        curve_data = dag.get_node_color_data(shape_node) if serialize_color else dict()
        curve_data.update({
            'knots': tuple(shape_node.getKnots()),
            'cvs': tuple(map(tuple, shape_node.getCVs(space))),
            'degree': shape_node.degree(),
            'form': int(shape_node.form()),
            'worldMatrix': get_transform_world_matrix(transform_node).formated() if serialize_transform_matrix else None,
            'matrix': transform_node.attr('matrix').get().formated() if serialize_transform_matrix else None})

        return curve_data

    data = dict()
    space = space or 'world'
    shapes = transform_node.getShapes()
    for shape_found in shapes:
        if shape_found.isIntermediateObject():
            continue
        curve_data = _get_curve_data(shape_found)
        curve_data['space'] = space
        if serialize_color:
            curve_data['outlinerColor'] = tuple(curve_data['outlinerColor'])
            curve_data['overrideColorRGB'] = tuple(curve_data['overrideColorRGB'])
        data[shape_found.nodeName(stripNamespace=True)] = curve_data

    if normalize:
        mx = 1
        for shape_name, shape_data in data.items():
            for cv in shape_data['cvs']:
                for p in cv:
                    if mx < abs(p):
                        mx = abs(p)
        for shape_name, shape_data in data.items():
            shape_data['cvs'] = [[p / mx for p in pt] for pt in shape_data['cvs']]

    return data


def deserialize_flag(flag_data, name=None, space=None, parent=None, replace=False):
    """
    Deserializes given flag data and creates a new flag based on it.

    :param dict flag_data: flag data serialized using serialize_flag function.
    :param str space: space we want to deserialize shape data with ('world', 'transform', 'object')
    :param pm.Transform or None parent: optional parent transform node for the deserialized flag shapes.
    :return: newly created flag.
    :rtype: Flag or None
    """

    # import here to avoid cyclic imports
    from mca.mya.rigging.flags import tek_flag

    space = flag_data.get('space', '') or space or 'world'

    if not parent:
        replace = False
    parent = parent or None

    new_curve = None
    current_shape = 0
    for shape_name, curve_data in iter(flag_data.items()):
        cvs = curve_data['cvs']
        knots = curve_data['knots']
        degree = curve_data['degree']
        form = curve_data['form']
        periodic = True if form == 3 else False

        if not parent:
            replace = False
            parent = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic, append=False)
            new_curve = parent
        else:
            if replace:
                pm.curve(parent, point=cvs, knot=knots, degree=degree, periodic=periodic, replace=True)
            else:
                child_curve = pm.curve(point=cvs, knot=knots, degree=degree, periodic=periodic)
                dag.parent_shape_node(
                    child_curve, parent, maintain_offset=True, freeze_transform=True, replace=False)

        current_shape += 1

    if not new_curve:
        logger.warning('Was not possible to deserialize flag')
        return None

    if name:
        pm.rename(new_curve, name)

    return tek_flag.Flag(new_curve)


def export_flag(transform_node, directory, flag_name=None, export_color=True, in_place=False):
    """
    Exports given flag node into given directory.

    :param Flag or pm.Transform transform_node: flag transform node we want to export shapes of.
    :param str directory: directory where flag file will be stored.
    :param str flag_name: optional name for the exported flag file.
    :param bool export_color: whether to flag color should be stored within file.
    :param bool in_place: whether the flag should be exported in place or in the 0, 0, 0 of the world.
    :return: True if the export flag operation was successful; False otherwise.
    :rtype: bool
    """

    flag_name = flag_name or transform_node.shortName(stripNamespace=True)
    flag_path = os.path.join(directory, f'{flag_name}.flag')
    if os.path.exists(flag_path):
        fileio.touch_path(flag_path)
    flag_data = FlagData(flag_path)

    if not in_place:
        duplicated_flag = pm.duplicate(transform_node)[0]
        duplicated_flag.setParent(world=True)
        attr_utils.unlock_transform_attributes(duplicated_flag)
        pm.move(duplicated_flag, [0, 0, 0])
        try:
            return flag_data.export_data(duplicated_flag, export_color=export_color)
        finally:
            if not duplicated_flag.getParent():
                pm.delete(duplicated_flag)
            else:
                pm.delete(duplicated_flag.getParent())
    else:
        return flag_data.export_data(transform_node, export_color_data=export_color)


class FlagData():
    """
    DataPart that represents Flag Curve data.
    """

    DATA_TYPE = 'rig.flag'
    NICE_NAME = 'Rig Flag'
    PRIORITY = 10
    VERSION = 1

    _has_trait = re.compile(r'\.flag$', re.I)
    
    def __init__(self, identifier):
        self._id = identifier

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        """
        Overrides base DataPart can_represent function.
        Returns whether this data part can represent by the given identifier.

        :param str identifier: data identifier. This could be a URL, a file path, a UUID, etc.
        :param bool only_extension: If True, only trait (usually extension) will be checked.
        :return: True if the current data part can be represented by the given identifier; False otherwise.
        :rtype: bool
        """

        if FlagData._has_trait.search(identifier):
            if only_extension:
                return True
            if os.path.exists(identifier):
                return True

        return False

    @classmethod
    def extension(cls):
        """
        Overrides base DataPart extension function.
        Returns extension of this data part.

        :return: data part extension.
        :rtype: str
        """

        return '.flag'

    @classmethod
    def icon(cls):
        """
        Overrides base DataPart icon function.
        Returns the icon of this data part.

        :return: data part icon
        :rtype: QIcon
        """

        return resources.icon(r'color\circle.png')

    def functionality(self):
        """
        Overrides base DataPart functionality function.
        Exposes per-data functionality in the form of a dictionary where the key is the string accessor, and the value
        is a callable one.
        In a situation where multiple DataParts are bound then a single dictionary with all the entries combined is
        returned.

        :return: data part functionality dictionary.
        :rtype: dict
        """

        return dict(
            read_data=self.read_data,
            save_data=self.save_data,
            import_data=self.import_data,
            export_data=self.export_data,
        )

    def read_data(self):
        """
        Reads flags data containing in file.

        :return: dictionary containing all flag data.
        :rtype: dict
        """

        file_path = self.identifier()
        file_path = strings.append_extension(file_path, self.extension())
        if not os.path.exists(file_path):
            logger.warning('Impossible to read flags data from non existent file: "{}"!'.format(file_path))
            return dict()

        logger.debug('Reading flags data from file: "{}"'.format(file_path))

        return jsonio.read_json_file(file_path)

    def save_data(self, flag_data=None):
        """
        Saves given curve data into a file in disk.

        :param dict flag_data: flags data to save.
        :return: True if the save operation was successful; False otherwise.
        :rtype: bool
        """

        file_path = self.identifier()
        if not file_path:
            logger.warning('Impossible to save flags data to file because save file path not defined!')
            return False
        file_path = strings.append_extension(file_path, self.extension())

        jsonio.write_to_json_file(flag_data, file_path)

        return True

    def import_data(self):
        """
        Imports flags data from file.

        :return: newly created flag from imported data.
        :rtype: Flag or None
        """

        file_path = self.identifier()
        file_path = strings.append_extension(file_path, self.extension())
        if not os.path.exists(file_path):
            logger.warning('Impossible to import flags data file "{}" because it does not exists!'.format(
                file_path))
            return False

        flag_data = self.functionality()['read_data']()
        if not flag_data:
            logger.warning(
                'Impossible to import flags data file "{}" because it does not contains valid skeleton data!'.format(
                    file_path))
            return False
        flag_data = flag_data.get('flag', dict())
        if not flag_data:
            logger.warning('No valid flag data found within file: {}'.format(file_path))
            return False

        return deserialize_flag(flag_data)
    
    def identifier(self):
        """
        Returns the identifier of this data part.

        :return: data part identifier.
        :rtype: str
        """

        return self._id

    def export_data(self, flag_to_export=None, export_color_data=False, **kwargs):
        """
        Exports flag data to file.

        :param Flag or pm.Transform flag_to_export: flag whose data we want to save.
        :param bool export_color_data: whether to export controls color data.
        :return: True if the export data operation was successful; False otherwise.
        :rtype: bool
        """

        file_path = self.identifier()
        if not file_path:
            logger.warning('Impossible to save flag data to file because save file path not defined!')
            return False
        file_path = strings.append_extension(file_path, self.extension())

        flag_to_export = flag_to_export or lists.get_first_in_list(pm.selected())
        if not flag_to_export:
            logger.warning('No flag selected to export. please, select flag to export')
            return False

        logger.debug('Saving {}'.format(file_path))

        space = kwargs.get('space', None)
        flag_data = serialize_flag(flag_to_export, normalize=False, serialize_color=export_color_data, space=space)
        if not flag_data:
            logger.warning('Was not possible to serialize flag data: {}'.format(flag_to_export))
            return False

        data_to_save = dict(
            flag=flag_data,
            dcc=dict(
                name='Maya',
                version=maya_utils.get_version(),
                up_axis=pm.upAxis(query=True, axis=True)
            ),
            version=FlagData.VERSION
        )

        valid = self.functionality()['save_data'](flag_data=data_to_save)
        if not valid:
            logger.warning(
                'Was not possible to save flag "{}" data properly in file: "{}"'.format(flag_to_export, file_path))
            return False

        return True


def get_transform_world_matrix_attribute(node):
    """
    Returns the MPlug pointing worldMatrix of the given Maya object pointing a DAG node.

    :param pm.PyNode node: PyMEL node we want to retrieve world matrix plug of.
    :return: World matrix Maya object attribute.
    :rtype: pm.Attribute
    """

    world_matrix = node.attr('worldMatrix')
    return world_matrix.elementByLogicalIndex(0)


def get_transform_world_matrix(node):
    """
    Returns world matrix of the given PyMEL node.

    :param pm.PyNode node: PyMEL node we want to retrieve world matrix of.
    :return: Maya object world matrix.
    :rtype: pm.datatypes.Matrix
    """

    return get_transform_world_matrix_attribute(node).get()

