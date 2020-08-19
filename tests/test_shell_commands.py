from commonkit.context_managers import captured_output
from commonkit.shell.commands import *
from commonkit.shell.constants import *

# Tests


class test_abort():
    try:
        abort("")
    except SystemExit:
        assert True

    # noinspection PyUnusedLocal
    with captured_output() as (output, error):
        try:
            abort("I can't go on.")
        except SystemExit:
            assert True


class TestCommand(object):

    def test_getattr(self):
        command = Command("ls -ls", env="testing")
        assert command.env == "testing"

    def test_get_command(self):
        command = Command("apachectl configtest", register="apache_ok", sudo=True)
        assert "sudo -u root" in command.get_command()
        assert "apache_ok=$?" in command.get_command()

    def test_preview(self):
        command = Command("ls -ls")
        assert "ls -ls" == command.preview()

        command = Command("ls -ls", path="commonkit")
        assert "(cd commonkit && ls -ls)" == command.preview()

        command = Command("ls -ls", prefix='echo "testing"')
        assert 'echo "testing" && ls -ls' == command.preview()

        command = Command("ls -ls", path="commonkit", prefix='echo "testing"')
        assert '(cd commonkit && echo "testing" && ls -ls)' == command.preview()

    def test_repr(self):
        command = Command("ls -ls")
        assert "<Command: ls -ls>" == repr(command)

    def test_run(self):
        command = Command("ls -ls", path="commonkit", prefix='echo "testing"')
        command.run()
        assert EXIT.OK == command.code

        command = Command("ls -ls", path="nonexistent")
        command.run()
        assert EXIT.UNKNOWN == command.code

    def test_str(self):
        command = Command("ls -ls")
        assert "ls -ls" == str(command)

    def test_sudo(self):
        command = Command("ls -ls", sudo=Sudo())
        assert isinstance(command.sudo, Sudo)
        assert command.sudo.enabled is False

        command = Command("ls -ls", sudo="deploy")
        assert isinstance(command.sudo, Sudo)
        assert command.sudo.enabled is True

        command = Command("ls -ls", sudo=True)
        assert isinstance(command.sudo, Sudo)
        assert command.sudo.enabled is True

        command = Command("ls -ls")
        assert isinstance(command.sudo, Sudo)
        assert command.sudo.enabled is False


class TestSudo(object):

    def test_bool(self):
        sudo = Sudo()
        assert bool(sudo) is False

        sudo = Sudo(enabled=True)
        assert bool(sudo) is True

    def test_repr(self):
        sudo = Sudo()
        assert repr(sudo) == "<Sudo root>"

    def test_str(self):
        sudo = Sudo()
        assert str(sudo) == "sudo -u root"

        sudo = Sudo(user=None)
        assert str(sudo) == "sudo"


# class TestCommand(unittest.TestCase):
#
#     def test_abort(self):
#         """Check that abort works as expected."""
#         try:
#             abort("")
#         except SystemExit:
#             self.assertTrue(True)
#
#         # noinspection PyUnusedLocal
#         with captured_output() as (output, error):
#             try:
#                 abort("I can't go on.")
#             except SystemExit:
#                 self.assertTrue(True)
#
#     def test_preview(self):
#         """Test the preview output of a command."""
#         command = Command("ls -ls")
#         self.assertEqual("ls -ls", command.preview())
#
#         command = Command("ls -ls", path="myninjas")
#         self.assertEqual("(cd myninjas && ls -ls)",command.preview())
#
#         command = Command("ls -ls", prefix='echo "testing"')
#         self.assertEqual('echo "testing" && ls -ls', command.preview())
#
#         command = Command("ls -ls", path="myninjas", prefix='echo "testing"')
#         self.assertEqual('(cd myninjas && echo "testing" && ls -ls)', command.preview())
#
#     def test_repr(self):
#         """Test the representation of a command."""
#         command = Command("ls -ls")
#         self.assertEqual("<Command: ls -ls>", repr(command))
#
#     def test_run(self):
#         """Test running a command."""
#         command = Command("ls -ls", path="myninjas", prefix='echo "testing"')
#         command.run()
#         self.assertEqual(EXIT_SUCCESS, command.code)
#
#         command = Command("ls -ls", path="nonexistent")
#         command.run()
#         self.assertEqual(EXIT_UNKNOWN, command.code)
#
#     def test_string(self):
#         """Test the string output of a command."""
#         command = Command("ls -ls")
#         self.assertEqual("ls -ls", str(command))
#
#     def test_sudo(self):
#         command = Command("ls -ls", sudo=True)
#         self.assertEqual("sudo ls -ls", command.preview())
#
#         command = Command("ls -ls", sudo="bob")
#         self.assertEqual("sudo -u bob ls -ls", command.preview())



# class TestScript(unittest.TestCase):
#
#     def test_add(self):
#         s = Script("testing")
#         s.add("ls -ls")
#         self.assertEqual(1, len(s._commands))
#
#         s.add(Command("du -hs"))
#         self.assertEqual(2, len(s._commands))
#
#         try:
#             s.add(123, comment="Raises a type error.")
#         except TypeError:
#             self.assertTrue(True)
#
#     def test_exists(self):
#         s = Script("testing")
#         s.path = os.path.join("tests", "config", "steps.cfg")
#         self.assertTrue(s.exists)
#
#         s.path = os.path.join("path", "to", "nonexistent", "steps.cfg")
#         self.assertFalse(s.exists)
#
#     def test_get_commands(self):
#         s = Script("testing")
#         s.add("ls -ls")
#         s.add(Command("du -hs"))
#
#         commands = s.get_commands()
#         self.assertIsInstance(commands, list)
#         self.assertEqual(2, len(commands))
#
#     def test_get_template_locations(self):
#         s = Script("testing")
#         s.path = os.path.join("tests", "config", "steps.cfg")
#
#         locations = s.get_template_locations()
#         self.assertTrue("tests/config/templates" in locations[0])
#
#     def test_iter(self):
#         s = Script("testing")
#         s.add("ls -ls")
#         s.add(Command("du -hs"))
#
#         for c in s:
#             self.assertIsInstance(c, Command)
#
#     def test_load(self):
#         class Page(object):
#             content = "This is a test."
#
#         context = {
#             'page': Page(),
#         }
#
#         s = Script("testing")
#         s.load(os.path.join("tests", "config", "steps.cfg"), context=context)
#         self.assertEqual(7, len(s._commands))
#         # print(s.to_string())
#
#         s = Script("nonexistent")
#         s.load(os.path.join("path", "to", "nonexistent", "steps.cfg"))
#         self.assertFalse(s.is_loaded)
#
#         context = {
#             'domain_tld': "example_com",
#             'release_root': "/var/www/example_com",
#         }
#         s = Script("with-context")
#         s.load(os.path.join("tests", "config", "steps.cfg.j2"), context=context)
#         self.assertEqual(5, len(s._commands))
#         self.assertTrue("example_com" in s.to_string())
#         self.assertTrue("/var/www/example_com" in s.to_string())
#         # print(s.to_string())
#
#     def test_repr(self):
#         s = Script("testing")
#         self.assertEqual("<Script testing>", repr(s))
#
#     def test_str(self):
#         s = Script("testing")
#         s.add(Command("ls -ls", comment="This is a test."))
#         self.assertTrue("This is a test." in str(s))
#
#     def test_to_string(self):
#         s = Script("testing")
#         s.add(Command("ls -ls", comment="This is a test."))
#         self.assertTrue("This is a test." in s.to_string())

