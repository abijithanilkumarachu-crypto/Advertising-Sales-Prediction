"""
Model loading and prediction functions for the Advertising Sales Prediction Application.
Provides single and batch inference using the saved Polynomial Regression pipeline.
"""

import os
import warnings
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Suppress version unpickling warnings for clean UI logging
warnings.filterwarnings("ignore", category=UserWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "advertising_sales_model.pkl")

# Historical dataset boundary limits (from Advertising.csv)
HISTORICAL_BOUNDS = {
    "TV": {"min": 0.7, "max": 296.4},
    "radio": {"min": 0.0, "max": 49.6},
    "newspaper": {"min": 0.3, "max": 114.0}
}


@st.cache_resource
def load_trained_model():
    """
    Loads and caches the trained Polynomial Regression pipeline.
    Does not retrain or alter the saved model.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Saved model file not found at: {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)
    return model


def check_budget_bounds(tv: float, radio: float, newspaper: float) -> list[str]:
    """
    Checks if any input budget exceeds the historical training dataset maximums.
    Returns a list of advisory warning messages.
    """
    warnings_list = []
    if tv > HISTORICAL_BOUNDS["TV"]["max"]:
        warnings_list.append(f"TV budget (${tv:,.1f}k) exceeds the historical training maximum of ${HISTORICAL_BOUNDS['TV']['max']}k.")
    if radio > HISTORICAL_BOUNDS["radio"]["max"]:
        warnings_list.append(f"Radio budget (${radio:,.1f}k) exceeds the historical training maximum of ${HISTORICAL_BOUNDS['radio']['max']}k.")
    if newspaper > HISTORICAL_BOUNDS["newspaper"]["max"]:
        warnings_list.append(f"Newspaper budget (${newspaper:,.1f}k) exceeds the historical training maximum of ${HISTORICAL_BOUNDS['newspaper']['max']}k.")
    return warnings_list


def predict_single_sales(tv: float, radio: float, newspaper: float) -> dict:
    """
    Predicts sales for a single set of TV, Radio, and Newspaper advertising budgets.

    Parameters:
        tv (float): TV advertising budget (thousands of dollars)
        radio (float): Radio advertising budget (thousands of dollars)
        newspaper (float): Newspaper advertising budget (thousands of dollars)

    Returns:
        dict: Exact predicted sales and boundary advisory warnings.
    """
    if tv < 0 or radio < 0 or newspaper < 0:
        raise ValueError("Advertising budgets cannot be negative.")

    model = load_trained_model()

    # Exact column names and order expected by the pipeline
    input_df = pd.DataFrame([{
        "TV": float(tv),
        "radio": float(radio),
        "newspaper": float(newspaper)
    }])

    raw_prediction = float(model.predict(input_df)[0])

    # Sales cannot be negative in physical reality
    prediction = max(0.0, raw_prediction)
    bounds_warnings = check_budget_bounds(tv, radio, newspaper)

    return {
        "prediction": prediction,
        "input_data": {"TV": tv, "radio": radio, "newspaper": newspaper},
        "is_out_of_bounds": len(bounds_warnings) > 0,
        "bounds_warnings": bounds_warnings
    }


def validate_and_prepare_batch_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Validates uploaded CSV columns and normalizes column headers to 'TV', 'radio', 'newspaper'.
    Returns (cleaned_df, error_messages).
    """
    errors = []

    if df.empty:
        errors.append("The uploaded CSV file contains no data.")
        return df, errors

    # Case-insensitive column matching
    col_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip().lower()
        if clean_col == "tv":
            col_mapping[col] = "TV"
        elif clean_col in ["radio", "rad"]:
            col_mapping[col] = "radio"
        elif clean_col in ["newspaper", "news", "np"]:
            col_mapping[col] = "newspaper"

    df_renamed = df.rename(columns=col_mapping)

    required_cols = ["TV", "radio", "newspaper"]
    missing_cols = [c for c in required_cols if c not in df_renamed.columns]

    if missing_cols:
        errors.append(f"Missing required column(s): {', '.join(missing_cols)}. The CSV must contain TV, radio, and newspaper columns.")
        return df_renamed, errors

    # Check for non-numeric values
    for c in required_cols:
        non_numeric = pd.to_numeric(df_renamed[c], errors="coerce").isna().sum()
        if non_numeric > 0:
            errors.append(f"Column '{c}' contains {non_numeric} invalid non-numeric value(s).")

    # If numeric conversion succeeded, check for negative numbers
    if not errors:
        for c in required_cols:
            df_renamed[c] = pd.to_numeric(df_renamed[c])
            neg_count = (df_renamed[c] < 0).sum()
            if neg_count > 0:
                errors.append(f"Column '{c}' contains {neg_count} negative budget value(s). Budgets must be non-negative.")

    return df_renamed, errors


def predict_batch_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Generates batch predictions for a validated DataFrame.
    Appends 'Predicted_Sales' (exact pipeline prediction, clipped at 0).
    Returns (result_df, out_of_bounds_count).
    """
    model = load_trained_model()

    features_df = df[["TV", "radio", "newspaper"]].astype(float)
    raw_preds = model.predict(features_df)

    result_df = df.copy()
    result_df["Predicted_Sales"] = np.clip(raw_preds, a_min=0.0, a_max=None).round(2)

    # Count rows exceeding historical bounds
    out_of_bounds_mask = (
        (df["TV"] > HISTORICAL_BOUNDS["TV"]["max"]) |
        (df["radio"] > HISTORICAL_BOUNDS["radio"]["max"]) |
        (df["newspaper"] > HISTORICAL_BOUNDS["newspaper"]["max"])
    )
    out_of_bounds_count = int(out_of_bounds_mask.sum())

    return result_df, out_of_bounds_count
