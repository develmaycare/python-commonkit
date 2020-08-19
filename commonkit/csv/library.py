# Imports

import csv
import os
from ..files import read_csv
from ..strings import slug
from ..types import smart_cast

# Exports

__all__ = (
    "AutoMapping",
    "CSVFile",
    "CSVRow",
    "IndexMapping",
    "KeywordMapping",
)

# Classes


class CSVFile(object):
    """A CSV file."""

    NONE_TYPE_VALUES = [
        "-",
        "--",
        "NA",
        "na",
        "N/A",
        "n/a",
        "NIL",
        "NILL",
        "nil",
        "nill",
        "NONE",
        "None",
        "none",
    ]
    """Imported values that evaluate to ``None``. See ``get_none_type_values()``."""

    def __init__(self, path, defaults=None, encoding="utf-8", mapping=None, none_type_values=None, row_class=None,
                 smart_cast_fields=None):
        self.defaults = defaults or dict()
        self.encoding = encoding
        self.is_loaded = False
        self.mapping = mapping
        self.none_type_values = none_type_values
        self.path = path
        self.row_class = row_class
        self.rows = list()
        self.smart_cast_fields = smart_cast_fields or list()
        self._column_names = None

        if isinstance(mapping, KeywordMapping):
            self.first_row_field_names = True
        elif isinstance(mapping, AutoMapping):
            self.first_row_field_names = True
        else:
            self.first_row_field_names = False

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.path)

    @property
    def exists(self):
        return os.path.exists(self.path)

    def get_column_names(self):
        """Get the column names of the CSV.

        :rtype: list[str] | None

        """
        if isinstance(self.mapping, AutoMapping):
            # noinspection PyProtectedMember
            return self.mapping._slugged_fields.values()
        elif isinstance(self.mapping, KeywordMapping):
            return self.mapping.fields.keys()
        elif isinstance(self.mapping, IndexMapping):
            return self.mapping.fields.keys()
        else:
            return None

    # noinspection PyUnusedLocal
    def get_default_value(self, field_name, row):
        """Get the default value for a given field.

        :param field_name: The name of the field.
        :type field_name: str

        :param row: The current row being processed.

        """
        return self.defaults.get(field_name, None)

    def get_none_type_values(self):
        """Get the values that are to be recognized as ``None``.

        :rtype: list[str]

        """
        return self.none_type_values or self.NONE_TYPE_VALUES

    def read(self, **kwargs):
        """Read the CSV file.

        :rtype: bool

        kwargs are passed to Python's ``csv.DictReader`` (when ``first_row_field_names`` is ``True``) or ``csv.reader``.

        """
        if not self.exists:
            return False

        row_class = self.row_class
        _rows = read_csv(self.path, encoding=self.encoding, first_row_field_names=self.first_row_field_names, **kwargs)

        for _row in _rows:
            if self.mapping is not None:
                _values = self.mapping.get_values(_row)
                values = dict()
                for key, value in _values.items():
                    values[key] = self.smart_cast(key, _row, value)
            else:
                values = _row

            if row_class is not None:
                self.rows.append(row_class(**values))
            else:
                self.rows.append(values)

        self.is_loaded = True

        return True

    def smart_cast(self, field_name, row, value):
        """Cast a value to the appropriate Python data type.

        :param field_name: The name of the field.
        :type field_name: str

        :param row: The current row being processed.

        :param value: The value to be cast.

        """
        # Handle non-values and empty-values.
        conditions = [
            value in self.get_none_type_values(),
            len(str(value)) == 0,
            str(value).isspace(),
            value is None,
        ]
        if any(conditions):
            return self.get_default_value(field_name, row)

        # Handle non-values and empty-values.
        # if value in self.get_none_type_values():
        #     return self.get_default_value(field_name, row)
        #
        # if len(str(value)) == 0 or str(value).isspace():
        #     return self.get_default_value(field_name, row)
        #
        # if value is None:
        #     return self.get_default_value(field_name, row)

        # There is nothing more to do if we haven't been instructed to cast the field.
        if field_name not in self.smart_cast_fields:
            return value

        # Handle a given callback.
        callback = None
        if type(self.smart_cast_fields) is dict:
            callback = self.smart_cast_fields.get(field_name, None)

        if callback is not None and callable(callback):
            return callback(field_name, row, value)

        # Use built-in smart cast as the default.
        return smart_cast(value)

    def write(self, columns=None, path=None, **kwargs):
        """Write a CSV file.

        :param columns: A list of column names to be included.
        :type columns: list[str]

        :param path: The path to the file. Defaults to the instantiated path.
        :type path: str

        kwargs are passed to Python's ``csv.writer()``.

        .. important::
            Column names are derived from the ``mapping``. When :py:class:`commonkit.csv.library.AutoMapping` is used,
            the column names will only exist if the file has been read prior to attempting the write. Use the
            ``columns`` paramet to provide the names you wish to write.

        .. note::
            The ``write()`` method works with rows that have been provided (or loaded using ``read()``) as lists,
            dictionaries, or :py:class:`commonkit.csv.library.CSVRow` instances. If you provide a ``row_class`` upon
            instantiation, this method cannot be used.

        """
        _path = path or self.path

        with open(_path, 'w', newline='') as f:
            writer = csv.writer(f, **kwargs)

            if self.first_row_field_names:
                _columns = columns or self.get_column_names()

                writer.writerow(_columns)

                for row in self.rows:
                    if isinstance(row, CSVRow):
                        _values = row.values
                    else:
                        _values = row

                    values = list()
                    for column in _columns:
                        values.append(_values[column])

                    writer.writerow(values)
            else:
                for row in self.rows:
                    writer.writerow(row)

            f.close()


