#!/usr/bin/env python

################################################################################
# cpm.receiver.tcp.2.py
# Ian Schofield
# August 22, 2019
#
# USAGE
# ./cpm.receiver.tcp.2.py CMP1
################################################################################
##### Parameters
################################################################################
iniFileInputPath="./" 

outputPath="./"
# outputPath="/autumndp/L0"
TCP_IP = "0.0.0.0"

################################################################################
import glob, os,sys
import socket, datetime, optparse, re
import Queue
import time

################################################################################
##### Global
################################################################################
fileHandler=None
q=Queue.Queue()
lastDay="-1"

iniDict=dict()
################################################################################
def processLine(line):
    global fileHandler,lastDay 

    line=line.split(",")
    x=line[0]
    y=line[1]
    z=line[2]
    H="FFFFFF"
    # print(line)
    dateStr=line[12]
    timeStr=line[4]    

    datetime=str2datetime(dateStr,timeStr)
    
    if not lastDay==dateStr:
        fileHandler=createDateFolder(datetime)
        lastDay=dateStr

    fileHandler.write(datetime2STR(datetime))
    fileHandler.write("\t".join([x,y,z,H])+"\n")

#########################################################################
def str2datetime(dateStr,timeStr):
    return time.strptime(dateStr+timeStr,"%d%m%y%H%M%S")     

def datetime2STR(datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S.000 %j\t', datetime)
#########################################################################

def createDateFolder(datetime):
    global fileHandler    
    
    folderPath=findOutputPath(datetime.tm_year,datetime.tm_mon,datetime.tm_mday)
    createOutputFolder(folderPath)
    
    if not fileHandler==None:
        fileHandler.close()
        
    name=findOutputFileName(datetime)
    fileHandler=createOutputFile(folderPath,name)
    
    return fileHandler


def findOutputPath(year,month,day,outputPath=outputPath): 
    global iniDict   
    return os.path.join(outputPath,iniDict["IAGA CODE"],str(year),str(month),str(day))

def createOutputFolder(path):  
    if not os.path.exists(path):
        os.makedirs(path)  
    return path
  
    
def findOutputFileName(datetime):
    global iniDict
    timestamp=time.strftime('%y%m%d', datetime)
    
    return ".".join(["L0",iniDict["Instrument Type"],iniDict["IAGA CODE"],iniDict["ISO Cadence"],timestamp,".txt"])

def createOutputFile(folderPath,fileName):  
    global iniDict   
    filePath=os.path.join(folderPath,fileName)

    fileExistsFlag=False
    if os.path.exists(filePath):
        fileExistsFlag=True

    fileHandler=open(filePath,"a") 

    if not fileExistsFlag:
        # ini=parseINI("CPM1.ini")
        generateTitle(iniDict,fileHandler)
        print("here")
    
   
    return fileHandler

#########################################################################

def str2Queue(string,q):    
    length=len(string)
    for i in string:
        q.put(i)
    return q

def parseINI(iniFile):
    global iniDict
    iniHandler=open(iniFile) 
    result=dict()
    for line in iniHandler:
        line=line.split("=",1)
        result[line[0]]=line[1].rstrip()
    iniDict=result
    # print(iniDict)
    return result
    # return result

def padding72(name,content,firstColumn=25,total=72):
    
    lenName=len(name)
    padding=" "*(firstColumn-lenName)
    name=name+padding
    
    nameContent=(name+content)
    lenNameContent=len(nameContent)
    padding=" "*(total-lenNameContent-1-1)+"|\n"   
    result=nameContent+padding
    return result

def generateTitle(ini,fileHandler):   
    titleElementList=["Format","Source of Data","Station Name","IAGA CODE","Geodetic Latitude","Geodetic Longitude","Reported","Sensor Orientation","Elevation","Digital Sampling","Data Interval Type","Data Type"]
    for x in titleElementList:      
        fileHandler.write(padding72(x,ini[x]))
        
    fileHandler.write("DATE       TIME         DOY     X       Y       Z       H\n")

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