# Imports

import re
from ..constants import BASE10, BASE62
from ..compat import get_formatter_by_name, get_lexer_by_name, highlight, remove_html, unidecode, JinjaTemplate
from ..regex import VARIABLE_NAME_PATTERN

# Exports

__all__ = (
    "append_ordinal",
    "base_convert",
    "camelcase_to_underscore",
    "highlight_code",
    "indent",
    "is_ascii",
    "is_variable_name",
    "parse_jinja_string",
    "remove_non_ascii",
    "replace_non_ascii",
    "slug",
    "strip_html_tags",
    "truncate",
    "underscore_to_camelcase",
    "underscore_to_title_case",
)

# Functions


def append_ordinal(number):
    """Add an ordinal string to an integer.

    :param number: The number to be converted to an ordinal.
    :type number: int

    :rtype: str

    """
    suffixes = dict()
    for i, v in enumerate(['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']):
        suffixes[str(i)] = v

    v = str(number)

    if v.endswith("11") or v.endswith("12") or v.endswith("13"):
        return v + "th"
    # if v in ['11', '12', '13']:
    #     return v + 'th'

    return v + suffixes[v[-1]]


def base_convert(number, from_digits=BASE10, to_digits=BASE62):
    """Convert a number between two bases of arbitrary digits.

    :param number: The number to be converted.
    :type number: int

    :param from_digits: The digits to use as the source of the conversion. ``number`` is included in these digits.
    :type from_digits: str

    :param to_digits: The digits to which the number will be converted.
    :type to_digits: str

    :rtype: str

    """

    if str(number)[0] == '-':
        number = str(number)[1:]
        negative = True
    else:
        negative = False

    x = 0
    for digit in str(number):
        x = x * len(from_digits) + from_digits.index(digit)

    if x == 0:
        result = to_digits[0]
    else:
        result = ""

        while x > 0:
            digit = x % len(to_digits)
            result = to_digits[digit] + result
            x = int(x / len(to_digits))

        if negative:
            result = "-" + result

    return result


def camelcase_to_underscore(string):
    """Convert a given string from ``CamelCase`` to ``camel_case``.

    :param string: The string to be converted.
    :type string: str

    :rtype: str

    """
    # http://djangosnippets.org/snippets/585/
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', string).lower().strip('_')


def highlight_code(string, formatter="terminal", include_lines=False, language="python"):
    """Highlight (colorize) the given string.

    :param string: The string to be highlighted.
    :type string: str

    :param formatter: The name of the formatter to use. Accepts any value supported by pygments'
                      ``get_formatter_by_name()``.
    :type formatter: str

    :param include_lines: Indicates whether line numbers should be included.
    :type include_lines: bool

    :param language: The programming (or other) language or format of the provided string.
    :type language: str

    :rtype: str

    .. code-block:: python

        from superpython.utils import highlight_code

        code = "<h1>Testing</h1><p>This is a test.</p>"
        print(highlight_code(code, language="html"))

    """
    lexer = get_lexer_by_name(language)
    formatter = get_formatter_by_name(formatter, linenos=include_lines)

    return highlight(string, lexer, formatter)


def indent(text, amount=4):
    """Indent a string.

    :param text: The text to be indented.
    :type text: str

    :param amount: The number of spaces to use for indentation.
    :type amount: int

    :rtype: str

    .. code-block:: python

        from superpython.utils import indent

        text = "This text will be indented."
        print(indent(text))

    """
    prefix = " " * amount
    return prefix + text.replace('\n', '\n' + prefix)


def is_ascii(string):
    """Indicates whether a string contains only ASCII characters.

    :param string: The string to be evaluated.
    :type string: str

    :rtype: bool

    .. note::
        As of Python 3.7, strings provide the ``isascii()`` method. See the discussions at:
        https://stackoverflow.com/q/196345/241720

    """
    try:
        string.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


def is_variable_name(string):
    """Indicates whether the given string may be used as a valid Python variable name.

    :param string: The string to be evaluated.
    :type string: str

    :rtype: bool

    """
    return bool(VARIABLE_NAME_PATTERN.match(string))


def parse_jinja_string(string, context):
    """Parse the given string as a Jinja 2 template.

    :param string: The template.
    :type string: str

    :param context: The context to be parsed into the template.
    :type context: dict

    :rtype: str

    .. code-block:: python

        from superpython.utils import parse_jinja_string

        context = {
            'domain_name': "example.com",
            'first_name': "Bob",
        }

        template = "Hello {{ first_name }}, welcome to the {{ domain_name }} website!"

        output = parse_jinja_string(template, context)

    """
    template = JinjaTemplate(string)

    return template.render(context)


def remove_non_ascii(text):
    """*Remove* non-ASCII characters from a string.

    :param text: The string that should have non-ASCII characters removed.
    :type text: str

    :rtype: str

    .. note::
        This may leave blank spaces in the text. Use ``strip()`` or ``replace()`` to remove them.

    """
    return ''.join(i for i in text if ord(i) < 128)


def replace_non_ascii(text):
    """Attempt to *replace* non-ASCII characters with ASCII characters.

    :param text: The string that should have non-ASCII characters replaced.
    :type text: str

    :rtype: str

    .. note::
        Requires the `Unidecode package`_.

    .. _Unidecode package: https://pypi.org/project/Unidecode/

    """
    return unidecode(str(text))


def slug(text, separator="-"):
    """Convert the given text into a slugline.

    :param text: The text to be slugged.
    :type text: str

    :param separator: The separator to use.
    :type separator: str

    :rtype: str

    .. note::
        This slug routine is both *simple* and *slow*. If you need faster or more sophisticated processing, check out
        awesome-slugify.

    """
    text = replace_non_ascii(text)

    removes = [
        ",",
        ":",
        ";",
        "'",
        '"',
        "|",
        "/",
        "\\",
    ]
    for r in removes:
        text = text.replace(r, "")

    text = text.replace(" ", separator)

    return text.lower()


def strip_html_tags(html):
    """Strip HTML tags from a string.

    :param html: The string from which HTML tags should be stripped.
    :type html: str || unicode

    :rtype: str

    .. code-block:: python

        from superpython.utils import strip_html_tags

        html = "<p>This string contains <b>HTML</b> tags.</p>"
        print(strip_html_tags(html))

    """
    return remove_html(html)


def truncate(string, continuation="...", limit=30):
    """Get a truncated version of a string if if over the limit.

    :param string: The string to be truncated.
    :type string: str | None

    :param limit: The maximum number of characters.
    :type limit: int

    :param continuation: The string to add to the truncated title.
    :type continuation: str | None

    :rtype: str

    .. code-block:: python

        from superpython.utils import truncate

        title = "This Title is Too Long to Be Displayed As Is"
        print(truncate(title))

    """
    # Make it safe to submit the string as None.
    if string is None:
        return ""

    # There's nothing to do if the string is not over the limit.
    if len(string) <= limit:
        return string

    # Adjust the limit according to the string length, otherwise we'll still be over.
    if continuation:
        limit -= len(continuation)

    # Return the altered title.
    if continuation:
        return string[:limit] + continuation
    else:
        return string[:limit]


def underscore_to_camelcase(string):
    """Convert a string with underscore separations to CamelCase.

    :param string: The string to be converted.
    :type string: str

    :rtype: str

    """
    return string.replace("_", " ").title().replace(" ", "")


def underscore_to_title_case(string):
    """Convert a string to title case.

    :param string: The string to be converted.
    :type string: str

    :rtype: str

    """
    return string.replace("_", " ").title()
