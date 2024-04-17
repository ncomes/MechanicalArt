# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE.GPL.txt, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

# Client library URL: https://googleapis.dev/python/cloudkms/latest/
# Import Example for client library:
# https://cloud.google.com/kms/docs/reference/libraries#client-libraries-install-python

from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('google-cloud-kms')
