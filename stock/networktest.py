# TCP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("10.64.109.245", 1785))
while 1:
    data = client_socket.recv(512).decode("utf-8")
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:
        print ("RECIEVED:" , data)
        data = input ( "SEND( TYPE q or Q to Quit):" )
        if (data != 'Q' and data != 'q'):
            client_socket.send(bytes(data, 'UTF-8'))
        else:
            client_socket.send(bytes(data, 'UTF-8'))
            client_socket.close()
            break