#!/usr/bin/env python

from subprocess import call
from threading import Thread, Event, Timer
import SocketServer, subprocess, sys 
import os
import random
import socket
import string
import sys
import tempfile
import time

RECV_MAX = 16384
PORT = 2000
BANNER =''' 
    ____  ______   ____  ___________________   ______  __________ 
   / __ \/ ____/  / __ \/ ____/ ____/ ____/ | / / __ \/ ____/ __ \\
  / /_/ / /      / / / / __/ / /_  / __/ /  |/ / / / / __/ / /_/ /
 / ____/ /___   / /_/ / /___/ __/ / /___/ /|  / /_/ / /___/ _, _/ 
/_/    \____/  /_____/_____/_/   /_____/_/ |_/_____/_____/_/ |_|  

     ==  Version 2.2.3 Build 17  Copyright AMTech 2015 ==

'''
VOICE = 'Daniel'

HACKER_MSGS=[
        'YOU_CANT_STOP_ME',
        'I_WILL_PWN_YOU',
        'WHAT_DO_YOU_DO_NOW',
        'GIVE_UP_YOU_LOSE',
        'HAHAHAHAHAHAHAHAHAHA'
        ]

URLS = [
        'http://www.russianbrides.com/',
        'http://thepiratebay.se',
        'http://www.worldjournal.com',
        'https://www.youtube.com/watch?v=sz_m6N1IYuc',
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'http://www.hamsterdance.org/hamsterdance/'
        ]

VIRUS_LOCS = [
        ('Downloads', '~/Downloads'),
        ('Documents', '~/Documents'),
        ('Pictures', '~/Pictures'),
        ('Movies', '~/Movies'),
        ('Music', '~/Music'),
        ('Home', '~'),
        ('Desktop', '~/Desktop')]


VIRUS_FILES = [
        'open_me!!!111.bat',
        'secret.tmp',
        'word97.exe',
        '69831D88-5CEB-45D7-8A4B-A0708C0FEF1A.mov',
        'HOT_LADIES.xls',
        'not-a-nigerian-scam.txt',
        'HALFLIFE3.zip'
        ]

global DEFENDER_GAME

SAY_ENABLED = True
TRACE_TIME = 90
MAX_VIRUSES = 6

random.seed()

################################################################################

def say(msg, voice=None, dur=None):
    if SAY_ENABLED:
        if voice is None:
            voice = VOICE
        if dur is None:
            call(["say", "-v", voice, msg])
        else:
            call(["say", "-v", voice, "-r", str(dur), msg])

def openRandomTempDir():
    d = tempfile.mkdtemp()
    msg = HACKER_MSGS[random.choice(range(len(HACKER_MSGS)))]
    call(["touch", os.path.join(d, "%s.decoy" % (msg))])
    time.sleep(0.3)
    call(["open", "-a", "Finder", d])


def openRandomURL():
    url = URLS[random.choice(range(len(URLS)))]
    call(["open", url])


def clean():

    for l in VIRUS_LOCS:
        for f in VIRUS_FILES:
            p = os.path.join(
                    os.path.expanduser(l[1]), f)
            call(["rm", "-f", p])


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class DefenderGameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
        self.game.intro()
        while not self.game.stopFlag.wait(0.5):
            self.game.run()


