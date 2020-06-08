

print('Imported!')

class Code():
    def __init__(self):
        self.place_id = '8201'
        self.device_type = 'test'

    def test_msg(self):
        return "MyMsg123!"

    def step(self, mqttc):
        mqttc.publish(f'state/{self.place_id}/{self.device_type}', self.test_msg())


