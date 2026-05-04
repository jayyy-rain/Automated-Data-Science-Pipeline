import os
import pandas as pd


def generate_report(profile, output_path="reports/auto_report.md"):

    os.makedirs("reports", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Automated EDA Report\n\n")

        f.write("## Dataset Overview\n")
        f.write(f"- Rows: {profile['shape'][0]}\n")
        f.write(f"- Columns: {profile['shape'][1]}\n\n")

        f.write("## Column Types\n")
        f.write(f"- Numerical: {profile['numerical']}\n")
        f.write(f"- Categorical: {profile['categorical']}\n")
        f.write(f"- Datetime: {profile['datetime']}\n\n")

        f.write("## Missing Values\n")
        missing = profile.get("missing", {})
        if any(v > 0 for v in missing.values()):
            for k, v in missing.items():
                if v > 0:
                    f.write(f"- {k}: {v}\n")
        else:
            f.write("No missing values detected.\n")

        f.write("\n## Special Columns\n")
        f.write(f"- Constant columns: {profile['constant_columns']}\n")
        f.write(f"- High cardinality columns: {profile['high_cardinality']}\n\n")

        f.write("## Visualizations\nAll plots saved in `reports/figures/`\n\n")

        if os.path.exists("reports/feature_importance.csv"):
            fi = pd.read_csv("reports/feature_importance.csv")
            f.write("## Feature Importance\n")
            for _, row in fi.head(10).iterrows():
                f.write(f"- {row['feature']}\n")
