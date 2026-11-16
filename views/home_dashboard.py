"""
Home Dashboard View: Project Overview & Key Metrics.
"""

import streamlit as st
import plotly.express as px
from utils.ui_components import render_page_header, render_kpi_card
from utils.data_loader import SELECTED_MODEL_METRICS, get_feature_importance_df
from utils.model_loader import predict_single_sales


def show():
    render_page_header(
        title="Advertising Sales Prediction Dashboard",
        subtitle="Machine Learning solution for marketing budget optimization and sales forecasting.",
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
            This application enables marketing teams to forecast product sales from advertising investments
            across **TV**, **Radio**, and **Newspaper** channels using a validated Machine Learning pipeline.

            #### Key Highlights:
            - **Non-Linear Synergies:** Traditional linear regression assumes channels act independently. 
              The selected **Polynomial Regression (Degree 2)** model captures real-world multiplier effects (e.g., TV and Radio reinforcement).
            - **Superior Validation:** Outperformed Simple Linear Regression, Multiple Linear Regression, and Random Forest 
              across both test-set metrics ($R^2 = 98.69\%$) and 5-fold cross-validation ($R^2 = 97.78\%$).
            - **Data-Driven Allocation:** Identifies that spending on TV and Radio yields over 98% of predictable sales volume, 
              while Newspaper spending provides minimal marginal returns.
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
            color_continuous_scale="Blues",
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
            font=dict(family="Inter, sans-serif", color="#f1f5f9")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Bottom Row: Quick Model Verification Simulator
    st.subheader("⚡ Quick Verification Simulator")
    st.markdown("Try the notebook baseline scenario to verify instant model response:")

    q1, q2, q3, q4 = st.columns([1, 1, 1, 1.2])
    with q1:
        tv_input = st.number_input("TV Budget ($k)", value=150.0, step=10.0, min_value=0.0, max_value=500.0)
    with q2:
        radio_input = st.number_input("Radio Budget ($k)", value=25.0, step=5.0, min_value=0.0, max_value=200.0)
    with q3:
        news_input = st.number_input("Newspaper Budget ($k)", value=20.0, step=5.0, min_value=0.0, max_value=200.0)
    with q4:
        st.markdown("**Sales Forecast**")
        res = predict_single_sales(tv_input, radio_input, news_input)
        st.success(f"**{res['prediction']:.2f}k units** (~{res['prediction']*1000:,.0f} units)")

    if res["is_out_of_bounds"]:
        st.caption("⚠️ *Note: One or more input budgets exceed the historical dataset training range.*")


if __name__ == "__main__":
    show()
