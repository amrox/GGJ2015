#!/usr/bin/env python

import socket
import sys
import time
from threading import Thread, Event

RECV_MAX = 16384


class GameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
        while not self.game.stopFlag.wait(0.5):

            if self.game.remainingTime() == 0:
                self.game._handle("LOST")

            elif self.game.socket is not None:
                try:
                    data = self.game.socket.recv(RECV_MAX)
                    lines = data.split('\n')
                    for l in lines:
                        self.game._handle(l)

                except socket.error as ex:
                    if str(ex) == "[Errno 35] Resource temporarily unavailable":
                        continue
                    raise


class Game(object):

    def __init__(self, host=None, port=None, duration=120):
        self.host = host
        self.port = port
        self.duration = duration

        self.over = False
        self.stopFlag = Event()
        self.socket = None
        self.startTime = None

    def start(self):
        if self.host is not None and self.port is not None:
            self._connect()

        self.thread = GameThread(self)
        self.thread.start()
        self.startTime = time.time()

    def stop(self):
        self.stopFlag.set()

    def remainingTime(self):
        r = self.startTime + self.duration - time.time()
        if r < 0:
            r = 0
        return int(r)


    def lost(self):
        print "GAME OVER\n\nPress enter to continue."
        self.over = True

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)  # optional non-blocking
    
    def _handle(self, msg):
        if msg == "LOST":
            self.lost()
            self.stop()



def usage():
    return "hacker.py [host] [port]"


def main():

    if len(sys.argv) not in (1,3):
        print usage()
        exit(1)

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = None
        port = None

    game = Game(host=host, port=port, duration=10)
    game.start()

    while not game.over:
        try:
            cmd = raw_input('%ds > ' % (game.remainingTime()))
            print "%s" % (cmd)
        except KeyboardInterrupt:
            game.stop()
            sys.exit(0)


if __name__ == '__main__':
    main()
