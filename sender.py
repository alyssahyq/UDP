#!/usr/bin/python
import socket
import sys
import os

def main():
    command = sys.stdin.readline()
    infos = (command.rstrip()) .split(" ")
    #sender <host> <port> <payload size> <file name>
    host = infos[1]
    port = infos[2]
    payload_size = int(infos[3])
    file_name = infos[4]
    recv_addr = (host,int(port))

    try:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    except:
        print('Failed to get socket.')
    file_size = os.path.getsize(file_name) #bytes
    bytes_sent = 0
    messages_sent = 0
    with open(file_name, 'r') as f:
        datagram_num = int(file_size/payload_size)+1
        claim = "WILL SEND "+str(datagram_num)+" MESSAGES"
        udp.sendto(bytes(claim, encoding='utf-8'),recv_addr)
        for i in range(datagram_num):
            buff = f.read(payload_size)
            bytes_sent = bytes_sent+len(buff)
            messages_sent = messages_sent+1
            udp.sendto(bytes(buff, encoding='utf-8'), recv_addr)
    print("Sent ",messages_sent," messages, ",bytes_sent, "bytes.")
    udp.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()
