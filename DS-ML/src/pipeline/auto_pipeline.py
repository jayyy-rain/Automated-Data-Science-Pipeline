from src.reporting.report_generator import generate_report
import os
from src.ingestion.data_loader import load_data, validate_dataframe, infer_column_types
from src.profiling.eda import generate_profile
from src.preprocessing.missing_values import handle_missing_values
from src.preprocessing.encoding import encode_categorical
from src.preprocessing.scaling import scale_numerical
from src.preprocessing.feature_engineering import feature_engineering
from src.visualization.plots import generate_plots
from src.utils.logger import get_logger

logger = get_logger("AutoPipeline")

def run_pipeline(csv_path: str):
    logger.info("Loading data")
    df = load_data(csv_path)
    validate_dataframe(df)

    logger.info("Inferring column types")
    column_types = infer_column_types(df)

    logger.info("Profiling data")
    profile = generate_profile(df, column_types)

    logger.info("Generating EDA plots")
    generate_plots(
        df,
        column_types["numerical"],
        column_types["categorical"],
        "reports/figures"
    )

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

    logger.info("Encoding categorical features")
    df = encode_categorical(
        df,
        column_types["categorical"],
        profile["high_cardinality"]
    )

    logger.info("Scaling numerical features")
    df = scale_numerical(df, column_types["numerical"])

    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/processed_data.csv"
    df.to_csv(output_path, index=False)

    logger.info(f"Pipeline complete. Output saved to {output_path}")
