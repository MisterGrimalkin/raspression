import RPi.GPIO as GPIO
import time

LATCH_MODE_1 = True
LATCH_MODE_2 = True

SAMPLES = 1

TRIG_1 = 23
ECHO_1 = 24
TRIG_2 = 25
ECHO_2 = 18

SENS_1 = 200
SENS_2 = 100
MIN = 25

def setup():
    print "Setting up...."
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_1,GPIO.OUT)
    GPIO.setup(TRIG_2,GPIO.OUT)
    GPIO.setup(ECHO_1,GPIO.IN)
    GPIO.setup(ECHO_2,GPIO.IN)

    GPIO.output(TRIG_1, False)
    GPIO.output(TRIG_2, False)
    time.sleep(2)
    print "Ready"

def measureDistance(trig, echo, sens):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    pulse_start = 0
    while GPIO.input(echo)==0:
      pulse_start = time.time()

    pulse_end = 0
    while GPIO.input(echo)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    value = round(pulse_duration*100000, 0)

    out = ((sens + MIN - value) / sens) * 100

    if out < 0:
        out = 0

    if out > 100:
        out = 100

    time.sleep(0.00001)


    return out

def printAsBar(value, symbol):

    outbar = ''
    i = 0
    while i < (value):
        outbar = outbar + symbol
        i = i + 1

    print outbar

def printAsInvertedBar(value, symbol):

    outbar = ''
    i = 0
    while i < (value):
        outbar = outbar + symbol
        i = i + 1

    i = 0
    while i < (100-value):
        outbar = ' ' + outbar
        i = i + 1

    print outbar


setup()
last1 = 0
last2 = 0
while True:
    tot1 = 0
    tot2 = 0
    for i in range(SAMPLES):
        tot1 = tot1 + measureDistance(TRIG_1, ECHO_1, SENS_1)
        tot2 = tot2 + measureDistance(TRIG_2, ECHO_2, SENS_2)

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

    printAsBar(avg1, '#')
    printAsBar(avg2, '=')


GPIO.cleanup()