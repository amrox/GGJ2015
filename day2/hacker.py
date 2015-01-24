#!/usr/bin/env python

import socket
import sys

#def client(string):
#    HOST, PORT = 'localhost', 2000
#    # SOCK_STREAM == a TCP socket
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    #sock.setblocking(0)  # optional non-blocking
#    sock.connect((HOST, PORT))
#    sock.send(string)
#    reply = sock.recv(16384)  # limit reply to 16K
#    sock.close()
#    return reply
#
#assert client('2+2') == '4'
#

def connect(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(0)  # optional non-blocking
    sock.connect((host, port))

    while True:
    
        reply = sock.recv(16384)  # limit reply to 16K
    
    
    #sock.send(string)


def usage():
    return "hacker.py [host] [port]"

def main():

    if len(sys.argv) < 2:
        print usage()
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    connect(host, port)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
