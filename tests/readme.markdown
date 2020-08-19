# Testing

Tests are located in this directory.

## Set Up for Testing

Install requirements:

`pip install tests/requirements.pip`

### Database Testing

Install requirements:

```bash
pip install SQLAlchemy;
pip install tablib;
```

**MS SQL**

Testing the MSSQL backend requires `pyodbc` which in turns depends upon a system library.

```bash
# See: https://apple.stackexchange.com/a/303331
brew tap microsoft/msodbcsql https://github.com/Microsoft/homebrew-mssql-release;
brew reinstall msodbcsql mssql-tools;
```

The with the virtual environment activated, run `pip install pyodbc`

**My SQL**

Testing the MySQL backend requires `MySQL-python`. However, this package appears to be lacking support for Python 3. See error when running `pip install MySQL-python`.

> Testing is skipped for now.

**Oracle**

Testing the Oracle backend requires `cx_Oracle`: `pip install cx_Oracle`.

**PostgreSQL**

Testing the Postgres backend requires `psycopg2`: `pip install psycopg2-binary`

## Running Tests

Run all tests with coverage:

``make tests``

Run a specific test:

``python -m pytest tests/test_name.py``

Example:

``python -m pytest tests/test_packages.py``

To allow output from print statements within a test method, add the ``-s`` switch:

``python -m pytest -s tests/test_name.py``

> Tip: Add ``-v`` to list the tests with PASS/FAIL.

## Reference

- [coverage](https://coverage.readthedocs.io/en/v4.5.x/)
- [pytest](https://pytest.org)
- [pytest-pythonpath](https://github.com/bigsassy/pytest-pythonpath)
