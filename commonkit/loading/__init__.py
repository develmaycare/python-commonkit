"""
Abstract
--------

Loading Python resources dynamically is a common enough requirement. The loading library facilitates some generic
utilities for making this a bit easier.

.. note::
    If you are using Django, you should be looking at ``django.utils.module_loading`` *first*. Likewise, SuperDjango
    provides additional loading utilities.

Usage
-----

Determine if an Instance Has a Callable
.......................................

Use the ``has_callable()`` function to determine if an instance has a callable method.

.. code-block:: python

    from commonkit import has_callable

    class MyWhatever(object):
        def testing(self):
            return True

    instance = MyWhatever()
    print(has_callable(instance, "testing")

Note this also works for classes, class methods, and static methods.

Discovering Modules
....................

The ``autodiscover()`` function allows you to find modules of the same name within a number of locations. This is
especially useful for loading pre-defined functionality for dispatching or plugins.

.. code-block:: python

    from commonkit.loading import autodiscover

    locations = [
        "myproject.apps",
    ]
    package_name = "plugins
    autodiscover(locations, package_name)

In the example above, any package within ``myproject/apps/`` that contains a ``plugin.py`` module will be imported
automatically.

Finding Python Packages
.......................

Use the ``find_packages`` function to locate Python packages within a given path.

.. code-block:: python

    from commonkit.loading import find_packages

    print(find_packages("myprojects/apps")

Note that

1. only packages at the top level of the path are identified, and
2. packages are returned as a list of dotted paths.

Importing a Member
..................

You may use the ``import_member()`` function as a shortcut for dynamically acquiring an attribute, class, or function
from any module that exists in the Python path.

.. code-block:: python

    from commonkit.loading import import_member

    config_class = import_member("settings.Config")

By default, exceptions are always raised. You can pass ``raise_exception=False`` to suppress this behavior, but be sure
to deal with this in your code. When exceptions are suppressed, ``import_member()`` returns ``None`` is something went
wrong in the attempt to import.

Testing Whether a Submodule Exists
..................................

It is sometimes useful to determine whether a package contains a specific submodule. The ``submodule_exists()`` function
may be used for this.

.. code-block:: python

    from commonkit.loading import submodule_exists

    if submodule_exists("settings.Config"):
        # ...

Working With a Module in an Object-Oriented Way
...............................................

There may be cases where you want to work with a module as an instance, rather than the module itself. The
:py:class:`commonkit.loading.library.Module` class allows just that.

.. code-block:: python

    from commonkit.loading import Module

    module = Module("settings.config")
    if module.load():
        print("Module:", module.name)
        print("Version:", module.version)
        print("")
        print(module.docstring)

Consider extending ``Module`` and customizing the ``_load()`` method to do additional handling on ``load()``.

For example,wWe've used this approach to generate dynamic documentation.

"""
__version__ = "0.2.0-d"

from .library import *
