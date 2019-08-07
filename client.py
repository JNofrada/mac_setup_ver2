import sys
import socket
import time

BUF_SIZE = 29
HOST = '172.20.1.232'
PORT = 5000

def message_back(socket):
    client = input("Which client are you? ")
    socket.send(bytes(client, "utf-8"))
    msg2 = ''
    full2 = ''
    pause = input("Waiting message")
    while True:
        msg2 = s.recv(32)
        full2 += msg.decode("utf-8")
    pause = input("Waiting print")
    print (full2)

def loop():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("connecting")
        s.connect((HOST, PORT))
        msg1 = ''
        full1 = ''
        new_msg = True
        print ("Waiting message")
        while True:
            msg1 = s.recv(32)
            if new_msg:
                msg_len = int(msg1[:BUF_SIZE])
                new_msg = False
            full1 += msg1.decode("utf-8")
            if len(full1)-BUF_SIZE == msg_len:
                print(full1[BUF_SIZE:])
                break
        s.send(bytes("Hello Server", "utf-8"))
        message_back(s)

def main():
    loop()
    pause = input("Press Enter to leave")

if __name__ == '__main__':
    main()
