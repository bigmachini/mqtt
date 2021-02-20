from time import sleep
from main.relay import RelayManager

relays = [
    {'pin_no': 12, "pin_type": "out", "name": "pin_12"},
    {'pin_no': 14, "pin_type": "out", "name": "pin_14"},
    {'pin_no': 27, "pin_type": "out", "name": "pin_27"},
]

relay_manager = RelayManager(relays)


def start():
    while True:
        for _ in relays:
            relay = relay_manager.get_relay_by_pin(_.pin_no)
            print(relay.name, relay.pin_no, relay.pin_type)
            relay.update_state(0)
            sleep(5)

        for _ in relays:
            relay = relay_manager.get_relay_by_pin(_.pin_no)
            print(relay.name, relay.pin_no, relay.pin_type)
            relay.update_state(1)
            sleep(5)
