import pandas as pd
import pathlib as path
import joblib 
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from matplotlib import pyplot
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit, cross_validate
from baseline import skill_score, compute_baseline_metrics

#https://stackoverflow.com/questions/32470543/open-file-in-another-directory-python
csv_path = path.Path(__file__).parents[1] / "ingestion" / "csv" / "merged_data.csv"
df = pd.read_csv(csv_path,sep=",")

target_variable ="cams_ghi"

#df["lagged_cams"] = df["cams_ghi"].shift(24)
from_cams = [target_variable,"cams_bhi", "cams_dhi", "cams_bni", "cams_reliability"]
target = df[target_variable]
directly_relevant_features = ["diffuse_radiation"]
noise = ["YEAR","is_day"]
features = df.drop(columns= from_cams + directly_relevant_features + noise)
#features = features.iloc[24:]
#target = target.iloc[24:]
#print(features.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=.2, shuffle=False)
#https://www.kaggle.com/code/prashant111/a-guide-on-xgboost-hyperparameters-tuning
model = XGBRegressor(random_state=42, n_estimators=1500, learning_rate=0.008, max_depth=5, alpha=6)
tscv = TimeSeriesSplit(n_splits=5)


model.fit(X_train, y_train)
# make predictions

print("XGBoost Model Training")
print("------------------------")
rmse = root_mean_squared_error(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))

#print(f"Root Mean Squared Error: {rmse}")
#print(f"Mean Absolute Error: {mae}")
print(f"R²(TEST): {model.score(X_test, y_test)}")
print(f"R²(TRAIN): {model.score(X_train, y_train)}\n")

feature_importance = []
feature_importance.append(model.feature_importances_)
print("Feature importance:")
for i in features.columns.tolist():
    print(f"{features[i].name}: {feature_importance[0][features.columns.get_loc(i)]}")

cv_results = cross_validate(
    model, features, target, cv=tscv,
    scoring=["r2", "neg_root_mean_squared_error", "neg_mean_absolute_error"]
)
cv_r2 = cv_results["test_r2"]
cv_rmse = -cv_results["test_neg_root_mean_squared_error"]
cv_mae = -cv_results["test_neg_mean_absolute_error"]

print("\nR² per fold:", cv_r2)
print(f"R² mean ± std: {cv_r2.mean():.4f} ± {cv_r2.std():.4f}")
print("RMSE per fold:", cv_rmse)
print(f"RMSE mean ± std: {cv_rmse.mean():.2f}W/m² ± {cv_rmse.std():.2f}W/m²")
print("MAE per fold:", cv_mae)
print(f"MAE mean ± std: {cv_mae.mean():.2f}W/m² ± {cv_mae.std():.2f}W/m²\n")

nrmse = (rmse / y_test.max()) * 100
print(f"RMSE: {rmse}W/m²")
print(f"nRMSE: {nrmse:.2f}%")
print(f"MAE: {mae}W/m²")

baseline_rmse, baseline_mae, baseline_r2_train, baseline_r2_test, baseline_nrmse = compute_baseline_metrics()
xgskill_rmse= skill_score(rmse, baseline_rmse)
xgskill_mae = skill_score(mae, baseline_mae)

print(f"Skill Score:\nRMSE = {xgskill_rmse}\nMAE = {xgskill_mae}")


model_path = path.Path(__file__).parents[1] / "models"
joblib.dump(model, model_path / "xgboost_model.joblib")

#importance = pd.Series(
#    model.feature_importances_,
#    index=features.columns
#).sort_values()

#importance.plot(kind="barh", figsize=(9, 6), title="XGBoost Feature Importances")

#pyplot.xlabel("Importance")
#pyplot.tight_layout()
#pyplot.show()