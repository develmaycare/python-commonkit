# Imports

from .backends.oracle import Oracle
from .backends.mssql import MSSQL
# from .backends.mysql import MYSQL
from .backends.pgsql import Postgres
from .backends.sqlite import SQLite
from .library import Database
from .exceptions import UnknownDatabaseBackend

# Exports

__all__ = (
    "load_backend",
    "load_database",
)

# Functions


def load_backend(name, **kwargs):
    """Load the named backend.

    :param name: The name of the backend to load.
    :type name: str

    kwargs are passed to instantiate the backend.

    :rtype: BaseType[Backend]
    :raises: UnknownDatabaseBackend

    """
    if name == "oracle":
        return Oracle(**kwargs)
    elif name == "mssql":
        return MSSQL(**kwargs)
    # elif name == "mysql":
    #     return MYSQL(**kwargs)
    elif name in ("pgsql", "psql", "postgres", "postgresql"):
        return Postgres(**kwargs)
    elif name == "sqlite":
        return SQLite(**kwargs)
    else:
        raise UnknownDatabaseBackend("Invalid or unsupported backend: %s" % name)


def load_database(backend, database_class=Database, debug=False, log=None, prefix=None, **kwargs):
    """Load the named backend.

    :param backend: The name of the backend to load.
    :type backend: str

    :param database_class: The class to use for database instantiation.

    :param debug: Indicates whether debug mode is enabled.
    :type debug: bool

    :param log: A logging instance to use rather than printing debug statements.
    :type log: logging.Logger

    :param prefix: A prefix to be added to table names.
    :type prefix: str

    kwargs are passed to instantiate the backend. See ``load_backend()``.

    :rtype: Database | None

    """
    try:
        _backend = load_backend(backend, **kwargs)
        return database_class(_backend, debug=debug, log=log, prefix=prefix)
    except UnknownDatabaseBackend:
        return None
