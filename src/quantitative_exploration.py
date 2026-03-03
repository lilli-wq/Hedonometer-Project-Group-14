import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path



ROOT = Path.cwd() 
DATA_PATH = ROOT / "Data_Set_S1.txt"
df = pd.read_csv(DATA_PATH, sep='\t', skiprows=3, na_values=["--"])
df.columns = [col.lower() for col in df.columns]
                
# Convert rank columns to numeric, replacing '--' with NaN
cols_to_fix = ['twitter_rank', 'google_rank', 'nyt_rank', 'lyrics_rank']
for col in cols_to_fix:
    df[col] = pd.to_numeric(df[col].replace('--', np.nan))
print(df.head())

#Histogram of happiness average scores
plt.figure(figsize=(10, 6))
sns.histplot(df['happiness_average'], bins=30, kde=True, color='skyblue')
plt.title('Distribution of Happiness Average Scores')
plt.xlabel('Happiness Score')
plt.ylabel('Frequency')
plt.show()

#Boxplot of happiness average scores
stats = {'Mean': df['happiness_average'].mean(),
'Median': df['happiness_average'].median(), 
'Std Dev': df['happiness_average'].std(), 
'5th Percentile': df['happiness_average'].quantile(0.05), 
'95th Percentile': df['happiness_average'].quantile(0.95)}
print(pd.Series(stats))

# 1. scatter plot of happiness average vs. standard deviation to visualize disagreement
plt.figure(figsize=(10, 6))
plt.scatter(df['happiness_average'], df['happiness_standard_deviation'], alpha=0.3, s=10)
plt.title('Happiness Average vs. Standard Deviation')
plt.xlabel('Average Happiness')
plt.ylabel('Standard Deviation (Disagreement)')
plt.show()

# 2. Identify words with the highest disagreement (highest standard deviation)
top_disputed = df.nlargest(15, 'happiness_standard_deviation')[['word', 'happiness_average', 'happiness_standard_deviation']]
print("15 Words with Highest Disagreement:")
print(top_disputed)

# calculate how many words from the labMT list are found in each corpus (i.e., have a non-NaN rank)
corpora_cols = ['twitter_rank', 'google_rank', 'nyt_rank', 'lyrics_rank']

# 1. create a matrix to store the counts of shared words between each pair of corpora
size = len(corpora_cols)
overlap_matrix = np.zeros((size, size))

for i in range(size):
    for j in range(size):
        col1 = corpora_cols[i]
        col2 = corpora_cols[j]
        # count how many words have non-NaN ranks in both corpora (i.e., are shared)
        common_count = df[df[col1].notna() & df[col2].notna()].shape[0]
        overlap_matrix[i, j] = common_count

# create a DataFrame for the heatmap, using the corpus names as labels
overlap_df = pd.DataFrame(
    overlap_matrix, 
    index=[c.replace('_rank', '').upper() for c in corpora_cols],
    columns=[c.replace('_rank', '').upper() for c in corpora_cols]
)
# 2. visualize the overlap using a heatmap
plt.figure(figsize=(10, 8))

sns.heatmap(overlap_df, annot=True, fmt=".0f", cmap='YlGnBu', cbar_kws={'label': 'Number of Shared Words'})

plt.title('2.3 Overlap of Common Words (Top 5000) Between Corpora')
plt.show()


twitter_unique = df[(df['twitter_rank'] <= 1000) & (df['nyt_rank'].isna())]

print("Words in Twitter's top 1000 that are not in NYT's top 5000:")
if not twitter_unique.empty:
   
    print(twitter_unique[['word', 'twitter_rank']].sort_values('twitter_rank').head(10))
    #1g