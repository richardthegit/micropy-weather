from json import dumps
import requests, time


def parse_iso8601(iso_str):
    """
    Return an integer epoch time for the specified ISO8601 UTC date.
    """
    return time.mktime((
        int(iso_str[0:4]),    # year
        int(iso_str[5:7]),    # month
        int(iso_str[8:10]),   # mday
        int(iso_str[11:13]),  # hour
        int(iso_str[14:16]),  # minute
        0,                    # second
        0,                    # weekday (0-6, padded)
        0,                    # yearday (1-366, padded)
        0,                    # DST
    ))


# Example coordinates (Manchester, UK)
lat = 53.2965683411
lon = -2.091498096493
 
params = {
    'latitude': lat,
    'longitude': lon,
    'hourly': 'cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,precipitation',
    'forecast_days': 2,
    'timezone': 'Europe/London',
}

url = 'https://api.open-meteo.com/v1/forecast'
response = requests.get(url, params = params)

if response.status_code == 200:
    data = response.json()
    print(dumps(data, indent = 2))

    now = time.time()
    hourly = data['hourly']

    for i in range(len(hourly['time'])):
        forecast_time = parse_iso8601(hourly['time'][i])
        hours = (forecast_time - now) // 3600
        if hours >= 0 and hours < 5:
            print(f'{hours} ({hourly['time'][i]})')
            print(f'  Cloud H {hourly['cloud_cover_high'][i]}%')
            print(f'  Cloud M {hourly['cloud_cover_mid'][i]}%')
            print(f'  Cloud L {hourly['cloud_cover_low'][i]}%')
            print(f'  Rain {hourly['precipitation'][i]}mm')

else:
    print(f'API Error: {response.status_code}')