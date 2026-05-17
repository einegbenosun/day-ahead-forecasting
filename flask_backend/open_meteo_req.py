#https://open-meteo.com/en/docs?hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,dew_point_2m,apparent_temperature,precipitation,rain,precipitation_probability,snowfall,snow_depth,is_day,sunshine_duration,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,wind_direction_10m,wind_gusts_10m,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation&forecast_days=1&latitude=51.8859&longitude=-8.5332
import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import numpy




# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 51.8859,
	"longitude": -8.5332,
	"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "dew_point_2m", "apparent_temperature", "precipitation", "rain", "precipitation_probability", "snowfall", "snow_depth", "is_day", "sunshine_duration", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "wind_direction_10m", "wind_gusts_10m", "shortwave_radiation", "direct_radiation", "diffuse_radiation", "direct_normal_irradiance", "global_tilted_irradiance", "terrestrial_radiation"],
	"forecast_days": 1,
}
responses = openmeteo.weather_api(url, params = params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(3).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
hourly_rain = hourly.Variables(6).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(7).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
hourly_is_day = hourly.Variables(10).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(11).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(12).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(13).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(14).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(15).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(16).ValuesAsNumpy()
hourly_cloud_cover_mid = hourly.Variables(17).ValuesAsNumpy()
hourly_cloud_cover_high = hourly.Variables(18).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(19).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(20).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(21).ValuesAsNumpy()
hourly_direct_radiation = hourly.Variables(22).ValuesAsNumpy()
hourly_diffuse_radiation = hourly.Variables(23).ValuesAsNumpy()
hourly_direct_normal_irradiance = hourly.Variables(24).ValuesAsNumpy()
hourly_global_tilted_irradiance = hourly.Variables(25).ValuesAsNumpy()
hourly_terrestrial_radiation = hourly.Variables(26).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["is_day"] = hourly_is_day
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["weather_code"] = hourly_weather_code
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["direct_radiation"] = hourly_direct_radiation
hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
hourly_data["global_tilted_irradiance"] = hourly_global_tilted_irradiance
hourly_data["terrestrial_radiation"] = hourly_terrestrial_radiation

df = pd.DataFrame(data = hourly_data)
#print("\nHourly data\n", hourly_dataframe)

import requests

api_url = "http://127.0.0.1:5000/xgbpredict"
time = hourly_data["date"]

list = []
for i in range(1,24):
    row = df.iloc[i].to_dict()

    row["Hour"] = int(row["date"].hour)
    row["DAY"] = int(row["date"].day)
    row["MONTH"] = int(row["date"].month)
    row["YEAR"] = int(row["date"].year)

    del row["date"]

    

    api_response = requests.post(api_url, json=row)
    print(api_response.json()) 
    list.append(api_response.json())

print(list)
total = (sum(list))
print(len(list))
print(total)