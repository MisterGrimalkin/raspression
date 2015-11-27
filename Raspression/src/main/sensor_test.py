__author__ = 'Barri Mason'

import time

import raspressionclient as client

print "Raspression Sensor Test"

trig = raw_input("Enter Trigger GPIO pin: ")
echo = raw_input("Enter Echo GPIO pin: ")

client.create_sensor(0, trig, echo)
client.setup_sensors()

rate = float(raw_input("Enter sample interval in seconds: "))

raw_input("\nMeasure maximum (hand away from sensor) ENTER to start and CTRL+C to stop:")

total = 0
samples = 0
try:
    while True:
        samples += 1
        total += client.measure_distance(0)
        # print round(client.measure_distance(0)*1000000, 4), "microseconds"
        time.sleep(rate)

except KeyboardInterrupt:
    pass

averageMax = round((total / samples)*1000000, 4)

print "\nAverage MAX =", averageMax, "microseconds\n"

raw_input("\nMeasure minimum (hand close to sensor) ENTER to start and CTRL+C to stop:")

total = 0
samples = 0
try:
    while True:
        samples += 1
        total += client.measure_distance(0)
        time.sleep(rate)

except KeyboardInterrupt:
    pass

averageMin = round((total / samples)*1000000, 4)

print "\nAverage MIN =", averageMin, "microseconds\n"

client.shutdown()