class DefenderGame(object):

    def __init__(self, singlePlayer=False):

        self.name = None
        self.hometown = None
        self.securityPin = None

        self.activeViruses = []

        self.intruderFlag = Event()
        self.stopFlag = Event()

        self.over = False

        self.vCount = 1

        self.TCPHandler = None

        self.singlePlayer = singlePlayer


    def sendToHacker(self, msg):
        if self.TCPHandler is not None:
            self.TCPHandler.request.send(msg)


    def intro(self):

        print BANNER 

        defaultPin = random.choice(range(1000,9999))

        raw_input("Press Enter to begin.\n\n")

        print "Welcome to PC Defender!" 
        say("Welcome to PC Defender.")
        say("Please register to continue.")
        print ""
        self.name = raw_input("Name: [Dork] ") or "Dork\n"
        self.hometown = raw_input("Hometown: [Philly] ") or "Philly\n"
        self.securityPin = raw_input("Security PIN: [%d] " % (defaultPin)) or str(defaultPin) 
        print ""

        self.sendToHacker("NAME\t%s" % (DEFENDER_GAME.name))
        self.sendToHacker("HOMETOWN\t%s" % (DEFENDER_GAME.hometown))
        self.sendToHacker("PIN\t%s" % (DEFENDER_GAME.securityPin))

        print "Now running\n  IP:   %s\n  PORT: %d" % (getIP(), PORT)
        say("Thank you for registering. PC Defender is now running.")
        print ""

        time.sleep(0.5)
        print " ****************************************************************"
        print " *      Virus locations will be displayed in this console.      *"
        print " *                                                              *"
        print " * Delete the viruses as they appear but beware of decoy files! *"
        print " ****************************************************************"
        print ""
        say("Virus locations will be displayed in this console.")
        say("Delete the viruses as they appear but beware of decoy files!")


    def run(self):

        self.intruderFlag.wait()

        print ""
        print "*** INTRUDER DETECTED ****"
        print ""
        say("intruder detected")
        say("repeat")
        say("intruder detected")

        time.sleep(0.5)

        print "Starting Countermeasures..."
        say("starting countermeasures")

        time.sleep(0.5)

        print "Beginning Trace..."
        say("beginning trace")

        time.sleep(0.5)

        print "Trace will complete in %d seconds" % (TRACE_TIME)
        print ""
        say("Trace will complete in %d seconds."% (TRACE_TIME))

        time.sleep(0.5)
        print "PREPARE TO DEFEND"
        say("prepare to defend")
        say("now", dur=2)

        time.sleep(0.5)

        startTime = time.time()

        # NOTIFY BEGIN
        self.sendToHacker("BEGIN\t%d" % (TRACE_TIME))

        while not DEFENDER_GAME.over:

            if self.singlePlayer:
                self.vCount = self.vCount + 1
            else:
                if len(self.activeViruses) == 0:
                    self.vCount = 1

            self.virusAttack()

            lastVirusCount = len(self.activeViruses)
            self.checkViruses()

            if len(self.activeViruses) > 0:
                print ""
                print "ACTIVE VIRUSES (%d/%d)" % (len(self.activeViruses), MAX_VIRUSES)
                for v in self.activeViruses:
                    print "   %s" % (v)
            elif len(self.activeViruses) == 0 and lastVirusCount > 0:
                print ""
                print "NO ACTIVE VIRUSES"

            if len(self.activeViruses) >= MAX_VIRUSES:
                print ""
                print "TOO MANY VIRUS. COMPUTER OVER. YOU LOSE."
                say("TOO MANY VIRUS. COMPUTER OVER. YOU LOSE.")

                self.sendToHacker("END\tHACKER")
                self.stop()
                break

            time.sleep(random.choice(range(2,5)))

            now = time.time()
            if startTime + TRACE_TIME < now:
                print ""
                print "TRACE COMPLETE. HACKER IP FOUND. CYBER POLICE NOTIFIED."
                print "SUCCESS!"
                say("TRACE COMPLETE. HACKER IP FOUND. CYBER POLICE NOTIFIED.")
                say("SUCCESS!")

                self.sendToHacker("END\tDEFENDER")
                self.stop()
                break

            else:
                left = TRACE_TIME - (now - startTime) - 1 # (fudge for say)
                if left < 1:
                    say("trace nearly complete!")
                else:
                    say("%d seconds left" % (left))


    def start(self):

        #self.intro()
        self.thread = DefenderGameThread(self)
        self.thread.daemon = True
        self.thread.start()

        if self.singlePlayer:
            time.sleep(2)
            self.intruderFlag.set()

    def stop(self):
        self.stopFlag.set()
        self.over = True


    def virusAttack(self):

        while self.vCount > 0:

            self.installVirus()
            for i in range(random.choice(range(1,4))):
                which = random.choice(range(2))
                if which == 0:
                    openRandomTempDir()
                else:
                    openRandomURL()

            self.vCount = self.vCount - 1


    def installVirus(self):

        while True:

            virusLoc = VIRUS_LOCS[random.choice(range(len(VIRUS_LOCS)))]
            virusDir = os.path.expanduser(virusLoc[1])
            virusFile = VIRUS_FILES[random.choice(range(len(VIRUS_FILES)))]
            virusPath = os.path.join(virusDir, virusFile)

            if virusPath not in self.activeViruses:
                self.activeViruses.append(virusPath)
                break

        call(["touch", virusPath])

        say("virus detected in %s" % (virusLoc[0]))
        call(["open", "-a", "Finder", virusDir])
        if len(self.activeViruses) == 1:
            say("delete it quickly!")


    def checkViruses(self):

        newViruses = []
        a = self.activeViruses
        for v in a:
            if os.path.exists(v):
                newViruses.append(v)
        self.activeViruses = newViruses


class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."

    def handle(self):
        DEFENDER_GAME.intruderFlag.set()

        DEFENDER_GAME.TCPHandler = self

        while not DEFENDER_GAME.over:

            hacker_move = self.request.recv(RECV_MAX)

            if hacker_move == "virus":
                DEFENDER_GAME.vCount = DEFENDER_GAME.vCount + random.choice((1,2))

            elif hacker_move.startswith("cracked"):
                target = hacker_move.split('\t')[1]
                msg = "%s compromised!" % (target)
                print ""
                print "**** %s" % (msg)
                print ""
                say(msg, voice="Zarvox")
                    


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


