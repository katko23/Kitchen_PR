# Python 3 server example
import json
import socket,Setings
import threading
from threading import Thread
import Items_Table
from flask import Flask, render_template, request, url_for, jsonify
import Orders_Table
hostName = Setings.serverName
serverPort = Setings.this_serverPort

class Server(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = Flask(__name__)

        @app.route('/order', methods=['POST'])
        def my_test_endpoint():
            input_json = request.get_json(force=True)
            # force=True, above, is necessary if another developer
            # forgot to set the MIME type to 'application/json'
            print('data from client:', input_json)
            serverLock = threading.Lock()
            serverLock.acquire()
            Orders_Table.Order_Table.orders_lock.acquire()
            Orders_Table.Order_Table.orders.append(input_json)
            Orders_Table.Order_Table.received_orders.append(1)
            Orders_Table.Order_Table.orders_lock.release()
            serverLock.release()
            print("Append raw orders to the queue")
            dictToReturn = {'Plates_on_prepairing': len(Items_Table.items_to_make + Items_Table.items_making + Items_Table.items_inoven + Items_Table.items_instove)}
            return jsonify(dictToReturn)


        app.run(host=hostName,port=serverPort,debug=False)
        # sock = socket.socket()  # socket creation
        # sock.bind((hostName, serverPort))  # socket binding on LAN
        # sock.listen(4096)  # server a listen
        #
        # print('socket is listening')
        #
        # while True:
        #     c, addr = sock.accept()
        #     print('got connection from ', addr)
        #
        #     jsonReceived = c.recv(1024).decode('utf-8')
        #     recvs = self.data_received(jsonReceived)
        #     ordersLock = threading.Lock()  # create a mutex
        #     ordersLock.acquire()
        #     Cooking.Cooking.orders.append(recvs)
        #     ordersLock.release()
        #     print("Json received -->\n", jsonReceived,"\n")
        #
        #     c.close()

    # def data_received(self,temp):
    #     string = temp.split("\n")
    #     for i in range(6):
    #         string.pop(0)
    #     dictionary = dict()
    #     for i in string:
    #         words = i.split(":")
    #         secondWord = str(words[1]).split(",")
    #         if(len(words) > 0):
    #             dictionary.update({str(words[0]) : str(secondWord[0])})
    #     return dictionary

