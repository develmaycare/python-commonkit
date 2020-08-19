import pytest
from commonkit.shell.commands import Command
from commonkit.shell.scripts import Script

# Tests


class TestScript(object):

    def test_add(self):
        script = Script("testing")
        script.add("ls -ls")
        assert script._commands[0].statement == "ls -ls"

        script.add(Command("touch /tmp/testing.txt"))
        assert script._commands[1].statement == "touch /tmp/testing.txt"

        with pytest.raises(TypeError):
            script.add(1234)

    def test_get_commands(self):
        script = Script("testing")
        script.add("ls -ls")
        script.add("touch /tmp/testing.txt")
        script.add("stat /tmp/testing.txt")

        assert len(script.get_commands()) == 3

    def test_iter(self):
        script = Script("testing")
        script.add("ls -ls")
        script.add("touch /tmp/testing.txt")
        script.add("stat /tmp/testing.txt")

        count = 0
        # noinspection PyUnusedLocal
        for command in script:
            count += 1

        assert count == 3

    def test_len(self):
        script = Script("testing")
        script.add("ls -ls")
        script.add("touch /tmp/testing.txt")
        script.add("stat /tmp/testing.txt")

        assert len(script) == 3

    def test_repr(self):
        script = Script("testing")
        assert repr(script) == "<Script testing>"

    def test_str(self):
        script = Script("testing")
        script.add("ls -ls")
        assert "ls -ls" in str(script)

    def test_to_string(self):
        script = Script("testing")
        script.add("ls -ls", comment="List directory.")
        assert "ls -ls" in script.to_string()
        assert "# List directory." in script.to_string()
