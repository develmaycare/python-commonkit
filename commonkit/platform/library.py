# Imports

import os

# Classes


class Platform(object):
    """Represents the platform and working environment in which the code is currently running."""

    def __init__(self, system):
        """Create an instance representing the current platform.

        :param system: The local sys module.

        .. code-block:: python

            import sys

            platform = Platform(sys)

            if platform.is_linux:
                print("Linux!")
            elif platform.is_osx:
                print("OS X!")
            elif platform.is_windows:
                print("Windows!")
            else:
                print("No idea!")

        """
        self.system = system

    # def get_distribution(self):
    #     """Get the name of the operating system distribution.
    #
    #     :rtype: str
    #
    #     """
    #     output = platform.platform().lower()
    #     if "centos" in output:
    #         return "centos"
    #     elif "darwin" in output:
    #         return "darwin"
    #     elif "debian" in output:
    #         return "debian"
    #     elif "fedora" in output:
    #         return "fedora"
    #     elif "redhat" in output:
    #         return "redhat"
    #     elif "ubuntu" in output:
    #         return "ubuntu"
    #     else:
    #         return "unknown"

    def get_configuration_path(self):
        """Get the platform's specific path for persistent configuration files that should be writable by any
        application.

        :rtype: str

        """
        if self.is_linux:
            path = "~/.config"
        elif self.is_osx:
            path = "~/Library/Application Support"
        elif self.is_windows:
            path = "~/AppData/Roaming"
        else:
            raise NotImplementedError("Unrecognized platform: %s" % self.system.platform)

        return os.path.expanduser(path)

    def get_temp_path(self):
        """Get the platform's specific path for temporary data that should be writable by any application.

        :rtype: str

        """
        if self.is_linux:
            path = "~/.cache"
        elif self.is_osx:
            path = "~/Library/Caches"
        elif self.is_windows:
            path = "~/AppData/Locals"
        else:
            raise NotImplementedError("Unrecognized platform: %s" % self.system.platform)

        return os.path.expanduser(path)

    @property
    def is_linux(self):
        """Indicates this is a Linux operating system.

        :rtype: bool

        """
        return self.system.platform.startswith('linux')

    @property
    def is_osx(self):
        """Indicates this is a Mac OS (Darwin) operating system.

        :rtype: bool

        """
        return self.system.platform.startswith('darwin')

    @property
    def is_python2(self):
        """Indicates the current Python version is 2.

        :rtype: bool

        """
        return self.system.version_info.major == 2

    @property
    def is_python3(self):
        """Indicates the current Python version is 3.

        :rtype: bool

        """
        return self.system.version_info.major == 3

    @property
    def is_windows(self):
        """Indicates this is a Windows operating system.

        :rtype: bool

        """
        return self.system.platform.startswith('win32')

    @property
    def supports_color(self):
        """Indicates whether the current system supports terminal colors.

        :rtype: bool

        Code adapted from ``pelican`` and in turn ``django.core.management.color``.

        """
        if "ANSICON" in os.environ:
            return False

        if self.is_windows:
            return False

        # Check atty, but this is not always implemented. See #6223.
        is_a_tty = hasattr(self.system.stdout, 'isatty') and self.system.stdout.isatty()
        if not is_a_tty:
            return False

        # Assume all of platforms support color.
        return True
