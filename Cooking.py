import threading
import time
from threading import Thread
import Plates
import Setings


class Cooking_C(Thread):

    def __init__(self, id_cook):
        Thread.__init__(self)
        self.items = []
        self.id_cks = id_cook

    def run(self):
        while True:
            if len(self.items) > 0:
                print("Cooking the food")
                self.cooking(self.items, self.id_cks - 1)
                self.items.clear()


    cookingLock = threading.Lock()

    def cooking(self, items, id_cks):
        item_temp = []
        item_temp.append(items[0])
        item_id = items[0]
        item_temp.append(0)
        cookingTime = Plates.plates[item_id]['preparation-time']
        time.sleep(cookingTime * Setings.timeUnit)
        #Orders_Table.delete_item(item_id, Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        #print("Update the list of items what cook made " , Cooks_Hiring.cooks[id_cks].items_making[id_cks])
        item_temp[1] = id_cks + 1
        if len(item_temp) > 1 :
            # print(order_Table.items_done,'\n\n')
            # print('items = ' , item_temp)
            # self.cookingLock.acquire()
            import Items_Table

            # with Items_Table.done_lock:
            temptemp = []
            temptemp.extend(item_temp)
            temptemp = item_temp[:]
            # Items_Table.lock.acquire()
            # Items_Table.items_done.append(temptemp)
            # Items_Table.lock.release()
            Items_Table.Items_done_append(temptemp)
            self.delete_cook_item(id_cks, item_id)

            # self.cookingLock.release()
            print(Items_Table.items_done)
            item_temp.clear()


        #print("add to the items that is done , the items that cook has make ", Orders_Table.Order_Table.items_done,'\n')
        #time.sleep(0.05)
        #print("Now I have order= ",order_Table.items_done,"  cook = ",Cooks_Hiring.cooks[id_cks].items_maded)


    def delete_cook_item(self,id_cks,item_id):
        import Items_Table
        for i in range(len(Items_Table.items_making[id_cks])):
            if Items_Table.items_making[id_cks][i] == item_id:
                # Items_Table.lock.acquire()
                # Items_Table.items_making[id_cks].pop(i)
                Items_Table.Items_making_pop(id_cks,i)
                print("Cooking items making = " , Items_Table.items_making)
                # Items_Table.lock.release()
                return



