# Steel Manufacturing Delay Analysis & Forecast Tool

## Project Overview

This project provides a modular analytics application to analyze steel production delay records and forecast delivery delay risk for incoming orders. It includes:

- Data ingestion and validation for CSV/Excel datasets.
- Operational delay metrics by stage, category, and shift.
- Bottleneck stage detection.
- Controllable vs external delay breakdown.
- Delay forecast based on required heats and a configurable planning buffer.
- Interactive Streamlit dashboard for business users.

## Project Structure

```text
steel_delay_analysis/
│
├── app.py
├── analysis.py
├── forecast.py
├── data_loader.py
├── utils.py
├── requirements.txt
└── README.md
```

## Dataset Format

Expected columns:

- `Heat_Number`
- `Product_Type`
- `Production_Stage`
- `Planned_Start_DateTime`
- `Actual_Start_DateTime`
- `Delay_Minutes`
- `Delay_Category`
- `Shift`

Each row represents a production stage delay event for a steel production heat.

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Launch the Streamlit app:

```bash
streamlit run app.py
```

3. Upload a CSV or Excel file and inspect:
   - average delay by stage
   - total delay by category
   - shift delay performance
   - controllable vs external delay split
   - bottleneck stage
   - delivery delay forecast for selected order tonnage

## Example Usage

1. Open the dashboard in your browser after starting Streamlit.
2. Upload your delay event dataset.
3. Enter an order tonnage value in the forecast panel.
4. Review heats required, expected delay, buffer, and final estimate.
