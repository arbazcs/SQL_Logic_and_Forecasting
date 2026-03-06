"""Data loading module for steel delay analysis."""

from __future__ import annotations

from typing import IO

import pandas as pd

from utils import clean_column_names, validate_required_columns

REQUIRED_COLUMNS: list[str] = [
    "Heat_Number",
    "Product_Type",
    "Production_Stage",
    "Planned_Start_DateTime",
    "Actual_Start_DateTime",
    "Delay_Minutes",
    "Delay_Category",
    "Shift",
]


def load_dataset(file: IO[bytes]) -> pd.DataFrame:
    """Load and validate a steel delay dataset from CSV or Excel.

    Args:
        file: Uploaded file-like object from Streamlit uploader.

    Returns:
        Cleaned and validated dataframe.

    Raises:
        ValueError: If file type is unsupported or required columns are missing.
    """
    filename = getattr(file, "name", "")
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(file)
    elif filename.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

    df.columns = clean_column_names(df.columns)
    validate_required_columns(df, REQUIRED_COLUMNS)

    df["Delay_Minutes"] = pd.to_numeric(df["Delay_Minutes"], errors="coerce").fillna(0.0)

    for col in ["Planned_Start_DateTime", "Actual_Start_DateTime"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return df
