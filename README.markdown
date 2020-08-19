# Common Kit

![](https://img.shields.io/badge/status-active-green.svg)
![](https://img.shields.io/badge/stage-development-blue.svg)
![](https://img.shields.io/badge/coverage-100%25-green.svg)

A collection of common utilities for use in Python projects.

- Config: A wrapper for convenient, object-oriented use of configuration files.
- Context Managers: A collection of managers that are especially useful for command line scripting, testing, and deployment activities.
- CSV: Work with CSV files in an object-oriented manner.
- Database: A database wrapper with convenient methods using natural language.
- Dispatcher: Implements a simple signal-receiver pattern in object-oriented code.
- Files: Various utilities for working with files.
- Lists: Some simple functions for working with lists.
- Logging: A helper for making Python logging easier to use.
- Math: Some help. With math.
- Platform: A light-weight detection tool for discovery information about the current operating system.
- Pluggable: Implements a simple plugin pattern.
- Shell: Various classes and utilities for creating and interacting with the command line, including command execution, consistent exit codes, colorized feedback, input prompts, and tables.
- Strings: Various utilities for working with strings.
- Types: Run-time data type detection and casting.
- Utils: A collection of functions implementing common and some not-so-common operations in Python.
- Watchers: A library for setting up a response to changes in files or directories.

Full documentation is available at: https://develmaycare.com/docs/
 
## Install

To install without database support: `pip install commonkit`

To install all dependencies, use: `pip install commonkit[all]`

> Note: All dependencies includes SQLAlchemy but *not* specific database drivers below.

### Database Support

For database support: `pip install commonkit[database]` (supports SQLite by default)

Or for specific database engines:

- MS SQL: `pip install commonkit[mssql]`
- Oracle: `pip install commonkit[oracle]`
- Postgres: `pip install commonkit[pgsql]`

Tablib is required for database export features: `pip install tablib`

### Files and Strings

Files and strings make optional use of BeautifulSoup, Jinja2, Pygments, and unidecode:

```bash
pip install bs4; for strip_html_tags()
pip install jinja2; for parse_jinja_string() and parse_jinja_template() and config when parsing files as templates
pip install pygments; for highlight_code()
pip install unidecode; for remove_non_ascii()
```

Or use `pip install commonkit[strings]` to install all of these dependencies.

### Shell

Full shell support requires colorama and tabulate:

```bash
pip install colorama; for shell.feedback
pip install tabulate; for shell.tables
```

Or use `pip install commonkit[shell]`.

