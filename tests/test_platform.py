import contextlib
import os
from commonkit.platform import Platform
import unittest
# noinspection PyCompatibility
from unittest.mock import MagicMock, patch

# Helpers


@contextlib.contextmanager
def modified_environ(**environ):
    """Temporarily modify environment variables.

    :param environ: The modified environment.

    """
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)

# Tests


class TestDarwinPlatform(unittest.TestCase):

    def setUp(self):
        self.sys = MagicMock()
        self.sys.configure_mock(platform="darwin")

    def test_get_configuration_path(self):
        """Check the path for persistent application data on OS X."""
        platform = Platform(self.sys)

        self.assertTrue("Library/Application Support" in platform.get_configuration_path())

    def test_get_temp_path(self):
        """Check the path for temporary application data on OS X."""
        platform = Platform(self.sys)

        self.assertTrue("Library/Caches" in platform.get_temp_path())

    def test_is(self):
        """Check that system identification works as expected on OS X."""
        platform = Platform(self.sys)

        self.assertFalse(platform.is_linux)
        self.assertTrue(platform.is_osx)
        self.assertFalse(platform.is_windows)

    def test_supports_color(self):
        """Check that color support works as expected on OS X."""
        platform = Platform(self.sys)

        self.assertTrue(platform.supports_color)


class TestLinuxPlatform(unittest.TestCase):

    def setUp(self):
        self.sys = MagicMock()
        self.sys.configure_mock(platform="linux")

    def test_get_configuration_path(self):
        """Check the path for persistent application data on Linux."""
        platform = Platform(self.sys)

        self.assertTrue(".config" in platform.get_configuration_path())

    def test_get_temp_path(self):
        """Check the path for temporary application data on Linux."""
        platform = Platform(self.sys)

        self.assertTrue(".cache" in platform.get_temp_path())

    def test_is(self):
        """Check that system identification works as expected on Linux."""
        platform = Platform(self.sys)

        self.assertTrue(platform.is_linux)
        self.assertFalse(platform.is_osx)
        self.assertFalse(platform.is_windows)

    def test_supports_color(self):
        """Check that color support works as expected on Linux."""
        platform = Platform(self.sys)

        self.assertTrue(platform.supports_color)


class TestPythonVersion(unittest.TestCase):

    def setUp(self):
        self.sys = MagicMock()
        self.sys.configure_mock(platform="darwin")

    def test_is_python(self):
        """Check that Python version identification works as expected."""
        platform = Platform(self.sys)

        # noinspection PyUnresolvedReferences
        with patch.object(self.sys, "version_info") as version_info:
            version_info.major = 2
            self.assertTrue(platform.is_python2)

        # noinspection PyUnresolvedReferences
        with patch.object(self.sys, "version_info") as version_info:
            version_info.major = 3
            self.assertTrue(platform.is_python3)


class TestUnrecognizedPlatform(unittest.TestCase):

    def setUp(self):
        self.sys = MagicMock()
        self.sys.configure_mock(platform="whatzit")

        class FakeStdOut(object):
            # noinspection PyMethodMayBeStatic
            def isatty(self):
                return False

        self.sys.stdout = FakeStdOut()

    def test_get_configuration_path(self):
        """Check the path for persistent application data for an unrecognized operating system."""
        platform = Platform(self.sys)

        self.assertRaises(NotImplementedError, platform.get_configuration_path)

    def test_get_temp_path(self):
        """Check the path for temporary application data for an unrecognized operating system."""
        platform = Platform(self.sys)

        self.assertRaises(NotImplementedError, platform.get_temp_path)

    def test_is(self):
        """Check that system identification works as expected for an unrecognized operating system."""
        platform = Platform(self.sys)

        self.assertFalse(platform.is_linux)
        self.assertFalse(platform.is_osx)
        self.assertFalse(platform.is_windows)

    def test_supports_color(self):
        """Check that color support does not work for ANSICON."""
        platform = Platform(self.sys)

        with modified_environ(ANSICON="present"):
            self.assertFalse(platform.supports_color)

        self.assertFalse(platform.supports_color)


class TestWindowsPlatform(unittest.TestCase):

    def setUp(self):
        self.sys = MagicMock()
        self.sys.configure_mock(platform="win32")

    def test_get_configuration_path(self):
        """Check the path for persistent application data on Windows."""
        platform = Platform(self.sys)

        self.assertTrue("Roaming" in platform.get_configuration_path())

    def test_get_temp_path(self):
        """Check the path for temporary application data on Windows."""
        platform = Platform(self.sys)

        self.assertTrue("Locals" in platform.get_temp_path())

    def test_is(self):
        """Check that system identification works as expected on Windows."""
        platform = Platform(self.sys)

        self.assertFalse(platform.is_linux)
        self.assertFalse(platform.is_osx)
        self.assertTrue(platform.is_windows)

    def test_supports_color(self):
        """Check that color support does not work for Windows."""
        platform = Platform(self.sys)

        self.assertFalse(platform.supports_color)
