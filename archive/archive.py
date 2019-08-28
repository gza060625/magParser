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