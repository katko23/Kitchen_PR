import threading

lock = threading.Lock()
done_lock = threading.RLock()

items_to_make = []
items_done = []
items_making = []

def Items_making_append(id_cook,item):
    with lock:
        items_making[id_cook].append(item)


def Items_to_make_pop(index):
    with lock:
        items_to_make.pop(index)

def Items_done_append(item):
    with lock:
        items_done.append(item)

def Items_making_pop(id_cook,index):
    with lock:
        items_making[id_cook].pop(index)

