#!/usr/bin/python3
import socket
import sys
import os

def main():
    #sender <host> <port> <payload size> <file name>
    host = sys.argv[1]
    port = sys.argv[2]
    payload_size = int(sys.argv[3])
    file_name = sys.argv[4]
    recv_addr = (host,int(port))


    try:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    except:
        print('Failed to get socket.')
    file_size = os.path.getsize(file_name) #bytes
    bytes_sent = 0
    messages_sent = 0
    with open(file_name, 'rb') as f:
        datagram_num = int(file_size/payload_size)+1
        claim = "WILL SEND "+str(datagram_num)+" MESSAGES"
        udp.sendto(claim.encode(),recv_addr)
        for i in range(datagram_num):
            buff = f.read(payload_size)
            bytes_sent = bytes_sent+len(buff)
            messages_sent = messages_sent+1
            udp.sendto(buff, recv_addr)
    result = "Sent "+str(messages_sent)+" messages, "+str(bytes_sent)+"bytes."
    print(result)
    udp.close()

if __name__ == "__main__":
    # execute only if run as a script
    main()
