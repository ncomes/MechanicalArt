#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# python imports
import pymel.core as pm
# software specific imports
#  python imports
from mca.common.utils import fileio


def touch_and_checkout_cmd(plastic_checkout=True, remove=False):
    """
    Attempts to check out the file in plastic.

    :param bool plastic_checkout: If True, it will attempt to check out the file in plastic.
    :param bool remove: If the file should be removed if it exists.
    """
    
    sn = pm.sceneName()
    fileio.touch_and_checkout(sn, plastic_checkout=plastic_checkout, remove=remove)
    
