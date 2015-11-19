from raspression import *

import RPi.GPIO as gpio
import time
import sys
import socket

TRIG_1 = 23
ECHO_1 = 24
TRIG_2 = 25
ECHO_2 = 18

SAMPLES = 5

LOCAL_HOST = "192.168.0.70"
PORT = 8888

serverIp = ""
serverOnline = False


def setupGpio():

    print "Starting Sensors...."

    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG_1, gpio.OUT)
    gpio.setup(TRIG_2, gpio.OUT)
    gpio.setup(ECHO_1, gpio.IN)
    gpio.setup(ECHO_2, gpio.IN)

    gpio.output(TRIG_1, False)
    gpio.output(TRIG_2, False)
    time.sleep(2)

    print "Sensors ready"


def waitforserver():

    global serverIp

    print "Waiting for Raspression server...."

    s = socket.socket()
    s.bind((LOCAL_HOST, PORT))
    s.listen(5)
    foundserver = False

    while not foundserver:
        c, addr = s.accept()
        message = c.recv(1024)
        if message == SERVER_ONLINE_MESSAGE:
            serverIp = addr[0]
            print "Found server", ":", serverIp
            foundserver = True
            s.close()


def measureDistance(trig, echo):

    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)

    scan_start = time.time()

    pulse_start = 0
    while gpio.input(echo) == 0:
        pulse_start = time.time()
        if time.time() - scan_start > 1:
            break

    pulse_end = 0
    while gpio.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    return pulse_duration


def postmessage(value):

    global serverIp, serverOnline

    try:
        s = socket.socket()
        s.connect((serverIp, PORT))
        s.send(value)
        s.close()

        if not serverOnline:
            print SERVER_ONLINE_MESSAGE
            serverOnline = True

    except socket.error:
        if serverOnline:
            print SERVER_OFFLINE_MESSAGE
            waitforserver()



setupGpio()
waitforserver()
postmessage(CLIENT_ONLINE_MESSAGE)

while True:

    try:
        tot1 = 0
        tot2 = 0
        for i in range(SAMPLES):
            tot1 += measureDistance(TRIG_1, ECHO_1)
            tot2 += measureDistance(TRIG_2, ECHO_2)

        avg1 = tot1 / SAMPLES
        avg2 = tot2 / SAMPLES

        postmessage(str(avg1) + "," + str(avg2))

    except KeyboardInterrupt:
        print "Shutting down"
        postmessage(CLIENT_OFFLINE_MESSAGE)
        gpio.cleanup()
        sys.exit()