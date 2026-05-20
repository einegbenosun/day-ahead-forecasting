# Day-Ahead Solar PV Forecasting

This project is a day-ahead photovoltaic forecasting dashboard. It uses live Open-Meteo weather forecast data,sends the processed features to a trained machine learning model API, and displays the forecast results in a React frontend.

The project runs with Docker Compose and contains three services:

| Service | Description | Port|
|---|---|---|
| 'main'|Flask model API | '5000'|
| 'api'| Flask middleman API that fetches weather data and calls the model API| '5001'|
|'frontend'| React/Vite dashboard |'5173'|


React Frontend
http://localhost:5173
->
Flask Request API
http://localhost:5001
->
Main Model Flask API
http://localhost:5000 

