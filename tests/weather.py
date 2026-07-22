from datetime import datetime, timezone
from json import dumps
import requests, time


def parse_iso8601(iso_str):
    """
    Return an integer epoch time for the specified ISO8601 UTC date.
    """
    dt = datetime.fromisoformat(iso_str)
    dt_utc = dt.replace(tzinfo = timezone.utc)
    print(dt_utc)
    return int(dt_utc.timestamp())


# Example coordinates (Manchester, UK)
lat = 53.2965683411
lon = -2.091498096493
 
params = {
    'latitude': lat,
    'longitude': lon,
    'hourly': 'precipitation',
    'forecast_days': 2,
    'timezone': 'UTC',
}

url = 'https://api.open-meteo.com/v1/forecast'
response = requests.get(url, params = params)

if response.status_code == 200:
    data = response.json()
    print(dumps(data, indent = 2))

    now = time.time()
    print(f'Now: {time.localtime(now)}')
    hourly = data['hourly']

    for i in range(len(hourly['time'])):
        forecast_time = parse_iso8601(hourly['time'][i])
        mins = (forecast_time - now) // 60
        hours = mins // 60
        if mins >= 0 and hours < 5:
            print(f'{hours}:{mins} ({hourly['time'][i]})')
            print(f'  Rain {hourly['precipitation'][i]}mm')

else:
    print(f'API Error: {response.status_code}')