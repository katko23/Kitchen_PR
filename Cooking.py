import threading
import time
from threading import Thread
import Plates


orders = []
orders_done = []

class Cooking(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            self.cooking()

    def cooking(self):
        if(len(orders)>0):
            last_ord_mutex = threading.Lock()  # create a mutex
            last_ord_mutex.acquire()  #stop
            last_order = orders.pop(0)
            print(orders)
            orders_done.append(last_order)
            last_ord_mutex.release() #release
            cookingTime = int(last_order['"max_wait"'])
            print("\n\n",cookingTime,"\n\n")
            time.sleep(cookingTime * 0.1)

