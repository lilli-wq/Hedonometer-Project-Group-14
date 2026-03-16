from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "met_with_scores.csv"

df = pd.read_csv(DATA_FILE)
# Remove rows where happiness_score is missing
df = df.dropna(subset=["happiness_score"])

print("Loaded dataset.")
print("Shape:", df.shape)

# Split by period
period_1900_1950 = df[df["period"] == "1900-1950"]
period_1951_2000 = df[df["period"] == "1951-2000"]

print("\nNumber of artworks per period:")
print("1900–1950:", len(period_1900_1950))
print("1951–2000:", len(period_1951_2000))

# Mean happiness
mean_1 = period_1900_1950["happiness_score"].mean()
mean_2 = period_1951_2000["happiness_score"].mean()

print("\nMean happiness score:")
print("1900–1950:", mean_1)
print("1951–2000:", mean_2)

# Difference in means
diff = mean_2 - mean_1
print("\nDifference in means (1951–2000 minus 1900–1950):", diff)

# Distribution summary for each period
distribution_summary = df.groupby("period")["happiness_score"].agg(
    count="count",
    mean="mean",
    median="median",
    std="std",
    min="min",
    q25=lambda x: x.quantile(0.25),
    q75=lambda x: x.quantile(0.75),
    q05=lambda x: x.quantile(0.05),
    q95=lambda x: x.quantile(0.95),
    max="max"
)

print("\nDistribution summary by period:")
print(distribution_summary)


# ---------------------------------------------------
# Bootstrap confidence interval
# ---------------------------------------------------

scores_1 = period_1900_1950["happiness_score"].values
scores_2 = period_1951_2000["happiness_score"].values

boot_diffs = []

for i in range(2000):
    sample1 = np.random.choice(scores_1, size=len(scores_1), replace=True)
    sample2 = np.random.choice(scores_2, size=len(scores_2), replace=True)

    boot_diffs.append(sample2.mean() - sample1.mean())

ci_lower = np.percentile(boot_diffs, 2.5)
ci_upper = np.percentile(boot_diffs, 97.5)

print("\nBootstrap 95% confidence interval for difference:")
print(ci_lower, "to", ci_upper)