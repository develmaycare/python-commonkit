# Imports

from getpass import getpass
from collections import OrderedDict
import re
from ..types import is_bool, is_email, to_bool

__version__ = "0.3.0-x"

# Exports

__all__ = (
    "get_choice",
    "get_input",
    "Boolean",
    "Divider",
    "Email",
    "Float",
    "Form",
    "Input",
    "Integer",
    "MetaForm",
    "Regex",
    "Secret",
    "String",
)

# Functions


def get_choice(label, choices=None, default=None):
    """Prompt the user to select from some number of choices.

    :param label: The label of the prompt.
    :param label: str

    :param choices: A list of valid choices. Default: ``["yes", "no"]``
    :type: list

    :param default: The default value.

    :rtype: str | None

    """
    if choices is None:
        choices = ["yes", "no"]

    if default:
        _label = "%s [%s]" % (label, default)
    else:
        _label = label

    print("")
    print(_label)
    print("-" * len(_label))

    count = 1
    numbers = list()
    for choice in choices:
        print("    %s. %s" % (count, choice))

        numbers.append(count)
        count += 1

    value = get_input("Enter Choice")

    if not value and default is not None:
        return default

    # print(type(value), value)

    if not value or int(value) not in numbers:
        print("Invalid choice ...")
        print("")

        return get_choice(label, choices=choices, default=default)

    return choices[int(value) - 1]


def get_input(label, default=None):
    """Prompt the user for input.

    :param label: The label of the prompt.
    :param label: str

    :param default: The default value.

    :rtype: str | None

    """
    if default:
        _label = "%s [%s]: " % (label, default)
    else:
        _label = "%s: " % label

    print("")
    value = input(_label)

    if not value:
        return default

    return value


# Classes


class Input(object):
    """Base class for input instances."""

    def __init__(self, label, choices=None, default=None, required=False):
        """Initialize the input.

        :param label: The label to display to the user.
        :type label: str

        :param choices: A list of valid choices.
        :type choices: list[str] | tuple[str]

        :param default: The default value, if any.

        :param required: Indicates the user must supply a value.
        :type required: bool

        """
        self.choices = choices
        self.default = default
        self.error = None
        self.label = label
        self.name = label.strip("':?").replace("'", "").replace(" ", "_").lower()
        self.required = required
        self.value = None

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.label)

    # noinspection PyMethodMayBeStatic
    def get_type(self):
        """Get the Python data type of the input. The default is ``str``."""
        return str

    def is_valid(self):
        """Validate the current value.

        :rtype: bool

        """
        if self.value is None and self.required:
            self.error = "%s is required." % self.label
            return False

        return True

    def prompt(self):
        """Prompt the user for input."""
        self.value = self._prompt()

        if not self.is_valid():
            print(self.error)
            self.prompt()

        return self.to_python()

    def to_python(self):
        """Get the value as a Python data type."""
        cast = self.get_type()
        return cast(self.value)

    def _prompt(self):
        """Support from ``prompt()``."""
        if self.choices is not None:
            return get_choice(self.label, choices=self.choices, default=self.default)

        return get_input(self.label, default=self.default)

# Input Types


class Boolean(Input):
    """Prompt and validate email input."""

    def __init__(self, label, choices=("yes", "no"), default=None, required=False):
        """Initialize the input with choices set to ``("yes", "no")`` by default."""
        super().__init__(label, choices=choices, default=default, required=required)

    def get_type(self):
        """Always returns ``bool``."""
        return bool

    def is_valid(self):
        """Validate the input as a boolean."""
        if not super().is_valid():
            return False

        if not is_bool(self.value):
            self.error = "Invalid input."
            return False

        return True

    def to_python(self):
        """Return the input as a boolean."""
        return to_bool(self.value)


class Divider(object):
    """Creates a divider between inputs, especially in a form."""

    def __init__(self, characters="=", label=None, length=80):
        self.characters = characters
        self.label = label
        self.length = length

    def prompt(self):
        """Does not prompt for input. Instead, the divider is displayed."""
        if self.label is not None:
            print("")
            print(self.label)

        print(self.characters * self.length)

        return None


class Email(Input):
    """Prompt and validate email input.

    See https://stackoverflow.com/a/8022584/241720

    """

    def is_valid(self):
        """Validate the input as an email address."""
        if not super().is_valid():
            return False

        return is_email(self.value)
        # pattern = re.compile(EMAIL_PATTERN, re.IGNORECASE)
        # if not pattern.match(self.value):
        #     self.error = "Enter a valid email address."
        #     return False
        #
        # return True


class Float(Input):
    """Prompt and validate for a float."""

    def get_type(self):
        """Always returns ``float``."""
        return float

    def is_valid(self):
        """Validate the input as a float.

        .. note::
            Integer values will be converted to a float. For example, ``1`` becomes ``1.0``.

        """
        if not super().is_valid():
            return False

        try:
            float(self.value)
        except ValueError:
            self.error = '"%s" is not a float.' % self.label
            return False

        return True


