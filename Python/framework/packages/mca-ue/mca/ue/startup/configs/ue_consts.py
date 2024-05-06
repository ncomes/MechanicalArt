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

TOOLS_PATH = 'MCA_UNREAL_TOOLS_PATH'
CONFIGS_PATH = 'MCA_UNREAL_CONFIGS_PATH'
DEPS_ROOT = 'MCA_UNREAL_DEPS_PATH'

PARENT_SEPARATOR = '|'
SIDE_LABELS = ['Center', 'Left', 'Right', 'None']       # order is important
JOINT_TYPE_LABELS = [
    'None', 'Root', 'Hip', 'Knee', 'Foot', 'Toe', 'Spine', 'Neck', 'Head', 'Collar', 'Shoulder', 'Elbow', 'Hand',
    'Finger', 'Thumb', 'PropA', 'PropB', 'PropC', 'Other', 'Index Finger', 'Middle Finger', 'Ring Finger',
    'Pinky Finger', 'Extra Finger', 'Big Toe', 'Index Toe', 'Middle Toe', 'Ring Toe', 'Pinky Toe', 'Foot Thumb'
]

MCA_INST_PREFIX = 'MI_'
UNREAL_FOLDER = 'Unreal'

MCA_SETTINGS = 'MaterialSettings'
SKINDUAL = 'M_CharacterSkinDual_Master'
MST_CHARACTER = 'M_CharacterMaster'
MST_EYE = 'M_CharacterEyeBall_Master'
MST_EYE_OCC_BLUR = 'M_CharacterEyeOccBlur_Master'
MST_EYE_WET = 'M_CharacterEyeWet_Master'
MST_HAIR = 'M_CharacterHair_Master'

TEXTURE_TYPES = ['d', 'n', 'nb', 'orme', 'sstd', 'r', 'rida']

DEFAULT_MATERIAL = 'WorldGridMaterial'
PLAIN_MATERIALS = ['MI_PlainColor_Blue',
                  'MI_PlainColor_Green',
                  'MI_PlainColor_Olive',
                  'MI_PlainColor_Orange',
                  'MI_PlainColor_Purple']

