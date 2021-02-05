# Complete project details at https://RandomNerdTutorials.com

import time
from umqttsimple import MQTTClient
import secrets as secret
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = secret.WIFI_SSID
password = secret.WIFI_PASSWORD
mqtt_server = secret.MQTT_HOST
mqtt_port = secret.MQTT_PORT
mqtt_username = secret.MQTT_USERNAME
mqtt_password = secret.MQTT_PASSWORD
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
