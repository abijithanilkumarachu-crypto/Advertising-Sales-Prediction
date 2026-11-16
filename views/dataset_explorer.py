"""
Dataset Explorer View: Comprehensive Exploratory Data Analysis & Visualizations.
"""

import streamlit as st
import plotly.express as px
from utils.ui_components import render_page_header
from utils.data_loader import load_dataset, get_feature_importance_df


def show():
    render_page_header(
        title="Dataset Explorer & Visual Analytics",
        subtitle="Exploratory Data Analysis of advertising investments across media channels and product sales.",
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
        st.subheader("Raw Dataset Preview")
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
                title=f"Histogram & Boxplot of {selected_feature.upper()}",
                color_discrete_sequence=["#38bdf8"],
                height=380
            )
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with col_b:
            fig_all_box = px.box(
                df[["TV", "radio", "newspaper"]],
                title="Comparative Boxplots of Advertising Channels",
                color_discrete_sequence=["#2dd4bf"],
                height=380
            )
            fig_all_box.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
            )
            st.plotly_chart(fig_all_box, use_container_width=True)

        st.info("💡 **Outlier Observation:** As shown in the boxplots, Newspaper advertising exhibits two minor upper outliers above $100k, whereas TV and Radio spend are well-distributed without extreme anomalies.")

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
                color_continuous_scale="Blues",
                title="Pearson Correlation Heatmap",
                height=380
            )
            fig_corr.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
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
                color_discrete_sequence=["#38bdf8"],
                height=380
            )
            fig_sc.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis_title=f"{scatter_col.upper()} Advertising Budget ($k)",
                yaxis_title="Sales (k units)",
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        st.markdown(
            """
            - **TV vs Sales:** Strongest linear correlation (**r = 0.782**). Heavy investment consistently elevates sales.
            - **Radio vs Sales:** Moderate-to-strong positive correlation (**r = 0.576**).
            - **Newspaper vs Sales:** Weak correlation (**r = 0.228**). Notice how points spread out, showing low predictive direct dependence.
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
            color_continuous_scale="Teal",
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
            font=dict(family="Inter, sans-serif", color="#f1f5f9")
        )
        st.plotly_chart(fig_imp, use_container_width=True)

        st.markdown(
            """
            <div class="info-card">
                <strong>Strategic Recommendation:</strong> Reallocate underperforming newspaper budgets into TV and Radio. 
                Because newspaper accounts for only 1.30% of importance, reducing newspaper spend and shifting it into TV/Radio 
                substantially increases predicted sales without increasing overall advertising budget.
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    show()
