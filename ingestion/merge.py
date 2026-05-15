import pandas as pd
from pathlib import Path
import csv 


cams_path = Path(__file__).with_name("cams_cleaned.csv")
cams_df = pd.read_csv(cams_path)


open_meteo_path = Path(__file__).with_name("open_meteo_cleaned.csv")
open_meteo_df = pd.read_csv(open_meteo_path)

merged_df = pd.merge(open_meteo_df, cams_df, on="timestamp", how="inner")
merged_df.to_csv("merged_data.csv", index=False)