import sys
import socket
import sendrec

BUF_SIZE = 29
HOST = "172.20.1.232"
PORT = 5000
CLIENTS = []
COMP =[]

class Client:
    def __init__(self, name, addigy):
        self.client_name = name
        self.addigy = addigy

    def print_obj(self):
        print(self.client_name)
        print(self.addigy)

class Comp:
    def __init__(self, serial, client, asset):
        self.serial = serial
        self.client = client
        self.asset = asset

    def print_obj(self):
        print(self.serial)
        print(self.client)
        print(self.asset)

def create_list(CLIENTS):
    client = open("client.txt")
    while True: 
        client_name = str(client.readline()).strip()
        if not client_name: break
        addigy = str(client.readline()).strip()
        if not addigy: break
        CLIENTS.append(Client(client_name,addigy))
    client.close()

def message_back(socket):
    message = sendrec.msgrecv(socket, BUF_SIZE)
    split = message.split('\n')
    serial = (split[0].split())[1].strip()
    client = (split[1].split())[1].strip()
    asset = (split[2].split())[1].strip()
    COMP.append(Comp(serial, client, asset))

    COMP[0].print_obj()
    for x in CLIENTS:
        if x.client_name == client:
            socket.send(bytes(sendrec.get_buff(x.addigy), "utf-8"))

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),PORT))
    print ("Bound")
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established")
        msg = "Welcome to the server"
        msg = sendrec.get_buff(msg, BUF_SIZE)
        clientsocket.send(bytes(msg, "utf-8"))
        message_back(clientsocket)

def main():
    create_list(CLIENTS)
    print ("Client List Created")
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()


