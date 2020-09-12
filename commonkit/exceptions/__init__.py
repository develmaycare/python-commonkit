"""
Abstract
--------

Because there is no reason exceptions can't be funny *and* useful.

Usage
-----

We often use ``DeeplyDisturbingError`` when something something is very (very) wrong with core or "deep" functionality.
It may be raised because the precise conditions for for arriving at the error may be puzzling or somewhat unknown, as is
often the case with run-time logic conditions that have yet to be proved.

Likewise, we like to use the ``DoesNotCompute`` exception when a mathematical or related logic operation has failed.
It's generally a lot more obvious and perhaps more humorous.

``IMustBeMissingSomething`` provides a shortcut for raising errors regarding a child implementation that is missing a
required attribute or method definition which returns the attribute value.

The ``ThisShouldNeverHappen`` exception is used to indicate an application state that should, in fact, never happen.
This could be, for example, when a setting that should always exist does not exist or has a value we can't use.

``YouShallNotPass`` is used exclusively in a set of conditional statements where it's important to know that the
``else`` is in fact a condition that should never occur. We *could* use ``ThisShouldNeverHappen`` here, but
``YouShallNotPass`` is much more amusing.

"""
__author__ = "Shawn Davis <shawn@develmaycare.com>"
__maintainer__ = "Shawn Davis <shawn@develmaycare.com>"
__version__ = "0.8.0-d"

from .library import *

__all__ = (
    "DeeplyDisturbingError",
    "DoesNotCompute",
    "IMustBeMissingSomething",
    "ThisShouldNeverHappen",
    "YouShallNotPass",
)
