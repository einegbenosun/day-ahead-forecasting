import pandas as pd
import pathlib as path
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score




#https://stackoverflow.com/questions/32470543/open-file-in-another-directory-python
csv_path = path.Path(__file__).parents[1] / "ingestion" / "csv" / "merged_data.csv"
df = pd.read_csv(csv_path,sep=",")

target_variable ="cams_ghi"

actual = df[target_variable]
predicted = df[target_variable].shift(24)

actual = actual.iloc[24:]
predicted = predicted.iloc[24:]


X_train, X_test, y_train, y_test = train_test_split(actual, predicted, test_size=0.2)

rmse = root_mean_squared_error(y_test, X_test)
mae = mean_absolute_error(y_test, X_test)
print(f"RMSE: {rmse}\n")
print(f"MAE: {mae}\n")

print(f"R-squared score(TEST): {r2_score(X_test, y_test)}")
print(f"R-squared score(TRAIN): {r2_score(X_train, y_train)}\n")
