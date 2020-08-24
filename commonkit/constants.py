BASE2 = "01"
BASE10 = "0123456789"
BASE16 = "0123456789ABCDEF"
BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"

FALSE_VALUES = (
    0,
    False,
    "f",
    "FALSE",
    "False",
    "false",
    "N",
    "n",
    "NO",
    "No",
    "no",
)
"""A collection of values that should evaluate to ``False``."""

TRUE_VALUES = (
    1,
    True,
    "t",
    "TRUE",
    "True",
    "true",
    "Y",
    "y",
    "YES",
    "Yes",
    "yes",
)
"""A collection of values that should evaluate to ``True``."""

BOOLEAN_VALUES = FALSE_VALUES + TRUE_VALUES
"""A collection of values that should be identified as boolean."""
