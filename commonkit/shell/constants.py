class EXIT:
    """Exit codes for command line operations."""
    OK = 0
    ERROR = 1
    INPUT = 2
    USAGE = 64
    ENVIRONMENT = 71
    IO = 74
    TEMP = 75
    PERMISSIONS = 77
    CONFIG = 78
    UNKNOWN = 99


# noinspection PyPep8Naming
class TABLE_FORMAT:
    """The standard formats for `python-tabulate`_ output.
    
    .. _python-tabulate: https://bitbucket.org/astanin/python-tabulate
    
    """
    FANCY_GRID = "fancy_grid"
    GITUB = "github"
    GRID = "grid"
    HTML = "html"
    JIRA = "jira"
    LATEX = "latex"
    LATEX_BOOKTABS = "latex_booktabs"
    LATEX_RAW = "latex_raw"
    MEDIAWIKI = "mediawiki"
    MOINMOIN = "moinmoin"
    ORGTBL = "orgtbl"
    PIPE = "pipe"
    PLAIN = "plain"
    PRESTO = "presto"
    PSQL = "psql"
    RST = "rst"
    SIMPLE = "simple"
    TEXTILE = "textile"
    YOUTRACK = "youtrack"


TABLE_FORMAT_CHOICES = [
    TABLE_FORMAT.FANCY_GRID,
    TABLE_FORMAT.GITUB,
    TABLE_FORMAT.GRID,
    TABLE_FORMAT.HTML,
    TABLE_FORMAT.JIRA,
    TABLE_FORMAT.LATEX,
    TABLE_FORMAT.LATEX_BOOKTABS,
    TABLE_FORMAT.LATEX_RAW,
    TABLE_FORMAT.MEDIAWIKI,
    TABLE_FORMAT.MOINMOIN,
    TABLE_FORMAT.ORGTBL,
    TABLE_FORMAT.PIPE,
    TABLE_FORMAT.PLAIN,
    TABLE_FORMAT.PRESTO,
    TABLE_FORMAT.PSQL,
    TABLE_FORMAT.RST,
    TABLE_FORMAT.SIMPLE,
    TABLE_FORMAT.TEXTILE,
    TABLE_FORMAT.YOUTRACK,
]
"""All table format choices."""

TABLE_FORMAT_COMMON_CHOICES = [
    TABLE_FORMAT.HTML,
    TABLE_FORMAT.PIPE,
    TABLE_FORMAT.PLAIN,
    TABLE_FORMAT.RST,
    TABLE_FORMAT.SIMPLE,
]
"""The more common table format choices."""
