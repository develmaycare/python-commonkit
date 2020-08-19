from commonkit.math.library import *

# Tests


def test_add():
    # No different than sum.
    s = add([1, 1, 1])
    assert s == 3

    s = add([1, 1, 1], base=2)
    assert s == 5

    s = add([1, 1.1, 1.2])
    assert s == 3.3


def test_average():
    """Check that averaging works as expected."""
    a = average([1, 2, 3, 4, 5])
    assert a == 3
    assert isinstance(a, float)

    a = average([1.1, 2.2, 3.3, 4.4, 5.5])
    assert a == 3.3

    a = average([])
    assert a == 0.0

    a = average([0, 5, 0, 0, 3, 1, 15, 0, 12], lazy=True)
    assert a == 7.2


def test_median():
    m = median([1, 3, 5])
    assert m == 3

    m = median([1, 3, 5, 7])
    assert m == 4.0

    m = median([])
    assert m == None


def test_percentage():
    """Check that percentage calculations work as expected."""
    p = percentage(50, 100)
    assert isinstance(p, float) is True
    assert p == 50.0
    assert p == 50

    p = percentage(50, 150)
    assert p == 33.333333333333336

    p = percentage(50, 0)
    assert p == 0.0


def test_product():
    p = product([5, 5])
    assert p == 25

    p = product([5, 5, 5], base=2)
    assert p == 250
