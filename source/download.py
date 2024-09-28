from structures import FileByteStream, FileChunk
import Math

def openDownloadSocket(targetIp, targetPortNumber, chuckSet):
    s = socket()
    s.connect((targetIp, targetPortNumber))
    s.send(chunckSet)
    return s

def requestPeerData(self, socket, fileName):
    try:
        chunkSet = {}
        chunk = socket.recv(512)

        while chunk:
            chunk = FileChunk.deserialize(chunk)
            chunkSet[chunk.index] = chunk
            chunk = socket.recv(512)

        s.close()

    except Exception as e:
        print(e)
        s.close()

def writeToFile(fileName, completeChunkSet):
    with open(filename, 'wb') as downFile:
        byteStream = []
        for i in range(0, Math.ceil(File.size/File.chunk_size)):
            data.append(chunkSet[i].data)

        fileToDownload.write(data)

def completeFileRequest(fileName, targetIp, targetPortNumber):
    s = openDownloadSocket(targetIp, targetPortNumber, fileName)
    # put this in while loop
    # chunkSet = requestPeerData(s, fileName)
    writeToFile(fileName, chunkSet)

class RequestMessage:
    def __init__(self, file, chunks):
        self.file = file
        self.chunks = chunks