import pandas as pd

def feature_engineering(df: pd.DataFrame,
                        datetime_cols: list,
                        constant_cols: list) -> pd.DataFrame:
    df = df.copy()

    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_day"] = df[col].dt.day
        df.drop(columns=col, inplace=True)

    if constant_cols:
        df.drop(columns=constant_cols, inplace=True)

    return df
