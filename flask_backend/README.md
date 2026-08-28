# Backend API and Deployment

## Services

The backend is two separate Flask services, run together via [`docker-compose.yml`](../docker-compose.yml):

| Service | File | Port | Role |
|---|---|---|---|
| `main` | [`main.py`](main.py) | 5000 | Serves GHI predictions from the trained ML models |
| `api` | [`api.py`](api.py) | 5001 | Runs the physics pipeline, serves the forecast to the frontend |
| `frontend` | [`pv-forecast/`](../pv-forecast/) | 5173 | React dashboard |

`api` depends on `main` (calls it internally at `http://main:5000/rfpredict` ); `frontend` depends on `api`.

## `main.py` routes

- `POST /rfpredict` - Random Forest GHI prediction
- `POST /xgbpredict` - XGBoost GHI prediction

Both take a JSON body of the required features and return a single predicted GHI value and are loaded with `joblib`, predicting on a **Python list**.

## `api.py` routes

- `GET /date` - the forecast's date
- `GET /params` - the location parameters used for the Open-Meteo request, plus a `pv_config` block (altitude, panel tilt/azimuth, capacity, temperature coefficient, pvwatts system loss)
- `GET /predict` - 24 hourly AC power predictions (watts), from `get_final_power()`
- `GET /total` - sum of the 24 hourly values (kWh downstream, in the frontend)
