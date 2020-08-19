from commonkit.lists.library import *

# Tests


def test_any_list_item():
    a = [1, 2, 3]
    b = [3, 4, 5]
    assert any_list_item(a, b) is True
    
    a = [1, 2, 3]
    b = [4, 5, 6]
    assert any_list_item(a, b) is False


def test_split_csv():
    a = "1, yes, 17.5, testing"
    b = split_csv(a)

    assert isinstance(b, list)
    assert isinstance(b[0], int)
    assert isinstance(b[1], bool)
    assert isinstance(b[2], float)
    assert isinstance(b[3], str)
