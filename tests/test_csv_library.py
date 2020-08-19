import os
from commonkit.files import read_csv
from commonkit.csv.library import *


class TestCSVFile(object):

    def test_init(self):
        path = os.path.join("tests", "data", "example-unnormalized-columns.csv")

        keyword_mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )
        csv = CSVFile(path, mapping=keyword_mapping)
        assert csv.first_row_field_names is True

        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path, mapping=AutoMapping())
        assert csv.first_row_field_names is True

        path = os.path.join("tests", "data", "example-no-columns.csv")
        csv = CSVFile(path)
        assert csv.first_row_field_names is False

    def test_exists(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path)
        assert csv.exists is True

        csv = CSVFile("nonexistent.csv")
        assert csv.exists is False

    def test_get_column_names(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path, mapping=AutoMapping())
        assert csv.read() is True
        columns = csv.get_column_names()
        assert "first_name" in columns
        assert "last_name" in columns
        assert "job_title" in columns
        assert "salary" in columns

        path = os.path.join("tests", "data", "example-unnormalized-columns.csv")
        keyword_mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )
        csv = CSVFile(path, mapping=keyword_mapping)
        columns = csv.get_column_names()
        assert "first_name" in columns
        assert "last_name" in columns
        assert "job_title" in columns
        assert "salary" in columns

        path = os.path.join("tests", "data", "example-no-columns.csv")
        index_mapping = IndexMapping(
            first_name=0,
            last_name=1,
            job_title=2,
            salary=3,
            nonexistent=99
        )
        csv = CSVFile(path, mapping=index_mapping)
        columns = csv.get_column_names()
        assert "first_name" in columns
        assert "last_name" in columns
        assert "job_title" in columns
        assert "salary" in columns

        path = os.path.join("tests", "data", "example-no-columns.csv")
        csv = CSVFile(path)
        assert csv.get_column_names() is None

    def test_iter(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path, mapping=AutoMapping())
        assert csv.read() is True
        count = 0
        for row in csv:
            count += 1

        assert count == 3

    def test_len(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path, mapping=AutoMapping())
        assert csv.read() is True
        assert len(csv) == 3

    def test_repr(self):
        csv = CSVFile("testing.csv")
        assert repr(csv) == "<CSVFile testing.csv>"

    def test_get_default_value(self):
        path = os.path.join("tests", "data", "example-bad-data.csv")
        csv = CSVFile(path, mapping=AutoMapping(), defaults={'job_title': "Unspecified"})
        assert csv.read() is True
        assert csv.get_default_value("job_title", None) == "Unspecified"

    def test_get_none_type_values(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path)
        assert "NA" in csv.get_none_type_values()

    def test_read(self):
        csv = CSVFile("path/to/nonexistent.csv")
        assert csv.read() is False

        path = os.path.join("tests", "data", "example-unnormalized-columns.csv")

        keyword_mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )
        csv = CSVFile(path, mapping=keyword_mapping, row_class=CSVRow)
        assert csv.read() is True

        path = os.path.join("tests", "data", "example-no-columns.csv")
        csv = CSVFile(path)
        assert csv.read() is True

    def test_smart_cast(self):
        path = os.path.join("tests", "data", "example.csv")
        csv = CSVFile(path, mapping=AutoMapping(), smart_cast_fields=["salary"])
        assert csv.read() is True

        assert csv.smart_cast("job_title", None, "NA") is None
        assert csv.smart_cast("job_title", None, "") is None
        assert csv.smart_cast("job_title", None, " ") is None
        assert csv.smart_cast("job_title", None, None) is None

        assert csv.smart_cast("salary", None, "100000") == 100000

        csv.defaults = {'job_title': "Unspecified"}
        assert csv.smart_cast("job_title", None, None) == "Unspecified"

        def cast_job_title(field_name, row, value):
            return value.title()

        csv.smart_cast_fields = {'job_title': cast_job_title}
        assert csv.smart_cast("job_title", None, "my job") == "My Job"

    def test_write(self):
        path = os.path.join("tests", "data", "tmp.csv")
        csv = CSVFile(path)
        csv.rows.append(["test 1", "test 2", "test 3"])
        csv.rows.append(["test 4", "test 5", "test 6"])
        csv.rows.append(["test 7", "test 8", "test 9"])
        csv.write()
        assert os.path.exists(path)
        os.remove(path)

        keyword_mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )
        csv = CSVFile(path, mapping=keyword_mapping)
        csv.rows.append({'first_name': "John", 'last_name': "Johnson", 'job_title': "CFO", 'salary': 100000})
        csv.rows.append({'first_name': "Jack", 'last_name': "Jackson", 'job_title': "CTO", 'salary': 110000})
        csv.rows.append({'first_name': "Ed", 'last_name': "Edwards", 'job_title': "CIO", 'salary': 100000})
        csv.write()
        assert os.path.exists(path)
        os.remove(path)

        keyword_mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )
        csv = CSVFile(path, mapping=keyword_mapping, row_class=CSVRow)
        csv.rows.append(CSVRow(**{'first_name': "John", 'last_name': "Johnson", 'job_title': "CFO", 'salary': 100000}))
        csv.rows.append(CSVRow(**{'first_name': "Jack", 'last_name': "Jackson", 'job_title': "CTO", 'salary': 110000}))
        csv.rows.append(CSVRow(**{'first_name': "Ed", 'last_name': "Edwards", 'job_title': "CIO", 'salary': 100000}))
        csv.write()
        assert os.path.exists(path)
        os.remove(path)


