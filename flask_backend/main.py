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


@app.route("/xgbpredict", methods=["POST"])
def xgbpredict():

    try:
        request_data = request.get_json()
        required_features = {'temperature_2m',
                            'relative_humidity_2m',
                            'wind_speed_10m',
                            'shortwave_radiation',
                            'direct_radiation',
                            'direct_normal_irradiance',
                            'global_tilted_irradiance',
                            'sunshine_duration',
                            'Hour',
                            'MONTH'}


        input_data = [[request_data[feature] for feature in required_features]]
        #Invalid/No data
        if not required_features:
            return jsonify({"error": "No input data provided"}), 400
        
        #For valid data
        if not all(feature in required_features for feature in required_features):
            return jsonify({"error": "Missing required features"}), 400
        
        xgb_prediction = xgb_model.predict(input_data)
        if xgb_prediction < 0:
            xgb_prediction = float(0)

#avoid negative values by setting 0 for no shortwave radiation
        prediction = float(xgb_prediction[0])
        if request_data["shortwave_radiation"] <= 0:
            prediction = float(0)

        response = float(prediction)

        return jsonify(response), 200
    
    

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/rfpredict", methods=["POST"])
def rfpredict():

    try:
        request_data = request.get_json()
        required_features = {'temperature_2m',
                            'relative_humidity_2m',
                            'wind_speed_10m',
                            'shortwave_radiation',
                            'direct_radiation',
                            'direct_normal_irradiance',
                            'global_tilted_irradiance',
                            'sunshine_duration',
                            'Hour',
                            'MONTH'}


        input_data = [[request_data[feature] for feature in required_features]]
        #Invalid/No data
        if not required_features:
            return jsonify({"error": "No input data provided"}), 400
        
        #For valid data
        if not all(feature in required_features for feature in required_features):
            return jsonify({"error": "Missing required features"}), 400
        
        rf_prediction = rf_model.predict(input_data)
        prediction = float(rf_prediction[0])
        if request_data["shortwave_radiation"] <= 0:
            prediction = float(0)

        response = float(prediction)

        return jsonify(response), 200
    
    

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
    