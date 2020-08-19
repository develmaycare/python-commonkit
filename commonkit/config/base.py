# Imports

import os
from ..types import smart_cast

# Classes


class Base(object):
    """Base class for implementing configuration readers.

    This class prepares or provides common resources for working with configuration files but is not responsible for
    loading or parsing a configuration. It is up to the child class to implement the ``load()`` method.

    It is also up to the child class to implement the ``get()`` and ``has()`` methods. You should also implement
    ``__getattr__()`` and ``__len()__``. See the current implementations as exampes.

    When implementing a configuration reader, care must be taken that no attribute will conflict with configuration
    values.

    The path, the location of the file, and the file name (without) the extension are stored internally using an
    underscore prefix so that these names will not conflict with configuration values.

    """

    DISALLOWED_VARIABLE_NAMES = [
        "exists",
        "get_error",
        "has_error",
        "is_loaded",
        "load",
        "relative_path_exists",
        "smart_cast",
    ]
    """A list of names that are not allowed as variables within the configuration file. This is intended to eliminate 
    nasty surprises where attributes or methods of the configuration instance might conflict with a variable named in 
    the configuration file.
    """

    def __init__(self, path):
        """Initialize a configuration.

        :param path: The path to the configuration file.
        :type path: str

        """
        self.is_loaded = False
        self._error = None
        self._name = os.path.basename(os.path.splitext(path)[0])
        self._path = path
        self._root = os.path.dirname(path)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self._path)

    @property
    def exists(self):
        """Indicates whether the configuration file exists."""
        return os.path.exists(self._path)

    def get(self, name, default=None):
        """Get the named value.

        :param name: The name of the value to return.
        :type name: str

        :param default: The default if the name does not exist or has no value.

        """
        raise NotImplementedError()

    def get_error(self):
        """Get an error encountered when loading the configuration.

        :rtype: str | None

        """
        return self._error

    def has(self, name):
        """Determine whether a value is defined and is not ``None``.

        :param name: The variable name.
        :type name: str

        :rtype: bool

        """
        raise NotImplementedError()

    @property
    def has_error(self):
        """Indicates whether an error has been encountered when loading the configuration.

        :rtype: bool

        """
        return self._error is not None

    def load(self):
        """Load the configuration file.

        :rtype: bool

        """
        raise NotImplementedError()

    def relative_path_exists(self, *parts):
        """Indicates whether the given path (parts) exists relative to the location of the configuration file.

        :rtype: bool

        """
        path = os.path.join(self._root, *parts)
        return os.path.exists(path)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def smart_cast(self, key, value, section=None):
        """Cast the value to the appropriate Python type during ``load()``.

        :param key: The name of the variable. Not used by default.
        :type key: str

        :param value: The value to be cast.

        :param section: The section or grouping of the variable. Not used by default.
        :type section: str

        """
        return smart_cast(value)

    def _disallowed_variable_names(self):
        """Get a list of variable names that may not be used.

        :rtype: str

        """
        return self.DISALLOWED_VARIABLE_NAMES

    def _process_key_value_pair(self, key, value, section=None):
        """An internal callback that processes a given key/value pair.

        :param key: The name of the variable.
        :type key: str

        :param value: The raw value of the variable. Possibly a string.

        :param section: The section or grouping of the variable. Not used by default.
        :type section: str

        :rtype: tuple
        :returns: The key and value, both of which may be modified.

        """
        return key, self.smart_cast(key, value, section=section)
