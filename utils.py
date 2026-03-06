"""Utility helpers for steel delay analysis."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def clean_column_names(columns: Iterable[str]) -> list[str]:
    """Normalize column names to expected underscore format."""
    cleaned = []
    for col in columns:
        normalized = str(col).strip().replace(" ", "_")
        cleaned.append(normalized)
    return cleaned


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Validate dataframe contains required columns.

    Raises:
        ValueError: if any required columns are missing.
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def format_minutes(value: float) -> str:
    """Format minute values for display in the UI."""
    return f"{value:,.2f} min"
