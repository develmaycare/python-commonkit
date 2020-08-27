# Imports

import re

# Exports

__all__ = (
    "EMAIL_PATTERN",
    "STRICT_EMAIL_PATTERN",
    "VARIABLE_NAME_PATTERN",
)

# Patterns


EMAIL_PATTERN = re.compile(r"[^@]+@[^@]+\.[^@]+", re.IGNORECASE)
"""A basic regex pattern for validating an email string."""

# From: https://github.com/cool-RR/python_toolbox/blob/master/python_toolbox/misc_tools/misc_tools.py
STRICT_EMAIL_PATTERN = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016'
    r'-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
    r'[A-Z0-9-]{2,}\.?)$)'
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|'
    r'[0-1]?\d?\d)){3}\]$',
    re.IGNORECASE
)
"""A strict regex pattern for validating an email string."""

VARIABLE_NAME_PATTERN = re.compile('^[a-zA-Z_][0-9a-zA-Z_]*$')
"""A pattern which may be used to validate that a string may be used as valid Python variable name."""

# More patterns at:
# https://www.geeksforgeeks.org/how-to-validate-ssn-social-security-number-using-regular-expression/
# https://medium.com/factory-mind/regex-cookbook-most-wanted-regex-aa721558c3c1
# http://emailregex.com
