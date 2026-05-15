from pathlib import Path
import pandas as pd
import csv

csv_path = Path(__file__).with_name("cams.csv")
df = pd.read_csv(csv_path,sep=";",comment="#")


#useful columns: Observation Period, GHI, BHI, DHI, BNI, RELIABILITY
clean_cams_df = df[["Observation period", "GHI", "BHI", "DHI", "BNI", "Reliability"]]
clean_cams_df = clean_cams_df.rename(columns={"Observation period": "timestamp",
                                                "GHI": "cams_ghi",
                                                "BHI": "cams_bhi",
                                                "DHI": "cams_dhi",
                                                "BNI": "cams_bni",
                                                "Reliability": "cams_reliability"})
#removing second half of the timestamp and replacing it with ":00" to match openmeteo timestamp format
clean_cams_df["timestamp"] = clean_cams_df["timestamp"].str.split("/").str[0]
clean_cams_df["timestamp"] = clean_cams_df["timestamp"].str.split(":").str[0] + ":00"
clean_cams_df.to_csv("cams_cleaned.csv", index=False)
print((clean_cams_df.columns.tolist()))
