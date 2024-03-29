from commonkit.loading import *
import os
import pytest
import sys


class FakePackage(object):
    pass

# Tests


def test_autodiscover():
    locations = ["tests.discovery"]
    autodiscover(locations, "loadme")

    locations = ["tests.discovery"]
    with pytest.raises(Exception):
        autodiscover(locations, "loadme_bad")


def test_get_packages():
    path = os.path.join("tests", "discovery")
    packages = find_packages(path)
    assert len(packages) == 3


def test_has_callable():
    assert has_callable(sys, "exit")


    class NoCallable(object):
        pass

    instance = NoCallable()
    assert has_callable(instance, "testing") is False

    class YesCallable(object):
        @classmethod
        def class_testing(cls):
            return True

        @staticmethod
        def static_testing():
            return True

        def testing(self):
            return True

        @property
        def also_testing(self):
            return self.testing()

    instance = YesCallable()
    assert has_callable(instance, "testing") is True
    assert has_callable(instance, "also_testing") is False
    assert has_callable(instance, "nonexistent") is False
    assert has_callable(YesCallable, "testing") is True
    assert has_callable(YesCallable, "class_testing") is True
    assert has_callable(YesCallable, "static_testing") is True


def test_import_member():
    with pytest.raises(ImportError):
        import_member("nonexistent")

    assert import_member("nonexistent", raise_exception=False) is None

    assert import_member("commonkit.config.INIConfig") is not None
    assert import_member("commonkit.config.NonexistentConfig", raise_exception=False) is None

    with pytest.raises(ImportError):
        import_member("commonkit.config.NonexistentConfig")


    # with pytest.raises(ImportError):
    #     import_member("commonkit.nonexistent.NonexistentMember")
    #
    # with pytest.raises(ImportError):
    #     import_member("commonkit.config.NonexistentConfig")


def test_submodule_exists():
    assert submodule_exists("nonexistent", "nonexistent") is False

    package = FakePackage()
    assert submodule_exists(package, "nonexistent") is False

    assert submodule_exists("commonkit", "config") is True
    assert submodule_exists("commonkit.config", "nonexistent") is False


class TestModule(object):

    def test_exists(self):
        m = Module("commonkit.nonexistent")
        assert m.exists is False

        m = Module("commonkit.config")
        assert m.exists is True

    def test_getattr(self):
        m = Module("commonkit.config")
        assert m.testing is None

        m._attributes['testing'] = True
        assert m.testing is True

    def test_load(self):
        m = Module("commonkit.nonexistent")
        assert m.load() is False

        m = Module("commonkit.config")
        assert m.load() is True

        m = Module("tests.plugins.testing1")
        assert m.load() is True

    def test_repr(self):
        m = Module("commonkit.config")
        assert repr(m) == "<Module commonkit.config>"
