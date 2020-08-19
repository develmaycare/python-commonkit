import os
import pytest
from commonkit.config.ini import *

# Tests


class TestINIConfig(object):

    def test_get(self):
        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        config.load()

        assert config.get("project") is not None
        assert config.get("project", key="title") is not None
        assert config.get("project", default="Pleasant Tents, LLC", key="copyright") == "Pleasant Tents, LLC"
        assert config.get("nonexistent") is None

        assert config.project.has("copyright") is False

    def test_getattr(self):
        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        config.load()
        assert config.project is not None

        config = INIConfig(os.path.join("tests", "config", "example.ini"), flatten="project")
        config.load()
        assert config.title is not None
        # print(config._sections['project'])
        assert config.nonexistent is None

        config = INIConfig(os.path.join("tests", "config", "example.ini"), auto_section=True)
        config.load()
        assert isinstance(config.nonexistent, Section)

    def test_has(self):
        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        config.load()
        assert config.has("testing") is False
        assert config.has("project") is True
        assert config.has("project", key="title") is True

    def test_iter(self):
        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        config.load()

        count = 0
        for section in config:
            count += 1

        assert count == 2

    def test_len(self):
        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        config.load()
        assert len(config) == 2

    def test_load(self):
        config = INIConfig("nonexistent.ini")
        assert config.load() is False

        config = INIConfig(os.path.join("tests", "config", "example.ini"))
        assert config.load() is True
        assert len(config) == 2

        context = {
            'client_code': "ACME",
            'client_name': "ACME, Inc."
        }
        config = INIConfig(os.path.join("tests", "config", "example.j2.ini"), context=context)
        assert config.load() is True
        assert config.client.code == "ACME"
        assert config.client.name == "ACME, Inc."

        config = INIConfig(os.path.join("tests", "config", "example-with-dummy.ini"), dummy="dummy")
        assert config.load() is True
        assert len(config) == 3
        assert config.dummy.testing is True

        config = INIConfig(os.path.join("tests", "config", "example-bad.ini"))
        assert config.load() is False


class TestSection(object):

    def test_get_attributes(self):
        s = Section("testing", **{'test1': True, 'test2': "testing", 'test3': 17})
        d = s.get_attributes()
        assert type(d) is dict

    def test_get_name(self):
        s = Section("testing", **{'test1': True, 'test2': "testing", 'test3': 17})
        assert s.get_name() == "testing"

    def test_repr(self):
        s = Section("testing", **{'test1': True, 'test2': "testing", 'test3': 17})
        assert repr(s) == "<Section testing>"
