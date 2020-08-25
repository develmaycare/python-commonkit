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

safe_join
.........

Safely join a list of values. Each value may be of a different Python type.

.. code-block:: python

    from commonkit import safe_join

    print(safe_join(",", [1, "two", 3.4, "five"]))

sort_by
.......

Sort an iterable of objects by an attribute of the object.

Suppose you have an object with a ``sort_order`` attribute:

.. code-block:: python

    class Sortable(object):

        def __init__(self, label, sort_order):
            self.label = label
            self.sort_order = sort_order

        def __repr__(self):
            return "%s:%s" % (self.sort_order, self.label)

Now suppose you want to sort a list of Sortable instances:

.. code-block:: python

    from commonkit import sort_by

    a = [
        Sortable("five", 5),
        Sortable("two", 2),
        Sortable("one", 1),
        Sortable("four", 4),
        Sortable("three", 3),
    ]

    sort_by("sort_order", a)
    print(a[0].label)
    print(a[-1].label)

Dictionaries are also supported:

.. code-block:: python

    from commonkit import sort_by

    d = [
        {'label': "five", 'sort_order': 5},
        {'label': "two", 'sort_order': 2},
        {'label': "one", 'sort_order': 1},
        {'label': "four", 'sort_order': 4},
        {'label': "three", 'sort_order': 3},
    ]
    sort_by("sort_order", d)
    print(d[0]['label'])
    print(d[-1]['label'])

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

    from commonkit import xor

    print("TTTT", xor(True, True, True, True))
    print("TTT", xor(True, True, True))
    print("TTTF", xor(True, True, True, False))
    print("TTTFT", xor(True, True, True, False, True))
    print("FFFF", xor(False, False, False, False))

Resources
---------

- `Python Lists: An In-Depth Tutorial`_

.. _Python Lists: An In-Depth Tutorial: https://howchoo.com/g/ytezyzdlzjg/python-list

"""
from .library import *

__version__ = "0.21.0-d"
