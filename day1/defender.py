#!/usr/bin/env python

import SocketServer, subprocess, sys 
from threading import Thread

my_unix_command = ['bc']
HOST = 'localhost'
PORT = 2000

hacker_prompt = """
W3hEr D0 w3 g0 fR0m H3r3?

CHOOSE VIRUS
1) DRAGON
2) RHINO
3) SHARK

> """

VIRUSES = ["DRAGON", "RHINO", "SHARK"]


startup =''' 
    ____  ______   ____  ___________________   ______  __________ 
   / __ \/ ____/  / __ \/ ____/ ____/ ____/ | / / __ \/ ____/ __ \\
  / /_/ / /      / / / / __/ / /_  / __/ /  |/ / / / / __/ / /_/ /
 / ____/ /___   / /_/ / /___/ __/ / /___/ /|  / /_/ / /___/ _, _/ 
/_/    \____/  /_____/_____/_/   /_____/_/ |_/_____/_____/_/ |_|  

     ==  Version 2.2.3 Build 17  Copyright AMTech 2015 ==

'''

defender_prompt = """

CHOOSE COUNTERMEASURE
1) FIREWALL
2) LANDSLIDE
3) ICE

> """

COUNTERMEASURES = ["FIREWALL", "LANDSLIDE", "ICE"]

starting_health = 3


results = [[0, -1, 1],
           [1, 0, -1],
           [-1, 1, 0]]


def resolve(hacker_move, defender_move):
    """return 1 if defender wins, -1 if hacker wins, 0 otherwise"""
    return results[hacker_move][defender_move]


def pipe_command(arg_list, standard_input=False):
    "arg_list is [command, arg1, ...], standard_input is string"
    pipe = subprocess.PIPE if standard_input else None
    subp = subprocess.Popen(arg_list, stdin=pipe, stdout=subprocess.PIPE)
    if not standard_input:
        return subp.communicate()[0]
    return subp.communicate(standard_input)[0]

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."


    def handle(self):

        print "*** INTRUDER DETECTED ****"

        defender_health = starting_health
        hacker_health = starting_health

        # self.request is the client connection
        while True:

            self.request.send(hacker_prompt)

            hacker_move = self.request.recv(1024)  # clip input at 1Kb
            hacker_move = int(hacker_move) - 1

            defender_move = input(defender_prompt)
            defender_move = int(defender_move) - 1

            v = resolve(hacker_move, defender_move)
        
            if v == 1:
                msg = "%s > %s" % (COUNTERMEASURES[defender_move], VIRUSES[hacker_move])

                msg = msg + "\n\nDEFENDED & TRACED!"
                hacker_health = hacker_health - 1
            elif v == -1:
                msg = "%s > %s" % (VIRUSES[hacker_move], COUNTERMEASURES[defender_move])
                msg = msg = "\n\nHACKED!"
                defender_health = defender_health - 1
            else:
                msg = "%s == %s" % (COUNTERMEASURES[defender_move], VIRUSES[hacker_move])
                msg = msg = "\n\nDEFENDED!"

            print msg
            self.request.send("\n%s\n" % (msg))

            score_string = "\nHACKER (%d/%d)     DEFENDER (%d/%d)\n" % (hacker_health, starting_health, defender_health, starting_health)

            print score_string
            self.request.send(score_string)

            if hacker_health == 0 or defender_health == 0:
                break

           
            
            #reply = pipe_command(my_unix_command, data)
            #if reply is not None:
            #    self.request.send(reply)
        self.request.close()

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
    print startup
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
