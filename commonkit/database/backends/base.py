# Imports

from sqlalchemy import create_engine, exc, inspect
from ..library import Session

# Exports

__all__ = (
    "Backend",
)

# Classes


class Backend(object):
    """Base class for defining a database backend."""

    def __init__(self, **kwargs):
        """Initialize the backend.

        kwargs are used to initialize the engine.

        """
        self.connection = None
        self.is_open = False
        self.params = kwargs

        # TODO: What exceptions may be raised on create_engine()?
        self.engine = create_engine(self._get_url())

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.disconnect()

    def __getattr__(self, item):
        return self.params.get(item)

    def __repr__(self):
        _open = "closed"
        if self.is_open:
            _open = "open"

        return "<%s %s>" % (self.__class__.__name__, _open)

    def connect(self):
        """Connect to the database."""
        self.connection = self.engine.connect()

        self.is_open = True

    def disconnect(self):
        """Close the database connection."""
        self.engine.dispose()
        self.is_open = False

    def get_database_name(self):
        """Get the name of the database.

        :rtype: str

        """
        if "database" in self.params:
            return self.params['database']

        return "unknown"

    def get_table_names(self):
        """Get the tables from the database.

        :rtype: list[str]

        """
        return inspect(self.engine).get_table_names()

    def get_session(self):
        """Get a session to use for running queries.

        :rtype: Session

        """
        if not self.is_open:
            raise exc.ResourceClosedError("Database is not open.")

        return Session(self.connection)

    @property
    def type(self):
        """Get the type of backend.

        :rtype: str

        """
        return self.__class__.__name__.lower()

    def _get_url(self):
        """Get the connection URL.

        :rtype: str

        """
        raise NotImplementedError()
