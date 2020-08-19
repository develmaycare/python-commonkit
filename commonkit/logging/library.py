# Imports

import logging
import sys
from ..platform import Platform

DefaultLogger = logging.getLoggerClass()

# Exports

__all__ = (
    "BaseFormatter",
    "ColorFormatter",
    "FileFormatter",
    "LoggingHelper",
    "PlainTextFormatter",
    "SuccessLogger",
)

# Formatters


class BaseFormatter(logging.Formatter):
    """Base for special log format classes.

    Code inspired and adapted from the Pelican project.

    """

    def __init__(self, fmt=None, datefmt=None):
        formatting = fmt or "[%(custom_level_name)s] %(message)s"
        super().__init__(fmt=formatting, datefmt=datefmt)

    def format(self, record):
        """Rework the output of a record to better display multi-line messages."""

        # Get the custom level name, if any.
        record.__dict__['custom_level_name'] = self._get_level_name(record.levelname)

        # Format multi-line messages.
        record.msg = record.msg.replace("\n", "\n  |  ")

        # Back to regularly scheduled programming.
        return super().format(record)

    def formatException(self, ei):  # pragma: no cover
        """Make the traceback info more readable."""
        # Get the super results.
        output = super().formatException(ei)

        # Make multi-line traceback look better.
        output = str("\n").join(str("    |  ") + line for line in output.splitlines())

        # Add an ending to the traceback for obvious separation.
        output = str("    |____\n{}").format(output)

        # Send it back.
        return output

    # noinspection PyMethodMayBeStatic
    def _get_level_name(self, name):
        """Get the name of the error level.

        :param name: The name of the level.
        :type name: str

        .. note::
            By default this just returns the name. Subclasses should do what they need to in order to represent the
            level name.

        """
        return name


class ColorFormatter(BaseFormatter):
    """Format log output using ANSI color codes.

    Code inspired and adapted from the Pelican project.

    """

    ANSI_CODES = {
        'bggrey': '\033[1;100m',
        'bgred': '\033[1;41m',
        'cyan': '\033[1;36m',
        'green': '\x1b[32m',
        'red': '\033[1;31m',
        'reset': '\033[0;m',
        'yellow': '\033[1;33m',
        'white': '\033[1;37m',
    }

    LEVEL_COLORS = {
        'INFO': 'cyan',
        'SUCCESS': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bgred',
        'DEBUG': 'bggrey'
    }

    def _get_level_name(self, name):
        """Wrap the level name in color."""
        color = self.ANSI_CODES[self.LEVEL_COLORS.get(name, 'white')]

        fmt = "{0}{1}{2}"

        return fmt.format(color, name, self.ANSI_CODES['reset'])


class FileFormatter(logging.Formatter):
    """Format output for a log file."""

    def __init__(self, fmt=None, datefmt=None):
        """Initialize the file formatter.

        If not unspecified the ``fmt`` defaults to: ``%(asctime)s | %(custom_level_name)-10s | %(message)s``. If you
        specify your own format, be sure to use ``custom_level_name`` instead of ``levelname``.

        """
        formatting = fmt or "%(asctime)s | %(custom_level_name)-10s | %(message)s"
        super().__init__(fmt=formatting, datefmt=datefmt)

        # TODO: Flatten the message using format() method?
    def format(self, record):
        """Rework the output of a record to better display multi-line messages."""

        # Get the custom level name, if any.
        record.__dict__['custom_level_name'] = self._get_level_name(record.levelname)

        # Squash and truncate multi-line messages.
        message = record.msg.replace("\n", " ")
        record.msg = message

        # Back to regularly scheduled programming.
        return super().format(record)

    # noinspection PyMethodMayBeStatic
    def _get_level_name(self, name):
        """Get the name of the error level.

        :param name: The name of the level.
        :type name: str

        .. note::
            By default this just returns the name. Subclasses should do what they need to in order to represent the
            level name.

        """
        return name


class PlainTextFormatter(BaseFormatter):
    """Format log output as plain text.

    Code inspired and adapted from the Pelican project.

    """

    def _get_level_name(self, name):
        """Get the name with a colon added to the end."""
        return name

# Classes


class LoggingHelper(object):
    """A friendly helper for logging setup.

    .. code-block:: python

        # In the first file to be loaded.
        from commonkit.logging import LoggingHelper

        logger = LoggingHelper(level=logging.DEBUG, path="tmp.log")
        logger.setup()

        # In any file where logging occurs.
        root_logger = logging.getLogger()
        root_logger.debug('This is a debug message just for you.')
        root_logger.info('This message is purely informational.')
        root_logger.warning('You better watch out!')
        root_logger.error('Something bad has happened.')
        root_logger.critical('Something even worse has happened.')

    """

    def __init__(self, colorize=True, console=True, level=logging.INFO, name=None, path=None, success=False):
        """Initialize a logging helper.

        :param colorize: Indicates whether color should be used for console output.
        :type colorize: bool

        :param console: Indicates whether console logging should be enabled.
        :type console: bool

        :param level: The logging level to use.
        :type level: int

        :param name: The name of the logger.
        :type name: str

        :param path: The path, if any, for log file output.
        :type path: str

        """
        self.colorize = colorize
        self.console = console
        self.level = level
        self.name = name
        self.path = path
        self.success_enabled = success

    @property
    def color_enabled(self):
        # Do nothing more if colorize was given as False.
        if self.colorize is False:
            return False

        # Check the platform.
        return Platform(sys).supports_color

    def get_console_formatter(self):
        """Get the formatter used for console output."""
        if self.color_enabled:
            return ColorFormatter()
        else:
            return PlainTextFormatter()

    # noinspection PyMethodMayBeStatic
    def get_file_formatter(self):
        """Get the formatter used for log file output.

        By default, this returns an instance of :py:class:`FileFormatter`. Sub-classes may override this to specify
        their own formatter for log file output.

        """
        return FileFormatter()

    def setup(self):
        """Set up the logger.

        :rtype: logging.Logger

        """
        if self.success_enabled:
            logging.setLoggerClass(SuccessLogger)
            logging.addLevelName(15, "SUCCESS")

        logger = logging.getLogger(self.name)

        if self.console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.get_console_formatter())
            logger.addHandler(console_handler)

        if self.path:
            file_handler = logging.FileHandler(self.path)
            file_handler.setFormatter(self.get_file_formatter())
            logger.addHandler(file_handler)

        logger.setLevel(self.level)

        return logger


class SuccessLogger(DefaultLogger):

    def success(self, message, *args, **kwargs):
        """Log a success message."""
        self._log(15, message, args, **kwargs)
        # self.log(15, message, *args, **kwargs)
