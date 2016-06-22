import socket
import sys
from _thread import *
import localfunctions
import time

stoxxver = "0.0.1rc1"
 
HOST = ''
PORT = 1785

localfunctions.dbSetup()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created on port ' + str(PORT))
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete to port ' + str(PORT))
print('Connection test in progress')
result = s.connect_ex((HOST,PORT))
time.sleep(1)
if result == 0:
    print("Connection successful")
else:
    print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\')
    print("WARNING: Can't connect locally")
    print('\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')

time.sleep(1)
#Start listening on socket
s.listen(10)
print('Socket now listening on ' + socket.gethostbyname(socket.gethostname()))
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    isstart = 1
    sendstr = "EHLO stoxxserv " + stoxxver
    while 1:
        conn.send(bytes(sendstr, 'UTF-8'))
        data = conn.recv(512).decode("utf-8")
        if ('EHLO' in data and isstart == 1):
            isstart = 2
            sendstr = "BLOK CONN ESTB"
        elif ('HELP' in data):
                sendstr = "EHLO issues a hello command to the server.\nVER gets the version from the server.\nLISTSTOK gets a list of the stock from the server.\nADDSTOK starts the addition of stock to the server."
        elif (isstart != 1):
            if ('HELP' in data):
                sendstr = "EHLO issues a hello command to the server.\nVER gets the version from the server.\nLISTSTOK gets a list of the stock from the server.\nADDSTOK starts the addition of stock to the server."
            elif ("VER" in data):
                sendstr = stoxxver
            elif("LISTSTOK" in data):
                sendstr = localfunctions.listStock()
            elif("ADDSTOK" in data):
                stkid = localfunctions.addStock(conn)
                if (stkid):
                    sendstr = "STK ADDED ID " + stkid
                else:
                    sendstr = "STK NOT ADDED"
            else:
                sendstr = "500 INVAL CMD"
        else:
                sendstr = "500 INVAL CMD AT POS"
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
