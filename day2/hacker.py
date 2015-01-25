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
infect            | Place virus on target's machine.
usekey <key>      | Use a generated key.
dc <file.enc>     | Decrypt a file.
link <from> <to>  | Route from one node to another.
help              | Display help.
================================================================
    """

#bankjob <amount>  | Access target's bank records.
#locker  <amount>  | Encrypt target data for ransom.

random.seed()

class GameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
        while self.game.setup == False:
            pass

        while not self.game.stopFlag.wait(0.5):

            if self.game.remainingTime() == 0:
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

        self.data = {}
        self.data["funds"] = 0.0
        self.data["targetFunds"] = 1000.0 # randomize?
    def start(self):
        if self.host is not None and self.port is not None:
            self._connect()
        else:
            self.setup = True

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
        try:
            fields = msg.split('\t')
            prop = fields[0]
            val = fields[1]
            self.data[prop] = val

            if self.data["begin"] is not None:
                self.duration = self["begin"]
                self.setup = True
        except IndexError:
            pass
    def send(self,msg):
        if self.socket is not None:
            self.socket.send(msg)
    def handleCommand(self, cmd):
        if cmd == "help" or cmd == "?":
            print help
        elif "infect" in string.lower(cmd):
            t = Tool(self,"dirt",1,"Gathering information from social network.", "Hacked social network.", "Failed to hack social network.")
            t.handleResult()
        elif cmd == "hack":
            self.send("virus")
        elif "bankjob" in cmd:
            try:
                t = Bankjob(self,cmd.split()[1])
                t.handleResult()
            except IndexError:
                print "Must enter an amount."
        elif "locker" in cmd:
            try:
                t = Tool(self,"locker", 1,"Attempting to ransom %s credits." % cmd.split()[1], "Target paid the ransom.", "Data lock failed.")
                t.handleResult()
            except IndexError:
                print "Must enter an amount."
        else:
            print "I did not understand that command."
    def promt(self):
        print "WHAT DO WE DO FROM HERE?\n\n"
    
    def decrypt(self):
        filename = ""
        for i in range(0,5):
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
        if string.upper(input) == string.upper("dc %s" % (filename)):
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
        
def usage():
    return "hacker.py [host] [port]"

class Tool(object):
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
        
class  Bankjob(Tool):
    """docstring for  Bankjob"""
    def __init__(self,game, amount):
        super(Bankjob, self).__init__(game,"bankjob", 1,"Attempting to withdraw %s credits.\n" % amount , "Accessed bank records.", "Supicious activity detected. Account Locked.")
        self.amount = amount

    def handleResult(self):
        if result == "SUCCESS.":
            percentage = self.game.data["targetFunds"] - float(self.amount)
            percentage = percentage / self.game.data["targetFunds"]
            percentage = (1 - percentage) * 100

            if percentage > 30:
                print self.onfailure
            else: 
                print self.onsuccess
                self.game.data["targetFunds"] -= float(self.amount)
                self.game.data["funds"] += float(self.amount)
                self.game.send("virus")
                print "%s credits added to funds." % self.amount
        else:
            print "FAILURE."

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

    global help
    print logo
    print help
    print "\n\nCONNECTING...\n\n"

    game.start()

    while not game.over:
        try:
            
            while not game.setup:
                pass
             
            print "WE ARE IN.\n"
            game.promt()
            
            cmd = raw_input('%ds > ' % (game.remainingTime()))
            if game.remainingTime() > 0:
                print "\n"
                game.handleCommand(cmd)
                print "\n"
        except KeyboardInterrupt:
            game.stop()
            sys.exit(0)

if __name__ == '__main__':
    main()
