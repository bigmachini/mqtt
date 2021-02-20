import esp
import network

import main.secrets as secret

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
