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

lastDay=None

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
    global counter,fileHandler,lastDay
    print(str(counter)+" "+line)
    counter+=1

    line=line.split(",")
    x=line[0]
    y=line[1]
    z=line[2]
    # print(line)
    dateStr=line[12]
    timeStr=line[4]
    

    datetime=str2datetime(dateStr,timeStr)
    
    if not lastDay==dateStr:
        fileHandler=createDateFolder(datetime)
        lastDay=dateStr

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

    # print(path)   
    
def findOutputFileName(year,month,day):    
    return "_".join([str(year),str(month),str(day)])+".txt"

def createOutputFile(folderPath,fileName):     
    filePath=os.path.join(folderPath,fileName)
    fileHandler=open(filePath,"a") 
    # print(filePath)     
    return fileHandler

#########################################################################

def str2Queue(string,q):    
    length=len(string)
    for i in string:
        q.put(i)
    return q

def parseINI(iniFile):
    iniHandler=open(iniFile) 
    result=dict()
    for line in iniHandler:
        line=line.split("=",1)
        result[line[0]]=line[1].replace('\n','')
    return result

def padding72(name,content,firstColumn=25,total=72):
    
    lenName=len(name)
    padding=" "*(firstColumn-lenName)
    name=name+padding
    
    nameContent=name+content
    lenNameContent=len(nameContent)
    padding=" "*(total-lenNameContent-1-1)+"|\n"   
   
    return nameContent+padding

def generateTitle(ini):
    fileHandler=open("test.txt",'a')
    titleElementList=["Format","Source of Data","Station Name","IAGA CODE","Geodetic Latitude","Geodetic Longitude","Reported","Sensor Orientation","Elevation","Digital Sampling","Data Interval Type","Data Type"]
    for x in titleElementList:
        print(x,ini[x])
        fileHandler.write(padding72(x,ini[x]))
        
    fileHandler.write("DATE      TIME      DOY     X      Y     Z    H")
#########################################################################
    

if __name__ =="__main__":
    iniDictioanry=parseINI("CPM1.ini")
    generateTitle(iniDictioanry)



    

    
    