def defender_main():

    single = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "single":
            single = True

    if single:
        print "# Single Player Mode"
    else:
        print "# Multiplayer Mode"

    clean()

    global DEFENDER_GAME
    DEFENDER_GAME = DefenderGame(singlePlayer=single)
    DEFENDER_GAME.start()

    if single:
        while True:
            time.sleep(0.25)

    else :
        # terminate with Ctrl-C
        server = SimpleServer((getIP(), PORT), SingleTCPHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            DEFENDER_GAME.stop()
            sys.exit(0)


################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
##################################### HACKER LAND ##############################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################



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


class HackerGameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
       

        while not self.game.stopFlag.wait(0.5):


            if self.game.winner is not None and self.game.setup:
                self.game.lost()
                self.game.stop()
            elif self.game.offline and self.game.remainingTime() == 0:
                self.game.winner = "DEFENDER"
                self.game.handleEndGame(self.game.winner)
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


class HackerGame(object):

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
        self.offline = True

        self.data = {}
    
    def start(self):
        if self.host is not None and self.port is not None:
            self._connect()
            self.offline = False
        else:
            self.setup = True

        self.thread = HackerGameThread(self)
        self.thread.daemon = True
        self.thread.start()
        

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
                self.handleEndGame(self.winner)
        except IndexError:
            pass
        except KeyError:
            pass
    def handleEndGame(self, winner):
        if self.winner == "HACKER":
            print "\n\nWE HAVE WON, ALL DATA IS BELONG TO US."
        else:
            print "\n\nWE HAVE BEEN TRACED."
        print "\nGAME OVER."

    def send(self,msg):
        if self.socket is not None:
            self.socket.send(msg)
    def handleCommand(self, cmd):
        if cmd == "help" or cmd == "?":
            print help
        elif "inf" in string.lower(cmd) or "infect" == cmd:
            v = Virus(self,"inf",1,"HACKING TARGET...", "\nCOMPRIMISED TARGET.", "\nFAILED TO DESTABALIZE TARTGET.")
            v.handleResult()
        else:
            print "I DID NOT UNDERSTAND THAT COMMAND.\n"
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
        result = None

        while result is None:
            print "ENCRYPTED FILE FOUND... %s\n" % filename
            input = raw_input('%ds > ' % (self.remainingTime()))
            if string.upper(input) == string.upper("dc %s" % (filename)) or string.upper(input) == string.upper("dc %s.enc" % (filename)):
                result = "SUCCESS."
            elif string.lower(input) == "help":
                print "\ndc <file.enc>\n"
            else:
                result = "FAILURE."
        return result

    def askkey(self):
        key = self.genkey()
        result = None

        while result is None:
            print "KEY GENERATED... %s\n" % key
            input = raw_input('%ds > ' % (self.remainingTime()))
            if string.upper(input) == string.upper("usekey %s" % key):
                result = "SUCCESS."
            elif string.lower(input) == "help":
                print "\nusekey <key>\n"
            else:
                result = "FAILURE."
        return result

    def asklink(self):
        a, b = self.brokenlink(2)
        result = None

        while result is None:
            print "LINK FROM NODE %s to NODE %s BROKEN.\n" % (a, b)
            input = raw_input('%ds > ' % (self.remainingTime()))
            if string.upper(input) == string.upper("link %s %s" % (a, b)):
                result = "SUCCESS."
            elif string.lower(input) == "help":
                print "\nlink <to> <from>\n"
            else:
                result = "FAILURE."
        return result


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
        print "\n" + self.result

        if self.result == "SUCCESS.":
            print self.onsuccess
            self.game.send("virus")
            self.game.successes +=1
            self.game.playsound(random.randint(500, 1000))
        else:
            print self.onfailure
            self.game.failures +=1
            self.game.playsound(random.randint(1000,1500))

        if len(self.game.data) > 0:
            if self.game.successes == 3:
                print "RETRIEVED TARGET'S NAME: %s" % self.game.data["NAME"]
                self.game.send("cracked\tname")
            if self.game.successes == 5:
                print "RETRIEVED TARGET'S HOMETOWN: %s" % self.game.data["HOMETOWN"]
                self.game.send("cracked\thome address")
            if self.game.successes == 8:
                print "RETRIEVED TARGET'S PIN: %s" % self.game.data["PIN"]
                self.game.send("cracked\tsecurity pin")

        if self.game.offline:
            if self.game.successes == 8:
                self.game.winner = "HACKER"
                self.game.handleEndGame(self.game.winner)
            elif self.game.failures == 8:
                self.game.winner = "DEFENDER"
                self.game.handleEndGame(self.game.winner)

def hacker_main():

    if len(sys.argv) not in (1,3):
        print usage()
        exit(1)

    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = None
        port = None

    game = HackerGame(host=host, port=port, duration=120)

    global help
    print logo
    print help
    print "\n\nCONNECTING...\n\n"

    game.start()

    while game.setup == False:
        pass
            

    print "WE ARE IN.\n"

    game.startTime = time.time()

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

    if len(sys.argv) < 2:
        print "legion-defender.py [hack|defend]"
        exit(1)

    mode = sys.argv[1]
    del sys.argv[1]

    if mode == "hack":
        hacker_main()
    elif mode == "defend":
        defender_main()
    else:
        print "UKNOWN MODE %s" % (mode)

