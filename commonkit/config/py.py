# Imports

from importlib import import_module
import os
from .base import Base

# Exports

__all__ = (
    "PythonConfig",
)

# Classes


class PythonConfig(Base):
    """Load configuration from a Python file."""

    def __init__(self, path, defaults=None):
        self._defaults = defaults or dict()
        self._module = None

        super().__init__(path)

    def __getattr__(self, item):
        """Get the named section instance."""
        return self.get(item)

    def get(self, name, default=None):
        """Get the named variable from the loaded module.

        :param name: The variable name.
        :type name: str

        :param default: The default value if the variable does not exist or is ``None``.

        """
        if self.has(name):
            if name in self._defaults:
                return self._defaults[name]

            return getattr(self._module, name)

        return default

    def has(self, name):
        """Indicates whether the named variable exists.

        :rtype: str

        """
        if hasattr(self._module, name) and getattr(self._module, name) is not None:
            return True

        if name in self._defaults:
            return self._defaults[name] is not None

        return False

    def load(self):
        """Load configuration from a Python file."""
        if not self.exists:
            return False

        name = "%s.%s" % (self._root.replace(os.sep, "."), self._name)
        self._module = import_module(name)

        # An import error shouldn't occur because we've already tested for the existence of the file. Of course,
        # something could be wrong within the file.
        # try:
        #     self._module = import_module(name)
        # except ImportError as e:
        #     self._error = e
        #     return False

        self.is_loaded = True

        return True
