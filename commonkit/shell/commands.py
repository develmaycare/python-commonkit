# Import

import subprocess
from .constants import EXIT

# Exports

__all__ = (
    "abort",
    "Command",
    "Sudo",
)

# Functions


def abort(message, code=EXIT.ERROR):
    """Stop processing and issue an exit/return code.

    :param message: A message to send to the user.
    :type message: str

    :param code: The exit code to issue.
    :type code: int

    .. code-block:: python

        from commonkit.shell import abort

        abort("I can't go on.")

    """
    if message:
        print(message)

    exit(code)

# Classes


class Command(object):
    """Run a shell command."""

    def __init__(self, statement, comment=None, path=None, prefix=None, register=None, shell=None, stop=False, sudo=False, **kwargs):
        """Initialize a command.

        :param statement: The command itself.
        :type statement: str

        :param comment: The comment on the command.
        :type comment: str

        :param path: The path from which the command should be executed.
        :type path: str

        :param prefix: A pre-command such as export or virtual env call to be executed (after the path) before the
                       command.
        :type prefix: str

        :param register: Save the output of the command as the named variable.
        :type register: str

        :param shell: The shell to use, for example: ``/bin/bash``
        :type shell: str

        :param stop: Indicates no additional commands should be executed if this command fails.
        :type stop: bool

        :param sudo: Indicates sudo should be used to execute the command
        :type sudo: bool | str | Sudo

        .. note::
            The ``stop`` argument is *not* used by the command instance, but may be used in scripting to determine if
            additional commands should be executed.

        .. code-block:: python

            from commonkit.shell import Command

            # A simple command.
            command = Command("ls -ls")
            print(command.preview())

            if command.run():
                print("Your listing is above.")

            # Create /tmp/tmp.txt file.
            command = Command("touch tmp.txt", path="/tmp")
            command.run()

            # Using a prefix.
            command = Command("pg_dumpall -U postgres", prefix='export PGPASSWORD="mypassword"')
            command.run()

        """
        self.code = None
        self.comment = comment
        self.error = None
        self.output = None
        self.path = path
        self.prefix = prefix
        self.register = register
        self.shell = shell
        self.statement = statement
        self.stop = stop

        if isinstance(sudo, Sudo):
            self.sudo = sudo
        elif type(sudo) is str:
            self.sudo = Sudo(enabled=True, user=sudo)
        elif sudo is True:
            self.sudo = Sudo(enabled=True)
        else:
            self.sudo = Sudo()

        self._attributes = kwargs

    def __getattr__(self, item):
        return self._attributes.get(item)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.statement)

    def __str__(self):
        return self.get_command(include_path=True)

    def get_command(self, include_path=False):
        """Get the command to be executed with prefix and path.

        :param include_path: Indicates whether the path should be included. Generally speaking, you want to include the
                             path to preview the command and omit the path when you want to run the command.
        :type include_path: bool

        :rtype: str

        """
        a = list()

        if self.path and include_path:
            a.append("(cd %s" % self.path)

        if self.prefix:
            a.append(self.prefix)

        if self.sudo:
            a.append("%s %s" % (self.sudo, self.statement))
            # if type(self.sudo) is str:
            #     a.append("sudo -u %s %s" % (self.sudo, self.statement))
            # else:
            #     a.append("sudo %s" % self.statement)
        else:
            a.append(self.statement)

        if self.path and include_path:
            command = " && ".join(a) + ")"
        else:
            command = " && ".join(a)

        if self.register:
            b = list()
            b.append(command)
            b.append("%s=$?;" % self.register)
            return "\n".join(b)

        return command

    def preview(self):
        """Get a preview of the command that will be executed.

        :rtype: str

        """
        return self.get_command(include_path=True)

    def run(self):
        """Run the command.

        :rtype: bool
        :returns: Returns ``True`` if the command was successful. The ``code``, ``error``, and ``output`` attributes
                  are also set.

        .. tip::
            Success depends upon the exit code of the command which is not available from all commands on all platforms.
            Check the command's documentation for exit codes and plan accordingly.

        """
        # Prepare to shell output.
        output_stream = subprocess.PIPE
        error_stream = subprocess.PIPE

        # The command without the path (if any) because path is passed to Popen via the cwd parameter.
        command = self.get_command()

        # Run the command. Capture output, error, and return code.
        try:
            p = subprocess.Popen(
                command,
                cwd=self.path,
                executable=self.shell,
                shell=True,
                stderr=error_stream,
                stdout=output_stream
            )
            (stdout, stderr) = p.communicate()

            self.code = p.returncode

            a = list()
            for line in str(stderr).split("\\n"):
                a.append(line.strip())

            self.error = "\n".join(a)

            a = list()
            for line in str(stdout).split("\\n"):
                a.append(line.strip())

            self.output = "\n".join(a)
        except Exception as e:
            self.code = EXIT.UNKNOWN
            self.error = str(e)

        return self.code == EXIT.OK


class Sudo(object):
    """Helper class for defining sudo options."""

    def __init__(self, enabled=False, user="root"):
        """Initialize the helper.

        :param enabled: Indicates sudo is enabled.
        :type enabled: bool

        :param user: The user to be invoked.
        :type user: str

        """
        self.enabled = enabled
        self.user = user

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.user)

    def __str__(self):
        if self.user is not None:
            return "sudo -u %s" % self.user

        return "sudo"

    def __bool__(self):
        return self.enabled
