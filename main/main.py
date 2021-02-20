import json
from time import sleep
from main.relay import RelayManager
from .umqttsimple import MQTTClient
import main.secrets as secret
import ubinascii
import machine
import time

mqtt_server = secret.MQTT_HOST_HOME_AUTO
mqtt_port = secret.MQTT_PORT_HOME_AUTO
mqtt_username = secret.MQTT_USERNAME_HOME_AUTO
mqtt_password = secret.MQTT_PASSWORD_HOME_AUTO
client_id = ubinascii.hexlify(machine.unique_id())
str_client_id = client_id.decode('utf-8')

TOPIC_CONFIG = 'home_auto/{}/config'.format(str_client_id).lower().encode('utf-8')
TOPIC_RELAY = 'home_auto/{}/relay'.format(str_client_id).lower().encode('utf-8')
TOPIC_UPDATE = 'home_auto/{}/update'.format(str_client_id).lower().encode('utf-8')
TOPICS = [TOPIC_CONFIG, TOPIC_RELAY, TOPIC_UPDATE]

relay_manager = None
update_firmware = None


def sub_cb(topic, msg):
    global relay_manager, update_firmware
    print('sub_cb:: topic -->', topic, 'msg', msg)
    if topic == TOPIC_CONFIG:
        relays = json.loads(msg.decode('utf-8'))
        if relay_manager is None:
            relay_manager = RelayManager(relays)
        else:
            relay_manager.add_relays(relays)
    elif topic == TOPIC_RELAY:
        relay = json.loads(msg.decode('utf-8'))
        relay_manager.update_relay(relay)
    elif topic == TOPIC_UPDATE:
        update_firmware()


def connect_and_subscribe():
    global client_id, mqtt_server, TOPICS, mqtt_password, mqtt_username
    client = MQTTClient(client_id, mqtt_server, user=mqtt_username, password=mqtt_password)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to {} MQTT broker'.format(mqtt_server))
    for _ in TOPICS:
        client.subscribe(_)
        print('Subscribed to {} topic'.format(_))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def start(connect_to_wifi_and_update):
    global relay_manager, update_firmware
    update_firmware = connect_to_wifi_and_update
    try:
        client = connect_and_subscribe()
    except OSError as e:
        restart_and_reconnect()

    while True:
        client.check_msg()
        if relay_manager is not None:
            pass
