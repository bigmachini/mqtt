from machine import Pin

PIN_TYPE = {'in': Pin.IN,
            'out': Pin.OUT}


class RelayController:
    def __init__(self, pin_no, pin_type, name):
        self.name = name + "_" + str(pin_no)
        self.pin_no = pin_no
        self.pin_type = PIN_TYPE[pin_type]
        self.state = False
        self.relay = Pin(pin_no, self.pin_type)
        print('relay -->', self.relay, 'pin no -->', self.pin_no, 'pin_type -->', self.pin_type)

    def update_state(self, state=0):
        if isinstance(state, int):
            self.relay.value(state)
            self.state = bool(state)
        else:
            raise Exception('INVALID_STATE')

    def get_state(self):
        return self.state

    def __str__(self):
        return self.name


class RelayManager:
    def __init__(self, relays=[]):
        self.relays = []
        self.pin_set = set([])
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

    def add_relays(self, relays):
        print('add_relays:: relays -->', relays)
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _pin_type = _.get('pin_type', None)
            _name = _.get('name', None)
            if _pin_no not in self.pin_set:
                self.relays.append(RelayController(_pin_no, _pin_type, _name))
                self.pin_set = set(self.relays)
                print('add_relays:: self.pin_set -->', self.pin_set)
            else:
                raise Exception('PIN_{}_ASSIGNED_ALREADY'.format(_pin_no))

    def update_relay(self, relays):
        for _ in relays:
            _pin_no = _.get('pin_no', None)
            _state = _.get('state', None)
            if _pin_no:
                relay = self.get_relay_by_pin(_pin_no)
                relay.update_state(_state)
            else:
                raise Exception('PIN_{}_NOT_ASSIGNED'.format(_pin_no))

    def get_relays(self):
        return self.relays