class TestCSVRow(object):

    def test_getattr(self):
        path = os.path.join("tests", "data", "example-no-columns.csv")
        mapping = IndexMapping(
            first_name=0,
            last_name=1,
            job_title=2,
            salary=3,
            nonexistent=99
        )
        csv = CSVFile(path, mapping=mapping, row_class=CSVRow, smart_cast_fields=["salary"])
        assert csv.read() is True

        for row in csv:
            assert isinstance(row, CSVRow)
            assert type(row.first_name) is str
            assert type(row.salary) is int


class TestAutoMapping(object):

    def test_get_values(self):
        path = os.path.join("tests", "data", "example.csv")
        rows = read_csv(path, first_row_field_names=True)

        mapping = AutoMapping()

        values = mapping.get_values(rows[0])
        assert values['first_name'] == "Bob"
        assert values['last_name'] == "White"
        assert values['job_title'] == "CEO"
        assert values['salary'] == "125000"

        path = os.path.join("tests", "data", "example-unnormalized-columns.csv")
        rows = read_csv(path, first_row_field_names=True)
        values = mapping.get_values(rows[0])
        assert values['first_name'] == "Bob"
        assert values['last_name'] == "White"
        assert values['job_title'] == "CEO"
        assert values['salary'] == "125000"


class TestIndexMapping(object):

    def test_get_values(self):
        path = os.path.join("tests", "data", "example-no-columns.csv")
        rows = read_csv(path)
        mapping = IndexMapping(
            first_name=0,
            last_name=1,
            job_title=2,
            salary=3,
            nonexistent=99
        )
        values = mapping.get_values(rows[0])
        assert values['first_name'] == "Bob"
        assert values['last_name'] == "White"
        assert values['job_title'] == "CEO"
        assert values['salary'] == "125000"
        assert values['nonexistent'] is None


class TestKeywordMapping(object):

    def test_get_values(self):
        path = os.path.join("tests", "data", "example-unnormalized-columns.csv")
        rows = read_csv(path, first_row_field_names=True)

        mapping = KeywordMapping(
            first_name="First Name",
            last_name="Last Name",
            job_title="Job Title",
            salary="Salary"
        )

        values = mapping.get_values(rows[0])
        assert values['first_name'] == "Bob"
        assert values['last_name'] == "White"
        assert values['job_title'] == "CEO"
        assert values['salary'] == "125000"
