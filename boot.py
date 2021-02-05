# Complete project details at https://RandomNerdTutorials.com

import time
from main.umqttsimple import MQTTClient
import main.secrets as secret
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = secret.WIFI_SSID
password = secret.WIFI_PASSWORD

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
