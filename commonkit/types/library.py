# Imports

import six
from ..regex import EMAIL_PATTERN, STRICT_EMAIL_PATTERN
from ..constants import BOOLEAN_VALUES, FALSE_VALUES, TRUE_VALUES

# Exports

__all__ = (
    "boolean_safe",
    "is_bool",
    "is_email",
    "is_float",
    "is_integer",
    "is_number",
    "is_string",
    "smart_cast",
    "to_bool",
    "BooleanBecause",
    "FalseBecause",
    "TrueBecause",
)

# Decorators


def boolean_safe(function):
    """Decorate a function such that any value provided as a bool will always return ``False`` before the value is
    evaluated by the function. See ``is_float()``, ``is_integer()``, and ``is_number()``.

    """

    def wrapper(value, **kwargs):
        # Booleans must be ignored.
        if type(value) is bool:
            return False

        return function(value, **kwargs)

    return wrapper

# Functions


def is_bool(value, test_values=BOOLEAN_VALUES):
    """Determine if the given value is a boolean at run time.

    :param value: The value to be checked.

    :param test_values: The possible values that could be True or False.
    :type test_values: list | tuple

    :rtype: bool

    .. code-block:: python

        from superpython.utils import is_bool

        print(is_bool("yes"))
        print(is_bool(True))
        print(is_bool("No"))
        print(is_bool(False))

    .. note::
        By default, a liberal number of values are used to test. If you *just* want ``True`` or ``False``, simply pass
        ``(True, False)`` as ``test_values``.

    """
    return value in test_values


def is_email(value, strict=False):
    """Determine whether the given value is an email address.

    :param value: The value to be checked.

    :param strict: Use a stricter match for evaluating the address.
    :type strict: bool

    :rtype: bool

    """
    if not is_string(value):
        return False

    if strict:
        return bool(STRICT_EMAIL_PATTERN.match(value))

    return bool(EMAIL_PATTERN.match(value))


@boolean_safe
def is_float(value):
    """Indicates whether the given value is a float.

    :param value: The value to be checked.

    :rtype: bool

    """
    if isinstance(value, float):
        return True

    if is_integer(value, cast=True):
        return False

    try:
        float(value)
        return True
    except ValueError:
        return False


@boolean_safe
def is_integer(value, cast=False):
    """Indicates whether the given value is an integer. Saves a little typing.

    :param value: The value to be checked.

    :param cast: Indicates whether the value (when given as a string) should be cast to an integer.
    :type cast: bool

    :rtype: bool

    .. code-block:: python

        from superpython.utils import is_integer

        print(is_integer(17))
        print(is_integer(17.5))
        print(is_integer("17"))
        print(is_integer("17", cast=True))

    """
    if isinstance(value, int):
        return True

    if isinstance(value, str) and cast:
        try:
            int(value)
        except ValueError:
            return False
        else:
            return True

    return False


@boolean_safe
def is_number(value):
    """Indicates whether a given value is a number; a decimal, float, or integer.

    :param value: The value to be tested.

    :rtype: bool

    """
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True


def is_string(value):
    """Indicates whether the given value is a string. Saves a little typing.

    :param value: The value to be checked.

    :rtype: bool

    .. code-block:: python

        from superpython.utils import is_string

        print(is_string("testing"))
        print(is_string("17"))
        print(is_string(17))

    """
    return isinstance(value, six.string_types)


def smart_cast(value):
    """Intelligently cast the given value to a Python data type.

    :param value: The value to be cast.
    :type value: str

    """
    # Handle integers first because is_bool() may interpret 0s and 1s as booleans.
    if is_integer(value, cast=True):
        return int(value)
    elif is_float(value):
        return float(value)
    elif is_bool(value):
        return to_bool(value)
    else:
        return value


def to_bool(value, false_values=FALSE_VALUES, true_values=TRUE_VALUES):
    """Convert the given value to it's boolean equivalent.

    :param value: The value to be converted.

    :param false_values: The possible values that could be False.
    :type false_values: list | tuple

    :param true_values: The possible values that could be True.
    :type true_values: list | tuple

    :rtype: bool

    :raises: ``ValueError`` if the value could not be converted.

    .. code-block:: python

        from superpython.utils import to_bool

        print(to_bool("yes"))
        print(to_bool(1))
        print(to_bool("no"))
        print(to_bool(0))

    """
    if value in true_values:
        return True

    if value in false_values:
        return False

    raise ValueError('"%s" cannot be converted to True or False.')

# Classes


class BooleanBecause(object):
    """Simulates a boolean value with an additional description or "cause" for the ``True`` or ``False`` value."""

    def __init__(self, value, because=None):
        """Initialize a boolean.

        :param value: The boolean value.
        :type value: bool

        :param because: The reason for ``True`` or ``False``.
        :type because: str

        """
        self.value = bool(value)
        self.because = because or "for unknown reason"

    def __bool__(self):
        return self.value

    def __eq__(self, other):
        return bool(self) == other

    def __hash__(self):
        return hash(bool(self))

    def __neq__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<%s %s>" % (self.value, self.because)


class FalseBecause(BooleanBecause):
    """BooleanBecause with a value of ``False``."""

    def __init__(self, because=None):
        super().__init__(False, because=because)


class TrueBecause(BooleanBecause):
    """BooleanBecause with a value of ``True``."""

    def __init__(self, because=None):
        super().__init__(True, because=because)
