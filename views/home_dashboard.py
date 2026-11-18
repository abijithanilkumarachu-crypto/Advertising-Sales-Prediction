"""
Home Dashboard View: Project Overview & Key Metrics.
Configured for Indian presentations with INR (₹) budget simulation.
"""

import streamlit as st
import plotly.express as px
from utils.ui_components import render_page_header, render_kpi_card, render_transparency_note
from utils.data_loader import SELECTED_MODEL_METRICS, get_feature_importance_df
from utils.model_loader import predict_single_sales
from utils.currency import DEFAULT_USD_TO_INR, format_inr_short


def show():
    render_page_header(
        title="Advertising Sales Prediction Dashboard",
        subtitle="Machine Learning solution for marketing budget optimization and sales forecasting with INR (₹) inputs.",
        badge="Production Model: Polynomial Regression (Deg 2)"
    )

    # Top Row: 4 Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            label="Selected Model",
            value="Polynomial Reg.",
            subtext="Degree 2 Pipeline",
            badge_good=True
        )
    with c2:
        render_kpi_card(
            label="Test R² Score",
            value=f"{SELECTED_MODEL_METRICS['r2'] * 100:.2f}%",
            subtext="Evaluated on 20% holdout",
            badge_good=True
        )
    with c3:
        render_kpi_card(
            label="Cross-Validation R²",
            value=f"{SELECTED_MODEL_METRICS['cv_r2'] * 100:.2f}%",
            subtext=f"± {SELECTED_MODEL_METRICS['cv_std'] * 100:.2f}% (5-Fold CV)",
            badge_good=True
        )
    with c4:
        render_kpi_card(
            label="Mean Absolute Error",
            value=f"{SELECTED_MODEL_METRICS['mae']:.3f}",
            subtext=f"RMSE: {SELECTED_MODEL_METRICS['rmse']:.3f} units",
            badge_good=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Middle Row: Project Summary & Channel Contribution
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("📌 Executive Summary")
        st.markdown(
            """
            This application enables marketing executives to forecast product sales from promotional investments
            across **Television**, **Radio**, and **Newspaper** channels using a validated Machine Learning pipeline.

            #### Key Highlights:
            - **Non-Linear Multi-Channel Synergies:** Traditional linear models assume channels act in isolation. 
              The selected **Polynomial Regression (Degree 2)** model captures real-world compounding effects (e.g., TV exposure reinforcing Radio recall).
            - **Superior Empirical Validation:** Outperformed Simple Linear Regression, Multiple Linear Regression, and Random Forest 
              across both holdout testing ($R^2 = 98.69\%$) and 5-fold cross-validation ($R^2 = 97.78\%$).
            - **Data-Driven Budget Allocation:** Identifies that spending on TV and Radio accounts for over 98% of predictable sales volume, 
              while Newspaper spending yields negligible marginal returns.
            - **Indian Market Adaptation:** Supports direct advertising budget inputs in **Indian Rupees (₹)** with an integrated conversion layer to the model's scale.
            """
        )

    with col_right:
        st.subheader("📊 Channel Importance Breakdown")
        df_fi = get_feature_importance_df()
        
        fig = px.bar(
            df_fi,
            x="Importance",
            y="Feature",
            orientation="h",
            text=df_fi["Importance"].apply(lambda x: f"{x * 100:.1f}%"),
            color="Importance",
            color_continuous_scale=[[0.0, "#174E4A"], [1.0, "#65C6AE"]],
            height=280
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=20, t=10, b=10),
            xaxis_title="Relative Impact on Sales",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            font=dict(family="Inter, sans-serif", color="#AABBB9")
        )
        fig.update_xaxes(showgrid=True, gridcolor="#22343A")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Bottom Row: Quick Model Verification Simulator in INR
    st.subheader("⚡ Quick Verification Simulator (INR ₹)")
    st.markdown(
        f"Test the model using the notebook baseline budget converted to Indian Rupees "
        f"*(Exchange Rate: 1 USD ≈ ₹{DEFAULT_USD_TO_INR:,.1f})*:"
    )

    q1, q2, q3, q4 = st.columns([1, 1, 1, 1.2])
    with q1:
        tv_input = st.number_input(
            "TV Budget (₹)",
            value=13_500_000,
            step=500_000,
            min_value=0,
            max_value=50_000_000,
            help=f"Default: ₹1.35 Cr (equivalent to $150k USD at ₹{DEFAULT_USD_TO_INR}/USD)"
        )
        st.caption(f"Selected: **{format_inr_short(tv_input)}**")
    with q2:
        radio_input = st.number_input(
            "Radio Budget (₹)",
            value=2_250_000,
            step=250_000,
            min_value=0,
            max_value=20_000_000,
            help=f"Default: ₹22.50 Lakh (equivalent to $25k USD at ₹{DEFAULT_USD_TO_INR}/USD)"
        )
        st.caption(f"Selected: **{format_inr_short(radio_input)}**")
    with q3:
        news_input = st.number_input(
            "Newspaper Budget (₹)",
            value=1_800_000,
            step=200_000,
            min_value=0,
            max_value=20_000_000,
            help=f"Default: ₹18.00 Lakh (equivalent to $20k USD at ₹{DEFAULT_USD_TO_INR}/USD)"
        )
        st.caption(f"Selected: **{format_inr_short(news_input)}**")
    with q4:
        st.markdown("**Sales Forecast**")
        res = predict_single_sales(tv_input, radio_input, news_input)
        st.success(f"**{res['prediction']:.2f}k units** (~{res['prediction']*1000:,.0f} units)")

    if res["is_out_of_bounds"]:
        st.caption("⚠️ *Note: One or more input budgets exceed the historical dataset training range.*")

    # Transparency Note
    render_transparency_note(DEFAULT_USD_TO_INR)


if __name__ == "__main__":
    show()
