#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base module classes used by PlasticSCM v1
"""

from __future__ import print_function, division, absolute_import

from mca.common.plasticscm.core import model


class RepId(model.RepId):
    def __new__(cls, id, module_id):
        """
        Instantiates a new PlasticSCM RepID model.

        :param int id:
        :param int module_id:
        """

        self = super(RepId, cls).__new__(cls)
        self._id = id
        self._module_id = module_id

        return self

    @property
    def id(self):
        return self._id

    @property
    def module_id(self):
        return self._module_id


class Owner(model.Owner):
    def __new__(cls, name, is_group=False):
        """
        Instantiates a new PlasticSCM owner model.

        :param str name:
        :param bool is_group:
        """

        self = super(Owner, cls).__new__(cls)
        self._name = name
        self._is_group = is_group

        return self

    @property
    def name(self):
        return self._name

    @property
    def is_group(self):
        return self._is_group


class Repository(model.Repository):
    def __new__(cls, name, server, owner=None, rep_id=None, guid=None):
        """
        Instantiates a new PlasticSCM repository model.

        :param str name:
        :param str server:
        :param Owner owner:
        :param RepID rep_id:
        :param UUID guid:
        """

        self = super(Repository, cls).__new__(cls)
        self._name = name
        self._server = server
        self._owner = owner
        self._rep_id = rep_id
        self._guid = guid

        return self

    @property
    def name(self):
        return self._name

    @property
    def server(self):
        return self._server

    @property
    def owner(self):
        return self._owner

    @property
    def rep_id(self):
        return self._rep_id

    @property
    def guid(self):
        return self._guid


class Workspace(model.Workspace):
    def __new__(cls, name, path, machine_name, guid=None):
        """
        Instantiates a new PlasticSCM workspace model.

        :param str name:
        :param str path:
        :param str machine_name:
        :param UUID guid:
        """

        self = super(Workspace, cls).__new__(cls)
        self._name = name
        self._path = path
        self._machine_name = machine_name
        self._guid = guid

        return self

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def machine_name(self):
        return self._machine_name

    def guid(self):
        return self._guid


class OperationStatus(model.OperationStatus):
    """
    Instantiates a new PlasticSCM operation status model.
    """

    def __new__(
            cls, status=None, message=None, total_files=None, total_bytes=None, updated_files=None, updated_bytes=None):
        self = super(OperationStatus, cls).__new__(cls)

        self._status = status
        self._message = message
        self._total_files = total_files
        self._total_bytes = total_bytes
        self._updated_files = updated_files
        self._updated_bytes = updated_bytes

        return self

    @property
    def satus(self):
        return self._status

    @property
    def message(self):
        return self._message

    @property
    def total_files(self):
        return self._total_files

    @property
    def total_bytes(self):
        return self._total_bytes

    @property
    def updated_files(self):
        return self._updated_files

    @property
    def updated_bytes(self):
        return self._updated_bytes


class XLink(model.XLink):

    def __new__(cls, changeset_id, changeset_guid, repo_name, server):
        self = super(XLink, cls).__new__(cls)

        self._changeset_id = changeset_id
        self._changeset_guid = changeset_guid
        self._repo_name = repo_name
        self._server = server

        return self

    @property
    def changeset_id(self):
        return self._changeset_id

    @property
    def changeset_guid(self):
        return self._changeset_guid

    @property
    def repo_name(self):
        return self._repo_name

    @property
    def server(self):
        return self._server


class Item(model.Item):

    class Type(model.Item.Type):
        FILE = 'file'
        DIRECTORY = 'directory'
        XLINK = 'xlink'

    def __new__(
            cls, type, name, path, revision_id, size, is_under_xlink, content, hash, items, xlink_targets,
            repository):
        self = super(Item, cls).__new__(cls)

        self._type = type
        self._name = name
        self._path = path
        self._revision_id = revision_id
        self._size = size
        self._is_under_xlink = is_under_xlink
        self._content = content
        self._hash = hash
        self._items = items
        self._xlink_targets = xlink_targets

        return self

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def revision_id(self):
        return self._revision_id

    @property
    def size(self):
        return self._size

    @property
    def is_under_xlink(self):
        return self._is_under_xlink

    @property
    def content(self):
        return self._content

    @property
    def hash(self):
        return self._hash

    @property
    def items(self):
        return self._items

    @property
    def xlink_targets(self):
        return self._xlink_targets


class AffectedPaths(model.AffectedPaths):
    """
    Instantiates a new PlasticSCM affected paths model.
    """

    def __new__(cls, affected_paths):
        self = super(AffectedPaths, cls).__new__(cls)

        self._affected_paths = affected_paths

        return self

    @property
    def affected_paths(self):
        return self._affected_paths


class FileInfo(object):
    """
    Instantiates a new PlasticSCM file info model.
    """

    def __new__(cls,
                client_path, relative_path, server_path, rep_spec, size, hash, owner, revision_head_changeset,
                revision_changeset, status, type, changelist):
        self = super(FileInfo, cls).__new__(cls)

        self._client_path = client_path
        self._relative_path = relative_path
        self._server_path = server_path
        self._rep_spec = rep_spec
        self._size = size
        self._hash = hash
        self._owner = owner
        self._revision_head_changeset = revision_head_changeset
        self._revision_changeset = revision_changeset
        self._status = status
        self._type = type
        self._changelist = changelist

        return self

    @property
    def client_path(self):
        return self._client_path

    @property
    def relative_path(self):
        return self._relative_path

    @property
    def server_path(self):
        return self._server_path

    @property
    def rep_spec(self):
        return self._rep_spec

    @property
    def size(self):
        return self._size

    @property
    def hash(self):
        return self._hash

    @property
    def owner(self):
        return self._owner

    @property
    def revision_head_changeset(self):
        return self._revision_head_changeset

    @property
    def revision_changeset(self):
        return self._revision_changeset

    @property
    def status(self):
        return self._status

    @property
    def type(self):
        return self._type

    @property
    def changelist(self):
        return self._changelist