class Integer(Input):
    """Prompt and validate for an integer."""

    def get_type(self):
        """Always returns ``int``."""
        return int

    def is_valid(self):
        """Validate the input as an integer."""
        if not super().is_valid():
            return False

        try:
            int(self.value)
        except ValueError:
            self.error = '"%s" is not an integer.' % self.label
            return False

        return True


class Regex(Input):
    """Prompt and validate a given regular expression."""

    def __init__(self, label, pattern, flags=0, **kwargs):
        """Initialize the input.

        :param pattern: The regular expression.
        :type pattern: str

        :param flags: Flags to be passed to ``re.match()``.

        See :py:class:`Input` for additional parameters.

        """
        super().__init__(label, **kwargs)

        self.flags = flags
        self.pattern = pattern

    def is_valid(self):
        """Validate the input using the given pattern and ``re.fullmatch()``."""
        if not super().is_valid():
            return False

        if not re.fullmatch(self.pattern, self.value, flags=self.flags):
            self.error = "Invalid input."
            return False

        return True

    def to_python(self):
        """Returns the result of ``re.match()``.

        :rtype: re.Match

        """
        return re.fullmatch(self.pattern, self.value, flags=self.flags)


class Secret(Input):
    """Prompt for a string without printing the input value."""

    def prompt(self):
        """Uses ``getpass()`` to prompt for input."""
        print("")
        self.value = getpass("%s: " % self.label)

        if len(self.value) == 0:
            self.value = None

        if not self.is_valid():
            print(self.error)
            self.prompt()

        return self.to_python()


class String(Input):
    """Prompt and validate string input."""

    def __init__(self, label, maximum=None, minimum=None, **kwargs):
        """Initialize the input.

        :param maximum: The maximum length of the string.
        :type maximum: int

        :param minimum: The minimum length of the string.
        :type minimum: int

        See :py:class:`Input` for additional parameters.

        .. note::
            If ``minimum`` is given, the ``required`` flag is automatically set to ``True``.

        """
        super().__init__(label, **kwargs)
        self.maximum = maximum
        self.minimum = minimum

        if self.minimum is not None:
            self.required = True

    def is_valid(self):
        """Validate the input, optionally using minimum and maximum string length (if provided)."""
        if not super().is_valid():
            return False

        if self.maximum is not None and len(self.value) > self.maximum:
            self.error = "%s must be no more than %s characters long. %s given." % (
                self.label, self.maximum,
                len(self.value)
            )
            return False

        if self.minimum is not None and len(self.value) < self.minimum:
            self.error = "%s must be at least %s characters long. %s given." % (
                self.label, self.maximum,
                len(self.value)
            )
            return False

        return True

# Forms


class MetaForm(type):
    """Meta class for forms."""

    def __new__(mcs, name, bases, attrs):
        """Add the inputs defined as class attributes as ``fields`` in the order in which they are defined."""
        attrs['fields'] = OrderedDict()
        for name, member in attrs.items():
            if isinstance(member, Input):
                attrs['fields'][name] = member

        return type.__new__(mcs, name, bases, attrs)


class Form(metaclass=MetaForm):
    """A form is a collection of inputs that may be dynamically assembled.

    .. code-block:: python

        from commonkit.shell import prompts

        class NewUserForm(prompts.Form):
            name = prompts.String("Name", minimum=2)
            email = prompts.Email("Email Address", required=True)
            password1 = prompts.Secret("Password", required=True)
            password2 = prompts.Secret("Password Again", required=True)

        form.prompt()
        print(form.values)

    """

    def __init__(self):
        """Initialize the form."""
        self.values = dict()

    # Saved for historical reference. Will be removed in future release.
    # def get_inputs(self):
    #     """Get the inputs associated with the form.
    #
    #     :rtype: list[BaseType[Input]]
    #
    #     """
    #
    #     inputs = list()
    #     members = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
    #     # members.sort(key=self.__get_line_number_of_member)
    #
    #     for name, obj in members:
    #         if isinstance(obj, Input):
    #             inputs.append(obj)
    #
    #     return inputs

    def get(self, name, default=None):
        """Get the value of the named field.

        :param name: The field name.
        :type name: str

        :param default: A default value if the field does not exist or has no value.

        """
        return self.values.get(name, default)

    def get_fields(self):
        """Get the fields defined on the form.

        :rtype: list[BaseType[Input]]

        """
        a = list()
        # noinspection PyUnresolvedReferences
        for name, field in self.fields.items():
            a.append(field)

        return a

    def prompt(self):
        """Prompt the user for all of the inputs."""
        # noinspection PyUnresolvedReferences
        for name, field in self.fields.items():

            if type(field.default) is str and field.default.startswith("$"):
                field.default = self.values.get(field.default.replace("$", ""))

            self.values[name] = field.prompt()
