import pandas as pd
import numpy as np

file_path = "data/raw/Data_Set_S1.txt"

df = pd.read_csv(
    file_path,
    sep="\t",
    skiprows=3,
    na_values=["--"],
    encoding="utf-8"
)

print("Columns:", df.columns)
print("Shape:", df.shape)
print(df.head())

# Convert numeric columns to numeric types
numeric_cols = [
    "happiness_rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("\nDtypes after conversion:")
print(df.dtypes)

from pathlib import Path

# Make sure tables/ exists
Path("tables").mkdir(parents=True, exist_ok=True)

# 1.2 Data dictionary info
dtypes = df.dtypes.astype(str)
missing_counts = df.isna().sum()

data_dict_df = (
    pd.DataFrame({
        "column": df.columns,
        "dtype": [dtypes[c] for c in df.columns],
        "n_missing": [int(missing_counts[c]) for c in df.columns],
        "example_value": [df[c].dropna().iloc[0] if df[c].dropna().shape[0] > 0 else None for c in df.columns],
    })
)

print("\n1.2 Data dictionary (column, dtype, missing):")
print(data_dict_df.to_string(index=False))

data_dict_df.to_csv("tables/data_dictionary.csv", index=False)