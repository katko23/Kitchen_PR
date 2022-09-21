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
        cookingLock.acquire()  # stop
        #Orders_Table.delete_item(item_id, Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        #print("Update the list of items what cook made " , Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        items[1] = id_cks + 1
        if len(items)>0 :
            print(order_Table.items_done,'\n\n')
            print('items = ' , items)
            order_Table.add_items_done(items)
        print("add to the items that is done the item that cook has made now ", Orders_Table.Order_Table.items_done,'\n')
        cookingLock.release()  # release
        print("Now I have = ",order_Table.items_done)






