"""
Module that contains the mca decorators at a base python level
"""

# python imports
# Qt imports
from mca.common.pyqt.pygui import qtcore
# software specific imports

# mca python imports
from mca.common import log


logger = log.MCA_LOGGER


def get_all_combobox_items(qcombobox):
	"""
	Returns all items from a QComboBox
	:param QComboBox qcombobox: QComboBox Widget.
	:return list: Returns all items from the QComboBox.
	"""
	if qcombobox.count() == 1:
		return [qcombobox.itemText(0)]
	all_items = [qcombobox.itemText(i) for i in range(qcombobox.count())]
	return all_items


def set_combobox_item(qcombobox, value):
	"""
	Set value in a QComboBox.
	:param QComboBox qcombobox: Drop down list of strings.
	:param string value: String name to be set.
	"""
	all_items = get_all_combobox_items(qcombobox)
	if not value:
		logger.warning('No Value was given to find in the given ComboBox.  '
						'Or the Value was "None"  {0}'.format(qcombobox))
		return
	
	if not all_items:
		logger.warning('The ComboBox is empty. {0}'.format(qcombobox))
		return
	if not value in all_items:
		logger.warning('The item "{0}" is not in the ComboBox {1}'.format(value, qcombobox))
		return
	qcombobox.setCurrentIndex(qcombobox.findText(value))


def set_combobox_to_index_matching_string(combo_box, string_to_match, qmatch_flag=None):
	"""
	Set the passed combobox's current index to the first index matching the string passed.

	:param qtgui.QComboBox combo_box: combo box to set
	:param str string_to_match: string to match
	:param qtcore.Qt.MatchFlag qmatch_flag: flag(s) to search by. Default is MatchFixedString (case insensitive)
	:return: True/False
	"""
	if not qmatch_flag:
		qmatch_flag = qtcore.Qt.MatchFixedString
	index = combo_box.findText(string_to_match, qmatch_flag)
	if index < 0:
		logger.info('No valid index found for string "{0}". '
						'Try adjusting the Qt.MatchFlag passed to '
						'qmatch_flag kwarg. Current : {1}'.format(string_to_match, qmatch_flag))
		return False
	combo_box.setCurrentIndex(index)
	return True

