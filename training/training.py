import csv
import pandas as pd
import pathlib as path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
import numpy as np



df_path = path.Path(__file__).with_name("merged_data.csv")
df = pd.read_csv(df_path)

pv_target = df["cams_ghi"]

X_train, X_test, y_train, y_test = train_test_split(df.drop(["cams_ghi"], axis="columns"),pv_target, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))

