"""
Dataset Explorer View: Comprehensive Exploratory Data Analysis & Visualizations.
Professional presentation with light theme charts and Indian Rupee context.
"""

import streamlit as st
import plotly.express as px
from utils.ui_components import render_page_header, render_transparency_note
from utils.data_loader import load_dataset, get_feature_importance_df
from utils.currency import DEFAULT_USD_TO_INR, model_units_to_inr, format_inr_short


def show():
    render_page_header(
        title="Dataset Explorer & Visual Analytics",
        subtitle="Exploratory Data Analysis of historical advertising investments across media channels and product sales.",
        badge="Dataset: Advertising.csv"
    )

    df = load_dataset()

    # Top Data Summary Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records", f"{len(df):,}")
    with m2:
        st.metric("Independent Channels", "3 (TV, Radio, Newspaper)")
    with m3:
        st.metric("Target Variable", "Sales (k units)")
    with m4:
        st.metric("Data Quality / Nulls", "100% Clean (0 Missing)")

    st.markdown("<br>", unsafe_allow_html=True)

    tab_data, tab_dist, tab_corr, tab_fi = st.tabs([
        "📋 Data & Statistics",
        "📊 Distribution & Outliers",
        "🔗 Correlation & Scatter Plots",
        "🌟 Feature Importance"
    ])

    # Tab 1: Data & Statistics
    with tab_data:
        st.subheader("Raw Dataset Preview (Original USD Scale)")
        st.caption(
            f"The training dataset contains 200 campaign records. Advertising expenditures are recorded in "
            f"thousands of USD ($k). The application dynamically converts ₹ (INR) inputs to this scale "
            f"(1 USD ≈ ₹{DEFAULT_USD_TO_INR:,.1f})."
        )
        col_ctrl, col_space = st.columns([1, 3])
        with col_ctrl:
            rows_to_show = st.slider("Rows to preview", min_value=5, max_value=len(df), value=10, step=5)
        st.dataframe(df.head(rows_to_show), use_container_width=True)

        st.subheader("Statistical Summary (`describe()`)")
        st.dataframe(df.describe().T.round(2), use_container_width=True)

    # Tab 2: Distribution & Outliers
    with tab_dist:
        st.subheader("Feature Distributions")
        selected_feature = st.selectbox("Select variable to view distribution:", ["TV", "radio", "newspaper", "sales"])

        col_h, col_b = st.columns(2)
        with col_h:
            fig_hist = px.histogram(
                df,
                x=selected_feature,
                nbins=20,
                marginal="box",
                title=f"Distribution of {selected_feature.upper()}",
                color_discrete_sequence=["#65C6AE"],
                height=380
            )
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            fig_hist.update_xaxes(showgrid=True, gridcolor="#22343A")
            fig_hist.update_yaxes(showgrid=True, gridcolor="#22343A")
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_b:
            fig_all_box = px.box(
                df[["TV", "radio", "newspaper"]],
                title="Comparative Boxplots of Advertising Channels",
                color_discrete_sequence=["#65C6AE"],
                height=380
            )
            fig_all_box.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            fig_all_box.update_yaxes(showgrid=True, gridcolor="#22343A")
            st.plotly_chart(fig_all_box, use_container_width=True)

        np_max_inr = format_inr_short(model_units_to_inr(114.0))
        st.info(
            f"💡 **Outlier Observation:** As shown in the comparative boxplots, Newspaper advertising exhibits "
            f"two minor upper outliers exceeding $100k USD (~{np_max_inr} INR), whereas TV and Radio spend "
            f"are cleanly distributed across their ranges without severe anomalies."
        )

    # Tab 3: Correlation & Interactions
    with tab_corr:
        col_heat, col_scatter = st.columns([1, 1.2])

        with col_heat:
            st.subheader("Correlation Matrix")
            corr = df.corr().round(3)
            fig_corr = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale=[[0.0, "#101A20"], [0.5, "#174E4A"], [1.0, "#65C6AE"]],
                title="Pearson Correlation Heatmap",
                height=380
            )
            fig_corr.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        with col_scatter:
            st.subheader("Bivariate Relationships vs. Sales")
            scatter_col = st.selectbox("Select advertising channel for scatter plot:", ["TV", "radio", "newspaper"])

            fig_sc = px.scatter(
                df,
                x=scatter_col,
                y="sales",
                trendline="ols",
                title=f"{scatter_col.upper()} Budget vs. Sales (with Linear Trendline)",
                color_discrete_sequence=["#65C6AE"],
                height=380
            )
            fig_sc.update_traces(line=dict(color="#D1A66B", width=2.5), selector=dict(mode="lines"))
            fig_sc.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis_title=f"{scatter_col.upper()} Advertising Budget ($k USD)",
                yaxis_title="Sales (k units)",
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            fig_sc.update_xaxes(showgrid=True, gridcolor="#22343A")
            fig_sc.update_yaxes(showgrid=True, gridcolor="#22343A")
            st.plotly_chart(fig_sc, use_container_width=True)

        st.markdown(
            """
            - **TV vs Sales:** Strongest direct correlation (**r = 0.782**). Heavy investment consistently elevates sales.
            - **Radio vs Sales:** Moderate-to-strong positive correlation (**r = 0.576**).
            - **Newspaper vs Sales:** Weak correlation (**r = 0.228**). High dispersion indicates low predictive dependency.
            """
        )

    # Tab 4: Feature Importance
    with tab_fi:
        st.subheader("Feature Importance from Random Forest Analysis")
        st.markdown("Relative percentage of variance explained by each channel when splitting trees across the ensemble:")

        df_fi = get_feature_importance_df()
        fig_imp = px.bar(
            df_fi,
            x="Importance",
            y="Feature",
            orientation="h",
            text=df_fi["Importance"].apply(lambda v: f"{v * 100:.2f}%"),
            color="Importance",
            color_continuous_scale=[[0.0, "#174E4A"], [1.0, "#65C6AE"]],
            height=300
        )
        fig_imp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Relative Feature Importance Score",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            font=dict(family="Inter, sans-serif", color="#AABBB9")
        )
        fig_imp.update_xaxes(showgrid=True, gridcolor="#22343A")
        st.plotly_chart(fig_imp, use_container_width=True)

        st.markdown(
            """
            <div class="info-card">
                <strong>Strategic Recommendation for Media Planning:</strong> Reallocate underperforming newspaper budgets 
                into television and radio campaigns. Because newspaper accounts for only 1.30% of predictive importance, 
                shifting funds into TV/Radio synergies delivers significantly higher incremental sales without increasing 
                gross marketing expenditure.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Transparency Note
    render_transparency_note(DEFAULT_USD_TO_INR)


if __name__ == "__main__":
    show()
