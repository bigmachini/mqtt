import json

from machine import Pin

PIN_TYPE = {'in': Pin.IN,
            'out': Pin.OUT}


class RelayController:
    def __init__(self, pin_no, pin_type, name, client_id):
        self.name = name + "_" + str(pin_no)
        self.pin_no = pin_no
        self.pin_type = PIN_TYPE[pin_type]
        self.state = False
        self.relay = Pin(pin_no, self.pin_type)
        self.client_id = client_id
        print('relay -->', self.relay, 'pin no -->', self.pin_no, 'pin_type -->', self.pin_type)

    def update_state(self, state=0):
        if isinstance(state, int):
            try:
                self.relay.value(state)
                self.state = bool(state)
                print('RelayController:: update_state:: relay.name -->', self.name, 'relay.pin_no -->', self.pin_no,
                      'relay.pin_type-->', self.pin_type, 'state', state)
                return True
            except Exception as ex:
                return False
        else:
            raise Exception('INVALID_STATE')

    def get_state(self):
        return self.state

    def __str__(self):
        return self.name


class RelayManager:
    def __init__(self, client_id, relays=[]):
        self.relays = []
        self.pin_set = set([])
        self.add_relays(relays)
        self.client_id = client_id

    def get_relay_by_name(self, name):
        for _ in self.relays:
            if _.lower().startswith(name.lower()):
                return _
        return False

    def get_relay_by_pin(self, pin_no):
        for _ in self.relays:
            if _.pin_no == pin_no:
                return _
        return False

    def get_pins(self):
        pin_list = []
        for _ in self.relays:
            pin_list.append(_.pin_no)
        return pin_list

    def add_relays(self, relays):
        print('RelayManager::add_relays:: relays -->', relays)
        _pin_list = self.get_pins()
        print('RelayManager::add_relays:: _pin_list -->', _pin_list)

        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _pin_type = _.get('pin_type', None)
            _name = _.get('name', None)
            if _pin_no not in _pin_list:
                self.relays.append(RelayController(_pin_no, _pin_type, _name, self.client_id))
                _pin_list.append(_.pin_no)
                self.pin_set = set(_pin_list)
                print('add_relays:: self.pin_set -->', self.pin_set)
            else:
                raise Exception('PIN_{}_ASSIGNED_ALREADY'.format(_pin_no))

    def update_relay(self, relays, client, topic_pub):
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _state = _.get('state', None)
            if _pin_no:
                relay = self.get_relay_by_pin(_pin_no)
                if relay.update_state(_state):
                    msg = {'pin_no': _pin_no, 'state': _state, 'client_id': self.client_id}
                    msg = json.dumps(msg)
                    msg = msg.encode('utf-8')
                    client.publish(topic_pub, msg)
            else:
                raise Exception('PIN_{}_NOT_ASSIGNED'.format(_pin_no))

    def get_relays(self):
        return self.relays
