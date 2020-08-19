# Imports

from ..files import parse_jinja_template, read_file
from .base import Base
from .exceptions import VariableNameNotAllowed

# Exports

__all__ = (
    "FlatConfig",
)

# Classes


class FlatConfig(Base):
    """Parse a flat configuration file.

    .. code-block:: cfg

        # Comments and blank lines are ignored.
        ; Comments and blank lines are ignored.
        ssh_key = ~/.ssh/deploy
        user = deploy

    """

    def __init__(self, path, context=None, defaults=None):
        """Initialize a "flat" configuration.

        :param path: The path to the file.
        :type path: str

        :param context: Context is used to parse the file as a Jinja template.
        :type context: dict

        :param defaults: Defaults values.
        :type defaults: dict

        """
        super().__init__(path)

        self._context = context
        self._variables = defaults or dict()

    def __getattr__(self, item):
        return self._variables.get(item)

    def __len__(self):
        return len(self._variables)

    def get(self, name, default=None):
        """Get the named value.

        :param name: The name of the value to return.
        :type name: str

        :param default: The default if the name does not exist or has no value.

        """
        return self._variables.get(name, default)

    def has(self, name):
        """Determine whether a value is defined and is not ``None``.

        :param name: The variable name.
        :type name: str

        :rtype: bool

        """
        if name in self._variables:
            return self._variables[name] is not None

        return False

    def load(self):
        """Load a flat configuration file."""
        if not self.exists:
            return False

        if self._context is not None:
            lines = parse_jinja_template(self._path, self._context).split("\n")
        else:
            lines = read_file(self._path).split("\n")

        line_number = 0
        for line in lines:
            line_number += 1

            if len(line) == 0:
                continue

            if line.startswith("#") or line.startswith(";"):
                continue

            key, value = line.split("=")
            key = key.strip()
            value = value.strip()

            if key in self._disallowed_variable_names():
                raise VariableNameNotAllowed(key, self._path, line=line_number)

            _key, _value = self._process_key_value_pair(key, value)
            self._variables[_key] = _value

        self.is_loaded = True

        return True
