import pandas as pd
import pathlib as path
from sklearn.model_selection import train_test_split
from xgboost 

from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import mean_absolute_error

csv_path = path.Path(__file__).with_name("merged_data.csv")
df = pd.read_csv(csv_path,sep=",")

target_variable ="cams_ghi"
from_cams = [target_variable,"cams_bhi", "cams_dhi", "cams_bni", "cams_reliability"]
target = df[target_variable]
directly_relevant_features = ["shortwave_radiation","global_tilted_irradiance"]
relevant_features = ["is_day","YEAR","direct_radiation","shortwave_radiation","diffuse_radiation","direct_normal_irradiance","global_tilted_irradiance","shortwave_radiation"]
noise = ["DAY","YEAR"]
features = df.drop(columns= directly_relevant_features + from_cams + noise)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=.2, random_state=100, shuffle=False)
model = XGBRegressor()

model.fit(X_train, y_train)
# make predictions


print(f"R-squared score(TEST): {model.score(X_test, y_test)}")
print(f"R-squared score(TRAIN): {model.score(X_train, y_train)}\n")
rmse = root_mean_squared_error(y_test, model.predict(X_test))
mae = mean_absolute_error(y_test, model.predict(X_test))
