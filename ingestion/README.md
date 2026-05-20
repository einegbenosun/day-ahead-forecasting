# Changing Location and Replacing Data

This folder contains scripts and CSV files used to prepare the training and forecast data.

To modify the project for a different location:
# Open Meteo
1. Modify the latitude and longitude values from: [Open-Meteo Historical Forecast API](https://open-meteo.com/en/docs/historical-forecast-api?hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,sunshine_duration,is_day,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance&tilt=35&start_date=2024-05-18&models=best_match#settings)
2. Download the CSV file and replace `open_meteo.csv` (rename downloaded file to this).
3. In this file, remove the first 3 rows.

# CAMS Copernicus
1. Create a free account and submit a data request form with the same longitude and latitude locations at: [CAMS solar radiation](https://ads.atmosphere.copernicus.eu/datasets/cams-solar-radiation-timeseries?tab=download)
2. Download the CSV and replace `cams.csv` (rename downloaded file to this).
3. In this file - it is important you remove the last # next to the header row so the headers can be read.

Ensure both date ranges are the same - the current system uses 2 years of data.

#Data Cleaning
1. Run files: `open_meteo_cleaning.py` and `cams_cleaning.py`
2. This will generate `open_meteo_cleaned.csv` and `cams_cleaned.csv`.
3. Replace the files in `/csv` with these generated files and run `merge.py` to created a cleaned `merged.csv`

   
