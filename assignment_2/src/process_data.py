from pathlib import Path
import json
import re
import pandas as pd

# -----------------------------------
# paths
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CACHE_DIR = BASE_DIR / "data" / "cache"

FILE_1900_1950 = RAW_DIR / "met_photographs_american_1900_1950_raw.json"
FILE_1951_2000 = RAW_DIR / "met_photographs_american_1951_2000_raw.json"

OUTPUT_FILE = CACHE_DIR / "processed_photographs_titles.csv"


# -----------------------------------
# load json
# -----------------------------------
def load_json_to_df(filepath: Path) -> pd.DataFrame:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return pd.DataFrame(data)

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                return pd.DataFrame(value)
        return pd.json_normalize(data)

    raise ValueError(f"Unsupported JSON structure in {filepath}")


# -----------------------------------
# clean title text
# -----------------------------------
def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# -----------------------------------
# main
# -----------------------------------
def main():
    print("Loading raw datasets...")

    df1 = load_json_to_df(FILE_1900_1950)
    df2 = load_json_to_df(FILE_1951_2000)

    df1["period"] = "1900-1950"
    df2["period"] = "1951-2000"

    df = pd.concat([df1, df2], ignore_index=True)

    print("Merged shape:", df.shape)
    print("Merged columns:")
    print(df.columns.tolist())
    print()

    # keep useful metadata
    keep_cols = [
        "objectID",
        "title",
        "artistDisplayName",
        "artistNationality",
        "objectDate",
        "objectBeginDate",
        "objectEndDate",
        "department",
        "classification",
        "medium",
        "repository",
        "objectURL",
        "period",
    ]

    df = df[keep_cols].copy()

    # remove missing or empty titles
    df = df[df["title"].notna()]
    df = df[df["title"].astype(str).str.strip() != ""]

    # clean title
    df["clean_title"] = df["title"].apply(clean_text)

    # remove rows with empty clean_title
    df = df[df["clean_title"].str.strip() != ""]

    print("Final columns:")
    print(df.columns.tolist())
    print()

    print("Period counts:")
    print(df["period"].value_counts(dropna=False))
    print()

    print("Sample rows:")
    print(df.head())
    print()

    print("Title length summary:")
    print(df["clean_title"].str.split().str.len().describe())
    print()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Saved processed dataset to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
