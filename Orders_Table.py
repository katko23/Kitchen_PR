import threading
from operator import itemgetter
from threading import Thread
import Setings
import requests
import time
from CookSocket import Cook

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
    funcLock = threading.Lock()
    funcLock.acquire()
    for i in range(len(list_search_elem)):
        if search_item(list_search_elem[i], list_where_search) == False : return False

    funcLock.release()
    return True

def delete_item(old_item, items_list):

    for i in range(len(items_list)):
        if items_list[i] == old_item:
            items_list.pop(i)
            return items_list

def delete_items(list_old_items, items_list):

    for i in range(len(list_old_items)):
        delete_item(list_old_items[i], items_list)

    return items_list

def delete_items_d(list_old_items, items_list):

    for i in range(len(list_old_items)):
        delete_item(list_old_items[i][0], items_list)

    return items_list

def delete_item_o(old_item, items_list):
    funcLock = threading.Lock()
    funcLock.acquire()
    for i in range(len(items_list)):
        if items_list[i][0] == old_item:
            items_list.pop(i)
            funcLock.release()
            return items_list
    return items_list
    funcLock.release()

def delete_items_o(list_old_items, items_list):
    for i in range(len(list_old_items)):
        items_list = delete_item_o(list_old_items[i],items_list)
    return items_list

class Order_Table(Thread):
    def __init__(self):
        Thread.__init__(self)




    host = Setings.hostName
    port = Setings.serverPort
    body = ""

    items_to_make = []
    items_update = []
    items_done = []
    orders = []
    orders_making = []
    orders_done = []
    items_to_make_lock = threading.RLock()
    items_done_lock = threading.RLock()
    orders_lock = threading.RLock()
    lockReceive = threading.RLock()
    received_orders = []


    def run(self):
        import CookingAparatus
        CookingAparatus.Start()

        while True:
            import Items_Table,CookSocket
            CookSocket.Cook.receivingLock.acquire()

            self.order_sender()
            for o in self.orders_done.copy():
                print("order_done = ", o)
                self.send_item(o)
                self.orders_done.remove(o)

            while(len(self.received_orders) > 0):
                self.received_orders.pop(0)
                self.order_receiving()
                self.item_sort()
                with Items_Table.lock:
                    print("Sending to items to make")
                    Items_Table.items_to_make = self.items_to_make.copy()
                    self.items_done = Items_Table.items_done
            # self.orders = []
            # self.item_sort()
            CookSocket.Cook.receivingLock.release()
            # with Items_Table.lock:



                # print(Items_Table.items_done)
                # print(Items_Table.items_to_make)


            #print(self.items_to_make)


            # # stergem toate itemurile care au fost realizate dar inca nu au fost trimise
            # delete_items(self.items_done, self.items_to_make)
            # if (len(self.items_done) > 0):
            #     print("\n Items done ", self.items_done, '\n')
            #     self.order_sender()
            #transmitem orderurile terminate




    def send_item(self,items):
        import json
        dictToSend = items
        if 'waiter_id' not in dictToSend:
            dictToSend['restaurant_id'] = Setings.restaurant_id
        res = requests.post("http://" + str(self.host) + ":" + str(self.port) + "/distribution", json=dictToSend)
        print('response from server:', res.text)
        dictFromServer = res.json()

    def order_sender(self):
        f = {}
        # global orders, orders_raw, items_to_make, items_done
        for item in self.orders_making.copy():
            if item == {}:
                self.orders_making.remove(item)
            f = self.orders_making[0]
        # for f in self.orders_making:
            # if len(self.items_to_make)>0:print('\n\n',self.items_to_make,"\n\n")
            # print("items = ",f['items'],self.items_done)
        if(f != {}):
            if search_items(f['items'], self.items_done):
                print("\n\n", "enter to order sender", "\n\n")
                print(f['items'], self.items_done)
                items_sending_l = []
                for o in f['items']:
                    items_sending = {}
                    items_sending['food_id'] = o
                    if search_item(o, self.items_done):
                        print("location = ", give_loc_item(o, self.items_done))
                        temp_i = self.items_done[give_loc_item(o, self.items_done)].copy()
                        items_sending['cook_id'] = temp_i[1]
                    items_sending_l.append(items_sending)
                self.items_done = delete_items_o(f['items'], self.items_done)
                f['cooking_time'] = time.time() - f['pick_up_time']
                f['cooking_details'] = items_sending_l
                temp = f.copy()
                self.orders_done.append(temp)
                self.orders_making.pop(0)
                self.orders.pop(0)
        for item in self.orders_making.copy():
            if item == {}:
                self.orders_making.remove(item)
        for item in self.orders.copy():
            if item == {}:
                self.orders.remove(item)


    def order_receiving(self):
        # sortam orderurile noi in dependenta de priority si le bagam in spatele listei
        if len(self.orders) > 0:
            # print("Enter to order_receiving")
            self.orders_lock.acquire()
            orders_raw_sorted = []
            orders_raw_sorted.extend(self.orders)
            # print(orders_raw_sorted)
            orders_raw_sorted = sorted(orders_raw_sorted, key=itemgetter('priority'), reverse=True)
            orders_raw_sorted = sorted(orders_raw_sorted, key=itemgetter('pick_up_time'))
            self.orders.clear()
            for o in orders_raw_sorted:
                self.orders.append(o)
            self.orders_lock.release()



    def add_items_to_make(self, new_items):
        funcLock = threading.Lock()
        funcLock.acquire()
        self.items_to_make = self.items_to_make + new_items
        funcLock.release()

    def add_items_done(self, new_items):
        funcLock = threading.Lock()
        funcLock.acquire()
        if(self.items_done == []):
            self.items_done.clear()
        self.items_done.append(new_items)
        funcLock.release()

    def item_sort(self):
        import Items_Table,CookingAparatus
        # self.items_to_make_lock.acquire()
        # self.items_to_make.clear()
        # Items_Table.lock.acquire()
        if (self.orders is not None):
            # print("item sort")
            self.items_to_make.clear()
            self.orders_making.clear()
            # print("item sort i to make =",Items_Table.items_to_make)
            # self.items_to_make = self.items_to_make + Items_Table.items_to_make.copy()
            for f in self.orders:
                # print("\n\n Data in order ",f, '\n\n')
                self.items_to_make = self.items_to_make + f['items']
                # print("Send all the items from orders to the Items_to_make list")
            self.orders_making = self.orders_making + self.orders
            with Items_Table.lock:
                temp_items_making = Items_Table.items_making.copy()
                temp_items_done = Items_Table.items_done.copy()
            with CookingAparatus.lock:
                temp_items_oven = CookingAparatus.ovens_items
                temp_items_stove = CookingAparatus.stoves_items
            # print("orders making = ", self.orders_making)
            # print("Items making = ", temp_items_making)
            # print("Items done = ", temp_items_done)
            for j in temp_items_making:
                delete_items(j, self.items_to_make)
            for j in temp_items_done:
                delete_item(j[0], self.items_to_make)
            for j in temp_items_oven:
                delete_item(j, self.items_to_make)
            for j in temp_items_stove:
                delete_item(j, self.items_to_make)
        # self.items_to_make_lock.release()
        # Items_Table.lock.release()

