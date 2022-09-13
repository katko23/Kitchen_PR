# Python 3 server example
import json
import socket,Setings
import threading
from threading import Thread
import Cooking

hostName = Setings.serverName
serverPort = Setings.this_serverPort

class Server(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sock = socket.socket()  # socket creation
        sock.bind((hostName, serverPort))  # socket binding on LAN
        sock.listen(4096)  # server a listen

        print('socket is listening')

        while True:
            c, addr = sock.accept()
            print('got connection from ', addr)

            jsonReceived = c.recv(1024).decode('utf-8')
            recvs = self.data_received(jsonReceived)
            ordersLock = threading.Lock()  # create a mutex
            ordersLock.acquire()
            Cooking.orders.append(recvs)
            ordersLock.release()
            print("Json received -->\n", jsonReceived,"\n")

            c.close()

    def data_received(self,temp):
        string = temp.split("\n")
        for i in range(6):
            string.pop(0)
        dictionary = dict()
        for i in string:
            words = i.split(":")
            secondWord = str(words[1]).split(",")
            if(len(words) > 0):
                dictionary.update({str(words[0]) : str(secondWord[0])})
        return dictionary

