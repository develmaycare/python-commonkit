"""
Abstract
--------

Python logging is powerful but can be daunting to get started. This library implements some basic formatters and a
helper class that makes logging a bit easier.

Using the Logging Helper
........................

The :py:class:`commonkit.logging.library.LoggingHelper` may be used to easily set up basic logging to the console or
to a file. Console colorization is enabled by default (on supported platforms), but may be turned off by passing
``colorize=False`` when instantiating the helper.

.. code-block:: python

    from commonkit.logging import LoggingHelper

    logger = LoggingHelper(level=logging.DEBUG, path="tmp.log")
    log = logger.setup()

    log.debug('This is a debug message just for you.')
    log.info('This message is purely informational.')
    log.warning('You better watch out!')
    log.error('Something bad has happened.')
    log.critical('Something even worse has happened.')

Logging Success
...............

The logging library comes with a minor override to the logging class called :py:class:`SuccessLogger`. To use this
logger:

.. code-block:: python

    from commonkit.logging import LoggingHelper

    logger = LoggingHelper(name="success-logger", success=True)
    log = logger.setup()

    log.success("Something positive has happened.")

.. tip::
    The success logger only works for named loggers. Otherwise an ``AttributeError`` is raised: "RootLogger object has
    no attribute 'success'.

Reference
---------

- Official `Python logging documentation`_.
- A `nice logging tutorial`_.

.. _nice logging tutorial: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
.. _Python logging documentation: https://docs.python.org/3.7/library/logging.html

"""

from .library import *

__version__ = "0.4.0-x"
