import os
import shutil
from commonkit.strings.library import *

# This was once used by the sites module, but was replaced by a template file. We can still use it for testing, though.
EXAMPLE_TEMPLATE = """# {{ title|default("Example Template") }}

{{ description }}

"""

# Tests


def test_append_ordinal():
    assert append_ordinal(1) == "1st"
    assert append_ordinal(2) == "2nd"
    assert append_ordinal(3) == "3rd"
    assert append_ordinal(4) == "4th"
    assert append_ordinal(5) == "5th"
    assert append_ordinal(6) == "6th"
    assert append_ordinal(7) == "7th"
    assert append_ordinal(8) == "8th"
    assert append_ordinal(9) == "9th"
    assert append_ordinal(10) == "10th"
    assert append_ordinal(11) == "11th"
    assert append_ordinal(12) == "12th"
    assert append_ordinal(13) == "13th"


def test_base_convert():
    """Check conversion of various numbers."""

    result = base_convert(0)
    assert result == "A"

    result = base_convert(12345)
    assert result == "DNH"

    result = base_convert(-12345)
    assert result == "-DNH"


def test_camelcase_to_underscore():
    """Check that CamelCase is correctly converted."""
    string = "CamelCase"
    new_string = camelcase_to_underscore(string)
    assert new_string == "camel_case"

    string = "MultipleCamelCaseString"
    new_string = camelcase_to_underscore(string)
    assert new_string == "multiple_camel_case_string"

    string = "not_camel_case"
    new_string = camelcase_to_underscore(string)
    assert string == new_string


def test_highlight_code():

    code = "<h1>Testing</h1><p>This is a test.</p>"
    output = highlight_code(code, language="html")
    assert type(output) is str


def test_indent():
    """Check that text indentation works."""

    assert indent("This text will be indented.") == "    This text will be indented."

    a = list()
    a.append("This is line 1.")
    a.append("This is line 2.")
    a.append("This is line 3.")

    text = "\n".join(a)

    index = 0
    output = indent(text)
    for line in output.splitlines():
        assert line == "    " + a[index]
        index += 1


def test_is_ascii():
    assert is_ascii("å fine méss") is False
    assert is_ascii("a fine mess") is True


def test_is_variable_name():
    assert is_variable_name("1776_testing") is False
    assert is_variable_name("testing-123") is False
    assert is_variable_name("Testing 123") is False
    assert is_variable_name("tésting") is False
    assert is_variable_name("testing_123") is True
    assert is_variable_name("_testing") is True


def test_parse_jinja_string():
    """Check the output of string template processing."""

    # First without context.
    context = dict()
    output = parse_jinja_string(EXAMPLE_TEMPLATE, context)

    assert "Example Template" in output

    # Then with context.
    context = {
        'title': "Example Site",
        'description': "This is an example template.",
    }
    output = parse_jinja_string(EXAMPLE_TEMPLATE, context)
    assert "Example Site" in output
    assert "This is an example template." in output


def test_remove_non_ascii():
    string = "å fine méss"
    assert remove_non_ascii(string) == " fine mss"


def test_replace_non_ascii():
    string = "å fine méss"
    assert replace_non_ascii(string) == "a fine mess"


def test_slug():
    string = "It's a Bad Mess: A Tale of Woe"
    # print(slug(string))
    assert slug(string) == "its-a-bad-mess-a-tale-of-woe"


def test_strip_html_tags():
    """Check that HTML is removed from a string."""

    html = "<p>This string contains <b>HTML</b> tags.</p>"
    plain = strip_html_tags(html)
    assert plain == "This string contains HTML tags."


def test_truncate():
    """Check the output of string truncation."""
    # It should be safe to submit an empty string.
    output = truncate(None)
    assert len(output) == 0

    # A string is mirrored if it doesn't exceed the limit.
    string = "1234567890"
    output = truncate(string, limit=10)
    assert string == output

    # Continuation impacts the limit.
    string = "1234567890"
    limit = 9
    output = truncate(string, limit=limit)
    assert len(output) == limit
    assert output == "123456..."

    # Check without continuation.
    string = "1234567890"
    limit = 5
    output = truncate(string, continuation=None, limit=limit)
    assert len(output) == limit
    assert output == "12345"


def test_underscore_to_camelcase():
    """Check that underscores are correctly converted."""
    string = "camel_case"
    new_string = underscore_to_camelcase(string)
    assert new_string == "CamelCase"

    string = "multiple_camel_case_string"
    new_string = underscore_to_camelcase(string)
    assert new_string == "MultipleCamelCaseString"

    string = "nounderscore"
    new_string = underscore_to_camelcase(string)
    assert new_string == "Nounderscore"


def test_underscore_to_title_case():
    """Check that underscores are correctly converted."""
    string = "title_case"
    new_string = underscore_to_title_case(string)
    assert new_string == "Title Case"

    string = "multiple_title_case_string"
    new_string = underscore_to_title_case(string)
    assert new_string == "Multiple Title Case String"

    string = "nounderscore"
    new_string = underscore_to_title_case(string)
    assert new_string == "Nounderscore"
