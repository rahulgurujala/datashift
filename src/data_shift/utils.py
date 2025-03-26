"""Utility functions for DataShift."""

import pathlib


def detect_format(path: pathlib.Path) -> str:
    """
    Detect the format of a file based on its extension.

    Args:
        path: Path to the file

    Returns:
        Format name as string
    """
    extension = get_extension(path)

    format_map = {
        ".csv": "csv",
        ".json": "json",
        ".xml": "xml",
        ".sqlite": "sql",
        ".sqlite3": "sql",
        ".db": "sql",
    }

    if extension in format_map:
        return format_map[extension]

    raise ValueError(f"Unsupported file extension: {extension}")


def get_extension(path: pathlib.Path) -> str:
    """Get the extension of a file."""
    return path.suffix.lower()
