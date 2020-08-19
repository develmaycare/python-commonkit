# Imports

import os

# Exports

__all__ = (
    "get_modified_times",
    "Watcher",
)

# Functions


def get_modified_times(path, extensions=None, follow_symlinks=True):
    """Get the modified times for all files within a given path.

    :param path: The path to the files.
    :type path: str

    :param extensions: A list of extensions (including the dot) to be watched. If omitted, all extensions are watched.
                       This parameter is optional, but recommended.
    :type extensions: list[str]

    :param follow_symlinks: Indicates whether symlinks should be followed.
    :type follow_symlinks: bool

    :rtype: collections.Iterable(time)
    :returns: Yields the last modified timestamp of each file.

    """
    for root, dirs, files in os.walk(path, followlinks=follow_symlinks):
        for f in files:
            if extensions is not None:
                if f.endswith(tuple(extensions)):
                    path = os.path.join(root, f)
                    try:
                        yield os.stat(path).st_mtime
                    except OSError:
                        pass
            else:
                path = os.path.join(root, f)
                try:
                    yield os.stat(path).st_mtime
                except OSError:
                    pass


# Classes


class Watcher(object):
    """A watcher may be used to determine if the contents of a directory or file has changed."""

    def __init__(self, path, extensions=None, follow_symlinks=True):
        """Initialize a watcher.

        :param path: The path to be watched. This may be a file or directory.
        :type path: str

        :param extensions: A list of extensions (including the dot) to be watched when ``path`` is a directory. If
                           omitted, all extensions are watched. This parameter is optional, but recommended.
        :type extensions: list[str]

        :param follow_symlinks: Indicates whether symlinks should be followed.
        :type follow_symlinks: bool

        """
        self.errors = list()
        self.extensions = extensions
        self.follow_symlinks = follow_symlinks
        self.last_modified_time = 0
        self.path = path
        self._is_directory = os.path.isdir(path)
        self._is_file = os.path.isfile(path)

    @property
    def exists(self):
        """Indicates whether the watched path exists.

        :rtype: bool

        """
        return os.path.exists(self.path)

    @property
    def is_directory(self):
        """Indicates the path is a directory.

        :rtype: bool

        """
        return self._is_directory

    @property
    def is_file(self):
        """Indicates the path is a file.

        :rtype: bool

        """
        return self._is_file

    def watch(self):
        """Watch the path for changes.

        :rtype: collections.Iterable(bool| None)
        :returns: ``True`` when the path has changed.

        Watches the ``path`` for changes, trapping any errors encountered. It yields ``True`` or ``False`` to indicate
        a change (or not), or ``None`` when an error is encountered.

        """
        if self.is_directory:
            while True:
                try:
                    modified_time = max(get_modified_times(
                        self.path,
                        extensions=self.extensions,
                        follow_symlinks=self.follow_symlinks)
                    )
                    if modified_time > self.last_modified_time:
                        self.last_modified_time = modified_time
                        yield True
                except ValueError as e:
                    self.errors.append("Directory watcher failed: %s (%s)" % (self.path, e))
                    yield None
                else:
                    yield False
        elif self.is_file:
            while True:
                try:
                    modified_time = os.stat(self.path).st_mtime
                except OSError as e:
                    self.errors.append("File watcher failed: %s (%s)" % (self.path, e))
                    yield None

                if modified_time > self.last_modified_time:
                    self.last_modified_time = modified_time
                    yield True
                else:
                    yield False
        else:
            raise ValueError("%s is not a file or directory." % self.path)
