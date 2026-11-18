"""
Model loading and prediction functions for the Advertising Sales Prediction Application.
Provides single and batch inference using the saved Polynomial Regression pipeline,
with seamless conversion from Indian Rupees (INR / ₹) to the model's USD-based scale.
"""

import os
import warnings
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils.currency import (
    DEFAULT_USD_TO_INR,
    inr_to_model_units,
    model_units_to_inr,
    format_inr_short,
    format_inr_currency
)

# Suppress version unpickling warnings for clean UI logging
warnings.filterwarnings("ignore", category=UserWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "advertising_sales_model.pkl")

# Historical dataset boundary limits (from Advertising.csv in thousands of USD)
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


def check_budget_bounds_inr(
    tv_inr: float,
    radio_inr: float,
    newspaper_inr: float,
    exchange_rate: float = DEFAULT_USD_TO_INR
) -> list[str]:
    """
    Checks if any input INR budget exceeds the historical training dataset maximums.
    Returns advisory warning messages formatted in INR and equivalent USD.
    """
    warnings_list = []
    tv_model = inr_to_model_units(tv_inr, exchange_rate)
    radio_model = inr_to_model_units(radio_inr, exchange_rate)
    newspaper_model = inr_to_model_units(newspaper_inr, exchange_rate)

    if tv_model > HISTORICAL_BOUNDS["TV"]["max"]:
        max_inr = model_units_to_inr(HISTORICAL_BOUNDS["TV"]["max"], exchange_rate)
        warnings_list.append(
            f"TV budget ({format_inr_short(tv_inr)}) exceeds the historical dataset training maximum "
            f"equivalent of {format_inr_short(max_inr)} (${HISTORICAL_BOUNDS['TV']['max']}k USD)."
        )
    if radio_model > HISTORICAL_BOUNDS["radio"]["max"]:
        max_inr = model_units_to_inr(HISTORICAL_BOUNDS["radio"]["max"], exchange_rate)
        warnings_list.append(
            f"Radio budget ({format_inr_short(radio_inr)}) exceeds the historical dataset training maximum "
            f"equivalent of {format_inr_short(max_inr)} (${HISTORICAL_BOUNDS['radio']['max']}k USD)."
        )
    if newspaper_model > HISTORICAL_BOUNDS["newspaper"]["max"]:
        max_inr = model_units_to_inr(HISTORICAL_BOUNDS["newspaper"]["max"], exchange_rate)
        warnings_list.append(
            f"Newspaper budget ({format_inr_short(newspaper_inr)}) exceeds the historical dataset training maximum "
            f"equivalent of {format_inr_short(max_inr)} (${HISTORICAL_BOUNDS['newspaper']['max']}k USD)."
        )
    return warnings_list


def predict_single_sales(
    tv_inr: float,
    radio_inr: float,
    newspaper_inr: float,
    exchange_rate: float = DEFAULT_USD_TO_INR
) -> dict:
    """
    Predicts sales for a single set of TV, Radio, and Newspaper advertising budgets in INR.
    Converts INR inputs to the model's USD scale before passing to the pipeline.

    Parameters:
        tv_inr (float): TV advertising budget in INR (₹)
        radio_inr (float): Radio advertising budget in INR (₹)
        newspaper_inr (float): Newspaper advertising budget in INR (₹)
        exchange_rate (float): USD to INR exchange rate (default: ₹90.0)

    Returns:
        dict: Exact predicted sales and boundary advisory warnings.
    """
    if tv_inr < 0 or radio_inr < 0 or newspaper_inr < 0:
        raise ValueError("Advertising budgets cannot be negative.")

    model = load_trained_model()

    # Convert INR to original model units (thousands of USD)
    tv_model = inr_to_model_units(tv_inr, exchange_rate)
    radio_model = inr_to_model_units(radio_inr, exchange_rate)
    newspaper_model = inr_to_model_units(newspaper_inr, exchange_rate)

    # Exact column names and order expected by the trained pipeline
    input_df = pd.DataFrame([{
        "TV": float(tv_model),
        "radio": float(radio_model),
        "newspaper": float(newspaper_model)
    }])

    raw_prediction = float(model.predict(input_df)[0])

    # Sales cannot be negative in physical reality
    prediction = max(0.0, raw_prediction)
    bounds_warnings = check_budget_bounds_inr(tv_inr, radio_inr, newspaper_inr, exchange_rate)

    return {
        "prediction": prediction,
        "input_inr": {"TV": tv_inr, "radio": radio_inr, "newspaper": newspaper_inr},
        "converted_model_units": {"TV": tv_model, "radio": radio_model, "newspaper": newspaper_model},
        "exchange_rate": exchange_rate,
        "is_out_of_bounds": len(bounds_warnings) > 0,
        "bounds_warnings": bounds_warnings
    }


