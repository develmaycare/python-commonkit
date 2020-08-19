# Imports

from colorama import init as colorama_init, Fore, Style
from ..context_managers import captured_output

colorama_init()

__version__ = "0.7.1-a"

# Exports

__all__ = (
    "BLUE",
    "GREEN",
    "RED",
    "YELLOW",
    "blue",
    "colorize",
    "green",
    "hr",
    "plain",
    "red",
    "yellow",
    "Feedback",
)

# Constants

BLUE = Fore.BLUE
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW

# Functions


def colorize(color, message, prefix=None, suffix=None):
    """Return the given message in color.

    :param color: The color to use. A ``coloroma.Fore`` class constant.
    :type color: int

    :param message: The message to be colorized.
    :type message: str

    :param prefix: A string to include before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to include after the message. A space is automatically added to the beginning.
    :type suffix: str

    :rtype: str

    """
    a = list()
    a.append(color)

    if prefix is not None:
        a.append(prefix + " ")

    a.append(message)

    if suffix is not None:
        a.append(" " + suffix)

    a.append(Style.RESET_ALL)

    return "".join(a)

# Colors


def blue(message, prefix=None, suffix=None):
    """Print the message in blue text.

    :param message: The message to be printed.
    :type message: str

    :param prefix: A string to print before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to print after the message. A space is automatically added to the beginning.
    :type suffix: str

    """
    print(colorize(BLUE, message, prefix=prefix, suffix=suffix))


def green(message, prefix=None, suffix=None):
    """Print the message in green text.

    :param message: The message to be printed.
    :type message: str

    :param prefix: A string to print before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to print after the message. A space is automatically added to the beginning.
    :type suffix: str

    """
    print(colorize(GREEN, message, prefix=prefix, suffix=suffix))


def hr(character="-", color=None, size=80):
    """Print a horizontal rule to feedback.

    :param character: The character to use for the line.
    :type character: str

    :param color: The color function to use.
    :type color: function

    :param size: The number of characters to print.
    :type size: int

    """
    message = character * size
    if callable(color):
        color(message)
        return

    print(message)


def plain(message, prefix=None, suffix=None):
    """Print the message in plain text.

    :param message: The message to be printed.
    :type message: str

    :param prefix: A string to print before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to print after the message. A space is automatically added to the beginning.
    :type suffix: str

    """
    a = list()

    if prefix is not None:
        a.append(prefix + " ")

    a.append(message)

    if suffix is not None:
        a.append(" " + suffix)

    print("".join(a))


def red(message, prefix=None, suffix=None):
    """Print the message in red text.

    :param message: The message to be printed.
    :type message: str

    :param prefix: A string to print before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to print after the message. A space is automatically added to the beginning.
    :type suffix: str

    """
    print(colorize(RED, message, prefix=prefix, suffix=suffix))


def yellow(message, prefix=None, suffix=None):
    """Print the message in yellow text.

    :param message: The message to be printed.
    :type message: str

    :param prefix: A string to print before the message. A space is automatically added to the end.
    :type prefix: str

    :param suffix: A string to print after the message. A space is automatically added to the beginning.
    :type suffix: str

    """
    print(colorize(YELLOW, message, prefix=prefix, suffix=suffix))


# Feedback Class


class Feedback(object):
    """Collects feedback in a single instance."""

    def __init__(self):
        self.messages = list()

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return "\n".join(self.messages)

    def blue(self, message, prefix=None, suffix=None):
        """Add a message in blue text.

        :param message: The message to be printed.
        :type message: str

        :param prefix: A string to print before the message. A space is automatically added to the end.
        :type prefix: str

        :param suffix: A string to print after the message. A space is automatically added to the beginning.
        :type suffix: str

        """
        self.messages.append(colorize(BLUE, message, prefix=prefix, suffix=suffix))

    def cr(self):
        """Add a carriage return (line feed) to the feedback."""
        self.messages.append("")

    def green(self, message, prefix=None, suffix=None):
        """Add a message in green text.

        :param message: The message to be printed.
        :type message: str

        :param prefix: A string to print before the message. A space is automatically added to the end.
        :type prefix: str

        :param suffix: A string to print after the message. A space is automatically added to the beginning.
        :type suffix: str

        """
        self.messages.append(colorize(GREEN, message, prefix=prefix, suffix=suffix))

    def heading(self, label, divider="="):
        """Add a heading to the output.

        :param label: The label of the heading.
        :type label: str

        :param divider: The divider that goes under the heading.
        :type divider: str

        """
        self.messages.append(label)
        self.messages.append(divider * len(label))
        self.cr()

    def hr(self, character="-", color=None, size=80):
        """Add a horizontal rule to feedback.

        :param character: The character to use for the line.
        :type character: str

        :param color: The color function to use.
        :type color: function

        :param size: The number of characters to print.
        :type size: int

        """
        message = character * size
        if callable(color):
            with captured_output() as (output, error):
                color(message)
                message = output.getvalue()

        self.messages.append(message)

    def plain(self, message, prefix=None, suffix=None):
        """Add a plain text message.

        :param message: The message to be printed.
        :type message: str

        :param prefix: A string to print before the message. A space is automatically added to the end.
        :type prefix: str

        :param suffix: A string to print after the message. A space is automatically added to the beginning.
        :type suffix: str

        """
        a = list()

        if prefix is not None:
            a.append(prefix + " ")

        a.append(message)

        if suffix is not None:
            a.append(" " + suffix)

        self.messages.append("".join(a))

    def red(self, message, prefix=None, suffix=None):
        """Add a message in red text.

        :param message: The message to be printed.
        :type message: str

        :param prefix: A string to print before the message. A space is automatically added to the end.
        :type prefix: str

        :param suffix: A string to print after the message. A space is automatically added to the beginning.
        :type suffix: str

        """
        self.messages.append(colorize(RED, message, prefix=prefix, suffix=suffix))

    def yellow(self, message, prefix=None, suffix=None):
        """Add a message in yellow text.

        :param message: The message to be printed.
        :type message: str

        :param prefix: A string to print before the message. A space is automatically added to the end.
        :type prefix: str

        :param suffix: A string to print after the message. A space is automatically added to the beginning.
        :type suffix: str

        """
        self.messages.append(colorize(YELLOW, message, prefix=prefix, suffix=suffix))
