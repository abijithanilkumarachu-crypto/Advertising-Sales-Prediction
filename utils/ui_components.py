"""
UI styling and reusable components for the Advertising Sales Prediction Application.
Modern, sleek dark theme with high-contrast, light headings and responsive layouts.
"""

import streamlit as st


def inject_custom_css():
    """Injects custom CSS styling for a dark theme with bright, readable headings and mobile responsiveness."""
    st.markdown(
        """
        <style>
        /* Global typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #f1f5f9;
        }

        /* App Background */
        .stApp {
            background-color: #0f172a;
            color: #f1f5f9;
        }

        /* All Headings: Lighter, clear, high-contrast text */
        h1, h2, h3, h4, h5, h6, [data-testid="stHeading"] {
            color: #f8fafc !important; /* Clean light silver-white */
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }

        /* Subheadings highlight */
        h2, h3 {
            color: #38bdf8 !important; /* Vibrant light sky blue */
        }
        
        h4, h5 {
            color: #e2e8f0 !important;
        }

        /* Responsive Page Header Banner Container */
        .page-header-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-left: 5px solid #38bdf8;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        .page-header-title {
            margin: 0;
            font-size: clamp(1.4rem, 4vw, 2rem);
            font-weight: 800;
            color: #f8fafc !important;
            line-height: 1.25;
        }
        .page-header-subtitle {
            margin: 6px 0 0 0;
            font-size: clamp(0.85rem, 2vw, 1rem);
            color: #94a3b8 !important;
            font-weight: 400;
        }

        /* Metric cards */
        .metric-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            margin-bottom: 12px;
            transition: all 0.2s ease-in-out;
        }
        .metric-card:hover {
            box-shadow: 0 4px 14px rgba(56, 189, 248, 0.15);
            border-color: #38bdf8;
        }
        .metric-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            margin-bottom: 4px;
        }
        .metric-value {
            font-size: clamp(1.4rem, 3vw, 1.85rem);
            font-weight: 700;
            color: #38bdf8;
            line-height: 1.2;
        }
        .metric-subtext {
            font-size: 0.8rem;
            color: #cbd5e1;
            margin-top: 4px;
        }
        .metric-badge-good {
            color: #34d399 !important;
            font-weight: 600;
        }

        /* Prediction Hero Box */
        .prediction-hero {
            background: linear-gradient(135deg, #1e293b 0%, #0f2744 100%);
            border: 2px solid #38bdf8;
            border-radius: 16px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 4px 18px rgba(56, 189, 248, 0.15);
            margin-top: 8px;
            margin-bottom: 16px;
        }
        .prediction-hero-title {
            font-size: 0.9rem;
            font-weight: 700;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .prediction-hero-value {
            font-size: clamp(2.4rem, 6vw, 3.2rem);
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 4px;
            line-height: 1.1;
        }
        .prediction-hero-unit {
            font-size: clamp(1rem, 2.5vw, 1.15rem);
            font-weight: 600;
            color: #7dd3fc;
        }
        .prediction-hero-subtext {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-top: 8px;
            line-height: 1.4;
        }

        /* Information cards */
        .info-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-left: 4px solid #38bdf8;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 14px;
            font-size: 0.95rem;
            color: #e2e8f0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 9999px;
            background-color: #0c4a6e;
            color: #7dd3fc;
            border: 1px solid #0284c7;
            margin-left: 8px;
            vertical-align: middle;
        }

        /* Warning Banner */
        .bounds-warning-box {
            background-color: #451a03;
            border: 1px solid #d97706;
            border-left: 5px solid #f59e0b;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 10px;
            margin-bottom: 15px;
            color: #fef3c7;
            font-size: 0.88rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_page_header(title: str, subtitle: str, badge: str = None):
    """Renders a responsive, clean, high-contrast page header banner on dark background."""
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
    """Renders a structured KPI card."""
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
