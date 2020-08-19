"""
Abstract
--------

The platform library provides an object-oriented representation of the current operating system.

Usage
-----

.. code-block:: python

    from commonkit.platform import Platform
    import sys

    platform = Platform(sys)

    if platform.is_linux:
        print("Linux!")
    elif platform.is_osx:
        print("OS X!")
    elif platform.is_windows:
        print("Windows!")
    else:
        print("No idea!")

"""
from .library import *

__all__ = (
    "Platform",
)

__version__ = "0.3.0-x"
