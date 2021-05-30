# import os
from decimal import Decimal
import pytest
# import shutil
from commonkit.types.library import *
from commonkit.constants import FALSE_VALUES, TRUE_VALUES

COUNT_2 = 2

# Tests


def test_is_bool():
    """Check that runtime boolean validation works as expected."""
    for f in FALSE_VALUES:
        assert is_bool(f) is True

    for t in TRUE_VALUES:
        assert is_bool(t) is True

    # False and 0 will result in a count of 2.
    false_count = 0
    for f in FALSE_VALUES:
        if is_bool(f, test_values=(True, False)):
            false_count += 1

    assert false_count == COUNT_2

    # True and 1 will result in a count of 2.
    true_count = 0
    for t in TRUE_VALUES:
        if is_bool(t, test_values=(True, False)):
            true_count += 1

    assert true_count == COUNT_2


def test_is_decimal():
    assert is_decimal(True) is False
    assert is_decimal("asdf") is False
    assert is_decimal("17") is True
    assert is_decimal(17) is True
    assert is_decimal(17.17) is True
    assert is_decimal(17.17000) is True


def test_is_email():
    assert is_email(17) is False
    assert is_email("bob@bob") is False
    assert is_email("bob@bob.com") is True

    assert is_email("bob@bob", strict=True) is False
    assert is_email("bob@bob.com", strict=True) is True


def test_is_empty():

    assert is_empty("") is True
    assert is_empty(" ") is True
    assert is_empty("testing") is False


def test_is_float():
    """Check that float recognition works as expected."""

    assert is_float(True) is False
    assert is_float(False) is False
    assert is_float(17) is False
    assert is_float(17.5) is True
    assert is_float("17.5") is True
    assert is_float("17") is False
    assert is_float("asdf") is False


def test_is_integer():
    """Check that integer recognition works as expected."""

    assert is_integer(True) is False
    assert is_integer(False) is False
    assert is_integer(17) is True
    assert is_integer(17.5) is False
    assert is_integer("17") is False
    assert is_integer("17", cast=True) is True
    assert is_integer("asdf", cast=True) is False


def test_is_magic_name():

    assert is_magic_name("__testing__") is True
    assert is_magic_name("__t__") is True
    assert is_magic_name("_testing") is False
    assert is_magic_name("_testing_") is False


def test_is_nothing():

    assert is_nothing(None) is True
    assert is_nothing("") is True
    assert is_nothing(0) is True
    assert is_nothing(0.0) is True
    assert is_nothing(0.1) is False


def test_is_number():
    assert is_number(True) is False
    assert is_number(False) is False
    assert is_number(17) is True
    assert is_number(Decimal('17.17')) is True
    assert is_number(1.1717) is True
    assert is_number("seventeen") is False


def test_is_string():
    """Check that string recognition works as expected."""

    assert is_string("testing") is True
    assert is_string("17") is True


def test_is_variable_name():

    assert is_variable_name("123") is False
    assert is_variable_name("testing123") is True
    assert is_variable_name("testing_123") is True
    assert is_variable_name("testing_123_") is True
    assert is_variable_name("_testing_123") is True
    assert is_variable_name("_testing_123_") is True
    assert is_variable_name("__testing_123__") is True


def test_smart_cast():
    """Check that values are correctly cast to a Python data type."""
    value = "123"
    assert isinstance(smart_cast(value), int)

    value = "yes"
    assert isinstance(smart_cast(value), bool)

    value = "why?"
    assert isinstance(smart_cast(value), str)

    value = "17.5"
    assert isinstance(smart_cast(value), float)


def test_to_bool():
    """Check that boolean conversion works as expected."""
    for f in FALSE_VALUES:
        assert to_bool(f) is False

    for t in TRUE_VALUES:
        assert to_bool(t) is True

    with pytest.raises(ValueError):
        to_bool("asdf")

    with pytest.raises(ValueError):
        to_bool(1.1)


def test_to_decimal():
    assert to_decimal(True) is None
    assert to_decimal("asdf") is None

    with pytest.raises(ValueError):
        to_decimal("asdf", fail_silently=False)

    assert isinstance(to_decimal("17"), Decimal)
    assert isinstance(to_decimal("17.17"), Decimal)
    assert isinstance(to_decimal(17), Decimal)
    assert isinstance(to_decimal(17.17), Decimal)
    assert isinstance(to_decimal(17.001), Decimal)


def test_to_ordered_dict():
    d = {
        'c': 3,
        'a': 1,
        'b': 2,
        'e': 5,
        'd': 4,
        'f': 6,
        'g': 7,
    }
    s = to_ordered_dict(d)
    assert list(s.keys()) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    assert list(s.values()) == [1, 2, 3, 4, 5, 6, 7]

    d = {
        'c': "zxcv",
        'a': "asdf",
        'b': "qwer",
    }
    s = to_ordered_dict(d)
    assert list(s.keys()) == ['a', 'b', 'c']
    assert list(s.values()) == ["asdf", "qwer", "zxcv"]

    d = {
        'c': "qwer",
        'a': "asdf",
        'b': "zxcv",
        'e': 5,
        'd': 4,
        'f': 6,
        'g': 7,
    }
    with pytest.raises(TypeError):
        to_ordered_dict(d)


def test_to_timedelta():
    d = to_timedelta("17m")
    assert d.seconds == 1020

    d = to_timedelta("1d 4h 15m")
    assert d.seconds == 15300

    with pytest.raises(ValueError):
        to_timedelta("1 day")


class TestBooleanBecause(object):

    def test_bool(self):
        value = BooleanBecause(True, because="testing")
        assert bool(value) is True

    def test_eq(self):
        value = BooleanBecause(True, because="testing")
        assert value == True

    def test_hash(self):
        value = BooleanBecause(True, because="testing")
        assert hash(value) == 1

    def test_neq(self):
        value = BooleanBecause(True, because="testing")
        assert value != False

        true = TrueBecause()
        false = FalseBecause()
        assert true.__neq__(false)

    def test_repr(self):
        value = BooleanBecause(True, because="testing")
        assert repr(value) == "<True testing>"


class TestDoesNotInstantiate(object):

    def test_init(self):
        class SETTINGS(DoesNotInstantiate):
            pass

        with pytest.raises(RuntimeError):
            settings = SETTINGS()


class TestFalseBecause(object):

    def test_init(self):
        value = FalseBecause("testing")
        assert bool(value) is False


class TestTrueBecause(object):

    def test_init(self):
        value = TrueBecause("testing")
        assert bool(value) is True
