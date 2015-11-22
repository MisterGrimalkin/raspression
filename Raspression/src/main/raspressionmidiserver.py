import simplecoremidi

from raspressionserver import RaspressionServer

STATUS_BYTE = 0xB0


class RaspressionMidiServer(RaspressionServer):

    def send_midi(self, sensor, value):
        simplecoremidi.send_midi((STATUS_BYTE, self.sensor_config[sensor]["cc"], value))

