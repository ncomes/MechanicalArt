#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Purpose: Creates an ikfk switch
"""

# System global imports
# python imports
import pymel.core as pm
#  python imports
from mca.mya.rigging.flags import tek_flag
from mca.mya.utils import attr_utils


def ikfk_switch(switch_joint,
                side,
                region,
                switch_attr_name='ikfk_switch',
                scale=1.0):

    switch_flag = tek_flag.Flag.create(switch_joint,
                                    label='{0}_{1}_ikfk_switch'.format(side, region),
                                    scale=scale*.5,
                                    add_align_transform=True)
    pm.addAttr(switch_flag, ln=switch_attr_name, k=True, at='double', min=0, max=1, dv=1)

    invert_node = attr_utils.invert_attribute("{0}.{1}".format(switch_flag, switch_attr_name))
    pm.rename(invert_node, "{0}_{1}_switch_invert_node".format(side, region))

    pm.pointConstraint(switch_joint, switch_flag.get_align_transform(), w=1, mo=1)
    pm.orientConstraint(switch_joint, switch_flag.get_align_transform(), w=1, mo=1)

    # create dictionary
    return_dictionary = {}
    return_dictionary['invert_node'] = invert_node
    return_dictionary['flag'] = switch_flag
    return_dictionary['name'] = switch_attr_name

    return return_dictionary

