__author__ = 'Barri Mason'

import time
import sys
import socket
import ConfigParser

import RPi.GPIO as gpio

from raspression import *


##########################
#   Raspression Client   #
##########################


local_host = ""
server_host = ""

sensor_config = {}
samples = 0
sensor_timeout = 1
sample_delay = 0

MAX_SENSOR_VALUE = 0.011

def start():

    load_config()
    setup_sensors()

    try:
        while True:
            wait_for_server()
            start_sensors()

    except KeyboardInterrupt:
        shutdown()


def shutdown():
    print "Shutting down"
    post_message_safe(CLIENT_OFFLINE_MESSAGE)
    gpio.cleanup()
    sys.exit()

def load_config():

    print "Loading Configuration...."

    global local_host, samples, sensor_timeout, sample_delay

    parser = ConfigParser.ConfigParser()
    parser.read("raspressionclient.config")

    # local IP address
    local_host = parser.get("General", "localHost")

    # Measurement samples per reading
    samples = int(parser.get("General", "samples"))

    # Sample Delay
    sample_delay = float(parser.get("General", "sampleDelay"))

    # Timeout for sensor measurement (seconds)
    sensor_timeout = int(parser.get("General", "sensorTimeout"))

    # GPIO pin numbers for each sensor
    for section in parser.sections():
        if section[0:6] == "Sensor":
            sensor = int(section[6:])
            create_sensor(sensor, int(parser.get(section, "triggerPin")), int(parser.get(section, "echoPin")))


def create_sensor(sensor, trig, echo):
    sensor_config[sensor] = \
        {"trig": int(trig),
         "echo": int(echo)}


def setup_sensors():

    print "Setting up sensors...."

    gpio.setmode(gpio.BCM)

    # initialise pins
    for sensor in sensor_config:
        config = sensor_config[sensor]
        gpio.setup(config["echo"], gpio.IN)
        gpio.setup(config["trig"], gpio.OUT)
        gpio.output(config["trig"], False)

    # Wait for sensors to settle
    time.sleep(2)

    print "Sensors ready"


def wait_for_server():

    global server_host

    print "Waiting for Raspression server...."

    found_server = False

    # Start listening for the server
    s = socket.socket()
    s.bind((local_host, PORT))
    s.listen(5)

    while not found_server:
        c, address = s.accept()
        message = c.recv(1024)

        if message == SERVER_ONLINE_MESSAGE:
            server_host = address[0]
            s.close()
            found_server = True

        elif message == CLIENT_OFFLINE_MESSAGE:
            s.close()
            raise KeyboardInterrupt()

    # Tell the server that client is online
    post_message_safe(CLIENT_ONLINE_MESSAGE)

    print "Found server: ", server_host


def start_sensors():

    print "Starting sensor loop...."

    while True:
        try:
            for sensor in sensor_config:
                total = 0
                for i in range(samples):
                    total += measure_distance(sensor)
                average = total / samples
                post_message(str(sensor) + "=" + str(average))

            time.sleep(sample_delay)

        except socket.error:
            print SERVER_OFFLINE_MESSAGE
            return


def measure_distance(sensor):

    # HC-SR04 ultrasonic sensor:
    #   Put a brief pulse on the TRIG pin
    #   The transmitter sends an ultrasonic burst
    #   Sound bounces off object (hand)
    #   The receiver senses the echo of the burst
    #   A pulse comes in on the ECHO pin
    #   The length of the pulse is the time between sound and echo

    trig = sensor_config[sensor]["trig"]
    echo = sensor_config[sensor]["echo"]

    # Send ultrasound pulse
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    pulse_start = 0
    pulse_end = 0

    # Wait for echo pulse
    scan_start = time.time()
    while gpio.input(echo) == 0:
        pulse_start = time.time()
        if time.time() - scan_start > sensor_timeout:
            break

    # Measure length of echo pulse
    while gpio.input(echo) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > MAX_SENSOR_VALUE:
            break

    pulse_duration = pulse_end - pulse_start

    return pulse_duration


def post_message(message):

    s = socket.socket()
    s.connect((server_host, PORT))
    s.send(message)
    s.close()


def post_message_safe(message):

    try:
        post_message(message)
    except socket.error:
        pass


if __name__ == '__main__':
    start()