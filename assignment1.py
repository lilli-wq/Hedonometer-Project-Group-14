#1.1
import pandas as pd

df = pd.read_csv("Data_Set_S1.txt", sep="\t", comment = "#", na_values="--")
df["column_name"] = pd.to_numeric(df["column_name"])
print (df.shape)