"""
Batch Prediction View: Upload CSV and Download Bulk Sales Predictions.
"""

import io
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_page_header
from utils.model_loader import validate_and_prepare_batch_df, predict_batch_sales


def show():
    render_page_header(
        title="Batch Sales Prediction",
        subtitle="Upload a CSV file with advertising budgets across TV, Radio, and Newspaper to generate bulk forecasts.",
        badge="Batch Processing Enabled"
    )

    col_info, col_template = st.columns([2, 1])

    with col_info:
        st.markdown(
            """
            #### 📄 Instructions
            1. Prepare a `.csv` file containing three columns: **`TV`**, **`radio`**, and **`newspaper`**.
            2. Budget values should be non-negative numeric amounts (in thousands of dollars, e.g., `150.0`).
            3. Upload your file below to process predictions with the saved Polynomial Regression pipeline.
            """
        )

    with col_template:
        st.markdown("#### 📥 Sample Template")
        st.caption("Download a pre-formatted template with sample budget scenarios:")
        sample_df = pd.DataFrame({
            "TV": [150.0, 180.8, 44.5, 230.1, 8.7],
            "radio": [25.0, 10.8, 39.3, 37.8, 48.9],
            "newspaper": [20.0, 58.4, 45.1, 69.2, 75.0]
        })
        sample_csv = sample_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Sample CSV Template",
            data=sample_csv,
            file_name="advertising_budget_template.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")

    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload your advertising budget CSV file:",
        type=["csv"],
        help="Must contain columns: TV, radio, newspaper (case-insensitive)"
    )

    if uploaded_file is not None:
        try:
            try:
                raw_df = pd.read_csv(uploaded_file, sep=None, engine="python")
            except Exception:
                uploaded_file.seek(0)
                raw_df = pd.read_csv(uploaded_file)

            st.markdown(f"**Uploaded File:** `{uploaded_file.name}` ({len(raw_df)} rows detected)")

            # Validate DataFrame
            clean_df, errors = validate_and_prepare_batch_df(raw_df)

            if errors:
                for err in errors:
                    st.error(f"❌ Validation Error: {err}")
                st.warning("Please correct the file and upload again.")
                return

            # Generate Batch Predictions
            with st.spinner("Processing batch predictions with Polynomial Regression pipeline..."):
                results_df, out_of_bounds_count = predict_batch_sales(clean_df)

            st.success(f"Successfully generated predictions for {len(results_df)} scenarios!")

            if out_of_bounds_count > 0:
                st.warning(f"⚠️ **Range Advisory:** {out_of_bounds_count} scenario(s) contain budget amounts exceeding historical dataset training maximums.")

            # Summary Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Rows Processed", f"{len(results_df):,}")
            with m2:
                st.metric("Average Predicted Sales", f"{results_df['Predicted_Sales'].mean():.2f}k units")
            with m3:
                st.metric("Max Predicted Sales", f"{results_df['Predicted_Sales'].max():.2f}k units")
            with m4:
                st.metric("Min Predicted Sales", f"{results_df['Predicted_Sales'].min():.2f}k units")

            st.markdown("<br>", unsafe_allow_html=True)

            # Results Preview Table
            st.subheader("📋 Predictions Preview")
            st.dataframe(results_df, use_container_width=True)

            # Export Button
            output_csv = results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Enriched Predictions (CSV)",
                data=output_csv,
                file_name=f"predicted_{uploaded_file.name}",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

            # Batch Distribution Chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📊 Distribution of Predicted Sales Across Batch")
            fig_batch = px.histogram(
                results_df,
                x="Predicted_Sales",
                nbins=15,
                marginal="box",
                title="Predicted Sales Distribution (k units)",
                color_discrete_sequence=["#0d9488"],
                height=350
            )
            fig_batch.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis_title="Predicted Sales (k units)",
                font=dict(family="Inter, sans-serif", color="#f1f5f9")
            )
            st.plotly_chart(fig_batch, use_container_width=True)

        except Exception as e:
            st.error(f"Failed to process CSV file: {str(e)}")


if __name__ == "__main__":
    show()
