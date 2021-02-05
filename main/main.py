# Complete project details at https://RandomNerdTutorials.com
from .umqttsimple import  MQTTClient
import main.secrets as secret
import ubinascii
import machine
import time

mqtt_server = secret.MQTT_HOST
mqtt_port = secret.MQTT_PORT
mqtt_username = secret.MQTT_USERNAME
mqtt_password = secret.MQTT_PASSWORD
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'hello'
topic_pub_2 = b'hello_2'

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub,mqtt_password,mqtt_username
  client = MQTTClient(client_id, mqtt_server,user=mqtt_username, password=mqtt_password)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def start():
    last_message = 0
    message_interval = 5
    counter = 0
    try:
      client = connect_and_subscribe()
    except OSError as e:
      restart_and_reconnect()

    while True:
      try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
          msg = b'Hello #%d' % counter
          client.publish(topic_pub, msg)
          client.publish(topic_pub_2, msg)
          last_message = time.time()
          counter += 1
      except OSError as e:
        restart_and_reconnect()