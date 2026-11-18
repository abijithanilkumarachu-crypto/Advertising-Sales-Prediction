"""
Advertising Sales Prediction - Multi-Page Streamlit Web Application
Main entry point connecting all views with modern navigation.
Configured for Indian corporate & interview presentations with INR (₹) budgets.
"""

import streamlit as st
from utils.ui_components import inject_custom_css
from utils.currency import DEFAULT_USD_TO_INR
from views import (
    home_dashboard,
    sales_prediction,
    model_comparison,
    dataset_explorer,
    batch_prediction,
    about_project
)

# 1. Global Page Configuration
st.set_page_config(
    page_title="AdSales AI - Advertising Sales Prediction (INR ₹)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Enterprise Theme Styling ("Midnight Graphite & Deep Teal")
inject_custom_css()

# 3. Sidebar Branding & Currency Metadata
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #2D4248; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2rem;">📈</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #F0F5F4;">AdSales AI</h2>
                    <span style="font-size: 0.8rem; font-weight: 500; color: #AABBB9;">Sales Forecasting & Optimization</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Active Pipeline Badge
    st.markdown(
        """
        <div style="background-color: #19282D; border: 1px solid #2D4248; border-left: 3px solid #65C6AE; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #65C6AE; letter-spacing: 0.06em;">Active ML Pipeline</div>
            <div style="font-size: 0.96rem; font-weight: 700; color: #F0F5F4; margin-top: 3px;">Polynomial Reg. (Deg 2)</div>
            <div style="font-size: 0.82rem; color: #65C6AE; font-weight: 600; margin-top: 3px;">● Holdout Accuracy (R²): 98.69%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Currency Adaptation Pill
    st.markdown(
        f"""
        <div style="background-color: #19282D; border: 1px solid #2D4248; border-left: 3px solid #D1A66B; border-radius: 8px; padding: 10px 12px; margin-bottom: 18px;">
            <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: #D1A66B; letter-spacing: 0.06em;">Currency Adaptation</div>
            <div style="font-size: 0.9rem; font-weight: 700; color: #F0F5F4; margin-top: 2px;">Indian Rupees (₹ / INR)</div>
            <div style="font-size: 0.78rem; color: #AABBB9; margin-top: 2px;">Conversion: 1 USD ≈ ₹{DEFAULT_USD_TO_INR:,.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Multi-Page Navigation Configuration with explicit unique URL paths
pages = [
    st.Page(home_dashboard.show, title="Home Dashboard", icon="🏠", url_path="home", default=True),
    st.Page(sales_prediction.show, title="Sales Prediction (₹)", icon="🎯", url_path="prediction"),
    st.Page(model_comparison.show, title="Model Comparison", icon="📊", url_path="model-comparison"),
    st.Page(dataset_explorer.show, title="Dataset Explorer", icon="🔍", url_path="dataset-explorer"),
    st.Page(batch_prediction.show, title="Batch Prediction (₹)", icon="📁", url_path="batch-prediction"),
    st.Page(about_project.show, title="About Project", icon="ℹ️", url_path="about"),
]

nav = st.navigation(pages)

# 5. Sidebar Footer
with st.sidebar:
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.74rem; color: #AABBB9; text-align: center; line-height: 1.45;">
            Advertising Sales Prediction v2.0 (INR)<br>
            Powered by Scikit-Learn & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

# 6. Run the active page
nav.run()
