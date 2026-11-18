"""
Batch Prediction View: Upload CSV and Download Bulk Sales Predictions.
Configured for Indian Rupee (INR / ₹) advertising budget files.
"""

import io
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui_components import render_page_header, render_transparency_note
from utils.model_loader import validate_and_prepare_batch_df, predict_batch_sales
from utils.currency import DEFAULT_USD_TO_INR, format_inr_short, format_inr_currency


def show():
    render_page_header(
        title="Batch Sales Prediction (INR ₹)",
        subtitle="Upload a CSV file with advertising budgets in Indian Rupees (₹) to generate bulk sales forecasts.",
        badge="Bulk Processing (INR)"
    )

    col_info, col_template = st.columns([2, 1])

    with col_info:
        st.markdown(
            f"""
            #### 📄 Instructions for Indian Rupee (₹) Batch Upload
            1. Prepare a `.csv` file containing three columns: **`TV`**, **`radio`**, and **`newspaper`**.
            2. Enter advertising budgets as **amounts in Indian Rupees (₹)** (e.g. `13500000` for ₹1.35 Crore).
            3. The application automatically converts INR values using the exchange rate *(1 USD ≈ ₹{DEFAULT_USD_TO_INR:,.1f})* 
               before running the Polynomial Regression pipeline.
            """
        )

    with col_template:
        st.markdown("#### 📥 Sample INR Template")
        st.caption("Download a pre-formatted template with sample budgets in Indian Rupees (₹):")
        sample_df = pd.DataFrame({
            "TV": [13_500_000, 16_272_000, 4_005_000, 20_709_000, 783_000],
            "radio": [2_250_000, 972_000, 3_537_000, 3_402_000, 4_401_000],
            "newspaper": [1_800_000, 5_256_000, 4_059_000, 6_228_000, 6_750_000]
        })
        sample_csv = sample_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Sample CSV Template (INR ₹)",
            data=sample_csv,
            file_name="advertising_budget_template_inr.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("---")

    # File Uploader
    uploaded_file = st.file_uploader(
        "Upload your advertising budget CSV file (Amounts in INR ₹):",
        type=["csv"],
        help="Must contain columns: TV, radio, newspaper with non-negative numeric budgets in INR"
    )

    if uploaded_file is not None:
        try:
            try:
                raw_df = pd.read_csv(uploaded_file, sep=None, engine="python")
            except Exception:
                uploaded_file.seek(0)
                raw_df = pd.read_csv(uploaded_file)

            st.markdown(f"**Uploaded File:** `{uploaded_file.name}` ({len(raw_df)} rows detected)")

            # Validate DataFrame (checks columns, non-numerics, negative numbers, missing values)
            clean_df, errors = validate_and_prepare_batch_df(raw_df)

            if errors:
                for err in errors:
                    st.error(f"❌ Validation Error: {err}")
                st.warning("Please correct the CSV file and upload again.")
                return

            # Generate Batch Predictions with INR conversion
            with st.spinner(f"Converting INR budgets (Rate: ₹{DEFAULT_USD_TO_INR}/USD) and executing pipeline..."):
                results_df, out_of_bounds_count = predict_batch_sales(clean_df, exchange_rate=DEFAULT_USD_TO_INR)

            st.success(f"Successfully generated sales predictions for {len(results_df)} campaign scenarios!")

            if out_of_bounds_count > 0:
                st.warning(
                    f"⚠️ **Range Advisory:** {out_of_bounds_count} scenario(s) contain budget amounts exceeding "
                    f"the historical dataset training maximums. Predictions for extreme values may reflect polynomial extrapolation divergence."
                )

            # Summary Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Scenarios", f"{len(results_df):,}")
            with m2:
                st.metric("Avg Predicted Sales", f"{results_df['Predicted_Sales'].mean():.2f}k units")
            with m3:
                st.metric("Max Predicted Sales", f"{results_df['Predicted_Sales'].max():.2f}k units")
            with m4:
                st.metric("Min Predicted Sales", f"{results_df['Predicted_Sales'].min():.2f}k units")

            st.markdown("<br>", unsafe_allow_html=True)

            # Results Preview Table with formatted INR
            st.subheader("📋 Predictions Preview")
            display_preview = results_df.copy()
            # Format preview display for Indian Rupee readability
            display_preview["TV (₹)"] = display_preview["TV"].apply(lambda v: format_inr_currency(v))
            display_preview["Radio (₹)"] = display_preview["radio"].apply(lambda v: format_inr_currency(v))
            display_preview["Newspaper (₹)"] = display_preview["newspaper"].apply(lambda v: format_inr_currency(v))
            display_preview["Predicted Sales (k units)"] = display_preview["Predicted_Sales"].apply(lambda v: f"{v:.2f}k")
            display_preview["Estimated Total Units"] = display_preview["Predicted_Sales"].apply(lambda v: f"{v * 1000:,.0f}")

            preview_cols = ["TV (₹)", "Radio (₹)", "Newspaper (₹)", "Predicted Sales (k units)", "Estimated Total Units"]
            st.dataframe(display_preview[preview_cols], use_container_width=True)

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

            # Batch Distribution Chart in Light Theme
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📊 Distribution of Predicted Sales Across Batch")
            fig_batch = px.histogram(
                results_df,
                x="Predicted_Sales",
                nbins=15,
                marginal="box",
                title="Predicted Sales Distribution (k units)",
                color_discrete_sequence=["#65C6AE"],
                height=350
            )
            fig_batch.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis_title="Predicted Sales (k units)",
                font=dict(family="Inter, sans-serif", color="#AABBB9")
            )
            fig_batch.update_xaxes(showgrid=True, gridcolor="#22343A")
            fig_batch.update_yaxes(showgrid=True, gridcolor="#22343A")
            st.plotly_chart(fig_batch, use_container_width=True)

        except Exception as e:
            st.error(f"Failed to process CSV file: {str(e)}")

    # Transparency Note
    render_transparency_note(DEFAULT_USD_TO_INR)


if __name__ == "__main__":
    show()
