# Imports

from contextlib import contextmanager
import os
from io import StringIO
import sys

# Exports

__all__ = (
    "captured_output",
    "cd",
    "modified_environ",
    "virtualenv",
)

# Functions


@contextmanager
def captured_output():
    """Capture command line output (including errors). Especially useful for testing.

    .. code-block:: python

        with captured_output() as (output, error):
            print "This is a test."
            self.assertEqual("This is a test.", output.getValue())

    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@contextmanager
def cd(path):
    """Change the current working directory for a set of statements or commands.

    :param path: The path from which to run the command.
    :type path: str || unicode

    .. code-block:: python

        from myninjas.context_managers import cd

        with cd("example_com/source"):
            os.system("./manage.py migrate")

    .. note::
        The previous working directory is restored after the command is executed.

    """
    previous_cwd = os.getcwd()

    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(previous_cwd)


@contextmanager
def modified_environ(**environ):
    """Temporarily modify environment variables.

    :param environ: The modified environment.

    """
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


@contextmanager
def virtualenv(command, path="python"):
    """Activate a Python virtual environment before running a command.

    :param command: The command to be executed.
    :type command: str || unicode

    :param path: The path to the virtual environment. Defaults to ``python``.
    :type path: str || unicode

    .. code-block:: python

        from myninjas.context_managers import virtualenv

        with virtualenv("./manage.py migrate") as command:
            print(command)

    """
    activation_script = os.path.join(path, "bin", "activate")

    try:
        yield "source %s && %s" % (activation_script, command)
    finally:
        pass
