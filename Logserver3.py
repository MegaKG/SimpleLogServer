#!/usr/bin/env python3
import gzip
import ConfigUtils
import TCPstreams5 as tcp
import Logger
import threading
import time
import datetime
import os

#Write Lock
WriteLock = False

def assess(Input,Good,Bad):
    FBad = False
    for i in Bad:
        if i.encode() in Input.lower():
            FBad = True
            break
    
    for i in Good:
        if i.encode() in Input.lower():
            FBad = False
            break

    return FBad


def saveInputLog(Log,Config):
    global WriteLock
    SortBy = Config['By'].lower()

    #Lock the File
    while WriteLock:
        time.sleep(0.1)
    WriteLock = True

    #Determine Type Sort
    Time = datetime.datetime.now()
    ToSort = {
        'year':Time.year,
        'month':Time.month,
        'day':Time.day,
        'hour':Time.hour,
        'minute':Time.minute
    }
    if SortBy not in ToSort:
        SortBy = 'day'
    
    BeforeArray = []
    for i in ToSort:
        if i == SortBy:
            break
        else:
            BeforeArray.append(ToSort[i])

    def prettyprint(IN,Length,Fill='0'):
        while len(IN) < Length:
            IN = '0' + IN
        return IN

    #Calculate Dir Name
    DirName = ""
    for i in BeforeArray:
        DirName += prettyprint(str(i),2) + '.'
    DirName = DirName[:-1]
    
    #Check if it exists
    if not os.path.exists(Config['FileDir'] + '/' + DirName):
        os.mkdir(Config['FileDir'] + '/' + DirName)


    #Open and Write
    file = gzip.open(Config['FileDir'] + '/' + DirName + '/' + str(ToSort[SortBy]) + '.log.gz','ab')
    file.write(Log + b'\n')
    file.close()

    #Check if Error
    if assess(Log,Config['NoTriggers']['NoTerm'],Config['ErrorTriggers']['ErrorTerm']):
        file = gzip.open(Config['FileDir'] + '/' + DirName + '/' + 'Errors.log.gz','ab')
        file.write(Log + b'\n')
        file.close()

    #release the file
    WriteLock = False

def clienthandle(CON,Config):
    while True:
        #Read a Log
        Data = CON.getdat()
        if Data == b'':
            #This represents a dead client
            break
        else:
            #Log the info
            saveInputLog(Data.replace(b'\n',b'').replace(b'\r',b''),Config)

    #Clean Up
    CON.close()


def main(CONFIGF):
    #initialise
    Config = ConfigUtils.complexParseConfig(CONFIGF)
    if type(Config['ErrorTriggers']['ErrorTerm']) != list:
        Config['ErrorTriggers']['ErrorTerm'] = [Config['ErrorTriggers']['ErrorTerm']]
    if type(Config['NoTriggers']['NoTerm']) != list:
        Config['NoTriggers']['NoTerm'] = [Config['NoTriggers']['NoTerm']]
    #print(Config)
    

    try:
        MainLogger = Logger.logger(Config['Logfile'])
    except Exception as E:
        print("Failed Logger")
        return

    #Send the First Log
    MainLogger.log("Loaded Configuration")

    #Establish a server
    ConnectionThreads = {}
    IDcounter = 0
    OpenCounter = 0
    try:
        Server = tcp.newServer(Config['Host'],int(Config['Port']))
        MainLogger.log("Start Server")
    except Exception as E:
        MainLogger.log("Failed to Launch Server")
        return

    def checkdead():
        nonlocal OpenCounter
        nonlocal ConnectionThreads

        tokill = []
        for i in ConnectionThreads:
            if not ConnectionThreads[i].is_alive():
                MainLogger.log("Connection " + str(i) + " Has Disconnected")
                tokill.append(i)
        
        for i in tokill:
            del ConnectionThreads[i]
            OpenCounter -= 1

    #Accept Connections
    while True:
        #Clean the Dead
        checkdead()

        #If we are full, we wait until it is free
        if OpenCounter > int(Config['MaxConns']):
            MainLogger.log("Reached Max Connections")
            while OpenCounter > int(Config['MaxConns']):
                time.sleep(1)
                checkdead()

        #We now Accept a Connection
        NewCon = tcp.serverCon(Server)
        MainLogger.log("Accepted Client " + str(IDcounter))

        #Start the Thread / Client Handler
        ConnectionThreads[IDcounter] = threading.Thread(target=clienthandle,args=(NewCon,Config),name="Handle ID " + str(IDcounter))
        ConnectionThreads[IDcounter].start()
        IDcounter += 1
        OpenCounter += 1







if __name__ == '__main__':
    main("Logserver.conf")
