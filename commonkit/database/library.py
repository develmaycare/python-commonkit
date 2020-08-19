# Imports

from collections import OrderedDict
from contextlib import contextmanager
from commonkit.types import is_string
from sqlalchemy import text as query_to_text
from .compat import tablib
from .constants import EXPORT_FORMAT
from .exceptions import MultipleObjectsReturned, ObjectDoesNotExist, OperationalError, ProgrammingError

# exports

__all__ = (
    "Database",
    "Expression",
    "Query",
    "Result",
    "Row",
    "Session",
    "Set",
)

# Classes


class Database(object):
    """A database."""

    def __init__(self, backend, debug=False, log=None, prefix=None):
        """Initialize the database.

        :param backend: The database backend to use.
        :type backend: BaseType[commonkit.database.backends.base.Backend]

        :param debug: Indicates whether debug mode is enabled.
        :type debug: bool

        :param log: A logging instance to use rather than printing debug statements.
        :type log: logging.Logger

        :param prefix: A prefix to be added to table names.
        :type prefix: str

        """
        self.backend = backend
        self.debug = debug
        self.log = log
        self.prefix = prefix

    def __repr__(self):
        return "<%s %s:%s>" % (self.__class__.__name__, self.backend.type, self.backend.get_database_name())

    def average(self, column, table, **criteria):
        """Get the average value of a given column.

        :param column: The column name.
        :type column: str

        :param table: The table name.
        :type table: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The average value.

        """
        return self._aggregate_query(Query.AVERAGE, column, table, **criteria)

    def count(self, table, column="id", **criteria):
        """Get a count of records using a given column as key.

        :param table: The table name.
        :type table: str

        :param column: The column name.
        :type column: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The total number of matching records.

        """
        return self._aggregate_query(Query.COUNT, column, table, **criteria)

    def delete(self, table, **criteria):
        """Remove records from a table.

        :param table: The table name.
        :type table: str

        :param criteria: The criteria used to identify the records.
        :type criteria: dict

        :rtype: Result
        :returns: The query result.

        """
        # Automatically prefix the table.
        table = self._prefix_table(table)

        # Initialize a query instance.
        query = Query(self, Query.DELETE)

        # Start the query string.
        # noinspection SqlDialectInspection
        query.statement = "DELETE FROM %s" % table

        # Add criteria.
        if criteria:
            query.statement += self._build_criteria(query.bindings, **criteria)

        # End the query string.
        query.statement += ";"

        # Return the query result.
        return query.run()

    def fetch(self, table, **criteria):
        """Fetch a specific (single) record from the database.

        :param table: The table name.
        :type table: str

        :param criteria: The criteria used to identify the records.
        :type criteria: dict

        :rtype: commonkit.database.library.Row
        :raises: MultipleObjectsReturned, ObjectDoesNotExist
        """
        result = self.select(table, **criteria)
        if result.count == 0:
            raise ObjectDoesNotExist("%s object does not exist." % table)

        if result.count > 1:
            raise MultipleObjectsReturned("%s query returned multiple records." % table)

        return result.rows[0]

    def insert(self, table, values):
        """Add a record.

        :param table: The table name.
        :type table: str

        :param values: The values to be updated.
        :type values: dict

        :rtype: Result
        :returns: The query result.

        """

        # Automatically prefix the table.
        table = self._prefix_table(table)

        # Initialize a query instance.
        query = Query(self, Query.INSERT)

        # Start the query string.
        query.statement = "INSERT INTO %s" % table

        # Add column names.
        query.statement += " (%s) VALUES (" % ", ".join(values.keys())

        # Add column placeholders.
        columns = list()
        for key in values.keys():
            columns.append(":%s" % key)
        # columns = ["?"] * len(values.values())
        query.statement += ", ".join(columns)

        # Add value bindings.
        query.bindings = values

        # End the query string.
        query.statement += ");"

        # Return the query result.
        return query.run()

    def max(self, column, table, **criteria):
        """Get the maximum value of a given column.

        :param column: The column name.
        :type column: str

        :param table: The table name.
        :type table: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The maximum value.

        """
        return self._aggregate_query(Query.MAXIMUM, column, table, **criteria)

    def min(self, column, table, **criteria):
        """Get the minimum value of a given column.

        :param column: The column name.
        :type column: str

        :param table: The table name.
        :type table: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The minimum value.

        """
        return self._aggregate_query(Query.MINIMUM, column, table, **criteria)

    def raw(self, query, bindings=None):
        """Run a query as is.

        :param query: The query string.
        :type query: str

        :param bindings: The bindings if any to be passed to the backend.
        :type bindings: list

        :rtype: Result
        :returns: The query result.

        """
        if query[-1] != ";":
            query += ";"

        _query = Query(self, Query.RAW, bindings=bindings, statement=query)

        return _query.run()

    def select(self, table, columns=None, limit=None, order_by=None, **criteria):
        """Select records from a table.

        :param table: The table name.
        :type table: str

        :param columns: The columns to be selected. Defaults to ``["*"]``.
        :type columns: list[str]

        :param limit: Limit the results to this number.
        :type limit: int

        :param order_by: Order by this column or columns.
        :type order_by: str

        :param criteria: The criteria used to identify the records.
        :type criteria: dict

        :rtype: Result
        :returns: The query result.

        """
        # Automatically prefix the table.
        table = self._prefix_table(table)

        # Initialize the query.
        query = Query(self, Query.SELECT)

        # Set columns to * if None.
        if columns is None:
            columns = ["*"]

        # Start the query string.
        # noinspection SqlDialectInspection
        query.statement = "SELECT %s FROM %s" % (", ".join(columns), table)

        # Add criteria to the query.
        if criteria:
            query.statement += self._build_criteria(query.bindings, **criteria)

        # Add ordering to the query.
        if order_by is not None:
            query.statement += " ORDER BY %s" % order_by

        # Add limit to the query.
        if limit is not None:
            query.statement += " LIMIT %s" % limit

        # End the query string.
        query.statement += ";"

        # Return the query result.
        return query.run()

    def sum(self, column, table, **criteria):
        """Get the sum of a given column.

        :param column: The column name.
        :type column: str

        :param table: The table name.
        :type table: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The sum value.

        """
        return self._aggregate_query(Query.SUM, column, table, **criteria)

    def update(self, table, values, **criteria):
        """Update existing records.

        :param table: The table name.
        :type table: str

        :param values: The values to be updated.
        :type values: dict

        :param criteria: The criteria used to identify the records.
        :type criteria: dict

        :rtype: Result
        :returns: The query result.

        """
        # Automatically prefix the table.
        table = self._prefix_table(table)

        # Initialize a query instance.
        query = Query(self, Query.UPDATE)

        # Start the query string.
        query.statement = "UPDATE %s SET " % table

        # Assemble the key = value portion of the query.
        keys = list()
        for key, value in values.items():

            query.bindings[key] = value
            keys.append("%s = :%s" % (key, key))

            query.statement += ", ".join(keys)

        # Assemble the criteria portion of the query. We can't use _build_criteria() because the criteria keys may be
        # the same as a key to be updated.
        if criteria:
            query.statement += " WHERE "

            keys = list()
            for key, value in criteria.items():
                criteria_key = "c_%s" % key
                if isinstance(value, Expression):
                    keys.append("%s %s" % (key, value))
                else:
                    keys.append("%s = :%s" % (key, criteria_key))
                    query.bindings[criteria_key] = value

            query.statement += " AND ".join(keys)

        # End the query string.
        query.statement += ";"

        # Return the query result.
        query.run()
        return query.result

    def _aggregate_query(self, aggregate, column, table, **criteria):
        """Common/standard support for running aggregate queries.

        :param aggregate: The name of the aggregate command.
        :type aggregate: str

        :param column: The column name.
        :type column: str

        :param table: The table name.
        :type table: str

        :param criteria: The criteria to use, if any.
        :type criteria: dict

        :returns: The aggregated value.
        """
        # Automatically prefix the table.
        table = self._prefix_table(table)

        # Initialize a query instance.
        query = Query(self, aggregate)

        # Start the query string.
        # noinspection SqlDialectInspection
        query.statement = "SELECT %s(%s) AS agg FROM %s" % (aggregate, column, table)

        # Incorporate criteria.
        if criteria:
            query.statement += self._build_criteria(query.bindings, **criteria)

        # End the query string.
        query.statement += ";"

        # Return the query result.
        return query.run()

    # noinspection PyMethodMayBeStatic
    def _build_criteria(self, bindings, **criteria):
        """Build criteria into a WHERE string.

        :param bindings: The bindings into which criteria values are organized.
        :type bindings: dict

        :param criteria: The criteria used to build the string.
        :type criteria: dict

        :rtype: str

        """
        statement = " WHERE "

        keys = list()
        for key, value in criteria.items():
            if isinstance(value, Expression):
                keys.append("%s %s" % (key, value))
            else:
                keys.append("%s = :%s" % (key, key))
                bindings[key] = value

        statement += " AND ".join(keys)

        return statement

    def _prefix_table(self, name):
        """Prefix the given table name (or not).

        :param name: The name of the table.
        :type name: str

        :rtype: str

        """
        if self.prefix is not None:
            return "%s_%s" % (self.prefix, name)

        return name


