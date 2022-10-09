import threading

lock = threading.Lock()
done_lock = threading.RLock()

items_to_make = []
items_done = []
items_making = []
items_inoven = [[]] * 3
items_instove = [[]] * 3

def Items_inoven_append(id_cook,item):
    with lock:
        items_inoven[id_cook].append(item)

def Items_instove_append(id_cook,item):
    with lock:
        items_instove[id_cook].append(item)


def Items_inoven_pop(id_cook,index):
    with lock:
        items_inoven[id_cook].pop(index)


def Items_instove_pop(id_cook,index):
    with lock:
        items_instove[id_cook].pop(index)

def Items_making_append(id_cook,item):
    with lock:
        items_making[id_cook].append(item)

def Items_making_append_begin(id_cook,item):
    with lock:
        items_making[id_cook].insert(0, item)

def Items_to_make_pop(index):
    with lock:
        items_to_make.pop(index)

def Items_done_append(item):
    with lock:
        items_done.append(item)

def Items_making_pop(id_cook,index):
    with lock:
        items_making[id_cook].pop(index)

