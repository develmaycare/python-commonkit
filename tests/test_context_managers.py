import os
from commonkit.context_managers import *
from commonkit.shell import Command
from subprocess import getoutput


def test_captured_output(monkeypatch):
    """Check that captured output works as expected."""

    def mock_input(label):
        return "yes"

    monkeypatch.setattr("builtins.input", mock_input)
    with captured_output() as (output, error):
        result = input("This is a Test (yes/no)? ")
        assert "yes" == result


def test_cd():
    """Check that cd works as expected."""
    path = os.path.join("tests", "data")
    with cd(path):
        command = Command("ls -ls")
        command.run()
        assert "example.csv" in command.output


def test_modified_environ():
    with modified_environ(PROJECT_HOME=os.path.join("docs", "source")):
        output = getoutput("ls -ls $PROJECT_HOME")
        assert "index.rst" in output


def test_virtualenv():
    """Check that virtualenv works as expected."""
    with virtualenv("./manage.py migrate") as command:
        assert command == "source python/bin/activate && ./manage.py migrate"
