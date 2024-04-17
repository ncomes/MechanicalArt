#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions related with sounds.
"""

# mca python imports
import os

WINSOUND_AVAILABLE = True
try:
	import winsound
except ModuleNotFoundError:
	WINSOUND_AVAILABLE = False

# software specific imports
# mca python imports
from mca.common.paths import paths


def play_sound(sound_file):
	"""
	Plays a simple WinSound.

	:param str sound_file: Name of a wav file in Common\Sounds directory.
	"""

	if not WINSOUND_AVAILABLE:
		return

	wave_file = os.path.join(paths.get_commond_sounds(), sound_file)
	winsound.PlaySound(wave_file, winsound.SND_ASYNC)


def sound_warning():
	"""
	Plays a warning sound.  Used for Warning or Warning Dialogs.
	"""

	play_sound('Windows Error.wav')


def sound_critical_stop():
	"""
	Plays a Critial Warning sound.  Used for Critical Errors.
	"""

	play_sound('Windows Critical Stop.wav')


def sound_ding():
	"""
	Plays a quick alert sound.  Used to grab attention on a minor subject.
	"""

	play_sound('Windows Ding.wav')


def sound_tada():
	"""
	Plays a Tada sound.  I mean... Why not?.
	"""

	play_sound('tada.wav')


def sound_recycle():
	"""
	Plays a recycle sound.  Sounds like crumpling paper.
	"""

	play_sound('recycle.wav')


def sound_recycle2():
	"""
	Plays a recycle sound.  Sounds like crumpling paper.
	"""

	play_sound('Windows Recycle.wav')


def sound_notify():
	"""
	Plays a notify sound.  Used to grab attention on a minor subject.
	"""

	play_sound('notify.wav')


def sound_battery_low():
	"""
	Plays a low battery sound.  Used to grab attention on a minor subject.
	"""

	play_sound('Windows Battery Low.wav')
