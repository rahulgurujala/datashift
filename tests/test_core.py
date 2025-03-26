"""Tests for the core functionality of datashift."""

import os
import tempfile

from data_shift import shift


def test_shift_csv_to_json():
    """Test converting from CSV to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test CSV file
        csv_path = os.path.join(tmpdir, "test.csv")
        with open(csv_path, "w") as f:
            f.write("name,age,city\n")
            f.write("John,30,New York\n")
            f.write("Jane,25,San Francisco\n")

        # Output JSON path
        json_path = os.path.join(tmpdir, "output.json")

        # Convert CSV to JSON
        shift(csv_path, json_path)

        # Verify the JSON file was created
        assert os.path.exists(json_path)

        # Read the JSON file to verify content
        import json

        with open(json_path, "r") as f:
            data = json.load(f)

        # Verify the data
        assert len(data) == 2
        assert data[0]["name"] == "John"
        assert data[0]["age"] == "30"
        assert data[0]["city"] == "New York"
        assert data[1]["name"] == "Jane"
        assert data[1]["age"] == "25"
        assert data[1]["city"] == "San Francisco"


def test_shift_json_to_csv():
    """Test converting from JSON to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test JSON file
        json_path = os.path.join(tmpdir, "test.json")
        data = [
            {"name": "John", "age": 30, "city": "New York"},
            {"name": "Jane", "age": 25, "city": "San Francisco"},
        ]
        with open(json_path, "w") as f:
            import json

            json.dump(data, f)

        # Output CSV path
        csv_path = os.path.join(tmpdir, "output.csv")

        # Convert JSON to CSV
        shift(json_path, csv_path)

        # Verify the CSV file was created
        assert os.path.exists(csv_path)

        # Read the CSV file to verify content
        import csv

        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Verify the data
        assert len(rows) == 2
        assert rows[0]["name"] == "John"
        assert rows[0]["age"] == "30"
        assert rows[0]["city"] == "New York"
        assert rows[1]["name"] == "Jane"
        assert rows[1]["age"] == "25"
        assert rows[1]["city"] == "San Francisco"
