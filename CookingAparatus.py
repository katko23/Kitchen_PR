import threading
import Setings
import oven,stove

lock = threading.Lock()
ovens = Setings.nr_of_ovens
stoves = Setings.nr_of_stoves

ovens_l = []
items_oven_l = []
stoves_l = []
items_stove_l = []
ovens_items = []
stoves_items = []

def Items_inoven_append(id_cook,item):
    with lock:
        tempcell = []
        tempcell.append(item)
        tempcell.append(id_cook)
        items_oven_l.append(tempcell)
        ovens_items.append(item)

def Items_instove_append(id_cook,item):
    with lock:
        tempcell = []
        tempcell.append(item)
        tempcell.append(id_cook)
        items_stove_l.append(tempcell)
        stoves_items.append(item)

def Items_inoven_pop(index):
    with lock:
        items_oven_l.pop(index)
        ovens_items.pop(index)


def Items_instove_pop(index):
    with lock:
        items_stove_l.pop(index)
        stoves_items.pop(index)

def Start():
    for i in range(ovens):
        ovenThread = oven.Oven_C()
        ovens_l.append(ovenThread)
        ovenThread.start()

    for i in range(stoves):
        stoveThread = stove.Stove_C()
        stoves_l.append(stoveThread)
        stoveThread.start()