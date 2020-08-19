import os
import pytest

INSERTS = (
    {
        'title': "Page 1",
        'body': "This is page 1.",
        'popularity': 1.0,
        'published_dt': "2020-01-01 10:20:05.123",
        'display_date': "2020-01-01",
    },
    {
        'title': "Page 2",
        'body': "This is page 2.",
        'popularity': 2.0,
        'published_dt': "2020-02-01 10:20:05.123",
        'display_date': "2020-02-01",
    },
    {
        'title': "Page 3",
        'body': "This is page 3.",
        'popularity': 3.0,
        'published_dt': "2020-03-01 10:20:05.123",
        'display_date': "2020-03-01",
    },
)

TEST_TABLE = """CREATE TABLE IF NOT EXISTS test_page (
id INTEGER PRIMARY KEY AUTOINCREMENT,
parent INTEGER,
title VARCHAR(128) NOT NULL,
type VARCHAR(64) DEFAULT 'page',
draft BOOL DEFAULT 1,
body TEXT,
published_dt VARCHAR(32),
display_date VARCHAR(10),
popularity REAL,
FOREIGN KEY (parent) REFERENCES page(test_page_id)
);"""


@pytest.fixture
def database_handle():
    from commonkit.database.factory import load_database

    path = os.path.join("tests", "tmp.db")
    db = load_database("sqlite", path=path, prefix="test")
    db.raw(TEST_TABLE)

    for values in INSERTS:
        db.insert("page", values)

    yield db

    os.remove(path)
