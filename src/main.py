import time

from rb.core.net import get_json
from rb.core.richtext import rt
from rb.core.tz import parse_iso8601
from rb.core.wifi import Wifi
from rb.dev.st7789 import color565, new_superwide


wifi = Wifi()
wifi.on()
wifi.ntp()

display, bl_pwm = new_superwide()
colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))
w = 284
h = 76 // 4
y = 0

for c in colors:
    display.fill_rect(0, y,  w, h, color565(*c))
    y += h

url = 'https://api.open-meteo.com/v1/forecast'
lat = 53.2965683411
lon = -2.091498096493

def latest(): 
    return get_json(url, {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,precipitation',
        'forecast_days': 2,
        'timezone': 'UTC',
    })


def debug_forecast(data):
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


debug_forecast(latest())

