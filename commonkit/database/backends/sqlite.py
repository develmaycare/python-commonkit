# Imports

import os
from .base import Backend

# Exports

__all__ = (
    "SQLite",
)

# Classes


class SQLite(Backend):
    """A backend for SQLite."""

    def __init__(self, path=None, **kwargs):
        """Initialize and SQL database.

        :param path: The path to the database file or ``memory`` for in-memory.
        :type path: str

        """
        _path = path or "tmp.db"
        super().__init__(path=_path, **kwargs)

    def get_database_name(self):
        """Override to return the base name of the path.

        :rtype: str

        """
        if self.path == "memory":
            return "memory"

        return os.path.basename(self.path)

    def _get_url(self):
        """Get the specific URL."""
        if self.path == "memory":
            return "sqlite://"

        return "sqlite:///%s" % self.path