class Expression(object):
    """Create advanced bindings to be converted to SQL."""

    def __init__(self, condition, value):
        """Initialize the expression.

        :param condition: The condition to be applied. For example, ``>=``.
        :type condition: str

        :param value: The value to be matched by the condition.

        """
        # self.column = column
        self.condition = condition
        self.value = value

    def __str__(self):
        if is_string(self.value):
            return "%s '%s'" % (self.condition, self.value)

        return "%s %s" % (self.condition, self.value)


class Query(object):
    """Represents a database query, allowing the statement to be built programmatically."""

    AVERAGE = "avg"
    COUNT = "count"
    DELETE = "delete"
    INSERT = "insert"
    MAXIMUM = "max"
    MINIMUM = "min"
    RAW = "raw"
    SELECT = "select"
    SUM = "sum"
    UPDATE = "update"

    def __init__(self, db, op, bindings=None, model=None, statement=None):
        """Initialize a query.

        :param db: The database instance.
        :type db: Database

        :param op: The type of query. Use an appropriate class attribute of ``Query``.
        :type op: str

        :param model: The model class to use for ``select()`` results.

        :param statement: The query statement. May be supplied as ``None``, but *must* be provided before ``run()``.
        :type statement: str

        """
        self.bindings = bindings or dict()
        self.db = db
        self.model = model
        self.op = op
        self.result = None
        self.statement = statement

    @property
    def is_aggregate(self):
        """Indicates whether this is an aggregate query.

        :rtype: bool

        """
        aggregates = (
            self.AVERAGE,
            self.COUNT,
            self.MAXIMUM,
            self.MINIMUM,
            self.SUM,
        )
        return self.op in aggregates

    def run(self):
        """Run the query.

        :rtype: superpthon.database.library.Result

        .. important::
            The ``run()`` method opens the database connection, processes the result, and closes the database
            connection.

        """
        # Print the query and bindings when debug is enabled.
        if self.db.debug:
            message = "%s | %s" % (self.statement, self.bindings)
            if self.db.log is not None:
                self.db.log.info(message)
            else:
                print("[DEBUG] %s" % message)

        if not self.db.backend.is_open:
            self.db.backend.connect()

        with self.db.backend.get_session() as session:
            if self.is_aggregate:
                result = session.aggregate(self.statement, **self.bindings)
            elif self.op == self.SELECT:
                result = session.query(self.statement, lazy=False, **self.bindings)
            else:
                result = session.raw(self.statement, **self.bindings)

        self.db.backend.disconnect()

        self.result = result

        return result


