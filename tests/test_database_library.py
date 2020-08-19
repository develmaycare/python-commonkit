from collections import OrderedDict
from commonkit.database.backends.sqlite import SQLite
# from commonkit.database.constants import EXPORT_FORMAT
from commonkit.database.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from commonkit.database.library import *
import os
import pytest
from tablib import Dataset


class FakeLog(object):

    def info(self, message):
        pass


backend = SQLite(path=os.path.join("tests", "tmp.db"))
db = Database(backend, debug=True, prefix="test")

# Tests


class TestDatabase(object):
    
    def test_average(self, database_handle):
        """Check that average is correctly calculated."""
        db.log = FakeLog()
        result = db.average("popularity", "page")
        assert result.error is None
        assert result.aggregate == 2.0
        db.log = None

        assert repr(result) == "<Result SELECT avg(popularity) AS agg FROM test_page;>"

    def test_count(self, database_handle):
        """Check the count is correctly calculated."""
        result = db.count("page")
        assert result.error is None
        assert result.aggregate == 3

        # noinspection PyTypeChecker
        result = db.count("page", popularity=1.0)
        assert result.error is None
        assert result.aggregate == 1

    def test_delete(self, database_handle):
        """Check that record deletion works."""
        result = db.insert("page", {'title': "Delete This Page"})
        assert result.error is None

        # noinspection PyTypeChecker
        result = db.delete("page", title="Delete This Page")
        assert result.error is None
        assert result.count == 1

    def test_expression(self, database_handle):
        """Test the use of expressions in select and aggregate queries."""
        # noinspection PyTypeChecker
        result = db.count("page", popularity=Expression(">", 1.0))
        assert result.aggregate == 2

        # noinspection PyTypeChecker
        result = db.select("page", popularity=Expression(">", 1.0))
        assert result.count == 2

    def test_fetch(self, database_handle):
        """Test that fetch returns results as expected."""
        # This should return a single result (Page instance)
        # noinspection PyTypeChecker
        page = db.fetch("page", id=1)
        assert isinstance(page, Row)
        assert page.id == 1

        # This should raise an ObjectDoesNotExist.
        with pytest.raises(ObjectDoesNotExist):
            db.fetch("page", id=99)

        # This should raise a MultipleObjectsReturned.
        with pytest.raises(MultipleObjectsReturned):
            db.fetch("page")

    def test_insert(self, database_handle):
        """Check that record insertion works."""
        result = db.insert("page", {'title': "Delete This Page"})
        assert result.error is None

        # noinspection PyTypeChecker
        result = db.delete("page", title="Delete This Page")
        assert result.error is None
        assert result.count == 1

    def test_max(self, database_handle):
        """Check that max is correctly calculated."""
        result = db.max("popularity", "page")
        assert result.error is None
        assert result.aggregate == 3.0

    def test_min(self, database_handle):
        """Check that min is correctly calculated."""
        result = db.min("popularity", "page")
        assert result.error is None
        assert result.aggregate == 1.0

    def test_prefix_table(self):
        """Check that an unprefixed table just returns the name."""
        db.prefix = None
        table = db._prefix_table("testing")
        assert table == "testing"

        db.prefix = "test"

    def test_raw(self, database_handle):
        """Check that a raw query works."""
        result = db.raw("SELECT * FROM test_page")
        assert result.error is None

    def test_repr(self):
        assert repr(db) == "<Database sqlite:tmp.db>"

    def test_select(self, database_handle):
        """Check that a select query works."""
        result = db.select("page", limit=2, order_by="title")
        assert result.error is None
        assert result.count == 2

        # noinspection PyTypeChecker
        result = db.select("page", title="Page 1")
        assert result.error is None
        assert result.count == 1

        result = db.select("page")
        assert result.error is None
        assert result.count == 3

        for row in result.rows:
            assert isinstance(row, Row)

    def test_sum(self, database_handle):
        """Check that sum is correctly calculated."""
        result = db.sum("popularity", "page")
        assert result.error is None
        assert result.aggregate == 6.0

    def test_update(self, database_handle):
        """Check that record updating works."""
        # noinspection PyTypeChecker
        result = db.update("page", {'title': "Page 3 Updated"}, id=3)
        assert result.error is None
        assert result.count == 1

        result = db.update("page", {'title': "Page 3"}, title=Expression("=", "Page 3 Updated"))
        assert result.error is None
        assert result.count == 1


class TestRow(object):

    def test_dir(self, database_handle):
        row = db.fetch("page", id=1)
        assert type(row.__dir__()) is list

    def test_getattr(self, database_handle):
        row = db.fetch("page", id=1)
        assert row.title == "Page 1"
        with pytest.raises(AttributeError):
            none = row.nonexistent

    def test_repr(self, database_handle):
        row = db.fetch("page", id=1)
        assert repr(row) == "<Row 9>"

    def test_as_dataset(self, database_handle):
        row = db.fetch("page", id=1)
        assert isinstance(row.as_dataset(), Dataset)

    def test_as_dict(self, database_handle):
        row = db.fetch("page", id=1)
        d = row.as_dict()
        assert type(d) is dict
        assert "title" in d
        assert d['title'] == "Page 1"

    def test_as_ordered_dict(self, database_handle):
        row = db.fetch("page", id=1)
        d = row.as_ordered_dict()
        assert type(d) is OrderedDict
        assert "title" in d
        assert d['title'] == "Page 1"

    def test_get(self, database_handle):
        row = db.fetch("page", id=1)
        assert row.get("title") == "Page 1"
        assert row.get("nonexistent", default="testing") == "testing"

    def test_export(self, database_handle):
        row = db.fetch("page", id=1)
        assert type(row.export()) is str

    def test_has(self, database_handle):
        row = db.fetch("page", id=1)
        assert row.has("title") is True


class TestSession(object):

    def test_aggregate(self, database_handle):
        result = db.count("nonexistent")
        assert result.error is not None

    def test_query(self, database_handle):
        result = db.select("nonexistent")
        assert result.error is not None

    def test_raw(self, database_handle):
        result = db.raw("SELECT * FROM nonexistent")
        assert result.error is not None

    def test_repr(self):
        db.backend.connect()
        session = db.backend.get_session()
        assert repr(session) == "<Session>"
        db.backend.disconnect()


class TestSet(object):

    def test_as_dataset(self, database_handle):
        result = db.select("page", id=99)
        assert isinstance(result.rows.as_dataset(), Dataset)

        result = db.select("page")
        assert isinstance(result.rows.as_dataset(), Dataset)

    def test_as_dict(self, database_handle):
        result = db.select("page")
        d = result.rows.as_dict()
        assert type(d) is list
        assert type(d[0]) is dict

    def test_as_ordered_dict(self, database_handle):
        result = db.select("page")
        d = result.rows.as_ordered_dict()
        assert type(d) is list
        assert type(d[0]) is OrderedDict

    def test_export(self, database_handle):
        result = db.select("page", )
        assert type(result.rows.export()) is str

    def test_next(self, database_handle):
        db.backend.connect()
        with db.backend.get_session() as session:
            result = session.query("SELECT * FROM test_page;")
            row = result.rows.next()
            assert isinstance(row, Row)

        db.backend.disconnect()

    def test_repr(self, database_handle):
        result = db.select("page")
        assert repr(result.rows) == "<Set 3>"
