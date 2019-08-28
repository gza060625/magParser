#!/usr/bin/env python

################################################################################
# cpm.receiver.tcp.2.py
# Ian Schofield
# August 22, 2019
#
# USAGE
# ./cpm.receiver.tcp.2.py CMP1
################################################################################

import socket, datetime, optparse, re
import sys
from smallFunctions import *

################################################################################
TCP_IP = "0.0.0.0"
#UDP_PORT = 5632


################################################################################


def parse_args():
	usage = "usage: %prog [ini file]"
	args = optparse.OptionParser(usage)

	_,inargs = args.parse_args()
	if len(inargs) < 1:
		print args.format_help()
		args.exit()
	station = inargs[0]
	return station

def initializeSock(ip,TCP_PORT):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((TCP_IP, TCP_PORT))

	sock.listen(2)
	conn,addr = sock.accept()

	return conn

if __name__ =="__main__":

	station = parse_args()

	ini = '/home/augouser/work/cellpico/'+station+'.ini'
	ini = './'+station+'.ini'

	ip=None
	TCP_PORT=None
	with open(ini, 'rb') as file:
		for line in file.xreadlines():
			#print line
			entry = re.split('=',line[0:len(line)-1])
			if entry[0] == 'ip':
				ip = entry[1]
			elif entry[0] == 'port':
				TCP_PORT = int(entry[1])

	print(ip)
	print(TCP_PORT)	

	conn=initializeSock(ip,TCP_PORT)

	firsttimeFlag=True

	line=""
	while True:
		data = conn.recv(8)  #2048
		
		q=str2Queue(data,q)

		if firsttimeFlag:
			while not q.empty():
				ch=q.get()
				if ch=="\n":
					firsttimeFlag=False

		while not q.empty():
			ch=q.get()
			line=line+ch
			if ch =="\n":
				processLine(line)
				line=""