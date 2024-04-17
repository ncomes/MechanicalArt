#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains REST class used by PlasticSCM
"""

from __future__ import print_function, division, absolute_import

import requests


class REST(object):

    def _get(url, *args, **kwargs):
        # response.status_code == 200
        response = requests.get(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def _post(url, *args, **kwargs):
        # response.status_code == 200
        response = requests.post(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def _put(url, *args, **kwargs):
        # response.status_code == 200
        response = requests.put(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def _patch(url, *args, **kwargs):
        # response.status_code == 200
        response = requests.patch(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def GET(url, rest=_get):
        def decorate(fn):
            fn.REST = (url, rest)
            return fn
        return decorate

    def POST(url, rest=_post):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def PUT(url, rest=_put):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def PATCH(url, rest=_patch):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate
