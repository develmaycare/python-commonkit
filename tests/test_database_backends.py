from commonkit.database.backends.base import Backend
from commonkit.database.backends.mssql import MSSQL
# from commonkit.database.backends.mysql import MYSQL
from commonkit.database.backends.oracle import Oracle
from commonkit.database.backends.pgsql import Postgres
from commonkit.database.backends.sqlite import SQLite
from commonkit.database.exceptions import ResourceClosedError
from commonkit.database.library import Session
import os
import pytest


class Fake(Backend):

    def _get_url(self):
        return "sqlite:///%s" % self.path


# Tests


class TestBackend(object):

    def test_enter(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        assert isinstance(b.__enter__(), Fake)

    def test_exit(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        b.connect()
        b.__exit__(None, None, None)
        assert b.is_open is False

    def test_getattr(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        assert b.path == "tests/tmp.db"

    def test_get_database_name(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        assert b.get_database_name() == "unknown"

        b.params['database'] = "tmp.db"
        assert b.get_database_name() == "tmp.db"

    def test_get_table_names(self, database_handle):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        tables = b.get_table_names()
        assert type(tables) is list
        assert "test_page" in tables

    def test_repr(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        assert repr(b) == "<Fake closed>"
        b.is_open = True
        assert repr(b) == "<Fake open>"

    def test_get_session(self, database_handle):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        with pytest.raises(ResourceClosedError):
            b.get_session()

        b.connect()
        session = b.get_session()
        assert isinstance(session, Session)

    def test_get_url(self):
        with pytest.raises(NotImplementedError):
            b = Backend()

    def test_type(self):
        path = os.path.join("tests", "tmp.db")
        b = Fake(path=path)
        assert b.type == "fake"


class TestMSSQL(object):

    def test_get_url(self):
        b = MSSQL(database="testing", password="secret", port=1234)
        assert b._get_url() == "mssql+pyodbc://admin:secret@localhost:1234/testing"


# class TestMYSQL(object):
# 
#     def test_get_url(self):
#         b = MYSQL(database="testing", password="secret", port=1234)
#         assert b._get_url() == "mysql//root:secret@localhost:1234/testing"


class TestOracle(object):
    
    def test_get_url(self):
        b = Oracle(database="testing", password="secret", user="admin")
        assert b._get_url() == "oracle://admin:secret@localhost:1521/testing"


class TestPostgres(object):

    def test_get_url(self):
        b = Postgres(database="testing", password="secret")
        assert b._get_url() == "postgresql://postgres:secret@localhost:5432/testing"


class TestSQLite(object):

    def test_get_database_name(self):
        b = SQLite()
        assert b.get_database_name() == "tmp.db"

        b = SQLite(path="memory")
        assert b.get_database_name() == "memory"

    def test_get_url(self):
        b = SQLite()
        assert b._get_url() == "sqlite:///tmp.db"

        b = SQLite(path="memory")
        assert b._get_url() == "sqlite://"
