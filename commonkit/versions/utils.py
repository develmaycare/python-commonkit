# Imports

from commonkit import read_file
import os
from .library import Version

# Exports

__all__ = (
    "bump_version",
    "get_current_version",
)

# Functions


def bump_version(current, build=None, major=False, minor=False, patch=False, status=None):
    """Bump the version.

    :param current: The current version.
    :type current: str

    :param build: The value of the build name.
    :type build: str

    :param major: Indicates major version should be increased. Minor and patch are reset to 0.
    :type major: bool

    :param minor: Indicates minor version should be increased. Patch is reset to 0.
    :type minor: bool

    :param patch: Indicates the patch level should be increased.

    :param status: The value of the pre-release identifier.
    :type status: str

    :rtype: str

    :returns: The new version).

    """
    # Create an instance for the current version.
    version = Version(current)

    # Create an instance for the new version.
    new_version = version.bump(
        major=major,
        minor=minor,
        patch=patch,
        status=status,
        build=build
    )

    return str(new_version)


def get_current_version(path=None):
    """Get the current version.

    :param path: The path to the version file.
    :type path: str

    :rtype: str
    :returns: The current version. If the version path does not exist, this will be ``0.1.0-p``.

    """
    _path = path or os.path.join(os.getcwd(), "VERSION.txt")
    if not os.path.exists(_path):
        return "0.1.0-p"

    return read_file(_path).strip()
