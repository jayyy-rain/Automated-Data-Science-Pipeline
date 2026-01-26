import pandas as pd

def generate_profile(df: pd.DataFrame, column_types: dict) -> dict:
    profile = {}

    profile["shape"] = df.shape
    profile["missing"] = df.isnull().sum().to_dict()
    profile["numerical"] = column_types["numerical"]
    profile["categorical"] = column_types["categorical"]
    profile["datetime"] = column_types["datetime"]

    profile["unique_counts"] = {
        col: df[col].nunique() for col in df.columns
    }

    profile["constant_columns"] = [
        col for col in df.columns if df[col].nunique() <= 1
    ]

    profile["high_cardinality"] = [
        col for col in column_types["categorical"]
        if df[col].nunique() > 20
    ]

    return profile
