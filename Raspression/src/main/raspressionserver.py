import threading

__author__ = 'Barri Mason'

import time
import sys
import socket
import random
import ConfigParser as config

from raspression import *


##########################
# Raspression Server   #
##########################


class RaspressionServer:
    transition = None

    local_host = ""
    client_host = ""

    sensor_config = {}

    def start(self):

        self.transition = Transition()
        self.transition.start()

        if len(sys.argv) == 1:
            print "Please specify local IP address"
            sys.exit()

        self.local_host = sys.argv[1]

        self.load_config()

        try:
            while True:
                sock = None
                while sock is None:
                    self.detect_client()
                    sock = self.create_socket()
                self.listen(sock)

        except KeyboardInterrupt:
            print "Shutting down"
            self.transition.stop()
            sys.exit()

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
                self.sensor_config[sensor] = \
                    {"sens": int(parser.get(section, "sensitivity")),
                     "cc": int(parser.get(section, "midiCC")),
                     "min": int(parser.get(section, "minValue")),
                     "max": int(parser.get(section, "maxValue")),
                     "def": int(parser.get(section, "defaultValue")),
                     "time": float(parser.get(section, "trackingTime")),
                     "last": 0}

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

            midi_value = self.as_midi(sensor, value)

            sc = self.sensor_config[sensor]
            if midi_value != sc["last"]:
                self.transition.slide_to(sensor, midi_value, sc["time"], self.send_midi)
                sc["last"] = midi_value

    def as_midi(self, sensor, value):

        factor = 10000000

        sens = self.sensor_config[sensor]["sens"]
        min_value = self.sensor_config[sensor]["min"]
        max_value = self.sensor_config[sensor]["max"]
        value_range = max_value - min_value

        normalised_value = ((value * factor) - MIN_VALUE) / sens

        midi_val = int(round((1 - normalised_value) * value_range, 0)) + min_value

        midi_val = min(max(midi_val, min_value), max_value)

        return midi_val

    def send_midi(self, sensor, value):
        print sensor, "--->", value

    def __init__(self):
        pass


class Transition(threading.Thread):

    running = True

    current_value = 0
    target_value = 0
    sensor = 0
    delta = 0
    func = None

    tick = 0.0001

    def run(self):
        super(Transition, self).run()
        while self.running:
            if self.current_value != self.target_value:
                if self.is_update():
                    self.current_value += self.delta

                if not self.is_update():
                    self.current_value = self.target_value

                if self.func is not None:
                    self.func(self.sensor, self.current_value)

            time.sleep(self.tick)

    def is_update(self):
        return (self.delta > 0 and self.current_value < self.target_value) \
            or (self.delta < 0 and self.current_value > self.target_value)

    def slide_to(self, sensor, value, duration, func):
        self.target_value = value
        self.sensor = sensor
        self.func = func
        self.delta = (self.target_value - self.current_value) / (duration / self.tick)

    def stop(self):
        self.running = False
