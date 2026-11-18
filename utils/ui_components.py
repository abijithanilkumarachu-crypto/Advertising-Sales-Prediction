"""
UI styling and reusable components for the Advertising Sales Prediction Application.
Theme: 'Midnight Graphite & Deep Teal' — A refined, understated enterprise analytics aesthetic.
"""

import streamlit as st
from utils.currency import TRANSPARENCY_NOTE, DEFAULT_USD_TO_INR


def inject_custom_css():
    """
    Injects custom CSS styling for the 'Midnight Graphite & Deep Teal' enterprise theme.
    Colour Palette:
      - Main Background: #101A20 (Deep Graphite)
      - Card / Panel Background: #19282D
      - Secondary Surfaces: #22343A
      - Primary Accent: #174E4A (Deep Teal)
      - Highlight Accent: #65C6AE (Mint Teal)
      - Secondary Accent: #D1A66B (Warm Bronze)
      - Main Text: #F0F5F4 (Crisp Off-White)
      - Secondary Text: #AABBB9 (Muted Sage-Slate)
      - Borders: #2D4248 (Subtle Muted Slate-Teal)
    """
    st.markdown(
        """
        <style>
        /* Global Typography & Font Family */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #F0F5F4;
        }

        /* App Background */
        .stApp {
            background-color: #101A20;
            color: #F0F5F4;
        }

        /* Main Headings */
        h1, h2, h3, h4, h5, h6, [data-testid="stHeading"] {
            color: #F0F5F4 !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em;
        }

        /* Section Subheadings */
        h2, h3 {
            color: #F0F5F4 !important;
        }
        
        h4, h5 {
            color: #AABBB9 !important;
        }

        /* Responsive Page Header Banner Container */
        .page-header-container {
            background-color: #19282D;
            border: 1px solid #2D4248;
            border-left: 4px solid #65C6AE;
            border-radius: 10px;
            padding: 18px 24px;
            margin-bottom: 22px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
        }
        .page-header-title {
            margin: 0;
            font-size: clamp(1.4rem, 4vw, 2.0rem);
            font-weight: 800;
            color: #F0F5F4 !important;
            line-height: 1.25;
        }
        .page-header-subtitle {
            margin: 6px 0 0 0;
            font-size: clamp(0.86rem, 2vw, 0.98rem);
            color: #AABBB9 !important;
            font-weight: 400;
        }

        /* Refined Metric Cards */
        .metric-card {
            background-color: #19282D;
            border: 1px solid #2D4248;
            border-radius: 10px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.18);
            margin-bottom: 12px;
            transition: border-color 0.15s ease-in-out;
        }
        .metric-card:hover {
            border-color: #3B575F;
        }
        .metric-label {
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #AABBB9;
            margin-bottom: 4px;
        }
        .metric-value {
            font-size: clamp(1.35rem, 3vw, 1.8rem);
            font-weight: 700;
            color: #F0F5F4;
            line-height: 1.2;
        }
        .metric-subtext {
            font-size: 0.8rem;
            color: #AABBB9;
            margin-top: 4px;
        }
        .metric-badge-good {
            color: #65C6AE !important;
            font-weight: 600;
        }

        /* Prediction Hero Box */
        .prediction-hero {
            background-color: #19282D;
            border: 1px solid #2D4248;
            border-top: 3px solid #65C6AE;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.22);
            margin-top: 8px;
            margin-bottom: 18px;
        }
        .prediction-hero-title {
            font-size: 0.86rem;
            font-weight: 700;
            color: #65C6AE;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .prediction-hero-value {
            font-size: clamp(2.3rem, 6vw, 3.1rem);
            font-weight: 800;
            color: #F0F5F4;
            margin-bottom: 2px;
            line-height: 1.1;
        }
        .prediction-hero-unit {
            font-size: clamp(0.95rem, 2.5vw, 1.1rem);
            font-weight: 600;
            color: #AABBB9;
        }
        .prediction-hero-subtext {
            font-size: 0.84rem;
            color: #AABBB9;
            margin-top: 8px;
            line-height: 1.45;
        }

        /* Information Cards */
        .info-card {
            background-color: #19282D;
            border: 1px solid #2D4248;
            border-left: 4px solid #174E4A;
            border-radius: 8px;
            padding: 16px 18px;
            margin-bottom: 14px;
            font-size: 0.92rem;
            color: #F0F5F4;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
        }

        /* Understated Badges */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            font-size: 0.74rem;
            font-weight: 600;
            border-radius: 6px;
            background-color: #22343A;
            color: #65C6AE;
            border: 1px solid #2D4248;
            margin-left: 8px;
            vertical-align: middle;
            letter-spacing: 0.03em;
        }

        /* Transparency Note Box (Warm Bronze Accent) */
        .transparency-box {
            background-color: #19282D;
            border: 1px solid #2D4248;
            border-left: 4px solid #D1A66B;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 14px;
            margin-bottom: 16px;
            font-size: 0.85rem;
            color: #AABBB9;
            line-height: 1.5;
        }
        .transparency-header {
            font-weight: 700;
            color: #D1A66B;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }

        /* Subtle Warning Box */
        .bounds-warning-box {
            background-color: #1C2223;
            border: 1px solid #3B382F;
            border-left: 4px solid #D1A66B;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 10px;
            margin-bottom: 14px;
            color: #E6D2B5;
            font-size: 0.86rem;
        }

        /* Streamlit Primary & Secondary Buttons */
        .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
            background-color: #174E4A !important;
            color: #F0F5F4 !important;
            border: 1px solid #65C6AE !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.15s ease-in-out !important;
        }
        .stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
            background-color: #65C6AE !important;
            color: #101A20 !important;
            border-color: #65C6AE !important;
        }
        .stButton > button[kind="secondary"], .stDownloadButton > button[kind="secondary"] {
            background-color: #19282D !important;
            color: #F0F5F4 !important;
            border: 1px solid #2D4248 !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            transition: all 0.15s ease-in-out !important;
        }
        .stButton > button[kind="secondary"]:hover, .stDownloadButton > button[kind="secondary"]:hover {
            border-color: #65C6AE !important;
            color: #65C6AE !important;
        }

        /* Inputs, Selectboxes, Dropdowns */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
            background-color: #19282D !important;
            border-color: #2D4248 !important;
            color: #F0F5F4 !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"] svg {
            fill: #AABBB9 !important;
        }

        /* Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #101A20 !important;
            border-bottom: 1px solid #2D4248 !important;
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #AABBB9 !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
        }
        .stTabs [aria-selected="true"] {
            color: #65C6AE !important;
            border-bottom-color: #65C6AE !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #19282D !important;
            border-right: 1px solid #2D4248 !important;
        }

        /* Native Metric Widgets */
        [data-testid="stMetricValue"] {
            color: #F0F5F4 !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #AABBB9 !important;
            font-weight: 500 !important;
        }

        /* Code Blocks */
        code {
            background-color: #22343A !important;
            color: #65C6AE !important;
            border: 1px solid #2D4248;
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.88em;
        }

        /* Horizontal Divider */
        hr {
            border: 0;
            border-top: 1px solid #2D4248 !important;
            margin: 20px 0;
        }

        /* Dataframe Container */
        [data-testid="stDataFrame"] {
            border: 1px solid #2D4248 !important;
            border-radius: 8px !important;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_page_header(title: str, subtitle: str, badge: str = None):
    """Renders a responsive, understated page header banner in Midnight Graphite & Deep Teal."""
    badge_html = f'<span class="badge">{badge}</span>' if badge else ""
    st.markdown(
        f"""
        <div class="page-header-container">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <h1 class="page-header-title">{title}</h1>
                {badge_html}
            </div>
            <p class="page-header-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(label: str, value: str, subtext: str = "", badge_good: bool = True):
    """Renders a structured KPI card with refined border depth."""
    sub_class = "metric-badge-good" if badge_good else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext {sub_class}">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_transparency_note(exchange_rate: float = DEFAULT_USD_TO_INR):
    """
    Renders the professional transparency and currency conversion note.
    Uses the warm bronze secondary accent for understated prominence.
    """
    st.markdown(
        f"""
        <div class="transparency-box">
            <div class="transparency-header">🌐 Currency & Market Calibration Note (Exchange Rate: 1 USD ≈ ₹{exchange_rate:,.1f})</div>
            {TRANSPARENCY_NOTE}
        </div>
        """,
        unsafe_allow_html=True
    )
