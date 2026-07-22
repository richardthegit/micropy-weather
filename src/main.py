import time

from rb.core.net import get_json
from rb.core.richtext import rt
from rb.core.tz import parse_iso8601
from rb.core.wifi import Wifi
from rb.dev.st7789 import color565, new_superwide

from fonts import noto20

display, bl_pwm = new_superwide()
colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))
w = 284
h = 76 // 4
y = 0

for c in colors:
    display.fill_rect(0, y,  w, h, color565(*c))
    y += h

display.write(noto20, '1234', 0, 20, color565(0, 0, 0), color565(255, 255, 255))

wifi = Wifi()
wifi.on()
wifi.ntp()

url = 'http://api.open-meteo.com/v1/forecast'
lat = 53.2965683411
lon = -2.091498096493

def latest(): 
    return get_json(url, {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'precipitation',
        'forecast_days': 1,
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
            print(f'  Rain {hourly['precipitation'][i]}mm')


debug_forecast(latest())