class Result(object):
    """Encapsulates the result of a query, populating attributes as appropriate.

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

    """

    def __init__(self, statement, aggregate=None, bindings=None, count=None, error=None, last_id=None, rows=None,
                 success=None):
        """Initialize a result.

        :param statement: The original query.
        :type statement: str

        :param aggregate: The value of an aggregate query.
        :type aggregate: float | int

        :param bindings: The bindings applied to the query.
        :type bindings: dict

        :param count: The number of rows returned or effected.
        :type count: int

        :param error: The error encountered, if any, when executing the query.
        :type error: str

        :param last_id: The last ID generated from an insert.
        :type last_id: int

        :param rows: The rows acquired from a select.
        :type rows: commonkit.database.library.Set

        :param success: Indicates success (``True``) or failure (``False``).
        :type success: bool

        """
        self.aggregate = aggregate
        self.bindings = bindings
        self.count = count
        self.error = error
        self.last_id = last_id
        self.rows = rows
        self.statement = statement
        self.success = success

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.statement)


class Row(object):
    """A row from a database."""
    
    __slots__ = ("_attributes", "_values")

    def __init__(self, attributes, values):
        """Initialize a row.

        :param attributes: The attribute (colum/field) names of the row.
        :type attributes: tuple[str]

        :param values: The values of the row.

        """
        self._attributes = attributes
        self._values = values

        assert len(self._attributes) == len(self._values)

    def __dir__(self):
        standard = dir(super(Row, self))
        return sorted(standard + [str(k) for k in self.attributes()])

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, item):  # pragma: no cover
        # Is this necessary?
        if isinstance(item, int):
            return self.values()[item]

        if item in self.attributes():
            index = self.attributes().index(item)
            if self.attributes().count(item) > 1:
                raise KeyError("The data has multiple fields named: %s" % item)

            return self.values()[index]

        raise KeyError("Invalid field name: %s" % item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, len(self.attributes()))

    def as_dataset(self):
        """Export the row as a dataset.

        :rtype: tablib.Dataset

        """
        data = tablib.Dataset(headers=self.attributes())

        _values = list()
        for value in self.values():
            if hasattr(value, 'isoformat'):
                value = value.isoformat()  # pragma: no cover

            _values.append(value)

        data.append(_values)

        return data

    def as_dict(self):
        """Export the row as a dictionary.
        
        :rtype: dict
        
        """
        d = dict()
        i = 0
        for name in self.attributes():
            d[name] = self.values()[i]
            i += 1

        return d

    def as_ordered_dict(self):
        """Export the row as a dictionary.

        :rtype: dict

        """
        return OrderedDict(self.as_dict())

    def attributes(self):
        """Get the attribute names for the row.

        :rtype: list[str]

        """
        return self._attributes

    def get(self, name, default=None):
        """Get the value of a given attribute.

        :param name: The name of the attribute.
        :type name: str

        :param default: The default value if the key is not defined.

        """
        try:
            return self[name]
        except KeyError:
            return default

    def export(self, output_format=EXPORT_FORMAT.JSON, **kwargs):
        """Export the row to the given output format.

        :param output_format: The format to which the data should be exported.
        :type output_format: str

        kwargs are passed to the ``export()`` method of the dataset.

        """
        ds = self.as_dataset()
        return ds.export(output_format, **kwargs)

    def has(self, name):
        """Indicates the given attribute exists.

        :param name: The name of the attribute.
        :type name: str

        """
        return name in self.attributes()

    def values(self):
        """Get the values of the record.

        :rtype: tuple

        """
        return self._values


