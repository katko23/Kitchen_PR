# Python 3 server example
import SocketServer,Orders_Table,Cooks_Hiring

order_Table = Orders_Table.Order_Table()
cook = Cooks_Hiring.cooks

if __name__ == "__main__":
    server = SocketServer.Server()
    server.start()

    order_Table.start()

    #def cooking():
    #    cook = [CookSocket.Cook(orders, i) for i in range(Setings.nr_of_cooks)]
    #    for i in range(Setings.nr_of_cooks):
    #        cook[i].start()

    #cookingTask = Thread(target=cooking())
    #cookingTask.start()