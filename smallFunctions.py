import Queue
import time
import glob, os,sys

#########################################################################
##### Parameters
#########################################################################
inputPath="" 

outputPath="/home/enson/magParser"
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
    print(line)
    dateStr=line[12]
    timeStr=line[4]
    

    datetime=str2datetime(dateStr,timeStr)
  

    fileHandler=createDateFolder(datetime)
    fileHandler.write(datetime2STR(datetime))
    fileHandler.write("\t".join([x,y,z])+"\n")

    # print(x,y,z,epoch)

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
        
    name=findOutputFileName(datetime.tm_year,datetime.tm_mon,datetime.tm_mday)
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
    print(filePath)     
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
    

    
    