"""
Abstract
--------

`Python's context managers`_ provide support for *with* statements. This is a powerful pattern described in `PEP 343`_
which facilitates automated try/finally expressions.

This library provides somewhat common context managers that a developer may find useful.

.. _Python's context managers: https://docs.python.org/3/library/contextlib.html
.. _PEP 343: https://www.python.org/dev/peps/pep-0343/

Usage
-----

Capturing Output
................

Capture command line output (including errors). Especially useful for testing.

.. code-block:: python

    from commonkit.context_managers import captured_output

    with captured_output() as (output, error):
        print("This is a test.")
        self.assertEqual("This is a test.", output.getValue())

Changing the Working Directory
..............................

Change the current working directory for a set of statements or commands.

.. code-block:: python

    from commonkit.context_managers import cd

    with cd("example_com/source"):
        os.system("./manage.py migrate")

Modifying the Environment
.........................

You may temporarily modify the operating environment using ``modified_environ``.

.. code-block:: python

    from commonkit.context_managers import modified_environ
    from subprocess import getstatusoutput

    with modified_environ(PROJECT_HOME="/path/to/temporary/projects"):
        status, output = getstatusoutput("ls -ls $PROJECT_HOME")
        print(output)

Using a Virtual Environment
...........................

Activate a Python virtual environment before running a command.

.. code-block:: python

    from commonkit.context_managers import virtualenv

    with virtualenv("./manage.py migrate") as command:
        print(command)

"""
from .library import *

__version__ = "0.5.0-d"
