#!/usr/local/bin/python
import socket
import sys
import re
import signal

timeout = 0
n_messages = 0
n_bytes = 0
sum = -1  # Get the sum of messages from sender

def set_timeout(callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                global timeout
                signal.signal(signal.SIGALRM, handle)
                signal.setitimer(signal.ITIMER_REAL, timeout)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                callback()
        return to_do
    return wrap


def after_timeout():
    global n_messages
    global n_bytes
    print("Error: time out.")
    print("Received ",n_messages," messages, ",n_bytes," bytes.")



@set_timeout(after_timeout)
def recv_loop(udp_socket,f):
    global sum
    global n_messages
    global n_bytes
    while True:
        recv(udp_socket,f)
        if sum == n_messages:
            break
    udp_socket.close()
    print("Received ", n_messages, " messages, ", n_bytes, " bytes.")
    return 0

def recv(udp_socket,f):
    global sum
    recv_data = udp_socket.recvfrom(1024)
    message = bytes.decode(recv_data[0])
    if re.match("WILL SEND [0-9]+ MESSAGES",message):
        sum = int(re.search("[0-9]+",message).group())
    else:
        f.write(message)
        global n_messages
        n_messages = n_messages+1
        global n_bytes
        n_bytes = n_bytes + len(message)

def main():
    command = sys.stdin.readline()
    infos = (command.rstrip()).split(" ")
    # receiver <file name> <timeout>
    file_name = infos[1]
    global timeout
    timeout = float(infos[2])/1000.0

    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print('Failed to get socket.', file=sys.stderr)
    port = 8000
    localaddr = ("", port)
    print("Port: ",port)
    with open('port', 'a') as p:
        p.write(str(port))
    try:
        udp_socket.bind(localaddr)
    except:
        print('Failed to bind.', file=sys.stderr)
    with open(file_name, 'a') as f:
        recv(udp_socket,f)
        recv_loop(udp_socket,f)
    return 0

if __name__ == "__main__":
    main()
