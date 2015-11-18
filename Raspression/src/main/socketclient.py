import socket

s = socket.socket()
host = "192.168.0.123"
port = 8888

s.connect((host, port))
s.send("Bloody hell")
print s.recv(1024)
s.close()


