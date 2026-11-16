"""
Advertising Sales Prediction - Multi-Page Streamlit Web Application
Main entry point connecting all views with modern navigation.
"""

import streamlit as st
from utils.ui_components import inject_custom_css
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
    page_title="AdSales AI - Advertising Sales Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Modern Light Theme Styling
inject_custom_css()

# 3. Sidebar Branding & Metadata
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #334155; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 2rem;">📈</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #f8fafc;">AdSales AI</h2>
                    <span style="font-size: 0.8rem; font-weight: 500; color: #94a3b8;">Sales Forecasting & Budget Optimization</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 12px 14px; margin-bottom: 20px;">
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #38bdf8; letter-spacing: 0.05em;">Active ML Pipeline</div>
            <div style="font-size: 0.98rem; font-weight: 700; color: #f8fafc; margin-top: 3px;">Polynomial Reg. (Deg 2)</div>
            <div style="font-size: 0.82rem; color: #34d399; font-weight: 600; margin-top: 4px;">● Accuracy (R²): 98.69%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Multi-Page Navigation Configuration with explicit unique URL paths
pages = [
    st.Page(home_dashboard.show, title="Home Dashboard", icon="🏠", url_path="home", default=True),
    st.Page(sales_prediction.show, title="Sales Prediction", icon="🎯", url_path="prediction"),
    st.Page(model_comparison.show, title="Model Comparison", icon="📊", url_path="model-comparison"),
    st.Page(dataset_explorer.show, title="Dataset Explorer", icon="🔍", url_path="dataset-explorer"),
    st.Page(batch_prediction.show, title="Batch Prediction", icon="📁", url_path="batch-prediction"),
    st.Page(about_project.show, title="About Project", icon="ℹ️", url_path="about"),
]

nav = st.navigation(pages)

# 5. Sidebar Footer
with st.sidebar:
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #94a3b8; text-align: center; line-height: 1.4;">
            Advertising Sales Prediction v1.0<br>
            Powered by Scikit-Learn & Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

# 6. Run the active page
nav.run()
