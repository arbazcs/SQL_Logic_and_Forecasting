"""Operational metric calculations for delay analytics."""

from __future__ import annotations

import pandas as pd

CONTROLLABLE_CATEGORIES = {
    "Equipment Breakdown",
    "Quality Hold",
    "Planned Maintenance",
}

EXTERNAL_CATEGORIES = {
    "Power Outage",
    "Material Shortage",
}


def average_delay_by_stage(df: pd.DataFrame) -> pd.DataFrame:
    """Return average delay grouped by production stage."""
    result = (
        df.groupby("Production_Stage", as_index=False)["Delay_Minutes"]
        .mean()
        .rename(columns={"Delay_Minutes": "Average_Delay_Minutes"})
        .sort_values("Average_Delay_Minutes", ascending=False)
    )
    return result


def total_delay_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Return total delay grouped by delay category."""
    result = (
        df.groupby("Delay_Category", as_index=False)["Delay_Minutes"]
        .sum()
        .rename(columns={"Delay_Minutes": "Total_Delay_Minutes"})
        .sort_values("Total_Delay_Minutes", ascending=False)
    )
    return result


def delay_by_shift(df: pd.DataFrame) -> pd.DataFrame:
    """Return average delay grouped by shift."""
    result = (
        df.groupby("Shift", as_index=False)["Delay_Minutes"]
        .mean()
        .rename(columns={"Delay_Minutes": "Average_Delay_Minutes"})
        .sort_values("Average_Delay_Minutes", ascending=False)
    )
    return result


def stage_bottleneck(df: pd.DataFrame) -> str:
    """Return the stage with the highest average delay."""
    stage_delay = average_delay_by_stage(df)
    if stage_delay.empty:
        return "N/A"
    return str(stage_delay.iloc[0]["Production_Stage"])


def controllable_vs_external(df: pd.DataFrame) -> pd.DataFrame:
    """Return percentage split of controllable vs external delays."""
    category_delay = df.groupby("Delay_Category")["Delay_Minutes"].sum()

    controllable_total = category_delay.loc[
        category_delay.index.intersection(CONTROLLABLE_CATEGORIES)
    ].sum()
    external_total = category_delay.loc[
        category_delay.index.intersection(EXTERNAL_CATEGORIES)
    ].sum()

    total = controllable_total + external_total
    if total == 0:
        return pd.DataFrame(
            {
                "Class": ["Controllable", "External"],
                "Percentage": [0.0, 0.0],
            }
        )

    return pd.DataFrame(
        {
            "Class": ["Controllable", "External"],
            "Percentage": [
                round((controllable_total / total) * 100, 2),
                round((external_total / total) * 100, 2),
            ],
        }
    )
