from genericpath import isfile

import pandas as pd
from pathlib import Path
import csv 
from datetime import datetime


cams_path = Path(__file__).with_name("cams_cleaned.csv")
cams_df = pd.read_csv(cams_path)


open_meteo_path = Path(__file__).with_name("open_meteo_cleaned.csv")
open_meteo_df = pd.read_csv(open_meteo_path)

merged_df = pd.merge(open_meteo_df, cams_df, on="timestamp", how="inner")

#https://www.geeksforgeeks.org/pandas/python-pandas-split-strings-into-two-list-columns-using-str-split/
split = merged_df["timestamp"].str.split("T", n=1, expand=True)

merged_df["Hour"] = split[1].str.split(":").str[0]
merged_df["Date"] = split[0]
merged_df["Date"] = pd.to_datetime(merged_df["Date"])
merged_df = merged_df.drop(columns=["timestamp"])

#https://stackoverflow.com/questions/77881238/using-datetime-in-machine-learning
merged_df['YEAR'] = merged_df['Date'].dt.year
merged_df['MONTH'] = merged_df['Date'].dt.month
merged_df['DAY'] = merged_df['Date'].dt.day
merged_df = merged_df.drop(columns=["Date"])



#https://stackoverflow.com/questions/74817120/convert-object-to-int-pandas-dataframe
merged_df["Hour"] = pd.to_numeric(merged_df["Hour"], errors="coerce")
#merged_df = pd.read_csv(merged_df, parse_dates=["timestamp"])


print(merged_df.info())
merged_df.to_csv("merged_data.csv", index=False)

