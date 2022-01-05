import socket
import time

ClientMultiSocket = socket.socket()
#connect to host server
host = '192.168.48.238'
port = 22000

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
while True:
    #send button number to server
    print ("enter button number (1 or 2)")
    Input = input()
    ClientMultiSocket.send(str.encode(Input))
    #receive response from server
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))
    time.sleep(3)

ClientMultiSocket.close()


