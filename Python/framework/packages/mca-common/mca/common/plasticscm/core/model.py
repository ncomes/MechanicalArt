#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base module classes used by PlasticSCM
"""

from __future__ import print_function, division, absolute_import

import aenum


class RepId(object):
    """
    PlasticSCM repository ID.
    """

    pass


class Owner(object):
    """
    PlasticSCM repository owner.
    """

    pass


class Repository(object):
    """
    PlasticSCM repository.
    """

    pass


class Workspace(object):
    """
    PlasticSCM workspace.
    """

    pass


class OperationStatus(object):
    """
    PlasticSCM operation status.
    """

    pass


class XLink(object):
    """
    PlasticSCM XLink target.
    """

    pass


class Item(object):
    """
    PlasticSCM item
    """

    @aenum.unique
    class Type(aenum.Enum):
        """
        Plastic SCM item type
        """

        pass


class AffectedPaths(object):
    """
    PlasticSCM affected paths.

    Represents the paths that were affected by an update operation.
    """

    pass


class FileInfo(object):
    """
    PlasticSCM file info.
    """

    pass
