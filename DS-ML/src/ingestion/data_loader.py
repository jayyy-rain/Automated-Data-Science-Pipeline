import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    if not path.endswith(".csv"):
        raise ValueError("Only CSV files are supported.")
    df = pd.read_csv(path)
    return df


def validate_dataframe(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Dataset is empty.")
    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names found.")


def infer_column_types(df: pd.DataFrame) -> dict:
    numerical = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = []

    for col in df.columns:
        if col not in numerical and col not in categorical:
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
            except Exception:
                pass

    return {
        "numerical": numerical,
        "categorical": categorical,
        "datetime": datetime_cols
    }
