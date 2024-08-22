#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related to building a simple FK chain.
"""

# python imports

# software specific imports
import pymel.all as pm

# Project python imports
from mca.common.utils import pymaths

from mca.mya.rigging import flags, joint_utils
from mca.mya.utils import attr_utils, constraint_utils, dag_utils, naming

def build_ik_chain(joint_chain, scale=None):
    scale = scale or 1.0

    if not len(joint_chain) == 3:
        return {}

    start_joint, mid_joint, end_joint = joint_chain
    wrapped_joint = joint_utils.JointMarkup(start_joint)
    if wrapped_joint.side and wrapped_joint.region:
        ik_system_name = naming.get_basename(f'{wrapped_joint.side}_{wrapped_joint.region}')
    else:
        joint_name = naming.get_basename(start_joint)
        if joint_name.startswith('b_'):
            joint_name = joint_name[2:]
        ik_system_name = f'ik_{joint_name}'

    # Find our PV location and give us a locator
    pole_vector_pos = pymaths.get_pole_vector_pos(*[pm.xform(x, q=True, t=True, ws=True) for x in joint_chain])
    pv_locator = pm.Locator(n=f'{ik_system_name}_pv').getParent()
    pv_locator.t.set(pole_vector_pos)
    pv_locator.setParent(mid_joint)

    # Setup our IK solver.
    ik_handle_node, eff = pm.ikHandle(sol='ikRPsolver', sj=start_joint, ee=end_joint)
    ik_handle_node.rename(f'{ik_system_name}_ikhandle')
    ik_handle_node.visibility.set(0)
    ik_solver = ik_handle_node.ikSolver.get()

    # Ik Handle align group
    ik_align_group = pm.group(name=f'{naming.get_basename(ik_handle_node)}_align_transform', empty=True, w=True)
    ik_align_group.v.set(False)
    pm.delete(pm.parentConstraint(ik_handle_node, ik_align_group, w=True, mo=False))
    ik_handle_node.setParent(ik_align_group)

    # Create flags
    ik_flag = flags.Flag.create(f'f_{ik_system_name}_ik', end_joint, scale)
    if wrapped_joint.side:
        ik_flag.side = wrapped_joint.side
        ik_flag.region = wrapped_joint.region
    ik_flag.swap_shape('pos and rot', scale, [0, 90, 0])
    ik_flag.set_attr_state(True, attr_utils.SCALE_ATTRS)
    pv_flag = flags.Flag.create(f'f_{ik_system_name}_pv', pv_locator, scale, flag_path='pos and rot')
    if wrapped_joint.side:
        pv_flag.side = wrapped_joint.side
        pv_flag.region = wrapped_joint.region
    pv_flag.set_attr_state(True, attr_utils.SCALE_ATTRS+attr_utils.ROTATION_ATTRS)
    flag_list = [ik_flag, pv_flag]

    # Reference line
    pv_curve = dag_utils.create_line_between(mid_joint, pv_flag.pynode, name=f'{ik_system_name}_pv_line')
    pv_curve.inheritsTransform.set(0)

    curve_shapes = pv_curve.listRelatives(s=True)
    all_clusters = []
    for shape_node in curve_shapes:
        clusters = shape_node.listConnections(type=pm.nt.Cluster)
        for cluster in clusters:
            if cluster not in all_clusters:
                all_clusters.append(cluster)

    # Constraints
    pv_constraint = pm.poleVectorConstraint(pv_flag.pynode, ik_handle_node, w=1)
    ik_constraint = pm.parentConstraint(ik_flag.pynode, ik_align_group, w=1, mo=1)
    constraint_utils.orient_constraint_safe(ik_flag.pynode, end_joint)
    pm.delete(pv_locator)

    # Add twist control
    ik_flag.pynode.addAttr('___', k=True, at='bool')
    ik_flag.pynode.setAttr('___', e=True, cb=True, l=True)
    ik_flag.pynode.addAttr('ikTwist', keyable=True, at='double')
    ik_flag.pynode.ikTwist >> ik_handle_node.twist

    unit_conv_nodes = [x for x in ik_flag.pynode.listConnections() if isinstance(x, pm.nt.UnitConversion)]

    # Fill out return dict.
    return_dict = {}
    return_dict['chain'] = joint_chain
    return_dict['start_joint'] = start_joint
    return_dict['end_joint'] = end_joint
    return_dict['flags'] = flag_list
    return_dict['ik_handle'] = ik_handle_node
    return_dict['ik_align_group'] = ik_align_group
    return_dict['ik_effector'] = eff
    return_dict['ik_flag'] = ik_flag
    return_dict['pv_flag'] = pv_flag
    return_dict['pv_constraint'] = pv_constraint
    return_dict['ik_constraint'] = ik_constraint
    return_dict['pv_curve'] = pv_curve
    return_dict['line_clusters'] = all_clusters
    return_dict['ik_solver'] = ik_solver
    return_dict['unit_conv_nodes'] = unit_conv_nodes
    return return_dict

def build_twopointik_chain(joint_chain, scale=None):
    scale = scale or 1.0

    if not len(joint_chain) == 2:
        return {}

    start_joint, end_joint = joint_chain
    wrapped_joint = joint_utils.JointMarkup(start_joint)
    if wrapped_joint.side and wrapped_joint.region:
        ik_system_name = naming.get_basename(f'{wrapped_joint.side}_{wrapped_joint.region}')
    else:
        joint_name = naming.get_basename(start_joint)
        if joint_name.startswith('b_'):
            joint_name = joint_name[2:]
        ik_system_name = f'ik_{joint_name}'

    # Setup our IK solver.
    ik_handle_node, eff = pm.ikHandle(sol='ikSCsolver', sj=start_joint, ee=end_joint)
    ik_handle_node.rename(f'{ik_system_name}_ikhandle')
    ik_handle_node.visibility.set(0)
    ik_solver = ik_handle_node.ikSolver.get()

    # Ik Handle align group
    ik_align_group = pm.group(name=f'{naming.get_basename(ik_handle_node)}_align_transform', empty=True, w=True)
    ik_align_group.v.set(False)
    pm.delete(pm.parentConstraint(ik_handle_node, ik_align_group, w=True, mo=False))
    ik_handle_node.setParent(ik_align_group)

    # Create flags
    ik_flag = flags.Flag.create(f'f_{ik_system_name}_ik', end_joint, scale)
    ik_flag.set_attr_state(attr_utils.SCALE_ATTRS)
    if wrapped_joint.side:
        ik_flag.side = wrapped_joint.side
        ik_flag.region = wrapped_joint.region
    ik_flag.swap_shape('pos and rot', scale, [0, 90, 0])
    
    # Constraints
    ik_constraint = pm.parentConstraint(ik_flag.pynode, ik_align_group, w=1, mo=1)

    unit_conv_nodes = [x for x in ik_flag.pynode.listConnections() if isinstance(x, pm.nt.UnitConversion)]

    # Fill out return dict.
    return_dict = {}
    return_dict['chain'] = joint_chain
    return_dict['start_joint'] = start_joint
    return_dict['end_joint'] = end_joint
    return_dict['flags'] = [ik_flag]
    return_dict['ik_handle'] = ik_handle_node
    return_dict['ik_align_group'] = ik_align_group
    return_dict['ik_effector'] = eff
    return_dict['ik_constraint'] = ik_constraint
    return_dict['ik_solver'] = ik_solver
    return_dict['unit_conv_nodes'] = unit_conv_nodes
    return return_dict