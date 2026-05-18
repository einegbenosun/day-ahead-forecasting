import pandas as pd
import pathlib as path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot



csv_path = path.Path(__file__).with_name("merged_data.csv")
df = pd.read_csv(csv_path,sep=",")


target_variable ="cams_ghi"
from_cams = [target_variable,"cams_bhi", "cams_dhi", "cams_bni", "cams_reliability"]
target = df[target_variable]
directly_relevant_features = ["diffuse_radiation"]
relevant_features = ["DAY","YEAR","is_day","direct_radiation","shortwave_radiation","diffuse_radiation","direct_normal_irradiance","global_tilted_irradiance","shortwave_radiation"]
noise = ["YEAR","is_day","DAY"]
features = df.drop(columns= from_cams + directly_relevant_features + noise)

print(features.columns.tolist())

x = features
y = target

#https://stats.stackexchange.com/questions/568897/random-forest-regressor-accuracy-reduces-when-the-input-data-is-not-shuffled
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=100, shuffle=False)
model = RandomForestRegressor()

#https://stackoverflow.com/questions/17197492/is-there-a-library-function-for-root-mean-square-error-rmse-in-python

model.fit(X_train, y_train)

#https://stackoverflow.com/questions/17197492/is-there-a-library-function-for-root-mean-square-error-rmse-in-python
rmse = root_mean_squared_error(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))

print(f"R-squared score(TEST): {model.score(X_test, y_test)}")
print(f"R-squared score(TRAIN): {model.score(X_train, y_train)}\n")
print(f"RMSE: {rmse}\n")
print(f"MAE: {mae}\n")
feature_importance = []
feature_importance.append(model.feature_importances_)
print("Feature importance:")
for i in features.columns.tolist():
    print(f"{features[i].name}: {feature_importance[0][features.columns.get_loc(i)]}")

#joblib.dump(model, "random_forest_model.joblib")


#https://scikit-learn.org/stable/auto_examples/inspection/plot_permutation_importance.html
importance = pd.Series(
    model.feature_importances_,
    index=features.columns
).sort_values()

#importance.plot(kind="barh", figsize=(9, 6), title="RandomForest Feature Importances")

#pyplot.xlabel("Importance")
#pyplot.tight_layout()
#pyplot.show()