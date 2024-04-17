#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an ik chain
"""

# System global imports
# python imports
import pymel.core as pm

from mca.mya.utils import dag, naming
from mca.mya.rigging import rig_utils
from mca.mya.rigging.flags import tek_flag
from mca.mya.rigging import ik_utils


def ik_joint_chain(start_joint,
                    end_joint,
                    side,
                    region,
                    scale=1.0,
                    ik_flag_orient=None,
                    ik_flag_pv_orient=None,
                    ik_flag_rotate_order=None):
    """
    Builds an IK joint chain rig.

    :param pm.nt.Joint start_joint: Start joint (ex: ankle)
    :param pm.nt.Joint end_joint: End joint (ex: toe)
    :param str side: Which side the foot is on.
    :param str region: A unique name for the region.  (ex: foot)
    :param list(str) ik_flag_orient: orientation of the ik flag.
    :param list(str) ik_flag_pv_orient: orientation of the ik pv flag.
    :param list(str) ik_flag_rotate_order: Rotate order of the ik flag.
    :return: Returns a dictionary with all the built nodes.
    :rtype: dictionary
    """

    # Chain
    chain = dag.get_between_nodes(start_joint, end_joint, pm.nt.Joint)
    if not (len(chain) == 3 or len(chain) == 4):
        raise RuntimeError("There can only be 3 or 4 joints between start_joint and end_joints")

    middle_joint = chain[1]
    if len(chain) > 3:
        end_joint = chain[2]

    # Pole Vector position
    pv_point = ik_utils.get_pole_vector_position([start_joint, middle_joint, end_joint])

    # Find pv point before ik, in case joints move
    pv_locator = rig_utils.create_locator_at_point(pv_point)

    # Ik Handle
    ik_handle_node, eff = pm.ikHandle(sol='ikRPsolver', sj=start_joint, ee=end_joint)
    ik_handle_node.rename('{0}_{1}_ikhandle'.format(side, region))
    ik_handle_node.visibility.set(0)
    ik_solver = ik_handle_node.ikSolver.get()

    # Create flags
    ik_flag = tek_flag.Flag.create(end_joint,
                                    scale=scale,
                                    label='{0}_{1}'.format(side, region),
                                    add_align_transform=True,
                                    orientation=ik_flag_orient)

    ik_flag_offset = tek_flag.Flag.create(end_joint,
                                           scale=scale*.75,
                                           label='{0}_{1}_offset'.format(side, region),
                                           add_align_transform=True,
                                           orientation=ik_flag_orient,
                                           is_detail=True)

    pv_flag = tek_flag.Flag.create(pv_locator,
                                    scale=scale,
                                    label='{0}_{1}_pv'.format(side, region),
                                    add_align_transform=True,
                                    orientation=ik_flag_pv_orient)

    # Reference line
    pv_line = rig_utils.create_line_between(middle_joint, pv_flag, name='{0}_{1}_pv_line'.format(side, region))
    pv_line.inheritsTransform.set(0)

    line_shapes = pv_line.listRelatives(s=True)
    all_clusters = []
    for shape in line_shapes:
        clusters = shape.listConnections(type=pm.nt.Cluster)
        for cluster in clusters:
            if cluster not in all_clusters:
                all_clusters.append(cluster)
    # Align group
    ik_align_group = pm.group(name=naming.get_basename(ik_handle_node) + "_align_transform", empty=True)
    pm.delete(pm.parentConstraint(ik_handle_node, ik_align_group, w=True, mo=False))
    ik_handle_node.setParent(ik_align_group)

    # Add twist control
    ik_flag.addAttr('___', k=True, at='bool')
    ik_flag.setAttr('___', e=True, cb=True, l=True)
    ik_flag.addAttr('ikTwist', keyable=True, at='double')
    ik_flag.ikTwist >> ik_handle_node.twist

    # Constraints
    pv_constraint = pm.poleVectorConstraint(pv_flag, ik_handle_node, w=1)
    ik_constraint = pm.parentConstraint(ik_flag, ik_align_group, w=1, mo=1)
    pm.delete(pv_locator)

    orient_str_val = {'xyz': 0, 'yzx': 1, 'zxy': 2, 'xzy': 3, 'yxz': 4, 'zyx': 5}

    if ik_flag_rotate_order and orient_str_val.keys():
        temp_loc = rig_utils.create_locator_at_object(ik_flag)
        ik_flag.rotateOrder.set(orient_str_val[ik_flag_rotate_order])
        pm.delete(pm.orientConstraint(temp_loc, ik_flag, w=True, mo=False))
        pm.delete(temp_loc)

    ik_offset_align_transform = ik_flag_offset.get_align_transform()
    pm.parent(ik_offset_align_transform, ik_flag)

    offset_constraint = pm.orientConstraint(ik_flag_offset, end_joint, mo=1, w=1)

    ik_flag.addAttr('offsetFlag', at='message')
    ik_flag_offset.addAttr('offsetFlag', at='message')
    ik_flag.offsetFlag >> ik_flag_offset.offsetFlag
    unit_conv_nodes = [x for x in ik_flag.listConnections() if isinstance(x, pm.nt.UnitConversion)]

    # create dictionary
    return_dictionary = dict()
    return_dictionary['chain'] = chain
    return_dictionary['start_joint'] = start_joint
    return_dictionary['end_joint'] = end_joint
    return_dictionary['ik_handle'] = ik_handle_node
    return_dictionary['ik_zero'] = ik_align_group
    return_dictionary['ik_effector'] = eff
    return_dictionary['ik_flag'] = ik_flag
    return_dictionary['ik_flag_offset'] = ik_flag_offset
    return_dictionary['pv_flag'] = pv_flag
    return_dictionary['pv_constraint'] = pv_constraint
    return_dictionary['ik_constraint'] = ik_constraint
    return_dictionary['offset_constraint'] = offset_constraint
    return_dictionary['pv_line'] = pv_line
    return_dictionary['flags'] = [ik_flag, ik_flag_offset, pv_flag]
    return_dictionary['line_clusters'] = all_clusters
    return_dictionary['ik_solver'] = ik_solver
    return_dictionary['unit_conv_nodes'] = unit_conv_nodes

    return return_dictionary
