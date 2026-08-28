# Day-Ahead Solar PV Forecasting

This project is a day-ahead photovoltaic forecasting dashboard. It combines live Open-Meteo weather forecast data, a trained machine learning model, and a pvlib physics simulation to predict actual panel power output, and displays the results in a React frontend.

The ML model predicts irradiance (GHI), and a separate physics pipeline converts that irradiance into predicted power for the specific panel setup (tilt, azimuth, capacity, losses).

The project runs with Docker Compose and contains three services:

| Service | Description | Port|
|---|---|---|
| `main`| Flask ML API — Random Forest / XGBoost models predicting GHI (solar irradiance) | `5000`|
| `api`| Flask API that fetches Open-Meteo weather data, calls `main` for a GHI forecast, then runs a pvlib physics pipeline (sun position, tilt transposition, cell temperature, DC/AC conversion, system losses) to convert that GHI into predicted AC power| `5001`|
|`frontend`| React/Vite dashboard |`5173`|

```text
React Frontend
http://localhost:5173
        |
        v
Flask Request API(api.py)
http://localhost:5001

- fetches Open-Meteo weather
- calls Main API for GHI
- pvlib: GHI -> predicted AC power

        |
        v
Main Model Flask API(main.py)
http://localhost:5000

Random Forest / XGBoost predict GHI from weather
```

The React frontend sends requests to the Flask Request API on port `5001`.
The Request API fetches live Open-Meteo data, prepares the features, then sends those features to the Main Model API on port `5000`, which returns a predicted GHI (not a final power figure).
The Request API then runs that GHI through its pvlib physics pipeline to produce predicted AC power output.
The Request API returns the final power forecast back to React.

Key endpoints:
- `api` (`5001`): `/predict`, `/total`, `/date`, `/params`
- `main` (`5000`): `/rfpredict`, `/xgbpredict`

# Requirements
- Docker Desktop
https://www.docker.com/products/docker-desktop/

No manual setup required


# Run the Project
`docker compose up -d --build`
Then open the Frontend:
`http://localhost:5173`

# Changing Location/Dataset

The current system is configured for a fixed location using Open-Meteo forecast data and can be changed by updating the Open-Meteo latitude and longitude values.

For full instructions on replacing CAMS and Open Meteo data, preparing ingestion files and adapting  to a new location, see:
```text
ingestion/README.md