class Session(object):
    """A database session."""

    def __init__(self, connection):
        """Initialize the session.

        :param connection: The database connection received from the engine.

        """
        self.is_open = not connection.closed
        self._connection = connection

    def close(self):
        """End the session."""
        self._connection.close()
        self.is_open = False

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        # _open = "closed"
        # if self.is_open:
        #     _open = "open"
        #
        # return "<%s %s>" % (self.__class__.__name__, _open)
        return "<%s>" % self.__class__.__name__

    def aggregate(self, statement, **params):
        """Run an aggregate query.

        :param statement: The query to execute.
        :type statement: str

        :param params: Any values to be bound to the statement.
        :type params: dict

        :rtype: commonkit.database.library.Result

        """
        try:
            cursor = self._connection.execute(query_to_text(statement), **params)
        except OperationalError as e:
            return Result(statement, bindings=params, error=str(e), success=False)

        return Result(statement, aggregate=cursor.scalar(), bindings=params, count=1, success=True)

    def query(self, statement, lazy=True, **params):
        """Run a select query.

        :param statement: The query to execute.
        :type statement: str

        :param lazy: Indicates whether rows should be loaded immediately (``False``) or later (``True``).
                     If later, the database connection *must* remain open.
        :type lazy: bool

        :param params: Any values to be bound to the statement.
        :type params: dict

        :rtype: commonkit.database.library.Result

        """
        try:
            cursor = self._connection.execute(query_to_text(statement), **params)
        except OperationalError as e:
            return Result(statement, bindings=params, error=str(e), success=False)

        generator = (Row(cursor.keys(), row) for row in cursor)
        rows = Set(generator)

        if not lazy:
            rows.all()

        return Result(statement, bindings=params, count=len(rows), rows=rows, success=True)

    def raw(self, statement, **params):
        """Run a query statement within a transaction.

        :param statement: The query to execute.
        :type statement: str

        :param params: Any values to be bound to the statement.
        :type params: dict

        :rtype: commonkit.database.library.Result

        """
        with self.transaction() as transaction:
            try:
                cursor = transaction.execute(query_to_text(statement), **params)
                return Result(statement, bindings=params, count=cursor.rowcount, last_id=cursor.lastrowid, success=True)
            except (OperationalError, ProgrammingError) as e:
                return Result(statement, bindings=params, error=str(e), success=False)

    @contextmanager
    def transaction(self):
        """Allows execution of a query within a transaction.

        :returns: Yields the current connection instance.

        """

        transaction = self._connection.begin()
        try:
            yield self._connection
            transaction.commit()
        except:  # pragma: no cover
            transaction.rollback()
        finally:
            transaction.close()


