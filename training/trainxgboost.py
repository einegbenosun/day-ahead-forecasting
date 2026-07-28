import pandas as pd
import pathlib as path
import joblib 
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from matplotlib import pyplot
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error

csv_path = path.Path(__file__).with_name("ingestion/csv/merged_data.csv")
df = pd.read_csv(csv_path,sep=",")

target_variable ="cams_ghi"
from_cams = [target_variable,"cams_bhi", "cams_dhi", "cams_bni", "cams_reliability"]
target = df[target_variable]
directly_relevant_features = ["diffuse_radiation"]
#relevant_features = ["DAY","YEAR","is_day","direct_radiation","shortwave_radiation","diffuse_radiation","direct_normal_irradiance","global_tilted_irradiance","shortwave_radiation"]
noise = ["YEAR","is_day","DAY"]
features = df.drop(columns= from_cams + directly_relevant_features + noise)

print(features.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=.2, random_state=100, shuffle=False)
#https://www.kaggle.com/code/prashant111/a-guide-on-xgboost-hyperparameters-tuning
model = XGBRegressor(n_estimators=1500, learning_rate=0.008, max_depth=5, alpha=6)
model.fit(X_train, y_train)
# make predictions


print(f"R-squared score(TEST): {model.score(X_test, y_test)}")
print(f"R-squared score(TRAIN): {model.score(X_train, y_train)}\n")
rmse = root_mean_squared_error(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))

#print(f"Root Mean Squared Error: {rmse}")
#print(f"Mean Absolute Error: {mae}")
feature_importance = []
feature_importance.append(model.feature_importances_)
print(f"RMSE: {rmse}\n")
print(f"MAE: {mae}\n")
print("Feature importance:")
for i in features.columns.tolist():
    print(f"{features[i].name}: {feature_importance[0][features.columns.get_loc(i)]}")

#joblib.dump(model, "xgboost_model.joblib")

importance = pd.Series(
    model.feature_importances_,
    index=features.columns
).sort_values()

importance.plot(kind="barh", figsize=(9, 6), title="XGBoost Feature Importances")

pyplot.xlabel("Importance")
pyplot.tight_layout()
pyplot.show()