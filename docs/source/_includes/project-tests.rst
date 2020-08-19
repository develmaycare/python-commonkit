Coverage Requirements
---------------------

100% coverage is required for the ``master`` branch.

See `current coverage report <coverage/index.html>`_.

.. csv-table:: Lines of Code
    :file: ../_data/cloc.csv

Running Tests
-------------

.. tip::
    You may use the ``tests`` target of the ``Makefile`` to run tests with coverage: ``make tests;``

To run unit tests:

.. code-block:: bash

    python -m pytest discover;

To run a specific test:

.. code-block:: bash

    python -m pytest tests/test_name.py;

Running tests with coverage:

.. code-block:: bash

    coverage run --source=. -m pytest discover;

Reviewing the coverage report:

.. code-block:: bash

    coverage report -m;

Reviewing the HTML coverage report:

.. code-block:: bash

    coverage html;
    open htmlcov/index.html;