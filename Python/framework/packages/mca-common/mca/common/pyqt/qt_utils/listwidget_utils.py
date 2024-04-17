#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox main UI
"""

# mca python imports
# PySide2 imports
from PySide2.QtWidgets import QWidget
# software specific imports
# mca python imports


def select_position_qlist_widget_item(qlist_widget, index=0):
	"""
	Selects a row in the list
	:param QlistWidget qlist_widget: QlistWidget.
	:param int index: Row index.
	"""
	items = get_qlist_widget_items(qlist_widget)
	if items:
		qlist_widget.setCurrentRow(index)


def get_qlist_widget_items(qlist_widget):
	"""
	Returns all the items in a QListWidget.
	:param QlistWidget qlist_widget: QListWidget.
	:return Returns all the items in a QListWidget.
	:rtype: str
	"""
	
	q_items = []
	for index in range(qlist_widget.count()):
		q_items.append(qlist_widget.item(index).text())
	return q_items


def select_qlist_widget_item(qlist_widget, item):
	"""
	Finds an string in a list widget and selects it.
	:param QlistWidget qlist_widget: QlistWidget.
	:param string item: name of the item to be selected.
	"""
	for i in range(qlist_widget.count()):
		if qlist_widget.item(i).text() == str(item):
			qlist_widget.setCurrentRow(i)
			break


def remove_qlist_widget_items(items, qlist_widget):
	"""
	Removes items in a QListWidget.
	:param list items: list of items in the QListWidget.
	:param QlistWidget qlist_widget: QListWidget.
	"""
	all_items = []
	for index in range(qlist_widget.count()):
		all_items.append(qlist_widget.item(index).text())
	
	all_items = list(map(lambda x: str(x), all_items))
	items = list(map(lambda x: str(x), items))
	
	[all_items.remove(x) for x in items if x in all_items]
	
	qlist_widget.clear()
	qlist_widget.addItems(all_items)


def get_qlist_widget_selected_items(qlist_widget):
	"""
	Returns all the selected items in a QListWidget.
	:param QWidget qlist_widget: QListWidget.
	:return: Returns all the selected items in a QListWidget.
	:rtype: list(str)
	"""
	items = qlist_widget.selectedItems()
	selected = []
	for i in range(len(items)):
		selected.append(str(qlist_widget.selectedItems()[i].text()))
	return selected