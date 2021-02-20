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

TOPIC_CONFIG = b'home_auto/config'
TOPIC_RELAY = b'home_auto/relay'
TOPICS = [TOPIC_CONFIG, TOPIC_RELAY]

relay_manager = []


def sub_cb(topic, msg):
    global relay_manager
    print('sub_cb:: topic -->', topic, 'msg', msg)
    if topic == TOPIC_CONFIG:
        relays = [
            {'pin_no': 12, "pin_type": "out", "name": "pin_12"},
            {'pin_no': 14, "pin_type": "out", "name": "pin_14"},
            {'pin_no': 27, "pin_type": "out", "name": "pin_27"}
        ]
        relay_manager = RelayManager(relays)
    elif topic == TOPIC_RELAY:
        pass


def connect_and_subscribe():
    global client_id, mqtt_server, TOPICS, mqtt_password, mqtt_username
    client = MQTTClient(client_id, mqtt_server, user=mqtt_username, password=mqtt_password)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to {} MQTT broker'.format(mqtt_server))
    for _ in TOPICS:
        client.subscribe(_)
        print('Subscribed to %{} topic'.format(_))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


def start():
    global relay_manager
    last_message = 0
    message_interval = 5
    counter = 0
    try:
        client = connect_and_subscribe()
    except OSError as e:
        restart_and_reconnect()

    while True:
        relays = relay_manager.get_relays()
        print('home_automation:: start:: relays --> {}'.format(relays))
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            print('_pin_no', _pin_no)
            # TODO: Add functionality to check for None
            relay = relay_manager.get_relay_by_pin(_pin_no)
            print(relay.name, relay.pin_no, relay.pin_type)
            relay.update_state(0)
            sleep(5)

        for _ in relays:
            _pin_no = _.get('pin_no', None)
            print('_pin_no', _pin_no)
            # TODO: Add functionality to check for None
            relay = relay_manager.get_relay_by_pin(_pin_no)
            print(relay.name, relay.pin_no, relay.pin_type)
            relay.update_state(1)
            sleep(5)