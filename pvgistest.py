import requests

latitude = 45.8120
longitude = 8.6280

response = requests.get("http://photovoltaic-geographic-information-system.ec.europa.eu/api/v6/performance/broadband", params={
    "latitude": latitude,
    "longitude": longitude,
    "start_time": "2022-01-01 00:00:00",
    "end_time": "2024-12-31 23:59:59"
})

print(response.json())