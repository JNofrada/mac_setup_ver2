import sys
import socket
import time

HOST = '172.20.1.232'
PORT = 5000

def message_back(socket):
    
    s.send(bytes(input("Which client are you? ", "utf-8")))
    msg2 = ''
    full2 = ''
    pause = input("Waiting message")
    while True:
        msg2 = s.recv(1024)
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
        print ("Waiting message")
        while True:
            msg1 = s.recv(16)
            try:
                full1 += msg.decode("utf-8")
            print (full1)
        pause = ''
        pause = input("Waiting print")
        print (full1)
        message_back(s)

def main():
    loop()
    pause = ''
    pause = raw_input("Press Enter to leave")

if __name__ == '__main__':
    main()
