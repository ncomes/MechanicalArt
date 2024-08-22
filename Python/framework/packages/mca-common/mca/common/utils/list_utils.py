"""
Functions related to lists
"""

# python imports
from collections import Counter
# software specific imports
# mca python imports
from mca.common import log

logger = log.MCA_LOGGER


def force_list(var):
    """
    Returns the given variable as list.

    :param object var: object we want to convert to list
    :return: object as list.
    :rtype: list(object)
    """

    if var is None:
        return list()

    if type(var) is not list:
        if type(var) in [tuple]:
            var = list(var)
        else:
            var = [var]

    return var


def force_tuple(var):
    """
    Returns the given variable as list.

    :param object var: object we want to convert to tuple
    :return: object as tuple.
    :rtype: tuple(object)
    """

    if var is None:
        return ()

    if type(var) is not tuple:
        var = tuple(var)

    return var


def index_exists_in_list(items_list, index):
    """
    Returns whether given index exists in given list.

    :param list or tuple items_list: iterable list of items.
    :param int index: index to check.
    :return: True if given index exists within the iterable object; False otherwise.
    :rtype: bool
    """

    return (0 <= index < len(items_list)) or (-len(items_list) <= index < 0)


def get_duplicates(iterable):
    """
    Returns all the duplicate values in the given iterable object.

    :param iterable iterable: sequence of possible duplicates.
    :return: list of duplicated values.
    :rtype: list(object)
    """

    seen = set()
    dups = list()
    for i in iterable:
        if i in seen:
            dups.append(i)
        seen.add(i)

    return dups


def get_most_common_item_in_list(iterable):
    """
    Returns the most common item in given list.

    :param list iterable: list to retrieve most common item from.
    :return: found most common item.
    :rtype: any
    """

    data = Counter(iterable)
    return max(iterable, key=data.get)


def pairwise(iterable):
    """
    Loops the given iterable returning pairs of elements as tuple.
    (s0, s1), (s2, s3), (s4, s5), ...

    :param iterable:
    :return: tuple of two elements from iterable.
    """

    a = iter(iterable)
    return zip(a, a)


def get_index_in_list(list_arg, index, default=None):
    """
    Returns the item at given index. If item does not exist, returns default value.

    :param list(any) list_arg: list of objects to get from.
    :param int index: index to get object at.
    :param any default: any value to return as default.
    :return: any
    """

    return list_arg[index] if list_arg and len(list_arg) > abs(index) else default


def get_first_in_list(list_arg, default=None):
    """
    Returns the first element of the list. If list is empty, returns default value.

    :param list(any) list_arg: An empty or not empty list.
    :param any default: If list is empty, something to return.
    :return: Returns the first element of the list.  If list is empty, returns default value.
    :rtype: any
    """

    return get_index_in_list(list_arg, 0, default=default)


def get_last_in_list(list_arg, default=None):
    """
    Returns the last element of the list. If list is empty, returns default value.

    :param list(any) list_arg: An empty or not empty list.
    :param any default: If list is empty, something to return.
    :return: Returns the last element of the list.  If list is empty, returns default value.
    :rtype: any
    """

    return get_index_in_list(list_arg, -1, default=default)


def flatten_list(list_arg):
    """
    Returns a flattened list that has nested lists.

    :param list(Any) list_arg: A list with nested lists.
    :return: Returns a flattened list that has nested lists.
    :rtype: List(Any)
    """

    result = lambda *n: (e for a in n for e in (result(*a) if isinstance(a, (tuple, list)) else (a,)))
    return list(result(list_arg))


def set_list_value_at(initial_list, index, value, buffer_value=None):
    """
    Sets a value into a list at an arbitrary index, buffering the list size until it meets that length.
    If the index value is negative it will buffer the start of the list until it could set a value at that index.

    IE:
    initial_list = [2,3]
    index = -2
    value = 0
    result [0, None, 2, 3]

    :param list initial_list: The list to set the value into.
    :param int index: The index at which to set that value.
    :param any value: The value to set into the list at that index
    :param any buffer_value: The value which should be used to buffer the list entries if it is not long enough.
    :return: The modified list.
    :rtype: list
    """

    if not isinstance(index, int):
        raise IndexError('Index must be an int')

    if index < 0:
        # If we use a negative index value
        # Add values to the front of the list until we could set that index relative to the original list.
        buffer_length = abs(index)
        index = 0
        buffer_list = [buffer_value for x in range(buffer_length)]
        initial_list = buffer_list + initial_list
    elif len(initial_list) <= index:
        # If the list is shorter than our desired index value
        # Add values to the list until we have one long enough to set at that index.
        buffer_length = index + 1 - len(initial_list)
        buffer_list = [buffer_value for x in range(buffer_length)]
        initial_list = initial_list + buffer_list

    # If the list was long enough to insert at that index just do it.
    # Or once we've modified the initial list enough to accommodate it.
    initial_list[index] = value

    return initial_list