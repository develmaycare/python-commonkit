import logging
from commonkit.logging import BaseFormatter, ColorFormatter, LoggingHelper
import os
import pytest

# See https://www.pythonhosted.org/testfixtures/logging.html for better testing?

# Tests


class TestBaseFormatter(object):
    """Pick up coverage for things no directly tested by TestLoggingHelper."""

    def test_format_exception(self):
        log = LoggingHelper()
        log.setup()

        with pytest.raises(RuntimeError):
            raise RuntimeError("This is a test of format exception.\nIt has more than one line in the error message.")

    def test_get_level_name(self):
        """Check that the level name returns the same name."""
        formatter = BaseFormatter()
        name = formatter._get_level_name("INFO")
        assert name == "INFO"


class TestColorFormatter(object):

    def test_get_level_name(self):
        formatter = ColorFormatter()
        output = formatter._get_level_name("INFO")
        assert "INFO" in output


class TestLoggingHelper(object):

    def test_setup_default(self, caplog):
        """Check the default friendly setup."""
        log = LoggingHelper()
        logger = log.setup()

        # formatter = log.get_console_formatter()
        # assert isinstance(formatter, ColorFormatter)

        # noinspection PyUnusedLocal
        with caplog.at_level(logging.DEBUG):
            logger.debug("test_setup_default() This is a debug message.")
            logger.info("test_setup_default() This message is informational.")
            logger.warning("test_setup_default() You better watch out!")
            logger.critical("test_setup_default() Something even worse has happened.")

        # TODO: This used to force a call to formatException(), but would fail if used with LogCapture. It seems to have
        # stopped working, and the only difference I can see is the virtual environment -- so a package change?
        logger.error("You can ignore this error.", exc_info=True)

    def test_setup_plain(self, caplog):
        """Check plain text friendly setup."""

        log = LoggingHelper(colorize=False)
        log.setup()

        logger = logging.getLogger()

        # Using LogCapture suppresses coverage.
        logger.info("test_setup_plain() This message is informational.")

        # noinspection PyUnusedLocal
        with caplog.at_level(logging.DEBUG):
            logger.debug("test_setup_plain() This is a debug message.")
            logger.info("test_setup_plain() This message is informational.")
            logger.warning("test_setup_plain() You better watch out!")
            logger.error("test_setup_plain() Something bad has happened.")
            logger.critical("test_setup_plain() Something even worse has happened.")

    def test_setup_path(self):
        """Check friendly setup for log file."""

        log_path = os.path.join("tests", "tmp.log")

        log = LoggingHelper(colorize=False, console=False, path=log_path)
        log.setup()

        logger = logging.getLogger()

        # Using LogCapture suppresses coverage.
        logger.debug("test_setup_path() This is a debug message.")
        logger.info("test_setup_path() This message is informational.")
        logger.warning("test_setup_path() You better watch out!")
        logger.error("test_setup_path() Something bad has happened.")
        logger.critical("test_setup_path() Something even worse has happened.")

        if os.path.exists(log_path):
            os.remove(log_path)


class TestSuccessLogger(object):

    def test_success(self):
        log = LoggingHelper(success=True, name="success-logger")
        logger = log.setup()

        # Using LogCapture suppresses coverage.
        logger.success("test_success() This is a success message.")
