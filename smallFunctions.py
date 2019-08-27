import queue
import time

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

counter=0        
def processLine(line):
    global counter
    print(str(counter)+" "+line)
    counter+=1

def Epoch2STR(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S.000 %j', time.gmtime(epoch))



if __name__ =="__main__":

    #inputQueue=file2String("input.txt")
    
    #lineBuffer=""
    #while not inputQueue.empty():
        #byte=inputQueue.get()
        #if byte==b'\n':
            #processLine(lineBuffer)
            #lineBuffer=""
        #else:
            #lineBuffer=lineBuffer+byte.decode("utf-8")
            
    
    print(Epoch2STR(1546370162))
    
    #for line in inputFile:
        #print(line)
        
    #while 1:
        #a=inputFile.read(1)
        #if not a:
            #break
        #if a== "\n":
            #print("newLine")
        ##print(a)
    #print("test")