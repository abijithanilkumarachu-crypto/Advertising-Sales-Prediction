"""
Data loading and project benchmark metrics for the Advertising Sales Prediction Application.
"""

import os
import pandas as pd
import streamlit as st


# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "Advertising.csv")

# Exact metrics recorded in Advertising_Sales_Prediction.ipynb
MODEL_BENCHMARKS = [
    {
        "Algorithm": "Simple Linear Regression",
        "Features Used": "TV only",
        "MAE": 2.444420,
        "MSE": 10.204654,
        "RMSE": 3.194472,
        "R2 Score": 0.676695,
        "Mean CV R2": 0.514143,
        "CV Std Dev": 0.208333,
        "Is Best": False
    },
    {
        "Algorithm": "Multiple Linear Regression",
        "Features Used": "TV, Radio, Newspaper",
        "MAE": 1.460757,
        "MSE": 3.174097,
        "RMSE": 1.781600,
        "R2 Score": 0.899438,
        "Mean CV R2": 0.870265,
        "CV Std Dev": 0.071844,
        "Is Best": False
    },
    {
        "Algorithm": "Polynomial Regression (Degree 2)",
        "Features Used": "TV, Radio, Newspaper (Poly terms)",
        "MAE": 0.526179,
        "MSE": 0.412910,
        "RMSE": 0.642581,
        "R2 Score": 0.986918,
        "Mean CV R2": 0.977835,
        "CV Std Dev": 0.017043,
        "Is Best": True
    },
    {
        "Algorithm": "Random Forest Regression",
        "Features Used": "TV, Radio, Newspaper (100 Trees)",
        "MAE": 0.620325,
        "MSE": 0.590926,
        "RMSE": 0.768717,
        "R2 Score": 0.981278,
        "Mean CV R2": 0.966255,
        "CV Std Dev": 0.013162,
        "Is Best": False
    }
]

# Random Forest Feature Importance from Cell 63
FEATURE_IMPORTANCE_DATA = {
    "TV": 0.624810,
    "radio": 0.362214,
    "newspaper": 0.012976
}

# Key benchmark metrics for the selected model
SELECTED_MODEL_METRICS = {
    "name": "Polynomial Regression (Degree 2)",
    "mae": 0.5262,
    "mse": 0.4129,
    "rmse": 0.6426,
    "r2": 0.9869,
    "cv_r2": 0.9778,
    "cv_std": 0.0170,
    "test_sample_pred": {
        "input": {"TV": 150.0, "radio": 25.0, "newspaper": 20.0},
        "expected_sales": 15.1393
    }
}


@st.cache_data
def load_dataset() -> pd.DataFrame:
    """Loads and caches the Advertising dataset without modifying the original file."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Dataset not found at: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df


def get_benchmark_df() -> pd.DataFrame:
    """Returns the benchmark results as a pandas DataFrame."""
    return pd.DataFrame(MODEL_BENCHMARKS)


def get_feature_importance_df() -> pd.DataFrame:
    """Returns feature importance data as a sorted DataFrame."""
    df_fi = pd.DataFrame([
        {"Feature": "TV Advertising", "Channel": "TV", "Importance": FEATURE_IMPORTANCE_DATA["TV"]},
        {"Feature": "Radio Advertising", "Channel": "radio", "Importance": FEATURE_IMPORTANCE_DATA["radio"]},
        {"Feature": "Newspaper Advertising", "Channel": "newspaper", "Importance": FEATURE_IMPORTANCE_DATA["newspaper"]},
    ])
    return df_fi.sort_values(by="Importance", ascending=False).reset_index(drop=True)
