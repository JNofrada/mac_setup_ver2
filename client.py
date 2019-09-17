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

def mainmenu():
    print ("1) Run setup\n2) Add Client\n3) Update Addigy Command\n4) Remove Client")


def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    message = sendrec.msgrecv(s, BUF_SIZE)
    print(message[BUF_SIZE:])
    mainmenu()
    message_back(s)
    addigy(s)
    s.close()

def main():
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()
