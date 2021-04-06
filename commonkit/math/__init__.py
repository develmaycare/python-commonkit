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

difference
..........

Calculate the percentage difference between two numbers.

.. code-block:: python

    from commonkit import difference

    v1 = 1000
    v2 = 1200
    print(difference(v1, v2))

factors_of
..........

Get the factors of a given integer. A ``TypeError`` is raised if the number is *not* an integer.

.. code-block:: python

    from commonkit import factors_of

    print(factors_of(10))
    print(factors_of(17))

is_prime
........

Determine whether a given number is a prime number. Note that a non-integer will always return ``False``.

.. code-block:: python

    from commonkit import is_prime

    print(is_prime(10))
    print(is_prime(17))

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

__version__ = "0.23.0-d"
