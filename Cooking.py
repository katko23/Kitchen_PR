import threading
import time
from threading import Thread
import Plates
import Setings

cookingLock = threading.Lock()

class Cooking_C(Thread):

    def __init__(self, id_cook):
        Thread.__init__(self)
        self.items = []
        self.id_cks = id_cook

    def run(self):
        while True:
            if len(self.items) > 0:
                print("Cooking the food")
                self.cooking(self.items, self.id_cks-1)
                self.items.clear()



    def cooking(self, items, id_cks):
        global cookingLock
        import Cooks_Hiring
        import Orders_Table
        from main import order_Table
        item_id = items[0]
        items.append(0)
        cookingTime = Plates.plates[item_id]['preparation-time']
        time.sleep(cookingTime * Setings.timeUnit)
        #Orders_Table.delete_item(item_id, Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        #print("Update the list of items what cook made " , Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        items[1] = id_cks + 1
        if len(items)>0 :
            print(order_Table.items_done,'\n\n')
            print('items = ' , items)

            Cooks_Hiring.cooks[id_cks].cook_lock.acquire()
            Cooks_Hiring.cooks[id_cks].items_maded.append(items)
            Cooks_Hiring.cooks[id_cks].cook_lock.release()
        print("add to the items that is done , the items that cook has make ", Orders_Table.Order_Table.items_done,'\n')
        # time.sleep(0.5)
        print("Now I have = ",order_Table.items_done)






