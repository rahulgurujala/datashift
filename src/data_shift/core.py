"""Core functionality for DataShift."""

import pathlib
from typing import Any, Dict, List, Union

from .formats import csv_handler, json_handler, sql_handler, xml_handler
from .utils import detect_format


def shift(
    source: Union[str, pathlib.Path],
    destination: Union[str, pathlib.Path],
    **kwargs: Any,
) -> None:
    """
    Transform data from one format to another.

    Args:
        source: Path to source file or database
        destination: Path to destination file or database
        **kwargs: Additional options for specific formats

    Examples:
        >>> from datashift import shift
        >>> shift("data.csv", "output.json")  # CSV to JSON
        >>> shift("db.sqlite", "data.xml")    # SQL to XML
    """
    # Convert to Path objects
    src_path = pathlib.Path(source)
    dst_path = pathlib.Path(destination)

    # Detect formats
    src_format = kwargs.get("src_format") or detect_format(src_path)
    dst_format = kwargs.get("dst_format") or detect_format(dst_path)

    # Read data from source
    data = _read_data(src_path, src_format, **kwargs)

    # Write data to destination
    _write_data(data, dst_path, dst_format, **kwargs)


def _read_data(
    path: pathlib.Path,
    format_type: str,
    **kwargs: Any,
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Read data from the source file based on its format."""
    if format_type == "csv":
        return csv_handler.read(path, **kwargs)
    elif format_type == "json":
        return json_handler.read(path, **kwargs)
    elif format_type == "xml":
        return xml_handler.read(path, **kwargs)
    elif format_type == "sql":
        return sql_handler.read(path, **kwargs)
    else:
        raise ValueError(f"Unsupported source format: {format_type}")


def _write_data(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    path: pathlib.Path,
    format_type: str,
    **kwargs: Any,
) -> None:
    """Write data to the destination file based on its format."""
    if format_type == "csv":
        csv_handler.write(data, path, **kwargs)
    elif format_type == "json":
        json_handler.write(data, path, **kwargs)
    elif format_type == "xml":
        xml_handler.write(data, path, **kwargs)
    elif format_type == "sql":
        sql_handler.write(data, path, **kwargs)
    else:
        raise ValueError(f"Unsupported destination format: {format_type}")
