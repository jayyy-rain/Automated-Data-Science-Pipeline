#python -m streamlit run app/streamlit_app.py

import streamlit as st
import pandas as pd
import tempfile
import os

from src.pipeline.auto_pipeline import run_pipeline

st.set_page_config(page_title="Auto DS Pipeline", layout="wide")
st.title("Automated Data Science Pipeline")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        csv_path = tmp.name

    df_preview = pd.read_csv(csv_path)

    st.subheader("Target Selection")
    target_column = st.selectbox(
        "Select target column (optional)",
        ["None"] + list(df_preview.columns)
    )

    if target_column == "None":
        target_column = None

    if st.button("Run Pipeline"):
        run_pipeline(csv_path, target_column)

        st.subheader("Processed Dataset")
        st.dataframe(pd.read_csv("data/processed/processed_data.csv").head())

        st.subheader("Feature Importance")
        if os.path.exists("reports/feature_importance.csv"):
            st.dataframe(pd.read_csv("reports/feature_importance.csv").head(10))
        else:
            st.info("Feature importance not available (no target selected).")

        st.subheader("EDA Visualizations")
        if os.path.exists("reports/figures"):
            cols = st.columns(2)
            images = os.listdir("reports/figures")
            for i, img in enumerate(images):
                cols[i % 2].image(
                    os.path.join("reports/figures", img),
                    width=350
                )

        st.subheader("Auto-generated Report")
        with open("reports/auto_report.md", encoding="utf-8") as f:
            st.markdown(f.read())