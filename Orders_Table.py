import threading
from operator import itemgetter
from threading import Thread
import Setings
import requests
import time


def search_item(elem, list_where_search):
    funcLock = threading.Lock()
    funcLock.acquire()
    if isinstance(list_where_search, list):
        for i in list_where_search:
            if i[0] == elem:
                funcLock.release()
                return True
    else:
        for i in list_where_search:
            if i == elem:
                funcLock.release()
                return True
    funcLock.release()
    return False

def give_loc_item(elem, list_where_search):
    funcLock = threading.Lock()
    funcLock.acquire()
    for i in range(len(list_where_search)):
        if list_where_search[i][0] == elem:
            funcLock.release()
            return i
    funcLock.release()

def search_items(list_search_elem, list_where_search):
    for i in range(len(list_where_search)):
        if search_item(list_search_elem[i], list_where_search) == False : return False
    return True

def delete_item(old_item, items_list):
    funcLock = threading.Lock()
    funcLock.acquire()
    for i in range(len(items_list)):
        if items_list[i] == old_item:
            items_list.pop(i)
            funcLock.release()
            return items_list
    funcLock.release()

def delete_items(list_old_items, items_list):
    for i in range(len(list_old_items)):
        delete_item(list_old_items[i], items_list)
    return items_list

def delete_item_o(old_item, items_list):
    funcLock = threading.Lock()
    funcLock.acquire()
    for i in range(len(items_list)):
        if items_list[i][0] == old_item:
            items_list.pop(i)
            funcLock.release()
            return items_list
    funcLock.release()

def delete_items_o(list_old_items, items_list):
    for i in range(len(list_old_items)):
        delete_item_o(list_old_items[i], items_list)

class Order_Table(Thread):
    def __init__(self):
        Thread.__init__(self)


    host = Setings.hostName
    port = Setings.serverPort
    body = ""

    orders_raw = []
    items_to_make = []
    items_update = []
    items_done = []
    orders = []
    orders_making = []
    orders_done = []
    items_to_make_lock = threading.Lock()
    received_orders = []

    def run(self):
        while True:
            while(len(self.received_orders) > 0):
                lockReceive = threading.Lock()
                lockReceive.acquire()
                self.received_orders.pop(0)
                self.order_receiving()
                print(self.items_to_make)
                lockReceive.release()


            # # stergem toate itemurile care au fost realizate dar inca nu au fost trimise
            # delete_items(self.items_done, self.items_to_make)
            # if (len(self.items_done) > 0):
            #     print("\n Items done ", self.items_done, '\n')
            #     self.order_sender()
            #transmitem orderurile terminate
            for o in self.orders_done:
                self.send_item(o)


    def send_item(self,items):
        dictToSend = self.body
        res = requests.post("http://" + str(self.host) + ":" + str(self.port) + "/distribution", json=dictToSend)
        print('response from server:', res.text)
        dictFromServer = res.json()

    def order_sender(self):
        # global orders, orders_raw, items_to_make, items_done
        for f in self.orders:
            # if len(self.items_to_make)>0:print('\n\n',self.items_to_make,"\n\n")
            if search_items(f['items'], self.items_done):
                items_sending_l = []
                for o in f['items']:
                    items_sending = {}
                    items_sending['food_id'] = o
                    if search_item(o, self.items_done):
                        items_sending['cook_id'] = self.items_done[give_loc_item(o, self.items_done)][1]
                    items_sending_l.append(items_sending)
                self.items_done = delete_items_o(f['items'], self.items_done)
                f['cooking_time'] = time.time() - f['pick_up_time']
                f['cookind_details'] = items_sending_l
                self.orders_done.append(f)

    def order_receiving(self):
        # sortam orderurile noi in dependenta de priority si le bagam in spatele listei
        if len(self.orders_raw) > 0:
            orders_raw_sorted = []
            orders_raw_sorted.append(self.orders_raw.pop(0))
            orders_raw_sorted = sorted(orders_raw_sorted, key=itemgetter('priority'), reverse=True)
            if (self.orders != None):
                # if (len(orders_raw_sorted) > 0): print(orders_raw_sorted)
                # print("Extend order by new sorted orders by priority")
                self.orders = self.orders + orders_raw_sorted
                orders_raw_sorted.clear()

        # alegem primele orderuri din orders si itemurile dinauntru le transmitem in lista itemurilor to make
        # if self.orders != None:
        #     if len(self.orders) > 0 : print(self.orders)
        self.items_to_make_lock.acquire()
        self.items_to_make.clear()
        if (self.orders is not None):
            for f in self.orders:
                # print("\n\n Data in order ",f, '\n\n')
                self.items_to_make = self.items_to_make + f['items']
                # print("Send all the items from orders to the Items_to_make list")

            # print(self.items_to_make)
        #print(self.items_to_make,' ', self.orders)
        # print("Deleting all the done items")
        # stergem toate itemurile care au fost realizate dar inca nu au fost trimise
        # if len(self.items_to_make) > 0:
        #     self.items_to_make = delete_items(self.items_done, self.items_to_make)
        if (len(self.items_done) > 0):
            print("\n Items done ", self.items_done, '\n')
            self.order_sender()
        self.items_to_make_lock.release()

    def add_items_to_make(self, new_items):
        funcLock = threading.Lock()
        funcLock.acquire()
        self.items_to_make = self.items_to_make + new_items
        funcLock.release()

    def add_items_done(self, new_items):
        funcLock = threading.Lock()
        funcLock.acquire()
        self.items_done.append(new_items)
        funcLock.release()
