#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loads the mya package and all the env variables.
"""

# mca python imports
import os
import sys
import logging
# software specific imports
# mca python imports
from mca.dccdata.paths import project_paths


logger = logging.getLogger('MCA_DCC_DATA')


def startup_init(skip_dialog=False):
    """
    Initializes MAT DCC Data Packages.
    """
    
    print('Starting startup!')
    if not skip_dialog:
        logger.info('Creating MAT Python DCC Data Window framework environment ...')
        print("""
          MAT DCC DATA Startup""")
        print('\n' + '=' * 118 + '\n')
    
    dependencies_path = project_paths.get_dependencies_path()
    sys.path.append(dependencies_path)
    print('Dependencies Path has been registered!')
    
    os.environ['PYTHONPATH'] = dependencies_path
    

    
    print('\n' + '=' * 118 + '\n')


def shutdown(skip_dialog=False):
    """

    :param bool skip_dialog: If True, nothing will be written to the console.
    """
    pass
    if not skip_dialog:
        logger.info('\n' + '=' * 160 + '\n')



