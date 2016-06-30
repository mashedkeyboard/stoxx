import sys, time, socket
from _thread import *
import localfunctions

stoxxver = "0.0.3"
 
HOST = ''
PORT = 1785

print('------------------------------')
print("Welcome to StoXXServer " + stoxxver)
print('------------------------------')
time.sleep(1)
print('Database configuration in progress')
localfunctions.dbSetup()
time.sleep(1)
print('Database configuration successful')
time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created on port ' + str(PORT))

 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete to port ' + str(PORT))

time.sleep(1)

#Start listening on socket
s.listen(10)
print('Socket now listening on ' + socket.gethostbyname(socket.gethostname()))
 
#Function for handling connections. This will be used to create threads
def clientthread(conn,addr):
    try:
        isstart = 1
        sendstr = "EHLO stoxxserv " + stoxxver
        while 1:
            conn.send(bytes(sendstr, 'utf-8'))
            data = conn.recv(512).decode("utf-8")
            if ('EHLO' in data and isstart == 1):
                isstart = 2
                sendstr = "BLOK CONN ESTB"
            elif (isstart != 1):
                if ('HELP' in data):
                    sendstr = "EHLO issues a hello command to the server.\nVER gets the version from the server.\nLISTSTOK gets a list of the stock from the server.\nADDSTOK starts the addition of stock to the server.\nSRCSTOK searches the stock server."
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
                elif("SRCSTOK" in data):
                    stkdat = localfunctions.srcStock(conn)
                    if (stkdat):
                        sendstr = "STK RTRN ARRINF " + stkdat
                    else:
                        sendstr = "STK NOT FOUND"
                else:
                    sendstr = "500 INVAL CMD"
            else:
                    sendstr = "500 INVAL CMD AT POS"
       
    except ConnectionResetError:
        print("Client on " + addr[0] + ':' + str(addr[1]) + " disconnected")
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,addr,))
 
s.close()