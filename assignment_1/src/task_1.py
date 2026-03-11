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

# 1.3 Sanity Checks
print("\n1.3 Sanity checks")

# Sanity check one: are any words repeated?
# `word` is the column that identifies the entry in this dataset
dup_mask = df["word"].duplicated(keep=False)
dupes = df.loc[dup_mask, "word"].unique()
if dupes.size: 
    print("\ncount of duplicated words:", dupes.size)
    print("duplicated words found:", dupes)
else:
    print("\ncount of duplicated words:", dupes.size)

# inspect a random sample
random_15 = df.sample(15, random_state=33)
print("\nrandom sample of 15 rows:")
print(random_15)
random_15.to_csv("tables/random_sample_15_rows.csv", index=False)

# ten most positive / ten most negative by happiness_average
sorted_df = df.sort_values("happiness_average", ascending=False)
top10 = sorted_df.head(10)[["word", "happiness_average"]]
bot10 = sorted_df.tail(10)[["word", "happiness_average"]]

print("\n10 most positive words:")
print(top10.to_string(index=False))
print("\n10 most negative words:")
print(bot10.to_string(index=False))

# save the results for later reference
top10.to_csv("tables/top_10_positive_words.csv", index=False)
bot10.to_csv("tables/top_10_negative_words.csv", index=False)