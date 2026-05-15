import csv
import pandas as pd
import pathlib as path

df_path = path.Path(__file__).with_name("merged_data.csv")
df = pd.read_csv(df_path)

print(df.head())
