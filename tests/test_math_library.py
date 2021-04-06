from commonkit.math.library import *
import pytest

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


def test_difference():
    result = difference(1000, 1200)
    assert result == 18.18

    result = difference(1000, 1200, absolute=False)
    assert result == -18.18

    result = difference(0, 0)
    assert result == 0.0


def test_factors_of():

    with pytest.raises(TypeError):
        factors_of(20.20)

    numbers = {
        5: [1, 5],
        6: [1, 2, 3, 6],
        7: [1, 7],
        10: [1, 2, 5, 10],
        15: [1, 3, 5, 15],
        17: [1, 17],
        20: [1, 2, 4, 5, 10, 20],
        21: [1, 3, 7, 21],
        24: [1, 2, 3, 4, 6, 8, 12, 24],
        40: [1, 2, 4, 5, 8, 10, 20, 40],
        144: [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72, 144],
    }
    for number, values in numbers.items():
        factors = factors_of(number)
        assert factors == values


def test_is_prime():
    numbers = {
        5: True,
        6: False,
        7: True,
        10: False,
        15: False,
        17: True,
        20: False,
        21: False,
        24: False,
        40: False,
        144: False,
    }
    for number, prime in numbers.items():
        assert is_prime(number) == prime

    assert is_prime(20.20) is False


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
