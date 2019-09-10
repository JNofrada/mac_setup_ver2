import sys
import time
import socket

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
        client_name = str(client.readline())
        if not client_name: break
        addigy = str(client.readline())
        if not addigy: break
        CLIENTS.append(Client(client_name,addigy))
    client.close()

def msgrecv(socket):
    msg1 = ''
    full1 = ''
    new_msg = True
    while True:
        msg1 = socket.recv(32)
        if new_msg:
            msg_len = int(msg1[:BUF_SIZE])
            new_msg = False
        full1 += msg1.decode("utf-8")
        if len(full1)-BUF_SIZE == msg_len:
            new_msg = True
            break
    return (full1[BUF_SIZE:])

def message_back(socket):
    message = msgrecv(socket)
    split = message.split('\n')
    serial = (split[0].split())[1]
    client = (split[1].split())[1]
    asset = (split[2].split())[1]
    COMP.append(Comp(serial, client, asset))
    COMP[0].print_obj()
    socket.send(bytes(get_buff(message), "utf-8"))

def get_buff(message):
    message = f"{len(message):<{BUF_SIZE}}" + message
    return (message)

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),PORT))
    print ("Bound")
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established")
        msg = "Welcome to the server"
        msg = get_buff(msg)
        clientsocket.send(bytes(msg, "utf-8"))
        message_back(clientsocket)

def main():
    create_list(CLIENTS)
    print ("Client List Created")
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()


