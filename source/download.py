import socket
import math
from structures import FileByteStream, FileChunk, RequestMessage

def openDownloadSocket(targetIp, targetPortNumber):
    print("Opening download socket")
    s = socket.socket()
    s.connect((targetIp, targetPortNumber))
    print(targetIp, targetPortNumber, s)
    return s

def requestPeerData(s):
    try:
        chunkSet = {}
        chunk = s.recv(512)
        print(chunk)

        while chunk:
            print("looping")
            print(chunk)
            print('pass')

            chunk = FileChunk.deserialize(chunk)
            print(chunk)
            chunkSet[chunk.index] = chunk
            chunk = s.recv(512)

        s.close()
        print('return')
        return chunkSet

    except Exception as e:
        print(e)
        s.close()
        return chunkSet

def writeToFile(fileName, chunkData, fileSize):
    with open(fileName, 'wb') as downFile:
        byteStream = []
        print(chunkData)
        for i in range(0, fileSize//256):
            byteStream.append(chunkData[i].data)

        fileToDownload.write(byteStream)

def completeFileRequest(fileName, fileInfo):
    fileSize, fileOwners = fileInfo[0], fileInfo[1]
    # chunk algorithm here
    # get the targetIp, targetPortNumber and chunkSet from algorithm
    chunkSet = [0, 100]
    fileName = "../files/test_2048.txt"
    targetIp = "localhost"
    targetPortNumber = 50001
    s = openDownloadSocket(targetIp, targetPortNumber)
    req = RequestMessage(fileName, chunkSet)
    s.send(req.serialize())

    # put this in while loop
    chunkData = requestPeerData(s)
    s.close()
    writeToFile("../files/received.txt", chunkData, fileSize)