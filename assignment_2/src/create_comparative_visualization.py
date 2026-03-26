from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AMERICA_FILE = ROOT / "data" / "processed" / "calculated_scores_America.csv"
EUROPE_FILE = ROOT / "data" / "processed" / "calculated_scores_Europe.csv"
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

# Load data
df_america = pd.read_csv(AMERICA_FILE)
df_europe = pd.read_csv(EUROPE_FILE)

# Add region column
df_america["region"] = "American"
df_europe["region"] = "European"

# Combine datasets
df_combined = pd.concat([df_america, df_europe], ignore_index=True)
df_combined = df_combined.dropna(subset=["happiness_score"])

print("Loaded combined dataset.")
print(f"Total artworks: {len(df_combined)}")

# ============================================================================
# Visualization 1: Grouped Bar Chart - Mean Happiness by Region and Period
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Calculate means for each group
grouped_means = df_combined.groupby(["region", "period"])["happiness_score"].mean().unstack()

x = np.arange(len(grouped_means.index))
width = 0.35

bars1 = ax.bar(x - width/2, grouped_means["1900-1950"], width, label="1900–1950", 
               color="coral", alpha=0.85, edgecolor="black", linewidth=1.5)
bars2 = ax.bar(x + width/2, grouped_means["1951-2000"], width, label="1951–2000",
               color="skyblue", alpha=0.85, edgecolor="black", linewidth=1.5)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel("Mean Happiness Score", fontsize=12, fontweight="bold")
ax.set_title("Mean Happiness Scores: American vs European Photographs\nby Time Period", 
             fontsize=14, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(grouped_means.index, fontsize=11)
ax.legend(fontsize=11, loc="upper right")
ax.grid(axis="y", alpha=0.3)
ax.set_ylim([0, 7])

plt.tight_layout()
plt.savefig(FIGURES_DIR / "comparison_mean_happiness_all_groups.png", dpi=300, bbox_inches="tight")
print("Saved: comparison_mean_happiness_all_groups.png")
plt.close()


# ============================================================================
# Visualization 2: Grouped Density Plots - All 4 Groups Overlay
# ============================================================================

fig, ax = plt.subplots(figsize=(13, 7))

colors_map = {
    ("American", "1900-1950"): ("coral", "--"),
    ("American", "1951-2000"): ("darkred", "-"),
    ("European", "1900-1950"): ("lightblue", "--"),
    ("European", "1951-2000"): ("darkblue", "-"),
}

labels_map = {
    ("American", "1900-1950"): "American 1900–1950",
    ("American", "1951-2000"): "American 1951–2000",
    ("European", "1900-1950"): "European 1900–1950",
    ("European", "1951-2000"): "European 1951–2000",
}

# Plot density for each group
for (region, period), (color, linestyle) in colors_map.items():
    data = df_combined[(df_combined["region"] == region) & (df_combined["period"] == period)]["happiness_score"]
    mean_val = data.mean()
    data.plot(kind="density", ax=ax, color=color, linewidth=2.5, linestyle=linestyle,
              label=f"{labels_map[(region, period)]} (μ={mean_val:.2f})", alpha=0.8)
    # Add vertical line for mean
    ax.axvline(mean_val, color=color, linestyle=linestyle, linewidth=1.5, alpha=0.4)

ax.set_xlabel("Happiness Score", fontsize=12, fontweight="bold")
ax.set_ylabel("Density", fontsize=12, fontweight="bold")
ax.set_title("Happiness Score Density Distributions\nAmerican vs European Photographs (1900–1950 vs 1951–2000)",
             fontsize=14, fontweight="bold")
ax.legend(fontsize=10, loc="upper right", framealpha=0.95)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "comparison_density_all_groups.png", dpi=300, bbox_inches="tight")
print("Saved: comparison_density_all_groups.png")
plt.close()


# ============================================================================
# Visualization 3: Side-by-Side Box Plots - All 4 Groups
# ============================================================================

fig, ax = plt.subplots(figsize=(13, 7))

