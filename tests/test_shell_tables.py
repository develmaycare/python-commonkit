from commonkit.context_managers import captured_output
from commonkit.shell.tables import *

# Tests


class TestTable(object):

    def test_add(self):
        headings = [
            "Column 1",
            "Column 2",
            "Column 3",
        ]

        table = Table(headings=headings)
        table.add(["a", "b", "c"])
        table.add(["d", "e", "f"])
        table.add(["g", "h", "i"])

        assert 3 == len(table._rows)
        assert 2 == table._rows[1].number

    def test_iter(self):
        headings = [
            "Column 1",
            "Column 2",
            "Column 3",
        ]

        table = Table(headings=headings)
        table.add(["a", "b", "c"])
        table.add(["d", "e", "f"])
        table.add(["g", "h", "i"])

        for row in table:
            assert isinstance(row, Row) is True

            for value in row:
                assert isinstance(value, str) is True

    def test_str(self):
        headings = [
            "Column 1",
            "Column 2",
            "Column 3",
        ]

        table = Table(headings=headings)
        table.add(["a", "b", "c"])
        table.add(["d", "e", "f"])
        table.add(["g", "h", "i"])

        with captured_output() as (output, error):
            print(table)
            assert "Column 1" in output.getvalue()
            assert "---" in output.getvalue()

    def test_to_string(self):
        headings = [
            "Column 1",
            "Column 2",
            "Column 3",
        ]

        table = Table(headings=headings)
        table.add(["a", "b", "c"])
        table.add(["d", "e", "f"])
        table.add(["g", "h", "i"])

        output = table.to_string()
        assert "Column 1" in output
        assert "---" in output
