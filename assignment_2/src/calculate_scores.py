import pandas as pd

# 1.
labmt = pd.read_csv('assignment_2/data/Data_Set_S1.txt', sep='\t', index_col=0)
# 

def get_happiness_score(text):
    if pd.isna(text):
        return None
    
    
    words = text.lower().split()
    scores = []
    
    for word in words:
        clean_word = word.strip('.,!?:;"()')
        
        
        if clean_word in labmt.index:
            score = labmt.loc[clean_word, 'happiness_average']
            scores.append(score)
    
    
    if len(scores) > 0:
        return sum(scores) / len(scores)
    else:
        return None 

# 2. read the cleaned dataset
df = pd.read_csv('assignment_2/data/processed/met_cleaned_data.csv')

# 3. calculate happiness scores for each title and add as a new column
df['happiness_score'] = df['title'].apply(get_happiness_score)

# 4. update the dataset with the new column and save it
df.to_csv('assignment_2/data/processed/met_with_scores.csv', index=False)