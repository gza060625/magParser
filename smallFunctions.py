import queue
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

#########################################################################

def file2String(inputFile):
    f=open(inputFile,"rb")
    q = queue.Queue()
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
    os.makedirs(path, exist_ok=True)    
    
def findOutputFileName(year,month,day):    
    return "_".join([str(year),str(month),str(day)])+".txt"

def createOutputFile(folderPath,fileName):     
    filePath=os.path.join(folderPath,fileName)
    fileHandler=open(filePath,"a")      
    return fileHandler
    

if __name__ =="__main__":


    f=createDateFolder(221212)
    
    
    
    f.write("text222222")
    
    f.close()
    

    
    