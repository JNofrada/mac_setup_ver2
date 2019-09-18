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

    def __eq__(self, other):
        if self.serial == other.serial:
            return True
        else:
            return False

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
    try:
        message = sendrec.msgrecv(socket, BUF_SIZE)
    except:
        print ("Client disconnected. Please restart client")
        return
    split = message.split('\n')
    serial = (split[0].split())[1].strip()
    client = (split[1].split())[1].strip()
    asset = (split[2].split())[1].strip()
    new_mac = Comp(serial, client, asset)
    if not COMP:
        COMP.append(new_mac)
    for x in COMP:
        if COMP[x] == new_mac:
            confirm = f"A previous Mac was found with the serial {serial}, but with the asset {COMP[x].asset} from the client {COMP[x].client}\nSetup with previous config (y/n)? "
            confirm = sendrec.get_buff(confirm, BUF_SIZE)
            socket.send(bytes(confirm, "utf-8"))
            response = sendrec.msgrecv(socket, BUF_SIZE)
            repeat = True
            while repeat:
                if response == 'y':
                    for y in CLIENTS:
                        if x.client_name == COMP[y].client:
                            socket.send(bytes(sendrec.get_buff(x.addigy, BUF_SIZE), "utf-8"))
                            del new_mac
                            repeat = False
                if response == 'n':
                    for y in CLIENTS:
                        if x.client_name == client:
                            socket.send(bytes(sendrec.get_buff(x.addigy, BUF_SIZE), "utf-8"))
                            COMP[x].client = client
                            COMP[x].asset = asset
                            repeat = False
                else:
                    socket.send(bytes(confirm, "utf-8"))
        else:
            for y in CLIENTS:
                if x.client_name == client:
                    socket.send(bytes(sendrec.get_buff(x.addigy, BUF_SIZE), "utf-8"))
                    COMP[x].client = client
                    COMP[x].asset = asset

def add_client(socket):
    try:
        message = sendrec.msgrecv(socket, BUF_SIZE)
    except:
        print ("Client disconnected. Please restart client")
        return
    split = message.split('\n')
    client_name = split[0].strip()
    addigy = split[1].strip()
    new_client = Client(client_name, addigy)
    CLIENTS.append(new_client)
    msg = f"Added {client_name}"
    msg = sendrec.get_buff(msg, BUF_SIZE)
    socket.send(bytes(msg, "utf-8"))

def update_addigy(socket):
    try:
        message = sendrec.msgrecv(socket, BUF_SIZE)
    except:
        print ("Client disconnected. Please restart client")
        return
    split = message.split('\n')
    client_name = split[0].strip()
    addigy = split[1].strip()
    for x in CLIENTS:
        if x.client_name == client_name:
            x.addigy = addigy
    msg = f"Updated Addigy command for {client_name}"
    msg = sendrec.get_buff(msg, BUF_SIZE)
    socket.send(bytes(msg, "utf-8"))

def remove_client(socket):
    try:
        client_name = sendrec.msgrecv(socket, BUF_SIZE)
    except:
        print ("Client disconnected. Please restart client")
        return
    for x in CLIENTS:
        if x.client_name == client_name:
            CLIENTS.remove(x)
    msg = f"Removed {client_name}"
    msg = sendrec.get_buff(msg, BUF_SIZE)
    socket.send(bytes(msg, "utf-8"))

def mainmenu(socket):
    while True:
        try:
            select =  sendrec.msgrecv(socket, BUF_SIZE)
        except:
            print ("Client disconnected. Please restart client")
        if select == '1':
            message_back(socket)
            break
        elif select == '2':
            add_client(socket)
            break
        elif select == '3':
            update_addigy(socket)
            break
        elif select == '4':
            remove_client(socket)
            break
        elif select == 'Exit' or select == 'exit':
            break
        else:
            print ("Invalid selection")
    socket.close()

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
        mainmenu(clientsocket)

def main():
    create_list(CLIENTS)
    print ("Client List Created")
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()