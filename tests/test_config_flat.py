import os
import pytest
from commonkit.config.exceptions import VariableNameNotAllowed
from commonkit.config.flat import *

# Tests


class TestFlat(object):

    def test_get(self):
        config = FlatConfig(os.path.join("tests", "config", "example.cfg"))
        assert config.load() is True

        assert config.get("project_title") == "Example Project"
        assert config.get("nonexistent", default="testing") == "testing"

    # def test_getattr(self):
    #     pass

    def test_has(self):
        config = FlatConfig(os.path.join("tests", "config", "example.cfg"))
        assert config.load() is True

        assert config.has("project_title") is True
        assert config.has("nonexistent") is False

    # def test_len(self):
    #     pass

    def test_load(self):
        config = FlatConfig("nonexistent.cfg")
        assert config.load() is False

        config = FlatConfig(os.path.join("tests", "config", "example.cfg"))
        assert config.load() is True
        assert len(config) == 5

        context = {
            'client_code': "ACME",
            'client_name': "ACME, Inc."
        }
        config = FlatConfig(os.path.join("tests", "config", "example.j2.cfg"), context=context)
        assert config.load() is True
        assert config.client_code == "ACME"
        assert config.client_name == "ACME, Inc."

        with pytest.raises(VariableNameNotAllowed):
            config = FlatConfig(os.path.join("tests", "config", "example-bad.cfg"))
            config.load()
