import os
import pytest
from commonkit.config.base import Base as BaseConfig
from commonkit.config.exceptions import VariableNameNotAllowed

# Tests


class TestBase(object):

    def test_disallowed_variable_names(self):
        config = BaseConfig("test.cfg")
        assert "exists" in config._disallowed_variable_names()

        # Cover without a line number.
        with pytest.raises(VariableNameNotAllowed):
            raise VariableNameNotAllowed("testing", "test.cfg")

    def test_get(self):
        config = BaseConfig("test.cfg")
        with pytest.raises(NotImplementedError):
            config.get("testing")

    def test_get_error(self):
        config = BaseConfig("test.cfg")
        assert config.get_error() is None

    def test_has(self):
        config = BaseConfig("test.cfg")
        with pytest.raises(NotImplementedError):
            config.has("testing")

    def test_has_error(self):
        config = BaseConfig("test.cfg")
        assert config.has_error is False

        config._error = "FakeError"
        assert config.has_error is True

    def test_load(self):
        config = BaseConfig("test.cfg")
        with pytest.raises(NotImplementedError):
            config.load()

    def test_process_key_value_pair(self):
        config = BaseConfig("test.cfg")

        key, value = config._process_key_value_pair("testing", "yes")
        assert key == "testing"
        assert value is True

    def test_relative_path_exists(self):
        config = BaseConfig(os.path.join("tests", "config", "example.cfg"))
        assert config.relative_path_exists("../data") is True
        assert config.relative_path_exists("example-bad.cfg") is True
        assert config.relative_path_exists("nonexistent.txt") is False

    def test_repr(self):
        config = BaseConfig("test.cfg")
        assert repr(config) == "<Base test.cfg>"

    def test_smart_cast(self):
        config = BaseConfig("test.cfg")

        key, value = config._process_key_value_pair("testing", "yes")
        assert key == "testing"
        assert value is True

        key, value = config._process_key_value_pair("testing", "17")
        assert value == 17
