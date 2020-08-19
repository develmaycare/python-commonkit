"""
Abstract
--------

Working with files and directories is a common requirement. The files module provides utility functions for common patterns of file and directory manipulation.

Install
-------

Jinja2 is required when using ``parse_jinja_template()``:

.. code-block:: bash

    pip install jinja2

Otherwise there are no other dependencies.

Usage
-----

append_file
...........

Append content to a file.

.. code-block:: python

    from commonkit import append_file

    append_file("log.txt", "Something interesting has happened.")

copy_file
.........

Copy a file from one location to another.

.. code-block:: python

    from commonkit import copy_file

    copy_file("readme-template.txt", "path/to/project/readme.txt")

copy_tree
.........

Recursively copy a source directory to a given destination.

.. code-block:: python

    from commonkit import copy_tree

    success = copy_tree("from/path", "to/path")
    print(success)

parse_jinja_template
....................

Parse a Jinja 2 template.

.. code-block:: python

    from commonkit import parse_jinja_template

    context = {
        'domain_name': "example.com",
        'first_name': "Bob",
    }

    template = "path/to/welcome.html"

    output = parse_jinja_template(template, context)


read_csv
........

Read the contents of a CSV file.

.. code-block:: text

    menu,identifier,sort_order,text,url
    main,product,10,Product,/product/
    main,solutions,20,Solutions,/solutions/
    main,resources,30,Resources,/resources/
    main,support,40,Support,https://support.example.com
    main,about,50,About,/about/
    main,contact,60,Contact,/contact/

.. code-block:: python

    from commonkit import read_csv

    rows = read_csv("path/to/menus.csv", first_row_fields_names=True)
    for r in rows:
        print("%s: %s" % (row['identifier'], row['url']


read_file
.........

Read a file and return its contents.

.. code-block:: python

    from commonkit import read_file

    output = read_file("path/to/readme.txt")
    print(output)


write_file
..........

Write a file.

.. code-block:: python

    from commonkit import write_file

    write_file("path/to/readme.txt", "This is a test.")

The File Class
..............

The :py:class:`commonkit.library.File` class is a simple helper for working with the various attributes of a
given file path.

For more robust handling of paths, see `pathlib`_.

.. _pathlib: https://docs.python.org/3/library/pathlib.html

.. code-block:: python

    from commonkit import File

    f = File("/path/to/config.ini")
    print("Path: %s" % f.path)
    print("Directory: %s" % f.directory)
    print("Name: %s" % f.name
    print("Name Without Extension: %s" % f.basename)
    print("Extension: %s" % f.extension)
"""
from .library import *

__version__ = "0.21.0-d"
