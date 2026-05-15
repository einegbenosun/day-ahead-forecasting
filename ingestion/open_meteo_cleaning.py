from pathlib import Path
import pandas as pd
import csv

csv_path = Path(__file__).with_name("open_meteo.csv")
df = pd.read_csv(csv_path,sep=";")

open_meteo_df = df[['time,temperature_2m (°C),relative_humidity_2m (%),dew_point_2m (°C),apparent_temperature (°C),precipitation (mm),rain (mm),snowfall (cm),snow_depth (m),weather_code (wmo code),pressure_msl (hPa),surface_pressure (hPa),cloud_cover (%),cloud_cover_low (%),cloud_cover_mid (%),cloud_cover_high (%),wind_speed_10m (km/h),wind_direction_10m (°),wind_gusts_10m (km/h),is_day (),sunshine_duration (s),shortwave_radiation (W/m²),direct_radiation (W/m²),direct_normal_irradiance (W/m²),diffuse_radiation (W/m²),global_tilted_irradiance (W/m²),terrestrial_radiation (W/m²)']]
print(df.columns.tolist())