import json

from machine import Pin,RTC

PIN_TYPE = {'in': Pin.IN,
            'out': Pin.OUT}


class Relay:
    def __init__(self, pin_no, pin_type, state, client_id):
        self.name = "pin_" + str(pin_no)
        self.pin_no = pin_no
        self.pin_type = pin_type
        self.state = state
        self.relay = Pin(pin_no, PIN_TYPE[pin_type])
        self.client_id = client_id
        print(self)

    def update_state(self, state=0):
        if isinstance(state, int):
            try:
                self.relay.value(state)
                self.state = state
                return True
            except Exception as ex:
                return False
        else:
            print('INVALID_STATE')

    def get_status(self):
        rtc = RTC()
        if rtc:

        return {"state": self.state, "pin": self.pin_no, "pin_type": self.pin_type, "client_id": self.client_id}

    def __repr__(self):
        return 'Relay(pin_no={},pin_type={},state={},client_id={})'.format(self.pin_no, self.pin_type, self.state,
                                                                           self.client_id)


class RelayManager:
    def __init__(self, client, client_id, topic, relays=[]):
        self.relays = []
        self.pin_set = set([])
        self.client = client
        self.client_id = client_id
        self.topic = topic
        self.add_relays(relays)

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
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _pin_type = _.get('pin_type', None)
            _state = _.get('state', None)
            if _pin_no not in _pin_list:
                _relay = Relay(_pin_no, _pin_type, _state, self.client_id)
                self.relays.append(_relay)
                _pin_list.append(_pin_no)
                self.pin_set = set(_pin_list)
                print('RelayManager::add_relays:: self.pin_set -->', self.pin_set)
                msg = {'pin_no': _pin_no, 'client_id': self.client_id}
                self.publish_message(msg, self.topic)
            else:
                print('PIN_{}_ASSIGNED_ALREADY'.format(_pin_no))

    def publish_message(self, msg, topic):
        msg = json.dumps(msg)
        msg = msg.encode('utf-8')
        self.client.publish(topic, msg)

    def update_relay(self, relays):
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _state = _.get('state', None)
            if _pin_no:
                relay = self.get_relay_by_pin(_pin_no)
                relay.update_state(_state)
            else:
                print('PIN_{}_NOT_ASSIGNED'.format(_pin_no))

    def update_status(self, topic):
        res = []
        for _ in self.relays:
            res.append(_.get_status())

        if res:
            self.publish_message(res, topic)

    def get_relays(self):
        return self.relays
