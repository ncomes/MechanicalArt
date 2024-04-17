#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related with Maya follicles
"""
# System global imports
# python imports
import pymel.core as pm
# mca python imports
from mca.mya.utils import naming


def create_empty_follicle(name=None, uv=None, hide_follicle=True):
    """
    Creates a new empty follicle.

    :param str name: name of the follicle.
    :param list(int, int) uv: uv where follicle will be created.
    :param bool hide_follicle: whether follicle should be hided by default.
    :return: name of the created follicle.
    :rtype: str
    """

    uv = uv if uv is not None else [0, 0]
    follicle_shape = pm.createNode('follicle')
    if hide_follicle:
        pm.hide(follicle_shape)
    follicle = pm.listRelatives(follicle_shape, p=True)[0]
    pm.setAttr('{}.inheritsTransform'.format(follicle), False)
    follicle.rename(name or 'follicle')

    pm.setAttr('{}.parameterU'.format(follicle), uv[0])
    pm.setAttr('{}.parameterV'.format(follicle), uv[1])

    return follicle


def create_mesh_follicle(mesh, description=None, uv=None, hide_follicle=True):
    """
    Crates follicle on given mesh.

    :param mesh: str, name of the mesh to attach follicle to.
    :param str description: description of the follicle.
    :param list(int, int) uv: corresponds to the UVs of the mesh in which the follicle will be attached.
    :param bool hide_follicle: whether follicle should be hide by default.
    :return: tuple with the created follicle transform and the follicle shape
    :rtype: tuple(str, str)
    """

    uv = uv if uv is not None else [0, 0]
    follicle = create_empty_follicle(description, uv, hide_follicle=hide_follicle)
    shape = pm.listRelatives(follicle, shapes=True)[0]
    pm.connectAttr('{}.outMesh'.format(mesh), '{}.inputMesh'.format(follicle))
    pm.connectAttr('{}.worldMatrix'.format(mesh), '{}.inputWorldMatrix'.format(follicle))
    pm.connectAttr('{}.outTranslate'.format(shape), '{}.translate'.format(follicle))
    pm.connectAttr('{}.outRotate'.format(shape), '{}.rotate'.format(follicle))

    return follicle, shape


def create_surface_follicle(surface, name=None, uv=None, hide_follicle=True):
    """
    Crates follicle on a surface.

    :param str surface: name of the surface to attach follicle to.
    :param str name: description of the follicle.
    :param list(int, int) uv: corresponds to the UVs of the mesh in which the follicle will be attached.
    :param bool hide_follicle: whether follicle should be hide by default.
    :return: tuple with the created follicle transform and the follicle shape.
    :rtype: tuple(str, str)
    """

    uv = uv if uv is not None else [0, 0]
    follicle = create_empty_follicle(name, uv, hide_follicle=hide_follicle)
    shape = pm.listRelatives(follicle, shapes=True)[0]
    pm.connectAttr('{}.local'.format(surface), '{}.inputSurface'.format(follicle))
    pm.connectAttr('{}.worldMatrix'.format(surface), '{}.inputWorldMatrix'.format(follicle))
    pm.connectAttr('{}.outTranslate'.format(shape), '{}.translate'.format(follicle))
    pm.connectAttr('{}.outRotate'.format(shape), '{}.rotate'.format(follicle))

    return follicle, shape


def create_follicle_constraint(node, mesh, maintain_offset=False):
    """
    Create a follicle and on the mesh and constrain the node.

    :param node: the object that will be constrained.
    :param mesh:  the mesh that the object will be constrained too.
    :param maintain_offset: sets maintain offset on the parent constraint.
    """

    closest = None

    try:
        shapes = pm.listRelatives(mesh, shapes=True)
        if shapes:
            if not pm.attributeQuery('inMesh', n=shapes[0], exists=True):
                raise Exception('{} is not a valid mesh'.format(mesh))
        else:
            raise Exception('{} is not a valid mesh'.format(mesh))

        closest = pm.createNode('closestPointOnMesh')
        pm.connectAttr('{}.outMesh'.format(mesh), '{}.inMesh'.format(closest))
        trans = pm.xform(node, t=True, q=True)

        pm.setAttr('{}.inPositionX'.format(closest), trans[0])
        pm.setAttr('{}.inPositionY'.format(closest), trans[1])
        pm.setAttr('{}.inPositionZ'.format(closest), trans[2])

        follicle_transform, follicle = create_mesh_follicle(mesh, 'follicle', hide_follicle=False)

        pm.setAttr('{}.simulationMethod'.format(follicle), 0)

        u = pm.getAttr('{}.result.parameterU'.format(closest))
        v = pm.getAttr('{}.result.parameterV'.format(closest))

        pm.setAttr('{}.parameterU'.format(follicle), u)
        pm.setAttr('{}.parameterV'.format(follicle), v)

        pm.parentConstraint(follicle_transform[0], node, mo=maintain_offset)

        # rename the follicle
        pm.rename(follicle_transform, '{}_FOL'.format(node))
    except Exception:
        raise
    finally:
        if closest:
            pm.delete(closest)


def create_follicle_constraint_from_selection(maintain_offset=False):
    """
    Create a follicle constraint based on the selection whereas the last selected node is the mesh.

    :param maintain_offset: Sets up the constraint's maintain offset.
    """

    sel_nodes = pm.ls(sl=True)
    mesh = sel_nodes[-1]
    nodes = sel_nodes[:-1]
    for node in nodes:
        create_follicle_constraint(node, mesh, maintain_offset=maintain_offset)
