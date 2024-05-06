#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for mca-package
"""

# mca python imports

# software specific imports
import unreal
# mca python imports


def get_content_browser_selection():
    eul = unreal.EditorUtilityLibrary()
    
    selected_asset = eul.get_selected_assets()
    
    for selection in selected_asset:
        print(selection)
    return selected_asset

