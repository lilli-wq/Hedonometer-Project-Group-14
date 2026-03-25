from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------
# 1. File paths
# ---------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUTPUTS_DIR = ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

AMERICA_FILE = DATA_DIR / "calculated_scores_America.csv"
EUROPE_FILE = DATA_DIR / "calculated_scores_Europe.csv"

# ---------------------------------------------------
# 2. Load the two datasets
# ---------------------------------------------------
df_america = pd.read_csv(AMERICA_FILE)
df_europe = pd.read_csv(EUROPE_FILE)

# Add a column that says which region each row belongs to
df_america["region"] = "America"
df_europe["region"] = "Europe"

# Combine both datasets into one big table
df = pd.concat([df_america, df_europe], ignore_index=True)

# Remove rows where happiness_score is missing
df = df.dropna(subset=["happiness_score"]).copy()

print("Combined dataset loaded.")
print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nRegions:")
print(df["region"].unique())

print("\nPeriods:")
print(df["period"].unique())

# ---------------------------------------------------
# 3. Summary statistics by region and period
# ---------------------------------------------------
summary = df.groupby(["region", "period"])["happiness_score"].agg(
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
).reset_index()

print("\nSummary statistics:")
print(summary)

print("\nStandard deviations by region and period:")
print(summary[["region", "period", "std"]])

summary.to_csv(OUTPUTS_DIR / "summary_stats_america_europe.csv", index=False)

# ---------------------------------------------------
# 4. Function for bootstrap confidence interval
# ---------------------------------------------------
def bootstrap_diff_ci(series_a, series_b, n_boot=2000, seed=42):
    rng = np.random.default_rng(seed)
    a = series_a.dropna().to_numpy()
    b = series_b.dropna().to_numpy()

    boot_diffs = []

    for _ in range(n_boot):
        sample_a = rng.choice(a, size=len(a), replace=True)
        sample_b = rng.choice(b, size=len(b), replace=True)
        boot_diffs.append(sample_b.mean() - sample_a.mean())

    observed_diff = b.mean() - a.mean()
    ci_lower = np.percentile(boot_diffs, 2.5)
    ci_upper = np.percentile(boot_diffs, 97.5)

    return observed_diff, ci_lower, ci_upper

# ---------------------------------------------------
# 5. Create the four groups
# ---------------------------------------------------
a_early = df[(df["region"] == "America") & (df["period"] == "1900-1950")]["happiness_score"]
a_late = df[(df["region"] == "America") & (df["period"] == "1951-2000")]["happiness_score"]
e_early = df[(df["region"] == "Europe") & (df["period"] == "1900-1950")]["happiness_score"]
e_late = df[(df["region"] == "Europe") & (df["period"] == "1951-2000")]["happiness_score"]

# ---------------------------------------------------
# 6. Compare groups with bootstrap confidence intervals
# ---------------------------------------------------
comparisons = []

def add_comparison(name, group1, group2):
    diff, low, high = bootstrap_diff_ci(group1, group2)
    comparisons.append({
        "comparison": name,
        "group1_mean": group1.mean(),
        "group2_mean": group2.mean(),
        "difference_group2_minus_group1": diff,
        "ci_lower": low,
        "ci_upper": high
    })

# Time change within each region
add_comparison("America: 1951-2000 minus 1900-1950", a_early, a_late)
add_comparison("Europe: 1951-2000 minus 1900-1950", e_early, e_late)

# Region difference within each period
add_comparison("1900-1950: Europe minus America", a_early, e_early)
add_comparison("1951-2000: Europe minus America", a_late, e_late)

comparisons_df = pd.DataFrame(comparisons)

print("\nBootstrap comparisons:")
print(comparisons_df)

comparisons_df.to_csv(OUTPUTS_DIR / "bootstrap_comparisons_america_europe.csv", index=False)

# ---------------------------------------------------
# 7. Difference-in-differences
# ---------------------------------------------------
america_change = a_late.mean() - a_early.mean()
europe_change = e_late.mean() - e_early.mean()
did_value = europe_change - america_change

print("\nDifference-in-differences (Europe time change minus America time change):")
print(did_value)

# Bootstrap DID
rng = np.random.default_rng(42)
did_boot = []

a_early_vals = a_early.dropna().to_numpy()
a_late_vals = a_late.dropna().to_numpy()
e_early_vals = e_early.dropna().to_numpy()
e_late_vals = e_late.dropna().to_numpy()

for _ in range(2000):
    a_early_s = rng.choice(a_early_vals, size=len(a_early_vals), replace=True)
    a_late_s = rng.choice(a_late_vals, size=len(a_late_vals), replace=True)
    e_early_s = rng.choice(e_early_vals, size=len(e_early_vals), replace=True)
    e_late_s = rng.choice(e_late_vals, size=len(e_late_vals), replace=True)

    america_change_s = a_late_s.mean() - a_early_s.mean()
    europe_change_s = e_late_s.mean() - e_early_s.mean()
    did_boot.append(europe_change_s - america_change_s)

did_low = np.percentile(did_boot, 2.5)
did_high = np.percentile(did_boot, 97.5)

did_df = pd.DataFrame([{
    "comparison": "Difference-in-differences",
    "estimate": did_value,
    "ci_lower": did_low,
    "ci_upper": did_high
}])

print("\nDID bootstrap CI:")
print(did_df)

did_df.to_csv(OUTPUTS_DIR / "difference_in_differences_america_europe.csv", index=False)