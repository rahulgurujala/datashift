"""
DataShift: Transform any data format into any other with one call, no schema.

Supported formats:
- CSV
- JSON
- XML
- SQL (SQLite)
"""

from .core import shift

__version__ = "0.1.0"
__all__ = ["shift"]


def hello() -> str:
    """Return a greeting message."""
    return "Hello from data-shift!"
