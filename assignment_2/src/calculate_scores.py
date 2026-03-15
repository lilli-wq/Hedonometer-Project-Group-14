import pandas as pd
import os

#1. define file paths
INPUT_FILE = 'assignment_2/data/cache/processed_photographs_titles.csv'

LABMT_FILE = 'assignment_2/data/Data_Set_S1.txt' 

OUTPUT_DIR = 'assignment_2/data/processed/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'met_with_scores.csv')

# 2.load labMT dictionary
print("loading labMT dictionary...")

labmt = pd.read_csv('assignment_2/data/Data_Set_S1.txt', 
                    sep='\t', 
                    skiprows=3, 
                    index_col=0)
def get_happiness_score(text):
    
    if pd.isna(text) or text == "":
        return None
    
    words = str(text).lower().split()
    scores = []
    
    for word in words:

        clean_word = word.strip('.,!?:;"()[]{}')
        
       
        if clean_word in labmt.index:
            
            score = labmt.loc[clean_word, 'happiness_average']
            scores.append(score)

    if len(scores) > 0:
        return sum(scores) / len(scores)
    else:
        return None

# 3.read input data and calculate scores
if not os.path.exists(INPUT_FILE):
    print(f"Error: File not found {INPUT_FILE}，！")
else:
    print(f"Reading data: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # check if 'title' column exists
    if 'title' not in df.columns:
        print(f"Error: Column 'title' not found. Available columns: {df.columns.tolist()}")
    else:
        # 4.calculate happiness scores
        print("Calculating happiness scores...")
        print("--checking data and dictionary--")
        print(f"Dictionary words: {labmt.index[:5].tolist()}")
        print(f"Dictionary columns: {labmt.columns.tolist()}")
        print(f"First title tokenized: {str(df['title'].iloc[0]).lower().split()}")
        print("----------------")

        df['happiness_score'] = df['title'].apply(get_happiness_score)
        
        # --- 5.save results ---
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"Created output directory: {OUTPUT_DIR}")
            
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Success! Scores saved to: {OUTPUT_FILE}")

        valid_scores = df['happiness_score'].notna().sum()
        print(f"Statistics: Total {len(df)} records, {valid_scores} successfully scored.")