# Prepare data for box plot
data_boxplot = [
    df_combined[(df_combined["region"] == "American") & (df_combined["period"] == "1900-1950")]["happiness_score"],
    df_combined[(df_combined["region"] == "American") & (df_combined["period"] == "1951-2000")]["happiness_score"],
    df_combined[(df_combined["region"] == "European") & (df_combined["period"] == "1900-1950")]["happiness_score"],
    df_combined[(df_combined["region"] == "European") & (df_combined["period"] == "1951-2000")]["happiness_score"],
]

labels_box = ["American\n1900–1950", "American\n1951–2000", "European\n1900–1950", "European\n1951–2000"]
colors_box = ["coral", "darkred", "lightblue", "darkblue"]

bp = ax.boxplot(data_boxplot, tick_labels=labels_box, patch_artist=True, widths=0.6, 
                 showmeans=True, meanline=False)

# Color the boxes
for patch, color in zip(bp["boxes"], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_linewidth(1.5)

# Style the other elements
for element in ["whiskers", "fliers", "means", "medians", "caps"]:
    plt.setp(bp[element], color="black", linewidth=1.5)

ax.set_ylabel("Happiness Score", fontsize=12, fontweight="bold")
ax.set_title("Happiness Score Distributions: Box Plot Comparison\nAmerican vs European Photographs (1900–1950 vs 1951–2000)",
             fontsize=14, fontweight="bold")
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "comparison_boxplot_all_groups.png", dpi=300, bbox_inches="tight")
print("Saved: comparison_boxplot_all_groups.png")
plt.close()


# ============================================================================
# Visualization 4: 2x2 Subplots - Detailed Comparison
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Comprehensive Comparison: American vs European Photographs\n1900–1950 vs 1951–2000",
             fontsize=15, fontweight="bold", y=1.00)

# American 1900-1950
ax = axes[0, 0]
data = df_combined[(df_combined["region"] == "American") & (df_combined["period"] == "1900-1950")]["happiness_score"]
ax.hist(data, bins=25, color="coral", edgecolor="black", alpha=0.7)
ax.axvline(data.mean(), color="darkred", linestyle="--", linewidth=2.5, label=f"Mean: {data.mean():.2f}")
ax.set_xlabel("Happiness Score", fontsize=10, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=10, fontweight="bold")
ax.set_title("American 1900–1950 (n={})".format(len(data)), fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)

# American 1951-2000
ax = axes[0, 1]
data = df_combined[(df_combined["region"] == "American") & (df_combined["period"] == "1951-2000")]["happiness_score"]
ax.hist(data, bins=25, color="darkred", edgecolor="black", alpha=0.7)
ax.axvline(data.mean(), color="coral", linestyle="--", linewidth=2.5, label=f"Mean: {data.mean():.2f}")
ax.set_xlabel("Happiness Score", fontsize=10, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=10, fontweight="bold")
ax.set_title("American 1951–2000 (n={})".format(len(data)), fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)

# European 1900-1950
ax = axes[1, 0]
data = df_combined[(df_combined["region"] == "European") & (df_combined["period"] == "1900-1950")]["happiness_score"]
ax.hist(data, bins=25, color="lightblue", edgecolor="black", alpha=0.7)
ax.axvline(data.mean(), color="darkblue", linestyle="--", linewidth=2.5, label=f"Mean: {data.mean():.2f}")
ax.set_xlabel("Happiness Score", fontsize=10, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=10, fontweight="bold")
ax.set_title("European 1900–1950 (n={})".format(len(data)), fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)

# European 1951-2000
ax = axes[1, 1]
data = df_combined[(df_combined["region"] == "European") & (df_combined["period"] == "1951-2000")]["happiness_score"]
ax.hist(data, bins=25, color="darkblue", edgecolor="black", alpha=0.7)
ax.axvline(data.mean(), color="lightblue", linestyle="--", linewidth=2.5, label=f"Mean: {data.mean():.2f}")
ax.set_xlabel("Happiness Score", fontsize=10, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=10, fontweight="bold")
ax.set_title("European 1951–2000 (n={})".format(len(data)), fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "comparison_subplots_2x2_all_groups.png", dpi=300, bbox_inches="tight")
print("Saved: comparison_subplots_2x2_all_groups.png")
plt.close()

print("\nAll comparative visualizations generated successfully!")
