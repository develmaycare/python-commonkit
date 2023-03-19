"""
This utility is based upon `Semantic Versioning`_. By default, it operates on ``VERSION.txt``.

.. _Semantic Versioning: http://semver.org

Calling the command with no arguments will simply print the current version.

"""
__version__ = "0.5.0-d"

from .constants import *
from .library import *
from .utils import *
