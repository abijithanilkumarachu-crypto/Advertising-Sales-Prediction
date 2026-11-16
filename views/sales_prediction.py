"""
Sales Prediction View: Interactive Marketing Budget Simulator.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.ui_components import render_page_header
from utils.model_loader import predict_single_sales, HISTORICAL_BOUNDS


def show():
    render_page_header(
        title="Interactive Sales Prediction",
        subtitle="Estimate product sales volume based on advertising budget allocations across channels.",
        badge="Inference Engine Active"
    )

    # Preset Scenarios (Responsive Selectbox)
    st.markdown("##### 💡 Quick Budget Scenarios")
    scenario = st.selectbox(
        "Choose a preset scenario or customize manually:",
        [
            "Custom Allocation",
            "Notebook Benchmark Sample ($150k TV, $25k Radio, $20k Newspaper)",
            "Dataset Average Allocation ($147k TV, $23k Radio, $31k Newspaper)",
            "TV-Heavy Allocation ($220k TV, $15k Radio, $10k Newspaper)",
            "High Radio Synergy Mix ($140k TV, $45k Radio, $5k Newspaper)"
        ],
        help="Select a scenario to populate default budget amounts or adjust sliders below."
    )

    # Set default values based on selected scenario
    if scenario.startswith("Notebook"):
        default_tv, default_radio, default_news = 150.0, 25.0, 20.0
    elif scenario.startswith("Dataset Average"):
        default_tv, default_radio, default_news = 147.0, 23.0, 30.5
    elif scenario.startswith("TV-Heavy"):
        default_tv, default_radio, default_news = 220.0, 15.0, 10.0
    elif scenario.startswith("High Radio"):
        default_tv, default_radio, default_news = 140.0, 45.0, 5.0
    else:
        default_tv, default_radio, default_news = 150.0, 25.0, 20.0

    st.markdown("<br>", unsafe_allow_html=True)

    col_input, col_output = st.columns([1.1, 0.9], gap="large")

    with col_input:
        st.subheader("⚙️ Channel Budget Controls")
        st.caption("All advertising budget values are expressed in thousands of dollars ($k).")

        # TV Input
        st.markdown("**📺 Television Advertising Budget**")
        tv_budget = st.slider(
            "TV Budget Slider",
            min_value=0.0,
            max_value=350.0,
            value=float(default_tv),
            step=1.0,
            key="slider_tv",
            help="Historical range in training data: $0.7k to $296.4k",
            label_visibility="collapsed"
        )
        c_tv1, c_tv2 = st.columns([3, 1])
        with c_tv1:
            st.caption(f"Historical Range: ${HISTORICAL_BOUNDS['TV']['min']}k – ${HISTORICAL_BOUNDS['TV']['max']}k (Median: $149.8k)")
        with c_tv2:
            st.markdown(f"**${tv_budget:,.1f}k**")

        st.markdown("<br>", unsafe_allow_html=True)

        # Radio Input
        st.markdown("**📻 Radio Advertising Budget**")
        radio_budget = st.slider(
            "Radio Budget Slider",
            min_value=0.0,
            max_value=60.0,
            value=float(default_radio),
            step=0.5,
            key="slider_radio",
            help="Historical range in training data: $0.0k to $49.6k",
            label_visibility="collapsed"
        )
        c_r1, c_r2 = st.columns([3, 1])
        with c_r1:
            st.caption(f"Historical Range: ${HISTORICAL_BOUNDS['radio']['min']}k – ${HISTORICAL_BOUNDS['radio']['max']}k (Median: $22.9k)")
        with c_r2:
            st.markdown(f"**${radio_budget:,.1f}k**")

        st.markdown("<br>", unsafe_allow_html=True)

        # Newspaper Input
        st.markdown("**📰 Newspaper Advertising Budget**")
        news_budget = st.slider(
            "Newspaper Budget Slider",
            min_value=0.0,
            max_value=120.0,
            value=float(default_news),
            step=0.5,
            key="slider_news",
            help="Historical range in training data: $0.3k to $114.0k",
            label_visibility="collapsed"
        )
        c_n1, c_n2 = st.columns([3, 1])
        with c_n1:
            st.caption(f"Historical Range: ${HISTORICAL_BOUNDS['newspaper']['min']}k – ${HISTORICAL_BOUNDS['newspaper']['max']}k (Median: $25.8k)")
        with c_n2:
            st.markdown(f"**${news_budget:,.1f}k**")

        total_budget = tv_budget + radio_budget + news_budget
        st.markdown("---")
        st.markdown(
            f"""
            <div style="background-color: #1e293b; border: 1px solid #334155; padding: 14px 18px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #cbd5e1;">Total Marketing Budget:</span>
                <span style="font-size: 1.3rem; font-weight: 700; color: #38bdf8;">${total_budget:,.1f}k (${total_budget * 1000:,.0f})</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Perform prediction
    res = predict_single_sales(tv_budget, radio_budget, news_budget)
    pred_sales = res["prediction"]

    with col_output:
        st.subheader("🎯 Sales Forecast")

        # Out-of-bounds warning
        if res["is_out_of_bounds"]:
            for w in res["bounds_warnings"]:
                st.warning(f"⚠️ **Range Advisory:** {w} Predictions at extreme values may reflect polynomial extrapolation divergence.")

        # Hero Card
        st.markdown(
            f"""
            <div class="prediction-hero">
                <div class="prediction-hero-title">Predicted Product Sales</div>
                <div class="prediction-hero-value">{pred_sales:.2f} <span class="prediction-hero-unit">k units</span></div>
                <div style="font-size: 1.15rem; font-weight: 600; color: #34d399; margin-top: 4px;">
                    ≈ {pred_sales * 1000:,.0f} Total Units
                </div>
                <div class="prediction-hero-subtext">
                    Model Accuracy Context: <strong>Test RMSE: ±0.64k units</strong> | <strong>R² Score: 98.69%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Budget Allocation Donut Chart
        if total_budget > 0:
            budget_df = pd.DataFrame([
                {"Channel": "TV", "Budget": tv_budget, "Color": "#38bdf8"},
                {"Channel": "Radio", "Budget": radio_budget, "Color": "#2dd4bf"},
                {"Channel": "Newspaper", "Budget": news_budget, "Color": "#f59e0b"}
            ])
            fig_donut = px.pie(
                budget_df,
                values="Budget",
                names="Channel",
                hole=0.6,
                color="Channel",
                color_discrete_map={"TV": "#38bdf8", "Radio": "#2dd4bf", "Newspaper": "#f59e0b"},
                height=240
            )
            fig_donut.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
            )
            st.plotly_chart(fig_donut, use_container_width=True)

    # Channel Sensitivity / What-If Analysis
    st.markdown("---")
    st.subheader("📈 Marginal ROI Analysis: +$10k Channel Boost Simulation")
    st.caption("How much additional sales volume would you generate by injecting +$10,000 into each specific channel?")

    boost_tv = predict_single_sales(tv_budget + 10.0, radio_budget, news_budget)["prediction"] - pred_sales
    boost_radio = predict_single_sales(tv_budget, radio_budget + 10.0, news_budget)["prediction"] - pred_sales
    boost_news = predict_single_sales(tv_budget, radio_budget, news_budget + 10.0)["prediction"] - pred_sales

    sens_col1, sens_col2, sens_col3 = st.columns(3)
    with sens_col1:
        st.metric(
            label="+$10k into TV Budget",
            value=f"+{boost_tv:.3f}k units",
            delta=f"+{boost_tv * 1000:,.0f} units",
            delta_color="normal"
        )
    with sens_col2:
        st.metric(
            label="+$10k into Radio Budget",
            value=f"+{boost_radio:.3f}k units",
            delta=f"+{boost_radio * 1000:,.0f} units",
            delta_color="normal"
        )
    with sens_col3:
        st.metric(
            label="+$10k into Newspaper Budget",
            value=f"+{boost_news:.3f}k units",
            delta=f"+{boost_news * 1000:,.0f} units",
            delta_color="normal"
        )


if __name__ == "__main__":
    show()
