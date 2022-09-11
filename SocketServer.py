# Python 3 server example
import socket

hostName = "127.12.12.128"
serverPort = 27003


sock = socket.socket() #socket creation
sock.bind((hostName,serverPort)) # socket binding on LAN
sock.listen(4096) #server a listen

print('socket is listening')

while True:
    c, addr = sock.accept()
    print('got connection from ', addr)

    jsonReceived = c.recv(1024)
    print("Json received -->", jsonReceived)

    c.close()