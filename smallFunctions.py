import Queue
import time
import glob, os,sys

#########################################################################
##### Parameters
#########################################################################
inputPath="" 

outputPath="./"
# outputPath=""
#########################################################################

fileHandler=None
q=Queue.Queue()

#########################################################################

def file2String(inputFile):
    f=open(inputFile,"rb")
    q = Queue.Queue()
    #stringBuffer=""
    while True:
        byte=f.read(1)
        if byte:
            #stringBuffer=stringBuffer+byte
            q.put(byte)            
        else:            
            break        
    return q           


#########################################################################
counter=0     
def processLine(line):
    global counter
    print(str(counter)+" "+line)
    counter+=1

def Epoch2STR(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S.000 %j', time.gmtime(epoch))
#########################################################################

def createDateFolder(epoch):
    global fileHandler
    
    date=time.gmtime(epoch)
    folderPath=findOutputPath(date.tm_year,date.tm_mon,date.tm_mday)
    createOutputFolder(folderPath)
    
    if not fileHandler==None:
        fileHandler.close()
        
    name=findOutputFileName(date.tm_year,date.tm_mon,date.tm_mday)
    fileHandler=createOutputFile(folderPath,name)
    
    return fileHandler


def findOutputPath(year,month,day,outputPath=outputPath):    
    return os.path.join(outputPath,str(year),str(month),str(day))

def createOutputFolder(path):  
    if not os.path.exists(path):
        os.makedirs(path)
        print("new")
    else:
        print("old")       
    
def findOutputFileName(year,month,day):    
    return "_".join([str(year),str(month),str(day)])+".txt"

def createOutputFile(folderPath,fileName):     
    filePath=os.path.join(folderPath,fileName)
    fileHandler=open(filePath,"a")      
    return fileHandler

#########################################################################

def str2Queue(string,q):    
    length=len(string)
    for i in string:
        q.put(i)
    return q


#########################################################################
    

if __name__ =="__main__":


    f=createDateFolder(221212)
    
    
    
    f.write("text222222")
    
    f.close()
    

    
    