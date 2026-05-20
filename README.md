# Day-Ahead Solar PV Forecasting

This project is a day-ahead photovoltaic forecasting dashboard. It uses live Open-Meteo weather forecast data,sends the processed features to a trained machine learning model API, and displays the forecast results in a React frontend.

The project runs with Docker Compose and contains three services:

| Service | Description | Port|
|---|---|---|
| `main`|Flask model API | `5000`|
| `api`| Flask middleman API that fetches weather data and calls the model API| `5001`|
|`frontend`| React/Vite dashboard |`5173`|

```text
React Frontend
http://localhost:5173
        |
        v
Flask Request API
http://localhost:5001
        |
        v
Main Model Flask API
http://localhost:5000
```

The React frontend sends requests to the Flask Request API on port `5001`.
The Request API fetches live Open-Meteo data, prepares the features, then sends those features to the main model API.
The main model API returns predictions to the Request API.
The Request API returns the final forecast predictions back to React.

# Requirements
- Docker Desktop

No manual setup required


# Run the Project
`docker compose up -d --build`
Then open the Frontend:
`http://localhost:5173`
