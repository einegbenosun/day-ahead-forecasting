import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("training/models/xgboost_model.joblib", "rb") as f:
    xgb_model = joblib.load(f)

with open("training/models/random_forest_model.joblib", "rb") as f:
    rf_model = joblib.load(f)


#https://www.youtube.com/watch?v=MvTqi2Mb_PM
@app.route("/")
def home():
    return "Photovoltaic Day-Ahead Forecasting API"


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()
        required_features = ['temperature_2m', 'relative_humidity_2m', 'wind_speed_10m', 'shortwave_radiation', 'direct_radiation', 'direct_normal_irradiance', 'diffuse_radiation', 'global_tilted_irradiance', 'is_day', 'sunshine_duration', 'Hour', 'YEAR', 'MONTH', 'DAY']

        input_data = [data[i] for i in required_features]
        
        #Invalid/No data
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        #For valid data
        if not all(feature in data for feature in required_features):
            return jsonify({"error": "Missing required features"}), 400
        
        xgb_prediction = xgb_model.predict([input_data])
        rf_prediction = rf_model.predict([input_data])

        response = {
            "xgboost_prediction": xgb_prediction[0],
            "random_forest_prediction": rf_prediction[0]
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
    