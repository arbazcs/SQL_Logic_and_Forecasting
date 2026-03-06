"""Streamlit application for steel delay analysis and forecasting."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from analysis import (
    average_delay_by_stage,
    controllable_vs_external,
    delay_by_shift,
    stage_bottleneck,
    total_delay_by_category,
)
from data_loader import load_dataset
from forecast import final_delivery_estimate
from utils import format_minutes

st.set_page_config(page_title="Steel Delay Analysis", layout="wide")
st.title("Steel Manufacturing Delay Analysis & Forecast Tool")

uploaded_file = st.file_uploader(
    "Upload delay dataset (CSV or Excel)",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file:
    try:
        df = load_dataset(uploaded_file)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Operational Metrics")

    col1, col2 = st.columns(2)

    with col1:
        stage_avg = average_delay_by_stage(df)
        st.markdown("#### Average Delay by Production Stage")
        st.dataframe(stage_avg, use_container_width=True)
        fig_stage = px.bar(
            stage_avg,
            x="Production_Stage",
            y="Average_Delay_Minutes",
            title="Average Delay by Production Stage",
        )
        st.plotly_chart(fig_stage, use_container_width=True)

        shift_avg = delay_by_shift(df)
        st.markdown("#### Average Delay by Shift")
        st.dataframe(shift_avg, use_container_width=True)

    with col2:
        category_total = total_delay_by_category(df)
        st.markdown("#### Total Delay by Category")
        st.dataframe(category_total, use_container_width=True)
        fig_category = px.bar(
            category_total,
            x="Delay_Category",
            y="Total_Delay_Minutes",
            title="Total Delay by Category",
        )
        st.plotly_chart(fig_category, use_container_width=True)

        class_split = controllable_vs_external(df)
        st.markdown("#### Controllable vs External Delay (%)")
        st.dataframe(class_split, use_container_width=True)
        fig_split = px.pie(
            class_split,
            names="Class",
            values="Percentage",
            title="Controllable vs External Delay Share",
        )
        st.plotly_chart(fig_split, use_container_width=True)

    bottleneck = stage_bottleneck(df)
    st.info(f"Bottleneck Stage: **{bottleneck}**")

    st.subheader("Forecast Delivery Delays")
    order_tonnage = st.number_input(
        "Enter order tonnage",
        min_value=0.0,
        value=1000.0,
        step=10.0,
    )

    if order_tonnage > 0:
        forecast_result = final_delivery_estimate(df, order_tonnage)

        fcol1, fcol2, fcol3, fcol4 = st.columns(4)
        fcol1.metric("Heats Required", int(forecast_result["heats_required"]))
        fcol2.metric(
            "Expected Delay",
            format_minutes(forecast_result["expected_delay_minutes"]),
        )
        fcol3.metric("Buffer", format_minutes(forecast_result["buffer_minutes"]))
        fcol4.metric(
            "Final Estimated Delay",
            format_minutes(forecast_result["final_estimated_delay_minutes"]),
        )
else:
    st.info("Upload a dataset to begin analysis.")
