"""
Model Comparison View: Comprehensive Benchmark of All Four Algorithms.
Professional presentation comparing regression algorithms with light theme charts.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.ui_components import render_page_header, render_transparency_note
from utils.data_loader import get_benchmark_df
from utils.currency import DEFAULT_USD_TO_INR


def show():
    render_page_header(
        title="Model Performance Comparison",
        subtitle="Detailed empirical evaluation of all four regression algorithms tested during model development.",
        badge="Official Notebook Results"
    )

    df_benchmarks = get_benchmark_df()

    # Highlight winner in the table
    st.subheader("📋 Regression Algorithms Evaluation Matrix")
    st.markdown(
        "All candidate models were evaluated under an identical 80/20 train-test split (`random_state=42`) "
        "and validated using 5-Fold Cross-Validation on the underlying training dataset."
    )

    display_df = df_benchmarks.copy()
    display_df["Test R²"] = display_df["R2 Score"].apply(lambda x: f"{x:.4f} ({x*100:.2f}%)")
    display_df["5-Fold CV R²"] = display_df.apply(lambda r: f"{r['Mean CV R2']:.4f} ± {r['CV Std Dev']:.4f}", axis=1)
    display_df["MAE"] = display_df["MAE"].apply(lambda x: f"{x:.4f}")
    display_df["MSE"] = display_df["MSE"].apply(lambda x: f"{x:.4f}")
    display_df["RMSE"] = display_df["RMSE"].apply(lambda x: f"{x:.4f}")

    columns_to_show = ["Algorithm", "Features Used", "MAE", "MSE", "RMSE", "Test R²", "5-Fold CV R²"]
    st.dataframe(display_df[columns_to_show], use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Charts in Light Theme
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📉 Prediction Error Comparison (Lower is Better)")
        error_df = pd.melt(
            df_benchmarks,
            id_vars=["Algorithm"],
            value_vars=["MAE", "RMSE"],
            var_name="Metric",
            value_name="Error Value"
        )
        fig_err = px.bar(
            error_df,
            x="Algorithm",
            y="Error Value",
            color="Metric",
            barmode="group",
            text=error_df["Error Value"].apply(lambda x: f"{x:.2f}"),
            color_discrete_map={"MAE": "#65C6AE", "RMSE": "#D1A66B"},
            height=360
        )
        fig_err.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title="",
            yaxis_title="Error (Units)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family="Inter, sans-serif", color="#AABBB9")
        )
        fig_err.update_xaxes(tickangle=-15)
        fig_err.update_yaxes(showgrid=True, gridcolor="#22343A")
        st.plotly_chart(fig_err, use_container_width=True)

    with col_chart2:
        st.subheader("🎯 Goodness of Fit (R² Score - Higher is Better)")
        fig_r2 = go.Figure()

        # Test R2
        fig_r2.add_trace(go.Bar(
            name="Test Set R²",
            x=df_benchmarks["Algorithm"],
            y=df_benchmarks["R2 Score"],
            text=df_benchmarks["R2 Score"].apply(lambda x: f"{x:.3f}"),
            textposition="auto",
            marker_color="#65C6AE"
        ))

        # 5-Fold CV Mean R2 with error bars
        fig_r2.add_trace(go.Bar(
            name="5-Fold CV Mean R²",
            x=df_benchmarks["Algorithm"],
            y=df_benchmarks["Mean CV R2"],
            error_y=dict(type="data", array=df_benchmarks["CV Std Dev"], visible=True, color="#AABBB9"),
            text=df_benchmarks["Mean CV R2"].apply(lambda x: f"{x:.3f}"),
            textposition="auto",
            marker=dict(color="#174E4A", line=dict(color="#65C6AE", width=1))
        ))

        fig_r2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            barmode="group",
            yaxis_title="R² Score",
            yaxis=dict(range=[0, 1.05], showgrid=True, gridcolor="#22343A"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=360,
            font=dict(family="Inter, sans-serif", color="#AABBB9")
        )
        fig_r2.update_xaxes(tickangle=-15)
        st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("---")

    # In-Depth Theoretical Justification
    st.subheader("🧠 Why Polynomial Regression was Selected")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.markdown(
            """
            <div class="info-card">
                <h4 style="margin-top:0; color: #65C6AE;">1. Cross-Channel Interaction & Synergies</h4>
                <p>Standard <strong>Multiple Linear Regression</strong> assumes an additive relationship where each channel operates in a vacuum:</p>
                <code>Sales = β₀ + β₁(TV) + β₂(Radio) + β₃(Newspaper)</code>
                <p>In real-world marketing, advertising channels cross-reinforce each other. A consumer who encounters a TV commercial 
                and subsequently hears a Radio ad experiences amplified brand recall. <strong>Polynomial Regression (Degree 2)</strong> explicitly models this with cross-product terms:</p>
                <code>+ β₄(TV²) + β₅(TV × Radio) + β₆(TV × Newspaper) ...</code>
                <p>The cross-term <strong>(TV × Radio)</strong> has a positive coefficient, driving an $R^2$ leap from 89.94% to <strong>98.69%</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_exp2:
        st.markdown(
            """
            <div class="info-card" style="border-left-color: #D1A66B;">
                <h4 style="margin-top:0; color: #D1A66B;">2. Stability over Ensemble Tree Models</h4>
                <p>While <strong>Random Forest Regressor</strong> also captured non-linear relationships ($R^2 = 98.13\%$), 
                decision trees partition continuous feature space with orthogonal step functions:</p>
                <ul>
                    <li>Cannot extrapolate smooth diminishing returns as naturally on compact datasets (200 records).</li>
                    <li>Exhibits higher variance and standard deviation across data folds.</li>
                </ul>
                <p>Polynomial Regression achieved both <strong>higher 5-fold cross-validation consistency (97.78% vs 96.63%)</strong> and 
                <strong>lower prediction error (MAE: 0.526 vs 0.620)</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Transparency Note
    render_transparency_note(DEFAULT_USD_TO_INR)


if __name__ == "__main__":
    show()
