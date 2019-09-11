import socket

def msgrecv(socket, BUF_SIZE): #socket receiving message, Expectant Buffer size
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

def get_buff(message, BUF_SIZE): #message to get buffed, buffer size added
    message = f"{len(message):<{BUF_SIZE}}" + message
    return (message)
