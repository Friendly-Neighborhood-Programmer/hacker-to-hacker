import socket
import math
from structures import FileByteStream, FileChunk, RequestMessage

def openDownloadSocket(targetIp, targetPortNumber):
    print("Opening download socket")
    s = socket.socket()
    s.connect((targetIp, targetPortNumber))
    return s

def requestPeerData(self, s, fileName):
    try:
        chunkSet = {}
        chunk = s.recv(512)

        while chunk:
            chunk = FileChunk.deserialize(chunk)
            chunkSet[chunk.index] = chunk
            chunk = s.recv(512)

        s.close()

    except Exception as e:
        print(e)
        s.close()

def writeToFile(fileName, completeChunkSet, fileSize):
    with open(fileName, 'wb') as downFile:
        byteStream = []
        for i in range(0, math.ceil(fileSize/256)):
            data.append(chunkSet[i].data)

        fileToDownload.write(data)

def completeFileRequest(fileName, fileInfo):
    fileSize, fileOwners = fileInfo[0], fileInfo[1]
    # chunk algorithm here
    # get the targetIp, targetPortNumber and chunkSet from algorithm
    chunkSet = [0, 100]
    fileName = "../files/tosend.png"
    targetIp = "localhost"
    targetPortNumber = 50001
    s = openDownloadSocket(targetIp, targetPortNumber)
    req = RequestMessage(fileName, chunkSet)
    s.send(req.serialize())

    # put this in while loop
    # chunkSet = requestPeerData(s, fileName)
    s.close()
    writeToFile("../files/received.png", chunkSet, fileSize)