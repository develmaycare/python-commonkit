# Imports

from functools import reduce
from ..types import smart_cast

# Exports

__all__ = (
    "any_list_item",
    "filter_by",
    "flatten",
    "safe_join",
    "sort_by",
    "split_csv",
    "strange",
    "xor",
    "Loop",
)

# Functions


def any_list_item(a, b):
    """Determine whether any item in ``a`` also exists in ``b``.

    :param a: The first list to be compared.
    :type a: list

    :param b: The second list to be compared.
    :type b: list

    :rtype: bool

    """
    for i in a:
        for j in b:
            if i == j:
                return True

    return False


def filter_by(attribute, iterable, values):
    """Filter an iterable based on the value of an attribute.

    :param attribute: The name of the attribute by which the iterable is filtered. This must exist as an attribute on
                      each instance within the iterable or as a dictionary key if the iterable contains dictionaries.
                      The attribute itself may be list or tuple.
    :type attribute: str

    :param iterable: An iterable (such as a list or tuple).

    :param values: The values to be matched. The type of each value must be the same as the type of the attribute. This
                   may be given as a list, tuple, str, integer, float, or bool.

    :returns: A list of iterable instances that been filtered.

    """
    if type(values) in (list, tuple):
        _values = values
    else:
        _values = [values]

    filtered = list()
    for i in iterable:

        # Get the actual value of attribute.
        if type(i) is dict:
            attr = i[attribute]
        else:
            attr = getattr(i, attribute)

        if type(attr) in (list, tuple):
            include = any_list_item(attr, _values)
        elif attr in _values:
            include = True
        else:
            include = False

        if include:
            filtered.append(i)

        # if attr not in _values:
        #
        # if type(attr) in (list, tuple) and not any_list_item(attr, _values):
        #     print("attr no match", attr, _values)
        #     continue
        # elif attr not in _values:
        #     continue
        # else:
        #     filtered.append(i)

    return filtered


def flatten(iterable):
    """Flatten a list, tuple, or other iterable so that nested iterables are combined into a single list.

    :param iterable: The iterable to be flattened. Each element is also an interable.

    :rtype: list

    """
    iterator = iter(iterable)
    try:
        return sum(iterator, next(iterator))
    except StopIteration:
        return []


def safe_join(separator, values):
    """Safely join a list of values.

    :param separator: The separator to use for the string.
    :type separator: str

    :param values: A list or iterable of values.

    :rtype: str

    """
    _values = [str(i) for i in values]

    return separator.join(_values)


def sort_by(attribute, iterable, new=False, reverse=False):
    """Sort an iterable by an attribute of the instance (or dictionary) within the iterable.

    :param attribute: The name of the attribute by which the iterable should be sorted.
    :type attribute: str

    :param iterable: An iterable (such as a list or tuple).

    :param new: Indicates a new list should be returned. When ``False`` the list is sorted "in place".
    :type new: bool

    :param reverse: Indicates the list should be sorted in reverse.
    :type reverse: bool

    :returns: A new iterable when ``new`` is ``True``. Otherwise, ``None``.

    This is a shortcut for using lambda functions for sortation:

    .. code-block:: python

        # To sort the list in place ...
        some_list.sort(key=lambda x: x.sort_order)

        # Or to return a new list using the sorted() built-in function ...
        new_list = sorted(some_list, key=lambda x: x.sort_order)

    I can never seem to remember the lambda syntax, hence ``sort_by()`` saves me looking up
    `how to sort a list of objects based on an attribute of the objects`_?

    .. _how to sort a list of objects based on an attribute of the objects: https://stackoverflow.com/a/403426/241720

    """
    def _get_attribute_value(instance):
        if type(instance) is dict:
            return instance[attribute]

        return getattr(instance, attribute)

    if new:
        return sorted(iterable, key=_get_attribute_value, reverse=reverse)

    # iterable.sort(key=lambda x: getattr(x, attribute), reverse=reverse)
    iterable.sort(key=_get_attribute_value, reverse=reverse)


def split_csv(string, separator=",", smart=True):
    """Split a comma (or other) separated string into a list.

    :param string: The string to be split.
    :type string: str

    :param separator: The value separator.
    :type separator: str

    :param smart: Also attempt to cast the values found in the string to the appropriate Python type.
    :type smart: bool

    :rtype: list

    .. code-block:: python

        from superpython.utils import split_csv

        a = "1, yes, 17.5, testing"
        print(split_csv(a))

    """
    a = list()
    for i in string.split(separator):
        value = i.strip()
        if smart:
            value = smart_cast(value)

        a.append(value)

    return a


def strange(start, end, step=1):
    """A sensible, or *standard* range that behaves as you would expect.

    :param start: The start of the range.
    :type start: int

    :param end: The end of the range.
    :type start: int

    :param step: The increment to be applied.
    :type step: int

    :rtype: range

    """
    return range(start , end + 1, step)


def xor(*values):
    """An `exclusive or`_ operation on a list of values.

    .. _exclusive or: https://en.wikipedia.org/wiki/Exclusive_or

    :rtype: bool
    :returns: ``True`` when an odd number of values are ``True`` or ``False`` when an even number of values are
              ``True``.

    .. note::
        The provided values *must* support casting as a ``bool``.

    """
    return reduce(lambda x, y: bool(x) ^ bool(y), values)


# Classes


class Loop(object):
    """A list with a built in index."""

    def __init__(self, values):
        """Initialize a loop.

        :param values: The values to be iterated. This may be a list, tuple, or any iterable that acts as a linear
                       sequence.

        """
        self.count = 0
        self.values = values

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.values)

    def __next__(self):
        try:
            value = self.values[self.count]
            self.count += 1

            return value
        except IndexError:
            raise StopIteration

    def is_first(self):
        """Indicates the loop is on the first row.

        :rtype: bool

        """
        return self.count == 1

    def is_last(self):
        """Indicates the loop is on the last row.

        :rtype: bool

        """
        return self.count == len(self.values)
