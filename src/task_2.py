# ---- Section 2: Quantitative exploration ----
SCORE = "happiness_average"
STD = "happiness_standard_deviation"
RANK_COLS = ["twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"]
LABELS = ["twitter", "google", "nyt", "lyrics"]


def describe_series(s: pd.Series) -> pd.DataFrame:
    s = s.dropna()
    return pd.DataFrame(
        {
            "metric": ["count", "mean", "median", "std", "p05", "p95"],
            "value": [
                int(s.shape[0]),
                float(s.mean()),
                float(s.median()),
                float(s.std()),
                float(s.quantile(0.05)),
                float(s.quantile(0.95)),
            ],
        }
    )


def save_hist(series: pd.Series, fname: str, title: str, xlabel: str, bins: int = 40):
    plt.figure()
    plt.hist(series.dropna(), bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("number of words")
    plt.tight_layout()
    save_figure(fname)
    plt.close()


def save_scatter(x, y, fname: str, title: str, xlabel: str, ylabel: str, s: int = 10, alpha: float = 0.35):
    plt.figure()
    plt.scatter(x, y, s=s, alpha=alpha)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    save_figure(fname)
    plt.close()


print_section("2.1 Distribution of happiness scores")
stats = describe_series(df[SCORE])
save_csv(stats, "happiness_average_summary_stats.csv", index=False)
save_hist(df[SCORE], "happiness_average_hist.png", "Distribution of happiness scores (labMT 1.0)", SCORE)

print_section("2.2 Contested words (disagreement)")
save_scatter(df[SCORE], df[STD], "happiness_vs_std_scatter.png", "Disagreement vs score", SCORE, STD)

show_cols = ["word", SCORE, STD]  # keep it explicit + small
top15 = df.sort_values(STD, ascending=False).head(15)[show_cols]
save_csv(top15, "top_15_contested_words.csv", index=False)

print_section("2.3 Corpus comparison")
coverage = pd.DataFrame(
    {
        "rank_column": RANK_COLS,
        "n_words_with_rank": [int(df[c].notna().sum()) for c in RANK_COLS],
    }
)
coverage["share_of_lexicon"] = coverage["n_words_with_rank"] / len(df)
save_csv(coverage, "corpus_rank_coverage.csv", index=False)

plt.figure()
plt.bar(coverage["rank_column"], coverage["n_words_with_rank"])
plt.title("Coverage: labMT words in each corpus top-5000")
plt.xlabel("corpus")
plt.ylabel("n words with rank")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
save_figure("corpus_rank_coverage_bar.png")
plt.close()

flags = pd.DataFrame({lab: df[col].notna() for lab, col in zip(LABELS, RANK_COLS)})
patterns = flags.apply(lambda r: "+".join([lab for lab in LABELS if r[lab]]) or "none", axis=1)
pattern_counts = patterns.value_counts().rename_axis("corpora_present").reset_index(name="n_words")
save_csv(pattern_counts, "corpus_overlap_patterns.csv", index=False)

pairwise = pd.DataFrame(
    [
        {"pair": f"{a}+{b}", "n_words_in_both": int((flags[a] & flags[b]).sum())}
        for i, a in enumerate(LABELS)
        for b in LABELS[i + 1 :]
    ]
).sort_values("pair")
save_csv(pairwise, "pairwise_overlap_counts.csv", index=False)

twitter_common_nyt_missing = (
    df[df["twitter_rank"].notna() & df["nyt_rank"].isna()]
    .sort_values("twitter_rank")
    .head(20)[["word", "twitter_rank", SCORE]]
)
save_csv(twitter_common_nyt_missing, "twitter_common_nyt_missing_top20.csv", index=False)

both = df.dropna(subset=["twitter_rank", "nyt_rank"])
save_scatter(
    both["twitter_rank"],
    both["nyt_rank"],
    "twitter_rank_vs_nyt_rank_scatter.png",
    "Twitter rank vs NYT rank (shared words)",
    "twitter_rank (1 = most frequent)",
    "nyt_rank (1 = most frequent)",
)

