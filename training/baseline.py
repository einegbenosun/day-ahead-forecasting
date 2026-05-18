import pandas as pd
import pathlib as path
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score





csv_path = path.Path(__file__).with_name("merged_data.csv")
df = pd.read_csv(csv_path,sep=",")


next_day = []
for i in range(1, 25):
    next_day.append(i)
df_pred = pd.read_csv(csv_path,sep="," , skiprows=next_day)

target_variable ="cams_ghi"
target = df[target_variable]
target = target.drop(index=target.index[-25:-1])
features = df_pred[target_variable]

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)
rmse = root_mean_squared_error(y_test, X_test)
mae = mean_absolute_error(y_test, X_test)
print(f"RMSE: {rmse}\n")
print(f"MAE: {mae}\n")

print(f"R-squared score(TEST): {r2_score(X_test, y_test)}")
print(f"R-squared score(TRAIN): {r2_score(X_train, y_train)}\n")

print(df_pred.head())
print(df.head())
