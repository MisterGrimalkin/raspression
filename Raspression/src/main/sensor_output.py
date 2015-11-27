__author__ = 'Barri Mason'

import time

import raspressionclient as client

print "Raspression Sensor Test"

client.load_config()
client.setup_sensors()

rate = float(raw_input("Enter sample interval in seconds: "))

try:
    sensor = int(raw_input("\nEnter sensor to track: "))
    while True:
        print round((client.measure_distance(sensor))*1000000, 4)
        time.sleep(rate)

except KeyboardInterrupt:
    pass

client.shutdown()


