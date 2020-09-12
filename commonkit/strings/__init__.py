"""
Abstract
--------

The strings module contains a number of string operations that may be useful in various situations.

Install
-------

BeautifulSoup, when available, is used by ``strip_html_tags()``:

.. code-block:: bash

    pip install bs4

Without the dependency, the function will attempt to do its best to strip HTML. For best results, though, install bs4.

Jinja2 is required when using ``parse_jinja_string()``:

.. code-block:: bash

    pip install jinja2

An error is raised if the dependency is not installed.

Pygments is required when using ``highlight_code``:

.. code-block:: bash

    pip install pygments

An error is raised if the dependency is not installed.

Unidecode is required for ``remove_non_ascii()``:

.. code-block:: bash

    pip install unidecode

An error is raised if the dependency is not installed.

Usage
-----

append_ordinal
..............

Add an ordinal string to an integer.

.. code-block:: python

    from commonkit import append_ordinal

    print(append_ordinal(1))
    print(append_ordinal(2))
    print(append_ordinal(3))

base_convert
............

Convert a number between two bases of arbitrary digits.

.. code-block:: python

    from commonkit import base_convert

    print(base_convert(12345))

camelcase_to_underscore
.......................

Convert a string from ``CamelCase`` to ``camel_case``.

.. code-block:: python

    from commonkit import camelcase_to_underscore

    model_name = "ProjectTasks"
    print(camelcase_to_underscore(model_name))

highlight_code
..............

Highlight (colorize) the given string.

.. code-block:: python

    from commonkit import highlight_code

    code = "<h1>Testing</h1><p>This is a test.</p>"
    print(highlight_code(code, language="html"))

indent
......

Indent a string.

.. code-block:: python

    from commonkit import indent

    text = "This text will be indented."
    print(indent(text))

is_ascii
........

Indicates whether a string contains only ASCII characters.

.. code-block:: python

    from commonkit import is_ascii

    print(is_ascii("å fine méss"))
    print(is_ascii("a fine mess"))

is_variable_name
................

Indicates whether the given string may be used as a valid Python variable name.

.. code-block:: python

    from commonkit import is_variable_name

    print(is_variable_name("123_testing"))
    print(is_variable_name("testing_123"))

parse_jinja_string
..................

Parse the given string as a Jinja 2 template.

.. code-block:: python

    from commonkit import parse_jinja_string

    context = {
        'domain_name': "example.com",
        'first_name': "Bob",
    }

    template = "Hello {{ first_name }}, welcome to the {{ domain_name }} website!"

    output = parse_jinja_string(template, context)


remove_non_ascii
................

Remove non-ASCII characters from a string.

.. code-block:: python

    from commonkit import remove_non_ascii

    string = "å fine méss"
    print(remove_non_ascii(string))


replace_non_ascii
.................

Replace non-ASCII characters with ASCII characters.

.. code-block:: python

    from commonkit import replace_non_ascii

    string = "å fine méss"
    print(replace_non_ascii(string))

slug
....

Convert the given text into a slugline.

.. note::
    This slug routine is both *simple* and *slow*. If you need faster or more sophisticated processing, check out
    awesome-slugify.

.. code-block:: python

    from commonkit import slug

    string = "It's a Test"
    print(slug(string))

strip_html_tags
...............

Strip HTML tags from a string.

.. code-block:: python

    from commonkit import strip_html_tags

    html = "<p>This string contains <b>HTML</b> tags.</p>"
    print(strip_html_tags(html))

truncate
........

Get a truncated version of a string if if over the limit.

.. code-block:: python

    from commonkit import truncate

    title = "This Title is Too Long to Be Displayed As Is"
    print(truncate(title))

underscore_to_camelcase
.......................

Convert a string from ``camel_case`` to ``CamelCase`` .

.. code-block:: python

    from commonkit import underscore_to_camelcase

    pattern_name = "project_detail"
    print(underscore_to_camelcase(pattern_name))

underscore_to_title_case
........................

Convert a string from ``under_score_case`` to ``Title Case``.

.. code-block:: python

    from commonkit import underscore_to_title_case

    pattern_name = "project_detail"
    print(underscore_to_title_case(pattern_name))

"""
from .library import *

__version__ = "0.25.0"
