import sys
import socket
import sendrec
import subprocess

BUF_SIZE = 29
HOST = '172.20.1.205'
PORT = 5000

def message_back(socket):
    #serial = get_serial()
    serial = "test serial"
    client = input("Which client are you? ")
    asset = set_asset()
    msg = sendrec.get_buff(f"Serial: {serial}\nClient: {client}\nAsset: {asset}", BUF_SIZE)
    socket.send(bytes(msg, "utf-8"))

def get_serial():
    task = subprocess.Popen(['system_profiler', 'SPHardwareDataType'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = task.communicate()
    for l in out.split('\n'):
        if 'Serial Number (system):' in l:
            serial_line = l.strip()
            break
        serial = serial_line.split(' ')[-1]
    return (serial)

def set_asset():
    asset = input("What is the asset tag: ")
    subprocess.call(["sudo", "scutil", "--set", "LocalHostName", asset])
    subprocess.call(["sudo", "scutil", "--set", "HostName", asset])
    subprocess.call(["sudo", "scutil", "--set", "ComputerName", asset])
    return (asset)

def addigy(socket):
    message = sendrec.msgrecv(socket, BUF_SIZE)
    addigy_download = message.split("&&")
    print ("Installing Addigy")
    subprocess.call(addigy_download[0].split())
    subprocess.call(addigy_download[1].split())
    subprocess.call(addigy_download[2].split())

def change_stuff(socket):
    client = input("Client name: ")
    addigy = input("Addigy command: ")
    msg = sendrec.get_buff(f"{client}\n{addigy}")
    socket.send(bytes(msg, "utf-8"))
    print (sendrec.msgrecv(socket, BUF_SIZE))

def mainmenu(socket):
    while True:
        select =  input("1) Run setup\n2) Add Client\n3) Update Addigy Command\n4) Remove Client\nExit to leave")
        socket.send(bytes(sendrec.get_buff(select)), BUF_SIZE)
        if select == '1':
            message_back(socket)
            addigy(socket)
            break
        elif select == '2':
            change_stuff(socket)
            break
        elif select == '3':
            change_stuff(socket)
            break
        elif select == '4':
            change_stuff(socket)
            break
        elif select == 'Exit' or select == 'exit':
            break
        else:
            print ("Invalid selection")
    socket.close()

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    message = sendrec.msgrecv(s, BUF_SIZE)
    print(message[BUF_SIZE:])
    mainmenu(s)

def main():
    loop()

if __name__ == '__main__':
    main()
