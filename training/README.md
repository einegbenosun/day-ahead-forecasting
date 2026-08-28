# Model Training
Run both from the repository root:
```powershell
python training/randomforest.py
python training/trainxgboost.py
```

`randomforest.py` and `trainxgboost.py` train the Random Forest and XGBoost GHI models and save them automatically to `models/random_forest_model.joblib` and `models/xgboost_model.joblib`.

Both use a fixed `random_state`, so retraining on unchanged data reproduces equivalent results. Retraining overwrites the `models/*.joblib` files used by the Flask API — rebuild the `main` container (`docker compose up -d --build`) for it to pick up the new files.

`baseline.py` computes a persistence-model baseline used for the skill-score printed by each of the scripts above, and doesn't need to be run on its own.
