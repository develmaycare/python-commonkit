from commonkit.lists.library import *

# Supporting


class Filterable(object):

    def __init__(self, label, tags):
        self.label = label
        self.tags = tags


class Sortable(object):

    def __init__(self, label, sort_order):
        self.label = label
        self.sort_order = sort_order

    def __repr__(self):
        return "%s:%s" % (self.sort_order, self.label)

# Tests


def test_any_list_item():
    a = [1, 2, 3]
    b = [3, 4, 5]
    assert any_list_item(a, b) is True
    
    a = [1, 2, 3]
    b = [4, 5, 6]
    assert any_list_item(a, b) is False


def test_filter_by():
    a = [
        Filterable("one", ["development", "testing"]),
        Filterable("two", ["testing", "staging"]),
        Filterable("three", ["live"]),
        Filterable("four", ["live"]),
        Filterable("five", ["live"]),
    ]
    b = filter_by("tags", a, "testing")
    assert len(b) == 2
    assert b[0].label == "one"
    assert b[1].label == "two"

    d = [
        {'label': "one", 'environment': "development"},
        {'label': "two", 'environment': "testing"},
        {'label': "three", 'environment': "staging"},
        {'label': "four", 'environment': "live"},
        {'label': "five", 'environment': "live"},
    ]
    e = filter_by("environment", d, "live")
    assert len(e) == 2

    e = filter_by("environment", d, ["live"])
    assert len(e) == 2


def test_flatten():
    a = [
        [1, 2],
        [3, 4, 5],
        [6, 7],
        [8, 9],
        [10],
    ]
    b = flatten(a)
    assert len(b) == 10

    c = []
    d = flatten(c)
    assert len(d) == 0


def test_safe_join():
    string = safe_join(",", [1, "two", 3.4, "five"])
    assert string == "1,two,3.4,five"

    string = safe_join(r"\n", [1, "two", 3.4, "five"])
    assert "1" in string
    assert "two" in string
    assert "3.4" in string
    assert "five" in string


def test_sort_by():
    a = [
        Sortable("five", 5),
        Sortable("two", 2),
        Sortable("one", 1),
        Sortable("four", 4),
        Sortable("three", 3),
    ]

    sort_by("sort_order", a)
    assert a[0].label == "one"
    assert a[-1].label == "five"

    b = [
        Sortable("five", 5),
        Sortable("two", 2),
        Sortable("one", 1),
        Sortable("four", 4),
        Sortable("three", 3),
    ]
    c = sort_by("sort_order", b, new=True, reverse=True)
    assert c is not None
    assert c[0].label == "five"
    assert c[-1].label == "one"

    d = [
        {'label': "five", 'sort_order': 5},
        {'label': "two", 'sort_order': 2},
        {'label': "one", 'sort_order': 1},
        {'label': "four", 'sort_order': 4},
        {'label': "three", 'sort_order': 3},
    ]
    sort_by("sort_order", d)
    assert d[0]['label'] == "one"
    assert d[-1]['label'] == "five"


def test_split_csv():
    a = "1, yes, 17.5, testing"
    b = split_csv(a)

    assert isinstance(b, list)
    assert isinstance(b[0], int)
    assert isinstance(b[1], bool)
    assert isinstance(b[2], float)
    assert isinstance(b[3], str)


def test_xor():
    assert xor(True, True, True, True) is False
    assert xor(True, True, True) is True
    assert xor(True, True, True, False) is True
    assert xor(True, True, True, False, True) is False
    assert xor(False, False, False, False) is False


class TestLoop(object):

    def test_iter(self):
        loop = Loop(["A", "B", "C", "D", "E", "F", "G"])
        for i in loop:
            if loop.is_first():
                assert i == "A"
            elif loop.is_last():
                assert i == "G"
            else:
                assert i in ("B", "C", "D", "E", "F")

    def test_len(self):
        loop = Loop(["A", "B", "C", "D", "E", "F", "G"])
        assert len(loop) == 7