def validate_and_prepare_batch_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Validates uploaded CSV columns and normalizes column headers to 'TV', 'radio', 'newspaper'.
    Supports headers like 'TV', 'tv', 'TV (INR)', 'Radio (₹)', etc.
    Returns (cleaned_df, error_messages).
    """
    errors = []

    if df.empty:
        errors.append("The uploaded CSV file contains no data.")
        return df, errors

    # Case-insensitive & currency suffix matching
    col_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip().lower().replace("(inr)", "").replace("(₹)", "").replace("_inr", "").strip()
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
        errors.append(
            f"Missing required column(s): {', '.join(missing_cols)}. "
            f"The CSV must contain TV, radio, and newspaper advertising budgets in INR (₹)."
        )
        return df_renamed, errors

    # Check for missing values / non-numeric values
    for c in required_cols:
        non_numeric = pd.to_numeric(df_renamed[c], errors="coerce").isna().sum()
        if non_numeric > 0:
            errors.append(f"Column '{c}' contains {non_numeric} invalid non-numeric or missing value(s).")

    # If numeric conversion succeeded, check for negative numbers
    if not errors:
        for c in required_cols:
            df_renamed[c] = pd.to_numeric(df_renamed[c])
            neg_count = (df_renamed[c] < 0).sum()
            if neg_count > 0:
                errors.append(f"Column '{c}' contains {neg_count} negative budget value(s). Budgets must be non-negative.")

    return df_renamed, errors


def predict_batch_sales(
    df: pd.DataFrame,
    exchange_rate: float = DEFAULT_USD_TO_INR
) -> tuple[pd.DataFrame, int]:
    """
    Generates batch predictions for a validated DataFrame containing INR budgets.
    Converts INR budgets to the model's USD scale before inference.
    Appends 'Predicted_Sales' (exact pipeline prediction, clipped at 0).
    Returns (result_df, out_of_bounds_count).
    """
    model = load_trained_model()

    # Convert INR to model units for each column
    tv_model = df["TV"].astype(float).apply(lambda x: inr_to_model_units(x, exchange_rate))
    radio_model = df["radio"].astype(float).apply(lambda x: inr_to_model_units(x, exchange_rate))
    newspaper_model = df["newspaper"].astype(float).apply(lambda x: inr_to_model_units(x, exchange_rate))

    features_df = pd.DataFrame({
        "TV": tv_model,
        "radio": radio_model,
        "newspaper": newspaper_model
    })

    raw_preds = model.predict(features_df)

    result_df = df.copy()
    result_df["Predicted_Sales"] = np.clip(raw_preds, a_min=0.0, a_max=None).round(2)

    # Count rows exceeding historical bounds
    out_of_bounds_mask = (
        (tv_model > HISTORICAL_BOUNDS["TV"]["max"]) |
        (radio_model > HISTORICAL_BOUNDS["radio"]["max"]) |
        (newspaper_model > HISTORICAL_BOUNDS["newspaper"]["max"])
    )
    out_of_bounds_count = int(out_of_bounds_mask.sum())

    return result_df, out_of_bounds_count
