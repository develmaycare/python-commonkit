# Imports

# noinspection PyUnresolvedReferences
from sqlalchemy.exc import OperationalError, ProgrammingError, ResourceClosedError

# Classes


class ImproperlyConfigured(Exception):
    """Indicates a problem with settings."""
    pass


class MultipleObjectsReturned(Exception):
    """Indicates a query for a specific record has instead identified multiple records."""
    pass


class ObjectDoesNotExist(Exception):
    """Indicates a query for a specific record has no match."""
    pass


class UnknownDatabaseBackend(Exception):
    """Indicates the given backend is unknown or unsupported."""
    pass
