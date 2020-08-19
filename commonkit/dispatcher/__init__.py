"""
Abstract
--------

The dispatcher component provides a simple signal-receiver API that allows events to be sent (by signals) to listeners
(receivers).

Usage
-----

Defining a Signal
.................

To create a signal instance, simply use the :py:class:`Signal`. For example:

.. code-block:: python

    from commonkit.dispatcher import Signal

    # in website/library/signals.py
    after_build_pages = Signal(arguments=["pages"])
    before_build_pages = Signal(arguments=["context", "site"])

You determine the arguments that will be sent.

Sending a Signal
................

In this example, we use the signals above to send a signal before and after a site build its pages:

.. code-block:: python

    from .signals import after_build_pages, before_build_pages

    class Site(object):
        def build_pages(self):
            context = self.get_context()

            before_build_pages.send(self.__class__, context=context, site=self)

            # build the pages ...

            after_build_pages.send(self.__class__, pages=pages)

Defining a Receiver
...................

Receivers are functions (or methods) that listen for a signal.

- The receiver must accept ``**kwargs``.
- The receiver must return a with two elements. The first element is a boolean indicating success or failure. The
  second element is any output of the callback or ``None``. Internally, this is captured in a
  :py:class:`commonkit.dispatcher.library.Response` instance so that ``Signal.send()`` returns a list of responses.
- A receiver should *never* issue feedback or use print statements. However, the receiver *may* use logging to provide
  additional information on signal processing.
- It is okay for receivers to raise exceptions.

.. code-block:: python

    def build_search_data(**kwargs):
        # do stuff
        return True, "Search data has been created."

Listening for a Signal
......................

To listen for a signal, connect the receiver with the signal. For example:

.. code-block:: python

    from website.library.signals import after_build_pages
    from website.library.sites import Site

    after_build_pages.connect(build_search_data, sender=Site)

Alternatives
------------

.. note::
    This code was inspired by `dispatch <https://github.com/olivierverdier/dispatch>`_ which was adapted from Django's
    dispatch module.

- `dispatch`_
- `PyDispatcher`_
- `python-dispatch`_

.. _dispatch: https://github.com/olivierverdier/dispatch
.. _PyDispatcher: http://pydispatcher.sourceforge.net
.. _python-dispatch: https://github.com/nocarryr/python-dispatch

"""
from .library import Receiver, Response, Signal

__all__ = (
    "Receiver",
    "Response",
    "Signal",
)

__version__ = "0.5.0-d"
