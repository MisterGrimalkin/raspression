from _socket import SHUT_RDWR
import socket
import sys
from simplecoremidi import send_midi

C1_STATUS_BYTE = 0xB0
C1_CC = 0x66

C2_STATUS_BYTE = 0xB0
C2_CC = 0x67

last1 = 0
last2 = 0


def startserver():

    s = socket.socket()
    host = "192.168.0.18"
    port = 8888
    s.bind((host, port))

    print "Starting Server"

    s.listen(5)
    while True:
        try:
            c, addr = s.accept()
            message = c.recv(1024)
            if message == "ONLINE":
                print "Raspression Client UP"
            elif message == "OFFLINE":
                print "Raspression Client DOWN"
            else:
                outputresult(message)
            c.close()

        except KeyboardInterrupt:
            print "Shutting Down"
            s.close()
            sys.exit()


def outputresult(data):
    global last1, last2
    l = data.split(",")
    # print l[0].rjust(3), " ---- ", l[1].ljust(3)

    c1value = int(l[0])
    if c1value != last1:
        print "C1 : ", c1value
        send_midi((C1_STATUS_BYTE, C1_CC, c1value))
        last1 = c1value

    c2value = int(l[1])
    if c2value != last2:
        print "C2 : ", c2value
        send_midi((C2_STATUS_BYTE, C2_CC, c2value))
        last2 = c2value



startserver()