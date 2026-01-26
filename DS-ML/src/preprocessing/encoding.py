import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_categorical(df: pd.DataFrame,
                       categorical_cols: list,
                       high_cardinality_cols: list) -> pd.DataFrame:
    df = df.copy()

    low_cardinality = [
        col for col in categorical_cols if col not in high_cardinality_cols
    ]

    if low_cardinality:
        encoder = OneHotEncoder(
            sparse_output=False,
            drop="first",
            handle_unknown="ignore"
        )

        encoded = encoder.fit_transform(df[low_cardinality])

        encoded_df = pd.DataFrame(
            encoded,
            columns=encoder.get_feature_names_out(low_cardinality),
            index=df.index
        )

        df.drop(columns=low_cardinality, inplace=True)
        df = pd.concat([df, encoded_df], axis=1)

    for col in high_cardinality_cols:
        freq = df[col].value_counts(normalize=True)
        df[col] = df[col].map(freq)

    return df
