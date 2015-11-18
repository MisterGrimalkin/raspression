import RPi.GPIO as GPIO
import time
import sys
import socket

serverIp = "192.168.0.18"
serverPort = 8888
serverOnline = False

LATCH_MODE_1 = False
LATCH_MODE_2 = False

SAMPLES = 1

TRIG_1 = 23
ECHO_1 = 24
TRIG_2 = 25
ECHO_2 = 18

SENS_1 = 200
SENS_2 = 100
MIN = 25

def setupGpio():
    print "Setting up...."
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_1,GPIO.OUT)
    GPIO.setup(TRIG_2,GPIO.OUT)
    GPIO.setup(ECHO_1,GPIO.IN)
    GPIO.setup(ECHO_2,GPIO.IN)

    GPIO.output(TRIG_1, False)
    GPIO.output(TRIG_2, False)
    time.sleep(2)
    print "Sensors ready"


def measureDistance(trig, echo, sens):

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    pulse_start = 0
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    pulse_end = 0
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    value = round(pulse_duration*100000, 0)

    out = int(((sens + MIN - value) / sens) * 127)

    if out < 0:
        out = 0

    if out > 127:
        out = 127

    return out


def postmessage(value):
    global serverOnline
    try:
        s = socket.socket()
        s.connect((serverIp, serverPort))
        s.send(value)
        s.close()

        if not serverOnline:
            print "Raspression Server UP"
            serverOnline = True

    except socket.error:
        if serverOnline:
            print "Raspression Server DOWN"
            serverOnline = False


setupGpio()
postmessage("ONLINE")
last1 = 0
last2 = 0
while True:

    try:
        tot1 = 0
        tot2 = 0
        for i in range(SAMPLES):
            tot1 += measureDistance(TRIG_1, ECHO_1, SENS_1)
            tot2 += measureDistance(TRIG_2, ECHO_2, SENS_2)

        avg1 = tot1 / SAMPLES
        avg2 = tot2 / SAMPLES

        if LATCH_MODE_1:
            if avg1 == 0:
                avg1 = last1
            last1 = avg1

        if LATCH_MODE_2:
            if avg2 == 0:
                avg2 = last2
            last2 = avg2

        postmessage(str(avg1) + "," + str(avg2))

    except KeyboardInterrupt:
        print "Shutting down"
        postmessage("OFFLINE")
        GPIO.cleanup()
        sys.exit()