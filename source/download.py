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
    s = socket.socket()
    s.connect((targetIp, targetPortNumber))
    return s

def requestPeerData(s,chunkRange):
    print("ChunkRangeinPeerData:",chunkRange)
    try:
        chunkSet = {}
        #chunk = s.recv(2048)
        chunk = s.recv(512)
        index = chunkRange[0]
        while chunk and (index<chunkRange[1]):
            #chunk = FileChunk.deserialize(chunk)
            #chunkSet[chunk.index] = chunk
            # if index > chunkRange[1]:
            #    continue
            chunkSet[index] = chunk
            print("index:",index)
            #chunk = s.recv(2048)
            chunk = s.recv(512)
            index = index+1

        s.close()
        return chunkSet

    except Exception as e:
        s.close()
        print("EXCEPTION______________________:",e)
        return chunkSet

def writeToFile(fileName, chunkData, fileSize):
    with open(fileName, 'wb') as downFile:
        byteStream = b""
        
        #print(chunkData)
        for i in range(0, math.ceil(fileSize/512)):
            byteStream += chunkData[i]

        downFile.write(byteStream)

def combinedSocket(targetIp,targetPortNumber,fileName,chunkRange,threadID):
    print("ChunkRangeinCominedSocket:",chunkRange)
    s = openDownloadSocket(targetIp, targetPortNumber)
    req = RequestMessage(fileName, chunkRange)
    s.send(req.serialize())
    newData = requestPeerData(s,chunkRange)
    #print("TargetIP:",targetIp)

    global threadFailedLock
    threadFailedLock.acquire()
    global threadFailed
    threadFailed[threadID] = True
    threadFailedLock.release()

    global chunkDataLock
    chunkDataLock.acquire()
    global chunkData
    chunkData.update(newData)
    with open(f"./logs{threadID}.data", "w") as logs:
        logs.write(str(newData))
        
    chunkDataLock.release()

    s.close()

def completeFileRequest(fileName, fileInfo):
        #File size and owner
    fileSize = fileInfo[0]
    fileOwners = fileInfo[1]

    #Calculate chunk count and chunks per person
    chunkCount = math.ceil(fileSize / 512)
    chunksPerPerson = math.ceil(chunkCount / len(fileOwners))
    print("chunkscount",chunkCount)
    print("chunks per person",chunksPerPerson)
    print("file own",len(fileOwners))

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
        
        for i in range(len(fileOwners)):
              #Make sure that we don't go past the chunk count
            upperBoundChunk = currentChunk+chunksPerPerson
            if (upperBoundChunk > chunkCount):
                upperBoundChunk = chunkCount
            if (currentChunk> chunkCount):
                currentChunk = chunkCount
            #If it is the first time create one thread for each
            fileIP = fileOwners[i][0]
            filePort = fileOwners[i][1]
            chunkRange = (currentChunk,upperBoundChunk)
            print("i:",i)
            print("chunkRange:",chunkRange)
            if (threadFailed[i] == False) and True not in threadFailed:
                curThread =threading.Thread(target=combinedSocket, args=(fileIP,filePort,fileName,chunkRange,i))
                threadList.append(curThread)
                curThread.start()
            else:
                print("((((((((((((((((((((((((((((((((((((((()))))))))))))))))))))))))))))))))))))))")
                #Shift all failed threads chunks to the next person in order
                index = i + 1
                if index >= len(fileOwners):
                    index = 0
                threadFailed[index] = False
                curThread = threading.Thread(target=combinedSocket, args=(fileIP,filePort,fileName,chunkRange,index))
                threadList.append(curThread)
                curThread.start()

            #Increase the current chunk
            currentChunk = currentChunk + chunksPerPerson
            print("Chunks per person")
            print(chunksPerPerson)
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