"""
Abstract
--------

Working with files containing comma-separated values (CSV) is quite common. Python's csv library provides an excellent
resource for working such files in various dialects. This component wraps that library to provide additional
convenience.

Usage
-----

Mapping Column Names
....................

Consider a CSV whose first row is ...

``First Name,Last Name,Job Title,Salary``

You may use the :py:class:`commonkit.csv.library.KeywordMapping` to change these columns to a Pythonic value such
as ``first_name``, etc.

.. code-block:: python

    from commonkit.csv import CSVFile, KeywordMapping

    keywords = KeywordMapping(
        first_name="First Name",
        last_name="Last Name",
        job_title="Job Title",
        salary="Salary"
    )
    csv = CSVFile("path.csv", mapping=keywords)
    csv.read()

    print(csv.rows)

This produces something like:

.. code-block:: python

    [
        {'first_name': 'Bob', 'last_name': 'White', 'job_title': 'CEO', 'salary': '125000'},
        {'first_name': 'Ed', 'last_name': 'Edwards', 'job_title': 'CIO', 'salary': '120000'},
        {'first_name': 'Jack', 'last_name': 'Jackson', 'job_title': 'CFP', 'salary': '12000'}
    ]

Auto Mapping CSV Column Names
.............................

Field names may also be auto-mapped to columns. This automatically converts things like ``First Name`` to ``first_name``
but is not explicit as with the keyword mapping above.

.. code-block:: python

    from commonkit.csv import AutoMapping, CSVFile

    auto = AutoMapping()
    csv = CSVFile("path.csv", mapping=auto)
    csv.read()

    print(csv.rows)

Mapping Column Indexes to Names
...............................

Another common scenario is when the CSV file has no column row. In such cases, it is possible to map fields using the
:py:class:`commonkit.csv.library.IndexMapping`.

.. code-block:: python

    from commonkit.csv import CSVFile, IndexMapping

    indexes = IndexMapping(
        first_name=0,
        last_name=1,
        job_title=2,
        salary=3
    )
    csv = CSVFile("path.csv", mapping=indexes)
    csv.read()

    print(csv.rows)

This produces the same results as keyword and auto mapping even when there is no column row.

Working With Object-Oriented Rows
.................................

Use the :py:class:`commonkit.csv.library.CSVRow` (or another class) to work with rows as objects rather than lists or
dictionaries.

.. code-block:: python

    from commonkit.csv import AutoMapping, CSVFile, CSVRow

    auto = AutoMapping()
    csv = CSVFile("path.csv", mapping=auto, row_class=CSVRow)
    csv.read()

    for row in csv:
        print("Name: %s %s" % (row.first_name, row.last_name)
        print("Title: %s" % row.title)
        print("Salary: %s" % row.salary)
        print("")

Handling Empty Values
.....................

By default the :py:class:`commonkit.csv.library.CSVFile` defines a number of values that are considered to be ``None``
rather than accepted as is. To override this behavior, supply ``none_type_values`` upon instantiation.

.. code-block:: python

    from commonkit.csv import AutoMapping, CSVFile

    auto = AutoMapping()
    csv = CSVFile("path.csv", mapping=auto, none_type_values=["NA", "...", "--"])
    csv.read()

Handling Default Values
.......................

You may use the ``defaults`` parameter upon instantiation to set default values. These values are used any time a value
is not provided.

.. code-block:: python

    from commonkit.csv import AutoMapping, CSVFile

    auto = AutoMapping()
    defaults = {
        'job_title': "Unspecified",
        'salary': 95000,
    }
    csv = CSVFile("path.csv", mapping=auto)
    csv.read()

Casting Data to Python Types
............................

It is possible to convert data from a CSV to the appropriate Python data type.

.. code-block:: python

    from commonkit.csv import AutoMapping, CSVFile

    auto = AutoMapping()
    csv = CSVFile("path.csv", mapping=auto, smart_cast_fields=["salary"])
    csv.read()

Using our previous CSV examples, the code above will automatically convert *salary* to an integer.

You may also specify a callback for casting data. This takes the form of ``callable(field_name, row, value)``.

The ``field_name`` and ``row`` provide additional context that may be used to cast ``value``.

.. code-block:: python

    from decimal import getcontext, Decimal
    from commonkit.csv import AutoMapping, CSVFile

    getcontext().prec = 2

    def cast_salary(field_name, row, value):
        return Decimal(value)

    auto = AutoMapping()
    casts = {
        'salary': cast_salary,
    }
    csv = CSVFile("path.csv", mapping=auto, smart_cast_fields=casts)
    csv.read()

Note that when supplying ``smart_cast_fields`` as a dictionary, fields without a callback should use ``None``.

.. code-block:: python

    casts = {
        'salary': cast_salary,
        'some_other_field': None,
    }

"""
from .library import *

__author__ = "Shawn Davis <shawn@develmaycare.com>"
__maintainer__ = "Shawn Davis <shawn@develmaycare.com>"
__version__ = "0.3.0-x"

__all__ = (
    "AutoMapping",
    "CSVFile",
    "CSVRow",
    "IndexMapping",
    "KeywordMapping",
)
