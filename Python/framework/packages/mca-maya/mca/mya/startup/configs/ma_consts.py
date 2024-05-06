#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports

# software specific imports

# mca python imports


# Environment Variables Names


FRAG_NODE_PACKAGE_PATHS = ['frag_node']

TOOLS_PATH = 'MCA_MAYA_TOOLS_PATH'
CONFIGS_PATH = 'MCA_MAYA_CONFIGS_PATH'
DEPS_ROOT = 'MCA_MAYA_DEPS_PATH'
STUDIOLIBRARY = 'MCA_STUDIO_LIBRARY_PATH'
THRIDPARTY = 'MCA_THIRDPARTY_PATH'
POSE_WRANGLER = 'MCA_POSE_WRANGLER'

PARENT_SEPARATOR = '|'
SIDE_LABELS = ['Center', 'Left', 'Right', 'None']       # order is important
JOINT_TYPE_LABELS = [
    'None', 'Root', 'Hip', 'Knee', 'Foot', 'Toe', 'Spine', 'Neck', 'Head', 'Collar', 'Shoulder', 'Elbow', 'Hand',
    'Finger', 'Thumb', 'PropA', 'PropB', 'PropC', 'Other', 'Index Finger', 'Middle Finger', 'Ring Finger',
    'Pinky Finger', 'Extra Finger', 'Big Toe', 'Index Toe', 'Middle Toe', 'Ring Toe', 'Pinky Toe', 'Foot Thumb'
]