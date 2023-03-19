# Imports

import semver
from .constants import STAGE

# Exports

__all__ = (
    "Compare",
    "Version",
)

# Classes


class Compare(object):
    """Convenience class for comparing two versions.

    See https://python-semver.readthedocs.io/en/latest/usage/compare-versions.html

    """

    def __init__(self, version1, version2):
        """Initialize the comparison.

        :param version1: The first version.
        :type version1: str

        :param version2: The second version.
        :type version2: str

        """
        self.compare = semver.compare(version1, version2)
        self.version1 = version1
        self.version2 = version2

    @property
    def is_equal_to(self):
        """Indicates the two version are the same.

        :rtype: bool

        """
        return self.compare == 0

    @property
    def is_greater_than(self):
        """Indicates version 1 is greater than version 2.

        :rtype: bool

        """
        return self.compare == 1

    @property
    def is_less_than(self):
        """Indicates version 1 is less than version 2.

        :rtype: bool

        """
        return self.compare == -1


class Version(object):
    """Represents a version/release string."""

    def __init__(self, identifier):
        """Initialize a version.

        :param identifier: The version string in semver.org format.
        :type identifier: str

        """
        self.identifier = identifier
        self._current = semver.VersionInfo.parse(identifier)

        self._new = self._current

    def __str__(self):
        return self.identifier

    @property
    def build(self):
        """Get the current build name."""
        return self._current.build

    def bump(self, build=None, major=False, minor=False, patch=False, status=None):
        """Bump the version.

        :param build: The value of the build name.
        :type build: str

        :param major: Indicates major version should be increased. Minor and patch are reset to 0.
        :type major: bool

        :param minor: Indicates minor version should be increased. Patch is reset to 0.
        :type minor: bool

        :param patch: Indicates the patch level should be increased.

        :param status: The value of the pre-release identifier.
        :type status: str

        :rtype: commonkit.version.library.Version
        :returns: The new version.

        """

        # Get the new version.
        if major:
            new_version = str(self._new.bump_major())
            # new_version = semver.VersionInfo.bump_major(self.identifier)
        elif minor:
            new_version = str(self._new.bump_minor())
            # new_version = semver.bump_minor(self.identifier)
        elif patch:
            new_version = str(self._new.bump_patch())
            # new_version = semver.bump_patch(self.identifier)
        else:
            new_version = self.identifier

        # Update the status.
        _status = None
        if status is not None:
            if len(status) == 0:
                pass
            else:
                _status = status
        else:
            _status = self._current.prerelease

        if _status:
            info = semver.VersionInfo.parse(new_version)

            new_version = "%s.%s.%s-%s" % (
                info.major,
                info.minor,
                info.patch,
                _status
            )

        # Update the build.
        if build:
            info = semver.VersionInfo.parse(new_version)

            new_version = "%s.%s.%s" % (info.major, info.minor, info.patch)
            if info.prerelease:
                new_version += "-%s" % info.prerelease

            new_version += "+%s" % build

        # Return the new version.
        return Version(new_version.strip())

    def get_stage(self):
        """Get the named development stage of the version.

        :rtype: str

        """
        if not self._current.prerelease:
            return STAGE.LIVE

        for name, identifier in STAGE.VERSION_IDENTIFIERS.items():
            if self._current.prerelease == identifier:
                return name

        return "unknown"

    @property
    def major(self):
        """Get the current major version."""
        return self._current.major

    @property
    def minor(self):
        """Get the current minor version."""
        return self._current.minor

    @property
    def patch(self):
        """Get the current patch level."""
        return self._current.patch

    @property
    def pep440(self):
        """Get the PEP440 version."""
        return "%s.%s.%s" % (self._current.major, self._current.minor, self._current.patch)

    @property
    def status(self):
        """Get the current pre-release status."""
        return self._current.prerelease
