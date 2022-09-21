# Python 3 server example
import SocketServer,Setings,CookSocket,Cooking
from threading import Thread

if __name__ == "__main__":
    server = SocketServer.Server()
    server.start()

    cookS = Cooking.Cooking()
    cookS.start()

    cook = [CookSocket.Cook(i) for i in range(Setings.nr_of_cooks)]
    for i in range(Setings.nr_of_cooks):
        cook[i].start()
    #def cooking():
    #    cook = [CookSocket.Cook(orders, i) for i in range(Setings.nr_of_cooks)]
    #    for i in range(Setings.nr_of_cooks):
    #        cook[i].start()

    #cookingTask = Thread(target=cooking())
    #cookingTask.start()