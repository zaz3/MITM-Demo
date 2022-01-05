import socket
import os
from _thread import *
import RPi.GPIO as GPIO

# set up server side socket
ServerSideSocket = socket.socket()
ServerSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '192.168.48.238'
port = 22000
ThreadCount = 0

#initialize RPi GPIO
button1 = 24
button2 = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.OUT)
GPIO.setup(button2, GPIO.OUT)

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

# process connection from client
def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        #receive data from client
        data = connection.recv(2048)
        cmd = data.decode()
        print ("Received command: " + str(cmd) + " len: " + str(len(cmd)))
        # server toggles button1 and button2 based on request from client
        if cmd == "1":
            if GPIO.input(button1) == GPIO.LOW:
              GPIO.output(button1,1)
              data = "Button1 pressed"
            else:
              GPIO.output(button1,0)
              data = "Button1 released"
        if cmd == "2":
            if GPIO.input(button2) == GPIO.LOW:
                GPIO.output(button2,1)
                data = "Button2 pressed"
            else:
                GPIO.output(button2,0)
                data = "Button2 released"
        print (data)
        response = 'Server message: ' + data
        if not data:
            break
        #send message to client
        connection.sendall(str.encode(response))
    connection.close()

while True:
    #accept connection from client and start a thread
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
