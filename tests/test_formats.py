"""Tests for format handlers in datashift."""

import os
import pathlib
import tempfile
from typing import Dict, List

from data_shift.formats import csv_handler, json_handler, xml_handler


def test_csv_handler():
    """Test CSV handler read and write functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test data
        data = [
            {"name": "John", "age": "30", "city": "New York"},
            {"name": "Jane", "age": "25", "city": "San Francisco"},
        ]

        # Write to CSV
        csv_path = pathlib.Path(os.path.join(tmpdir, "test.csv"))
        csv_handler.write(data, csv_path)

        # Read from CSV
        read_data = csv_handler.read(csv_path)

        # Verify data
        assert len(read_data) == 2
        assert read_data[0]["name"] == "John"
        assert read_data[0]["age"] == "30"
        assert read_data[0]["city"] == "New York"
        assert read_data[1]["name"] == "Jane"
        assert read_data[1]["age"] == "25"
        assert read_data[1]["city"] == "San Francisco"


def test_json_handler():
    """Test JSON handler read and write functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test data
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "San Francisco"},
        ]

        # Write to JSON
        json_path = pathlib.Path(os.path.join(tmpdir, "test.json"))
        json_handler.write(data, json_path)

        # Read from JSON
        read_data = json_handler.read(json_path)

        # Verify data
        assert len(read_data) == 2
        assert read_data[0]["name"] == "John"
        assert read_data[0]["age"] == 30
        assert read_data[0]["city"] == "New York"
        assert read_data[1]["name"] == "Jane"
        assert read_data[1]["age"] == 25
        assert read_data[1]["city"] == "San Francisco"


def test_xml_handler() -> None:
    """Test XML handler read and write functions."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test data
        data: Dict[str, List[Dict[str, str]]] = {
            "people": [
                {"name": "John", "age": "30", "city": "New York"},
                {"name": "Jane", "age": "25", "city": "San Francisco"},
            ]
        }

        # Write to XML
        xml_path = pathlib.Path(os.path.join(tmpdir, "test.xml"))
        xml_handler.write(data, xml_path)

        # Read from XML
        read_data = xml_handler.read(xml_path)

        # Verify data
        assert "people" in read_data
        people = read_data["people"]
        assert isinstance(people, list)
        assert len(people) == 2
        assert people[0]["name"] == "John"
        assert people[0]["age"] == "30"
        assert people[0]["city"] == "New York"
        assert people[1]["name"] == "Jane"
        assert people[1]["age"] == "25"
        assert people[1]["city"] == "San Francisco"
