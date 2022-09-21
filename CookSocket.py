import random
import threading
import time,datetime
import Setings
from threading import Thread
import Cooking,Randoms
import Plates



class Cook(Thread):
    def __init__(self,id,rank,proficiency):
        Thread.__init__(self)
        self.id_cook = id
        self.rank = rank
        self.proficiency = proficiency
        self.name = Randoms.Names[random.randint(0,7)] + ' ' + Randoms.Surname[random.randint(0,7)]
        self.catch_phrase = Randoms.CatchPhrase[random.randint(0,7)]

        self.cooking_threads = []

    items_making = []
    cookingLock = threading.Lock()

        #print("order of  waiter :")
        #print(o_l)

    def run(self):
        print("initialize list of threads that can one cook make at a time")
        cooking_list = []

        for i in range(self.proficiency):
            cookingThread = Cooking.Cooking_C(self.id_cook)
            cooking_list.append(cookingThread)
            cookingThread.start()
        printing = 1

        while True:
            self.select_items()
            # if len(self.items_making[self.id_cook-1]) > 0 :
            #     if printing > 0 :
            #         print("Cook ", self.name, " has ", self.items_making[self.id_cook-1])
            #         printing = printing - 1
            for c in cooking_list:
                if (len(c.items) == 0 and len(self.items_making[self.id_cook - 1]) > 0):
                    item_Now = self.items_making[self.id_cook-1].pop(0)
                    c.items.append(item_Now)




    def select_items(self):
        from main import order_Table
        import Orders_Table
        index = 0
        #print("Cook taking the items")
        checkLock = threading.Lock()
        checkLock.acquire()
        order_Table.order_receiving()
        items_to_make = order_Table.items_to_make
        checkLock.release()
        if(items_to_make != None):
            x = len(items_to_make)
        else:
            x = 0
        #if x>0: print(items_to_make)
        while ((self.proficiency - len(self.items_making[self.id_cook-1])) > 0) and ( x > 0):

            if index<len(order_Table.items_to_make):item = order_Table.items_to_make[index]
            else:index = 0

            if (self.rank == 1):
                if Plates.plates[item]['complexity'] == 1:
                    self.items_making[self.id_cook-1].append(item)
                    checkLock.acquire()
                    order_Table.items_to_make.pop(index)
                    checkLock.release()
                    index = 0
                else:
                    index = index + 1

            if (self.rank == 2):
                if (Plates.plates[item]['complexity'] == 1) or (Plates.plates[item]['complexity'] == 2):
                    self.items_making[self.id_cook-1].append(item)
                    checkLock.acquire()
                    order_Table.items_to_make.pop(index)
                    checkLock.release()
                    index = 0
                else:
                    index = index + 1

            if (self.rank == 3):
                self.items_making[self.id_cook-1].append(item)
                checkLock.acquire()
                order_Table.items_to_make.pop(index)
                checkLock.release()
                index = 0

            checkLock.acquire()
            x = len(order_Table.items_to_make)
            checkLock.release()





        # body_bytes = self.body.encode('ascii')
        # header_bytes = self.headers.format(
        #     content_type="application/json",
        #     content_length=len(body_bytes),
        #     host=str(self.host) + ":" + str(self.port)
        # ).encode('iso-8859-1')
        #
        # payload = header_bytes + body_bytes
        #
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((self.host, self.port))
        #
        # s.sendall(payload)
        # print(s.recv(1024))

