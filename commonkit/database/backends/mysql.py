# Imports

from .base import Backend

# Exports

__al__ = (
    "MYSQL",
)

# Classes


class MYSQL(Backend):
    """A backend for MySQL."""

    def __init__(self, database=None, host="localhost", password=None, port=None, user="root"):
        """Initialize the backend.

        :param database: The database name.
        :type database: str

        :param host: The host name or IP address.
        :type host: str

        :param password: The database password.
        :type password: str

        :param port: The database port to use for the connection.
        :type port: int

        :param user: The database user name.
        :type user: str

        """
        super().__init__(
            database=database or user,
            host=host,
            password=password,
            port=port,
            user=user
        )

    def _get_url(self):
        """Get the specific URL."""
        a = list()
        a.append("mysql://%s" % self.user)
        if self.password is not None:
            a.append(":%s" % self.password)

        a.append("@%s" % self.host)

        if self.port is not None:
            a.append(":%s" % self.port)

        a.append("/%s" % self.database)

        return "".join(a)
