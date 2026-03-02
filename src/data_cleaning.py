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