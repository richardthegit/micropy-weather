import time

from rb.core.net import get_json
from rb.core.richtext import rt
from rb.core.tz import local_secs, parse_iso8601
from rb.core.wifi import Wifi
from rb.dev.st7789 import color565, new_superwide

from fonts import condensed26

display, bl_pwm = new_superwide()

dark_blue = color565(6,79,110)
light_blue = color565(167,212,228)
brown = color565(124,66,38)
pink = color565(243,127,148)


def cell(x, epoch_time, precipitation, temp):
    y, m, d, h, m, s, wd, yd = time.localtime(local_secs(epoch_time))

    display.fill_rect(x + 2, 4,  66, 44, light_blue)
    display.fill_rect(x + 2, 52,  66, 20, pink)
    display.aligned(condensed26, f'{temp}°', x + 4, 6, brown, light_blue)
    display.aligned(condensed26, f'{precipitation:.1f}', x + 65, 46, 
                    brown, light_blue, halign = 'right', valign = 'bottom')
    display.aligned(condensed26, f'{h}:{m:02d}', x + 2 + 33, 61, brown, pink,
                    halign = 'center', valign = 'middle')

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
        'hourly': 'precipitation,temperature_2m',
        'forecast_days': 1,
        'timezone': 'UTC',
    })


def debug_forecast(data):
    now = time.time()
    hourly = data['hourly']
    display.fill(dark_blue)

    cell_index = 0
    for i in range(len(hourly['time'])):
        forecast_time = parse_iso8601(hourly['time'][i])
        mins = (forecast_time - now) // 60
        hours = mins // 60
        if mins > -60:
            cell(cell_index * 71, forecast_time,
                 hourly['precipitation'][i], 
                 hourly['temperature_2m'][i])

            cell_index += 1
            if cell_index >= 4:
                return

debug_forecast(latest())
