"""
Abstract
--------

Working with Python types, especially at runtime when a given variable type is unknown, is an essential programming
activity. This types module provides flexible type detection and "smart" casting to dynamically coerce data to the most
appropriate type.

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

is_decimal
..........

Determine if a given value is a decimal number.

.. code-block:: python

    from commonkit import is_decimal

    assert is_decimal(True) is False
    assert is_decimal("asdf") is False
    assert is_decimal("17") is True
    assert is_decimal(17) is True
    assert is_decimal(17.17) is True
    assert is_decimal(17.17000) is True

.. important::
    Float and integer values will return a positive match, so (if it matters), first call ``is_float()`` or
    ``is_integer()`` to determine if the value is one of those types.

is_email
........

Determine if a given value is a valid email address.

.. code-block:: python

    from commonkit import is_email

    print(is_email("bob@bob"))
    print(is_email("bob@bob.com"))

is_empty
........

Determine whether a string is empty or a blank space.

.. code-block:: python

    from commonkit import is_empty

    print(is_empty(""))
    print(is_empty(" "))

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

is_magic_name
.............

Indicates whether a given string is a valid Python magic name, e.g. ``__name__``.

.. code-block:: python

    from commonkit import is_magic_name

    print(is_magic_name("_testing"))
    print(is_magic_name("__testing__"))

is_nothing
...........

Indicates whether a variable has any appreciable value. This will return ``True`` for integers an floats that are zero,
for zero-length strings, and for ``None``.

.. code-block:: python

    from commonkit import is_nothing

    var = ""
    print(is_nothing(var))

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

is_variable_name
................

Indicates whether a given string is a valid Python variable name.

.. code-block:: python

    from commonkit import is_variable_name

    print(is_variable_name("123"))
    pritn(is_variable_name("testing123"))

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

to_decimal
..........

Convert a value to a decimal number.

.. code-block:: python

    from commonkit import to_decimal

    print(to_decimal("17.0001"))

to_ordered_dict
...............

Given a dictionary with simple key/value pairs, sort the values into an ``OrderedDict``.

.. code-block:: python

    from commonkit import to_ordered_dict

to_timedelta
............

Convert a given string to a timedelta.

.. code-block:: python

    from commonkit import to_timedelta

    print(to_timedelta("1d 4h"))
    print(to_timedelta("1h 15m"))
    print(to_timedelta("1m10s"))

smart_cast
..........

Intelligently cast the given value to a Python data type.

.. code-block:: python

    from commonkit import smart_cast

    value = "123"
    print(type(smart_cast(value)), smart_cast(value))

    value = "yes"
    print(type(smart_cast(value)), smart_cast(value))

BooleanBecause
..............

The ``BooleanBecause`` class provides a boolean value with an optional cause or description of the ``True`` or ``False``
value.

.. code-block:: python

    from commonkit import BooleanBecause

    value = BooleanBecause(False, because="it's just not true.")
    print(value)

There are two convenience classes that extend ``BooleanBecause``: ``FalseBecause`` and ``TrueBecause``. These
automatically set the internal value to ``False`` and ``True`` respectively while still accepting the optional
``because`` parameter.

DoesNotInstantiate
..................

The ``DoesNotInstantiate`` class may be extended to prevent any class from be instantiated. This can be useful for
settings and class-based constants.

.. code-block:: python

    from commonkit import DoesNotInstantiate

    class MYSETTINGS(DoesNotInstantiate):
        # ...

"""
from .library import *

__version__ = "0.30.0-d"
