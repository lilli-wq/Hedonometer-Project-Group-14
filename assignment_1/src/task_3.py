"""
Task 3.1 — Build a small "exhibit" of words (20 total)

Outputs:
- tables/word_exhibit_20_words.csv

Selection:
- 5 very positive (highest happiness_average)
- 5 very negative (lowest happiness_average)
- 5 highly contested (highest happiness_standard_deviation)
- 5 weird / surprising / historically dated / culturally loaded (manual list)
"""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/raw/Data_Set_S1.txt")
TABLES_DIR = Path("tables")
TABLES_DIR.mkdir(parents=True, exist_ok=True)

WEIRD_WORDS = ["porn", "capitalism", "churches", "mortality", "cigarette"]


def load_labmt(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}. Put it in data/raw/.")

    df = pd.read_csv(
        path,
        sep="\t",
        skiprows=3,
        na_values=["--"],
        encoding="utf-8",
    )

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

    df["word"] = df["word"].astype("string")
    return df


def main() -> None:
    df = load_labmt(DATA_PATH)

    pos5 = df.sort_values("happiness_average", ascending=False).head(5).copy()
    pos5["category"] = "very positive"

    neg5 = df.sort_values("happiness_average", ascending=True).head(5).copy()
    neg5["category"] = "very negative"

    con5 = df.sort_values("happiness_standard_deviation", ascending=False).head(5).copy()
    con5["category"] = "highly contested"

    # weird words (manual selection) — currently empty
    weird5 = df[df["word"].isin(WEIRD_WORDS)].copy()
    weird5["category"] = "weird/culturally loaded"

    exhibit_cols = [
        "category",
        "word",
        "happiness_average",
        "happiness_standard_deviation",
        "twitter_rank",
        "google_rank",
        "nyt_rank",
        "lyrics_rank",
    ]

    exhibit = pd.concat([pos5, neg5, con5, weird5], ignore_index=True)[exhibit_cols]

    print(exhibit.to_string(index=False))

    out_path = TABLES_DIR / "word_exhibit_20_words.csv"
    exhibit.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()