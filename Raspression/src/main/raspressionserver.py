
__author__ = 'Barri Mason'

import sys
import time
import socket

import threading
import ConfigParser as config

from raspression import *
from transitions import Linear
from transitions import Instant
from web_server import WebServer
from moving_average import AverageQueue


##########################
# Raspression Server   #
##########################


def valid_midi(value):
    return 0 <= value <= 127


class RaspressionServer:

    local_host = ""
    client_host = ""

    sensor_config = {}

    queues = {}

    ws = None

    def start(self):

        if len(sys.argv) == 1:
            print "Please specify local IP address"
            sys.exit()

        self.local_host = sys.argv[1]

        self.load_config()

        self.start_raspression_server()
        # t = threading.Thread(target=self.start_raspression_server)
        # t.start()

        # WebServer(self).start()

    def start_raspression_server(self):

        print "Starting...."

        try:
            while True:
                sock = None
                while sock is None:
                    self.detect_client()
                    sock = self.create_socket()
                self.listen(sock)

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print "Shutting down"
        for sensor in self.sensor_config:
            self.sensor_config[sensor]["trans"].stop()
        sys.exit()

    def get_values(self, prop):
        result = {}
        for sensor in self.sensor_config:
            cfg = self.sensor_config[sensor]
            result[sensor] = cfg[prop]
        return result

    def set_min(self, sensor, value):
        if valid_midi(value):
            self.sensor_config[int(sensor)]["min"] = value

    def set_max(self, sensor, value):
        if valid_midi(value):
            self.sensor_config[int(sensor)]["max"] = int(value)

    def set_def(self, sensor, value):
        if valid_midi(value):
            self.sensor_config[int(sensor)]["def"] = int(value)

    def set_cc(self, sensor, value):
        if valid_midi(value):
            self.sensor_config[int(sensor)]["cc"] = int(value)

    def set_sens(self, sensor, value):
        if 0 <= value <= 20000:
            self.sensor_config[int(sensor)]["sens"] = int(value)

    def set_time(self, sensor, value):
        if 0 < value <= 30000:
            self.sensor_config[sensor]["time"] = float(value/1000.0)
        print self.sensor_config[sensor]["time"]

    def load_config(self):

        print "Loading Configuration...."

        parser = config.ConfigParser()
        parser.read("raspressionserver.config")

        # Client IP address
        self.client_host = parser.get("General", "clientHost")

        # Settings for each sensor
        for section in parser.sections():
            if section[0:6] == "Sensor":
                sensor = int(section[6:])
                self.queues[sensor] = AverageQueue(int(parser.get(section, "samples")))
                self.sensor_config[sensor] = \
                    {"sens": int(parser.get(section, "sensitivity")),
                     "cc": int(parser.get(section, "midiCC")),
                     "min": int(parser.get(section, "minValue")),
                     "max": int(parser.get(section, "maxValue")),
                     "def": int(parser.get(section, "defaultValue")),
                     "slideup": float(parser.get(section, "slideUp")),
                     "slidedown": float(parser.get(section, "slideDown")),
                     "trans": Instant(sensor),
                     "value": 0}
                self.sensor_config[sensor]["trans"].start()

        print "OK"

    def save_config(self):

        print "Saving Configuration"

    def detect_client(self):

        print "Connecting to Raspression Client...."

        client_online = False

        while not client_online:

            s = socket.socket()
            try:
                s.connect((self.client_host, PORT))
                s.send(SERVER_ONLINE_MESSAGE)
                client_online = True

            except socket.error:
                print "No response"
                time.sleep(1)

            finally:
                s.close()

        print "Client Online:", self.client_host

    def create_socket(self):

        print "Starting Raspression Server...."

        s = socket.socket()
        try:
            s.bind((self.local_host, PORT))
            s.listen(5)
            print "Server running on:", self.local_host

        except socket.error:
            s.close()
            s = None
            print "Error, trying again in 5 seconds"
            time.sleep(5)

        return s

    def listen(self, sock):

        print "Listening for data...."

        while True:
            try:
                c, addr = sock.accept()
                message = c.recv(1024)
                if message == CLIENT_ONLINE_MESSAGE:
                    print message
                elif message == CLIENT_OFFLINE_MESSAGE:
                    print message
                    sock.close()
                    return
                else:
                    self.process_message(message)
                    c.close()

            except socket.error:
                sock.close()
                return

    def process_message(self, message):

        l = message.split("=")

        if len(l) == 2:

            sensor = int(l[0])
            value = float(l[1])

            queue = self.queues[sensor]

            midi_value = self.as_midi(sensor, value)
            queue.put_value(midi_value)
            avg_value = int(queue.get_average())

            cfg = self.sensor_config[sensor]

            if avg_value != cfg["value"]:

                trans_time = cfg["slideup"]
                if avg_value < cfg["value"]:
                    trans_time = cfg["slidedown"]

                cfg["trans"].slide_to(avg_value, trans_time, self.put_value)

    def as_midi(self, sensor, value):

        factor = 10000000

        cfg = self.sensor_config[sensor]

        normalised_value = ((value * factor) - MIN_VALUE) / cfg["sens"]

        min_value = cfg["min"]
        max_value = cfg["max"]
        def_value = cfg["def"]
        value_range = max_value - min_value

        val_before_offset = int(round((1 - normalised_value) * value_range, 0))

        midi_val = val_before_offset + min_value

        if val_before_offset == 0:
            if def_value <= 0:
                midi_val = cfg["value"]
            elif def_value > 0:
                midi_val = def_value

        midi_val = int(round(min(max(midi_val, min_value), max_value), 0))

        return midi_val

    def put_value(self, sensor, value):
        self.sensor_config[sensor]["value"] = value
        self.send_midi(sensor, value)

    def send_midi(self, sensor, value):
        print sensor, "--->", value

    def __init__(self):
        pass


