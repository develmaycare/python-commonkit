"""
Abstract
--------

Working with Python types, especially at runtime when a given variable type is unknown, is an essential programming activity. This types module provides flexible type detection and "smart" casting to dynamically coerce data to the most appropriate type.

Usage
-----

is_bool
.......

Determine if a given value is a boolean at run time.

.. code-block:: python

    from commonkit import is_bool

    print(is_bool("yes"))
    print(is_bool(True))
    print(is_bool("No"))
    print(is_bool(False))

.. tip::
    By default, a liberal number of values are used to test. If you *just* want ``True`` or ``False``, simply pass
    ``(True, False)`` as ``test_values``.

is_email
........

Determine if a given value is a valid email address.

.. code-block:: python

    from commonkit import is_email

    print(is_email("bob@bob"))
    print(is_email("bob@bob.com"))

is_float
........

Indicates whether the given value is a float.

.. code-block:: python

    from commonkit import is_float

    print(is_float("testing"))
    print(is_float("1.2"))

is_integer
..........

Indicates whether the given value is an integer. Saves a little typing.

.. code-block:: python

    from commonkit import is_integer

    print(is_integer(17))
    print(is_integer(17.5))
    print(is_integer("17"))
    print(is_integer("17", cast=True))

is_number
.........

Indicates whether the given value is a number; a decimal, float, or integer.

.. code-block:: python

    from commonkit import is_number

    print(is_number(17))
    print(is_number(17.5))
    print(is_number(Decimal("17.50")))
    print(is_number("seventeen")

is_string
.........

Indicates whether the given value is a string. Saves a little typing.

.. code-block:: python

    from commonkit import is_string

    print(is_string("testing"))
    print(is_string("17"))
    print(is_string(17))

to_bool
.......

Convert a given value to it's boolean equivalent.

.. code-block:: python

    from commonkit import to_bool

    print(to_bool("yes"))
    print(to_bool(1))
    print(to_bool("no"))
    print(to_bool(0))

Note that an unrecognized value will raise a value error.

.. code-block:: python

    from commonkit import to_bool

    value = "not a boolean"
    try:
        print(to_bool(value))
    except ValueError:
        print('"%s" is not a boolean value.' % value)

smart_cast
..........

Intelligently cast the given value to a Python data type.

.. code-block:: python

    from commonkit import smart_cast

    value = "123"
    print(type(smart_cast(value)), smart_cast(value))

    value = "yes"
    print(type(smart_cast(value)), smart_cast(value))

Boolean Because
...............

The ``BooleanBecause`` class provides a boolean value with an optional cause or description of the ``True`` or ``False``
value.

.. code-block:: python

    from commonkit import BooleanBecause

    value = BooleanBecause(False, because="it's just not true.")
    print(value)

"""
from .library import *

__version__ = "0.25.2-d"
