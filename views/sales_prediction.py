"""
Sales Prediction View: Interactive Marketing Budget Simulator.
Configured with Indian Rupee (INR / ₹) inputs and dynamic conversion.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui_components import render_page_header, render_transparency_note
from utils.model_loader import predict_single_sales, HISTORICAL_BOUNDS
from utils.currency import (
    DEFAULT_USD_TO_INR,
    format_inr_short,
    format_inr_currency,
    format_inr_readable,
    model_units_to_inr
)


def show():
    render_page_header(
        title="Interactive Sales Prediction",
        subtitle="Estimate product sales volume based on promotional budgets in Indian Rupees (₹).",
        badge="INR (₹) Mode Active"
    )

    # Preset Scenarios in INR (Responsive Selectbox)
    st.markdown("##### 💡 Quick Budget Scenarios (INR ₹)")
    scenario = st.selectbox(
        "Choose a preset scenario or customize manually:",
        [
            "Custom Allocation",
            "Notebook Benchmark Sample (₹1.35 Cr TV, ₹22.50 Lakh Radio, ₹18.00 Lakh Newspaper)",
            "Dataset Average Allocation (₹1.32 Cr TV, ₹20.70 Lakh Radio, ₹27.45 Lakh Newspaper)",
            "TV-Heavy Allocation (₹1.98 Cr TV, ₹13.50 Lakh Radio, ₹9.00 Lakh Newspaper)",
            "High Radio Synergy Mix (₹1.26 Cr TV, ₹40.50 Lakh Radio, ₹4.50 Lakh Newspaper)"
        ],
        help="Select a scenario to populate budget amounts or adjust sliders below."
    )

    # Set default values in INR based on selected scenario
    # Benchmark amounts: TV=150, radio=25, news=20 -> at ₹90/USD: 13.5M, 2.25M, 1.8M
    if scenario.startswith("Notebook"):
        default_tv, default_radio, default_news = 13_500_000, 2_250_000, 1_800_000
    elif scenario.startswith("Dataset Average"):
        default_tv, default_radio, default_news = 13_230_000, 2_070_000, 2_745_000
    elif scenario.startswith("TV-Heavy"):
        default_tv, default_radio, default_news = 19_800_000, 1_350_000, 900_000
    elif scenario.startswith("High Radio"):
        default_tv, default_radio, default_news = 12_600_000, 4_050_000, 450_000
    else:
        default_tv, default_radio, default_news = 13_500_000, 2_250_000, 1_800_000

    st.markdown("<br>", unsafe_allow_html=True)

    col_input, col_output = st.columns([1.1, 0.9], gap="large")

    # Compute INR historical boundary limits
    tv_max_inr = model_units_to_inr(HISTORICAL_BOUNDS["TV"]["max"])
    radio_max_inr = model_units_to_inr(HISTORICAL_BOUNDS["radio"]["max"])
    news_max_inr = model_units_to_inr(HISTORICAL_BOUNDS["newspaper"]["max"])

    with col_input:
        st.subheader("⚙️ Channel Budget Controls (₹)")
        st.caption(f"Inputs in Indian Rupees (₹). Converted at 1 USD ≈ ₹{DEFAULT_USD_TO_INR:,.1f} for model inference.")

        # TV Input
        st.markdown("**📺 Television Advertising Budget**")
        tv_budget = st.slider(
            "TV Budget Slider",
            min_value=0,
            max_value=30_000_000,
            value=int(default_tv),
            step=100_000,
            key="slider_tv",
            help=f"Historical max: {format_inr_short(tv_max_inr)} (${HISTORICAL_BOUNDS['TV']['max']}k USD)",
            label_visibility="collapsed"
        )
        c_tv1, c_tv2 = st.columns([3, 2])
        with c_tv1:
            st.caption(f"Historical Max: {format_inr_short(tv_max_inr)} (${HISTORICAL_BOUNDS['TV']['max']}k USD)")
        with c_tv2:
            st.markdown(f"**{format_inr_readable(tv_budget)}**")

        st.markdown("<br>", unsafe_allow_html=True)

        # Radio Input
        st.markdown("**📻 Radio Advertising Budget**")
        radio_budget = st.slider(
            "Radio Budget Slider",
            min_value=0,
            max_value=6_000_000,
            value=int(default_radio),
            step=50_000,
            key="slider_radio",
            help=f"Historical max: {format_inr_short(radio_max_inr)} (${HISTORICAL_BOUNDS['radio']['max']}k USD)",
            label_visibility="collapsed"
        )
        c_r1, c_r2 = st.columns([3, 2])
        with c_r1:
            st.caption(f"Historical Max: {format_inr_short(radio_max_inr)} (${HISTORICAL_BOUNDS['radio']['max']}k USD)")
        with c_r2:
            st.markdown(f"**{format_inr_readable(radio_budget)}**")

        st.markdown("<br>", unsafe_allow_html=True)

        # Newspaper Input
        st.markdown("**📰 Newspaper Advertising Budget**")
        news_budget = st.slider(
            "Newspaper Budget Slider",
            min_value=0,
            max_value=12_000_000,
            value=int(default_news),
            step=50_000,
            key="slider_news",
            help=f"Historical max: {format_inr_short(news_max_inr)} (${HISTORICAL_BOUNDS['newspaper']['max']}k USD)",
            label_visibility="collapsed"
        )
        c_n1, c_n2 = st.columns([3, 2])
        with c_n1:
            st.caption(f"Historical Max: {format_inr_short(news_max_inr)} (${HISTORICAL_BOUNDS['newspaper']['max']}k USD)")
        with c_n2:
            st.markdown(f"**{format_inr_readable(news_budget)}**")

        total_budget = tv_budget + radio_budget + news_budget
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background-color: #19282D; border: 1px solid #2D4248; padding: 14px 18px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #AABBB9;">Total Marketing Budget:</span>
                <span style="font-size: 1.25rem; font-weight: 800; color: #F0F5F4;">{format_inr_readable(total_budget)}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Perform prediction with INR conversion
    res = predict_single_sales(tv_budget, radio_budget, news_budget, exchange_rate=DEFAULT_USD_TO_INR)
    pred_sales = res["prediction"]

    with col_output:
        st.subheader("🎯 Sales Forecast")

        # Out-of-bounds warning
        if res["is_out_of_bounds"]:
            for w in res["bounds_warnings"]:
                st.warning(f"⚠️ **Range Advisory:** {w}")

        # Hero Card
        st.markdown(
            f"""
            <div class="prediction-hero">
                <div class="prediction-hero-title">Predicted Product Sales</div>
                <div class="prediction-hero-value">{pred_sales:.2f} <span class="prediction-hero-unit">k units</span></div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #65C6AE; margin-top: 4px;">
                    ≈ {pred_sales * 1000:,.0f} Total Units
                </div>
                <div class="prediction-hero-subtext">
                    Model Accuracy Context: <strong style="color: #F0F5F4;">Test RMSE: ±0.64k units</strong> | <strong style="color: #F0F5F4;">R² Score: 98.69%</strong><br>
                    <span style="font-size: 0.78rem; color: #AABBB9;">
                        Converted Model Scale: TV={res['converted_model_units']['TV']:.1f}, 
                        Radio={res['converted_model_units']['radio']:.1f}, 
                        Newspaper={res['converted_model_units']['newspaper']:.1f}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Budget Allocation Donut Chart (Midnight Graphite & Deep Teal Theme)
        if total_budget > 0:
            budget_df = pd.DataFrame([
                {"Channel": "TV", "Budget": tv_budget, "Display": format_inr_short(tv_budget)},
                {"Channel": "Radio", "Budget": radio_budget, "Display": format_inr_short(radio_budget)},
                {"Channel": "Newspaper", "Budget": news_budget, "Display": format_inr_short(news_budget)}
            ])
            fig_donut = px.pie(
                budget_df,
                values="Budget",
                names="Channel",
                hole=0.6,
                color="Channel",
                color_discrete_map={"TV": "#65C6AE", "Radio": "#174E4A", "Newspaper": "#D1A66B"},
                height=230
            )
            fig_donut.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # Channel Sensitivity / What-If Analysis in INR (+₹10 Lakh injection)
    st.markdown("---")
    st.subheader("📈 Marginal ROI Analysis: +₹10 Lakh Channel Boost Simulation")
    st.caption("How much additional sales volume would you generate by injecting +₹10,00,000 (+₹10 Lakh) into each specific channel?")

    boost_amount = 1_000_000  # ₹10 Lakh
    boost_tv = predict_single_sales(tv_budget + boost_amount, radio_budget, news_budget)["prediction"] - pred_sales
    boost_radio = predict_single_sales(tv_budget, radio_budget + boost_amount, news_budget)["prediction"] - pred_sales
    boost_news = predict_single_sales(tv_budget, radio_budget, news_budget + boost_amount)["prediction"] - pred_sales

    sens_col1, sens_col2, sens_col3 = st.columns(3)
    with sens_col1:
        st.metric(
            label="+₹10 Lakh into TV Budget",
            value=f"+{boost_tv:.3f}k units",
            delta=f"+{boost_tv * 1000:,.0f} units",
            delta_color="normal"
        )
    with sens_col2:
        st.metric(
            label="+₹10 Lakh into Radio Budget",
            value=f"+{boost_radio:.3f}k units",
            delta=f"+{boost_radio * 1000:,.0f} units",
            delta_color="normal"
        )
    with sens_col3:
        st.metric(
            label="+₹10 Lakh into Newspaper Budget",
            value=f"+{boost_news:.3f}k units",
            delta=f"+{boost_news * 1000:,.0f} units",
            delta_color="normal"
        )

    # Transparency & Market Calibration Note
    render_transparency_note(DEFAULT_USD_TO_INR)


if __name__ == "__main__":
    show()
