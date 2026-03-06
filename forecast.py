"""Forecasting logic for delivery delay estimation."""

from __future__ import annotations

import math
from typing import Dict

import pandas as pd

from analysis import average_delay_by_stage


def calculate_heats_required(order_tonnage: float, heat_capacity: float = 80) -> int:
    """Calculate number of heats required to fulfill an order."""
    if heat_capacity <= 0:
        raise ValueError("heat_capacity must be greater than 0")
    if order_tonnage <= 0:
        return 0
    return int(math.ceil(order_tonnage / heat_capacity))


def expected_delay_per_heat(df: pd.DataFrame) -> float:
    """Compute expected delay per heat from average stage delays."""
    avg_stage = average_delay_by_stage(df)
    if avg_stage.empty:
        return 0.0
    return float(avg_stage["Average_Delay_Minutes"].sum())


def estimate_total_delay(df: pd.DataFrame, heats: int) -> float:
    """Estimate total delay for a given number of heats."""
    if heats <= 0:
        return 0.0
    return expected_delay_per_heat(df) * heats


def add_buffer(delay_minutes: float, buffer_percent: float = 25) -> float:
    """Add contingency buffer to delay estimate."""
    if delay_minutes <= 0:
        return 0.0
    return delay_minutes * (buffer_percent / 100)


def final_delivery_estimate(df: pd.DataFrame, order_tonnage: float) -> Dict[str, float]:
    """Generate final delivery delay estimate with buffer.

    Returns:
        Dictionary with heats required, expected delay, buffer, and final delay.
    """
    heats = calculate_heats_required(order_tonnage)
    expected_delay = estimate_total_delay(df, heats)
    buffer = add_buffer(expected_delay)
    final_estimate = expected_delay + buffer

    return {
        "heats_required": float(heats),
        "expected_delay_minutes": round(expected_delay, 2),
        "buffer_minutes": round(buffer, 2),
        "final_estimated_delay_minutes": round(final_estimate, 2),
    }
