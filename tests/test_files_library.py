import logging
import os
import shutil

import pytest

from commonkit.files.library import *


def patch_os_path_getsize_0(path):
    return 0


def patch_os_path_get_size_kb(path):
    return 1500


def patch_os_path_get_size_gb(path):
    return 2_500_000_000


def patch_os_path_get_size_mb(path):
    return 1_000_000

# Tests


def test_append_file():
    path = os.path.join("tmp", "test.log")

    assert append_file(path, "The file doesn't exist yet, so we can't append to it.") is False

    write_file(path, content="# This is a temporary log file", make_directories=True)

    assert append_file(path, "Something interesting has happened.") is True
    content = read_file(path)
    assert "Something interesting has happened." in content

    assert append_file(path, "Something else has happened.") is True
    content = read_file(path)
    assert "Something else has happened." in content

    os.remove(path)
    os.rmdir(os.path.dirname(path))


def test_copy_file():
    """Check that files copy correctly."""
    from_path = os.path.join("tests", "readme.markdown")
    to_path = os.path.join("tests", "tmp", "readme.markdown")
    copy_file(from_path, to_path, make_directories=True)

    assert os.path.exists(to_path) is True

    os.remove(to_path)
    os.removedirs(os.path.dirname(to_path))

    # This will not copy because the directory doesn't exist.
    to_path = os.path.join("tmp", "readme.txt")
    success, message = copy_file(from_path, to_path)
    assert success is False
    assert isinstance(message, str)


def test_copy_tree(caplog):
    """Check that a tree is copied correctly."""
    from_path = os.path.join("tests", "plugins")

    # First try a nonexistent destination.
    with caplog.at_level(logging.DEBUG):
        success = copy_tree(from_path, os.path.join("tests", "nonexistent"))
        assert success is False

    # Next try a good directory.
    to_path = os.path.join("tests", "tmp")
    os.makedirs(to_path)
    success = copy_tree(from_path, to_path)
    assert success is True

    # A directory with bad files.
    with caplog.at_level(logging.DEBUG):
        from_path = os.path.join("tests", "watched")
        success = copy_tree(from_path, to_path)
        assert success is False

    shutil.rmtree(to_path)


def test_get_files():

    path = os.path.join("tests", "config", "example.cfg")
    with pytest.raises(ValueError):
        get_files(path)

    assert len(get_files("nonexistent", raise_exception=False)) == 0

    path = os.path.join("tests", "config")
    files = get_files(path)
    assert len(files) == 13

    path = os.path.join("tests", "config")
    files = get_files(path, extension=".ini")
    assert len(files) == 5


def test_parse_jinja_template():
    """Check the output of template file processing."""

    class Page(object):
        content = "<p>This is the content.</p>"

    context = {
        'page': Page(),
    }

    path = os.path.join("tests", "templates", "example.html")

    output = parse_jinja_template(path, context)
    assert "This is the content." in output


def test_read_csv():
    """Check the output of reading a CSV file."""
    path = os.path.join("tests", "data", "example.csv")

    # Without DictReader.
    rows = read_csv(path)
    count_4 = 4
    assert len(rows) == count_4

    # With DictReader.
    rows = read_csv(path, first_row_field_names=True)
    count_3 = 3
    assert len(rows) == count_3


def test_read_file():
    """Check that a file may be read."""
    path = os.path.join("tests", "readme.markdown")
    output = read_file(path)
    assert "Tests are located in this directory." in output


def test_write_file():
    """Check that files are written."""
    path = os.path.join("tmp", "readme.txt")
    content = u"This is a test file."

    write_file(path, content, make_directories=True)

    assert os.path.exists(path) is True

    os.remove(path)
    os.rmdir(os.path.dirname(path))


class TestFile():

    def test_exists(self):
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.exists is True

        f = File(os.path.join("tests", "config", "nonexistent.ext"))
        assert f.exists is False

    def test_get_file_size(self):
        f = File(os.path.join("tests", "config", "example.ini"))
        assert type(f.get_file_size()) is int
        assert type(f.get_file_size(unit=File.SIZE_KILOBYTES)) is float
        assert type(f.get_file_size(unit=File.SIZE_MEGABYTES)) is float
        assert type(f.get_file_size(unit=File.SIZE_GIGABYTES)) is float

    def test_get_file_size_0(self, monkeypatch):
        monkeypatch.setattr("os.path.getsize", patch_os_path_getsize_0)
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.size == 0

    def test_get_file_size_display(self, monkeypatch):
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.get_file_size_display() == "99B"

    def test_get_file_size_display_gb(self, monkeypatch):
        monkeypatch.setattr("os.path.getsize", patch_os_path_get_size_gb)
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.get_file_size_display() == "2.5GB"

    def test_get_file_size_display_kb(self, monkeypatch):
        monkeypatch.setattr("os.path.getsize", patch_os_path_get_size_kb)
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.get_file_size_display() == "1.5KB"

    def test_get_file_size_display_mb(self, monkeypatch):
        monkeypatch.setattr("os.path.getsize", patch_os_path_get_size_mb)
        f = File(os.path.join("tests", "config", "example.ini"))
        assert f.get_file_size_display() == "1.0MB"

    def test_init(self):
        """Check that file properties are correctly initialized."""
        f = File("/path/to/config.ini")

        assert "config.ini" == f.basename
        assert "/path/to" == f.directory
        assert ".ini" == f.extension
        assert "config" == f.name
        assert "/path/to/config.ini" == f.path

    def test_repr(self):
        f = File("path/to/config.ini")
        assert "<File config.ini>" == repr(f)
