# Imports

from ..types import smart_cast

# Exports

__all__ = (
    "any_list_item",
    "split_csv",
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
