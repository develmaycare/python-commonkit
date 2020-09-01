.. _getting-started:

***************
Getting Started
***************

System Requirements
===================

Python 3.6 or greater is required.

Install
=======

To install without database support: ``pip install commonkit``

To install all dependencies, use: ``pip install commonkit[all]``

.. note::
    All dependencies includes SQLAlchemy but *not* specific database drivers below.

Database Support
----------------

For database support: ``pip install commonkit[database]`` (supports SQLite by default)

Or for specific database engines:

- MS SQL: ``pip install commonkit[mssql]``
- Oracle: ``pip install commonkit[oracle]``
- Postgres: ``pip install commonkit[pgsql]``

Tablib is required for database export features: ``pip install tablib``

Files and Strings Support
-------------------------

Files and strings make optional use of BeautifulSoup, Jinja2, Pygments, and unidecode:

.. code-block:: bash

    pip install beautifulsoup4; # for strip_html_tags()
    pip install jinja2; # for parse_jinja_string() and parse_jinja_template() and config when parsing files as templates
    pip install pygments; # for highlight_code()
    pip install unidecode; # for replace_non_ascii() and slug()

Or use ``pip install commonkit[strings]`` to install all of these dependencies.

Shell Support
-------------

Full shell support requires colorama and tabulate:

.. code-block:: bash

    pip install colorama; for shell.feedback
    pip install tabulate; for shell.tables

Or use ``pip install commonkit[shell]``.

Examples
========

The :ref:`components` chapter contains a number examples for getting started with each component. See also :ref:`how-to`.

Next Steps
==========

Check out :ref:`components` and :ref:`reference`.

FAQs
====

**Why not break the library out into separate packages?**

Common Kit's components are designed around common usage patterns. There are a lot of advantages to organizing these into a single package. See this article for our thoughts on `doing one thing well`_.

.. _doing one thing well: https://develmaycare.com/blog/doing-one-thing-well/

Have a question? `Just ask`_!

.. _Just ask: https://develmaycare.com/contact/?support=1&product=Common%20Kit
