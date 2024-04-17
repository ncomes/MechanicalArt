#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A way to interact with joint chains in rigs.
"""
# System global imports
# Software specific imports

#  python imports
from mca.common import log
# Internal module imports

logger = log.MCA_LOGGER


class SkeletonJoint(object):
	def __init__(self):
		self.root = None


class SkeletonSerialization(object):
	def __init__(self):
		self.root = None
		
	