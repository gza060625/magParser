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

dayFlag=-1

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
    global counter,fileHandler
    print(str(counter)+" "+line)
    counter+=1

    line=line.split(",")
    x=line[0]
    y=line[1]
    z=line[2]
    epoch=int(line[4])

    print(epoch)

    fileHandler=createDateFolder(epoch)
    fileHandler.write(Epoch2STR(epoch))
    fileHandler.write(",".join([x,y,z])+"\n")

    # print(x,y,z,epoch)



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

    print(path)   
    
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
    

# if __name__ =="__main__":


#     f=createDateFolder(221212)
    
    
    
#     f.write("text222222")
    
#     f.close()
    

    
    