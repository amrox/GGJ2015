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
DURATION=120
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
        'YOU_CANT_HIDE',
        'I_WILL_PWN_YOU',
        'WHAT_DO_YOU_DO_NOW']

VIRUS_LOCS = [
        ('Downloads', '~/Downloads'),
        ('Documents', '~/Documents'),
        ('Desktop', '~/Desktop')]


VIRUS_FILES = [
        'open_me!!!111.bat',
        'secret.tmp',
        'word97.exe',
        '69831D88-5CEB-45D7-8A4B-A0708C0FEF1A.mov',
        'HOT_LADIES.xls'
        ]

SAY_ENABLED = True
SINGLE_PLAYER = False

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


def clean():

    for l in VIRUS_LOCS:
        for f in VIRUS_FILES:
            p = os.path.join(
                    os.path.expanduser(l[1]), f)
            call(["rm", "-f", p])


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
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
        self.favoriteColor = None

        self.activeViruses = []

        self.intruderFlag = Event()
        self.stopFlag = Event()

        self.over = False

    def intro(self):
    
        print BANNER 
        
        raw_input("Press Enter to begin.\n\n")
    
        print "Welcome to PC Defender!" 
        say("Welcome to PC Defender.")
        say("Please register to continue.")
        print ""
        self.name = raw_input("Name: [Dork] ") or "Dork\n"
        self.hometown = raw_input("Hometown: [Philly] ") or "Philly\n"
        self.favoriteColor = raw_input("Favorite Color: [Red] ") or "Red\n"
        print ""
    
        print "Now running\n  IP:   %s\n  PORT: %d" % (getIP(), PORT)
        say("Thank you for registering. PC Defender is now running.")
        print ""
        
        time.sleep(0.5)
    

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
    
        print "Trace will complete in 1 minute"
        print ""
        say("Trace will complete in 1 minutes.")
    
        time.sleep(1.0)
        say("Virus locations will be displayed in the console.")
        say("Beware of decoy files.")
        
        time.sleep(0.5)
        print "PREPARE TO DEFEND"
        say("prepare to defend")
        say("now", dur=2)
    
        time.sleep(0.5)
    
        max_viruses = 5
        duration = 60
    
        startTime = time.time()
    
        while not GAME.over:

            if SINGLE_PLAYER:
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
    
            if len(self.activeViruses) == max_viruses:
                print ""
                print "TOO MANY VIRUS. COMPUTER OVER. YOU LOSE."
                say("TOO MANY VIRUS. COMPUTER OVER. YOU LOSE.")
                self.stop()
    
            time.sleep(random.choice(range(2,5)))
    
            now = time.time()
            if startTime + duration < now:
                say("TRACE COMPLETE. HACKER IP FOUND. POLICE NOTIFIED.")
                say("SUCCESS!")
                self.stop()
            else:
                left = duration - (now - startTime)
                say("%d seconds left" % (left))


    def start(self):
        self.intro()
        self.thread = GameThread(self)
        self.thread.start()

    def stop(self):
        self.stopFlag.set()
        self.over = True


    def virusAttack(self):

        self.installVirus()
        for i in range(random.choice(range(1, 3))):
            openRandomTempDir()



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

        self.request.send("NAME\t%s" % (GAME.name))
        self.request.send("HOMETOWN\t%s" % (GAME.hometown))
        self.request.send("COLOR\t%s" % (GAME.favoriteColor))

        while not GAME.over:
            hacker_move = self.request.recv(RECV_MAX)

            if hacker_move == "virus":
                GAME.virusAttack()
        


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":

    clean()

    global GAME
    GAME = Game()
    GAME.start()

    # terminate with Ctrl-C
    server = SimpleServer((getIP(), PORT), SingleTCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        GAME.stop()
        sys.exit(0)


