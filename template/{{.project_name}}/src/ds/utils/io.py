"""I/O helpers for Unity Catalog tables."""
from typing import Optional


def table_full_name(table: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> str:
    return f"{catalog+'.' if catalog else ''}{schema+'.' if schema else ''}{table}"
