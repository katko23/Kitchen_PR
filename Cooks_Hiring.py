import random
import CookSocket, Setings

cooks = []

for i in range(Setings.nr_of_line_cooks):
    cook = CookSocket.Cook(len(cooks)+1, 1, random.randint(1, 3))
    cook.start()
    items = []
    cook.items_making.append(items)
    cooks.append(cook)

for i in range(Setings.nr_of_saucier):
    cook = CookSocket.Cook(len(cooks)+1, 2, random.randint(2, 4))
    cook.start()
    items = []
    cook.items_making.append(items)
    cooks.append(cook)

for i in range(Setings.nr_of_chef_cooks):
    cook = CookSocket.Cook(len(cooks)+1, 3, random.randint(3, 4))
    cook.start()
    items = []
    cook.items_making.append(items)
    cooks.append(cook)
