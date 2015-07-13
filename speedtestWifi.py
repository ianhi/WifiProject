import os
import datetime
import time
import urllib.request
import subprocess


def internet_on():
    try:
        response=urllib.request.urlopen('http://www.google.com',timeout=1)
        return True
    except urllib.request.URLError:
        return False    


def timeout_command(command, timeout):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None"""
    import subprocess, datetime, os, time, signal
    start = datetime.datetime.now()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            print("Did not complete within ",timeout,"seconds")
            return None
    out = process.stdout.read() # gives no output when you just return proccess.stdout.read() dunno why
    return out 


def output_data(file_name,results):
#date and time
    t = datetime.datetime.now()
    hour = str(t.hour)
    if t.hour<10:
        hour = '0'+str(t.hour)
    mint = ':'+str(t.minute)
    if t.minute<10:
        mint = ':0'+str(t.minute)
    milTime = hour+mint
    
    day = str((t.weekday()+1)%7) #python uses 0 for monday in previous data sunday is 0
    date = str(t.month)+'/'+str(t.day) + '/'+str(t.year)


#server and latency
    host = results[4][10:results[4].find(' (')]
    location = results[4][results[4].find('(')+1:results[4].find(')')].replace(',',';') 
    latency = results[4][results[4].find(':')+2:results[4].find(' ms')]

#getting Download Speed
    downspeed = results[6][10:15].strip()
    downunits = results[6][15:].strip()

#getting Upload Speed
    upspeed = results[8][7:13].strip()
    upunits = results[8][13:].strip()

#outputting Data
    seq = (date,day,milTime,downspeed,upspeed,location,host,'0',latency,upunits,
                downunits)
    line = ','.join(seq)#assuming wifi
    print(line+'\n')
    output_file = open(file_name,'a+')
    output_file.write('\n')
    output_file.write(line)
    output_file.close()
    


connection = True
t = datetime.datetime.now()
nHours = int(input('Enter an interger number of hours you want to run this for: '))
startT = time.time()
print('starting')
while ((time.time()-startT)//3600)<nHours:
    if internet_on():
        if not connection:
            print("connection restored")
            connection = True
        output = timeout_command("speedtest-cli",120) # arg1 is command arg2 is how long to let run before timeout
        if output == None:
            continue
        results = output.decode(encoding="UTF-8").split('\n') #string split into a list - 2 line for readability
    else:
        if connection:
            print("no internet connection. Will restart on connection restore")
            time.sleep(5000)
        connection = False
        continue
    if len(results)<10:
        print("unexpected output")
        continue
    
    print(results[4],results[6],results[8], sep='\n')
    
    if float(results[6][10:15].strip())== 0:
        output_data("weirdPoints.csv",results)
    output_data("speeddata.csv",results)



