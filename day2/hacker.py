#!/usr/bin/env python

import socket
import sys
import time
import random
import string
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
Commands          | Description
================================================================
inf               | Place virus on target's machine.
usekey <key>      | Use a generated key.
dc <file.enc>     | Decrypt a file.
link <from> <to>  | Route from one node to another.
help              | Display help.
================================================================
    """

random.seed()

class GameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
       

        while not self.game.stopFlag.wait(0.5):


            if self.game.winner is not None and self.game.setup:
                    self.game.lost()
                    self.game.stop()

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

        self.setup = False 
        self.winner = None

        self.successes = 0
        self.failures = 0

        self.data = {}
    def start(self):
        if self.host is not None and self.port is not None:
            self._connect()
        else:
            self.setup = True

        self.thread = GameThread(self)
        self.thread.daemon = True
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
        self.over = True

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)  # optional non-blocking
    
    def _handle(self, msg):
        try:
            fields = msg.split('\t')
            prop = fields[0]
            val = fields[1]
            self.data[prop] = val

            if self.data["BEGIN"] is not None:
                self.duration = int(self.data["BEGIN"])
                self.setup = True
            if self.data["END"] is not None:
                self.winner = self.data["END"]
                if self.winner == "HACKER":
                    print "WE HAVE WON, ALL DATA IS BELONG TO US."
                else:
                    print "WE HAVE BEEN TRACED."
        except IndexError:
            pass
        except KeyError:
            pass
    def send(self,msg):
        if self.socket is not None:
            self.socket.send(msg)
    def handleCommand(self, cmd):
        if cmd == "help" or cmd == "?":
            print help
        elif "inf" in string.lower(cmd) or "infect" == cmd:
            v = Virus(self,"inf",1,"Gathering information from social network.", "Hacked social network.", "Failed to hack social network.")
            v.handleResult()
        else:
            print "I did not understand that command."
    def promt(self):
        print "WHAT DO WE DO FROM HERE?\n\n"
    
    def decrypt(self):
        filename = ""
        for i in range(0,4):
            filename += random.choice(list(string.ascii_lowercase))
        return string.upper("%s.enc" % (filename))

    def  genkey(self):
        key = ""
        for i in range(0,4):
            if i % 2 == 0:
                key += str(random.randint(0,9))
            else:
                key += random.choice(list(string.ascii_uppercase))
        return "%s" % key

    def brokenlink(self, lenth):
        a = ""
        b = ""
        for i in range(0,lenth):
            a += str(random.randint(0,9))
            b += str(random.randint(0,9))
        return (a, b) 

    def askdec(self):
        filename = self.decrypt()
        print "ENCRYPTED FILE FOUND... %s" % filename
        input = raw_input('%ds > ' % (self.remainingTime()))
        if string.upper(input) == string.upper("dc %s" % (filename)) or string.upper(input) == string.upper("dc %s.enc" % (filename)):
            return "SUCCESS."
        else:
            return "FAILURE."

    def askkey(self):
        key = self.genkey()
        print "KEY GENERATED... %s" % key
        input = raw_input('%ds > ' % (self.remainingTime()))
        if string.upper(input) == string.upper("usekey %s" % key):
            return "SUCCESS."
        else:
            return "FAILURE."

    def asklink(self):
        a, b = self.brokenlink(2)
        print "LINK FROM NODE %s to NODE %s BROKEN." % (a, b)
        input = raw_input('%ds > ' % (self.remainingTime()))
        if string.upper(input) == string.upper("link %s %s" % (a, b)):
            return "SUCCESS."
        else:
            return "FAILURE."


    def genCmd(self,times):
        for i in range(0, times):
            choices = ["key", "decrypt","link"]
            result = "FAILURE."
            c = random.choice(choices)
            if c == "key":
                result = self.askkey()
            elif c == "decrypt":
                result = self.askdec()
            elif c == "link":
                result = self.asklink()

            if result == "FAILURE.":
                return "FAILURE."
        return "SUCCESS."
    def playsound(self, freq):
        try:
            import winsound
            winsound.Beep(freq,300)
        except ImportError:
            pass
def usage():
    return "hacker.py [host] [port]"

class Virus(object):
    """docstrinTool"""
    def __init__(self,game,name,diff,started, completion, failure):
        self.game = game
        self.done = False
        self.name = name
        self.onsuccess = completion
        self.onfailure = failure
        print  "%s" % started 
        self.result = self.game.genCmd(diff)
    def handleResult(self):
        print self.result

        if self.result == "SUCCESS.":
            self.game.send("virus")
            self.game.successes +=1
            self.game.playsound(random.randint(500, 1000))
        else:
            self.game.failures -=1
            self.game.playsound(random.randint(5000,10000))

        if len(self.game.data) > 0:
            if successes == 3:
                print "RETRIEVED TARGET'S NAME: %s" % self.game.data["NAME"]
            if successes == 5:
                print "RETRIEVED TARGET'S HOMETOWN: %s" % self.game.data["HOMETOWN"]
            if successes == 8:
                print "RETRIEVED TARGET'S PIN: %s" % self.game.data["PIN"]

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

    game = Game(host=host, port=port, duration=120)

    global help
    print logo
    print help
    print "\n\nCONNECTING...\n\n"

    game.start()

    while game.setup == False:
        pass
             
    print "WE ARE IN.\n"

    while not game.over:
        try:
            game.promt()
            
            cmd = raw_input('%ds > ' % (game.remainingTime()))
            if game.winner is None:
                print "\n"
                game.handleCommand(cmd)
                print "\n"
        except KeyboardInterrupt:
            game.stop()
            sys.exit(0)

if __name__ == '__main__':
    main()
