from raspression import *
import socket
import sys
import time

localhost = ""

class RaspressionServer:

    def waitforclient(self):

        print "Looking for Raspression Client...."

        clientOnline = False

        while not clientOnline:

            s = socket.socket()
            try:
                s.connect((CLIENT_HOST, PORT))
                s.send(SERVER_ONLINE_MESSAGE)
                s.close()

                clientOnline = True
                print "Client Online:", CLIENT_HOST
                time.sleep(2)

            except socket.error:
                print "Cannot Find Client"
                s.close()
                time.sleep(1)

    def startserver(self):

        global localhost

        print "Starting Server on", localhost

        s = socket.socket()
        try:
            s.bind((localhost, PORT))
            s.listen(5)

        except socket.error:
            print "Error starting server, try again in 10 seconds"
            s = socket.socket()
            s.connect((CLIENT_HOST, PORT))
            s.send(SERVER_OFFLINE_MESSAGE)
            s.close()
            time.sleep(10)
            self.startserver()
            return

        print "Server online"

        while True:
            try:
                c, addr = s.accept()
                message = c.recv(1024)
                if message == CLIENT_ONLINE_MESSAGE:
                    print message
                elif message == CLIENT_OFFLINE_MESSAGE:
                    print message
                    self.waitforclient()
                else:

                    self.outputresult(self.converttomidivalues(message))
                c.close()

            except socket.error:
                print CLIENT_OFFLINE_MESSAGE
                s.close()
                self.waitforclient()

            except KeyboardInterrupt:
                print "Shutting Down"
                s.close()
                s.connect((CLIENT_HOST, PORT))
                s.send(SERVER_OFFLINE_MESSAGE)
                s.close()
                sys.exit()

    def converttomidivalues(self, data):
        l = data.split(",")

        midiValue1 = self.normalise(float(l[0]), SENSITIVITY_1)
        midiValue2 = self.normalise(float(l[1]), SENSITIVITY_2)

        return midiValue1, midiValue2

    def normalise(self, value, sensitivity):

        factor = 10000000

        normalisedvalue = ((value * factor) - MIN_VALUE) / sensitivity

        midival = int(round((1 - normalisedvalue) * 127, 0))

        midival = min(max(midival, 0), 127)

        return midival

    def outputresult(self, values):

        print str(values[0]), " ---- ", str(values[1])

    def start(self):

        global localhost

        if len(sys.argv) > 1:
            localhost = sys.argv[1]

        print localhost

        self.waitforclient()
        self.startserver()

