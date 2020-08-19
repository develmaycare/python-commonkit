from commonkit.database.backends.mssql import MSSQL
# from commonkit.database.backends.mysql import MYSQL
from commonkit.database.backends.oracle import Oracle
from commonkit.database.backends.pgsql import Postgres
from commonkit.database.backends.sqlite import SQLite
from commonkit.database.exceptions import UnknownDatabaseBackend
from commonkit.database.factory import load_backend, load_database
import pytest

# Tests


def test_load_backend():
    with pytest.raises(UnknownDatabaseBackend):
        load_backend("nonexistent", testing=True)


def test_load_database():

    connections = {
        'mssql': {
            'database': "testing",
            'password': "secret",
            'port': 1234,
        },
        # 'mysql': {
        #     'database': "testing",
        #     'password': "secret",
        #     'port': 1234,
        # },
        'oracle': {
            'database': "testing",
            'password': "secret",
            'user': "admin",
        },
        'postgres': {
            'database': "testing",
            'password': "secret",
        },
        'sqlite': {
            'path': "tmp.db",
        }
    }

    db = load_database("mssql", **connections['mssql'])
    assert isinstance(db.backend, MSSQL)

    # db = load_database("mysql", **connections['mysql'])
    # assert isinstance(db.backend, MYSQL)

    db = load_database("oracle", **connections['oracle'])
    assert isinstance(db.backend, Oracle)

    db = load_database("pgsql", **connections['postgres'])
    assert isinstance(db.backend, Postgres)

    db = load_database("sqlite", **connections['sqlite'])
    assert isinstance(db.backend, SQLite)

    db = load_database("nonexistent", testing=True)
    assert db is None
