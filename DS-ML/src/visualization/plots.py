import os
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots(df, numerical_cols, categorical_cols, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for col in numerical_cols:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(col)
        plt.savefig(f"{output_dir}/{col}_hist.png")
        plt.close()

        plt.figure()
        sns.boxplot(x=df[col])
        plt.title(col)
        plt.savefig(f"{output_dir}/{col}_box.png")
        plt.close()

    for col in categorical_cols:
        plt.figure()
        df[col].value_counts().head(10).plot(kind="bar")
        plt.title(col)
        plt.savefig(f"{output_dir}/{col}_count.png")
        plt.close()

    if len(numerical_cols) > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[numerical_cols].corr(), annot=False, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_dir}/correlation_heatmap.png")
        plt.close()
