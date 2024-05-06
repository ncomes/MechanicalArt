# -*- coding: utf-8 -*-

"""
UI for importing Skeletal Meshes in Unreal.
"""

# mca python imports
import os
# PySide2 imports
# software specific imports
# mca python imports
from mca.common import log
from mca.common.pyqt import common_windows
from mca.ue.assetlist import ue_assetlist

logger = log.MCA_LOGGER


class MATUnrealSKImporter(common_windows.MCAMainWindow):
    """
    UI for importing Textures and creating Material Instance Constants.
    """

    VERSION = '1.0.0'

    def __init__(self, parent=None):
        root_path = os.path.dirname(os.path.realpath(__file__))
        ui_path = os.path.join(root_path, 'ui', 'sk_importer.ui')
        super().__init__(title='Asset Importer',
                         ui_path=ui_path,
                         version=MATUnrealSKImporter.VERSION,
                         parent=parent)

        # Get the local preferences
        self.ue_asset_list = ue_assetlist.UnrealAssetListToolBox()

        ############################################
        # Signals
        ############################################

    ############################################
    # Slots
    ############################################

