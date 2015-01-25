#!/usr/bin/env python

import SocketServer, subprocess, sys 
from threading import Thread, Event
from subprocess import call
import time
import os
import tempfile
import random
import socket

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
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
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

SAY_ENABLED = True
SINGLE_PLAYER = False
TRACE_TIME = 90

global GAME


def say(msg, dur=None):
    if SAY_ENABLED:
        if dur is None:
            call(["say", "-v", VOICE, msg])
        else:
            call(["say", "-v", VOICE, "-r", str(dur), msg])

def openRandomTempDir():
    d = tempfile.mkdtemp()
    msg = HACKER_MSGS[random.choice(range(len(HACKER_MSGS)))]
    call(["touch", os.path.join(d, msg)])
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


class GameThread(Thread):

    def __init__(self, game):
        Thread.__init__(self)
        self.game = game 

    def run(self):
        while not self.game.stopFlag.wait(0.5):
            self.game.run()


class Game(object):

    def __init__(self):

        self.name = None
        self.hometown = None
        self.securityPin = None

        self.activeViruses = []

        self.intruderFlag = Event()
        self.stopFlag = Event()

        self.over = False

        self.vCount = 1

        self.TCPHandler = None


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
    
        max_viruses = 5
        duration = TRACE_TIME
    
        startTime = time.time()

        # NOTIFY BEGIN
        self.sendToHacker("BEGIN\t%d" % (duration))
    
        while not GAME.over:

            if SINGLE_PLAYER:
                self.vCount = self.vCount + 1
            else:
                if self.vCount == 0:
                    self.vCount = 1
           
            self.virusAttack()

            lastVirusCount = len(self.activeViruses)
            self.checkViruses()
    
            if len(self.activeViruses) > 0:
                print ""
                print "ACTIVE VIRUSES (%d/%d)" % (len(self.activeViruses), max_viruses)
                for v in self.activeViruses:
                    print "   %s" % (v)
            elif len(self.activeViruses) == 0 and lastVirusCount > 0:
                print ""
                print "NO ACTIVE VIRUSES"
    
            if len(self.activeViruses) >= max_viruses:
                print ""
                print "TOO MANY VIRUS. COMPUTER OVER. YOU LOSE."
                say("TOO MANY VIRUS. COMPUTER OVER. YOU LOSE.")

                self.sendToHacker("END\tHACKER")
                self.stop()
                break

            time.sleep(random.choice(range(2,5)))
    
            now = time.time()
            if startTime + duration < now:
                print ""
                print "TRACE COMPLETE. HACKER IP FOUND. CYBER POLICE NOTIFIED."
                print "SUCCESS!"
                say("TRACE COMPLETE. HACKER IP FOUND. CYBER POLICE NOTIFIED.")
                say("SUCCESS!")

                self.sendToHacker("END\tDEFENDER")
                self.stop()
                break

            else:
                left = duration - (now - startTime) - 1 # (fudge for say)
                if left < 1:
                    say("trace nearly complete!")
                else:
                    say("%d seconds left" % (left))


    def start(self):
        self.intro()
        self.thread = GameThread(self)
        self.thread.daemon = True
        self.thread.start()

        if SINGLE_PLAYER:
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
        GAME.intruderFlag.set()

        GAME.TCPHandler = self

        self.request.send("NAME\t%s" % (GAME.name))
        self.request.send("HOMETOWN\t%s" % (GAME.hometown))
        self.request.send("PIN\t%s" % (GAME.securityPin))

        while not GAME.over:
            hacker_move = self.request.recv(RECV_MAX)

            if hacker_move == "virus":
                GAME.vCount = GAME.vCount + random.choice((1,2))


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":

    random.seed()

    if len(sys.argv) > 1:
        if sys.argv[1] == "single":
            SINGLE_PLAYER = True

    if SINGLE_PLAYER:
        print "# Single Player Mode"
    else:
        print "# Multiplayer Mode"

    clean()

    global GAME
    GAME = Game()
    GAME.start()

    if SINGLE_PLAYER:

        while True:
            time.sleep(0.25)

    else :
        # terminate with Ctrl-C
        server = SimpleServer((getIP(), PORT), SingleTCPHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            GAME.stop()
            sys.exit(0)


