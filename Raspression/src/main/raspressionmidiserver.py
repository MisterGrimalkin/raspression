from simplecoremidi import send_midi
from raspressionserver import *

C1_STATUS_BYTE = 0xB0
C1_CC = 0x66

C2_STATUS_BYTE = 0xB0
C2_CC = 0x67

LOCAL_HOST = "192.168.0.14"

last1 = 0
last2 = 0

class RaspressionMidiServer(RaspressionServer):

    def outputresult(self, values):
        global last1, last2

        c1value = int(values[0])
        if c1value != last1:
            send_midi((C1_STATUS_BYTE, C1_CC, c1value))
            last1 = c1value

        c2value = int(values[1])
        if c2value != last2:
            send_midi((C2_STATUS_BYTE, C2_CC, c2value))
            last2 = c2value

