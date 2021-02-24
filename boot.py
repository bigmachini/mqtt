import esp
import network
from machine import RTC, reset
import main.secrets as secret
import time

esp.osdebug(None)
import gc

gc.collect()

ssid = secret.WIFI_SSID
password = secret.WIFI_PASSWORD

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

count = 0
print("connecting to wifi: ")
while not station.isconnected():

    print(".", end="")
    time.sleep(1)
    count = count + 1
    # TODO make this a configuration
    if count >= 120:
        reset()

if station.isconnected():
    import ntptime

    ntptime.settime()

print('Connection successful at {}'.format(RTC().datetime()))
print(station.ifconfig())

