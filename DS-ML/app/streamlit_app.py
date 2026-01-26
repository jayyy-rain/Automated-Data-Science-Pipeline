import streamlit as st
import pandas as pd
import tempfile
import os

from src.pipeline.auto_pipeline import run_pipeline

st.set_page_config(page_title="Auto DS Pipeline", layout="wide")

st.title("🧠 Automated Data Science Pipeline")
st.write("Upload a CSV file and automatically generate EDA, preprocessing, and ML-ready data.")

# ---- File upload ----
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        csv_path = tmp.name

    st.success("CSV uploaded successfully")

    if st.button("Run Pipeline"):
        with st.spinner("Running data pipeline..."):
            run_pipeline(csv_path)

        st.success("Pipeline completed successfully")

        # ---- Show processed data ----
        processed_path = "data/processed/processed_data.csv"

        if os.path.exists(processed_path):
            df_processed = pd.read_csv(processed_path)

            st.subheader("📦 Processed Dataset Preview")
            st.dataframe(df_processed.head())

            st.download_button(
                label="⬇️ Download Processed CSV",
                data=df_processed.to_csv(index=False),
                file_name="processed_data.csv",
                mime="text/csv"
            )

        # ---- Show EDA images ----
        st.subheader("📊 EDA Visualizations")
        figures_dir = "reports/figures"

        if os.path.exists(figures_dir):
            images = sorted(os.listdir(figures_dir))
            for img in images:
                st.image(os.path.join(figures_dir, img), caption=img, use_container_width=True)

        # ---- Show report ----
        report_path = "reports/auto_report.md"
        if os.path.exists(report_path):
            st.subheader("📝 Auto-generated Report")
            with open(report_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
