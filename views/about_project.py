"""
About Project View: Objectives, Methodology, Mathematical Framework, Features & Limitations.
"""

import streamlit as st
from utils.ui_components import render_page_header


def show():
    render_page_header(
        title="About Advertising Sales Prediction",
        subtitle="Comprehensive technical documentation, methodology, mathematical formulation, and model limitations.",
        badge="Documentation & Architecture"
    )

    tab_overview, tab_math, tab_workflow, tab_limits = st.tabs([
        "🎯 Objectives & Overview",
        "📐 Mathematical Formulation",
        "🔄 Methodology & Workflow",
        "⚠️ Limitations & Considerations"
    ])

    with tab_overview:
        st.subheader("1. Business & Project Objectives")
        st.markdown(
            """
            In commercial marketing, allocating promotional budgets across diverse media channels 
            is critical for maximizing return on marketing investment.

            **Core Objectives:**
            - **Quantify Impact:** Analyze the historical empirical relationship between marketing spend across **TV**, **Radio**, and **Newspaper** and the resulting **Sales** volume.
            - **Detect Cross-Channel Synergy:** Determine whether multi-channel campaigns exhibit compounding multiplier effects compared to isolated single-channel promotions.
            - **Compare Candidate Algorithms:** Rigorously evaluate multiple regression paradigms under identical validation criteria.
            - **Interactive Decision Support:** Deliver an accessible, high-performance web dashboard allowing non-technical stakeholders to test budget allocation scenarios in real time.
            """
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("2. Key Features of this Application")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                - **Interactive Budget Simulator:** Synchronized sliders and numeric inputs with instant visual sales forecasting.
                - **Preset Budget Scenarios:** One-click comparisons against baseline, average, TV-heavy, and high-synergy mixes.
                - **Marginal ROI Analyzer:** Dynamic sensitivity analysis revealing the projected incremental sales for +$10k invested in each channel.
                """
            )
        with c2:
            st.markdown(
                """
                - **Automated Batch Inference:** Bulk CSV file processing with automated column validation, data cleansing, and enriched exports.
                - **Transparent Model Comparison:** Direct side-by-side benchmark of MAE, MSE, RMSE, Test $R^2$, and 5-Fold Cross-Validation.
                - **Interactive Visual Analytics:** Rich Plotly charts including correlation heatmaps, regression scatter plots, and budget allocation donuts.
                """
            )

    with tab_math:
        st.subheader("Mathematical Formulation of the Selected Model")
        st.markdown(
            """
            The deployed production model uses **Polynomial Features (Degree 2) coupled with Ordinary Least Squares (OLS) Linear Regression**.

            #### 1. Why Standard Multiple Linear Regression is Insufficient:
            A standard multiple linear regression model assumes strictly additive and independent channel responses:
            $$\\text{Sales} = \\beta_0 + \\beta_1(\\text{TV}) + \\beta_2(\\text{radio}) + \\beta_3(\\text{newspaper}) + \\epsilon$$
            This fails to capture the common marketing phenomenon where consumer exposure across television reinforces radio recall (cross-channel synergy).

            #### 2. Degree-2 Polynomial Expansion:
            The input feature vector $\\mathbf{x} = [\\text{TV}, \\text{radio}, \\text{newspaper}]$ is expanded non-linearly into 9 terms (with bias excluded):
            $$\\phi(\\mathbf{x}) = \\left[ \\text{TV},\\; \\text{radio},\\; \\text{newspaper},\\; \\text{TV}^2,\\; \\text{TV} \\cdot \\text{radio},\\; \\text{TV} \\cdot \\text{newspaper},\\; \\text{radio}^2,\\; \\text{radio} \\cdot \\text{newspaper},\\; \\text{newspaper}^2 \\right]$$

            #### 3. Prediction Equation:
            $$\\widehat{\\text{Sales}} = \\beta_0 + \\sum_{k=1}^{9} \\beta_k \\phi_k(\\mathbf{x})$$

            - **Intercept ($\\beta_0$):** $\\approx 4.9390$
            - **TV × Radio Synergy Term:** Positive weight of $+0.00111$, mathematically formalizing the multi-channel boost observed in empirical sales data.
            """
        )

    with tab_workflow:
        st.subheader("End-to-End Machine Learning Pipeline")
        st.markdown(
            """
            The machine learning workflow followed strict reproducible data science best practices:

            1. **Data Ingestion & Cleansing:**
               - Checked for null values (0 found) and duplicate entries (0 found).
               - Stripped non-informative serial index columns (`Unnamed: 0`).
            2. **Exploratory Data Analysis (EDA):**
               - Distribution checks (KDE & Histograms) and outlier identification (Boxplots).
               - Correlation analysis ($r_{\\text{TV}} = 0.782$, $r_{\\text{radio}} = 0.576$, $r_{\\text{newspaper}} = 0.228$).
            3. **Train-Test Split & Validation Strategy:**
               - 80% Training subset (160 samples) and 20% Testing subset (40 samples) with seed fixed at `random_state=42`.
               - 5-Fold Cross-Validation (`KFold(n_splits=5, shuffle=True, random_state=42)`) to verify model generalizability across diverse data slices.
            4. **Algorithm Benchmarking:**
               - Evaluated Simple Linear Regression, Multiple Linear Regression, Polynomial Regression, and Random Forest.
            5. **Model Serialization:**
               - Encapsulated preprocessor and regressor within an `sklearn.pipeline.Pipeline` and exported via `joblib`.
            6. **Deployment:**
               - Served via this modular Streamlit web application.
            """
        )

    with tab_limits:
        st.subheader("Project Limitations & Operating Boundaries")
        st.markdown(
            """
            In accordance with the findings documented in the original project analysis, users should note the following constraints:

            - **Compact Dataset Size:** The model was trained on 200 historical records. While performance on this sample is high ($R^2 = 98.69\%$), small datasets may not capture rare macroeconomic events.
            - **Excluded Confounding Variables:** The dataset only tracks media expenditure. Real-world sales are influenced by other variables such as unit pricing, competitor discounting, promotions, seasonality, brand equity, and macroeconomic sentiment.
            - **Historical Market Calibration:** Historical consumer conversion rates may shift as digital media consumption habits evolve over time.
            - **Extrapolation Boundaries:** Extreme budget extrapolations significantly beyond training ranges (e.g., TV > $350k or Radio > $60k) may produce diminishing-return divergence.
            - **Correlation vs. Causation:** Identified mathematical associations reflect statistical correlation and should be combined with domain judgment and controlled A/B experiments.
            """
        )


if __name__ == "__main__":
    show()
