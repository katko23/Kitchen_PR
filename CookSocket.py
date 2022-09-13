import socket
import threading

import Setings
import time,datetime
from threading import Thread
import Cooking


class Cook(Thread):
    def __init__(self,id):
        Thread.__init__(self)
        self.id_cook = id

        #print("order of  waiter :")
        #print(o_l)

    def run(self):
        while True:
            queueLock = threading.Lock()  # create a mutex
            queueLock.acquire()  # stop others thread
            if (len(Cooking.orders_done) > 0):
                cook_order_list = Cooking.orders_done.pop(0)
                self.setbody(cook_order_list)
                self.send_item()
            queueLock.release()  # resume other threads


    host = Setings.hostName
    port = Setings.serverPort
    headers = """\
    POST /order HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""
    body = ""


    def setbody(self,items):
        if len(Cooking.orders_done)>0:
            self.body = Cooking.orders_done[0] + \
                        '    {' \
                        '"food_id": 3,' \
                        '"cook_id": 1,' \
                        '},' \
                        '{' \
                        '"food_id": 4,' \
                        '"cook_id": 1,' \
                        '},' \
                        '{' \
                        '"food_id": 4,' \
                        '"cook_id": 2,' \
                        '},' \
                        '{' \
                        '"food_id": 2,' \
                        '"cook_id": 3,' \
                        '},' \
                        ']'

    def send_item(self):
        body_bytes = self.body.encode('ascii')
        header_bytes = self.headers.format(
            content_type="application/json",
            content_length=len(body_bytes),
            host=str(self.host) + ":" + str(self.port)
        ).encode('iso-8859-1')

        payload = header_bytes + body_bytes

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        s.sendall(payload)
        print(s.recv(1024))

