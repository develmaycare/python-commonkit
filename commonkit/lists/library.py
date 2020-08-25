# Imports

from functools import reduce
from ..types import smart_cast

# Exports

__all__ = (
    "any_list_item",
    "safe_join",
    "sort_by",
    "split_csv",
    "xor",
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

    This is a shortcut for using lambda functions sort sortation:

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
