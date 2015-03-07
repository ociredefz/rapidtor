#!/usr/bin/python
#
# Copyright (C) 2012-2015 Federico Fazzi - http://deftcode.ninja
# rapidtor.py - timedelay id changer in Tor network
#
# First generate hashed control password:
# deftcode ~ $ tor --quiet --hash-password torpasswd
# 16:C9B4152185E88628607DE42FA83F01801BD332C8D91ACC6B29CC863F4A
# 
# Edit ~/.torrc configuration file and uncomment these lines
# then change the HashedControlPassword with previously generated:
# --
# RunAsDaemon 1
# ControlPort 9051
# HashedControlPassword 16:C9B4152185E88628607DE42FA83F01801BD332C8D91ACC6B29CC863F4A
# --
#
# Force tor daemon to use your custom configuration file:
# deftcode ~ $ tor --quiet -f ~/.torrc
# Mar 07 09:46:12.543 [notice] Tor v0.2.4.20 (git-0d50b03673670de6).
# Mar 07 09:46:12.543 [notice] Read configuration file "/home/eurialo/.torrc".
# Mar 07 09:46:12.550 [notice] Opening Socks listener on 127.0.0.1:9050
# Mar 07 09:46:12.550 [notice] Opening Control listener on 127.0.0.1:9051
# Mar 07 09:46:12.550 [notice] Opening OR listener on 0.0.0.0:9001
#
# deftcode ~ $ python rapidtor.py
# Authentication....OK!
# >> Changed identity in 5 second/s..OK!
# >> Changed identity in 5 second/s..OK!
# >> Changed identity in 5 second/s..OK!
# ..

import os, sys
import socket, signal, time

class RapidTor:

	host = 'localhost'		# server tor host
	port = 9051				# need ControlPort enabled
	passwd = 'torpasswd'	# your tor server password
	delay = 15				# change my identity after 5 secs..
	enable_cache = 1 		# 1=enable, 0=disable

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
