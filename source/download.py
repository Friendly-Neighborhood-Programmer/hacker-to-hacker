import socket
import math
from structures import FileByteStream, FileChunk, RequestMessage
from threading import Lock
import threading

threadFailed = []
threadFailedLock = Lock()
chunkData = {}
chunkDataLock = Lock()

def openDownloadSocket(targetIp, targetPortNumber):
    print("Opening download socket")
    s = socket.socket()
    print(targetIp)
    print(targetPortNumber)

    s.connect((targetIp, targetPortNumber))
    print(targetIp, targetPortNumber, s)
    return s

def requestPeerData(s,chunkRange):
    try:
        chunkSet = {}
        #chunk = s.recv(2048)
        chunk = s.recv(512)
        index = chunkRange[0]
        while chunk:
            #chunk = FileChunk.deserialize(chunk)
            print(chunk)
            #print("index:", chunk.index)
            #chunkSet[chunk.index] = chunk
            chunkSet[index] = chunk
            #chunk = s.recv(2048)
            chunk = s.recv(512)
            print("last",chunk)
            index = index+1

        s.close()
        print('return')
        return chunkSet

    except Exception as e:
        print(e)
        s.close()
        return chunkSet

def writeToFile(fileName, chunkData, fileSize):
    with open(fileName, 'wb') as downFile:
        byteStream = b""
        print(chunkData)
        for i in range(0, math.ceil(fileSize/512)):
            byteStream += chunkData[i]

        downFile.write(byteStream)

def combinedSocket(targetIp,targetPortNumber,fileName,chunkRange,threadID):
    print("will not print")
    s = openDownloadSocket(targetIp, targetPortNumber)
    req = RequestMessage(fileName, chunkRange)
    s.send(req.serialize())
    newData = requestPeerData(s,chunkRange)

    global threadFailedLock
    threadFailedLock.acquire()
    global threadFailed
    threadFailed[threadID] = True
    threadFailedLock.release()

    global chunkDataLock
    chunkDataLock.acquire()
    global chunkData
    chunkData.update(newData)
    chunkDataLock.release()

    s.close()

def completeFileRequest(fileName, fileInfo):
        #File size and owner
    fileSize = fileInfo[0]
    fileOwners = fileInfo[1]

    #Calculate chunk count and chunks per person
    chunkCount = math.ceil(fileSize / 512)
    chunksPerPerson = math.ceil(chunkCount / len(fileOwners))

    #Fill the thread failed array
    global threadFailedLock
    threadFailedLock.acquire()
    global threadFailed
    for i in range(len(fileOwners)):
        threadFailed.append(False)
    threadFailedLock.release()
    
    threadList = []
    currentChunk = 0

    continueLooping = True
    while continueLooping:

        threadFailedLock.acquire()

        #Make sure that we don't go past the chunk count
        upperBoundChunk = currentChunk+chunksPerPerson
        if (upperBoundChunk > chunkCount):
            upperBoundChunk = chunkCount
        
        for i in range(len(fileOwners)):
            
            #If it is the first time create one thread for each
            print("***********************************")
            print(fileOwners)
            print(len(fileOwners))
            fileIP = fileOwners[i][0]
            filePort = fileOwners[i][1]
            chunkRange = (currentChunk,upperBoundChunk)
            if (threadFailed[i] == False) and True not in threadFailed:
                print(i)
                print(fileOwners[i][0])
                print("Passed first")
                print(fileOwners[i][1])
                print("passed second")
                curThread =threading.Thread(target=combinedSocket, args=(fileIP,filePort,fileName,chunkRange,i))
                threadList.append(curThread)
                curThread.start()
            else:
                #Shift all failed threads chunks to the next person in order
                index = i + 1
                if index >= len(fileOwners):
                    index = 0
                threadFailed[index] = False
                curThread = threading.Thread(target=combinedSocket, args=(fileIP,filePort,fileName,chunkRange,index))
                threadList.append(curThread)
                curThread.start()

            #Increase the current chunk
            currentChunk = currentChunk + chunksPerPerson + 1
        threadFailedLock.release()

        #Wait for all threads to finish
        for i in range(len(threadList)):
            threadList[i].join(timeout=10) 

        #Look to see if we continue looping
        threadFailedLock.acquire()
        threadFailed
        if False in threadFailed:
            continueLooping = True
        else:
            continueLooping = False
        threadFailedLock.release()

        #Clear the previous data
        currentChunk = 0
        threadList = []
   

    # put this in while loop
    writeToFile("../files/received.png", chunkData, fileSize)