import sys
import socket
import time

BUF_SIZE = 29
HOST = '172.20.1.205'
PORT = 5000

def message_back(socket):
    #serial = get_serial()
    serial = "test serial"
    print (serial)
    client = input("Which client are you? ")
    asset = set_asset()
    msg = get_buff(f"Serial: {serial}\nClient: {client}\nAsset: {asset}")
    socket.send(bytes(msg, "utf-8"))
    message = msgrecv(socket)
    print (message)

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
    #subprocess.call(["sudo", "scutil", "--set", "LocalHostName", asset])
    #subprocess.call(["sudo", "scutil", "--set", "HostName", asset])
    #subprocess.call(["sudo", "scutil", "--set", "ComputerName", asset])
    return (asset)

def get_buff(message):
    message = f"{len(message):<{BUF_SIZE}}" + message
    return (message)

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

def loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), PORT))
    message = msgrecv(s)
    print(message[BUF_SIZE:])
    print("going to message")
    message_back(s)
    s.close()

def main():
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()
