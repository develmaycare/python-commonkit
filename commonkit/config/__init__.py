"""
Abstract
--------

The config library provides classes for working with configuration data, and in particular a friendly interface on top
of Python's ``configparser`` that allows INI files to be represented as objects. Additionally, sections within the INI
file are also represented as objects.

Install
-------

Jinja is required for `Loading a Configuration as a Template`_.

.. code-block:: bash

    pip install jinja2

Usage
-----

The settings component supports INI files, "flat" configuration files, and also loading Python files. The examples below
demonstrate INI files. See :ref:`reference` for other configuration file types.

Defining a Configuration File
.............................

A typical configuration file might look like so:

.. code-block:: ini

    ; etc/project.ini
    [project]
    title = Rocket Skates
    active = yes
    release = 1

    [client]
    name = ACME, Inc.
    code = ACME

Loading a Configuration File
............................

An example of loading a file and working with the objects contained therein:

.. code-block:: python

    from commonkit.config import INIConfig

    config = INIConfig("etc/project.ini")
    if config.load():
        print("Title: %s" % config.project.title)
        print("Client: %s" % config.client.name)

The sections and items within the file are now available as objects on the config instance.

Flattening a Section
....................

It is possible to instruct the configuration loader to "flatten" a given section so that its items are available as
attributes of the instance.

.. code-block:: python

    from commonkit.config import INIConfig

    project = INIConfig("etc/project.ini", flatten="project")
    if project.load():
        print("Title: %s" % project.title)
        print("Client: %s" % project.client.name)

Loading a Configuration as a Template
.....................................

It is possible to load a configuration file as a Jinja2 template prior to parsing its sections:

.. code-block:: ini

    ; project.j2.ini
    [project]
    title = {{ project_title }}
    active = yes
    release = 1

    [client]
    name = {{ client_name }}
    code = {{ client_code }}

The code above redefines the previous INI example, but changes some of the configuration into template variables.

Then in your code:

.. code-block:: python

    from commonkit.config import INIConfig

    context = {
        'client_code': "ACME",
        'client_name': "ACME, Inc."
        'project_title': "Rocket Skates",
    }

    config = INIConfig("etc/project.j2.ini", context=context)
    if config.load():
        print("Title: %s" % config.project.title)
        print("Client: %s" % config.client.name)

INI Configuration Without a Section
...................................

The example below is an INI file that includes settings that do not belong to a section:

.. code-block:: ini

    some_value = 123
    some_other_value = testing

    [section1]
    some_value = 456
    some_other_value = also testing

The :py:class:`commonkit.config.library.INI` class provides a means of capturing the "bare" values using the
``dummy`` parameter.

.. code-block:: python

    from commonkit.config import INIConfig

    # dummy can be any name you like.
    config = INIConfig("example.ini", dummy="raw")
    if config.load():
        print("Some Value: %s" % config.raw.some_value)
        print("Some Other Value: %s" % config.raw.some_other_value)

Other Configuration Files
.........................

The config library also supports configuration files without sections (a "flat" configuration) and may be used to load
Python files as configuration.

An example flat file:

.. code-block:: text

    # This is a comment.
    project_title = Example Project
    project_active = yes
    project_release = 1
    client_code = ACME
    client_name = ACME, Inc.

    ; This is also a comment after a blank line.

May be loaded with:

.. code-block:: python

    from commonkit.config import FlatConfig

    config = FlatConfig("flat.cfg")
    if config.load():
        print("Title:", config.project_title)
        print("Client:", config.client_name)

Comments beginning with ``#`` and ``;`` are ignored and blank lines are skipped.

.. note::
    ``FlatConfig`` does *not* support multi-line text for values.

As with ``INIConfig``, ``FlatConfig`` supports pre-processing as a Jinja template when ``context`` is provided.
Additionally, you may pass default values to the flat config to account for values that do not exist.

.. code-block:: python

    from commonkit.config import FlatConfig

    defaults = {
        'project_active': True,
    }
    config = FlatConfig("flat.cfg", defaults=defaults)
    if config.load():
        print("Title:", config.project_title)
        print("Client:", config.client_name)
        print("Active:", config.project_active)

The ``PythonConfig`` loads a Python file whose contents may be used for configuration.

An example file:

.. code-block:: python

    test1 = "abc"
    test2 = 123
    test3 = dict()
    test4 = None

May be loaded with:

.. code-block:: python

    from commonkit.config import PythonConfig

    config = PythonConfig("path/to/config.py")
    if config.load():
        print("Test 1:", config.test1)
        # and so on

The file must be eligible for loading using ``import_module()`` and be free of syntax (or other) errors.

Unlike ``INIConfig`` and ``FlatConfig``, Python files used for configuration may *not* be pre-processed as Jinja
templates. However, default values *are* supported by passing ``defaults`` dictionary as with ``FlatConfig``.

"""

from .flat import *
from .ini import *
from .py import *

__version__ = "0.14.0-d"
