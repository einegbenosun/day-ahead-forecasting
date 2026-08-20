import pandas as pd
import pathlib as path
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score




#https://stackoverflow.com/questions/32470543/open-file-in-another-directory-python
csv_path = path.Path(__file__).parents[1] / "ingestion" / "csv" / "merged_data.csv"
df = pd.read_csv(csv_path,sep=",")

def compute_baseline_metrics():
    target_variable ="cams_ghi"

    actual = df[target_variable]
    predicted = df[target_variable].shift(24)

    actual = actual.iloc[24:]
    predicted = predicted.iloc[24:]


    X_train, X_test, y_train, y_test = train_test_split(actual, predicted, test_size=0.2, random_state=42)

    rmse = root_mean_squared_error(y_test, X_test)
    mae = mean_absolute_error(y_test, X_test)
    r2_train = r2_score(X_train, y_train)
    r2_test = r2_score(X_test, y_test)
    return rmse, mae, r2_train, r2_test

def skill_score(rmse_model, rmse_baseline):
    return 1 - (rmse_model/rmse_baseline)

if __name__=="__main__":
    rmse, mae, r2_train, r2_test = compute_baseline_metrics()
    print(f"R-squared score(TEST): {r2_score(X_test, y_test)}")
    print(f"R-squared score(TRAIN): {r2_score(X_train, y_train)}\n")
    print(f"R-squared score(TEST): {r2_test}")
    print(f"R-squared score(TRAIN): {r2_train}")