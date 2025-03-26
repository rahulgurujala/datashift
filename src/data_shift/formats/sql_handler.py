"""SQL format handler for DataShift."""

import pathlib
import sqlite3
from typing import Any, Dict, List, Union


def read(path: pathlib.Path, **kwargs: Any) -> Dict[str, List[Dict[str, Any]]]:
    """
    Read data from a SQLite database.

    Args:
        path: Path to the SQLite database
        **kwargs: Additional options for SQL reading

    Returns:
        Dictionary with table names as keys and lists of row dictionaries as values
    """
    table_name = kwargs.get("table")

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    result: Dict[str, List[Dict[str, Any]]] = {}

    # Get list of tables
    if table_name:
        tables = [table_name]
    else:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

    # Read data from each table
    for table in tables:
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        result[table] = [dict(row) for row in rows]

    conn.close()
    return result


def write(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    path: pathlib.Path,
    **kwargs: Any,
) -> None:
    """
    Write data to a SQLite database.

    Args:
        data: Data to write (list of dictionaries or dictionary)
        path: Path to the SQLite database
        **kwargs: Additional options for SQL writing
    """
    table_name = kwargs.get("table", "data")

    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Handle different data structures
    if isinstance(data, list):
        # List of dictionaries -> single table
        _create_and_populate_table(cursor, table_name, data)
    elif isinstance(data, dict):
        # Check if it's a dict of tables
        if all(isinstance(v, list) for v in data.values()):
            # Dict of tables
            for table, rows in data.items():
                if rows:  # Only create tables with data
                    _create_and_populate_table(cursor, table, rows)
        else:
            # Single row -> single table with one row
            _create_and_populate_table(cursor, table_name, [data])

    conn.commit()
    conn.close()


def _create_and_populate_table(
    cursor: sqlite3.Cursor, table_name: str, rows: List[Dict[str, Any]]
) -> None:
    """Create a table and populate it with data."""
    if not rows:
        return

    # Get column names and types from the first row
    first_row = rows[0]
    columns = []

    for key, value in first_row.items():
        col_type = "TEXT"
        if isinstance(value, int):
            col_type = "INTEGER"
        elif isinstance(value, float):
            col_type = "REAL"
        columns.append(f'"{key}" {col_type}')

    # Create table
    create_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({", ".join(columns)});'
    cursor.execute(create_query)

    # Insert data
    for row in rows:
        keys = [f'"{k}"' for k in row.keys()]
        placeholders = ["?" for _ in keys]
        insert_query = f'INSERT INTO "{table_name}" ({", ".join(keys)}) \
            VALUES ({", ".join(placeholders)});'
        cursor.execute(insert_query, list(row.values()))
