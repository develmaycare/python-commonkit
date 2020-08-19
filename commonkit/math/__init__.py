"""
Abstract
--------

The helper functions here are simply shortcuts for common math calculations, wrapped in try/except. This makes the operation more expressive, easier to remember, and also saves repetitive exception catching code.

Usage
-----

add
...

Like the ``sum`` builtin, but numbers may be of different types.

.. code-block:: python

    from commonkit import add

    s = add([1, 1.1, 1.2])
    print(s)

average
.......

Calculate the average of a given number of values, taking care to handle zero division.

.. code-block:: python

    from commonkit import average

    values = [1, 2, 3, 4, 5]
    print(average(values))

median
......

Calculate the median of number values. The need not be of the same type.

.. code-block:: python

    from commonkit import median
    m = median([1, 3, 5, 7])
    print(m)

percentage
..........

Calculate the percentage that a portion makes up of a total.

.. code-block:: python

    from commonkit import percentage

    p = percentage(50, 100)
    print(p + "%")

product
.......

Multiple numbers.

.. code-block:: python

    from commonkit import product

    p = product([5, 5])
    print(p)

"""
from .library import *

__version__ = "0.21.0-d"
