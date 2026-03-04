# 2. QUANTITATIVE EXPLORATION
# -----------------------------------------------------------------------------

print_section("2.1 Distribution of happiness_average")

h = df["happiness_average"].dropna()
summary_stats = pd.DataFrame(
    {
        "metric": [
            "count",
            "mean",
            "median",
            "std",
            "p05 (5th percentile)",
            "p95 (95th percentile)",
        ],
        "value": [
            float(h.shape[0]),
            float(h.mean()),
            float(h.median()),
            float(h.std()),
            float(h.quantile(0.05)),
            float(h.quantile(0.95)),
        ],
    }
)

print(summary_stats.to_string(index=False))
save_csv(summary_stats, "happiness_average_summary_stats.csv", index=False)

# Histogram
plt.figure()
plt.hist(h, bins=40)
plt.title("Distribution of happiness_average (labMT 1.0)")
plt.xlabel("happiness_average (1–9)")
plt.ylabel("number of words")
plt.tight_layout()
save_figure("happiness_average_hist.png")
plt.close()


print_section("2.2 Disagreement: happiness_standard_deviation")

# Scatter: happiness score vs standard deviation
plt.figure()
plt.scatter(
    df["happiness_average"],
    df["happiness_standard_deviation"],
    s=10,
    alpha=0.35,
)
plt.title("Disagreement vs score: happiness_average vs happiness_standard_deviation")
plt.xlabel("happiness_average")
plt.ylabel("happiness_standard_deviation")
plt.tight_layout()
save_figure("happiness_vs_std_scatter.png")
plt.close()

# Which words do people disagree about most?
most_contested_15 = df.sort_values("happiness_standard_deviation", ascending=False).head(15)[show_cols]
print("Top 15 most 'contested' words (highest standard deviation):")
print(most_contested_15.to_string(index=False))
save_csv(most_contested_15, "top_15_contested_words.csv", index=False)


print_section("2.3 Corpus comparison: rank coverage + overlaps")

rank_cols = ["twitter_rank", "google_rank", "nyt_rank", "lyrics_rank"]

# (A) Coverage: how many words have a rank in each corpus?
coverage_rows = []
for col in rank_cols:
    n_present = int(df[col].notna().sum())
    coverage_rows.append(
        {
            "rank_column": col,
            "n_words_with_rank": n_present,
            "share_of_lexicon": n_present / len(df),
        }
    )

coverage = pd.DataFrame(coverage_rows)
print(coverage.to_string(index=False))
save_csv(coverage, "corpus_rank_coverage.csv", index=False)

# Bar chart (coverage)
plt.figure()
plt.bar(coverage["rank_column"], coverage["n_words_with_rank"])
plt.title("How many labMT words appear in each corpus top-5000?")
plt.xlabel("corpus rank column")
plt.ylabel("number of words with a rank")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
save_figure("corpus_rank_coverage_bar.png")
plt.close()

# (B) Overlap patterns: which corpora contain which words?
flags = pd.DataFrame(
    {
        "twitter": df["twitter_rank"].notna(),
        "google": df["google_rank"].notna(),
        "nyt": df["nyt_rank"].notna(),
        "lyrics": df["lyrics_rank"].notna(),
    }
)

labels = ["twitter", "google", "nyt", "lyrics"]
patterns = flags.apply(lambda row: "+".join([lab for lab in labels if row[lab]]) or "none", axis=1)

pattern_counts = patterns.value_counts().reset_index()
pattern_counts.columns = ["corpora_present", "n_words"]

print("\nMost common overlap patterns (top 12):")
print(pattern_counts.head(12).to_string(index=False))
save_csv(pattern_counts, "corpus_overlap_patterns.csv", index=False)

# A small table of pairwise overlaps can be easier to discuss in writing.
pairs = []
for i in range(len(labels)):
    for j in range(i + 1, len(labels)):
        a, b = labels[i], labels[j]
        pairs.append({"pair": f"{a}+{b}", "n_words_in_both": int((flags[a] & flags[b]).sum())})

pairwise_overlap = pd.DataFrame(pairs).sort_values("pair")
save_csv(pairwise_overlap, "pairwise_overlap_counts.csv", index=False)

# (C) One concrete example: frequent in one corpus, missing in another.
# Here we look for words that are relatively frequent on Twitter but do NOT appear in NYT's top-5000.

twitter_common_nyt_missing = (
    df[(df["twitter_rank"].notna()) & (df["nyt_rank"].isna())]
    .sort_values("twitter_rank")
    .head(20)[["word", "twitter_rank", "happiness_average"]]
)

print("\nExample words frequent on Twitter but missing in NYT top-5000 (top 20 by twitter_rank):")
print(twitter_common_nyt_missing.to_string(index=False))
save_csv(twitter_common_nyt_missing, "twitter_common_nyt_missing_top20.csv", index=False)

# Optional: compare ranks directly for words present in BOTH corpora.
# (This can hint at how similar/different the corpora are.)

both_twitter_nyt = df.dropna(subset=["twitter_rank", "nyt_rank"])

plt.figure()
plt.scatter(both_twitter_nyt["twitter_rank"], both_twitter_nyt["nyt_rank"], s=10, alpha=0.35)
plt.title("Twitter rank vs NYT rank (words present in both)")
plt.xlabel("twitter_rank (1 = most frequent)")
plt.ylabel("nyt_rank (1 = most frequent)")
plt.tight_layout()
save_figure("twitter_rank_vs_nyt_rank_scatter.png")
plt.close()





