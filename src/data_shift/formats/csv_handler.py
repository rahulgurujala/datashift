"""CSV format handler for DataShift."""

import csv
import pathlib
from typing import Any, Dict, List, Union


def read(path: pathlib.Path, **kwargs: Any) -> List[Dict[str, Any]]:
    """
    Read data from a CSV file.

    Args:
        path: Path to the CSV file
        **kwargs: Additional options for CSV reading

    Returns:
        List of dictionaries representing the CSV data
    """
    delimiter = kwargs.get("delimiter", ",")

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [dict(row) for row in reader]


def write(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    path: pathlib.Path,
    **kwargs: Any,
) -> None:
    """
    Write data to a CSV file.

    Args:
        data: Data to write (list of dictionaries or dictionary)
        path: Path to the CSV file
        **kwargs: Additional options for CSV writing
    """
    delimiter = kwargs.get("delimiter", ",")

    # Convert single dict to list if needed
    if isinstance(data, dict):
        data = [data]

    # Ensure we have data to write
    if not data:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return

    # Get fieldnames from the first row
    fieldnames = list(data[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)
