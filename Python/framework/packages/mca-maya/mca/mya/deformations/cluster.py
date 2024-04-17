#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parameter data for working with the facial rigs.
"""
# System global imports

# software specific imports
import pymel.core as pm

# mca python imports
from mca.mya.utils import namespace

def create_cluster_from_component_names(points, name, relative=False, front_of_chain=True, exclusive=False):
    """
    Creates a cluster on the CV/vertex names.

    :param points: list(str), names of cv points to cluster.

    :param str name: name of the cluster.
    :param bool relative: whether cluster is created in relative mode. In this mode, only the transformations
        directly above the cluster are used by the cluster.
    :param bool front_of_chain:
    :param bool exclusive: whether cluster deformation set is put in deform partition. If True, a vertex/CV
        only will be able to be deformed by one cluster.
    :return: list(str, str), [cluster, handle]
    """

    # NOTE: for some reason if we try to create a cluster with a namespace active a RuntimeError with the following
    # description will raise: Problems occurred with dependency graph setup. For that reason, we make sure we
    # set the root namespace and after creating the clusters we assign them to the specific namespace (if necessary).
    current_namespace = pm.namespaceInfo(currentNamespace=True, absoluteName=True)
    if current_namespace != ':':
        pm.namespace(setNamespace=':')

    try:
        # NOTE: bug detected in Maya 2019 and older versions. If we pass exclusive argument, no matter if we pass True
        # of False, exclusivity will be enabled.
        if exclusive:
            cluster, handle = pm.cluster(points, n=name, relative=relative, frontOfChain=front_of_chain, exclusive=True)
        else:
            cluster, handle = pm.cluster(points, n=name, relative=relative, frontOfChain=front_of_chain)
    finally:
        if current_namespace != ':':
            pm.namespace(setNamespace=current_namespace)

    if current_namespace != ':':
        pm.rename(f'{current_namespace}{cluster}')
        pm.rename(f'{current_namespace}{handle}')

    return cluster, handle
