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
import Queue
import time
import glob, os,sys

from smallFunctions import *

################################################################################
TCP_IP = "0.0.0.0"
iniDict=dict()
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

def initializeSock():
	global iniDict
	ip=iniDict["ip"]
	TCP_PORT=int(iniDict["port"])
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((TCP_IP, TCP_PORT))

	sock.listen(2)
	conn,addr = sock.accept()

	return conn

def initializeIni(station):

	iniPath=os.path.join(iniFileInputPath,station+'.ini')
	return parseINI(iniPath)

if __name__ =="__main__":

	station = parse_args()

	iniDict=initializeIni(station)

	conn=initializeSock()



	firsttimeFlag=2
	line=""
	while True:
		data = conn.recv(8)  #2048
		
		q=str2Queue(data,q)

		if firsttimeFlag:
			while not q.empty():
				ch=q.get()
				if ch=="\n":
					firsttimeFlag=firsttimeFlag-1

		while not q.empty():
			ch=q.get()
			line=line+ch
			if ch =="\n":
				processLine(line)
				line=""