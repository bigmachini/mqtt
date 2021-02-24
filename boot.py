import esp
import network
from machine import RTC
import main.secrets as secret

esp.osdebug(None)
import gc

gc.collect()

ssid = secret.WIFI_SSID
password = secret.WIFI_PASSWORD

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

if station.isconnected():
    import ntptime

    ntptime.settime()

print('Connection successful at {}'.format(RTC().datetime()))
print(station.ifconfig())
