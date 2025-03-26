"""Tests for utility functions in datashift."""

import pathlib

import pytest

from data_shift.utils import detect_format, get_extension


def test_get_extension():
    """Test getting file extensions."""
    assert get_extension(pathlib.Path("file.csv")) == ".csv"
    assert get_extension(pathlib.Path("file.json")) == ".json"
    assert get_extension(pathlib.Path("file.xml")) == ".xml"
    assert get_extension(pathlib.Path("file.sqlite")) == ".sqlite"
    assert get_extension(pathlib.Path("file.sqlite3")) == ".sqlite3"
    assert get_extension(pathlib.Path("file.db")) == ".db"


def test_detect_format():
    """Test format detection from file extensions."""
    assert detect_format(pathlib.Path("file.csv")) == "csv"
    assert detect_format(pathlib.Path("file.json")) == "json"
    assert detect_format(pathlib.Path("file.xml")) == "xml"
    assert detect_format(pathlib.Path("file.sqlite")) == "sql"
    assert detect_format(pathlib.Path("file.sqlite3")) == "sql"
    assert detect_format(pathlib.Path("file.db")) == "sql"


def test_detect_format_unsupported():
    """Test detection of unsupported formats."""
    with pytest.raises(ValueError):
        detect_format(pathlib.Path("file.unsupported"))
