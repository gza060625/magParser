def datetime2STR(dateStr,timeStr):
    # result=""
    # year="20"+date[4:6]
    # month=date[2:4]
    # day=date[0:2]  

    # dateStr="-".join([year,month,day]) 

    # hour=time[0:2]
    # minute=time[2:4]
    # second=time[4:6]

    # timeStr=":".join([hour,minute,second])

    # " ".join([dateStr,timeStr])+".000    "
    timeDate=time.strptime(date+time,"%d%m%y%H%M%S")

    return time.strftime('%Y-%m-%d %H:%M:%S.000 %j', time.gmtime(epoch))