"""
Abstract
--------

The database package contains various resources for working with data sources programmatically, including from command
line scripts or from within your own Python application.

It wraps `SQL Alchemy`_ and provides optional integration with `tablib`_.

.. _SQL Alchemy: https://www.sqlalchemy.org
.. _tablib: https://tablib.readthedocs.io/en/stable/

No ORM is provided. Instead, a database is represented as an object with various shortcuts for running queries.

Install
-------

The following will install SQLAlchemy: ``pip install[database]``

SQLite is supported by default. Specific database engines require additional, third-party packages:

- MS SQL: ``pip install commonkit[mssql]``
- Oracle: ``pip install commonkit[oracle]``
- Postgres: ``pip install commonkit[pgsql]``

.. note::
    MS SQL utilizes pyodbc which may require the installation of system libraries.

If you wish to work with tablib datasets or use the export functionality, you must also install: ``pip install tablib``

Additionally, the Excel and YAML export formats require additional packages.

.. code-block:: bash

    pip install tablib[xlsx];
    pip install tablib[yaml];

See the tablib documentation for more information.

.. note::
    Although a backend is provided for MySQL, the ``MySQL-python`` package does not yet appear to support Python 3.

Usage
-----

Connecting
..........

Use the ``load_database()`` function to connect to a database:

.. code-block:: python

    from commonkit.database import load_database

    db = load_database("sqlite", debug=True, path="path/to/my.db")

The ``debug=True`` causes queries to be printed before execution. You may also log queries instead:

.. code-block:: python

    import logging
    from commonkit.database import load_database

    log = logging.getLogger("query_log")
    db = load_database("sqlite", debug=True, log=log, path="path/to/my.db")

Specifying a Table Prefix
.........................

If you want to prefix all tables with a given database, use the ``prefix`` parameter:

.. code-block:: python

    from commonkit.database import load_database

    db = load_database("sqlite", debug=True, path="path/to/my.db", prefix="myprefix)

.. note::
    It is assumed that an underscore should be appended to the prefix.

Using Your Own Database Class
.............................

If it possible to extend the Database class to add or override methods as needed. In the example below, we deal with
custom table prefixes.

.. code-block:: python

    from commonkit.database import Database

    class MyDatabase(Database):

        def _prefix_table(self, name):
            if name in ("page", "site"):
                return "web_%s" % name

            return name

Then provide your database to the load function:

.. code-block:: python

    from commonkit.database import load_database

    db = load_database("sqlite", database_class=MyDatabase, path="path/to/my.db")

Common CRUD
...........

Create, Read, Update, and Delete are supported.

**Create/Insert**

.. code-block:: python

    values = {
        'title': "Page 1",
        'body': "This is page 1.",
    }
    result = db.insert("page", values)
    print("Last ID: %s" % result.last_id)

**Read/Select**

.. code-block:: python

    result = db.select("page", limit=10, order_by="title")
    print(result.rows)

**Update**

.. code-block:: python

    values = {
        'title': "Page 1 - Popular!",
        'popularity': 3.0,
    }
    result = db.update("page", values, id=1)
    print(result.success)

**Delete**

.. code-block:: python

    result = db.delete("page", id=1)
    print(db.success)

Aggregation
...........

.. code-block:: python

    result = db.average("popularity", "page")
    print(result.aggregate)

    result = db.count("page")
    print(result.aggregate)

    result = db.max("popularity", "page")
    print(result.aggregate)

    result = db.min("popularity", "page")
    print(result.aggregate)

    result = db.sum("popularity", "page")
    print(result.aggregate)

Using Expressions
.................

Aggregate queries as well as ``delete()``, ``select()``, and ``update()`` support a simple expressions system.

.. code-block:: python

    from commonkit.database import Expression

    result = db.select("page", popularity=Expression(">=", 2.0)

Raw Queries
...........

The ``raw()`` method allows any query to be executed as is. For example, to create or remove tables, or run complex
queries that are not easily presented to ``select()``.

Lazy Loading
............

When using a Database instance, all rows are loaded by default. Lazy loading is possible, though, with a bit more code:

.. code-block:: python

    db.backend.connect()
    with db.backend.get_session() as session:
        result = session.query("SELECT * FROM mytable;")
        try:
            row = result.rows.next()
        except StopIteration:
            pass

    db.backend.disconnect()

This is because the ``select()`` method passes ``lazy=False`` to ``session.query()``. Above we allow the default of
``lazy=True`` and take control of dealing with the rows while the database connection is still open.

Results
.......

The ``fetch()`` method of the Database returns a :py:class:`commonkit.database.library.Row` instance or raises
`MultipleObjectsReturned` or `ObjectDoesNotExist`.

All other methods of the Database class will return a :py:class:`commonkit.database.library.Result` instance. This
encapsulates various aspects of a query:

Properties that are always available:

- ``bindings``: The original bindings, if any, used to execute the query.
- ``error``: The error message, if one was encountered. Otherwise, ``None``.
- ``statement``: The query string.
- ``success``: ``True`` or ``False`` indicating whether the query was successful. Note that this indicates whether
  the query was executed without identifiable problems, but does *not* qualify the results.

The possible properties are:

- ``aggregate``: The return value of an aggregate query.
- ``count``: The number of rows affected or returned.
- ``last_id``: The last ID that was part of an ``insert()`` operation. Otherwise, ``None``.
- ``rows``: From a ``select()`` operation, this will be a :py:class:`commonkit.database.library.Set` instance.
  Otherwise, ``None``.

Working With Sets
.................

The ``result.rows`` is a :py:class:`commonkit.database.library.Set` instance which contains a collection of
:py:class:`commonkit.database.library.Row` instances. You may iterate over these rows:

.. code-block:: python

    for row in result.rows:
        # ...

A set may be converted into a ``tablib.Dataset`` (if tablib is installed) or a list of dictionaries or ordered
dictionaries -- using ``as_dataset()``, ``as_dict()``, and ``as_ordered_dict)`` respectively.

If tablib is installed you may also export the set to CSV and JSON. Exports to YAML and Excel are supported if you've
installed the dependencies.

.. code-block:: bash

    pip install tablib[xlsx];
    pip install tablib[yaml];

The ``EXPORT_FORMAT`` constant is provided to reduce errors:

.. code-block:: python

    from commonkit.database.constants import EXPORT_FORAMT

    print(result.rows.export(output_format=EXPORT_FORMAT.JSON)

    with open('export.xlsx', 'wb') as f:
        f.write(result.rows.export(EXPORT_FORMAT.EXCEL))
        f.close()

Working With a Row
..................

A :py:class:`commonkit.database.library.Row` represents an individual row from a table in the database. The fields are
available as attributes.

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS web_page (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent INTEGER,
        title VARCHAR(128) NOT NULL,
        type VARCHAR(64) DEFAULT 'page',
        draft BOOL DEFAULT 1,
        body TEXT,
        published_dt VARCHAR(32),
        display_date VARCHAR(10),
        popularity REAL,
        FOREIGN KEY (parent) REFERENCES page(web_page_id)
    );

So, for example, a row selected from the table above would have an attribute called ``title`` and would be accessible as
``row.title``.

The instance also supports all of the conversion and export functionality of Set described above.

Notes
-----

The Life Cycle of a Query
.........................

.. note::
    This section is for the curious. All operations may be handled by a Database instance acquired from
    ``load_database()``.

The overall processing of a query is as follows:

1. A backend is instantiated and supplied to a Database instance. An unsupported (or simply misspelled backend) will
   raise an ``UnknownDatabaseBackend`` error internally and ``load_database()`` will return ``None``. The engine is
   initialized immediately, which may result in an error if the appropriate dependencies are not installed. However, a
   connection is *not* attempted at this time.
2. When a Database method is called, it assembles the query and creates a :py:class:`commonkit.database.library.Query`
   instance. The ``run()`` method of this instance is called which connects to the database and opens a
   :py:class:`commonkit.database.library.Session`.
3. Aggregate queries use the ``aggregate()`` method of Session. Select queries use the ``query()`` method, and all other
   operations use the ``raw()`` method. Each method attempts to execute the query and captures any errors. The ``raw()``
   runs within a database transaction. A :py:class:`commonkit.database.library.Result` instance is created and
   returned back to the Query instance.
4. The Query instance then closes the database connection and returns the Result instance.
5. The result instance (described above) contains all the information about the query, including any error encountered.

Alternatives
------------

This component was inspired by `python-records`_ and uses some of the same conventions and resources.

.. _python-records: https://github.com/kennethreitz-archive/records

"""
from .factory import load_database
from .library import Database, Expression

__version__ = "0.7.0-x"
