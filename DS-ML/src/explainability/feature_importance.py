import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor


def compute_feature_importance(df: pd.DataFrame, target_column: str):

    X = df.drop(columns=[target_column])
    y = df[target_column]

    if y.dtype == "object" or y.nunique() <= 10:
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    else:
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )

    model.fit(X, y)

    fi_df = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    return fi_df
