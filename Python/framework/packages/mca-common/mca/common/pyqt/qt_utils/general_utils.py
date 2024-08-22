"""
Module that contains Test tool implementation.
"""

# System global imports
# Software specific imports
# PySide2 imports
# mca python imports


def delete_layout_and_children(parent_layout, layout_to_remove):
    delete_items_of_layout(layout_to_remove)
    for i in range(parent_layout.count()):
        layout_item = parent_layout.itemAt(i)
        if layout_item.layout() == layout_to_remove:
            parent_layout.removeItem(layout_item)
            return


def delete_items_of_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                delete_items_of_layout(item.layout())


def get_qwidget_text(qwidget_list):
    """
    Returns the text for each QWidget listed
    
    :param list(QWidget) qwidget_list:
    :return:  Returns the text for each QWidget listed
    :rtype: list(str)
    """
    
    if not isinstance(qwidget_list, (tuple, list)):
        qwidget_list = [qwidget_list]
        
    text = []
    for qwidget in qwidget_list:
        text.append(qwidget.text())
    return text

