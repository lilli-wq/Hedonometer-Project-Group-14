from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "met_with_scores.csv"
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(DATA_FILE)
df = df.dropna(subset=["happiness_score"])

print("Loaded dataset.")
print(f"Total artworks: {len(df)}")

# =====================================================
# Histogram 1: Overall distribution of happiness scores
# =====================================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df["happiness_score"], bins=30, color="steelblue", edgecolor="black", alpha=0.7)
ax.set_xlabel("Happiness Score", fontsize=12, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=12, fontweight="bold")
ax.set_title("Distribution of Happiness Scores\nMetropolitan Museum American Photographs (1900-2000)", 
             fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "happiness_distribution_overall.png", dpi=300, bbox_inches="tight")
print(f"Saved: happiness_distribution_overall.png")
plt.close()

# =====================================================
# Visualization: Density plots by period (smooth comparison)
# =====================================================
fig, ax = plt.subplots(figsize=(11, 6))

period_1900_1950 = df[df["period"] == "1900-1950"]["happiness_score"]
period_1951_2000 = df[df["period"] == "1951-2000"]["happiness_score"]

# Density plots
period_1900_1950.plot(kind="density", ax=ax, color="coral", linewidth=2.5, 
                       label=f"1900–1950 (μ={period_1900_1950.mean():.2f})", alpha=0.8)
period_1951_2000.plot(kind="density", ax=ax, color="skyblue", linewidth=2.5,
                       label=f"1951–2000 (μ={period_1951_2000.mean():.2f})", alpha=0.8)

# Add vertical lines for means
ax.axvline(period_1900_1950.mean(), color="coral", linestyle="--", linewidth=2, alpha=0.6)
ax.axvline(period_1951_2000.mean(), color="skyblue", linestyle="--", linewidth=2, alpha=0.6)

ax.set_xlabel("Happiness Score", fontsize=12, fontweight="bold")
ax.set_ylabel("Density", fontsize=12, fontweight="bold")
ax.set_title("Happiness Score Distribution by Period\n(Density plots with means)", fontsize=13, fontweight="bold")
ax.legend(fontsize=11, loc="upper right", framealpha=0.9)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "happiness_distribution_by_period.png", dpi=300, bbox_inches="tight")
print(f"Saved: happiness_distribution_by_period.png")
plt.close()

# =====================================================
# Box plots by period (highlight quartiles & outliers)
# =====================================================
fig, ax = plt.subplots(figsize=(10, 6))

data_to_plot = [period_1900_1950, period_1951_2000]
bp = ax.boxplot(data_to_plot, labels=["1900–1950", "1951–2000"], patch_artist=True,
                 widths=0.6, showmeans=True)

# Color the boxes
colors = ["coral", "skyblue"]
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel("Happiness Score", fontsize=12, fontweight="bold")
ax.set_title("Happiness Score Distribution by Period\n(Box plot comparison)", fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "happiness_boxplot_by_period.png", dpi=300, bbox_inches="tight")
print(f"Saved: happiness_boxplot_by_period.png")
plt.close()

plt.close()

# =====================================================
# Trend plot: Happiness by decade
# =====================================================
fig, ax = plt.subplots(figsize=(12, 6))

# Create decade bins
df["decade"] = (df["objectBeginDate"] // 10 * 10).astype(int)

# Calculate mean happiness per decade
decade_stats = df.dropna(subset=["happiness_score"]).groupby("decade")["happiness_score"].agg(
    mean="mean",
    std="std",
    count="count"
).reset_index()

# Remove decades with very few samples (optional, e.g., < 5)
decade_stats = decade_stats[decade_stats["count"] >= 5]

# Scatter plot of means
ax.scatter(decade_stats["decade"], decade_stats["mean"], s=120, color="coral", 
           alpha=0.7, edgecolors="black", linewidth=1.5, zorder=3, label="Mean happiness per decade")

# Add error bars (standard deviation)
ax.errorbar(decade_stats["decade"], decade_stats["mean"], yerr=decade_stats["std"], 
            fmt="none", ecolor="coral", alpha=0.3, capsize=5, capthick=1.5)

# Trend line (polyfit)
if len(decade_stats) > 1:
    z = np.polyfit(decade_stats["decade"], decade_stats["mean"], 1)
    p = np.poly1d(z)
    decade_range = np.linspace(decade_stats["decade"].min(), decade_stats["decade"].max(), 100)
    ax.plot(decade_range, p(decade_range), "r--", linewidth=2.5, alpha=0.7, label="Trend line")

ax.set_xlabel("Decade", fontsize=12, fontweight="bold")
ax.set_ylabel("Mean Happiness Score", fontsize=12, fontweight="bold")
ax.set_title("Emotional Language Trends in Met Photograph Titles by Decade (1900–2000)", 
             fontsize=13, fontweight="bold")
ax.grid(alpha=0.3)
ax.legend(fontsize=11, loc="best")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "happiness_trend_by_decade.png", dpi=300, bbox_inches="tight")
print(f"Saved: happiness_trend_by_decade.png")
plt.close()

# =====================================================
# Trend plot: Happiness by year
# =====================================================
fig, ax = plt.subplots(figsize=(12, 6))

# Use objectBeginDate as the year
df_trend = df.dropna(subset=["happiness_score", "objectBeginDate"]).copy()
df_trend["year"] = df_trend["objectBeginDate"].astype(int)

# Calculate mean happiness per year
year_stats = df_trend.groupby("year")["happiness_score"].agg(
    mean="mean",
    std="std",
    count="count"
).reset_index()

# Remove years with very few samples (optional, e.g., < 3)
year_stats = year_stats[year_stats["count"] >= 3]

# Scatter plot of means
ax.scatter(year_stats["year"], year_stats["mean"], s=80, color="steelblue", 
           alpha=0.6, edgecolors="black", linewidth=1, zorder=3, label="Mean happiness per year")

# Add error bars (standard deviation)
ax.errorbar(year_stats["year"], year_stats["mean"], yerr=year_stats["std"], 
            fmt="none", ecolor="steelblue", alpha=0.2, capsize=4, capthick=1)

# Trend line (polyfit)
if len(year_stats) > 1:
    z = np.polyfit(year_stats["year"], year_stats["mean"], 1)
    p = np.poly1d(z)
    year_range = np.linspace(year_stats["year"].min(), year_stats["year"].max(), 100)
    ax.plot(year_range, p(year_range), "r--", linewidth=2.5, alpha=0.7, label="Trend line")

ax.set_xlabel("Year", fontsize=12, fontweight="bold")
ax.set_ylabel("Mean Happiness Score", fontsize=12, fontweight="bold")
ax.set_title("Emotional Language Trends in Met Photograph Titles (1900–2000)", 
             fontsize=13, fontweight="bold")
ax.grid(alpha=0.3)
ax.legend(fontsize=11, loc="best")

plt.tight_layout()
plt.savefig(FIGURES_DIR / "happiness_trend_by_year.png", dpi=300, bbox_inches="tight")
print(f"Saved: happiness_trend_by_year.png")
plt.close()

print("\nVisualization complete!")

