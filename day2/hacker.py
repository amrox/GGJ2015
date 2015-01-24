#!/usr/bin/env python

import socket
import sys
from threading import Thread, Event


class ReceiveThread(Thread):
    def __init__(self, event, sock):
        Thread.__init__(self)
        self.stopped = event
        self.sock = sock

    def run(self):
        while not self.stopped.wait(0.5):
            try:
                data = self.sock.recv(16384)  # limit reply to 16K
                #print reply
                if data.strip() == "LOST":
                    print "YOU LOSE"
                    break

            except socket.error as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    continue
                raise


class Client(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.receiveThread = None
        self.stopFlag = Event()

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.setblocking(0)  # optional non-blocking
    
        self.receiveThread = ReceiveThread(self.stopFlag, sock)
        self.receiveThread.start()

    def stop(self):
        self.stopFlag.set()
    

def usage():
    return "hacker.py [host] [port]"


def main():

    if len(sys.argv) < 2:
        print usage()
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    c = Client(host, port)
    c.connect()

    while c.receiveThread.isAlive():
        try:
            cmd = raw_input('> ')
            print "%s" % (cmd)
        except KeyboardInterrupt:
            c.stop()
            sys.exit(0)


if __name__ == '__main__':
    main()
