import Setings
import requests
import Plates

def register():
    id = Setings.restaurant_id
    host = Setings.FoodOrderingService_Host
    port = Setings.FoodOrderingService_Port

    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
        dictToSend = {"restaurant_id": id, "name": "McDonald's",
                      "address": str(Setings.serverName) + ":" + str(Setings.this_serverPort),
                      "menu_items": len(Plates.plates), "menu": Plates.plates }
        res = requests.post("http://" + str(host) + ":" + str(port) + "/register", json=dictToSend)
        return True
    sock.close()
    return False