class CSVRow(object):
    """A simple placeholder that may be used for the ``row_class`` parameter of :py:class:`CSVReader`."""

    def __init__(self, **values):
        self.values = values

    def __getattr__(self, item):
        return self.values.get(item)


# Mapping Classes


class AutoMapping(object):
    """Automatically map the column names of a CSV to fields of the same name in each row."""

    def __init__(self, slugger=None):
        """Initialize an automapping.

        :param slugger: The callable to use for normalizing the column names found in the file. Defaults to
                        :py:func:`commonkit.utils.slug`.
        :type slugger: callable

        """
        self.slug = slugger or slug
        self._slugged_fields = dict()

    def get_values(self, row):
        """Get the values for a given row.

        :param row: A row from Python's ``csv.DictReader``.
        :type row: dict

        :rtype: dict

        """
        values = dict()
        for column_name, value in row.items():

            if column_name not in self._slugged_fields:
                self._slugged_fields[column_name] = self.slug(column_name, separator="_")

            field_name = self._slugged_fields[column_name]
            values[field_name] = value

        return values


class IndexMapping(object):
    """Map fields based on their column index."""

    def __init__(self, **fields):
        """Initialize an index mapping.

        Fields are provided in the form field/index pairs: For example:

        .. code-block:: python

            mapping = IndexMapping(first_name=0, last_name=0)

        """
        self.fields = fields

    def get_values(self, row):
        """Get the values for a given row.

        :param row: A row from Python's ``csv.reader``.
        :type row: list

        :rtype: dict

        """
        values = dict()
        for field_name, index in self.fields.items():
            try:
                value = row[index]
            except IndexError:
                value = None

            values[field_name] = value

        return values


class KeywordMapping(object):
    """Map fields based on column names."""

    def __init__(self, **fields):
        """Initialize a keyword mapping.

        Fields are provided in field name/column name pairs. For example:

        .. code-block:: python

            mapping = KeywordMapping(first_name="First Name", last_name="Last Name")

        """
        self.fields = fields

    def get_values(self, row):
        """Get the values for a given row.

        :param row: A row from Python's ``csv.DictReader``.
        :type row: dict

        :rtype: dict

        """
        values = dict()
        for field_name, column_name in self.fields.items():
            values[field_name] = row[column_name]

        return values
