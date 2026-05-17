from pathlib import Path
import pandas as pd

csv_path = Path(__file__).with_name("open_meteo.csv")
df = pd.read_csv(csv_path,sep=",")

#All columns in the original csv file
#open_meteo_df = df[['time,temperature_2m (°C),relative_humidity_2m (%),dew_point_2m (°C),apparent_temperature (°C),precipitation (mm),rain (mm),snowfall (cm),snow_depth (m),weather_code (wmo code),pressure_msl (hPa),surface_pressure (hPa),cloud_cover (%),cloud_cover_low (%),cloud_cover_mid (%),cloud_cover_high (%),wind_speed_10m (km/h),wind_direction_10m (°),wind_gusts_10m (km/h),is_day (),sunshine_duration (s),shortwave_radiation (W/m²),direct_radiation (W/m²),direct_normal_irradiance (W/m²),diffuse_radiation (W/m²),global_tilted_irradiance (W/m²),terrestrial_radiation (W/m²)']]

open_meteo_df = df[["time", "temperature_2m (°C)", "relative_humidity_2m (%)", "wind_speed_10m (km/h)", "shortwave_radiation (W/m²)", "direct_radiation (W/m²)", "direct_normal_irradiance (W/m²)", "diffuse_radiation (W/m²)", "global_tilted_irradiance (W/m²)", "is_day ()", "sunshine_duration (s)"]]
open_meteo_df = open_meteo_df.rename(columns={"time": "timestamp",
                                              "temperature_2m (°C)": "temperature_2m",
                                              "relative_humidity_2m (%)": "relative_humidity_2m",
                                              "wind_speed_10m (km/h)": "wind_speed_10m",
                                              "shortwave_radiation (W/m²)": "shortwave_radiation",
                                              "direct_radiation (W/m²)": "direct_radiation",
                                              "direct_normal_irradiance (W/m²)": "direct_normal_irradiance",
                                              "diffuse_radiation (W/m²)": "diffuse_radiation",
                                              "global_tilted_irradiance (W/m²)": "global_tilted_irradiance",
                                              "is_day ()": "is_day",
                                              "sunshine_duration (s)": "sunshine_duration"
                                              })

open_meteo_df.to_csv("open_meteo_cleaned.csv", index=False)
print((df.columns.tolist()))