class Set(object):
    """A collection of database rows."""

    def __init__(self, rows):
        """Initialize the collection.

        :param rows: The rows included in the set. See ``Session.query()``.

        """
        self.pending = True
        self._all = list()
        self._rows = rows

    def __getitem__(self, item):  # pragma: no cover
        item_is_integer = isinstance(item, int)

        if item_is_integer:
            item = slice(item, item + 1)

        while len(self) < item.stop or item.stop is None:
            try:
                next(self)
            except StopIteration:
                break

        rows = self._all[item]
        if item_is_integer:
            return rows[0]

        return Set(iter(rows))

    def __iter__(self):
        index = 0
        while True:
            if index < len(self):
                yield self[index]
            else:
                try:
                    yield next(self)
                except StopIteration:
                    return

            index += 1

    def __len__(self):
        return len(self._all)

    def __next__(self):
        try:
            row = next(self._rows)
            self._all.append(row)
            return row
        except StopIteration:
            self.pending = False
            raise StopIteration("There are no more rows in the set.")

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, len(self))

    def all(self):
        """Get all rows in the set.

        :rtype: list[rows]

        """
        return list(self)

    def as_dataset(self):
        """Export the rows as a dataset.

        :rtype: tablib.Dataset

        """
        data = tablib.Dataset()

        if len(list(self)) == 0:
            return data

        data.headers = self[0].attributes()
        for row in self.all():
            values = list()
            for value in row.values():
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()  # pragma: no cover

                values.append(value)

            data.append(values)

        return data

    def as_dict(self):
        """Get the rows as a list of dictionaries.

        :rtype: list[dict]

        """
        a = list()
        rows = self.all()
        for row in rows:
            a.append(row.as_dict())

        return a

    def as_ordered_dict(self):
        """Get the rows as a list of ordered dictionaries.

        :rtype: list[OrderedDict]

        """
        a = list()
        rows = self.all()
        for row in rows:
            a.append(row.as_ordered_dict())

        return a

    def export(self, output_format=EXPORT_FORMAT.CSV, **kwargs):
        """Export the rows to the given output format.

        :param output_format: The format to which the data should be exported.
        :type output_format: str

        kwargs are passed to the ``export()`` method of the dataset.

        """
        ds = self.as_dataset()
        return ds.export(output_format, **kwargs)

    def next(self):
        """Get the next row in the set.

        :rtype: Row | None

        At present, ``next()`` cannot be executed from within :py:class:`commonkit.databse.library.Database`. Instead,
        you must manually execute the connection and query. For example:

        .. code-block:: python

            db.backend.connect()
            with db.backend.get_session() as session:
                result = session.query("SELECT * FROM mytable;")
                try:
                    row = result.rows.next()
                except StopIteration:
                    pass

            db.backend.discconnect()

        """
        return self.__next__()
