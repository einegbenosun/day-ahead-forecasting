import pandas as pd
import pathlib as path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot
from sklearn.model_selection import TimeSeriesSplit, cross_validate
from baseline import compute_baseline_metrics, skill_score

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

#https://stats.stackexchange.com/questions/568897/random-forest-regressor-accuracy-reduces-when-the-input-data-is-not-shuffled
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)
tscv = TimeSeriesSplit(n_splits=5)
model = RandomForestRegressor(random_state=42, max_depth=10)



model.fit(X_train, y_train)
print("Random Forest Model Training")
print("------------------------")

#https://stackoverflow.com/questions/17197492/is-there-a-library-function-for-root-mean-square-error-rmse-in-python
rmse = root_mean_squared_error(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))

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
print(f"R² mean ± std: {cv_r2.mean():.4f}W/m² ± {cv_r2.std():.4f}W/m²")
print("RMSE per fold:", cv_rmse)
print(f"RMSE mean ± std: {cv_rmse.mean():.2f}W/m ± {cv_rmse.std():.2f}W/m")
print("MAE per fold:", cv_mae)
print(f"MAE mean ± std: {cv_mae.mean():.2f}W/m ± {cv_mae.std():.2f}\nW/m")

nrmse = (rmse / y_test.max()) * 100
print(f"RMSE: {rmse}W/m")
print(f"nRMSE: {nrmse:.2f}%")
print(f"MAE: {mae}W/m")
baseline_rmse, baseline_mae, baseline_r2_train, baseline_r2_test, baseline_nrmse = compute_baseline_metrics()
rfskill_rmse= skill_score(rmse, baseline_rmse)
rfskill_mae = skill_score(mae, baseline_mae)

print(f"Skill Score:\n RMSE = {rfskill_rmse}W/m\n MAE = {rfskill_mae}W/m")
joblib.dump(model, "models/random_forest_model.joblib")


#https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
#importance = pd.Series(
    #model.feature_importances_,
    #index=features.columns
#).sort_values()

#importance.plot(kind="barh", figsize=(9, 6), title="RandomForest Feature Importances")

#pyplot.xlabel("Importance")
#pyplot.tight_layout()
#pyplot.show()