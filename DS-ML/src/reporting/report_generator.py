import os

def generate_report(profile: dict, output_path: str = "reports/auto_report.md"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Automated EDA Report\n\n")

        f.write("## Dataset Overview\n")
        f.write(f"- Rows: {profile['shape'][0]}\n")
        f.write(f"- Columns: {profile['shape'][1]}\n\n")

        f.write("## Column Types\n")
        f.write(f"- Numerical: {profile['numerical']}\n")
        f.write(f"- Categorical: {profile['categorical']}\n")
        f.write(f"- Datetime: {profile['datetime']}\n\n")

        f.write("## Missing Values\n")
        for col, count in profile["missing"].items():
            if count > 0:
                f.write(f"- {col}: {count}\n")
        f.write("\n")

        f.write("## Dropped / Special Columns\n")
        f.write(f"- Constant columns: {profile['constant_columns']}\n")
        f.write(f"- High cardinality columns: {profile['high_cardinality']}\n\n")

        f.write("## Visualizations\n")
        f.write("All plots are saved in `reports/figures/`\n")
