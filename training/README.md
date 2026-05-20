# Model Training
To use the Random Forest model in in the Flask API, remove the comment(#) from line 51 in `randomforest.py`
- `joblib.dump(model, "random_forest_model.joblib")`

To use the XGBoost model in the Flask API, remove the comment(#) from line 45 in `trainxgboost.py`
- `joblib.dump(model, "random_forest_model.joblib")`

This will create joblib files for both models that should be replaced in `flask_backend/models'
