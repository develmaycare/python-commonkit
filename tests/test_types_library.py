import os
from decimal import Decimal
import pytest
import shutil
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


def test_is_email():
    assert is_email(17) is False
    assert is_email("bob@bob") is False
    assert is_email("bob@bob.com") is True

    assert is_email("bob@bob", strict=True) is False
    assert is_email("bob@bob.com", strict=True) is True


def test_is_float():
    """Check that float recognition works as expected."""

    assert is_float(17) is False
    assert is_float(17.5) is True
    assert is_float("17.5") is True
    assert is_float("17") is False
    assert is_float("asdf") is False


def test_is_integer():
    """Check that integer recognition works as expected."""

    assert is_integer(17) is True
    assert is_integer(17.5) is False
    assert is_integer("17") is False
    assert is_integer("17", cast=True) is True
    assert is_integer("asdf", cast=True) is False


def test_is_number():
    assert is_number(17) is True
    assert is_number(Decimal('17.17')) is True
    assert is_number(1.1717) is True
    assert is_number("seventeen") is False


def test_is_string():
    """Check that string recognition works as expected."""

    assert is_string("testing") is True
    assert is_string("17") is True


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


class TestFalseBecause(object):

    def test_init(self):
        value = FalseBecause("testing")
        assert bool(value) is False


class TestTrueBecause(object):

    def test_init(self):
        value = TrueBecause("testing")
        assert bool(value) is True
