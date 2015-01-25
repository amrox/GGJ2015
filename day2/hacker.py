#!/usr/bin/env python

import socket
import sys
import time
from threading import Thread, Event, Timer

RECV_MAX = 16384

logo = """ 
        .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'          `98v8P'          `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
        _______  ______ _____  _____  __   _   _______ _     _ _______     
 |      |______ |  ____   |   |     | | \  |   |______  \___/  |______     
 |_____ |______ |_____| __|__ |_____| |  \_| . |______ _/   \_ |______     
                                                                           
"""

help = """
================================================================
Tool             | Cost       | Description
================================================================
bankjob <amount> | 15 sec     | Access bank records.
foe              | 5 sec      | Hack social network.
locker  <amount> | 12 sec     | Encrypt target data and ransom.
================================================================
    """

#TEMPORARY global values
targetFunds = 1000.0
hackerFunds = 0.0

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
                    if str(ex) == "[Errno 35] Resource temporarily unavailable" or str(ex) == "[Errno 10035] A non-blocking socket operation could not be completed immediately":
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

        self.tools = []

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
    def handleCommand(self, cmd):
        if cmd == "help":
            print help
        elif "bankjob" in cmd:
            try:
                t = Bankjob(cmd.split()[1])
                self.tools.append(t)
            except IndexError:
                print "Must enter an amount."
        elif "foe" in cmd:
            t = Tool("foe",5, "Gathering information from social network.", "Hacked social network.", "Failed to hack social network.")
            self.tools.append(t)
        elif "locker" in cmd:
            try:
                t = Tool("locker", 15,"Attempting to ransom %s credits." % cmd.split()[1], "Target paid the ransom.", "Data lock failed.")
                self.tools.append(t)
            except IndexError:
                print "Must enter an amount."
        elif cmd == "stat" or cmd == "":
            print "\n"
            for t in enumerate(self.tools):
                if not t[1].done: 
                    print "%s in progress." % t[1].name
            print "\n" 

        else:
            print "I did not understand that command."
    def promt(self):
        print "WHAT DO WE DO FROM HERE?\n\n"
    def initprompt(self):
        global help
        print logo
        print help
        print "WE ARE IN.\n"
def usage():
    return "hacker.py [host] [port]"


class Tool(object):
    """docstrinTool"""
    def __init__(self,name,duration,started, completion, failure):
        self.done = False
        self.name = name
        self.duration = duration
        self.onsuccess = completion
        self.onfailure = failure
        self.timer = Timer(self.duration, self.finished)
        print  "%s" % started 
        print "It will take %s seconds." % duration
        self.timer.start()
    def finished(self):
        self.done = True
        print self.onsuccess

class  Bankjob(Tool):
    """docstring for  Bankjob"""
    bankBeingHacked = 0
    def __init__(self, amount):
        super(Bankjob, self).__init__("bankjob", 15,"Attempting to withdraw %s credits.\n" % amount , "Accessed bank records.", "Supicious activity detected. Account Locked.")
        Bankjob.bankBeingHacked += 1 
        self.amount = amount
    def finished(self):
        global targetFunds
        self.done = True
        percentage = targetFunds - float(self.amount)
        percentage = percentage / targetFunds
        percentage = (1 - percentage) * 100

        if Bankjob.bankBeingHacked >= 2:
            print self.onfailure

        elif percentage > 30:
            print self.onfailure
        else: 
            global hackerFunds
            print self.onsuccess
            targetFunds -= float(self.amount)
            hackerFunds += float(self.amount)
            print "%s credits added to funds." % self.amount

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

    game = Game(host=host, port=port, duration=60)
    game.start()
    
    
    game.initprompt()

    while not game.over:
        try:
            game.promt()
            
            cmd = raw_input('%ds > ' % (game.remainingTime()))
            #print "%s" % (cmd)
            if game.remainingTime() > 0:
                print "\n"
                game.handleCommand(cmd)
                print "\n"
        except KeyboardInterrupt:
            game.stop()
            sys.exit(0)


if __name__ == '__main__':
    main()
