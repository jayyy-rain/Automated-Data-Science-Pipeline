import pandas as pd

def handle_missing_values(df: pd.DataFrame,
                          numerical_cols: list,
                          categorical_cols: list) -> pd.DataFrame:
    df = df.copy()

    for col in numerical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    for col in categorical_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0])

    return df
