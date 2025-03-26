"""JSON format handler for DataShift."""

import json
import pathlib
from typing import Any, Dict, List, Union, cast


def read(path: pathlib.Path) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Read data from a JSON file.

    Args:
        path: Path to the JSON file

    Returns:
        Data from the JSON file as a list of dictionaries or a dictionary
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Explicitly cast the return value to the expected type
    if isinstance(data, list):
        return cast(List[Dict[str, Any]], data)
    return cast(Dict[str, Any], data)


def write(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    path: pathlib.Path,
    **kwargs: Any,
) -> None:
    """
    Write data to a JSON file.

    Args:
        data: Data to write (list of dictionaries or dictionary)
        path: Path to the JSON file
        **kwargs: Additional options for JSON writing
    """
    indent = kwargs.get("indent", 2)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)
