import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_numerical(df: pd.DataFrame, numerical_cols: list) -> pd.DataFrame:
    df = df.copy()

    if numerical_cols:
        scaler = StandardScaler()
        df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    return df
