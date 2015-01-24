#!/usr/bin/env python

import socket
import sys
from threading import Thread, Event

RECV_MAX = 16384


class ReceiveThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        while not self.client.stopFlag.wait(0.5):
            try:
                data = self.client.socket.recv(RECV_MAX)
                lines = data.split('\n')
                for l in lines:
                    self.client._handle(l)

                #if data.strip() == "LOST":
                #    self.game.lost()
                #    break

            except socket.error as ex:
                if str(ex) == "[Errno 35] Resource temporarily unavailable":
                    continue
                raise


class Client(object):

    def __init__(self, host, port, game):
        self.host = host
        self.port = port
        self.game = game

        self.receiveThread = None
        self.stopFlag = Event()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)  # optional non-blocking
    
        self.receiveThread = ReceiveThread(self)
        self.receiveThread.start()

    def _handle(self, msg):
        if msg == "LOST":
            self.game.lost()
            self.stop()


    def stop(self):
        self.stopFlag.set()


class Game(object):

    def __init__(self):
        self.over = False

    def lost(self):
        print "GAME OVER\n\nPress enter to continue."
        self.over = True


def usage():
    return "hacker.py [host] [port]"


def main():

    if len(sys.argv) < 2:
        print usage()
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    game = Game()

    client = Client(host, port, game)
    client.connect()

    while not game.over:
        try:
            cmd = raw_input('> ')
            print "%s" % (cmd)
        except KeyboardInterrupt:
            client.stop()
            sys.exit(0)


if __name__ == '__main__':
    main()
