import os
from commonkit.config.py import *

# Tests


class TestPython(object):

    def test_get(self):
        config = PythonConfig(os.path.join("tests", "config", "config_test.py"), defaults={'test5': "testing"})
        config.load()
        assert config.get("test2") == 123
        assert config.get("test5") == "testing"
        assert config.get("test6", default="nonexistent") == "nonexistent"

    def test_getattr(self):
        config = PythonConfig(os.path.join("tests", "config", "config_test.py"), defaults={'test5': "testing"})
        config.load()

        assert type(config.test3) is dict

    def test_has(self):
        config = PythonConfig(os.path.join("tests", "config", "config_test.py"), defaults={'test5': "testing"})
        config.load()

        assert config.has("test1") is True
        assert config.has("test4") is False
        assert config.has("test5") is True

    def test_load(self):
        config = PythonConfig("nonexistent.py")
        assert config.load() is False

        config = PythonConfig(os.path.join("tests", "config", "config_test.py"), defaults={'test5': "testing"})
        assert config.load() is True
