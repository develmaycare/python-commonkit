"""
Abstract
--------

`List manipulation in Python`_ may be quite advanced. The functions here provide some additional convenience for working with lists.

.. _List manipulation in Python: https://howchoo.com/g/ytezyzdlzjg/python-list

Usage
-----

any_list_item
.............

Determine whether any item in ``a`` also exists in ``b``.

.. code-block:: python

    from commonkit import any_list_item

    a = [1, 2, 3]
    b = [3, 4, 5]
    print(any_list_item(a, b))

split_csv
.........

Split a comma separated string into a list.

.. code-block:: python

    from commonkit import split_csv

    a = "1, yes, 17.5, testing"
    print(split_csv(a))

xor
...

An `exclusive or`_ operation on a list of values.

.. _exclusive or: https://en.wikipedia.org/wiki/Exclusive_or

.. note::
    The provided values *must* support casting as a ``bool``.

``xor()`` returns ``True`` when an *odd* number of values are ``True`` or ``False`` when an *even* number of values are
``True``.

.. code-block:: python

    print("TTTT", xor(True, True, True, True))
    print("TTT", xor(True, True, True))
    print("TTTF", xor(True, True, True, False))
    print("TTTFT", xor(True, True, True, False, True))
    print("FFFF", xor(False, False, False, False))

"""
from .library import *

__version__ = "0.21.0-d"
