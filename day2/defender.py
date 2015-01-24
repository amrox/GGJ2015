#!/usr/bin/env python

import SocketServer, subprocess, sys 
from threading import Thread
from subprocess import call
import time
import os
import tempfile
import random

DURATION=120
HOST = 'localhost'
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
        'WHERE_DO_WE_GO_FROM_HERE']

VIRUS_LOCS = [
        ('Home', '~'),
        ('Documents', '~/Documents'),
        ('Desktop', '~/Desktop')]


VIRUS_FILES = [
        'open_me!!!111.bat',
        'secret.tmp',
        'word97.exe',
        '69831D88-5CEB-45D7-8A4B-A0708C0FEF1A.mov',
        'HOT_LADIES.xls'
        ]


ACTIVE_VIRUSES = []

def say(msg):
    call(["say", "-v", VOICE, msg])

def openRandomTempDir():
    d = tempfile.mkdtemp()
    msg = HACKER_MSGS[random.choice(range(len(HACKER_MSGS)))]
    call(["touch", os.path.join(d, msg)])
    time.sleep(0.3)
    call(["open", "-a", "Finder", d])


def installVirus():

    while True:

        virusLoc = VIRUS_LOCS[random.choice(range(len(VIRUS_LOCS)))]
        virusDir = os.path.expanduser(virusLoc[1])
        virusFile = VIRUS_FILES[random.choice(range(len(VIRUS_FILES)))]
        virusPath = os.path.join(virusDir, virusFile)

        if virusPath not in ACTIVE_VIRUSES:
            ACTIVE_VIRUSES.append(virusPath)
            break

    call(["touch", virusPath])

    say("virus detected in %s" % (virusLoc[0]))
    if len(ACTIVE_VIRUSES) == 1:
        say("delete it quickly!")

    
def checkViruses():

    global ACTIVE_VIRUSES

    newViruses = []
    a = ACTIVE_VIRUSES

    for v in a:
        if os.path.exists(v):
            newViruses.append(v)

    ACTIVE_VIRUSES = newViruses




def intro():
    time.sleep(0.5)

    for i in range(0, 3):
        print "Scanning..."
        call(["say", "-v", VOICE, "scanning"])
        time.sleep(2)

    print ""
    print ""

    print "*** INTRUDER DETECTED ****"
    print ""
    call(["say", "-v", VOICE, "intruder detected"])
    call(["say", "-v", VOICE, "repeat"])
    call(["say", "-v", VOICE, "intruder detected"])

    time.sleep(0.5)

    print "Starting Countermeasures..."
    call(["say", "-v", VOICE, "starting countermeasures"])

    time.sleep(0.5)

    print "Beginning Trace..."
    call(["say", "-v", VOICE, "beginning trace"])

    time.sleep(0.5)

    print "Trace will complete in 1 minute"
    print ""
    call(["say", "-v", VOICE, "Trace will complete in 1 minutes."])

    time.sleep(1.0)

    print "PREPARE TO DEFEND"
    call(["say", "-v", VOICE, "prepare to defend"])
    call(["say", "-v", VOICE, "-r", "2'", "now"])

    time.sleep(0.5)

def go():

    raw_input("Press Enter to begin.\n\n")


    max_viruses = 5
    duration = 60

    intro()

    startTime = time.time()

    while(True):

        installVirus()
        for i in range(random.choice(range(1, 3))):
            openRandomTempDir()

        checkViruses()

        if len(ACTIVE_VIRUSES) > 0:
            print ""
            print "ACTIVE VIRUSES (%d/%d)" % (len(ACTIVE_VIRUSES), max_viruses)
            for v in ACTIVE_VIRUSES:
                print "   %s" % (v)

        if len(ACTIVE_VIRUSES) == max_viruses:
            print ""
            print "TOO MANY VIRUS. COMPUTER OVER. YOU LOSE."
            say("TOO MANY VIRUS. COMPUTER OVER. YOU LOSE.")
            exit(0)

        time.sleep(random.choice(range(2,5)))

        now = time.time()
        if startTime + duration < now:
            say("TRACE COMPLETE. HACKER IP FOUND. POLICE NOTIFIED.")
            say("SUCCESS!")
            exit(0)
        else:
            left = duration - (now - startTime)
            say("%d seconds left" % (left))



class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."


    def handle(self):
        go()
    

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    print BANNER 
    go()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
