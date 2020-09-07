"""
Variables based on the current environment.

``SCREEN_COLUMNS``: An integer representing the current columns available on the screen.

``SCREEN_ROWS``: An integer representing the current rows available on the screen.

"""
# Imports

import shutil

# Exports

__all__ = (
    "SCREEN_COLUMNS",
    "SCREEN_ROWS",
)

# Variables

screen_size = shutil.get_terminal_size((80, 20))
SCREEN_COLUMNS = screen_size.columns
SCREEN_ROWS = screen_size.lines
