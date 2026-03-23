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

FILE_1900_1950 = RAW_DIR / "met_photographs_european_1900_1950_raw.json"
FILE_1951_2000 = RAW_DIR / "met_photographs_european_1951_2000_raw.json"

OUTPUT_FILE = CACHE_DIR / "processed_photographs_titles_european.csv"


# -----------------------------------
# load json
# -----------------------------------
def load_json_to_df(filepath: Path) -> pd.DataFrame:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

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
    print("Loading European raw datasets...")

    df1 = load_json_to_df(FILE_1900_1950)
    df2 = load_json_to_df(FILE_1951_2000)

    print(f"1900-1950 shape: {df1.shape}")
    print(f"1951-2000 shape: {df2.shape}")
    print()

    df1["period"] = "1900-1950"
    df2["period"] = "1951-2000"

    # Optional: mark region/source
    df1["group"] = "European"
    df2["group"] = "European"

    # merge
    df = pd.concat([df1, df2], ignore_index=True)

    print("Merged shape:", df.shape)
    print("Merged columns:")
    print(df.columns.tolist())
    print()

    # keep useful metadata only if present
    preferred_cols = [
        "objectID",
        "title",
        "artistDisplayName",
        "artistNationality",
        "artistDisplayBio",
        "objectDate",
        "objectBeginDate",
        "objectEndDate",
        "department",
        "classification",
        "medium",
        "culture",
        "country",
        "region",
        "repository",
        "objectURL",
        "period",
        "group",
    ]

    keep_cols = [col for col in preferred_cols if col in df.columns]
    df = df[keep_cols].copy()

    if "title" not in df.columns:
        raise KeyError("Column 'title' not found in merged dataset.")

    # remove missing / empty titles
    before = len(df)
    df = df[df["title"].notna()]
    df = df[df["title"].astype(str).str.strip() != ""]
    after = len(df)

    print(f"Removed {before - after} rows with missing/empty titles.")
    print()

    # clean titles
    df["clean_title"] = df["title"].apply(clean_text)

    # remove rows whose clean_title becomes empty
    before_clean = len(df)
    df = df[df["clean_title"].str.strip() != ""]
    after_clean = len(df)

    print(f"Removed {before_clean - after_clean} rows with empty cleaned titles.")
    print()

    # title length variable (useful for later analysis)
    df["title_length"] = df["clean_title"].str.split().str.len()

    print("Final shape:", df.shape)
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
    print(df["title_length"].describe())
    print()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Saved processed dataset to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    