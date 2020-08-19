.. _how-to:

******
How To
******

.. note::
    The how-tos provided here may *not* specific to commonkit.

Create a Command Console
========================

A console is a stateful interface for executing commands. For example, the ``psql`` or ``mysql`` commands are examples of consoles that may be used to execute various commands within a database interface.

.. note::
    A full `tutorial on command consoles`_ may be found on our web site.

.. _tutorial on command consoles: https://develmaycare.com/blog/creating-command-console/

Here is a quick example:

.. code-block:: python

    #! /usr/bin/env python
    import cmd


    class Console(cmd.Cmd):
        intro = "Welcome to the console. Type 'help' or '?' and press ENTER."
        prompt = "=> "

        # noinspection PyPep8Naming
        def do_EOF(self, args):
            """Exit on system end of file character."""
            return self.do_exit(args)

        def emptyline(self):
            """Do nothing on empty input line."""
            pass

        def do_exit(self):
            """Exit the console."""
            return True

        def do_hello(self):
            """Say hello."""
            print("Hello!")


    def main():
        console = Console()
        console.cmdloop()


    if __name__ == '__main__':
        main()

Assuming the file is named ``example.py``, simply run ``./example.py`` to load the console.

Implement a Context Manager
===========================

`Python's contextlib`_ allows for powerful changes to operation. The ``with`` statement changes the operational context of the statements that follow.

.. _Python's contextlib: https://docs.python.org/3/library/contextlib.html

The example below is from commonkit's ``context_managers`` library:

.. code-block:: python

    def cd(path):
        # We save the directory from which we start so we can restore it below.
        previous_cwd = os.getcwd()

        # Switch Python file IO to the desired (given) path.
        os.chdir(path)

        # In this case there is nothing to yield. When the exiting the context, we restore the previous path.
        try:
            yield
        finally:
            os.chdir(previous_cwd)

Using the context manage is simple, yet powerful:

.. code-block:: python

    from subprocess import getstatusoutput

    # Statements execute with the current working directory as /path/to/new/directory.
    with cd("/path/to/new/directory"):
        status, output = getstatusoutput("ls -ls")
        if status != 0:
            print("Failed to get directory listing.")
        else:
            print(output)

    # Now statements execute with the current working directory from which Python was started.
    # ...
