"""
Abstract
--------

Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems. -- `Jamie Zawinsk`_

.. _Jamie Zawinsk: https://blog.codinghorror.com/regular-expressions-now-you-have-two-problems/

Common patterns for validating data.

.. note::
    We hope to implement a) more pre-defined patterns, and b) a regex wrapper that makes common regex operations a
    little easier.

Usage
-----

Currently, usage is tied to the types library.

Resources
---------

See the `official Python how-to for regular expressions`_.

- `Debuggex`_ A tool for testing regular expressions for JavaScript, PHP, or Python.
- `Pythex`_: A tool for testing regular Python expressions.
- `Rexegg`_: "The world's most tyrannosaurical regex tutorial".

.. _Debuggex: https://debuggex.com
.. _official Python how-to for regular expressions: https://docs.python.org/3/howto/regex.html
.. _Pythex: https://pythex.org
.. _Rexegg: http://www.rexegg.com

.. image:: https://imgs.xkcd.com/comics/perl_problems.png

"""

from .patterns import *

__version__ = "0.1.0-d"
