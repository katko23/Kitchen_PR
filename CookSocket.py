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
        self.items_maded = []
        self.cook_lock = threading.Lock()
        self.cooking_threads = []


    cookingLock = threading.RLock()
    selectLock = threading.RLock()
    receivingLock = threading.Lock()

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
        import Items_Table
        import CookingAparatus
        while True:
            self.select_items()


            # print("\n Items making real",Items_Table.items_making,"\n Items to make real",Items_Table.items_to_make,"\n");
            # if ((len(Items_Table.items_making[self.id_cook - 1]) - self.proficiency ) == 0) or (len(Items_Table.items_to_make) == 0):
            if (len(Items_Table.items_making[self.id_cook - 1]) != 0) or (len(Items_Table.items_to_make) == 0):

                # print("enter to cooking");
                for index,c in enumerate(cooking_list , start=1):
                    # print(len(c.items))
                    if (len(c.items) == 0 and len(Items_Table.items_making[self.id_cook - 1]) >= index):
                        # Items_Table.lock.acquire()
                        print('Cooking one item from cooking list',Items_Table.items_making[self.id_cook - 1])
                        with Items_Table.lock:
                            item_Now = Items_Table.items_making[self.id_cook - 1].pop(0)
                        # Items_Table.items_making[self.id_cook - 1].append(item_Now)
                        if Plates.plates[item_Now]['cooking-apparatus'] == "null":
                            Items_Table.Items_making_append(self.id_cook - 1, item_Now)
                            # Items_Table.lock.release()
                            c.cookingLock.acquire()
                            c.items.append(item_Now)
                            # print(c.items)
                            c.cookingLock.release()
                        elif Plates.plates[item_Now]['cooking-apparatus'] == "oven":
                            print("In Oven",CookingAparatus.ovens_items,CookingAparatus.ovens_l)
                            CookingAparatus.Items_inoven_append(self.id_cook - 1, item_Now)
                            # Items_Table.lock.release()
                        elif Plates.plates[item_Now]['cooking-apparatus'] == "stove":
                            print("In Stove",CookingAparatus.stoves_items,CookingAparatus.stoves_l)
                            CookingAparatus.Items_instove_append(self.id_cook - 1, item_Now)
                            # Items_Table.lock.release()


                        # self.cookFunc()
                    # if (len(c.items) == 0 and len(Items_Table.items_making[self.id_cook - 1]) >= index):
                    #     # Items_Table.lock.acquire()
                    #     print('Cooking one item from cooking list',Items_Table.items_making[self.id_cook - 1])
                    #     item_Now = Items_Table.items_making[self.id_cook - 1][index]
                    #     # Items_Table.items_making[self.id_cook - 1].append(item_Now)
                    #     # Items_Table.Items_making_append(self.id_cook-1,item_Now)
                    #     # Items_Table.lock.release()
                    #     c.cookingLock.acquire()
                    #     c.items.append(item_Now)
                    #     print(c.items)
                    #     c.cookingLock.release()
                    #     # self.cookFunc()




    def select_items(self):
        #from main import order_Table
        #print("Cook taking the items")
        # self.selectLock.acquire()
        import Items_Table
        # print(Items_Table.items_to_make)
        # items_to_make = Items_Table.items_to_make
        # self.cookingLock.release()
        # if(items_to_make != None):
        #     x = len(items_to_make)
        # else:
        #     x = 0
        #if x>0: print(items_to_make)
        index = 0
        # with Items_Table.lock:
        # Items_Table.lock.acquire()

        if ((self.proficiency - len(Items_Table.items_making[self.id_cook - 1])) > 0) and (len(Items_Table.items_to_make) > 0):
            # print("Enter to select items")
            b = True
            while b :
                self.selectLock.acquire()
                if len(Items_Table.items_to_make) > 0:
                    item = Items_Table.items_to_make[0]
                if index <= len(Items_Table.items_to_make) - 1:
                    tmp = Items_Table.items_to_make.copy()
                    item = Items_Table.items_to_make[index]
                else:
                    index = 0

                if (self.rank == 1) and len(Items_Table.items_to_make) > 0:
                    if Plates.plates[item]['complexity'] == 1:
                        # with Items_Table.lock:
                        # Items_Table.lock.acquire()
                        # Items_Table.items_making[self.id_cook - 1].append(item)
                        # Items_Table.items_to_make.pop(index)
                        # Items_Table.lock.release()
                        Items_Table.Items_making_append_begin(self.id_cook - 1, item)
                        b = False
                        Items_Table.Items_to_make_pop(index)
                        print(".", Items_Table.items_to_make)
                        index = 0
                    else:
                        index = index + 1

                if (self.rank == 2) and len(Items_Table.items_to_make) > 0:
                    if (Plates.plates[item]['complexity'] == 1) or (Plates.plates[item]['complexity'] == 2):
                        # with Items_Table.lock:
                        # Items_Table.lock.acquire()
                        # Items_Table.items_making[self.id_cook - 1].append(item)
                        # Items_Table.items_to_make.pop(index)
                        # Items_Table.lock.release()
                        Items_Table.Items_making_append_begin(self.id_cook - 1, item)
                        b = False
                        Items_Table.Items_to_make_pop(index)
                        print("..", Items_Table.items_to_make)
                        index = 0
                    else:
                        index = index + 1

                if (self.rank == 3) and len(Items_Table.items_to_make) > 0:
                    # with Items_Table.lock:
                    # Items_Table.lock.acquire()
                    # Items_Table.items_making[self.id_cook - 1].append(item)
                    # Items_Table.items_to_make.pop(index)
                    # Items_Table.lock.release()
                    Items_Table.Items_making_append_begin(self.id_cook - 1, item)
                    b = False
                    Items_Table.Items_to_make_pop(index)
                    print("...", Items_Table.items_to_make)
                    index = 0

                if len(Items_Table.items_to_make) == 0 :
                    b = False
                if len(Items_Table.items_to_make) > 0:
                    print("\n", item, "\n")
                print("Items to make", Items_Table.items_to_make, self.id_cook)
                print("Items making", Items_Table.items_making, self.id_cook)
                x = len(Items_Table.items_to_make)
                self.selectLock.release()
        # Items_Table.lock.release()

    def cookFunc(self):
        from R1Kitchen import order_Table
        order_Table.items_done_lock.acquire()
        for item in self.items_maded:
            order_Table.add_items_done(item)
        order_Table.items_done_lock.release()


