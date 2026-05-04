import os

from src.ingestion.data_loader import load_data, validate_dataframe, infer_column_types
from src.profiling.eda import generate_profile
from src.preprocessing.missing_values import handle_missing_values
from src.preprocessing.encoding import encode_categorical
from src.preprocessing.scaling import scale_numerical
from src.preprocessing.feature_engineering import feature_engineering
from src.visualization.plots import generate_plots
from src.reporting.report_generator import generate_report
from src.explainability.feature_importance import compute_feature_importance
from src.utils.logger import get_logger

logger = get_logger("AutoPipeline")


def detect_target_column(df):
    for col in ["diagnosis", "target", "label", "aqi", "y"]:
        if col in df.columns:
            return col
    return None


def run_pipeline(csv_path: str, target_column: str | None = None):

    # ------------------------------
    # CLEAR OLD ARTIFACTS
    # ------------------------------
    if os.path.exists("reports/figures"):
        for f in os.listdir("reports/figures"):
            os.remove(os.path.join("reports/figures", f))

    if os.path.exists("reports/feature_importance.csv"):
        os.remove("reports/feature_importance.csv")

    if os.path.exists("reports/auto_report.md"):
        os.remove("reports/auto_report.md")

    # ------------------------------
    # LOAD DATA
    # ------------------------------
    logger.info("Loading data")
    df = load_data(csv_path)
    validate_dataframe(df)

    logger.info("Inferring column types")
    column_types = infer_column_types(df)

    logger.info("Profiling data")
    profile = generate_profile(df, column_types)

    # ------------------------------
    # GENERATE EDA VISUALS
    # ------------------------------
    logger.info("Generating EDA plots")
    generate_plots(
        df,
        column_types["numerical"],
        column_types["categorical"],
        "reports/figures"
    )

    # ------------------------------
    # PREPROCESSING
    # ------------------------------
    logger.info("Handling missing values")
    df = handle_missing_values(
        df,
        column_types["numerical"],
        column_types["categorical"]
    )

    logger.info("Feature engineering")
    df = feature_engineering(
        df,
        column_types["datetime"],
        profile["constant_columns"]
    )

    # ------------------------------
    # TARGET SELECTION LOGIC
    # ------------------------------
    if target_column:
        TARGET_COLUMN = target_column
    else:
        TARGET_COLUMN = detect_target_column(df)

    if TARGET_COLUMN and TARGET_COLUMN in df.columns:
        y = df[TARGET_COLUMN]
        X = df.drop(columns=[TARGET_COLUMN])

        categorical_cols = [
            c for c in column_types["categorical"] if c != TARGET_COLUMN
        ]
        numerical_cols = [
            n for n in column_types["numerical"] if n != TARGET_COLUMN
        ]
    else:
        y = None
        X = df
        categorical_cols = column_types["categorical"]
        numerical_cols = column_types["numerical"]

    # ------------------------------
    # ENCODING & SCALING
    # ------------------------------
    logger.info("Encoding categorical features")
    X = encode_categorical(
        X,
        categorical_cols,
        profile["high_cardinality"]
    )

    logger.info("Scaling numerical features")
    X = scale_numerical(X, numerical_cols)

    if y is not None:
        df = X.copy()
        df[TARGET_COLUMN] = y
    else:
        df = X

    # ------------------------------
    # SAVE PROCESSED DATA
    # ------------------------------
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/processed_data.csv", index=False)

    # ------------------------------
    # FEATURE IMPORTANCE
    # ------------------------------
    if TARGET_COLUMN and TARGET_COLUMN in df.columns:
        logger.info(f"Computing feature importance for target: {TARGET_COLUMN}")
        fi_df = compute_feature_importance(df, TARGET_COLUMN)
        fi_df.to_csv("reports/feature_importance.csv", index=False)

    # ------------------------------
    # REPORT
    # ------------------------------
    logger.info("Generating report")
    generate_report(profile)

    logger.info("Pipeline completed")
