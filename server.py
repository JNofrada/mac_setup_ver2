import sys
import time
import socket

BUF_SIZE = 29
HOST = "172.20.1.232"
PORT = 5000
CLIENTS = []

class Client:
    def __init__(self, name, addigy):
        self.client_name = name
        self.addigy = addigy

    def print_obj(self):
        print(self.client_name)
        print(self.addigy)

def create_list(CLIENTS):
    client = open("clients.txt")
    while True: 
        client_name = str(client.readline())
        if not client_name: break
        addigy = str(client.readline())
        if not addigy: break
        CLIENTS.append(Client(client_name,addigy))
    client.close()

def message_back(socket):
    client = ''
    print ("waiting message")
    while True:
        msg = s.recv(30)
        client += msg.decode("utf-8")
    print(client)
    s.send(bytes(client, "utf-8"))

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),PORT))
    print ("Bound")
    s.listen(5)
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established")
        msg = "Welcome to the server"
        msg = f"{len(msg):<BUF-SIZE}" + msg
        clientsocket.send(bytes(msg, "utf-8"))
        msg = ''
        full_msg = ''
        while True:
            msg = clientsocket.recv(30)
            try:
                full_msg += msg.decode("utf-8)")
            except:
                print ("full message except")
            if (len(full_msg) >= 12):
                break
        print (full_msg)
        if clientsocket is True:
            message_back(s)

def main():
    #create_list(CLIENTS)
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()


