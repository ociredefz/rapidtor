#!/usr/bin/python
#
# rapidtor.py - timedelay id changer in Tor network
# Federico Fazzi <eurialo@deftcode.ninja>
#
# (c) 2014 - MIT License.
#

import os, sys
import socket, signal, time

class RapidTor:

    host = 'localhost'      # server tor host
    port = 9051             # need ControlPort enabled
    passwd = 'torpasswd'    # your tor server password
    delay = 15              # change my identity after 5 secs..
    enable_cache = 1        # 1=enable, 0=disable

    def __init__(self, host = None, port = None, passwd = None, delay = None, enable_cache = None):
        if host is not None:
            self.host = host
            self.port = port
            self.passwd = passwd
            self.delay = delay
            self.enable_cache = enable_cache

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            return True
        except Exception, e:
            sys.stdout.write("%s: %s\n" % (self.host, e))

    def signal_newnym(self):
        sys.stdout.write('Authentication..')
        self.sock.send("AUTHENTICATE \"%s\"\r\n" % self.passwd)
        self.data = self.sock.recv(1024)

        if not self.data.find('250 OK'):
            sys.stdout.write("..SUCCESS!\n")
        else:
            sys.stdout.write("..BAD!\n" + self.data)
            return -1

        while len(self.data):
            sys.stdout.write(">> Changed identity in %d second/s" % self.delay)
            time.sleep(self.delay)
            self.sock.send("SIGNAL NEWNYM\r\n")
            self.data = self.sock.recv(1024)
            
            if self.enable_cache == 1:
                self.signal_cleardnscache()

            sys.stdout.write('..OK!\n')

    def signal_cleardnscache(self):
        self.sock.send("SIGNAL CLEARDNSCACHE\r\n")
        self.data = self.sock.recv(1024)

if __name__ == "__main__":
    rapidtor = RapidTor('localhost', 9051, 'torpasswd', 15, 1)

    if rapidtor.connect() is True:
        rapidtor.signal_newnym()
